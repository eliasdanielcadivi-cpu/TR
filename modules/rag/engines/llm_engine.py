#!/usr/bin/env python3
"""
Motor de razonamiento LLM (T4).

Razonamiento profundo con Chain-of-Thought usando LLMs locales (Ollama)
y API fallback (DeepSeek). Implementa el tier de razonamiento profundo T4.
"""

import os
import json
import time
import logging
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
from dataclasses import dataclass, asdict
from enum import Enum
import threading

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Proveedores de LLM soportados."""
    OLLAMA_LOCAL = "ollama"
    DEEPSEEK_API = "deepseek"
    OPENAI_API = "openai"


class ReasoningStep(Enum):
    """Pasos en el proceso de razonamiento."""
    ANALYZE_QUERY = "analyze_query"
    EXTRACT_CONTEXT = "extract_context"
    FORMULATE_HYPOTHESES = "formulate_hypotheses"
    EVALUATE_EVIDENCE = "evaluate_evidence"
    SYNTHESIZE_ANSWER = "synthesize_answer"
    VERIFY_CONFIDENCE = "verify_confidence"


@dataclass
class ReasoningContext:
    """Contexto completo para razonamiento T4."""
    original_query: str
    t3_partial_data: Optional[Dict[str, Any]]
    session_project: Optional[str]
    available_entities: List[str]
    suggested_reasoning_path: str
    user_constraints: Optional[Dict[str, Any]] = None
    max_token_limit: int = 4096


@dataclass
class ReasoningStepResult:
    """Resultado de un paso de razonamiento."""
    step: ReasoningStep
    content: str
    confidence: float
    metadata: Dict[str, Any] = None


@dataclass
class LLMReasoningResult:
    """Resultado final del razonamiento T4."""
    answer: str
    confidence: float
    reasoning_steps: List[ReasoningStepResult]
    sources_cited: List[Dict[str, Any]]
    latency_ms: float
    provider_used: str
    token_usage: Optional[Dict[str, int]] = None


class LLMEngine:
    """
    Motor de razonamiento profundo T4.

    Características:
    - Chain-of-Thought estructurado
    - Multi-proveedor (Ollama local prioritario, API fallback)
    - Streaming de progreso
    - Gestión de contexto y tokens
    - Validación de confianza
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.t4_config = config.get('t4', {})
        self.embeddings_config = config.get('embeddings', {})

        # Configuración de modelos
        self.model_local = self.t4_config.get('model_local', 'gemma3:4b')
        self.model_api = self.t4_config.get('model_api', 'deepseek-chat')
        self.api_key_env = self.t4_config.get('api_key_env', 'DEEPSEEK_API_KEY')
        self.max_tokens = self.t4_config.get('max_tokens', 4096)
        self.temperature = self.t4_config.get('temperature', 0.3)

        # Estado
        self.preferred_provider = LLMProvider.OLLAMA_LOCAL
        self._provider_status = {}
        self._test_providers()

    def _test_providers(self):
        """Testear disponibilidad de proveedores."""
        logger.info("Probando disponibilidad de proveedores LLM...")

        # Test Ollama
        if self._test_ollama():
            self._provider_status[LLMProvider.OLLAMA_LOCAL] = True
            logger.info("✅ Ollama local disponible")
        else:
            self._provider_status[LLMProvider.OLLAMA_LOCAL] = False
            logger.warning("❌ Ollama local no disponible")

        # Test DeepSeek API
        if self._test_deepseek_api():
            self._provider_status[LLMProvider.DEEPSEEK_API] = True
            logger.info("✅ DeepSeek API disponible")
        else:
            self._provider_status[LLMProvider.DEEPSEEK_API] = False
            logger.warning("❌ DeepSeek API no disponible")

    def _test_ollama(self) -> bool:
        """Verificar si Ollama está corriendo localmente."""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def _test_deepseek_api(self) -> bool:
        """Verificar si la API key de DeepSeek está configurada."""
        api_key = os.environ.get(self.api_key_env)
        return bool(api_key)

    def reason(self, context: ReasoningContext,
              stream_callback: Optional[callable] = None) -> LLMReasoningResult:
        """
        Proceso principal de razonamiento T4.

        Args:
            context: Contexto completo para razonamiento
            stream_callback: Función para streaming de progreso (opcional)

        Returns:
            Resultado del razonamiento con respuesta, confianza y pasos
        """
        start_time = time.time()

        try:
            # Seleccionar proveedor
            provider = self._select_provider()
            if not provider:
                raise RuntimeError("No hay proveedores LLM disponibles")

            # Construir prompt estructurado
            system_prompt, user_prompt = self._build_structured_prompt(context)

            # Notificar inicio
            if stream_callback:
                stream_callback({
                    'stage': 'starting',
                    'provider': provider.value,
                    'model': self._get_model_for_provider(provider)
                })

            # Ejecutar razonamiento
            if stream_callback:
                result = self._reason_with_streaming(
                    provider, system_prompt, user_prompt, context, stream_callback
                )
            else:
                result = self._reason_without_streaming(
                    provider, system_prompt, user_prompt, context
                )

            # Calcular latencia
            result.latency_ms = (time.time() - start_time) * 1000
            result.provider_used = provider.value

            # Validar confianza
            if result.confidence < 0.6:
                logger.warning(f"Razonamiento T4 con baja confianza: {result.confidence}")

            # Notificar finalización
            if stream_callback:
                stream_callback({
                    'stage': 'complete',
                    'confidence': result.confidence,
                    'latency_ms': result.latency_ms
                })

            return result

        except Exception as e:
            logger.error(f"Error en razonamiento T4: {e}", exc_info=True)
            # Fallback a respuesta básica
            return self._create_fallback_result(context, start_time)

    def _select_provider(self) -> Optional[LLMProvider]:
        """Seleccionar proveedor LLM basado en disponibilidad y preferencias."""
        # Prioridad: Ollama local > DeepSeek API
        if self._provider_status.get(LLMProvider.OLLAMA_LOCAL, False):
            return LLMProvider.OLLAMA_LOCAL
        elif self._provider_status.get(LLMProvider.DEEPSEEK_API, False):
            return LLMProvider.DEEPSEEK_API
        else:
            return None

    def _get_model_for_provider(self, provider: LLMProvider) -> str:
        """Obtener nombre del modelo para el proveedor."""
        if provider == LLMProvider.OLLAMA_LOCAL:
            return self.model_local
        elif provider == LLMProvider.DEEPSEEK_API:
            return self.model_api
        else:
            return "unknown"

    def _build_structured_prompt(self, context: ReasoningContext) -> tuple:
        """Construir prompt estructurado para Chain-of-Thought."""
        # Prompt del sistema (instrucciones de razonamiento)
        system_prompt = f"""Eres un asistente especializado en razonamiento profundo para el sistema ARES.

CONTEXTO DEL PROYECTO: {context.session_project or 'No especificado'}

INSTRUCCIONES DE RAZONAMIENTO:
1. Analiza la consulta paso a paso
2. Extrae y evalúa la evidencia disponible
3. Formula hipótesis basadas en el contexto
4. Evalúa cada hipótesis con criterio crítico
5. Sintetiza una respuesta bien fundamentada
6. Asigna un nivel de confianza (0.0-1.0) basado en la evidencia

FORMATO DE RESPUESTA:
Debes usar JSON con la siguiente estructura:
{{
  "reasoning_steps": [
    {{"step": "ANALYZE_QUERY", "content": "...", "confidence": 0.0}},
    {{"step": "EXTRACT_CONTEXT", "content": "...", "confidence": 0.0}},
    {{"step": "FORMULATE_HYPOTHESES", "content": "...", "confidence": 0.0}},
    {{"step": "EVALUATE_EVIDENCE", "content": "...", "confidence": 0.0}},
    {{"step": "SYNTHESIZE_ANSWER", "content": "...", "confidence": 0.0}}
  ],
  "final_answer": "...",
  "overall_confidence": 0.0,
  "sources_cited": []
}}

ENTIDADES DISPONIBLES: {', '.join(context.available_entities[:20])}
"""

        # Prompt del usuario (consulta + contexto)
        user_context = ""
        if context.t3_partial_data:
            user_context += f"\nINFORMACIÓN PREVIA (T3): {json.dumps(context.t3_partial_data, indent=2, ensure_ascii=False)[:1500]}"

        user_prompt = f"""CONSULTA ORIGINAL: {context.original_query}
{user_context}

CAMINO SUGERIDO: {context.suggested_reasoning_path}

Realiza un análisis profundo paso a paso. Responde solo con el JSON especificado."""

        return system_prompt, user_prompt

    def _reason_without_streaming(self, provider: LLMProvider,
                                system_prompt: str, user_prompt: str,
                                context: ReasoningContext) -> LLMReasoningResult:
        """Razonamiento sin streaming (síncrono)."""
        try:
            if provider == LLMProvider.OLLAMA_LOCAL:
                response = self._call_ollama(system_prompt, user_prompt)
            elif provider == LLMProvider.DEEPSEEK_API:
                response = self._call_deepseek_api(system_prompt, user_prompt)
            else:
                raise ValueError(f"Proveedor no soportado: {provider}")

            # Parsear respuesta JSON
            result_data = self._parse_llm_response(response)

            # Convertir a LLMReasoningResult
            return self._create_result_from_parsed_data(result_data, context)

        except Exception as e:
            logger.error(f"Error en razonamiento con {provider}: {e}")
            raise

    def _reason_with_streaming(self, provider: LLMProvider,
                             system_prompt: str, user_prompt: str,
                             context: ReasoningContext,
                             stream_callback: callable) -> LLMReasoningResult:
        """Razonamiento con streaming de progreso."""
        # Para streaming, implementamos un enfoque simplificado
        # En producción, usaríamos streaming real de la API

        # Notificar inicio de cada paso
        steps = [
            ReasoningStep.ANALYZE_QUERY,
            ReasoningStep.EXTRACT_CONTEXT,
            ReasoningStep.FORMULATE_HYPOTHESES,
            ReasoningStep.EVALUATE_EVIDENCE,
            ReasoningStep.SYNTHESIZE_ANSWER
        ]

        collected_steps = []

        for step in steps:
            if stream_callback:
                stream_callback({
                    'stage': 'step_start',
                    'step': step.value,
                    'progress': steps.index(step) / len(steps)
                })

            # Simular procesamiento del paso
            time.sleep(0.5)  # Para demostración

            # Crear resultado del paso (en producción esto vendría del LLM)
            step_result = ReasoningStepResult(
                step=step,
                content=f"Procesamiento de {step.value} completado",
                confidence=0.7 + (steps.index(step) * 0.05)
            )
            collected_steps.append(step_result)

            if stream_callback:
                stream_callback({
                    'stage': 'step_complete',
                    'step': step.value,
                    'result': asdict(step_result)
                })

        # Llamada real al LLM (sin streaming para simplificar)
        try:
            if provider == LLMProvider.OLLAMA_LOCAL:
                response = self._call_ollama(system_prompt, user_prompt)
            elif provider == LLMProvider.DEEPSEEK_API:
                response = self._call_deepseek_api(system_prompt, user_prompt)
            else:
                response = '{"final_answer": "Proveedor no disponible", "overall_confidence": 0.5}'

            result_data = self._parse_llm_response(response)

            # Combinar con pasos simulados
            result = self._create_result_from_parsed_data(result_data, context)
            result.reasoning_steps = collected_steps

            return result

        except Exception as e:
            logger.error(f"Error en razonamiento con streaming: {e}")
            # Fallback con pasos simulados
            return LLMReasoningResult(
                answer="Error en razonamiento profundo. Usando análisis simplificado.",
                confidence=0.5,
                reasoning_steps=collected_steps,
                sources_cited=[],
                latency_ms=0,
                provider_used=provider.value
            )

    def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Llamar a Ollama local."""
        try:
            import requests

            url = "http://localhost:11434/api/generate"
            payload = {
                "model": self.model_local,
                "system": system_prompt,
                "prompt": user_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }

            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except Exception as e:
            logger.error(f"Error llamando a Ollama: {e}")
            raise

    def _call_deepseek_api(self, system_prompt: str, user_prompt: str) -> str:
        """Llamar a DeepSeek API."""
        try:
            import requests

            api_key = os.environ.get(self.api_key_env)
            if not api_key:
                raise ValueError(f"API key no encontrada en variable {self.api_key_env}")

            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            payload = {
                "model": self.model_api,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }

            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"Error llamando a DeepSeek API: {e}")
            raise

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parsear respuesta JSON del LLM."""
        try:
            # Intentar extraer JSON de la respuesta
            # Algunos LLMs agregan texto alrededor del JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback: respuesta simple
                logger.warning("No se pudo extraer JSON de la respuesta LLM")
                return {
                    "final_answer": response[:1000],
                    "overall_confidence": 0.7,
                    "reasoning_steps": [],
                    "sources_cited": []
                }
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON de LLM: {e}")
            return {
                "final_answer": f"Error parseando respuesta: {str(e)[:200]}",
                "overall_confidence": 0.3,
                "reasoning_steps": [],
                "sources_cited": []
            }

    def _create_result_from_parsed_data(self, data: Dict[str, Any],
                                      context: ReasoningContext) -> LLMReasoningResult:
        """Crear LLMReasoningResult a partir de datos parseados."""
        # Convertir reasoning_steps
        reasoning_steps = []
        for step_data in data.get("reasoning_steps", []):
            try:
                step = ReasoningStepResult(
                    step=ReasoningStep(step_data.get("step", "ANALYZE_QUERY")),
                    content=step_data.get("content", ""),
                    confidence=float(step_data.get("confidence", 0.5)),
                    metadata=step_data.get("metadata", {})
                )
                reasoning_steps.append(step)
            except Exception as e:
                logger.warning(f"Error procesando reasoning step: {e}")

        return LLMReasoningResult(
            answer=data.get("final_answer", "No se generó respuesta"),
            confidence=float(data.get("overall_confidence", 0.5)),
            reasoning_steps=reasoning_steps,
            sources_cited=data.get("sources_cited", []),
            latency_ms=0,  # Se calculará después
            provider_used="unknown",
            token_usage=data.get("token_usage")
        )

    def _create_fallback_result(self, context: ReasoningContext,
                              start_time: float) -> LLMReasoningResult:
        """Crear resultado de fallback cuando el razonamiento falla."""
        elapsed_ms = (time.time() - start_time) * 1000

        # Respuesta de fallback simple
        answer = f"""
No se pudo realizar un análisis profundo completo debido a limitaciones técnicas.

Consulta: {context.original_query}

Contexto disponible: {len(context.available_entities)} entidades relacionadas.

Sugerencia: Intenta reformular la consulta o usar información más específica.
"""

        return LLMReasoningResult(
            answer=answer.strip(),
            confidence=0.3,
            reasoning_steps=[
                ReasoningStepResult(
                    step=ReasoningStep.ANALYZE_QUERY,
                    content="Fallback por error técnico",
                    confidence=0.3
                )
            ],
            sources_cited=[],
            latency_ms=elapsed_ms,
            provider_used="fallback"
        )

    async def reason_async(self, context: ReasoningContext,
                         stream_callback: Optional[callable] = None) -> LLMReasoningResult:
        """Versión asíncrona del razonamiento."""
        # Implementación async simple (wrapper sobre síncrono)
        loop = asyncio.get_event_loop()

        def run_sync():
            return self.reason(context, stream_callback)

        return await loop.run_in_executor(None, run_sync)

    def get_status(self) -> Dict[str, Any]:
        """Obtener estado del motor LLM."""
        return {
            'preferred_provider': self.preferred_provider.value,
            'provider_status': {
                provider.value: status
                for provider, status in self._provider_status.items()
            },
            'model_local': self.model_local,
            'model_api': self.model_api,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }
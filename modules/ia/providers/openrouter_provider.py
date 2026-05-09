"""OpenRouterProvider: Placeholder para futura integración OpenRouter.

OpenRouter (https://openrouter.ai) permite acceso a múltiples modelos
de IA mediante una API unificada.

NOTA: Este módulo es un placeholder. La implementación real requiere:
- API key de OpenRouter
- Configuración de modelos disponibles
- Manejo específico de la API

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import os
import requests
import json
from typing import Dict, Any, List, Optional

from .base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):
    """Provider para OpenRouter API.
    
    Permite acceso a múltiples modelos mediante la API unificada de OpenRouter.
    """

    def __init__(self, config: Dict[str, Any]):
        """Inicializar OpenRouterProvider.
        
        Args:
            config: Configuración con base_url, model, api_key_env.
        """
        super().__init__(config)
        self.base_url = config.get("base_url", "https://openrouter.ai/api/v1")
        self.default_model = config.get("model", "google/gemma-2-9b-it")
        self.api_key_env = config.get("api_key_env", "OPENROUTER-API-KEY")
        self.api_key = os.getenv(self.api_key_env)
        self._initialized = self.validate_config()

    def generate(self, prompt: str, **kwargs) -> str:
        """Generar respuesta usando API de OpenRouter.
        
        Args:
            prompt: Prompt de entrada.
            **kwargs: model, temperature, max_tokens, etc.
            
        Returns:
            Respuesta generada por OpenRouter.
        """
        model = kwargs.get("model", self.default_model)
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 2048)

        messages = [{"role": "user", "content": prompt}]
        
        return self._chat_completion(messages, model, temperature, max_tokens)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generar respuesta en modo chat.
        
        Args:
            messages: Lista de mensajes con rol y contenido.
            **kwargs: model, temperature, max_tokens, etc.
            
        Returns:
            Respuesta del asistente.
        """
        model = kwargs.get("model", self.default_model)
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 2048)
        
        return self._chat_completion(messages, model, temperature, max_tokens)

    def list_models(self) -> List[str]:
        """Listar modelos OpenRouter (hardcoded por ahora)."""
        return [
            "google/gemma-2-9b-it",
            "deepseek/deepseek-chat",
            "meta-llama/llama-3-8b-instruct",
            "anthropic/claude-3-haiku",
        ]

    def validate_config(self) -> bool:
        """Validar configuración y API key.
        
        Returns:
            True si API key está configurada.
        """
        return bool(self.api_key)

    def _chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Llamada a API de OpenRouter chat completions."""
        if not self.api_key:
            return "Error: API key de OpenRouter no configurada (OPENROUTER-API-KEY)"

        # Asegurar que la URL sea correcta
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://ares-tron.local",
            "X-Title": "ARES-TRON",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            # Depuración silenciosa
            # print(f"DEBUG: Calling OpenRouter: {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            
            if response.status_code != 200:
                return f"Error OpenRouter API: {response.status_code} - {response.text}"
            
            result = response.json()
            choices = result.get("choices", [])
            
            if choices:
                return choices[0]["message"]["content"]
            return "Error: Sin respuesta de OpenRouter"
            
        except requests.exceptions.RequestException as e:
            return f"Error OpenRouter API: {str(e)}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"Error procesando respuesta: {str(e)}"

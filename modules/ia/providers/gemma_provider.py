"""GemmaProvider: Módulo independiente para modelos Gemma vía Ollama.

Este módulo es autocontenido y puede ser modificado sin afectar el resto de ARES.
Soporta:
- Modelos: gemma3:1b, gemma3:4b, gemma3:12b, gemma3:27b
- Templates de prompt optimizados
- Function calling con salida JSON estructurada
- Parámetros de generación configurables
- Obtención automática de plantilla nativa desde Ollama API

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import requests
import json
from typing import Dict, Any, List, Optional

from .base_provider import BaseProvider


class GemmaProvider(BaseProvider):
    """Provider para modelos Google Gemma vía Ollama.
    
    Módulo independiente que encapsula toda la lógica de comunicación
    con Ollama para modelos Gemma.
    """

    # Templates por defecto (fallback si no se puede obtener de Ollama)
    DEFAULT_GEMMA_CHAT_TEMPLATE = "<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
    DEFAULT_GEMMA_SYSTEM_TEMPLATE = "<start_of_turn>system\n{system}<end_of_turn>\n<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"

    def __init__(self, config: Dict[str, Any]):
        """Inicializar GemmaProvider.
        
        Args:
            config: Configuración con base_url, model default, templates.
        """
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.default_model = config.get("model", "gemma3:4b")
        self.templates = config.get("templates", {})
        self._model_cache: Dict[str, Dict[str, Any]] = {}
        self._initialized = self.validate_config()

    def generate(self, prompt: str, **kwargs) -> str:
        """Generar respuesta usando API /api/generate de Ollama.
        
        Args:
            prompt: Prompt de entrada.
            **kwargs: model, template, stream, temperature, etc.
            
        Returns:
            Respuesta generada por el modelo Gemma.
        """
        model = kwargs.get("model", self.default_model)
        template_name = kwargs.get("template")
        stream = kwargs.get("stream", False)
        options = kwargs.get("options", {})

        # Obtener plantilla nativa del modelo si no se especifica template
        if not template_name:
            model_info = self._get_model_info(model)
            native_template = model_info.get("template")
            if native_template:
                # Usar la plantilla nativa directamente con Ollama
                # Ollama maneja el formateo internamente
                pass  # No aplicamos template manualmente, Ollama lo hace
            # Si no hay template nativo, usamos fallback
        else:
            # Usar plantilla YAML específica
            prompt = self._load_template(template_name, prompt)

        # Fusionar opciones con parámetros del modelo
        model_options = self._get_model_options(model)
        if model_options:
            for key, value in model_options.items():
                if key not in options:
                    options[key] = value

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": options
        }

        url = f"{self.base_url}/api/generate"
        
        try:
            # Timeout más largo para carga de modelo (5 minutos)
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            if stream:
                return self._parse_stream(response)
            else:
                result = response.json()
                return result.get("response", "Error: Sin respuesta.")
                
        except requests.exceptions.Timeout:
            return f"Error: Timeout - El modelo '{model}' está tardando en cargar. Intenta nuevamente o usa un modelo más pequeño."
        except requests.exceptions.RequestException as e:
            return f"Error Ollama/Gemma: {str(e)}"
        except json.JSONDecodeError as e:
            return f"Error JSON: {str(e)}"

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generar respuesta en modo chat usando API /api/chat.
        
        Args:
            messages: Lista de mensajes con rol (system/user/assistant).
            **kwargs: model, tools, stream, temperature, etc.
            
        Returns:
            Respuesta del asistente.
        """
        model = kwargs.get("model", self.default_model)
        stream = kwargs.get("stream", False)
        tools = kwargs.get("tools")
        options = kwargs.get("options", {})

        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": options
        }

        if tools:
            payload["tools"] = tools

        url = f"{self.base_url}/api/chat"
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            if stream:
                return self._parse_chat_stream(response)
            else:
                result = response.json()
                return result.get("message", {}).get("content", "Error: Sin respuesta.")
                
        except requests.exceptions.RequestException as e:
            return f"Error Ollama/Gemma Chat: {str(e)}"
        except json.JSONDecodeError as e:
            return f"Error JSON: {str(e)}"

    def list_models(self) -> List[str]:
        """Listar todos los modelos disponibles en Ollama.

        Returns:
            Lista de todos los modelos Ollama disponibles.
        """
        url = f"{self.base_url}/api/tags"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            result = response.json()

            models = result.get("models", [])
            # Retornar TODOS los modelos, no solo Gemma
            all_models = [m["name"] for m in models]

            return all_models if all_models else ["gemma3:4b", "gemma3:12b"]

        except requests.exceptions.RequestException:
            return ["gemma3:4b", "gemma3:12b", "gemma3:1b"]

    def validate_config(self) -> bool:
        """Validar conexión con Ollama.
        
        Returns:
            True si Ollama está accesible.
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _get_model_info(self, model: str) -> Dict[str, Any]:
        """Obtener información del modelo desde Ollama API.
        
        Args:
            model: Nombre del modelo.
            
        Returns:
            Diccionario con template, parameters, etc.
        """
        # Verificar caché
        if model in self._model_cache:
            return self._model_cache[model]
        
        # Obtener desde API
        try:
            url = f"{self.base_url}/api/show"
            response = requests.post(url, json={"model": model}, timeout=30)
            response.raise_for_status()
            
            info = response.json()
            self._model_cache[model] = info
            return info
            
        except requests.exceptions.RequestException:
            return {}

    def _get_model_options(self, model: str) -> Dict[str, Any]:
        """Obtener parámetros por defecto del modelo.
        
        Args:
            model: Nombre del modelo.
            
        Returns:
            Diccionario con parámetros (temperature, top_p, top_k, etc.).
        """
        info = self._get_model_info(model)
        params_str = info.get("parameters", "")
        
        options = {}
        if params_str:
            for line in params_str.strip().split("\n"):
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    key, value = parts
                    key = key.lower()
                    # Convertir valores
                    if key in ("temperature", "top_p", "repeat_penalty"):
                        try:
                            options[key] = float(value)
                        except ValueError:
                            pass
                    elif key in ("top_k", "num_predict", "num_keep"):
                        try:
                            options[key] = int(value)
                        except ValueError:
                            pass
                    elif key == "stop":
                        # Limpiar comillas
                        options["stop"] = [value.strip('"')]
        
        return options

    def _apply_native_template(self, template: str, prompt: str) -> str:
        """Aplicar plantilla nativa del modelo.
        
        Args:
            template: Plantilla nativa de Ollama.
            prompt: Prompt del usuario.
            
        Returns:
            Prompt formateado.
        """
        # Plantillas de Ollama usan sintaxis Go template
        # Para uso simple, reemplazamos placeholders básicos
        try:
            # Reemplazo simple para templates básicos
            if "{{ .Prompt }}" in template:
                return template.replace("{{ .Prompt }}", prompt)
            elif "{prompt}" in template:
                return template.format(prompt=prompt)
            else:
                # Fallback: usar template genérico
                return f"{template}\n{prompt}"
        except (KeyError, ValueError):
            return prompt

    def _apply_gemma_template(self, prompt: str, system: Optional[str] = None) -> str:
        """Aplicar formato de template Gemma 3 (fallback).
        
        Args:
            prompt: Prompt del usuario.
            system: Mensaje de sistema opcional.
            
        Returns:
            Prompt formateado para Gemma 3.
        """
        if system:
            return self.DEFAULT_GEMMA_SYSTEM_TEMPLATE.format(system=system, prompt=prompt)
        return self.DEFAULT_GEMMA_CHAT_TEMPLATE.format(prompt=prompt)

    def _load_template(self, template_name: str, prompt: str) -> str:
        """Cargar plantilla desde configuración.
        
        Args:
            template_name: Nombre de la plantilla.
            prompt: Prompt para insertar.
            
        Returns:
            Plantilla procesada o prompt original.
        """
        template = self.templates.get(template_name, "{prompt}")
        try:
            return template.format(prompt=prompt)
        except (KeyError, ValueError):
            return prompt

    def _parse_stream(self, response) -> str:
        """Parsear respuesta streaming de /api/generate.
        
        Args:
            response: Response object de requests.
            
        Returns:
            Contenido concatenado de la respuesta.
        """
        content = []
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if data.get("response"):
                        content.append(data["response"])
                except json.JSONDecodeError:
                    continue
        return "".join(content)

    def _parse_chat_stream(self, response) -> str:
        """Parsear respuesta streaming de /api/chat.
        
        Args:
            response: Response object de requests.
            
        Returns:
            Contenido concatenado de la respuesta.
        """
        content = []
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    message = data.get("message", {})
                    if message.get("content"):
                        content.append(message["content"])
                except json.JSONDecodeError:
                    continue
        return "".join(content)

    # === Funciones de utilidad para function calling ===
    
    def parse_tool_call(self, response: str) -> Optional[Dict[str, Any]]:
        """Parsear llamada a herramienta desde respuesta JSON.
        
        Args:
            response: Respuesta del modelo en formato JSON.
            
        Returns:
            Diccionario con name y parameters, o None si no es tool call.
        """
        try:
            response = response.strip()
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start == -1 or end == 0:
                return None
                
            json_str = response[start:end]
            data = json.loads(json_str)
            
            if "name" in data and "parameters" in data:
                return data
            return None
            
        except (json.JSONDecodeError, ValueError):
            return None

    def format_tools_for_prompt(self, tools: List[Dict[str, Any]]) -> str:
        """Formatear definición de herramientas para prompt.
        
        Args:
            tools: Lista de definiciones de herramientas.
            
        Returns:
            String formateado para incluir en el prompt.
        """
        formatted = []
        for tool in tools:
            formatted.append(json.dumps(tool, indent=2))
        return "\n\n".join(formatted)

"""DeepSeekProvider: Módulo independiente para DeepSeek API.

Este módulo es autocontenido y maneja exclusivamente la comunicación
con la API de DeepSeek (https://api.deepseek.com).

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import requests
import os
import json
from typing import Dict, Any, List, Optional

from .base_provider import BaseProvider


class DeepSeekProvider(BaseProvider):
    """Provider para API DeepSeek.
    
    Módulo independiente que encapsula toda la lógica de comunicación
    con DeepSeek API. Ya funcional en ARES.
    """

    def __init__(self, config: Dict[str, Any]):
        """Inicializar DeepSeekProvider.
        
        Args:
            config: Configuración con base_url, model, api_key_env.
        """
        super().__init__(config)
        self.base_url = config.get("base_url", "https://api.deepseek.com")
        self.default_model = config.get("model", "deepseek-chat")
        self.api_key_env = config.get("api_key_env", "DEEPSEEK_API_KEY")
        self.api_key = os.getenv(self.api_key_env)
        self._initialized = self.validate_config()

    def generate(self, prompt: str, **kwargs) -> str:
        """Generar respuesta usando API de DeepSeek.
        
        Args:
            prompt: Prompt de entrada.
            **kwargs: model, temperature, max_tokens, etc.
            
        Returns:
            Respuesta generada por DeepSeek.
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
        """Listar modelos DeepSeek disponibles.
        
        Returns:
            Lista de modelos DeepSeek.
        """
        # DeepSeek no tiene endpoint público de lista de modelos
        # Retornamos los conocidos
        return ["deepseek-chat", "deepseek-coder"]

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
        """Llamada a API de DeepSeek chat completions.
        
        Args:
            messages: Lista de mensajes.
            model: Modelo a usar.
            temperature: Temperatura de generación.
            max_tokens: Máximo de tokens.
            
        Returns:
            Respuesta de la API.
        """
        if not self.api_key:
            return "Error: API key de DeepSeek no configurada"

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            choices = result.get("choices", [])
            
            if choices:
                return choices[0]["message"]["content"]
            return "Error: Sin respuesta de DeepSeek"
            
        except requests.exceptions.RequestException as e:
            return f"Error DeepSeek API: {str(e)}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"Error procesando respuesta: {str(e)}"

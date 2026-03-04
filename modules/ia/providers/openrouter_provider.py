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
from typing import Dict, Any, List

from .base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):
    """Provider para OpenRouter API (placeholder).
    
    Módulo reservado para futura integración con OpenRouter.
    Actualmente no funcional - solo estructura base.
    """

    def __init__(self, config: Dict[str, Any]):
        """Inicializar OpenRouterProvider.
        
        Args:
            config: Configuración con base_url, model, api_key_env.
        """
        super().__init__(config)
        self.base_url = config.get("base_url", "https://openrouter.ai/api/v1")
        self.default_model = config.get("model", "google/gemma-3-4b-it")
        self.api_key_env = config.get("api_key_env", "OPENROUTER_API_KEY")
        self.api_key = os.getenv(self.api_key_env)
        self._initialized = False  # No inicializado hasta implementación

    def generate(self, prompt: str, **kwargs) -> str:
        """Generar respuesta (placeholder).
        
        Args:
            prompt: Prompt de entrada.
            **kwargs: Parámetros adicionales.
            
        Returns:
            Mensaje de placeholder.
        """
        return (
            "⚠️ OpenRouterProvider no implementado aún.\n"
            "Este es un placeholder para futura integración.\n"
            "Configura OPENROUTER_API_KEY y completa la implementación."
        )

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generar respuesta en modo chat (placeholder).
        
        Args:
            messages: Lista de mensajes.
            **kwargs: Parámetros adicionales.
            
        Returns:
            Mensaje de placeholder.
        """
        return (
            "⚠️ OpenRouterProvider no implementado aún.\n"
            "Este es un placeholder para futura integración."
        )

    def list_models(self) -> List[str]:
        """Listar modelos OpenRouter disponibles (placeholder).
        
        Returns:
            Lista de modelos de ejemplo.
        """
        return [
            "google/gemma-3-4b-it",
            "google/gemma-3-12b-it",
            "deepseek/deepseek-chat",
            "meta-llama/llama-3-70b-instruct",
        ]

    def validate_config(self) -> bool:
        """Validar configuración (siempre False en placeholder).
        
        Returns:
            False indicando que no está implementado.
        """
        return False

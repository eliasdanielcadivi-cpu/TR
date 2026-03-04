"""BaseProvider: Interfaz abstracta para providers de IA.

Filosofía atómica: máximo 3 funciones por módulo.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class BaseProvider(ABC):
    """Interfaz base para todos los providers de IA.
    
    Cada provider implementa su propia lógica específica
    manteniendo máximo 3 funciones públicas principales.
    """

    def __init__(self, config: Dict[str, Any]):
        """Inicializar provider con configuración.
        
        Args:
            config: Diccionario con configuración específica del provider.
        """
        self.config = config
        self._initialized = False

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generar respuesta para un prompt.
        
        Args:
            prompt: Prompt de entrada.
            **kwargs: Parámetros adicionales (model, temperature, etc.).
            
        Returns:
            Respuesta generada por el modelo.
        """
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generar respuesta en modo chat.
        
        Args:
            messages: Lista de mensajes con rol y contenido.
            **kwargs: Parámetros adicionales.
            
        Returns:
            Respuesta del asistente.
        """
        pass

    @abstractmethod
    def list_models(self) -> List[str]:
        """Listar modelos disponibles.
        
        Returns:
            Lista de nombres de modelos.
        """
        pass

    def validate_config(self) -> bool:
        """Validar configuración requerida.
        
        Returns:
            True si la configuración es válida.
        """
        return True

    def _apply_template(self, template: str, **kwargs) -> str:
        """Aplicar plantilla con variables.
        
        Args:
            template: Plantilla con placeholders.
            **kwargs: Variables para reemplazar.
            
        Returns:
            Plantilla procesada.
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            return f"Error en plantilla: variable {e} no encontrada"

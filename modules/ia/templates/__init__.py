"""Gestor de plantillas YAML para ARES.

Sistema de configuración basado en YAML para:
- Plantillas de prompt optimizadas
- Definición de herramientas (functions/tools)
- Parámetros de generación
"""

from .manager import TemplateManager

__all__ = ["TemplateManager"]

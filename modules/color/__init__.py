"""
TR Color Module - Coloreado automático de pestañas Kitty
=========================================================

Módulo independiente para gestión de colores de pestañas kitty
basado en rutas de archivos o patrones.

Uso:
    from modules.color import ColorEngine
    
    engine = ColorEngine('modules/color/config.yaml')
    engine.apply('/home/daniel/Escritorio/QT5/elAsunto.md')
"""

from .color_engine import ColorEngine, ColorRule

__all__ = ['ColorEngine', 'ColorRule']
__version__ = '1.0.0'

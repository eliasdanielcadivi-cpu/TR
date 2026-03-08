"""
TR Aviso Module - Sistema de Recordatorios y Alarmas
=====================================================

Módulo independiente para gestión de avisos/recordatorios.
Programa alertas con zenity o comandos personalizados.

Uso como módulo:
    from modules.aviso import crear_aviso, listar_avisos, verificar_y_ejecutar
    
    # Programar recordatorio
    id = crear_aviso(['en', '10min', '"Recordatorio"'])
    
    # Verificar y ejecutar pendientes
    ejecutados = verificar_y_ejecutar()

Uso CLI:
    aviso en 10min "mensaje"
    aviso a las 15:30 "mensaje"
    aviso lista
    aviso borrar 1
    aviso daemon
"""

from .aviso_db import (
    guardar_aviso,
    listar_avisos,
    borrar_aviso,
    actualizar_estado,
    obtener_pendientes,
    Aviso
)
from .aviso_engine import (
    parsear_tiempo,
    ejecutar_aviso,
    verificar_y_ejecutar
)
from .aviso_cli import (
    crear_aviso,
    mostrar_lista,
    borrar_unico
)

__all__ = [
    # DB
    'guardar_aviso',
    'listar_avisos', 
    'borrar_aviso',
    'actualizar_estado',
    'obtener_pendientes',
    'Aviso',
    # Engine
    'parsear_tiempo',
    'ejecutar_aviso',
    'verificar_y_ejecutar',
    # CLI
    'crear_aviso',
    'mostrar_lista',
    'borrar_unico'
]
__version__ = '1.0.0'

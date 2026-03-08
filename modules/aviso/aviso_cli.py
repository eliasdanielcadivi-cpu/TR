"""
Aviso CLI - Interfaz de línea de comandos
==========================================

Módulo atómico para CLI de avisos.
Máximo 3 funciones principales.

Opciones en español natural:
    aviso a las 15:30 mensaje       # Hora específica
    aviso en 10min mensaje          # Relativo
    aviso el 25/12 mensaje          # Fecha específica
    aviso comando cmd a las 17:00   # Ejecutar comando
    aviso lista                     # Ver pendientes
    aviso borrar <id>               # Eliminar
    aviso daemon                    # Iniciar en background
    aviso debug                     # Activar/desactivar debug
    aviso log                       # Ver log
"""

import sys
import re
import logging
from datetime import datetime
from typing import List, Optional, Tuple
from pathlib import Path

from .aviso_engine import parsear_tiempo, verificar_y_ejecutar
from .aviso_db import (
    guardar_aviso, 
    listar_avisos, 
    borrar_aviso, 
    Aviso, 
    LOG_PATH, 
    DEBUG_PATH,
    toggle_debug,
    limpiar_logs
)

logger = logging.getLogger('aviso.cli')

# Archivo de debug en papelera
DEBUG_FILE = Path.home() / "tron/programas/TR/papelera/aviso_debug.txt"


def extraer_tiempo_y_mensaje(args: List[str]) -> Tuple[Optional[datetime], str, int]:
    """
    Extraer expresión de tiempo y mensaje de los argumentos.
    
    Estrategia:
    1. Unir todos los argumentos
    2. Buscar patrones de tiempo (en X, a las X, el X, mañana)
    3. Todo lo demás es el mensaje
    
    Retorna: (fecha_datetime, mensaje, indice_inicio_mensaje)
    """
    texto = ' '.join(args)
    logger.debug(f"Extrayendo tiempo y mensaje de: '{texto}'")
    
    # Patrones de tiempo con sus índices
    patrones = [
        (r'en\s+\d+\s*(?:minutos?|mins?|horas?|hrs?|días?|dias?|semanas?)', 'en'),
        (r'a\s+las?\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?', 'a las'),
        (r'el\s+\d{1,2}/\d{1,2}(?:/\d{4})?', 'el'),
        (r'mañana', 'mañana'),
        (r'pasado\s+mañana', 'pasado mañana'),
    ]
    
    for patron, tipo in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            # Encontrar dónde termina la expresión de tiempo
            fin_tiempo = match.end()
            mensaje = texto[fin_tiempo:].strip()
            
            # Si el mensaje empieza con comillas, quitarlas
            if mensaje.startswith('"') or mensaje.startswith("'"):
                mensaje = mensaje.strip('"\'')
            
            fecha = parsear_tiempo(texto)
            logger.debug(f"Tiempo encontrado: {fecha}, mensaje: '{mensaje}'")
            return fecha, mensaje, fin_tiempo
    
    logger.warning(f"No se encontró patrón de tiempo en: '{texto}'")
    return None, "", 0


def crear_aviso(args: List[str]) -> Optional[int]:
    """
    Crear un aviso desde argumentos CLI.
    
    Soporta:
    - aviso en 10min "mensaje" o aviso en 10min mensaje
    - aviso a las 15:30 "mensaje"
    - aviso comando "cmd" a las 17:00
    
    Retorna ID del aviso creado o None.
    """
    texto_completo = ' '.join(args)
    logger.info(f"Creando aviso desde CLI: '{texto_completo}'")
    
    # Detectar si es comando personalizado
    es_comando = 'comando' in texto_completo.lower()
    comando = 'zenity'
    
    if es_comando:
        # Extraer comando: aviso comando "echo hola" a las 15:00
        # o aviso comando echo hola a las 15:00
        match = re.search(r'comando\s+(?:["\']([^"\']+)["\']|(\S+))', texto_completo, re.IGNORECASE)
        if match:
            comando = match.group(1) or match.group(2)
            logger.debug(f"Comando personalizado: '{comando}'")
        else:
            print("❌ Error: 'comando' requiere especificar qué ejecutar")
            logger.error("Error: 'comando' sin argumento")
            return None
    
    # Extraer tiempo y mensaje
    fecha, mensaje, _ = extraer_tiempo_y_mensaje(args)
    
    if not fecha:
        print("❌ Error: No pude entender la fecha/hora. Usa:")
        print("   - aviso en 10min mensaje")
        print("   - aviso en 2horas mensaje")
        print("   - aviso a las 15:30 mensaje")
        print("   - aviso a las 3pm mensaje")
        print("   - aviso el 25/12 mensaje")
        print("   - aviso mañana mensaje")
        logger.error(f"No se pudo parsear fecha/hora: '{texto_completo}'")
        return None
    
    if not mensaje:
        print("❌ Error: Debes incluir un mensaje")
        logger.error("Error: mensaje vacío")
        return None
    
    # Guardar
    fecha_str = fecha.strftime('%Y-%m-%d %H:%M')
    aviso_id = guardar_aviso(mensaje, fecha_str, comando)
    
    print(f"✅ Aviso #{aviso_id} programado:")
    print(f"   📅 {fecha.strftime('%d/%m/%Y %H:%M')}")
    print(f"   💬 {mensaje}")
    if comando != 'zenity':
        print(f"   ⚙️  Comando: {comando}")
    
    logger.info(f"Aviso creado exitosamente: ID={aviso_id}")
    return aviso_id


def mostrar_lista(estado: str = 'pendiente') -> None:
    """
    Mostrar lista de avisos filtrados por estado.
    
    Args:
        estado: 'pendiente', 'ejecutado', 'error', 'todos'
    """
    logger.debug(f"Mostrando lista de avisos con estado='{estado}'")
    
    if estado == 'todos':
        # Mostrar todos los estados
        print("📂 HISTORIAL COMPLETO DE AVISOS:")
        print("=" * 60)
        for estado_tipo in ['pendiente', 'ejecutado', 'error']:
            mostrar_lista(estado_tipo)
        return
    
    avisos = listar_avisos(estado)

    if not avisos:
        if estado == 'pendiente':
            print("📋 No hay avisos pendientes")
        else:
            print(f"📋 No hay avisos con estado '{estado}'")
        return

    icono_estado = {'pendiente': '⏰', 'ejecutado': '✅', 'error': '❌'}
    print(f"{icono_estado.get(estado, '📋')} AVISOS {estado.upper()}:")
    print("-" * 60)
    for aviso in avisos:
        try:
            fecha = datetime.fromisoformat(aviso.fecha_hora)
            fecha_fmt = fecha.strftime('%d/%m %H:%M')
        except:
            fecha_fmt = aviso.fecha_hora

        estado_icono = "🔔" if aviso.comando == 'zenity' else "⚙️"
        linea = f"{estado_icono} #{aviso.id} | {fecha_fmt} | {aviso.mensaje}"
        if estado != 'pendiente':
            linea += f" [{aviso.estado}]"
        print(linea)
        if aviso.comando != 'zenity':
            print(f"      Comando: {aviso.comando}")
    print("-" * 60)
    print(f"Total: {len(avisos)} aviso(s)")


def borrar_unico(aviso_id: int) -> bool:
    """
    Borrar un aviso por ID.
    Retorna True si se borró.
    """
    logger.info(f"Borrando aviso #{aviso_id}")
    if borrar_aviso(aviso_id):
        print(f"✅ Aviso #{aviso_id} eliminado")
        return True
    else:
        print(f"❌ No se encontró el aviso #{aviso_id}")
        return False


def mostrar_log() -> None:
    """Mostrar el archivo de log."""
    if not LOG_PATH.exists():
        print("📋 No hay log disponible")
        return
    
    print(f"📄 LOG DE AVISO ({LOG_PATH}):")
    print("=" * 60)
    with open(LOG_PATH, 'r') as f:
        contenido = f.read()
        print(contenido[-5000:] if len(contenido) > 5000 else contenido)  # Últimos 5000 chars
    print("=" * 60)


def mostrar_debug_file() -> None:
    """Mostrar archivo de debug en papelera."""
    if not DEBUG_FILE.exists():
        print("📋 No hay archivo de debug en papelera")
        return
    
    print(f"📄 DEBUG FILE ({DEBUG_FILE}):")
    print("=" * 60)
    with open(DEBUG_FILE, 'r') as f:
        print(f.read())
    print("=" * 60)

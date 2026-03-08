"""
Aviso Engine - Motor de gestión de recordatorios
=================================================

Módulo atómico para lógica de avisos.
Máximo 3 funciones principales.

Integra:
- Parsing de tiempo natural en español
- Ejecución de comandos/zenity
- Interfaz con base de datos
"""

import subprocess
import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
from pathlib import Path

from .aviso_db import guardar_aviso, listar_avisos, borrar_aviso, actualizar_estado, obtener_pendientes, Aviso

# Configuración de logging
LOG_PATH = Path.home() / "tron/programas/TR/logs/aviso.log"
DEBUG_PATH = Path.home() / "tron/programas/TR/logs/aviso.debug"
DEBUG_FILE = Path.home() / "tron/programas/TR/papelera/aviso_debug.txt"

logger = logging.getLogger('aviso.engine')


def parsear_tiempo(texto: str) -> Optional[datetime]:
    """
    Parsear expresiones de tiempo naturales en español.
    
    Soporta:
    - "en 10 minutos", "en 2 horas", "en 3 dias"
    - "a las 15:30", "a las 3pm", "a las 8am"
    - "el 25/12", "el 31/12/2026"
    - "mañana", "pasado mañana"
    
    Retorna datetime o None si no puede parsear.
    """
    logger.debug(f"Parseando tiempo: '{texto}'")
    
    texto = texto.lower().strip()
    ahora = datetime.now()
    
    # Patrones relativos: "en X minutos/horas/dias"
    match = re.search(r'en\s+(\d+)\s*(minutos?|mins?|horas?|hrs?|días?|dias?|semanas?)', texto)
    if match:
        valor = int(match.group(1))
        unidad = match.group(2)[:2]
        if unidad == 'mi':
            resultado = ahora + timedelta(minutes=valor)
            logger.debug(f"Patrón relativo minutos: +{valor}min → {resultado}")
            return resultado
        elif unidad == 'ho':
            resultado = ahora + timedelta(hours=valor)
            logger.debug(f"Patrón relativo horas: +{valor}h → {resultado}")
            return resultado
        elif unidad == 'dí' or unidad == 'di':
            resultado = ahora + timedelta(days=valor)
            logger.debug(f"Patrón relativo días: +{valor}d → {resultado}")
            return resultado
        elif unidad == 'se':
            resultado = ahora + timedelta(weeks=valor)
            logger.debug(f"Patrón relativo semanas: +{valor}sem → {resultado}")
            return resultado
    
    # Patrones de hora: "a las 15:30", "a las 3pm"
    match = re.search(r'a\s+las?\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', texto)
    if match:
        hora = int(match.group(1))
        minuto = int(match.group(2)) if match.group(2) else 0
        ampm = match.group(3)
        if ampm == 'pm' and hora < 12:
            hora += 12
        elif ampm == 'am' and hora == 12:
            hora = 0
        resultado = ahora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
        logger.debug(f"Patrón hora: {hora}:{minuto} → {resultado}")
        return resultado
    
    # Patrones de fecha: "el 25/12", "el 31/12/2026"
    match = re.search(r'el\s+(\d{1,2})/(\d{1,2})(?:/(\d{4}))?', texto)
    if match:
        dia = int(match.group(1))
        mes = int(match.group(2))
        anio = int(match.group(3)) if match.group(3) else ahora.year
        try:
            resultado = ahora.replace(year=anio, month=mes, day=dia, hour=9, minute=0, second=0)
            logger.debug(f"Patrón fecha: {dia}/{mes}/{anio} → {resultado}")
            return resultado
        except ValueError as e:
            logger.warning(f"Fecha inválida: {e}")
            return None
    
    # "mañana", "pasado mañana"
    if 'mañana' in texto and 'pasado' in texto:
        resultado = ahora + timedelta(days=2)
        logger.debug(f"Pasado mañana: +2d → {resultado}")
        return resultado
    elif 'mañana' in texto:
        resultado = ahora + timedelta(days=1)
        logger.debug(f"Mañana: +1d → {resultado}")
        return resultado
    
    logger.warning(f"No se pudo parsear: '{texto}'")
    return None


def ejecutar_aviso(aviso: Aviso) -> bool:
    """
    Ejecutar un aviso: mostrar zenity o ejecutar comando.
    
    Si comando es 'zenity', muestra diálogo gráfico.
    Si es otro comando, lo ejecuta con subprocess.
    
    Retorna True si se ejecutó exitosamente.
    """
    logger.info(f"Ejecutando aviso ID={aviso.id}: '{aviso.mensaje}' (comando={aviso.comando})")
    
    # Escribir archivo de debug en papelera
    DEBUG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DEBUG_FILE, 'a') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"[{datetime.now().isoformat()}] EJECUTANDO AVISO\n")
        f.write(f"ID: {aviso.id}\n")
        f.write(f"Mensaje: {aviso.mensaje}\n")
        f.write(f"Comando: {aviso.comando}\n")
        f.write(f"Fecha programada: {aviso.fecha_hora}\n")
        f.write(f"{'='*60}\n")
    
    try:
        if aviso.comando == 'zenity':
            logger.debug("Ejecutando zenity (timeout 10s)...")
            # Zenity con timeout para no bloquear indefinidamente
            result = subprocess.run([
                'zenity',
                '--info',
                '--title', '⏰ AVISO - Recordatorio',
                '--text', aviso.mensaje,
                '--width', '400',
                '--height', '150',
                '--timeout', '10'  # Auto-cierre después de 10 segundos
            ], timeout=15, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Zenity ejecutado correctamente")
            elif result.returncode == 1:  # Timeout o cancelado
                logger.info("Zenity cerrado por timeout/usuario (comportamiento normal)")
            else:
                logger.warning(f"Zenity retornó {result.returncode}: {result.stderr}")
        else:
            logger.debug(f"Ejecutando comando: {aviso.comando}")
            result = subprocess.run(aviso.comando, shell=True, timeout=300, capture_output=True, text=True)
            logger.info(f"Comando retornó {result.returncode}")
            if result.stdout:
                logger.debug(f"STDOUT: {result.stdout}")
            if result.stderr:
                logger.warning(f"STDERR: {result.stderr}")
        
        return True
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout ejecutando aviso ID={aviso.id}")
        return True  # Considerar como ejecutado aunque haya timeout
    except FileNotFoundError as e:
        logger.error(f"Comando no encontrado: {e}")
        return False
    except Exception as e:
        logger.error(f"Error ejecutando aviso: {e}")
        return False


def verificar_y_ejecutar() -> int:
    """
    Verificar avisos pendientes y ejecutar los que corresponden.
    
    Compara la hora actual con la hora programada.
    Ejecuta los avisos vencidos y actualiza su estado.
    
    Retorna cantidad de avisos ejecutados.
    """
    logger.debug("=== Iniciando verificación de avisos ===")
    
    ahora = datetime.now()
    ejecutados = 0
    errores = 0
    
    for aviso in obtener_pendientes():
        try:
            fecha_aviso = datetime.fromisoformat(aviso.fecha_hora)
            diferencia = (ahora - fecha_aviso).total_seconds()
            
            logger.debug(f"Aviso #{aviso.id}: programado={aviso.fecha_hora}, diferencia={diferencia}s")
            
            if diferencia >= 0:
                logger.info(f"Aviso #{aviso.id} VENCIDO (diferencia={diferencia}s)")
                
                if ejecutar_aviso(aviso):
                    actualizar_estado(aviso.id, 'ejecutado')
                    ejecutados += 1
                else:
                    actualizar_estado(aviso.id, 'error')
                    errores += 1
        except (ValueError, Exception) as e:
            logger.error(f"Error procesando aviso #{aviso.id}: {e}")
            actualizar_estado(aviso.id, 'error')
            errores += 1
    
    logger.info(f"Verificación completada: {ejecutados} ejecutados, {errores} errores")
    return ejecutados

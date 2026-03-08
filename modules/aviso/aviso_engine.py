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
from datetime import datetime, timedelta
from typing import Optional, Tuple
from .aviso_db import guardar_aviso, listar_avisos, borrar_aviso, actualizar_estado, obtener_pendientes, Aviso


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
    texto = texto.lower().strip()
    ahora = datetime.now()
    
    # Patrones relativos: "en X minutos/horas/dias"
    match = re.search(r'en\s+(\d+)\s*(minutos?|mins?|horas?|hrs?|días?|dias?|semanas?)', texto)
    if match:
        valor = int(match.group(1))
        unidad = match.group(2)[:2]
        if unidad == 'mi':
            return ahora + timedelta(minutes=valor)
        elif unidad == 'ho':
            return ahora + timedelta(hours=valor)
        elif unidad == 'dí' or unidad == 'di':
            return ahora + timedelta(days=valor)
        elif unidad == 'se':
            return ahora + timedelta(weeks=valor)
    
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
        return ahora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
    
    # Patrones de fecha: "el 25/12", "el 31/12/2026"
    match = re.search(r'el\s+(\d{1,2})/(\d{1,2})(?:/(\d{4}))?', texto)
    if match:
        dia = int(match.group(1))
        mes = int(match.group(2))
        anio = int(match.group(3)) if match.group(3) else ahora.year
        try:
            return ahora.replace(year=anio, month=mes, day=dia, hour=9, minute=0, second=0)
        except ValueError:
            return None
    
    # "mañana", "pasado mañana"
    if 'mañana' in texto and 'pasado' in texto:
        return ahora + timedelta(days=2)
    elif 'mañana' in texto:
        return ahora + timedelta(days=1)
    
    return None


def ejecutar_aviso(aviso: Aviso) -> bool:
    """
    Ejecutar un aviso: mostrar zenity o ejecutar comando.
    
    Si comando es 'zenity', muestra diálogo gráfico.
    Si es otro comando, lo ejecuta con subprocess.
    
    Retorna True si se ejecutó exitosamente.
    """
    try:
        if aviso.comando == 'zenity':
            subprocess.run([
                'zenity',
                '--info',
                '--title', '⏰ AVISO - Recordatorio',
                '--text', f'{aviso.mensaje}',
                '--width', '400',
                '--height', '150'
            ], timeout=300)
        else:
            # Ejecutar comando personalizado
            subprocess.run(aviso.comando, shell=True, timeout=300)
        return True
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"Error ejecutando aviso: {e}")
        return False


def verificar_y_ejecutar() -> int:
    """
    Verificar avisos pendientes y ejecutar los que corresponden.
    
    Compara la hora actual con la hora programada.
    Ejecuta los avisos vencidos y actualiza su estado.
    
    Retorna cantidad de avisos ejecutados.
    """
    ahora = datetime.now()
    ejecutados = 0
    
    for aviso in obtener_pendientes():
        try:
            fecha_aviso = datetime.fromisoformat(aviso.fecha_hora)
            if fecha_aviso <= ahora:
                if ejecutar_aviso(aviso):
                    actualizar_estado(aviso.id, 'ejecutado')
                    ejecutados += 1
        except (ValueError, Exception):
            # Si hay error parseando la fecha, marcar como error
            actualizar_estado(aviso.id, 'error')
    
    return ejecutados

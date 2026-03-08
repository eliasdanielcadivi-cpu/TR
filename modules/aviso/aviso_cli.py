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
"""

import sys
import re
from datetime import datetime
from typing import List, Optional, Tuple
from .aviso_engine import parsear_tiempo, verificar_y_ejecutar
from .aviso_db import guardar_aviso, listar_avisos, borrar_aviso, Aviso


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
            return fecha, mensaje, fin_tiempo
    
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
    
    # Detectar si es comando personalizado
    es_comando = 'comando' in texto_completo.lower()
    comando = 'zenity'
    
    if es_comando:
        # Extraer comando: aviso comando "echo hola" a las 15:00
        # o aviso comando echo hola a las 15:00
        match = re.search(r'comando\s+(?:["\']([^"\']+)["\']|(\S+))', texto_completo, re.IGNORECASE)
        if match:
            comando = match.group(1) or match.group(2)
        else:
            print("❌ Error: 'comando' requiere especificar qué ejecutar")
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
        return None
    
    if not mensaje:
        print("❌ Error: Debes incluir un mensaje")
        return None
    
    # Guardar
    fecha_str = fecha.strftime('%Y-%m-%d %H:%M')
    aviso_id = guardar_aviso(mensaje, fecha_str, comando)
    
    print(f"✅ Aviso #{aviso_id} programado:")
    print(f"   📅 {fecha.strftime('%d/%m/%Y %H:%M')}")
    print(f"   💬 {mensaje}")
    if comando != 'zenity':
        print(f"   ⚙️  Comando: {comando}")
    
    return aviso_id


def mostrar_lista() -> None:
    """
    Mostrar lista de avisos pendientes.
    """
    avisos = listar_avisos('pendiente')
    
    if not avisos:
        print("📋 No hay avisos pendientes")
        return
    
    print("⏰ AVISOS PENDIENTES:")
    print("-" * 60)
    for aviso in avisos:
        try:
            fecha = datetime.fromisoformat(aviso.fecha_hora)
            fecha_fmt = fecha.strftime('%d/%m %H:%M')
        except:
            fecha_fmt = aviso.fecha_hora
        
        estado_icono = "🔔" if aviso.comando == 'zenity' else "⚙️"
        print(f"{estado_icono} #{aviso.id} | {fecha_fmt} | {aviso.mensaje}")
        if aviso.comando != 'zenity':
            print(f"      Comando: {aviso.comando}")
    print("-" * 60)
    print(f"Total: {len(avisos)} aviso(s)")


def borrar_unico(aviso_id: int) -> bool:
    """
    Borrar un aviso por ID.
    Retorna True si se borró.
    """
    if borrar_aviso(aviso_id):
        print(f"✅ Aviso #{aviso_id} eliminado")
        return True
    else:
        print(f"❌ No se encontró el aviso #{aviso_id}")
        return False

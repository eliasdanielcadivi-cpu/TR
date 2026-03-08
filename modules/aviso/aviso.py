#!/usr/bin/env python3
"""
AVISO - Sistema de Recordatorios y Alarmas
===========================================

CLI principal para el módulo de avisos.
Opciones en español natural diseñadas para fluir como palabras normales.

USO:
    aviso [OPCIÓN] [ARGUMENTOS]

OPCIONES:
    en <tiempo> "<mensaje>"       Recordatorio relativo
        Ej: aviso en 10min "reunión"
        Ej: aviso en 2horas "tomar medicina"
    
    a las <hora> "<mensaje>"      Hora específica
        Ej: aviso a las 15:30 "llamar al cliente"
        Ej: aviso a las 3pm "café"
    
    el <fecha> "<mensaje>"        Fecha específica
        Ej: aviso el 25/12 "feliz navidad"
        Ej: aviso el 31/12/2026 "fin de año"
    
    mañana "<mensaje>"            Para mañana
        Ej: aviso mañana "entregar informe"
    
    comando "<cmd>" ...            Ejecutar comando/script
        Ej: aviso comando "notify-send 'Hora!'" a las 17:00
        Ej: aviso comando "/ruta/script.sh" en 1hora
    
    lista                          Ver avisos pendientes
        Ej: aviso lista
    
    ejecutados                     Ver avisos ejecutados
        Ej: aviso ejecutados
    
    historial                      Ver todos los avisos
        Ej: aviso historial
    
    borrar <id>                    Eliminar aviso por ID
        Ej: aviso borrar 5
    
    daemon                         Iniciar verificador en background
        Ej: aviso daemon
    
    debug                          Activar/desactivar modo debug
        Ej: aviso debug
    
    log                            Ver log de ejecución
        Ej: aviso log
    
    ayuda, --help                  Mostrar esta ayuda

EJEMPLOS DE FLUJO NATURAL:
    aviso en 5min "revisar el horno"
    aviso a las 8am "tomar pastillas"
    aviso el 15/03 "pago de tarjeta"
    aviso comando "mpv /musica/alarma.mp3" a las 7am
    aviso lista
    aviso borrar 3

INTEGRACIÓN CON ARES IA:
    La IA puede usar este módulo para programar recordatorios:
    - "coloca una alarma para las 3pm" → aviso a las 3pm "alarma"
    - "recuérdame esto en 10 minutos" → aviso en 10min "mensaje"
"""

import sys
import os
import subprocess
import time
import argparse
import logging

# Añadir TR al PATH para imports
TRON_PATH = os.path.expanduser("~/tron/programas/TR")
sys.path.insert(0, TRON_PATH)

# Configurar logging primero
from pathlib import Path
LOG_PATH = Path.home() / "tron/programas/TR/logs/aviso.log"
DEBUG_PATH = Path.home() / "tron/programas/TR/logs/aviso.debug"

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

level = logging.DEBUG if DEBUG_PATH.exists() else logging.INFO
logging.basicConfig(
    level=level,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
    ]
)

logger = logging.getLogger('aviso')

from modules.aviso import (
    crear_aviso,
    mostrar_lista,
    borrar_unico,
    verificar_y_ejecutar,
    mostrar_log,
    mostrar_debug_file
)
from modules.aviso.aviso_db import toggle_debug, limpiar_logs


def mostrar_ayuda():
    """Mostrar ayuda detallada."""
    print(__doc__)


def iniciar_daemon():
    """
    Iniciar verificador en background.
    Revisa avisos cada 30 segundos.
    """
    print("🔔 Iniciando daemon de avisos...")
    print("   Revisando cada 30 segundos")
    print("   Presiona Ctrl+C para detener")
    logger.info("Daemon iniciado")
    
    try:
        while True:
            ejecutados = verificar_y_ejecutar()
            if ejecutados > 0:
                print(f"   ⏰ {ejecutados} aviso(s) ejecutado(s)")
                logger.info(f"{ejecutados} avisos ejecutados")
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Daemon detenido por usuario")
        print("\n✅ Daemon detenido")


def test_aviso():
    """
    Crear un aviso de prueba para 1 minuto y verificar funcionamiento.
    """
    print("🧪 TEST DE AVISO - Creando aviso para 1 minuto...")
    logger.info("Iniciando test de aviso")
    
    from datetime import datetime, timedelta
    from modules.aviso.aviso_db import guardar_aviso
    
    ahora = datetime.now()
    futuro = (ahora + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
    
    aviso_id = guardar_aviso("TEST DE AVISO - Si ves esto, funciona!", futuro, 'zenity')
    print(f"✅ Aviso de prueba #{aviso_id} creado para {futuro}")
    print(f"   Espera 1 minuto y ejecuta: aviso verificar")
    print(f"   O ejecuta: aviso daemon (para verificación automática)")
    logger.info(f"Test creado: ID={aviso_id}, fecha={futuro}")
    
    # Escribir en papelera
    debug_file = Path.home() / "tron/programas/TR/papelera/aviso_test.txt"
    debug_file.parent.mkdir(parents=True, exist_ok=True)
    with open(debug_file, 'w') as f:
        f.write(f"TEST DE AVISO\n")
        f.write(f"=============\n")
        f.write(f"ID: {aviso_id}\n")
        f.write(f"Fecha programada: {futuro}\n")
        f.write(f"Fecha creación: {ahora.isoformat()}\n")
        f.write(f"Espera: 1 minuto\n")
        f.write(f"Verifica: ejecuta 'aviso verificar' o 'aviso daemon'\n")
    print(f"   📄 Info en: {debug_file}")


def main():
    """Punto de entrada principal CLI."""
    logger.info(f"AVISO CLI iniciado con args: {sys.argv}")
    
    if len(sys.argv) < 2:
        mostrar_ayuda()
        return
    
    arg = sys.argv[1]
    
    # Comandos simples
    if arg in ['lista', 'ls', 'listar']:
        mostrar_lista()
        return
    
    if arg in ['historial', 'historico', 'todos', 'all']:
        mostrar_lista('todos')
        return
    
    if arg in ['ejecutados', 'ejecutado']:
        mostrar_lista('ejecutado')
        return
    
    if arg in ['errores', 'error']:
        mostrar_lista('error')
        return
    
    if arg in ['ayuda', '--help', '-h', 'help']:
        mostrar_ayuda()
        return
    
    if arg in ['daemon', 'background', 'bg']:
        iniciar_daemon()
        return
    
    if arg in ['borrar', 'del', 'delete', 'rm']:
        if len(sys.argv) < 3:
            print("❌ Error: Debes especificar el ID del aviso")
            print("   Ej: aviso borrar 5")
            return
        try:
            aviso_id = int(sys.argv[2])
            borrar_unico(aviso_id)
        except ValueError:
            print(f"❌ Error: '{sys.argv[2]}' no es un número válido")
        return
    
    if arg in ['verificar', 'check', 'run', 'ejecutar']:
        ejecutados = verificar_y_ejecutar()
        print(f"✅ {ejecutados} aviso(s) ejecutado(s)")
        return
    
    if arg in ['debug', 'depurar']:
        toggle_debug()
        if DEBUG_PATH.exists():
            print("✅ Debug ACTIVADO")
            print(f"   Log: {LOG_PATH}")
            print(f"   Ver con: aviso log")
        else:
            print("✅ Debug DESACTIVADO")
        return
    
    if arg in ['log', 'logs']:
        mostrar_log()
        return
    
    if arg in ['debug-file', 'papelera']:
        mostrar_debug_file()
        return
    
    if arg in ['test', 'prueba']:
        test_aviso()
        return
    
    if arg in ['limpiar-log', 'clean-log']:
        limpiar_logs()
        print("✅ Log limpiado")
        return
    
    # Crear aviso: todo lo demás son argumentos para crear
    # Soporta múltiples formatos naturales
    args = sys.argv[1:]  # Incluir primer arg para parsing
    crear_aviso(args)


if __name__ == "__main__":
    main()

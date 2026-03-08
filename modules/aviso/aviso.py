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
    
    borrar <id>                    Eliminar aviso por ID
        Ej: aviso borrar 5
    
    daemon                         Iniciar verificador en background
        Ej: aviso daemon
    
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

# Añadir TR al PATH para imports
TRON_PATH = os.path.expanduser("~/tron/programas/TR")
sys.path.insert(0, TRON_PATH)

from modules.aviso import (
    crear_aviso,
    mostrar_lista,
    borrar_unico,
    verificar_y_ejecutar
)


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
    
    try:
        while True:
            ejecutados = verificar_y_ejecutar()
            if ejecutados > 0:
                print(f"   ⏰ {ejecutados} aviso(s) ejecutado(s)")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n✅ Daemon detenido")


def main():
    """Punto de entrada principal CLI."""
    if len(sys.argv) < 2:
        mostrar_ayuda()
        return
    
    arg = sys.argv[1]
    
    # Comandos simples
    if arg in ['lista', 'ls', 'listar']:
        mostrar_lista()
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
    
    if arg in ['verificar', 'check', 'run']:
        ejecutados = verificar_y_ejecutar()
        print(f"✅ {ejecutados} aviso(s) ejecutado(s)")
        return
    
    # Crear aviso: todo lo demás son argumentos para crear
    # Soporta múltiples formatos naturales
    args = sys.argv[1:]  # Incluir primer arg para parsing
    crear_aviso(args)


if __name__ == "__main__":
    main()

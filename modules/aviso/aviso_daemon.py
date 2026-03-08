#!/usr/bin/env python3
"""
AVISO Daemon - Verificador en segundo plano
============================================

Script independiente para ejecutar en background.
Revisa avisos pendientes cada 30 segundos y ejecuta los vencidos.

USO:
    python aviso_daemon.py &
    
O usar el comando:
    aviso daemon

LOG:
    Escribe eventos a ~/tron/programas/TR/logs/aviso.log
"""

import os
import sys
import time
from datetime import datetime

# Añadir TR al PATH
TRON_PATH = os.path.expanduser("~/tron/programas/TR")
sys.path.insert(0, TRON_PATH)

from modules.aviso import verificar_y_ejecutar

LOG_FILE = os.path.join(TRON_PATH, "logs/aviso.log")


def log(mensaje: str):
    """Escribir mensaje al log con timestamp."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {mensaje}\n")


def main():
    """Loop principal del daemon."""
    log("=== Daemon iniciado ===")
    print("🔔 Daemon de avisos iniciado")
    print(f"   Log: {LOG_FILE}")
    print("   Intervalo: 30 segundos")
    print("   Presiona Ctrl+C para detener")
    
    try:
        while True:
            ejecutados = verificar_y_ejecutar()
            if ejecutados > 0:
                msg = f"{ejecutados} aviso(s) ejecutado(s)"
                log(msg)
                print(f"   ⏰ {msg}")
            time.sleep(30)
    except KeyboardInterrupt:
        log("=== Daemon detenido por usuario ===")
        print("\n✅ Daemon detenido")
    except Exception as e:
        log(f"ERROR: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

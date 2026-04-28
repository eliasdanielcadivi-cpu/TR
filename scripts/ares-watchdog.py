#!/usr/bin/env python3
import requests
import json
import time
import os
from datetime import datetime

# --- CONFIGURACIÓN ESTATAL ---
RPC_URL = "http://localhost:6800/jsonrpc"
LOG_FILE = "/home/daniel/tron/programas/TR/logs/watchdog_telemetry.log"
INV_PATH = "/home/daniel/tron/programas/TR/db/multimedia/inventario.json"

def log_event(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def get_telemetry():
    payload = {
        "jsonrpc": "2.0",
        "id": "ares-watchdog",
        "method": "aria2.tellActive"
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=5)
        return response.json().get("result", [])
    except:
        return None

def monitor():
    log_event("🔭 INICIANDO TELEMETRÍA DETERMINISTA (Capítulos 1-4)")
    while True:
        tasks = get_telemetry()
        if tasks is None:
            log_event("❌ ERROR: No se pudo contactar con el núcleo RPC. ¿aria2c daemon activo?")
        elif not tasks:
            log_event("⚠️  INFO: No hay descargas activas en el núcleo.")
        else:
            for t in tasks:
                gid = t.get("gid")
                # Intentamos sacar el nombre del archivo o los metadatos
                name = t.get("bittorrent", {}).get("info", {}).get("name", "Resolviendo Metadatos...")
                completed = int(t.get("completedLength", 0))
                total = int(t.get("totalLength", 0))
                speed = int(t.get("downloadSpeed", 0))
                
                if total > 0:
                    perc = round((completed / total) * 100, 2)
                    status = f"[{perc}%] | {round(speed/1024, 2)} KB/s | {name}"
                else:
                    status = f"[METADATA] | Negociando con enjambre... | {gid}"
                
                log_event(f"📊 {status}")
                
                # Si se completa al 100%, podríamos marcar en inventario
                if total > 0 and completed >= total:
                     log_event(f"✅ FINALIZADO: {name}")

        log_event("--- Auditoría completada. Ciclo de espera: 30s ---")
        time.sleep(30)

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))
    monitor()

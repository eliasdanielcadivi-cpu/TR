#!/usr/bin/env python3
import subprocess
import time
import os
import json
import sys
import yaml
from pathlib import Path

# --- CONFIGURACIÓN MAESTRA ARES ---
BASE_DIR = Path("/home/daniel/tron/programas/TR")
SOCKET = "unix:/tmp/ares_master_final"
BIN_DIR = BASE_DIR / "bin"
PAPELERA = BASE_DIR / "papelera"

# Paleta Hacker Neon Oficial (Active FG, Inactive FG, Active BG, Inactive BG)
PALETTE = {
    'GEMINI':  {'afg': '#00FFFF', 'ifg': '#00AAAA', 'abg': '#001A1A', 'ibg': '#000D0D'}, # Cyberpunk
    'QWEN':    {'afg': '#FF00FF', 'ifg': '#AA00AA', 'abg': '#1A001A', 'ibg': '#0D000D'}, # Neon Goddess
    'COMANDO': {'afg': '#39FF14', 'ifg': '#22AA00', 'abg': '#0A1A0A', 'ibg': '#050D05'}, # Matrix
    'NOTAS':   {'afg': '#FF6600', 'ifg': '#AA4400', 'abg': '#1A0D00', 'ibg': '#0D0600'}, # Blade Runner
    'AGENDA':  {'afg': '#FF0000', 'ifg': '#AA0000', 'abg': '#1A0000', 'ibg': '#0D0000'}, # Red Alert
    'BR':      {'afg': '#0000FF', 'ifg': '#0000AA', 'abg': '#00001A', 'ibg': '#00000D'}  # Deep Blue
}

def run_remote(args):
    """Control remoto via Socket Dedicado."""
    return subprocess.run(["kitten", "@", "--to", SOCKET] + args, capture_output=True, text=True)

def apply_neon(title, key):
    """Aplica la pigmentación Hacker Neon."""
    c = PALETTE[key]
    run_remote([
        "set-tab-color", "--match", f"title:^{title}$",
        f"active_fg={c['afg']}", f"inactive_fg={c['ifg']}",
        f"active_bg={c['abg']}", f"inactive_bg={c['ibg']}"
    ])

def main():
    print(f"🚀 [MISIÓN FINAL] Levantando Ecosistema ARES en {SOCKET}...")
    
    # 1. Limpieza de rastros y procesos huerfanos del socket
    for f in PAPELERA.glob("test_*.txt"): f.unlink()
    subprocess.run(["pkill", "-f", f"listen-on {SOCKET}"], stderr=subprocess.DEVNULL)
    time.sleep(1.0)

    # 2. LANZAR PROCESO MAESTRO (Ventana Soberana)
    # Se inicia con zsh para que la pestaña GEMINI esté lista
    subprocess.Popen([
        "kitty", 
        "--title", "Ares por Daniel Hung", 
        "--listen-on", SOCKET,
        "-o", "allow_remote_control=yes",
        "--detach"
    ])
    
    # Handshake (Espera activa al socket)
    print("⏳ Sincronizando con el Socket...")
    retries = 0
    while retries < 20:
        if run_remote(["ls"]).returncode == 0: break
        time.sleep(0.5); retries += 1
    if retries == 20: print("❌ ERROR: El proceso Kitty no respondió al socket."); sys.exit(1)

    # 3. CONFIGURAR PESTAÑA 1 (GEMINI)
    print("💎 Configurando GEMINI...")
    run_remote(["set-tab-title", "--match", "recent:0", "GEMINI"])
    apply_neon("GEMINI", "GEMINI")

    # 4. DESPLIEGUE SECUENCIAL DE PESTAÑAS (2 a 6)
    # Formato: (Título, ColorKey, Comando)
    sequence = [
        ("QWEN", "QWEN", None),
        ("COMANDO", "COMANDO", None),
        ("NOTAS", "NOTAS", f"{BIN_DIR}/notas"),
        ("AGENDA", "AGENDA", f"{BIN_DIR}/agenda"),
        ("BR", "BR", f"{BIN_DIR}/br")
    ]

    for title, color, cmd in sequence:
        print(f"  ↳ Lanzando {title}...")
        # Usamos launch directo con comando para que sea el dueño del proceso en la pestaña
        args = ["launch", "--type=tab", "--tab-title", title]
        if cmd:
            rastro = PAPELERA / f"test_{title.lower()}.txt"
            # Inyección robusta: rastro + ejecución interactiva
            args.extend(["sh", "-c", f"touch {rastro}; exec {cmd}"])
        
        run_remote(args)
        time.sleep(0.5) # Estabilidad entre lanzamientos
        apply_neon(title, color)

    print("\n✅ ECOSISTEMA DESPLEGADO.")
    print("Pestañas: 6 | Colores: Hacker Neon | Socket: Dedicado")

if __name__ == "__main__":
    main()

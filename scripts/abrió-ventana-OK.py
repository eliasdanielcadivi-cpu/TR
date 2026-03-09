#!/usr/bin/env python3
import subprocess
import time
import os
import sys
import yaml
from pathlib import Path

# --- CONFIGURACIÓN TÁCTICA ---
BASE_DIR = Path("/home/daniel/tron/programas/TR")
SOCKET = "unix:/tmp/mykitty"
BIN_DIR = BASE_DIR / "bin"
PAPELERA = BASE_DIR / "papelera"

# Cargar Título Soberano
with open(BASE_DIR / "config/config.yaml", 'r') as f:
    config = yaml.safe_load(f)
SOVEREIGN_TITLE = config.get('identity', {}).get('window_title', "Ares por Daniel Hung")

# Paleta Hacker Neon (4 componentes)
PALETTE = {
    'GEMINI':  {'afg': '#00FFFF', 'ifg': '#00AAAA', 'abg': '#001A1A', 'ibg': '#000D0D'},
    'QWEN':    {'afg': '#FF00FF', 'ifg': '#AA00AA', 'abg': '#1A001A', 'ibg': '#0D000D'},
    'COMANDO': {'afg': '#39FF14', 'ifg': '#22AA00', 'abg': '#0A1A0A', 'ibg': '#050D05'},
    'NOTAS':   {'afg': '#FF6600', 'ifg': '#AA4400', 'abg': '#1A0D00', 'ibg': '#0D0600'},
    'AGENDA':  {'afg': '#FF0000', 'ifg': '#AA0000', 'abg': '#1A0000', 'ibg': '#0D0000'},
    'BR':      {'afg': '#0000FF', 'ifg': '#0000AA', 'abg': '#00001A', 'ibg': '#00000D'}
}

def run_remote(args):
    return subprocess.run(["kitten", "@", "--to", SOCKET] + args, capture_output=True, text=True)

def apply_color(title, key):
    c = PALETTE[key]
    run_remote([
        "set-tab-color", "--match", f"title:^{title}$",
        f"active_fg={c['afg']}", f"inactive_fg={c['ifg']}",
        f"active_bg={c['abg']}", f"inactive_bg={c['ibg']}"
    ])

def main():
    print(f"🚀 [MIGAS DE PAN] Despliegue en {SOCKET}...")
    
    # 1. Crear nueva ventana OS (Identidad ARES)
    # Kitty abrirá una pestaña inicial que mutaremos
    run_remote(["launch", "--type=os-window", "--window-title", SOVEREIGN_TITLE, "zsh"])
    time.sleep(1.0)
    
    # Mutar la pestaña 0 (de la nueva ventana) a GEMINI
    run_remote(["set-tab-title", "--match", f"window_title:^{SOVEREIGN_TITLE}$", "GEMINI"])
    apply_color("GEMINI", "GEMINI")
    
    # 2. Secuencia de pestañas
    tabs = [
        ("QWEN", "QWEN", None),
        ("COMANDO", "COMANDO", None),
        ("NOTAS", "NOTAS", f"{BIN_DIR}/notas"),
        ("AGENDA", "AGENDA", f"{BIN_DIR}/agenda"),
        ("BR", "BR", f"{BIN_DIR}/br")
    ]
    
    for title, color_key, cmd in tabs:
        print(f"  ↳ Pestaña: {title}")
        args = ["launch", "--type=tab", "--tab-title", title, "--match", f"window_title:^{SOVEREIGN_TITLE}$"]
        if cmd:
            args.extend(["sh", "-c", f"touch {PAPELERA}/test_{title.lower()}.txt; exec {cmd}"])
        
        run_remote(args)
        time.sleep(0.3)
        apply_color(title, color_key)

    print("🏁 Despliegue Maestro Finalizado.")

if __name__ == "__main__":
    main()

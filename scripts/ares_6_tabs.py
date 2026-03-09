#!/usr/bin/env python3
import subprocess
import time
import os
import json
import yaml
from pathlib import Path

# --- CONFIGURACIÓN TÁCTICA ---
BASE_DIR = Path("/home/daniel/tron/programas/TR")
SOCKET = "unix:/tmp/mykitty"
BIN_DIR = BASE_DIR / "bin"
PAPELERA = BASE_DIR / "papelera"

# Cargar Identidad Soberana
with open(BASE_DIR / "config/config.yaml", 'r') as f:
    config = yaml.safe_load(f)
SOVEREIGN_TITLE = config.get('identity', {}).get('window_title', "Ares por Daniel Hung")

# Paleta Hacker Neon (4 componentes) de COLOR_SYSTEM.md
PALETTE = {
    'GEMINI':  {'afg': '#00FFFF', 'ifg': '#00AAAA', 'abg': '#001A1A', 'ibg': '#000D0D'}, # Cyberpunk
    'QWEN':    {'afg': '#FF00FF', 'ifg': '#AA00AA', 'abg': '#1A001A', 'ibg': '#0D000D'}, # Neon Goddess
    'COMANDO': {'afg': '#39FF14', 'ifg': '#22AA00', 'abg': '#0A1A0A', 'ibg': '#050D05'}, # Matrix
    'NOTAS':   {'afg': '#FF6600', 'ifg': '#AA4400', 'abg': '#1A0D00', 'ibg': '#0D0600'}, # Blade Runner
    'AGENDA':  {'afg': '#FF0000', 'ifg': '#AA0000', 'abg': '#1A0000', 'ibg': '#0D0000'}, # Red Alert (Custom)
    'BR':      {'afg': '#0000FF', 'ifg': '#0000AA', 'abg': '#00001A', 'ibg': '#00000D'}  # Deep Blue (Custom)
}

def run_remote(args):
    return subprocess.run(["kitten", "@", "--to", SOCKET] + args, capture_output=True, text=True)

def main():
    print(f"🚀 [BASE EMPÍRICA] Localizando ventana: {SOVEREIGN_TITLE}")
    
    # 1. Obtener el ID de la ventana que ya sabemos que abre bien
    ls_output = run_remote(["ls"]).stdout
    try:
        data = json.loads(ls_output)
    except:
        print("❌ Error al leer el estado de Kitty.")
        return

    target_window_id = None
    for window in data:
        if window.get('title') == SOVEREIGN_TITLE:
            target_window_id = window.get('id')
            break
    
    if not target_window_id:
        # Si no la encuentra por título de ventana, busca por título de pestaña
        for window in data:
            for tab in window.get('tabs', []):
                if tab.get('title') == SOVEREIGN_TITLE or tab.get('title') == "GEMINI":
                    target_window_id = window.get('id')
                    break

    if not target_window_id:
        print("❌ No se encontró la ventana soberana. ¿Está abierta?")
        return

    print(f"✅ Ventana identificada (ID: {target_window_id})")

    # 2. Configurar Pestaña 1: GEMINI (Mutación de la pestaña activa de esa ventana)
    # Buscamos la pestaña activa de esa ventana específica
    active_tab_id = None
    for window in data:
        if window.get('id') == target_window_id:
            for tab in window.get('tabs', []):
                if tab.get('is_focused'):
                    active_tab_id = tab.get('id')
                    break
    
    print("🔧 Configurando GEMINI...")
    run_remote(["set-tab-title", "--match", f"window_id:{target_window_id} and state:focused", "GEMINI"])
    c = PALETTE['GEMINI']
    run_remote(["set-tab-color", "--match", "title:^GEMINI$", 
                f"active_fg={c['afg']}", f"inactive_fg={c['ifg']}", 
                f"active_bg={c['abg']}", f"inactive_bg={c['ibg']}"])

    # 3. Lanzar las otras 5 pestañas en esa misma ventana
    tabs = [
        ("QWEN", "QWEN", None),
        ("COMANDO", "COMANDO", None),
        ("NOTAS", "NOTAS", f"{BIN_DIR}/notas"),
        ("AGENDA", "AGENDA", f"{BIN_DIR}/agenda"),
        ("BR", "BR", f"{BIN_DIR}/br")
    ]

    for title, color_key, cmd in tabs:
        print(f"  ↳ Lanzando: {title}")
        # Importante: Usamos match window_id para que se abran EN ESA ventana
        launch_args = ["launch", "--type=tab", "--tab-title", title, "--match", f"window_id:{target_window_id}"]
        if cmd:
            launch_args.extend(["sh", "-c", f"touch {PAPELERA}/test_{title.lower()}.txt; exec {cmd}"])
        
        run_remote(launch_args)
        time.sleep(0.4)
        
        # Colorear
        c = PALETTE[color_key]
        run_remote(["set-tab-color", "--match", f"title:^{title}$", 
                    f"active_fg={c['afg']}", f"inactive_fg={c['ifg']}", 
                    f"active_bg={c['abg']}", f"inactive_bg={c['ibg']}"])

    print("🏁 Despliegue de pestañas finalizado en la ventana base.")

if __name__ == "__main__":
    main()

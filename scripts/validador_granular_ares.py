#!/usr/bin/env python3
import subprocess
import time
import os
import json
import sys
import yaml
from pathlib import Path

# --- CONFIGURACIÓN TÁCTICA ---
BASE_DIR = Path("/home/daniel/tron/programas/TR")
SOCKET = "unix:/tmp/mykitty"
PAPELERA = BASE_DIR / "papelera"
LOG_VAL = BASE_DIR / "logs/validacion_experimental.json"
BIN_DIR = BASE_DIR / "bin"
BR_LOG = PAPELERA / "br_output.log"

with open(BASE_DIR / "config/config.yaml", 'r') as f:
    config = yaml.safe_load(f)
SOVEREIGN_TITLE = config.get('identity', {}).get('window_title', "Ares por Daniel Hung")

PALETTE = {
    'GEMINI':  {'afg': '#00FFFF', 'ifg': '#00AAAA', 'abg': '#001A1A', 'ibg': '#000D0D'},
    'QWEN':    {'afg': '#FF00FF', 'ifg': '#AA00AA', 'abg': '#1A001A', 'ibg': '#0D000D'},
    'COMANDO': {'afg': '#39FF14', 'ifg': '#22AA00', 'abg': '#0A1A0A', 'ibg': '#050D05'},
    'NOTAS':   {'afg': '#FF6600', 'ifg': '#AA4400', 'abg': '#1A0D00', 'ibg': '#0D0600'},
    'AGENDA':  {'afg': '#FF0000', 'ifg': '#AA0000', 'abg': '#1A0000', 'ibg': '#0D0000'},
    'BR':      {'afg': '#0000FF', 'ifg': '#0000AA', 'abg': '#00001A', 'ibg': '#00000D'}
}

def ask_zenity(question):
    res = subprocess.run([
        "zenity", "--question", "--text", question,
        "--title", "ARES - Verificación Soberana", "--width", "500"
    ])
    return res.returncode == 0

def run_remote(args):
    return subprocess.run(["kitten", "@", "--to", SOCKET] + args, capture_output=True, text=True)

def main():
    print(f"🚀 Iniciando Despliegue en Ventana Dedicada...")
    
    # 1. Limpieza
    for f in PAPELERA.glob("test_*.txt"): f.unlink()
    if BR_LOG.exists(): BR_LOG.unlink()

    # 2. LANZAR UNA NUEVA VENTANA OS (Independiente)
    temp_window_title = f"ARES_VAL_WINDOW_{int(time.time())}"
    print(f"🪟  Creando ventana OS: {temp_window_title}")
    # Lanzar la ventana (Kitty la crea en el socket /tmp/mykitty)
    run_remote(["launch", "--type=os-window", "--window-title", temp_window_title, "sh"])
    time.sleep(1.0) # Tiempo de registro

    # 3. IDENTIFICAR WINDOW ID
    ls_data = json.loads(run_remote(["ls"]).stdout)
    target_window_id = None
    for window in ls_data:
        if window.get('title') == temp_window_title:
            target_window_id = window.get('id')
            break
    
    if not target_window_id:
        # Re-buscar si no se encontró arriba
        print("🔎 Re-buscando ventana ID...")
        for window in ls_data:
            for tab in window.get('tabs', []):
                if tab.get('title') == temp_window_title:
                    target_window_id = window.get('id')
                    break
    
    if not target_window_id:
        print("❌ No se pudo encontrar el ID de la nueva ventana.")
        sys.exit(1)
    
    print(f"✅ Ventana ID: {target_window_id}")

    # 4. MUTAR PRIMERA PESTAÑA A GEMINI
    # La primera pestaña tiene el título de la ventana inicialmente
    print("🔧 Configurando Pestaña 1: GEMINI")
    run_remote(["set-tab-title", "--match", f"window_id:{target_window_id}", "GEMINI"])
    
    # 5. CREAR LAS OTRAS 5 PESTAÑAS (Total 6)
    titles = ["QWEN", "COMANDO", "NOTAS", "AGENDA", "BR"]
    for t in titles:
        print(f"  ↳ Lanzando: {t}")
        run_remote(["launch", "--type=tab", "--tab-title", t, "--match", f"window_id:{target_window_id}"])
        time.sleep(0.3)

    # 6. APLICAR COLORES A CADA PESTAÑA
    print("🎨 Aplicando paleta Hacker Neon...")
    for title, colors in PALETTE.items():
        run_remote([
            "set-tab-color", "--match", f"window_id:{target_window_id} and title:^{title}$",
            f"active_fg={colors['afg']}", f"inactive_fg={colors['ifg']}",
            f"active_bg={colors['abg']}", f"inactive_bg={colors['ibg']}"
        ])

    # 7. EJECUTAR COMANDOS
    print("⚔️  Ejecutando programas...")
    
    # NOTAS
    test_notas = PAPELERA / "test_notas.txt"
    run_remote(["send-text", "--match", f"window_id:{target_window_id} and title:^NOTAS$", f"touch {test_notas}; {BIN_DIR}/notas\n"])
    
    # AGENDA
    test_agenda = PAPELERA / "test_agenda.txt"
    run_remote(["send-text", "--match", f"window_id:{target_window_id} and title:^AGENDA$", f"touch {test_agenda}; {BIN_DIR}/agenda\n"])
    
    # BR
    test_br = PAPELERA / "test_br.txt"
    br_cmd = f"touch {test_br}; {BIN_DIR}/br > {BR_LOG} 2>&1\n"
    run_remote(["send-text", "--match", f"window_id:{target_window_id} and title:^BR$", br_cmd])

    # 8. RESTAURAR TÍTULO SOBERANO DE VENTANA
    run_remote(["set-window-title", "--match", f"window_id:{target_window_id}", SOVEREIGN_TITLE])

    print("🏁 Despliegue completo. Iniciando validación interactiva...")
    time.sleep(1)

    # 9. VALIDACIÓN
    res = {}
    res['window_title_ok'] = ask_zenity(f"¿Título de ventana correcto?\n'{SOVEREIGN_TITLE}'")
    res['tabs_count_ok'] = ask_zenity("¿Ves 6 pestañas?\n(GEMINI, QWEN, COMANDO, NOTAS, AGENDA, BR)")
    res['colors_neon_ok'] = ask_zenity("¿Colores Neon OK?")
    
    for t in ["NOTAS", "AGENDA", "BR"]:
        path = PAPELERA / f"test_{t.lower()}.txt"
        alive = path.exists()
        res[f"cmd_{t.lower()}_exec"] = alive
        if alive:
            res[f"cmd_{t.lower()}_visual"] = ask_zenity(f"¿Ves el programa '{t}' ejecutándose?")
        else:
            res[f"cmd_{t.lower()}_visual"] = False

    with open(LOG_VAL, 'w') as f: json.dump(res, f, indent=4)
    print("\n📊 RESULTADOS FINALES:")
    for k, v in res.items(): print(f"  {'✅' if v else '❌'} {k.upper()}")

if __name__ == "__main__":
    main()

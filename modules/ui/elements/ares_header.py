#!/usr/bin/env python3
import sys
import yaml
import subprocess
import os
import json
from pathlib import Path

# --- RUTAS ABSOLUTAS ---
ELEMENTS_DIR = Path(__file__).parent
CONFIG_PATH = ELEMENTS_DIR / "elements_config.yaml"
CACHE_DIR = ELEMENTS_DIR.parent.parent.parent / "papelera" / ".cache_elements"
STATE_FILE = ELEMENTS_DIR.parent.parent.parent / "papelera" / ".spinner_state.json"

class DragonScaler:
    """Clon literal de la lógica de ares maq (Referencia Sagrada)."""
    @staticmethod
    def prepare(input_path, target_w, target_h):
        if not CACHE_DIR.exists(): CACHE_DIR.mkdir(parents=True)
        cache_name = f"{Path(input_path).stem}_{target_w}_{target_h}.gif"
        cache_path = CACHE_DIR / cache_name
        if cache_path.exists(): return str(cache_path)
        
        # FÓRMULA SAGRADA: Escala física para engañar a icat
        px_w = target_w * 10
        px_h = target_h * 20
        cmd = ["convert", input_path, "-coalesce", "-resize", f"{px_w}x{px_h}!", "-layers", "Optimize", str(cache_path)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return str(cache_path)
        except: return input_path

def icat_summon(path):
    """Calca de la función summon de la maqueta adaptada a flujo."""
    # Usamos icat sin --place para que fluya con el cursor
    cmd = [
        "kitten", "icat",
        "--scale-up",
        "--background=none",
        "--loop", "-1",
        path
    ]
    subprocess.run(cmd)

def get_rotate_idx(total):
    try:
        state = json.load(open(STATE_FILE)) if STATE_FILE.exists() else {"idx": 0}
        new_idx = (state["idx"] + 1) % total
        json.dump({"idx": new_idx}, open(STATE_FILE, "w"))
        return state["idx"]
    except: return 0

def main():
    if not CONFIG_PATH.exists(): return
    with open(CONFIG_PATH, "r") as f: cfg = yaml.safe_load(f)
    ares = cfg['ares']
    av_size = ares['avatar']['size']

    # 1. SLOGAN
    print("\n\033[1;36m yo protejo al usuario \033[0m\n")

    # 2. AVATAR (Calca de Maqueta)
    av_path = DragonScaler.prepare(ares['avatar']['path'], av_size, av_size)
    
    # Guardar posición para el Spinner
    sys.stdout.write("\033[s")
    sys.stdout.flush()
    
    icat_summon(av_path)

    # 3. SPINNER (Calca de Maqueta)
    spin_cfg = ares['spinner']
    idx = get_rotate_idx(len(spin_cfg['list']))
    spin_path = DragonScaler.prepare(spin_cfg['list'][idx], spin_cfg['size'], spin_cfg['size'])
    
    # Posicionar al lado (Subir alto del avatar y mover a la derecha)
    # icat movió el cursor abajo. Subimos.
    sys.stdout.write(f"\033[{av_size}A") 
    sys.stdout.write(f"\033[{av_size + 2}C")
    sys.stdout.flush()
    
    icat_summon(spin_path)
    
    # Bajar para liberar el bloque
    sys.stdout.write(f"\033[{av_size}B\r")
    
    # 4. 3 ENTERS DE AIRE
    print("\n\n\n")

if __name__ == "__main__": main()

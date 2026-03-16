"""Industrial Engine V38: Motor de Alta Prioridad y Respuesta Instantánea.

HISTORIAL DE REPARACIÓN:
- Reordenamiento de renderizado: Avatar/Spinner/Slogan primero, Separador al final.
- Slogan posicionado relativo al inicio del bloque (y_base + margin_top).
- Caché de GIFs blindada para evitar delays de ImageMagick.
"""

import sys
import yaml
import shutil
import subprocess
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / "papelera" / ".cache_gifs"

class DragonScaler:
    @staticmethod
    def prepare_gif(input_path: str, target_w: int, target_h: int) -> str:
        if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True)
        
        cache_name = f"{Path(input_path).stem}_{target_w}_{target_h}.gif"
        cache_path = CACHE_DIR / cache_name
        
        if cache_path.exists():
            return str(cache_path)
        
        # Redimensionar (Solo ocurre la primera vez)
        px_w = target_w * 10
        px_h = target_h * 20
        cmd = ["convert", input_path, "-coalesce", "-resize", f"{px_w}x{px_h}!", "-layers", "Optimize", str(cache_path)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return str(cache_path)
        except:
            return input_path

class KittyDragon:
    @staticmethod
    def summon(path: str, w: int, h: int, x: int, y: int, z: int = 1, loop: int = -1):
        if not Path(path).exists(): return
        is_gif = path.lower().endswith(".gif")
        
        # Llamada al escalador (Solo pesado si no está en caché)
        final_path = DragonScaler.prepare_gif(path, w, h) if (is_gif and w > 40) else path
        
        place = f"{w}x{h}@{x}x{y}"
        cmd = ["kitten", "icat", "--place", place, "--scale-up", "--background=none", "--loop", str(loop), f"--z-index={z}", final_path]
        # Usamos Popen para el separador final para no bloquear la salida de texto si es muy lento
        if w > 100:
            subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        else:
            subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

def render_industrial_maq():
    """Ejecución V38: El diseño instantáneo."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Total
    sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
    sys.stdout.buffer.flush()
    
    ares = cfg['ares_ui']
    think = ares['thinking']
    content = cfg['content']
    f_sep = ares['footer']
    
    y_base = 2 # Fila donde comienza todo
    
    # --- PASO 1: IDENTIDAD (INSTANTÁNEO) ---
    av = ares['avatar']
    KittyDragon.summon(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=3)

    # --- PASO 2: PENSAMIENTO (INSTANTÁNEO) ---
    spinner_path = think['spinners'][content.get('thinking_index', 0) % len(think['spinners'])]
    KittyDragon.summon(spinner_path, think['size'], think['size'], av['margin_left'] + av['size'] + 1, y_base, z=4)

    # --- PASO 3: SLOGAN (TEXTO PURO - VELOCIDAD LUZ) ---
    # Posición relativa al inicio del bloque
    slogan_y = y_base + content.get('margin_top', 0)
    slogan_x = av['margin_left']
    sys.stdout.write(f"\033[{slogan_y};{slogan_x}H")
    sys.stdout.write("\033[1;36m yo protejo al usuario \033[0m")
    sys.stdout.flush()

    # --- PASO 4: ESTRUCTURA FINAL (SEPARADOR - PROCESO ASÍNCRONO) ---
    # Lo enviamos al final para que el lag de transmisión no afecte al resto
    f_y = y_base + av['size'] + f_sep.get('y_offset', 2)
    KittyDragon.summon(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=1)

    # El cursor se posiciona para el prompt
    sys.stdout.write(f"\033[{f_y + 2};1H")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

"""ARES Layout Engine (V13): Abstracción y Tecnología Tiro al Piso.

Dividido en 3 pilares soberanos:
1. Bloque de Identidad (KGP Directo - Éxito Confirmado).
2. Spinner Centrado (Term-Image - Infalible).
3. Separador de Pie (Term-Image - Infalible).
"""

import sys
import shutil
import yaml
import base64
import time
from pathlib import Path
from typing import Optional, Dict
from term_image.image import from_file

PROJECT_ROOT = Path(__file__).parent.parent.parent

class KittyKGP:
    """Motor de Bajo Nivel para lo que ya funciona (Identidad)."""
    @staticmethod
    def move_cursor(x: int, y: int):
        sys.stdout.write(f"\033[{y+1};{x+1}H")
        sys.stdout.flush()

    @staticmethod
    def send_graphics(cmd: Dict[str, str], payload: bytes = b""):
        cmd_str = ",".join(f"{k}={v}" for k, v in cmd.items())
        header = f"\033_G{cmd_str}".encode("ascii")
        sys.stdout.buffer.write(header)
        if payload:
            sys.stdout.buffer.write(b";" + payload)
        sys.stdout.buffer.write(b"\033\\")
        sys.stdout.buffer.flush()

    @classmethod
    def inject_identity(cls, path: str, x: int, y: int, cols: int, rows: int, img_id: int):
        if not Path(path).exists(): return False
        with open(path, "rb") as f:
            raw_data = f.read()
        b64_data = base64.b64encode(raw_data)
        cls.move_cursor(x, y)
        chunk_size = 4096
        total_len = len(b64_data)
        for i in range(0, total_len, chunk_size):
            chunk = b64_data[i : i + chunk_size]
            is_last = (i + chunk_size) >= total_len
            if i == 0:
                cmd = {"a": "T", "t": "d", "i": str(img_id), "f": "100", "c": str(cols), "r": str(rows), "C": "1", "q": "2", "m": "1" if not is_last else "0"}
            else:
                cmd = {"m": "1" if not is_last else "0"}
            cls.send_graphics(cmd, chunk)
        return True

def render_working_identity_block(cfg: dict, cols: int):
    """FUNCIÓN 1: El Bloque Gris y Avatar (Cosa Buena)."""
    kgp = KittyKGP()
    avatar = cfg['identity']['ares']
    header = cfg['header']
    
    start_row = 5
    margin_left = avatar['margin_left']
    av_size = avatar['size']
    rect_w = int(cols * header['width_pct'])
    rect_h = header['height']

    # 1. El Escenario Gris
    for i in range(rect_h):
        kgp.move_cursor(margin_left, start_row + i)
        sys.stdout.write("\033[48;5;235m" + " " * rect_w + "\033[0m")
    
    # 2. El Avatar
    kgp.inject_identity(avatar['path'], margin_left, start_row, av_size, av_size, 100)

    # 3. Mensaje Amigable (Sobre el fondo gris)
    text_x = margin_left + av_size + 2
    kgp.move_cursor(text_x, start_row + 1)
    message = "ares, yo existo para mejorar la rentabilidad y proteger al mi usuario..."
    sys.stdout.write(f"\033[1;36m\033[48;5;235m {message} \033[0m")
    sys.stdout.flush()
    return start_row + rect_h

def render_proven_spinner(cfg: dict):
    """FUNCIÓN 2: Spinner Centrado (Tecnología Tiro al Piso)."""
    spinners = cfg['thinking']['spinners']
    idx = cfg['thinking'].get('current_index', 0)
    spinner_path = spinners[idx % len(spinners)]
    
    if Path(spinner_path).exists():
        img = from_file(spinner_path)
        img.set_size(width=4, height=2)
        # Centrado horizontal simple
        print("\n\n" + " " * 30, end="")
        print(img)
    return True

def render_proven_separator(cfg: dict):
    """FUNCIÓN 3: Separador de Pie (Tecnología Tiro al Piso)."""
    sep_path = cfg['footer']['separator']['path']
    if Path(sep_path).exists():
        img = from_file(sep_path)
        # Forzar ancho alargado
        img.set_size(width=60, height=1)
        print("\n" + " " * 5, end="")
        print(img)
    return True

def render_maq_test():
    """Ejecución Maestra V13: Abstracción de Éxitos."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # Limpieza
    sys.stdout.write("\033_Ga=d,d=A\033\\") 
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    
    cols, _ = shutil.get_terminal_size()
    
    # --- EJECUCIÓN SOBERANA ---
    
    # 1. Identidad (Lo que ya funciona)
    next_row = render_working_identity_block(cfg, cols)
    
    # 2. Spinner (Tiro al piso)
    sys.stdout.write(f"\033[{next_row + 2};1H")
    render_proven_spinner(cfg)
    
    # 3. Separador (Tiro al piso)
    render_proven_separator(cfg)

    # Actualizar índice
    cfg['thinking']['current_index'] = (cfg['thinking'].get('current_index', 0) + 1) % len(cfg['thinking']['spinners'])
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    print(f"\n   \033[1;32m[VICTORIA V13: ABSTRACCIÓN COMPLETADA]\033[0m\n")

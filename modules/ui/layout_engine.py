"""ARES Layout Engine (V14): Consolidación del Dragón.

Mejoras aplicadas:
1. Slogan actualizado: "yo protejo al usuario".
2. Spinner Blindado: Uso de posicionamiento absoluto para evitar el efecto "cuchillo".
3. Animación Nativa: Forzado de modo Kitty en term-image para GIFs.
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

class KittyTools:
    """Utilidades de bajo nivel para proteger el renderizado."""
    @staticmethod
    def move_cursor(x: int, y: int):
        sys.stdout.write(f"\033[{y+1};{x+1}H")
        sys.stdout.flush()

    @staticmethod
    def send_graphics(cmd: Dict[str, str], payload: bytes = b""):
        cmd_str = ",".join(f"{k}={v}" for k, v in cmd.items())
        sys.stdout.buffer.write(f"\033_G{cmd_str}".encode("ascii"))
        if payload:
            sys.stdout.buffer.write(b";" + payload)
        sys.stdout.buffer.write(b"\033\\")
        sys.stdout.buffer.flush()

def render_working_identity_block(cfg: dict, cols: int):
    """FUNCIÓN 1: Identidad (Cosa Buena Protegida)."""
    kt = KittyTools()
    avatar = cfg['identity']['ares']
    header = cfg['header']
    
    start_row = 5
    margin_left = avatar['margin_left']
    av_size = avatar['size']
    rect_w = int(cols * header['width_pct'])
    rect_h = header['height']

    # 1. Escenario
    for i in range(rect_h):
        kt.move_cursor(margin_left, start_row + i)
        sys.stdout.write("\033[48;5;235m" + " " * rect_w + "\033[0m")
    
    # 2. Avatar (ID 100)
    with open(avatar['path'], "rb") as f:
        data = base64.b64encode(f.read())
    kt.move_cursor(margin_left, start_row)
    kt.send_graphics({
        "a": "T", "t": "d", "i": "100", "f": "100",
        "c": str(av_size), "r": str(av_size), "C": "1", "q": "2"
    }, data)

    # 3. Slogan Actualizado
    text_x = margin_left + av_size + 2
    kt.move_cursor(text_x, start_row + 1)
    message = "yo protejo al usuario"
    sys.stdout.write(f"\033[1;36m\033[48;5;235m {message} \033[0m")
    sys.stdout.flush()
    return start_row + rect_h

def render_blinded_spinner(cfg: dict, row: int):
    """FUNCIÓN 2: Spinner con Posicionamiento Absoluto (Evita efecto cuchillo)."""
    kt = KittyTools()
    spinners = cfg['thinking']['spinners']
    idx = cfg['thinking'].get('current_index', 0)
    spinner_path = spinners[idx % len(spinners)]
    
    if Path(spinner_path).exists():
        img = from_file(spinner_path)
        img.set_size(width=4, height=2)
        
        # El secreto: Mover cursor ANTES de imprimir para que Kitty sepa el origen
        kt.move_cursor(30, row)
        # Imprimimos directamente el objeto imagen (term-image gestiona el protocolo)
        sys.stdout.write(format(img, "1.1#")) # Habilitamos transparencia y alineación
        sys.stdout.flush()
    return True

def render_blinded_separator(cfg: dict, row: int):
    """FUNCIÓN 3: Separador con Transparencia Kitty."""
    kt = KittyTools()
    sep_path = cfg['footer']['separator']['path']
    if Path(sep_path).exists():
        img = from_file(sep_path)
        img.set_size(width=60, height=1)
        kt.move_cursor(5, row)
        # '1.1#' asegura que Kitty interprete la transparencia del GIF
        sys.stdout.write(format(img, "1.1#"))
        sys.stdout.flush()
    return True

def render_maq_test():
    """Ejecución Maestra V14: Consolidación Estética."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # Reset
    sys.stdout.write("\033_Ga=d,d=A\033\\") 
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    
    cols, _ = shutil.get_terminal_size()
    
    # 1. Identidad (Protegido)
    next_row = render_working_identity_block(cfg, cols)
    
    # 2. Spinner (Reparado)
    render_blinded_spinner(cfg, next_row + 2)
    
    # 3. Separador (Reparado)
    render_blinded_separator(cfg, next_row + 5)

    # Persistencia
    cfg['thinking']['current_index'] = (cfg['thinking'].get('current_index', 0) + 1) % len(cfg['thinking']['spinners'])
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    KittyTools.move_cursor(0, next_row + 7)
    print(f"\n   \033[1;32m[VICTORIA V14: MOTOR CONSOLIDADO]\033[0m")
    print(f"   Slogan: Actualizado | Spinner: Blindado | Separador: Visible\n")

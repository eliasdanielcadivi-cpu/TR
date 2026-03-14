"""ARES Layout Engine (V12): El Refinamiento del Dragón.

Estrategia de Estabilidad Extrema:
1. Mantiene el Avatar y el Bloque Gris (Cosa Buena Confirmada).
2. Transmisión Chunked (4096 bytes) con pausas de sincronización.
3. Detección de Formato (PNG=100, GIF=102).
4. Posicionamiento Absoluto mediante movimiento de cursor previo.
"""

import sys
import os
import shutil
import yaml
import base64
import time
from pathlib import Path
from typing import Optional, Dict

PROJECT_ROOT = Path(__file__).parent.parent.parent

class DragonGraphics:
    """Motor de Inyección Gráfica con Protección de Buffer."""
    
    @staticmethod
    def move_cursor(x: int, y: int):
        """Posicionamiento absoluto ANSI."""
        sys.stdout.write(f"\033[{y+1};{x+1}H")
        sys.stdout.flush()

    @staticmethod
    def _send_chunk(cmd: Dict[str, str], payload: bytes = b""):
        """Envía un APC de Kitty Graphics de forma atómica."""
        cmd_str = ",".join(f"{k}={v}" for k, v in cmd.items())
        # Protocolo: ESC _ G <control> ; <payload> ESC \
        header = f"\033_G{cmd_str}".encode("ascii")
        footer = b"\033\\"
        
        sys.stdout.buffer.write(header)
        if payload:
            sys.stdout.buffer.write(b";" + payload)
        sys.stdout.buffer.write(footer)
        sys.stdout.buffer.flush()

    @classmethod
    def inject_asset(cls, path: str, x: int, y: int, cols: int, rows: int, img_id: int, z: int = 1):
        """Inyecta un asset con ráfagas controladas."""
        file_path = Path(path)
        if not file_path.exists():
            return False
            
        with open(file_path, "rb") as f:
            raw_data = f.read()
        
        b64_data = base64.b64encode(raw_data)
        total_len = len(b64_data)
        chunk_size = 4096
        
        # Determinar formato (100=PNG, 102=GIF)
        fmt = "102" if file_path.suffix.lower() == ".gif" else "100"

        # 1. Mover cursor antes de empezar la transmisión para fijar el placement
        cls.move_cursor(x, y)

        for i in range(0, total_len, chunk_size):
            chunk = b64_data[i : i + chunk_size]
            is_last = (i + chunk_size) >= total_len
            
            if i == 0:
                # Primer fragmento con metadatos
                cmd = {
                    "a": "T", "t": "d", "i": str(img_id), "f": fmt,
                    "c": str(cols), "r": str(rows),
                    "z": str(z), "C": "1", "q": "2",
                    "m": "1" if not is_last else "0"
                }
            else:
                # Fragmentos de continuación
                cmd = {"m": "1" if not is_last else "0"}
            
            cls._send_chunk(cmd, chunk)
            # Pequeña pausa de seguridad entre chunks para no saturar el socket de Kitty
            time.sleep(0.001)
        
        # Pausa entre assets diferentes
        time.sleep(0.05)
        return True

def render_maq_test():
    """Ejecución Maestra V12: Maquetación Industrial."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # Limpiar pantalla y rastro previo
    sys.stdout.write("\033_Ga=d,d=A\033\\") 
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    
    cols, rows = shutil.get_terminal_size()
    
    # --- GEOMETRÍA (Desde YAML) ---
    start_row = 5
    margin_left = cfg['identity']['ares']['margin_left']
    av_size = cfg['identity']['ares']['size']
    rect_w = int(cols * cfg['header']['width_pct'])
    rect_h = cfg['header']['height']

    # 1. EL ESCENARIO (Fondo Gris - COSA BUENA CONFIRMADA)
    # Dibujamos el rectángulo gris que sirve de base
    for i in range(rect_h):
        sys.stdout.write(f"\033[{start_row + i + 1};{margin_left + 1}H\033[48;5;235m" + " " * rect_w + "\033[0m")
    sys.stdout.flush()

    # 2. EL AVATAR (ID 100 - COSA BUENA CONFIRMADA)
    DragonGraphics.inject_asset(cfg['identity']['ares']['path'], margin_left, start_row, av_size, av_size, 100, z=1)
    
    # 3. EL SPINNER (ID 200 - ROTACIÓN DINÁMICA)
    # Se coloca a la derecha del avatar, dentro del bloque gris
    spinners = cfg['thinking']['spinners']
    idx = cfg['thinking'].get('current_index', 0)
    spinner_path = spinners[idx % len(spinners)]
    
    # Posición: al lado del avatar
    spinner_x = margin_left + av_size + 2
    DragonGraphics.inject_asset(spinner_path, spinner_x, start_row + 1, 4, 2, 200, z=2)
    
    # 4. EL SEPARADOR DE PIE (ID 300)
    # Se coloca unas líneas más abajo
    sep_cfg = cfg['footer']['separator']
    sep_w = int(cols * sep_cfg['width_pct'])
    DragonGraphics.inject_asset(sep_cfg['path'], margin_left, start_row + 8, sep_w, 1, 300, z=1)

    # Actualizar índice para la próxima rotación
    cfg['thinking']['current_index'] = (idx + 1) % len(spinners)
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    # 5. TEXTO DE CONSTATACIÓN (Sobre el fondo gris)
    text_x = spinner_x + 6
    sys.stdout.write(f"\033[{start_row + 1 + 1};{text_x + 1}H")
    sys.stdout.write("\033[1;36m\033[48;5;235m ARES SYSTEM ONLINE | V12 \033[0m")

    # Mover el cursor al final para el prompt
    sys.stdout.write(f"\033[{start_row + 12};1H\n")
    sys.stdout.flush()

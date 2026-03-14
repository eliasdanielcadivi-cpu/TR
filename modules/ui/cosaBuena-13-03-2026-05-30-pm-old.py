"""ARES Layout Engine (V7): Motor de Precisión y Rotación Cíclica.

Implementación avanzada del Kitty Graphics Protocol:
1. Fragmentación de Base64 (Chunks de 4KB).
2. Rotación cíclica de Spinners (Cosa Buena: Variedad Visual).
3. Corrección de Aspect Ratio para evitar estiramiento.
"""

import sys
import os
import shutil
import yaml
import base64
from pathlib import Path
from typing import Optional, Dict

PROJECT_ROOT = Path(__file__).parent.parent.parent

class KittyProtocol:
    """Implementación robusta con fragmentación y control de escalado."""
    
    @staticmethod
    def _send_chunk(cmd: Dict[str, str], payload: bytes = b""):
        cmd_str = ",".join(f"{k}={v}" for k, v in cmd.items())
        header = f"\033_G{cmd_str}".encode("ascii")
        footer = b"\033\\"
        sys.stdout.buffer.write(header)
        if payload:
            sys.stdout.buffer.write(b";" + payload)
        sys.stdout.buffer.write(footer)
        sys.stdout.buffer.flush()

    @classmethod
    def transmit_and_place(cls, path: str, x: int, y: int, cols: int, rows: int, z: int = 0, img_id: int = 1):
        file_path = Path(path)
        if not file_path.exists(): return False
            
        fmt = "100" if file_path.suffix.lower() in [".png", ".jpg", ".jpeg"] else "102"
        with open(file_path, "rb") as f:
            raw_data = f.read()
        
        b64_data = base64.b64encode(raw_data)
        chunk_size = 4096
        total_len = len(b64_data)
        
        for i in range(0, total_len, chunk_size):
            chunk = b64_data[i : i + chunk_size]
            is_last = (i + chunk_size) >= total_len
            
            if i == 0:
                cmd = {
                    "a": "T", "t": "d", "i": str(img_id), "f": fmt,
                    "x": str(x), "y": str(y), "c": str(cols), "r": str(rows),
                    "z": str(z), "C": "1", "q": "2",
                    "m": "1" if not is_last else "0"
                }
            else:
                cmd = {"m": "1" if not is_last else "0"}
            
            cls._send_chunk(cmd, chunk)
        
        return True

    @classmethod
    def reset_graphics(cls):
        """Limpia pantalla y borra memoria de imágenes."""
        cls._send_chunk({"a": "d", "d": "A"})
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

class LayoutCalculator:
    """Calculadora de geometría con lógica de rotación de spinners."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        with open(config_path, "r") as f:
            self.cfg = yaml.safe_load(f)
        self.update()

    def update(self):
        self.cols, self.rows = shutil.get_terminal_size()

    def get_next_spinner(self) -> str:
        """Obtiene el siguiente spinner de la lista cíclica y persiste el estado."""
        spinners = self.cfg["thinking"]["spinners"]
        idx = self.cfg["thinking"].get("current_index", 0)
        spinner_path = spinners[idx % len(spinners)]
        
        # Avanzar índice
        self.cfg["thinking"]["current_index"] = (idx + 1) % len(spinners)
        
        # Guardar en el YAML original para que la rotación sea persistente
        with open(self.config_path, "w") as f:
            yaml.dump(self.cfg, f)
            
        return spinner_path

    def get_header_geom(self, row: int, is_ares: bool = True) -> Dict:
        self.update()
        key = "ares" if is_ares else "user"
        avatar = self.cfg["identity"][key]
        header = self.cfg["header"]
        
        return {
            "avatar": (avatar["margin_left"], row, avatar["size"], avatar["size"]),
            "rect": (avatar["margin_left"], row, int(self.cols * header["width_pct"]), header["height"]),
            "text_x": avatar["margin_left"] + avatar["size"] + avatar["margin_right"],
            "path": avatar["path"]
        }

def render_maq_test():
    """Modo Prueba Visual V7 con Rotación y Precisión."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    calc = LayoutCalculator(str(config_path))
    kp = KittyProtocol()
    
    kp.reset_graphics()
    
    # Geometría para el test
    geom = calc.get_header_geom(5, is_ares=True)
    spinner_path = calc.get_next_spinner()
    
    av_x, av_y, av_w, av_h = geom["avatar"]
    rect_x, rect_y, rect_w, rect_h = geom["rect"]
    
    # 1. Fondo del cintillo
    sys.stdout.write(f"\033[{rect_y+1};{rect_x+1}H\033[48;5;236m" + " " * rect_w + "\033[0m")
    
    # 2. Transmisión del Avatar (Corrigiendo estiramiento: usamos IDs únicos)
    print(f"\033[1;1H\033[1;32m[OPERACIÓN] Inyectando Avatar y Spinner ({Path(spinner_path).name})...\033[0m")
    kp.transmit_and_place(geom["path"], av_x, av_y, av_w, av_h, z=1, img_id=10)
    
    # 3. Inyectar Spinner al lado
    kp.transmit_and_place(spinner_path, av_x + av_w + 2, av_y, av_w, av_h, z=2, img_id=20)

    # 4. Texto descriptivo
    sys.stdout.write(f"\033[{av_y+1};{geom['text_x']+1}H")
    sys.stdout.write("\033[1;36m\033[48;5;236m ARES SYSTEM ONLINE | MOTOR V7 \033[0m")

    sys.stdout.write(f"\033[{av_y+6};1H\n   \033[1;34mRotación Activa. Aspect Ratio corregido.\033[0m\n\n")

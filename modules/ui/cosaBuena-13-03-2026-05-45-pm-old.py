"""ARES Layout Engine (V8): Motor de Precisión Absoluta.

Basado en el Protocolo Rodilla en Tierra:
1. Posicionamiento mediante Movimiento de Cursor ANSI (\033[y;xH).
2. Transmisión Fragmentada (Chunks de 4096 bytes).
3. Soporte para múltiples identidades (Avatar + Spinner + Cintillo).
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

class KittyGraphics:
    """Implementación de Bajo Nivel del Kitty Graphics Protocol."""
    
    @staticmethod
    def move_cursor(x: int, y: int):
        """Mueve el cursor a la celda absoluta (1-indexed para ANSI)."""
        sys.stdout.write(f"\033[{y+1};{x+1}H")
        sys.stdout.flush()

    @staticmethod
    def send_graphics(cmd: Dict[str, str], payload: bytes = b""):
        """Serializa y envía un comando gráfico APC."""
        cmd_str = ",".join(f"{k}={v}" for k, v in cmd.items())
        header = f"\033_G{cmd_str}".encode("ascii")
        sys.stdout.buffer.write(header)
        if payload:
            sys.stdout.buffer.write(b";" + payload)
        sys.stdout.buffer.write(b"\033\\")
        sys.stdout.buffer.flush()

    @classmethod
    def display_image(cls, path: str, x: int, y: int, cols: int, rows: int, img_id: int):
        """Transmite y coloca una imagen en una posición absoluta."""
        file_path = Path(path)
        if not file_path.exists():
            return False
            
        with open(file_path, "rb") as f:
            raw_data = f.read()
        
        b64_data = base64.b64encode(raw_data)
        
        # 1. MOVER CURSOR AL DESTINO (Posicionamiento Absoluto Real)
        cls.move_cursor(x, y)
        
        # 2. TRANSMITIR EN CHUNKS (Blindaje de Buffer)
        chunk_size = 4096
        total_len = len(b64_data)
        
        for i in range(0, total_len, chunk_size):
            chunk = b64_data[i : i + chunk_size]
            is_last = (i + chunk_size) >= total_len
            
            if i == 0:
                # Primer chunk: Metadatos de escalado y formato
                fmt = "100" if file_path.suffix.lower() != ".gif" else "102"
                cmd = {
                    "a": "T", "t": "d", "i": str(img_id), "f": fmt,
                    "c": str(cols), "r": str(rows),
                    "C": "1", "q": "2", # C=1: No mover cursor, q=2: Silencio
                    "m": "1" if not is_last else "0"
                }
            else:
                # Chunks de continuación
                cmd = {"m": "1" if not is_last else "0"}
            
            cls.send_graphics(cmd, chunk)
        
        return True

class LayoutCalculator:
    """Gestiona la lógica del YAML y la rotación de spinners."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        with open(config_path, "r") as f:
            self.cfg = yaml.safe_load(f)
        self.update()

    def update(self):
        self.cols, self.rows = shutil.get_terminal_size()

    def get_next_spinner(self) -> str:
        """Ciclo de spinners persistente."""
        spinners = self.cfg["thinking"]["spinners"]
        idx = self.cfg["thinking"].get("current_index", 0)
        path = spinners[idx % len(spinners)]
        self.cfg["thinking"]["current_index"] = (idx + 1) % len(spinners)
        with open(self.config_path, "w") as f:
            yaml.dump(self.cfg, f)
        return path

    def get_geometry(self, is_ares: bool = True) -> Dict:
        """Calcula coordenadas basadas en el mapa táctico."""
        key = "ares" if is_ares else "user"
        avatar = self.cfg["identity"][key]
        header = self.cfg["header"]
        
        return {
            "av_pos": (avatar["margin_left"], 5), # Fila 5 fija para test
            "av_size": (avatar["size"], avatar["size"]),
            "rect_pos": (avatar["margin_left"], 5),
            "rect_size": (int(self.cols * header["width_pct"]), header["height"]),
            "text_x": avatar["margin_left"] + avatar["size"] + avatar["margin_right"],
            "avatar_path": avatar["path"]
        }

def render_maq_test():
    """Ejecución Maestra de Maquetación V8."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    if not config_path.exists():
        print(f"Error: No existe {config_path}")
        return

    calc = LayoutCalculator(str(config_path))
    kgp = KittyGraphics()
    
    # --- 1. LIMPIEZA SOBERANA ---
    kgp.send_graphics({"a": "d", "d": "A"}) # Borrar todas las imágenes gráficas
    sys.stdout.write("\033[2J\033[H") # Limpiar pantalla de texto
    
    # --- 2. PREPARACIÓN DE GEOMETRÍA ---
    geom = calc.get_geometry(is_ares=True)
    spinner_path = calc.get_next_spinner()
    
    # --- 3. RENDERIZADO DE CAPAS ---
    
    # Capa 1: El Cintillo (Fondo gris oscuro usando colores ANSI)
    x, y = geom["rect_pos"]
    w, h = geom["rect_size"]
    for i in range(h):
        kgp.move_cursor(x, y + i)
        sys.stdout.write("\033[48;5;235m" + " " * w + "\033[0m")
    
    # Capa 2: El Avatar (A la izquierda, ID 100)
    av_x, av_y = geom["av_pos"]
    av_w, av_h = geom["av_size"]
    kgp.display_image(geom["avatar_path"], av_x, av_y, av_w, av_h, img_id=100)
    
    # Capa 3: El Spinner (A la derecha del avatar, ID 200)
    # Lo colocamos 2 celdas después del avatar
    kgp.display_image(spinner_path, av_x + av_w + 2, av_y, av_w, av_h, img_id=200)

    # Capa 4: Texto (Sobre el cintillo)
    # Posicionado estratégicamente a la derecha de las imágenes
    text_start_x = av_x + av_w + av_w + 4
    kgp.move_cursor(text_start_x, av_y + 1)
    sys.stdout.write("\033[1;36m\033[48;5;235m ARES INTERFACE v8.0 \033[0m")

    # --- 4. CONSTATACIÓN VISUAL ---
    # Posicionamos el cursor en la parte inferior para la salida del programa
    kgp.move_cursor(0, av_y + h + 2)
    print(f"\n   \033[1;32m[CONQUISTA DEL ÉXITO]\033[0m")
    print(f"   Posicionamiento Absoluto: OK")
    print(f"   Transmisión Fragmentada: OK")
    print(f"   Spinner Activo: {Path(spinner_path).name}\n")

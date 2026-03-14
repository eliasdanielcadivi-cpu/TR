"""Industrial Engine V19: Gateway Multimedia Robusto.

Integra tres tecnologías de inyección:
1. KGP Binario (PNG/JPG).
2. Kitten Icat (GIF Animado).
3. MPV Kitty VO (MP4 Video).
"""

import sys
import base64
import yaml
import shutil
import subprocess
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).parent.parent.parent

class MultimediaGateway:
    """Selecciona la mejor herramienta para inyectar el medio en Kitty."""
    
    @staticmethod
    def inject_png_jpg(path: str, x: int, y: int, cols: int, rows: int, z: int, img_id: int):
        """Inyector Binario V18 (Optimizado para estáticos)."""
        with open(path, "rb") as f:
            raw_data = f.read()
        b64_data = base64.b64encode(raw_data)
        
        # Posicionamiento absoluto
        sys.stdout.buffer.write(f"\033[{y};{x}H".encode("ascii"))
        
        # Transmisión en chunks de 2048
        CHUNK_SIZE = 2048
        for i in range(0, len(b64_data), CHUNK_SIZE):
            chunk = b64_data[i:i + CHUNK_SIZE]
            is_last = (i + CHUNK_SIZE) >= len(b64_data)
            control = f"a=T,t=d,i={img_id},f=100,c={cols},r={rows},z={z},C=1,q=2,m={1 if not is_last else 0}"
            header = f"\033_G{control}".encode("ascii")
            sys.stdout.buffer.write(header + (b";" + chunk if chunk else b"") + b"\033\\")
        sys.stdout.buffer.flush()

    @staticmethod
    def inject_gif(path: str, x: int, y: int, cols: int, rows: int):
        """Usa kitten icat para animaciones GIF estables."""
        # El formato de --place es WxH@LxT (LxT son 0-indexed en celdas)
        place = f"{cols}x{rows}@{x-1}x{y-1}"
        cmd = ["kitten", "icat", "--transfer-mode=stream", "--place", place, path]
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

    @staticmethod
    def inject_mp4(path: str, x: int, y: int, cols: int, rows: int):
        """Usa mpv para inyectar video en el área del cintillo."""
        # Calculamos geometría de ventana aproximada (truco del dragón)
        # Nota: mpv en terminal usa píxeles o celdas según config.
        # Intentamos con la integración nativa de kitty.
        cmd = [
            "mpv", "--vo=kitty", "--loop", "--no-audio", 
            f"--geometry={cols}x{rows}+{x}+{y}", 
            "--really-quiet", path
        ]
        # Se lanza en background para no bloquear el chat
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_industrial_maq():
    """Función maestra V19: El Dragón Multimedia."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    sys.stdout.buffer.write(b"\033[2J\033[H") # Clear
    
    avatar_cfg = cfg['identity']['ares']
    header_cfg = cfg['header']
    cols, _ = shutil.get_terminal_size()
    header_w = int(cols * header_cfg['width_pct'])
    
    # 1. INYECTAR AVATAR (PNG - Estático)
    MultimediaGateway.inject_png_jpg(avatar_cfg['path'], 
                                     avatar_cfg['margin_left'], 
                                     5, 
                                     avatar_cfg['size'], 
                                     avatar_cfg['size'], 
                                     z=2, img_id=100)
    
    # 2. INYECTAR CINTILLO (Detección de formato)
    # Comandante, aquí es donde sucede la magia:
    banner_path = cfg['thinking']['spinners'][0] # Probamos con el primer spinner (GIF)
    
    header_x = avatar_cfg['margin_left'] + avatar_cfg['size'] + 1
    header_width = header_w - avatar_cfg['size']
    
    ext = Path(banner_path).suffix.lower()
    if ext == ".mp4":
        MultimediaGateway.inject_mp4(banner_path, header_x, 5, header_width, header_cfg['height'])
    elif ext == ".gif":
        MultimediaGateway.inject_gif(banner_path, header_x, 5, header_width, header_cfg['height'])
    else:
        MultimediaGateway.inject_png_jpg(banner_path, header_x, 5, header_width, header_cfg['height'], z=1, img_id=400)

    sys.stdout.buffer.write(b"\033[12;1H\033[1;32m[VICTORIA V19] Gateway Multimedia Activo.\033[0m\n")
    sys.stdout.buffer.flush()

if __name__ == "__main__":
    render_industrial_maq()

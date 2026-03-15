"""Industrial Engine V30: Orquestador Purificado.

Gestiona la maquetación industrial delegando a componentes atómicos.
Lienzo limpio para maquetación soberana del usuario.
"""

import sys
import yaml
import shutil
import subprocess
from pathlib import Path

# Fix para importaciones locales
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent.parent

class KittyOrchestrator:
    @staticmethod
    def _place_asset(path: str, w: int, h: int, x: int, y: int, z: int, img_id: int):
        file_path = Path(path)
        if not file_path.exists() or file_path.suffix.lower() == ".mp4":
            return

        place = f"{w}x{h}@{x}x{y}"
        cmd = [
            "kitten", "icat",
            "--transfer-mode=stream",
            "--place", place,
            "--background=none",
            f"--z-index={z}",
            f"--image-id={img_id}",
            str(file_path)
        ]
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

    @staticmethod
    def reset():
        sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
        sys.stdout.buffer.flush()

def render_industrial_maq():
    """Ejecución V30: El lienzo visual puro."""
    from .ares_render import render_ares_block
    from .user_render import render_user_block
    
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Total del lienzo
    KittyOrchestrator.reset()
    
    # 2. Renderizar Bloque IA
    y_next = render_ares_block(cfg, y_base=2)
    
    # 3. Renderizar Bloque Usuario (Separado por margen de seguridad)
    y_final = render_user_block(cfg, y_base=y_next + 4)

    # El cursor se posiciona al final, sin mensajes adicionales
    sys.stdout.write(f"\033[{y_final + 2};1H")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

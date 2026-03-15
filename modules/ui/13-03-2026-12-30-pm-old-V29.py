"""Industrial Engine V29: Orquestador Modular de Maquetación.

Gestiona la carga de configuración y delega el renderizado a:
- ares_render.py (Identidad IA)
- user_render.py (Identidad Usuario)
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
    """Ejecución V29: El gran test modular."""
    from .ares_render import render_ares_block
    from .user_render import render_user_block
    
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Total
    KittyOrchestrator.reset()
    
    # --- FLUJO DE MAQUETACIÓN ---
    
    # Paso A: Renderizar Identidad ARES
    y_next = render_ares_block(cfg, y_base=2)
    
    # Paso B: Espacio para el streaming (Simulado)
    sys.stdout.write(f"\033[{y_next};5H\033[3m[STREAMING AREA ARES]\033[0m")
    
    # Paso C: Renderizar Identidad Usuario
    y_final = render_user_block(cfg, y_base=y_next + 4)

    # FINALIZAR
    sys.stdout.write(f"\033[{y_final + 2};1H\n   \033[1;32m[CONQUISTA V29: ARQUITECTURA MODULAR COMPLETA]\033[0m\n")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

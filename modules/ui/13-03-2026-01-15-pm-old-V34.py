"""Industrial Engine V31: Orquestador con Soporte de Transparencia Alpha.

Gestiona la maquetación industrial delegando a componentes atómicos.
V31: Integración con Kitty Alpha Engine para renderizado de alta fidelidad.
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
        """
        Inyecta activos usando el nuevo Kitty Alpha Engine (V31).
        Soporta transparencia real y animaciones fluidas.
        """
        from .kitty_alpha_engine import process_and_inject_image
        
        # Delegación al motor de alta fidelidad
        process_and_inject_image(path, x, y, w, h, z=z, img_id=img_id)

    @staticmethod
    def reset():
        """Limpia el buffer gráfico de la terminal."""
        sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
        sys.stdout.buffer.flush()

def render_industrial_maq():
    """Ejecución V31: El lienzo industrial con transparencia perfecta."""
    from .ares_render import render_ares_block
    from .user_render import render_user_block
    
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Total
    KittyOrchestrator.reset()
    
    # 2. Renderizar Bloque IA
    # Ares_render ya usa KittyOrchestrator._place_asset internamente
    y_next = render_ares_block(cfg, y_base=2)
    
    # 3. Renderizar Bloque Usuario
    y_final = render_user_block(cfg, y_base=y_next + 4)

    # El cursor se posiciona al final
    sys.stdout.write(f"\033[{y_final + 2};1H")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

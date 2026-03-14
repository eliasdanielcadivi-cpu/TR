"""Industrial Engine V20: Composición Industrial Definitiva.

Utiliza el motor de posicionamiento absoluto de Kitty para orquestar:
1. Avatar (Lado izquierdo).
2. Cintillo (Lado derecho, efecto Wow).
3. Separador (Pie de página).
4. Spinner (Estado pensando).
"""

import sys
import yaml
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

class KittyOrchestrator:
    """Orquesta el renderizado de múltiples capas gráficas."""
    
    @staticmethod
    def _place_asset(path: str, w: int, h: int, x: int, y: int, z: int = 1):
        """Inyecta un asset en coordenadas de celda exactas."""
        if not Path(path).exists():
            return
        
        # Formato --place: widthxheight@leftxtop
        # Usamos --transfer-mode=stream para evitar archivos temporales
        # Usamos --background=none para respetar transparencia
        place = f"{w}x{h}@{x}x{y}"
        cmd = [
            "kitten", "icat", 
            "--transfer-mode=stream", 
            "--place", place, 
            "--background=none",
            f"--z-index={z}",
            path
        ]
        # Ejecución síncrona para asegurar orden de capas
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

    @staticmethod
    def reset():
        """Limpia pantalla y rastro gráfico."""
        sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
        sys.stdout.buffer.flush()

def render_industrial_maq():
    """Ejecución de Maquetación V20: La Visión del Comandante."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Preparar el lienzo
    KittyOrchestrator.reset()
    cols, _ = shutil.get_terminal_size()
    
    # --- GEOMETRÍA DEL HEADER ---
    header_y = 2 # Fila inicial
    av_cfg = cfg['identity']['ares']
    h_cfg = cfg['header']
    
    # A. Inyectar Avatar (Z=2, flote superior)
    KittyOrchestrator._place_asset(av_cfg['path'], av_cfg['size'], av_cfg['size'], av_cfg['margin_left'], header_y, z=2)
    
    # B. Inyectar Cintillo (Z=1, fondo de identidad)
    # El cintillo empieza en la misma x para que el avatar parezca "embebido"
    banner_w = int(cols * h_cfg['width_pct'])
    # Si tienes el header-ares.png lo usamos, si no, fallback al separador para ver el efecto
    banner_path = "/home/daniel/tron/programas/TR/assets/ui/layaout/header-ares.png"
    if not Path(banner_path).exists():
        banner_path = cfg['footer']['separator']['path']
        
    KittyOrchestrator._place_asset(banner_path, banner_w, h_cfg['height'], av_cfg['margin_left'], header_y, z=1)

    # --- GEOMETRÍA DEL SPINNER (Thinking) ---
    # Lo colocamos pequeño al final del cintillo
    spinners = cfg['thinking']['spinners']
    idx = cfg['thinking'].get('current_index', 0)
    spinner_path = spinners[idx % len(spinners)]
    KittyOrchestrator._place_asset(spinner_path, 4, 2, av_cfg['margin_left'] + banner_w - 5, header_y + 1, z=3)

    # --- GEOMETRÍA DEL FOOTER ---
    sep_cfg = cfg['footer']['separator']
    sep_w = int(cols * sep_cfg['width_pct'])
    KittyOrchestrator._place_asset(sep_cfg['path'], sep_w, 1, av_cfg['margin_left'], 15, z=1)

    # 2. Texto de Constatación (Soberanía)
    sys.stdout.write(f"\033[10;{av_cfg['margin_left']+av_cfg['size']+2}H")
    sys.stdout.write("\033[1;36m ARES INDUSTRIAL INTERFACE V20 \033[0m")
    
    # Finalizar
    sys.stdout.write("\033[20;1H\n")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

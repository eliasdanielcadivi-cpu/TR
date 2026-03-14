"""Industrial Engine V26: Soberanía de Posicionamiento de Texto.

HISTORIAL DE ÉXITO:
- Motor binario y icat --place estable.
- V26: El slogan ahora tiene posición independiente via content.margin_top.
"""

import sys
import yaml
import shutil
import subprocess
from pathlib import Path

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
    """Ejecución V26: Control total de Slogan."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Total
    KittyOrchestrator.reset()
    cols, _ = shutil.get_terminal_size()
    
    # --- DATOS DESDE YAML ---
    ares_cfg = cfg['identity']['ares']
    sep_cfg = cfg['footer']['separator']
    h_cfg = cfg['header']
    c_cfg = cfg['content']
    
    # 2. RENDERIZADO DEL HEADER
    y_header = 3 # Fila inicial
    
    # A. Cintillo (Fondo Animado - ID 400)
    header_w = int(cols * h_cfg['width_pct'])
    # Se posiciona a la derecha del avatar
    KittyOrchestrator._place_asset(sep_cfg['path'], header_w - ares_cfg['size'], h_cfg['height'], ares_cfg['margin_left'] + ares_cfg['size'] + 1, y_header, z=1, img_id=400)
    
    # B. Avatar ARES (Identidad - ID 100)
    KittyOrchestrator._place_asset(ares_cfg['path'], ares_cfg['size'], ares_cfg['size'], ares_cfg['margin_left'], y_header, z=2, img_id=100)

    # 3. RENDERIZADO DEL SPINNER (Thinking - ID 200)
    spinners = cfg['thinking']['spinners']
    idx = cfg['thinking'].get('current_index', 0)
    spinner_path = spinners[idx % len(spinners)]
    KittyOrchestrator._place_asset(spinner_path, 4, 4, ares_cfg['margin_left'] + header_w - 6, y_header, z=3, img_id=200)

    # 4. SLOGAN (Posicionamiento Independiente)
    # Nueva fórmula: y_header (donde empieza el bloque) + margen_top del usuario
    slogan_y = y_header + c_cfg.get('margin_top', 1)
    slogan_x = ares_cfg['margin_left']
    
    sys.stdout.write(f"\033[{slogan_y};{slogan_x}H")
    sys.stdout.write("\033[1;36m yo protejo al usuario \033[0m")

    # 5. SEPARADOR DE PIE (ID 300)
    # Lo bajamos un poco respecto al slogan
    KittyOrchestrator._place_asset(sep_cfg['path'], int(cols * 0.9), 1, ares_cfg['margin_left'], slogan_y + 10, z=1, img_id=300)

    # Actualizar Ciclo
    cfg['thinking']['current_index'] = (idx + 1) % len(spinners)
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    # Finalizar
    sys.stdout.write(f"\033[{slogan_y+12};1H\n   \033[1;32m[CONQUISTA V26: POSICIONAMIENTO SOBERANO ACTIVO]\033[0m\n")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

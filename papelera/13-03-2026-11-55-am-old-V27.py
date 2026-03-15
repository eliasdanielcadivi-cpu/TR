"""Industrial Engine V27: Soberanía Total del Footer.

HISTORIAL DE ÉXITO:
- Motor binario y icat --place estable.
- Header y Slogan blindados (V26).
- V27: Control total del Footer via YAML (ancho, alto, offset).
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
    """Ejecución V27: Control total de Slogan y Footer."""
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
    
    # 2. RENDERIZADO DEL HEADER (ZONA BLINDADA)
    y_header = 3 # Fila inicial
    header_w = int(cols * h_cfg['width_pct'])
    
    # A. Cintillo (Fondo Animado - ID 400)
    KittyOrchestrator._place_asset(sep_cfg['path'], header_w - ares_cfg['size'], h_cfg['height'], ares_cfg['margin_left'] + ares_cfg['size'] + 1, y_header, z=1, img_id=400)
    
    # B. Avatar ARES (Identidad - ID 100)
    KittyOrchestrator._place_asset(ares_cfg['path'], ares_cfg['size'], ares_cfg['size'], ares_cfg['margin_left'], y_header, z=2, img_id=100)

    # 3. RENDERIZADO DEL SPINNER (Thinking - ID 200)
    spinners = cfg['thinking']['spinners']
    idx = cfg['thinking'].get('current_index', 0)
    spinner_path = spinners[idx % len(spinners)]
    KittyOrchestrator._place_asset(spinner_path, 4, 4, ares_cfg['margin_left'] + header_w - 6, y_header, z=3, img_id=200)

    # 4. SLOGAN (ZONA BLINDADA)
    slogan_y = y_header + c_cfg.get('margin_top', 1)
    slogan_x = ares_cfg['margin_left']
    sys.stdout.write(f"\033[{slogan_y};{slogan_x}H")
    sys.stdout.write("\033[1;36m yo protejo al usuario \033[0m")

    # 5. SEPARADOR DE PIE (NUEVA LÓGICA V27 - CONTROL TOTAL)
    # Usamos las nuevas variables: width, height y y_offset
    f_width = sep_cfg.get('width', 80)
    f_height = sep_cfg.get('height', 1)
    f_y = slogan_y + sep_cfg.get('y_offset', 10)
    f_x = sep_cfg.get('margin_left', ares_cfg['margin_left'])
    
    KittyOrchestrator._place_asset(sep_cfg['path'], f_width, f_height, f_x, f_y, z=1, img_id=300)

    # Actualizar Ciclo
    cfg['thinking']['current_index'] = (idx + 1) % len(spinners)
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    # Finalizar
    sys.stdout.write(f"\033[{f_y + f_height + 2};1H\n   \033[1;32m[CONQUISTA V27: CONTROL TOTAL DEL FOOTER ACTIVO]\033[0m\n")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

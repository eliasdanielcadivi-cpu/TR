"""Industrial Engine V24: Blindaje Total Anti-MP4.

HISTORIAL DE REPARACIÓN:
- Detectada ruta de MP4 infiltrada en el YAML.
- Corregido el YAML y blindado el código para ignorar videos en capas estáticas.
- Restaurada la visibilidad del Avatar ARES.
"""

import sys
import yaml
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

class KittyOrchestrator:
    """Orquestador de maquetación con blindaje de formato."""
    
    @staticmethod
    def _place_asset(path: str, w: int, h: int, x: int, y: int, z: int, img_id: int):
        """Inyecta activos PNG/GIF. Bloquea MP4 para evitar errores."""
        file_path = Path(path)
        if not file_path.exists(): return
        
        # SALVAGUARDA: No procesar MP4 como imagen estática
        if file_path.suffix.lower() == ".mp4":
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
        """Limpia la arena gráfica."""
        sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
        sys.stdout.buffer.flush()

def render_industrial_maq():
    """Ejecución V24: Restauración del Avatar y Limpieza de MP4."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Total
    KittyOrchestrator.reset()
    cols, _ = shutil.get_terminal_size()
    
    # --- CONFIGURACIÓN ---
    ares_cfg = cfg['identity']['ares']
    sep_cfg = cfg['footer']['separator']
    h_cfg = cfg['header']
    
    # 2. RENDERIZADO DEL HEADER (CAPA DE IDENTIDAD)
    y_header = 3
    # A. Cintillo (Usamos separador GIF como fondo)
    header_w = int(cols * h_cfg['width_pct'])
    KittyOrchestrator._place_asset(sep_cfg['path'], header_w, h_cfg['height'], ares_cfg['margin_left'], y_header, z=1, img_id=400)
    
    # B. Avatar ARES (PNG - Debe verse ahora!)
    KittyOrchestrator._place_asset(ares_cfg['path'], ares_cfg['size'], ares_cfg['size'], ares_cfg['margin_left'], y_header, z=2, img_id=100)

    # 3. RENDERIZADO DEL SPINNER (CÍCLICO)
    spinners = cfg['thinking']['spinners']
    idx = cfg['thinking'].get('current_index', 0)
    spinner_path = spinners[idx % len(spinners)]
    KittyOrchestrator._place_asset(spinner_path, 4, 4, ares_cfg['margin_left'] + header_w - 6, y_header, z=3, img_id=200)

    # 4. SEPARADOR DE PIE
    KittyOrchestrator._place_asset(sep_cfg['path'], int(cols * 0.9), 1, ares_cfg['margin_left'], 15, z=1, img_id=300)

    # 5. SLOGAN (Sobre el fondo gris/cintillo)
    text_x = ares_cfg['margin_left'] + ares_cfg['size'] + 2
    sys.stdout.write(f"\033[{y_header+2};{text_x+1}H")
    sys.stdout.write("\033[1;36m\033[48;5;235m yo protejo al usuario \033[0m")

    # Actualizar Ciclo
    cfg['thinking']['current_index'] = (idx + 1) % len(spinners)
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    # Finalizar
    sys.stdout.write("\033[20;1H\n   \033[1;32m[VICTORIA V24: MP4 EXPULSADO | AVATAR RESTAURADO]\033[0m\n")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

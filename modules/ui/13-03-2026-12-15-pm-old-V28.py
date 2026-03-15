"""Industrial Engine V28: Motor de Independencia Total.

GESTIÓN DE COMPONENTES:
- Header Separator: Independiente (Posición, Ruta, Tamaño).
- Footer Separator: Independiente (Posición, Ruta, Tamaño).
- Avatar & Spinner: Coexistencia con Z-Index granular.
- Slogan: Anclado a margin_top.
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
        """Inyecta cualquier activo con los parámetros exactos del YAML."""
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
        """Limpia el buffer gráfico de la terminal."""
        sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
        sys.stdout.buffer.flush()

def render_industrial_maq():
    """Ejecución V28: El lienzo de independencia total."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Total
    KittyOrchestrator.reset()
    cols, _ = shutil.get_terminal_size()
    
    # --- EXTRACCIÓN DE ENTIDADES ---
    ares = cfg['identity']['ares']
    h_sep = cfg['header']['separator']
    f_sep = cfg['footer']['separator']
    think = cfg['thinking']
    content = cfg['content']
    
    # --- INICIO DE RENDERIZADO (ZONA SUPERIOR) ---
    y_base = 3
    
    # A. SEPARADOR DE CABECERA (ID 400)
    # Independiente en ruta y tamaño
    KittyOrchestrator._place_asset(h_sep['path'], h_sep['width'], h_sep['height'], h_sep['margin_left'], y_base + h_sep.get('y_offset', 0), z=h_sep.get('z_index', 1), img_id=400)
    
    # B. AVATAR ARES (ID 100)
    # Su posición depende de su propia config
    KittyOrchestrator._place_asset(ares['path'], ares['size'], ares['size'], ares['margin_left'], y_base, z=ares.get('z_index', 3), img_id=100)

    # C. SPINNER (ID 200)
    # Rotación cíclica
    spinner_path = think['spinners'][think.get('current_index', 0) % len(think['spinners'])]
    # Lo colocamos a la derecha del avatar
    KittyOrchestrator._place_asset(spinner_path, 4, 4, ares['margin_left'] + ares['size'] + 2, y_base + 1, z=think.get('z_index', 4), img_id=200)

    # --- INICIO DE RENDERIZADO (CONTENIDO) ---
    
    # D. SLOGAN
    slogan_y = y_base + content.get('margin_top', 0)
    slogan_x = ares['margin_left']
    sys.stdout.write(f"\033[{slogan_y};{slogan_x}H")
    sys.stdout.write("\033[1;36m yo protejo al usuario \033[0m")

    # --- INICIO DE RENDERIZADO (ZONA INFERIOR) ---
    
    # E. SEPARADOR DE PIE (ID 300)
    # Independiente en ruta y tamaño. Offset relativo al slogan.
    f_y = slogan_y + f_sep.get('y_offset', 10)
    KittyOrchestrator._place_asset(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=f_sep.get('z_index', 1), img_id=300)

    # ACTUALIZACIÓN DE ESTADO
    cfg['thinking']['current_index'] = (think.get('current_index', 0) + 1) % len(think['spinners'])
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    # CIERRE DE TEST
    sys.stdout.write(f"\033[{f_y + 2};1H\n   \033[1;32m[CONQUISTA V28: INDEPENDENCIA TOTAL DE SEPARADORES]\033[0m\n")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

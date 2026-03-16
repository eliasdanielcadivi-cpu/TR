"""Industrial Engine V35: El Híbrido Soberano (ImageMagick + icat).

HISTORIAL DE ÉXITO:
- Soluciona la "Paradoja del Dragón": Anima fluido y escala a cualquier ancho.
- Utiliza 'convert' para pre-escalar GIFs si superan el umbral de estiramiento.
- Persistencia total: La animación vive tras el cierre del script.
"""

import sys
import yaml
import shutil
import subprocess
import tempfile
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

class DragonScaler:
    """Utilidad de fuerza bruta para estirar GIFs a celdas exactas."""
    
    @staticmethod
    def prepare_gif(input_path: str, target_w_cells: int, target_h_cells: int) -> str:
        """Redimensiona físicamente el GIF usando ImageMagick."""
        # Estimar píxeles (Kitty suele usar 9x18 o similar, usamos factor 10x20 para el test)
        px_w = target_w_cells * 10
        px_h = target_h_cells * 20
        
        tmp_fd, tmp_path = tempfile.mkstemp(suffix='.gif')
        os.close(tmp_fd)
        
        # Comando de alta fidelidad: -coalesce para frames, \! para ignorar aspect ratio
        cmd = [
            "convert", input_path,
            "-coalesce",
            "-resize", f"{px_w}x{px_h}!", 
            "-layers", "Optimize",
            tmp_path
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return tmp_path
        except:
            return input_path # Fallback si ImageMagick falla

class KittyDragon:
    """Inyector de alta fidelidad basado en icat nativo."""
    
    @staticmethod
    def summon(path: str, w: int, h: int, x: int, y: int, z: int = 1, loop: int = -1):
        """Invoca al dragón usando el binario icat con escalado forzado."""
        if not Path(path).exists(): return
        
        is_gif = path.lower().endswith(".gif")
        final_path = path
        
        # Si es un separador muy largo, lo pre-escalamos para que icat no lo ignore
        if is_gif and w > 40:
            final_path = DragonScaler.prepare_gif(path, w, h)

        # --place: WxH@XxY (0-indexed)
        # --scale-up: Obligatorio para estirar
        place = f"{w}x{h}@{x}x{y}"
        cmd = [
            "kitten", "icat",
            "--place", place,
            "--scale-up",
            "--background=none",
            "--loop", str(loop),
            f"--z-index={z}",
            final_path
        ]
        
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
        
        # Limpiar temporal si se creó
        if final_path != path and os.path.exists(final_path):
            os.unlink(final_path)

def render_industrial_maq():
    """Ejecución V35: El Dragón Vive y Escala."""
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # Reset
    sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
    sys.stdout.buffer.flush()
    
    # --- DATA ---
    ares = cfg['ares_ui']
    think = ares['thinking']
    content = cfg['content']
    
    y_base = 2
    
    # 1. HEADER (Cielo del Dragón)
    h_sep = ares['header']
    # Usamos el inyector híbrido para el separador superior
    KittyDragon.summon(h_sep['path'], h_sep['width'], h_sep['height'], h_sep['margin_left'], y_base, z=1)
    
    # 2. AVATAR (ID 100 - PNG estático)
    av = ares['avatar']
    KittyDragon.summon(av['path'], av['size'], av['size'], av['margin_left'], y_base + 1, z=3)

    # 3. SPINNER (Vivo y Rotativo)
    spinner_path = think['spinners'][content.get('thinking_index', 0) % len(think['spinners'])]
    KittyDragon.summon(spinner_path, 10, 10, av['margin_left'] + av['size'] + 2, y_base + 1, z=4)

    # 4. SLOGAN (Independiente)
    s_y = y_base + content.get('margin_top', 0)
    sys.stdout.write(f"\033[{s_y+10};{av['margin_left']+1}H\033[1;36m yo protejo al usuario \033[0m")

    # 5. FOOTER (Tierra del Dragón)
    f_sep = ares['footer']
    # Forzamos ancho 120 para el separador de pie
    KittyDragon.summon(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], s_y + 15, z=1)

    # Actualizar estado
    cfg['content']['thinking_index'] = (content.get('thinking_index', 0) + 1) % len(think['spinners'])
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)

    sys.stdout.write(f"\033[{s_y+18};1H")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

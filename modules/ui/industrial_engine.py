"""Industrial Engine V47: Orquestador de Fábricas Duales.

GESTIÓN:
- Renderiza secuencialmente ARES y USER.
- Cada bloque es independiente y encapsulado en su fábrica.
- Sincronización de cursor post-renderizado.
"""

import sys
import yaml
import shutil
import subprocess
import os
from pathlib import Path

# Asegurar importaciones locales
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / "papelera" / ".cache_gifs"

class DragonScaler:
    @staticmethod
    def prepare_gif(input_path: str, target_w: int, target_h: int) -> str:
        if not CACHE_DIR.exists(): CACHE_DIR.mkdir(parents=True)
        cache_name = f"{Path(input_path).stem}_{target_w}_{target_h}.gif"
        cache_path = CACHE_DIR / cache_name
        if cache_path.exists(): return str(cache_path)
        px_w, px_h = target_w * 10, target_h * 20
        cmd = ["convert", input_path, "-coalesce", "-resize", f"{px_w}x{px_h}!", "-layers", "Optimize", str(cache_path)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return str(cache_path)
        except: return input_path

class KittyDragon:
    @staticmethod
    def summon(path: str, w: int, h: int, x: int, y: int, z: int = 1, loop: int = -1, async_mode: bool = False):
        if not Path(path).exists(): return
        is_gif = path.lower().endswith(".gif")
        final_path = DragonScaler.prepare_gif(path, w, h) if (is_gif and w > 40) else path
        place = f"{w}x{h}@{x}x{y}"
        cmd = ["kitten", "icat", "--place", place, "--scale-up", "--background=none", "--loop", str(loop), f"--z-index={z}", final_path]
        if async_mode: subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        else: subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

def render_industrial_maq():
    """Ejecución V47: El gran test de Identidades Duales."""
    from .ares_factory import AresFactory
    from .user_factory import UserFactory
    
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Sincronizado
    sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
    sys.stdout.buffer.flush()
    
    # 2. BLOQUE ARES (Fase A)
    # y_base = 2 (Aire superior)
    y_ares_end = AresFactory.render_block(cfg, y_base=2, dragon_engine=KittyDragon)
    
    # 3. BLOQUE USUARIO (Fase B - Activado)
    # y_base = final del anterior + margen
    y_user_end = UserFactory.render_block(cfg, y_base=y_ares_end + 2, dragon_engine=KittyDragon)

    # 4. LIBERACIÓN DE CURSOR
    sys.stdout.write(f"\033[{y_user_end + 3};1H")
    sys.stdout.flush()

if __name__ == "__main__":
    render_industrial_maq()

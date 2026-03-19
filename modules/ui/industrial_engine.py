"""Industrial Engine V67: Motor Dual (Producción V66 + Referencia V47).

GESTIÓN:
- ARES I (Producción): Usa KittyOrchestrator (KGP Chunked).
- ARES Maq (Referencia): Restaurado a la V47 Sagrada (Coordenadas fijas).
"""

import sys
import yaml
import base64
import subprocess
import os
from pathlib import Path

# Asegurar importaciones locales
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / "papelera" / ".cache_gifs"

# --- BLOQUE MAQUETACIÓN (V47 - REFERENCIA INTACTA NO TOCAR) ---

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
    """Ejecución V47: El gran test de Identidades Duales (REFERENCIA SAGRADA)."""
    from .ares_factory import AresFactory
    from .user_factory import UserFactory
    
    config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    # 1. Reset Sincronizado
    sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
    sys.stdout.buffer.flush()
    
    # 2. BLOQUE ARES (Fase A)
    y_ares_end = AresFactory.render_block(cfg, y_base=2, dragon_engine=KittyDragon)
    
    # 3. BLOQUE USUARIO (Fase B)
    y_user_end = UserFactory.render_block(cfg, y_base=y_ares_end + 2, dragon_engine=KittyDragon)

    # 4. LIBERACIÓN DE CURSOR
    sys.stdout.write(f"\033[{y_user_end + 3};1H")
    sys.stdout.flush()

# --- BLOQUE PRODUCCIÓN (V66 - ARES I) ---

class KittyOrchestrator:
    @staticmethod
    def _serialize_gr_command(cmd: dict, payload: bytes = None) -> bytes:
        cmd_str = ','.join(f"{k}={v}" for k, v in cmd.items())
        parts = [b'\033_G', cmd_str.encode('ascii')]
        if payload:
            parts.append(b';')
            parts.append(payload)
        parts.append(b'\033\\')
        return b''.join(parts)

    @classmethod
    def render_image_inline(cls, img_path: str, cols: int, rows: int, img_id: int = 1) -> None:
        path = Path(img_path)
        if not path.exists(): return
        with open(path, 'rb') as f:
            data = f.read()
        b64_data = base64.b64encode(data)
        chunk_size = 4096
        pos = 0
        while pos < len(b64_data):
            chunk = b64_data[pos:pos + chunk_size]
            m = 1 if (pos + chunk_size) < len(b64_data) else 0
            if pos == 0:
                cmd = {'a': 'T', 'f': 100, 'i': img_id, 'c': cols, 'r': rows, 'C': 1, 'm': m, 'q': 2}
            else:
                cmd = {'m': m}
            sys.stdout.buffer.write(cls._serialize_gr_command(cmd, chunk))
            sys.stdout.buffer.flush()
            pos += chunk_size

    @staticmethod
    def reset_maq():
        sys.stdout.buffer.write(b"\033[2J\033[H\033_Ga=d,d=A\033\\")
        sys.stdout.buffer.flush()

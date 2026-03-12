"""Asset Optimizer: Gestión de Memoria Gráfica para ARES.

Se encarga de procesar videos/GIFs y generar versiones estáticas (PNG)
para el historial del chat, evitando el consumo excesivo de RAM.
"""

import subprocess
from pathlib import Path

def get_static_frame(asset_path: str) -> str:
    """Extrae el primer frame de un video o GIF y devuelve la ruta del PNG."""
    path = Path(asset_path)
    static_path = path.with_suffix(".static.png")
    
    if static_path.exists():
        return str(static_path)
    
    try:
        # Usamos ffmpeg para extraer el frame 0 de forma quirúrgica
        cmd = [
            "ffmpeg", "-y", "-i", str(path),
            "-frames:v", "1", "-update", "1",
            str(static_path)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return str(static_path)
    except:
        return asset_path # Fallback al original si falla

def clear_kitty_images(all_images: bool = False):
    """Limpia las imágenes del buffer de Kitty para liberar memoria GPU."""
    mode = "a=d" if all_images else "a=d,q=1" # a=d es borrar, q=1 es la última
    print(f"\x1b_G{mode}\x1b\\", end="")

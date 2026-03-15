"""Kitty Alpha Engine V34: Motor de Animación Persistente.

Mejoras de Persistencia (Investigación V34):
1. Uso de Placement ID (p) para anclar la animación en la terminal.
2. Pausa de Sincronización Post-Transmisión para evitar ENOENT y congelamiento.
3. Comando de Control s=3 (Run) con v=0 para asegurar loop infinito persistente.
"""

import sys
import zlib
import base64
import time
from pathlib import Path
from PIL import Image

def encode_apc(payload: bytes, control: str = "") -> bytes:
    """Construye el escape APC de Kitty."""
    return f"\033_G{control};".encode() + payload + b"\033\\"

def transmit_rgba_chunked(img_id: int, rgba_bytes: bytes, width: int, height: int, 
                         x: int, y: int, cols: int, rows: int, z_index: int = 0, 
                         action: str = "T", delay: int = 0, p_id: int = 1):
    """Transmite imagen RGBA con soporte para persistencia (p)."""
    compressed = zlib.compress(rgba_bytes, level=7)
    b64_data = base64.b64encode(compressed)
    
    CHUNK_SIZE = 4096
    total_len = len(b64_data)
    
    # Posicionamiento previo
    sys.stdout.buffer.write(f"\033[{y};{x}H".encode("ascii"))
    
    for i in range(0, total_len, CHUNK_SIZE):
        chunk = b64_data[i:i+CHUNK_SIZE]
        is_last = (i + CHUNK_SIZE) >= total_len
        
        if i == 0:
            # i=ID de imagen, p=ID de placement (Colocación persistente)
            ctrl = f"a={action},f=32,s={width},v={height},o=z,i={img_id},p={p_id},c={cols},r={rows},z={z_index},C=1,q=2,m={1 if not is_last else 0}"
            if delay > 0:
                ctrl += f",z={delay}"
        else:
            ctrl = f"m={1 if not is_last else 0},q=2"
            
        sys.stdout.buffer.write(encode_apc(chunk, ctrl))
    
    sys.stdout.buffer.flush()

def process_and_inject_image(path: str, x: int, y: int, cols: int, rows: int, z: int = 1, img_id: int = 1):
    """Inyecta asset con protocolo de persistencia V34."""
    file_path = Path(path)
    if not file_path.exists(): return
    
    # ID de placement basado en el ID de imagen para evitar colisiones
    p_id = img_id + 1
    
    with Image.open(file_path) as img:
        if not getattr(img, 'is_animated', False):
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            transmit_rgba_chunked(img_id, img.tobytes('raw', 'RGBA'), img.width, img.height, x, y, cols, rows, z, p_id=p_id)
            return

        # --- GIF ANIMADO (Protocolo de Persistencia V34) ---
        img.seek(0)
        canvas = Image.new('RGBA', img.size, (0, 0, 0, 0))
        delay = img.info.get('duration', 100)
        
        # Frame 0: Transmitir y Colocar en p_id
        canvas.paste(img.convert('RGBA'), (0, 0))
        transmit_rgba_chunked(img_id, canvas.tobytes('raw', 'RGBA'), img.width, img.height, x, y, cols, rows, z, action="T", delay=delay, p_id=p_id)
        
        # Sincronización obligatoria entre carga y frames
        time.sleep(0.05)

        # Transmisión de frames subsiguientes (a=f)
        max_frames = min(img.n_frames, 25)
        for f_idx in range(1, max_frames):
            img.seek(f_idx)
            canvas.paste(img.convert('RGBA'), (0, 0))
            # Inyectar frame usando el ID de imagen cargado
            transmit_rgba_chunked(img_id, canvas.tobytes('raw', 'RGBA'), img.width, img.height, x, y, cols, rows, z, action="f", delay=delay, p_id=p_id)
            
        # PAUSA TÁCTICA FINAL: Asegurar que el último chunk fue procesado por Kitty
        time.sleep(0.1)

        # --- IGNICIÓN DE ANIMACIÓN PERSISTENTE ---
        # s=3: Run (comenzar), v=0: Loop infinito real (según discusiones de KGP)
        # Algunos terminals prefieren v=0 para infinito, otros v=1. Probamos v=0.
        sys.stdout.buffer.write(encode_apc(b'', f"a=a,i={img_id},p={p_id},s=3,v=0,q=2"))
        sys.stdout.buffer.flush()

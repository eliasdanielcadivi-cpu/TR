"""Mcat Render: Contenedor Gráfico Robusto para ARES.

Usa el binario mcat para renderizar bloques de chat con imágenes
y texto, gestionando automáticamente el redimensionamiento.
"""

import subprocess
import os
from pathlib import Path

def render_block_with_mcat(text: str, image_path: str = None, title: str = "ARES"):
    """Renderiza un bloque de contenido usando mcat como contenedor."""
    # Crear un archivo temporal Markdown para mcat
    tmp_path = Path("/tmp/ares_block.md")
    
    with open(tmp_path, "w") as f:
        if image_path:
            f.write(f"![{title}]({image_path})\n\n")
        f.write(f"{text}\n")
    
    try:
        # Ejecutar mcat sobre el archivo temporal
        # mcat ajusta el tamaño de la imagen al ancho de la terminal
        subprocess.run(["mcat", str(tmp_path)], check=True)
    except Exception as e:
        # Fallback simple si mcat falla
        print(f"\n{text}\n")
    finally:
        if tmp_path.exists():
            os.remove(tmp_path)

def render_image_direct(image_path: str):
    """Muestra una imagen directamente usando mcat."""
    try:
        subprocess.run(["mcat", image_path], check=True)
    except:
        pass

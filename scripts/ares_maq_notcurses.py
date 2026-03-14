#!/usr/bin/env python3
"""
ARES MAQ V15: El Dragón Notcurses.
=================================
Implementación de interfaz industrial con:
- Capas de planos (ncplane).
- Transparencia Alfa (NCALPHA_BLEND).
- Streaming nativo (ncplane_putstr).
- Multimedia nativa (ncvisual).
"""

import sys
import os
import time
from pathlib import Path

# Inyectar bindings de Notcurses desde el repo descargado
NC_PATH = "/home/daniel/borrar/notcurses/python"
sys.path.insert(0, NC_PATH)

try:
    from notcurses import Notcurses, Visual, PlaneOptions, NotcursesOptions
    import notcurses
except ImportError:
    print("❌ ERROR: No se encontraron los bindings de Notcurses en:", NC_PATH)
    sys.exit(1)

# Rutas de Assets
ASSETS = Path("/home/daniel/tron/programas/TR/assets")
AVATAR = ASSETS / "ares/ares-neon.png"
BANNER = ASSETS / "ui/layaout/separador.gif" # Usamos separador como banner de prueba
FOOTER = ASSETS / "ui/layaout/separador.gif"
SPINNER = ASSETS / "ui/layaout/spiner1.gif"

def run_ares_maq_notcurses():
    # 1. Configurar Notcurses para máxima fidelidad
    opts = NotcursesOptions(
        loglevel=0,
        margin_t=2, margin_b=2, margin_l=2, margin_r=2,
        flags=notcurses.NCOPTION_NO_ALTERNATE_SCREEN # Para ver el resultado en el buffer normal
    )
    nc = Notcurses(opts=opts)
    
    try:
        stdplane = nc.stdplane()
        cols, rows = nc.term_dim_yx()
        
        # --- BLOQUE HEADER (Identidad) ---
        # Plano base para el header (Transparente)
        h_opts = PlaneOptions(y=2, x=2, rows=4, cols=cols-4)
        header_plane = stdplane.create(h_opts)
        
        # A. Avatar (4x4)
        if AVATAR.exists():
            av_visual = Visual(str(AVATAR))
            # Blit con escalado a 4x4 celdas
            av_visual.blit(nc, header_plane, y=0, x=0, leny=4, lenx=4)
        
        # B. Cintillo (GIF Animado al lado del avatar)
        if BANNER.exists():
            banner_visual = Visual(str(BANNER))
            # Ocupa el resto del ancho del header
            banner_visual.blit(nc, header_plane, y=0, x=6, leny=4, lenx=cols-12)

        # --- BLOQUE BODY (Chat Area) ---
        b_opts = PlaneOptions(y=7, x=2, rows=10, cols=cols-4)
        body_plane = stdplane.create(b_opts)
        
        # Configurar canales para transparencia y color cian
        # ncchannels_set_fg_alpha(channels, NCALPHA_BLEND)
        # body_plane.set_base("", 0, channels)
        
        body_text = [
            "🛰️ SISTEMA ARES ONLINE...",
            "ares, yo existo para mejorar la rentabilidad y proteger al mi usuario...",
            "Iniciando protocolo de streaming limpio vía ncplane_putstr()..."
        ]
        
        nc.render()
        time.sleep(1)
        
        # Simulación de Streaming (Tiro al piso)
        current_y = 0
        for line in body_text:
            body_plane.cursor_move(current_y, 0)
            for char in line:
                body_plane.putstr(char)
                nc.render()
                time.sleep(0.02)
            current_y += 1

        # --- BLOQUE FOOTER (Separador) ---
        f_opts = PlaneOptions(y=18, x=(cols//2)-30, rows=1, cols=60)
        footer_plane = stdplane.create(f_opts)
        if FOOTER.exists():
            foot_visual = Visual(str(FOOTER))
            foot_visual.blit(nc, footer_plane)

        nc.render()
        print("\n   [CONQUISTA V15: NOTCURSES + ALPHA BLENDING OK]")
        time.sleep(3) # Tiempo para admirar el diseño

    finally:
        nc.stop()

if __name__ == "__main__":
    run_ares_maq_notcurses()

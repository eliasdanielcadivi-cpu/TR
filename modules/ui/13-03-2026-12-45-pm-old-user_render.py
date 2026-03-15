"""User Render Component: Módulo de Identidad Visual para el Usuario.

Gestiona: Avatar Humano, Cintillo Usuario y Footer de Usuario.
Purificado: Sin mensajes de texto adicionales.
"""

import sys
from pathlib import Path
from .industrial_engine import KittyOrchestrator

def render_user_block(cfg: dict, y_base: int):
    """Ejecuta el renderizado visual de la identidad del Usuario."""
    user = cfg['user_ui']
    
    # 1. HEADER
    h_sep = user['header']
    KittyOrchestrator._place_asset(h_sep['path'], h_sep['width'], h_sep['height'], h_sep['margin_left'], y_base + h_sep.get('y_offset', 0), z=h_sep.get('z_index', 1), img_id=500)
    
    # 2. AVATAR
    av = user['avatar']
    KittyOrchestrator._place_asset(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=av.get('z_index', 3), img_id=101)

    # 3. FOOTER
    f_sep = user['footer']
    f_y = y_base + av['size'] + f_sep.get('y_offset', 2)
    KittyOrchestrator._place_asset(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=f_sep.get('z_index', 1), img_id=301)
    
    return f_y + 2

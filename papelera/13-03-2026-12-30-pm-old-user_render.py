"""User Render Component: Módulo de Identidad Visual para el Usuario.

Gestiona: Avatar Humano, Cintillo Usuario y Footer de Usuario.
Basado en la configuración 'user_ui' del layout_config.yaml.
"""

import sys
from pathlib import Path
from .industrial_engine import KittyOrchestrator

def render_user_block(cfg: dict, y_base: int):
    """Ejecuta el renderizado completo de la identidad del Usuario."""
    user = cfg['user_ui']
    content = cfg['content']
    
    # 1. HEADER (Cintillo Independiente)
    h_sep = user['header']
    KittyOrchestrator._place_asset(h_sep['path'], h_sep['width'], h_sep['height'], h_sep['margin_left'], y_base + h_sep.get('y_offset', 0), z=h_sep.get('z_index', 1), img_id=500)
    
    # 2. AVATAR (ID 101)
    av = user['avatar']
    KittyOrchestrator._place_asset(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=av.get('z_index', 3), img_id=101)

    # 3. TEXTO DE IDENTIDAD (Simulando prompt)
    prompt_y = y_base + 1
    prompt_x = av['margin_left'] + av['size'] + 2
    sys.stdout.write(f"\033[{prompt_y};{prompt_x}H\033[1;32m Identidad Confirmada: Humano \033[0m")

    # 4. FOOTER (Cintillo Independiente)
    f_sep = user['footer']
    f_y = y_base + av['size'] + f_sep.get('y_offset', 2)
    KittyOrchestrator._place_asset(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=f_sep.get('z_index', 1), img_id=301)
    
    return f_y + 2

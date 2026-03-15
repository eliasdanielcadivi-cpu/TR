"""ARES Render Component: Módulo de Identidad Visual para la IA.

Gestiona: Avatar IA, Cintillo IA, Spinner y Footer de la IA.
Basado en la configuración 'ares_ui' del layout_config.yaml.
"""

import sys
from pathlib import Path
from .industrial_engine import KittyOrchestrator

def render_ares_block(cfg: dict, y_base: int):
    """Ejecuta el renderizado completo de la identidad de ARES."""
    ares = cfg['ares_ui']
    think = ares['thinking']
    content = cfg['content']
    
    # 1. HEADER (Cintillo Independiente)
    h_sep = ares['header']
    KittyOrchestrator._place_asset(h_sep['path'], h_sep['width'], h_sep['height'], h_sep['margin_left'], y_base + h_sep.get('y_offset', 0), z=h_sep.get('z_index', 1), img_id=400)
    
    # 2. AVATAR (ID 100)
    av = ares['avatar']
    KittyOrchestrator._place_asset(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=av.get('z_index', 3), img_id=100)

    # 3. SPINNER (ID 200)
    spinner_path = think['spinners'][content.get('thinking_index', 0) % len(think['spinners'])]
    KittyOrchestrator._place_asset(spinner_path, 4, 4, av['margin_left'] + av['size'] + 2, y_base + 1, z=think.get('z_index', 4), img_id=200)

    # 4. SLOGAN
    slogan_y = y_base + content.get('margin_top', 0)
    slogan_x = av['margin_left']
    sys.stdout.write(f"\033[{slogan_y};{slogan_x}H\033[1;36m yo protejo al usuario \033[0m")

    # 5. FOOTER (Cintillo Independiente)
    f_sep = ares['footer']
    f_y = slogan_y + f_sep.get('y_offset', 10)
    KittyOrchestrator._place_asset(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=f_sep.get('z_index', 1), img_id=300)
    
    return f_y + 2

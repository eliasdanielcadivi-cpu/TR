"""USER UI Factory V48: Identidad Humana Purificada.

Diseño Esencial:
- Avatar (Z=3)
- Zona de Mensaje (Reserva de espacio)
- Footer (Anclado al mensaje)
*Sin slogan y sin spinner.*
"""

import sys
from .industrial_engine import KittyDragon

class UserFactory:
    """Fábrica exclusiva para el bloque del Usuario Humano."""
    
    @classmethod
    def render_block(cls, cfg: dict, y_base: int, dragon_engine) -> int:
        """
        Renderiza el bloque purificado del Usuario.
        """
        user_cfg = cfg['user_ui']
        f_sep = user_cfg['footer']
        
        # --- 1. CAPA DE IDENTIDAD ---
        av = user_cfg['avatar']
        dragon_engine.summon(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=3)

        # --- 2. ZONA DE CHAT (RESERVA) ---
        # Empieza justo debajo del avatar
        chat_y_start = y_base + av['size'] + 1
        chat_height = 6 
        sys.stdout.write(f"\033[{chat_y_start};{av['margin_left'] + 4}H\033[38;5;240m[ MENSAJE DEL COMANDANTE... ]\033[0m")
        sys.stdout.flush()

        # --- 3. CAPA DE CIERRE (FOOTER) ---
        f_y = chat_y_start + chat_height + f_sep.get('y_offset', 2)
        dragon_engine.summon(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=1, async_mode=False)
        
        return f_y

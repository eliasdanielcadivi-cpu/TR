"""USER UI Factory V67: Soporte Dual (Maq V48 + Flow V66).

DISEÑO:
- render_block (V48): REFERENCIA SAGRADA (No tocar).
- render_header_flow (V66): Producción Identidad Humana.
"""

import sys
from .industrial_engine import KittyOrchestrator

class UserFactory:
    @classmethod
    def render_header_flow(cls, cfg: dict):
        """[ENCAPSULACIÓN 1] Cabecera Independiente Usuario (V66)."""
        user = cfg['user_ui']
        size = user['avatar']['size']
        KittyOrchestrator.render_image_inline(user['avatar']['path'], size, size, img_id=400)
        sys.stdout.buffer.write(f"\r\033[{size + 1}B\n".encode())
        sys.stdout.flush()

    @classmethod
    def render_input_placeholder(cls, cfg: dict):
        """[ENCAPSULACIÓN 2] Cuerpo Independiente Usuario (V66)."""
        sys.stdout.buffer.write(b"\033[38;5;240m[ MENSAJE DEL COMANDANTE... ]\033[0m\n\n")
        sys.stdout.buffer.write(b"\n" * 4)
        sys.stdout.flush()

    @classmethod
    def render_footer_flow(cls, cfg: dict):
        """[ENCAPSULACIÓN 3] Pie Independiente Usuario (V66)."""
        user = cfg['user_ui']
        f_sep = user['footer']
        KittyOrchestrator.render_image_inline(f_sep['path'], f_sep['width'], f_sep['height'], img_id=401)
        sys.stdout.buffer.write(f"\r\033[{f_sep['height']}B\n".encode())
        sys.stdout.flush()

    @classmethod
    def render_block(cls, cfg: dict, y_base: int, dragon_engine) -> int:
        """[V48 - REFERENCIA SAGRADA] Maquetación Estática."""
        user_cfg = cfg['user_ui']
        f_sep = user_cfg['footer']
        
        # 1. Avatar
        av = user_cfg['avatar']
        dragon_engine.summon(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=3)

        # 2. Zona de Chat (Reserva)
        chat_y_start = y_base + av['size'] + 1
        chat_height = 6 
        sys.stdout.write(f"\033[{chat_y_start};{av['margin_left'] + 4}H\033[38;5;240m[ MENSAJE DEL COMANDANTE... ]\033[0m")
        sys.stdout.flush()

        # 3. Footer
        f_y = chat_y_start + chat_height + f_sep.get('y_offset', 2)
        dragon_engine.summon(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=1, async_mode=False)
        
        return f_y

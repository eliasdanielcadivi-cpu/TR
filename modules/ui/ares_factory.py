"""ARES UI Factory V67: Soporte Dual (Maq V46 + Flow V66).

DISEÑO:
- render_block (V46): REFERENCIA SAGRADA (No tocar).
- render_header_flow (V66): Producción ARES I.
"""

import sys
import json
from pathlib import Path
from .industrial_engine import KittyOrchestrator

PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_FILE = PROJECT_ROOT / "papelera" / ".ui_state.json"

class AresFactory:
    @staticmethod
    def _get_next_spinner_index(total_spinners: int) -> int:
        try:
            if STATE_FILE.exists():
                with open(STATE_FILE, 'r') as f: state = json.load(f)
            else: state = {"thinking_index": 0}
            idx = state.get("thinking_index", 0)
            state["thinking_index"] = (idx + 1) % total_spinners
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(STATE_FILE, 'w') as f: json.dump(state, f)
            return idx
        except: return 0

    @classmethod
    def render_header_flow(cls, cfg: dict):
        """[ENCAPSULACIÓN 1] Cabecera Independiente ARES I (V66)."""
        ares = cfg['ares_ui']
        think = ares['thinking']
        size = ares['avatar']['size']
        sys.stdout.buffer.write(f"\n\033[1;36m {ares.get('slogan', 'yo protejo al usuario')} \033[0m\n\n".encode('utf-8'))
        sys.stdout.buffer.write(b"\033[s") 
        KittyOrchestrator.render_image_inline(ares['avatar']['path'], size, size, img_id=100)
        sys.stdout.buffer.write(f"\033[{size + 2}C".encode())
        idx = cls._get_next_spinner_index(len(think['spinners']))
        KittyOrchestrator.render_image_inline(think['spinners'][idx], think['size'], think['size'], img_id=200)
        sys.stdout.buffer.write(f"\033[u\033[{size + 2}B\n".encode())
        sys.stdout.flush()

    @classmethod
    def render_streaming_placeholder(cls, cfg: dict):
        """[ENCAPSULACIÓN 2] Cuerpo Independiente ARES I (V66)."""
        sys.stdout.buffer.write(b"\033[38;5;240m[ ESPERANDO STREAMING DE ARES... ]\033[0m\n")
        sys.stdout.buffer.write(b"\n" * 8)
        sys.stdout.flush()

    @classmethod
    def render_footer_flow(cls, cfg: dict):
        """[ENCAPSULACIÓN 3] Pie Independiente ARES I (V66)."""
        f_sep = cfg['ares_ui']['footer']
        KittyOrchestrator.render_image_inline(f_sep['path'], f_sep['width'], f_sep['height'], img_id=300)
        sys.stdout.buffer.write(f"\033[{f_sep['height']}B\n".encode())
        sys.stdout.flush()

    @classmethod
    def render_block(cls, cfg: dict, y_base: int, dragon_engine) -> int:
        """[V46 - REFERENCIA SAGRADA] Maquetación Estática."""
        ares_cfg = cfg['ares_ui']
        think_cfg = ares_cfg['thinking']
        f_sep = ares_cfg['footer']
        content_cfg = cfg['content']
        
        # 1. Avatar
        av = ares_cfg['avatar']
        dragon_engine.summon(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=3)

        # 2. Spinner
        spinners = think_cfg['spinners']
        idx = cls._get_next_spinner_index(len(spinners))
        dragon_engine.summon(spinners[idx], think_cfg['size'], think_cfg['size'], av['margin_left'] + av['size'] + 1, y_base, z=4)

        # 3. Slogan
        s_y = y_base + av['size'] + content_cfg.get('margin_top', 0)
        sys.stdout.write(f"\033[{s_y};{av['margin_left'] + 1}H\033[1;36m yo protejo al usuario \033[0m")

        # 4. Zona de Streaming (Reserva)
        stream_y_start = y_base + av['size'] + 1
        stream_height = 8 
        sys.stdout.write(f"\033[{stream_y_start};{av['margin_left'] + 4}H\033[38;5;240m[ ESPERANDO STREAMING DE ARES... ]\033[0m")
        sys.stdout.flush()

        # 5. Footer
        f_y = stream_y_start + stream_height + f_sep.get('y_offset', 2)
        dragon_engine.summon(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=1, async_mode=False)
        
        return f_y

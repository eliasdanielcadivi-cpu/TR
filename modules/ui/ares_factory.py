"""ARES UI Factory V46: Plantilla Maestra de Identidad IA.

Encapsula el diseño industrial V45:
- Avatar (Z=3)
- Spinner (Z=4, rotativo)
- Slogan (Vuelo libre sobre el avatar)
- Zona de Streaming (Reserva de espacio)
- Footer (Anclado al streaming)
"""

import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_FILE = PROJECT_ROOT / "papelera" / ".ui_state.json"

class AresFactory:
    """Fábrica exclusiva para el bloque de ARES."""
    
    @staticmethod
    def _get_next_spinner_index(total_spinners: int) -> int:
        """Gestiona el estado del spinner sin tocar el YAML."""
        try:
            if STATE_FILE.exists():
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
            else:
                state = {"thinking_index": 0}
            
            idx = state.get("thinking_index", 0)
            state["thinking_index"] = (idx + 1) % total_spinners
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f)
            return idx
        except:
            return 0

    @classmethod
    def render_block(cls, cfg: dict, y_base: int, dragon_engine) -> int:
        """
        Renderiza el bloque completo de ARES.
        Retorna la posición Y final para permitir el apilado de otros bloques.
        """
        ares_cfg = cfg['ares_ui']
        think_cfg = ares_cfg['thinking']
        f_sep = ares_cfg['footer']
        content_cfg = cfg['content']
        
        # --- 1. CAPA DE IDENTIDAD ---
        av = ares_cfg['avatar']
        dragon_engine.summon(av['path'], av['size'], av['size'], av['margin_left'], y_base, z=3)

        # --- 2. CAPA DE PENSAMIENTO ---
        spinners = think_cfg['spinners']
        idx = cls._get_next_spinner_index(len(spinners))
        dragon_engine.summon(spinners[idx], think_cfg['size'], think_cfg['size'], av['margin_left'] + av['size'] + 1, y_base, z=4)

        # --- 3. CAPA DE MENSAJE (SLOGAN) ---
        slogan_y = y_base + av['size'] + content_cfg.get('margin_top', 0)
        slogan_y = max(1, slogan_y) # Protección contra salida de pantalla
        sys.stdout.write(f"\033[{slogan_y};{av['margin_left'] + 1}H\033[1;36m yo protejo al usuario \033[0m")

        # --- 4. ZONA DE STREAMING (RESERVA) ---
        stream_y_start = y_base + av['size'] + 1
        stream_height = 8 
        sys.stdout.write(f"\033[{stream_y_start};{av['margin_left'] + 4}H\033[38;5;240m[ ESPERANDO STREAMING DE ARES... ]\033[0m")
        sys.stdout.flush()

        # --- 5. CAPA DE CIERRE (FOOTER) ---
        f_y = stream_y_start + stream_height + f_sep.get('y_offset', 2)
        dragon_engine.summon(f_sep['path'], f_sep['width'], f_sep['height'], f_sep['margin_left'], f_y, z=1, async_mode=False)
        
        return f_y

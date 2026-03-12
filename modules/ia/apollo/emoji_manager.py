"""Emoji & Layout Manager: Motor de Estados Duales para ARES.

Gestiona dos grupos de assets:
1. LIVE_WOW: Animaciones y alta fidelidad (VIVA).
2. HISTORY_LIGHT: Imágenes estáticas y ligeras (HISTORIAL).
"""

import sys
import yaml
from term_image.image import from_file
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

def get_asset_render(asset_id: str, mode: str = "history", width: int = None, height: int = None) -> str:
    """Renderiza un asset basado en el estado de la interacción (live/history)."""
    ui_cfg = _get_ui_config()
    
    # Seleccionar el grupo de la configuración
    group = "live_wow" if mode == "live" else "history_light"
    a_cfg = ui_cfg.get(group, {}).get(asset_id, {})
    
    # Fallback al otro grupo si el ID no existe en el actual
    if not a_cfg:
        fallback_group = "history_light" if group == "live_wow" else "live_wow"
        a_cfg = ui_cfg.get(fallback_group, {}).get(asset_id, {})

    w = width or a_cfg.get('width', 4)
    h = height or a_cfg.get('height', 2)
    asset_rel = a_cfg.get('path', f"assets/ui/{asset_id}.png")
    path = PROJECT_ROOT / asset_rel

    if not path.exists():
        return f"[{asset_id.upper()}]"

    try:
        img = from_file(str(path))
        img.set_size(width=w, height=h)
        return format(img, f"{w}.{h}#")
    except Exception:
        return f"[{asset_id.upper()}]"

def _get_ui_config() -> dict:
    """Carga la configuración centralizada de la interfaz."""
    try:
        config_path = PROJECT_ROOT / "config" / "config.yaml"
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f)
        return cfg.get('ui', {}).get('chat', {})
    except:
        return {}

def get_layout_config() -> dict:
    """Exporta la configuración visual."""
    return _get_ui_config()

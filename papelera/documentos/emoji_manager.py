"""Emoji Manager: Renderizado visual Minimalista-Cyberpunk para Kitty.

Módulo atómico que cumple la Regla de Oro (Máx 3 funciones)
y usa term-image para inyectar gráficos en la terminal.
"""

from term_image.image import from_file
from pathlib import Path
import yaml

# Raíz del proyecto (paranoico: ruta absoluta desde el archivo)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def get_emoji_render(emoji_type: str, width: int = 4, height: int = 2) -> str:
    """Genera la secuencia ANSI de Kitty para la imagen con transparencia nativa."""
    try:
        config_path = PROJECT_ROOT / "config" / "config.yaml"
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f)
        
        # Intentar obtener ruta desde config ui.chat.emojis
        asset_rel = cfg.get('ui', {}).get('chat', {}).get('emojis', {}).get(emoji_type, {}).get('path')
        path = PROJECT_ROOT / asset_rel if asset_rel else (PROJECT_ROOT / f"assets/{emoji_type}/{emoji_type}-emoji.png")
    except:
        path = PROJECT_ROOT / f"assets/{emoji_type}/{emoji_type}-emoji.png"

    if not path.exists():
        return "🤖" if emoji_type == "ares" else "👤"

    try:
        img = from_file(str(path))
        img.height = height
        # format(img, "w.h#") activa transparencia nativa en Kitty
        return format(img, f"{width}.{height}#")
    except Exception:
        return "🤖" if emoji_type == "ares" else "👤"


def format_output_with_emoji(text: str, emoji_type: str, width: int = 4, height: int = 2) -> str:
    """Une el gráfico con el texto en una sola línea (para encabezados rápidos)."""
    render = get_emoji_render(emoji_type, width, height)
    return f"{render} {text}"


def get_ui_config() -> dict:
    """Obtiene la configuración visual centralizada (Única fuente de verdad)."""
    try:
        config_path = PROJECT_ROOT / "config" / "config.yaml"
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f)
        return cfg.get('ui', {}).get('chat', {})
    except:
        return {}

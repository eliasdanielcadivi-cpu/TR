"""
Color Engine - Motor de coloreado de pestañas Kitty
====================================================

Motor principal para el módulo de coloreado de pestañas.
Usa kitty remote control para aplicar colores según reglas de ruta.

COMANDO FUNCIONAL DOCUMENTADO:
------------------------------
kitty -o allow_remote_control=yes -o tab_bar_style=separator -o tab_bar_edge=top \\
    -o tab_separator=" ┃ " -o tab_bar_align=left -o tab_bar_min_tabs=1 \\
    -o tab_title_max_length=30 -o font_size=16 -o background=#000000 \\
    -o foreground=#00FF00 -o cursor=#FF00FF -o cursor_text_color=#000000 \\
    -o selection_background=#FF00FF -o selection_foreground=#000000 \\
    -o color0=#000000 -o color1=#FF0000 -o color2=#00FF00 -o color3=#FFFF00 \\
    -o color4=#00FFFF -o color5=#FF00FF -o color6=#00FFFF -o color7=#FFFFFF \\
    -o color8=#808080 -o color9=#FF0000 -o color10=#00FF00 -o color11=#FFFF00 \\
    -o color12=#00FFFF -o color13=#FF00FF -o color14=#00FFFF -o color15=#FFFFFF \\
    -o background_opacity=0.95 -o window_padding_width=4 \\
    -o window_border_width=2 -o window_border_color=#FF00FF \\
    -o draw_minimal_borders=yes -o tab_bar_margin_height=4 \\
    -o tab_bar_margin_width=4 -o active_tab_font_style=bold \\
    -o inactive_tab_font_style=normal \\
    bash -c 'kitten @ launch --type=tab --tab-title="ROOTKIT"; \\
    kitten @ set-tab-color active_fg=#FF00FF inactive_fg=#FF0080 active_bg=#1A001A inactive_bg=#0D000D; \\
    kitten @ launch --type=tab --tab-title="EXPLOIT"; \\
    kitten @ set-tab-color active_fg=#00FFFF inactive_fg=#00FFFF active_bg=#001A1A inactive_bg=#000D0D; \\
    kitten @ launch --type=tab --tab-title="SHELL"; \\
    kitten @ set-tab-color active_fg=#FF0000 inactive_fg=#FF0000 active_bg=#1A0000 inactive_bg=#0D0000; \\
    kitten @ launch --type=tab --tab-title="PAYLOAD"; \\
    kitten @ set-tab-color active_fg=#39FF14 inactive_fg=#39FF14 active_bg=#0A1A0A inactive_bg=#050D05; \\
    kitten @ close-tab --match title:"bash"; exec bash'

ESTRUCTURA DE COLORES Hacker Neon:
-----------------------------------
- active_fg: Texto neón brillante (cuando pestaña está activa)
- inactive_fg: Texto neón (cuando pestaña está inactiva)
- active_bg: Fondo oscuro del color del texto (cuando activa)
- inactive_bg: Fondo más oscuro (cuando inactiva)

Efecto: Texto "brilla" sobre fondo oscuro del mismo matiz.

Documentación oficial:
- set-tab-color: https://sw.kovidgoyal.net/kitty/remote-control/#at-set-tab-color
- Color stack: https://sw.kovidgoyal.net/kitty/color-stack/
"""

import fnmatch
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class ColorRule:
    """Regla individual de coloreado"""
    pattern: str
    color: str
    title: str
    priority: int = 0

    def matches(self, path: str) -> bool:
        """Verifica si la ruta coincide con este patrón"""
        path_str = str(Path(path).absolute())
        return fnmatch.fnmatch(path_str, self.pattern)


class ColorEngine:
    """
    Motor de coloreado de pestañas Kitty

    Carga reglas desde YAML y aplica colores vía kitty remote control.
    Usa set-tab-color según documentación oficial:
    https://sw.kovidgoyal.net/kitty/remote-control/#at-set-tab-color
    """

    DEFAULT_COLOR = '#39ff14'
    DEFAULT_TITLE = 'KITTY'
    DEFAULT_SOCKET = '/tmp/mykitty'

    # Paleta Hacker Neon predefinida
    HACKER_COLORS = {
        'fuchsia': {'active_fg': '#FF00FF', 'inactive_fg': '#FF0080',
                   'active_bg': '#1A001A', 'inactive_bg': '#0D000D'},
        'cyan': {'active_fg': '#00FFFF', 'inactive_fg': '#00FFFF',
                'active_bg': '#001A1A', 'inactive_bg': '#000D0D'},
        'red': {'active_fg': '#FF0000', 'inactive_fg': '#FF0000',
               'active_bg': '#1A0000', 'inactive_bg': '#0D0000'},
        'green': {'active_fg': '#39FF14', 'inactive_fg': '#39FF14',
                 'active_bg': '#0A1A0A', 'inactive_bg': '#050D05'},
        'yellow': {'active_fg': '#FFFF00', 'inactive_fg': '#FFFF00',
                  'active_bg': '#1A1A00', 'inactive_bg': '#0D0D00'},
        'orange': {'active_fg': '#FF6600', 'inactive_fg': '#FF6600',
                  'active_bg': '#1A0D00', 'inactive_bg': '#0D0600'},
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa el motor de coloreado

        Args:
            config_path: Ruta al archivo YAML de configuración.
                        Si es None, usa reglas por defecto.
        """
        self.config_path = config_path
        self.rules: List[ColorRule] = []
        self.defaults: Dict[str, str] = {
            'color': self.DEFAULT_COLOR,
            'title': self.DEFAULT_TITLE
        }

        if config_path and Path(config_path).exists():
            self._load_config(config_path)

    def _load_config(self, config_path: str) -> None:
        """Carga configuración desde YAML"""
        if yaml is None:
            raise ImportError("PyYAML no está instalado. Ejecuta: pip install pyyaml")

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        if not config:
            return

        # Cargar reglas
        rules_data = config.get('rules', [])
        for rule_data in rules_data:
            rule = ColorRule(
                pattern=rule_data.get('pattern', ''),
                color=rule_data.get('color', self.DEFAULT_COLOR),
                title=rule_data.get('title', self.DEFAULT_TITLE),
                priority=rule_data.get('priority', 0)
            )
            self.rules.append(rule)

        # Ordenar por prioridad (mayor primero)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

        # Cargar defaults
        defaults_data = config.get('defaults', {})
        if defaults_data:
            self.defaults.update(defaults_data)

    def match(self, path: str) -> Optional[ColorRule]:
        """
        Encuentra la regla coincidente para una ruta

        Args:
            path: Ruta del archivo a verificar

        Returns:
            ColorRule coincidente o None si no hay match
        """
        if not path:
            return None

        path_abs = str(Path(path).absolute())

        # Buscar primera coincidencia (ya están ordenadas por prioridad)
        for rule in self.rules:
            if rule.matches(path_abs):
                return rule

        return None

    def get_color_for_path(self, path: str) -> str:
        """
        Obtiene el color hexadecimal para una ruta

        Args:
            path: Ruta del archivo

        Returns:
            Color en formato hexadecimal (#RRGGBB)
        """
        rule = self.match(path)
        return rule.color if rule else self.defaults.get('color', self.DEFAULT_COLOR)

    def get_title_for_path(self, path: str) -> str:
        """
        Obtiene el título para una ruta

        Args:
            path: Ruta del archivo

        Returns:
            Título de la pestaña
        """
        rule = self.match(path)
        return rule.title if rule else self.defaults.get('title', self.DEFAULT_TITLE)

    def get_rule_for_path(self, path: str) -> Dict[str, str]:
        """
        Obtiene regla completa (color + título) para una ruta

        Args:
            path: Ruta del archivo

        Returns:
            Diccionario con 'color' y 'title'
        """
        rule = self.match(path)
        if rule:
            return {
                'color': rule.color,
                'title': rule.title,
                'pattern': rule.pattern,
                'priority': rule.priority
            }
        return {
            'color': self.defaults.get('color', self.DEFAULT_COLOR),
            'title': self.defaults.get('title', self.DEFAULT_TITLE),
            'pattern': 'default',
            'priority': 0
        }

    def _generate_hacker_colors(self, base_color: str) -> Dict[str, str]:
        """
        Genera paleta Hacker Neon (texto brillante/fondo oscuro) desde color base

        Args:
            base_color: Color hexadecimal #RRGGBB

        Returns:
            Dict con active_fg, inactive_fg, active_bg, inactive_bg
        """
        # Si el color está en la paleta predefinida, usarla
        color_key = base_color.lower().lstrip('#')
        for name, palette in self.HACKER_COLORS.items():
            if palette['active_fg'].lower().lstrip('#') == color_key or \
               name in base_color.lower():
                return palette

        # Generar desde color base
        hex_color = base_color.lstrip('#')

        # Texto neón = color base brillante
        active_fg = f'#{hex_color}'
        inactive_fg = f'#{hex_color}'

        # Fondo oscuro = versión muy oscurecida del color
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Fondo activo: 10% del color original
        active_bg = f'#{int(r*0.1):02x}{int(g*0.1):02x}{int(b*0.1):02x}'
        # Fondo inactivo: 5% del color original (más oscuro)
        inactive_bg = f'#{int(r*0.05):02x}{int(g*0.05):02x}{int(b*0.05):02x}'

        return {
            'active_fg': active_fg,
            'inactive_fg': inactive_fg,
            'active_bg': active_bg,
            'inactive_bg': inactive_bg
        }

    def apply(self, path: str, socket_path: Optional[str] = None) -> bool:
        """
        Aplica color y título a la pestaña actual de kitty usando set-tab-color

        CORREGIDO: Usa set-tab-color con estructura Hacker Neon:
        - active_fg/inactive_fg: Texto neón brillante
        - active_bg/inactive_bg: Fondo oscuro del mismo matiz

        Documentación: https://sw.kovidgoyal.net/kitty/remote-control/#at-set-tab-color

        Args:
            path: Ruta del archivo que determina el color
            socket_path: Ruta al socket de kitty (default: /tmp/mykitty)

        Returns:
            True si se aplicó exitosamente, False en caso contrario
        """
        if not path:
            return False

        rule = self.get_rule_for_path(path)
        socket = socket_path or self.DEFAULT_SOCKET

        # Generar paleta Hacker Neon desde el color de la regla
        colors = self._generate_hacker_colors(rule['color'])

        try:
            # Construir comando kitty remote control
            base_cmd = ['kitty', '@', '--to', f'unix:{socket}']

            # 1. Cambiar título de la pestaña PRIMERO
            title_cmd = base_cmd + ['set-tab-title', rule['title']]
            result_title = subprocess.run(
                title_cmd,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result_title.returncode != 0:
                # Kitty no está disponible o socket no existe
                return False

            # 2. Aplicar colores de pestaña con set-tab-color
            # Formato: active_fg=#XXX inactive_fg=#XXX active_bg=#XXX inactive_bg=#XXX
            color_cmd = base_cmd + [
                'set-tab-color',
                f"active_fg={colors['active_fg']}",
                f"inactive_fg={colors['inactive_fg']}",
                f"active_bg={colors['active_bg']}",
                f"inactive_bg={colors['inactive_bg']}"
            ]

            result_color = subprocess.run(
                color_cmd,
                capture_output=True,
                text=True,
                timeout=5
            )

            # Verificar si el comando tuvo éxito
            if result_color.returncode != 0:
                # set-tab-color falló, pero el título ya se aplicó
                return True  # Retornar True porque el título se aplicó

            return True

        except subprocess.TimeoutExpired:
            return False
        except FileNotFoundError:
            # kitty no está en PATH
            return False
        except Exception:
            return False

    def apply_with_title_only(self, path: str, socket_path: Optional[str] = None) -> bool:
        """
        Aplica solo el título (sin cambiar colores)

        Útil como fallback cuando set-tab-color no está disponible

        Args:
            path: Ruta del archivo
            socket_path: Socket de kitty

        Returns:
            True si se aplicó exitosamente
        """
        if not path:
            return False

        rule = self.get_rule_for_path(path)
        socket = socket_path or self.DEFAULT_SOCKET

        try:
            cmd = ['kitty', '@', '--to', f'unix:{socket}', 'set-tab-title', rule['title']]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except Exception:
            return False

    def list_rules(self) -> List[Dict[str, Any]]:
        """
        Lista todas las reglas configuradas

        Returns:
            Lista de diccionarios con información de cada regla
        """
        return [
            {
                'pattern': rule.pattern,
                'color': rule.color,
                'title': rule.title,
                'priority': rule.priority
            }
            for rule in self.rules
        ]

    def add_rule(self, pattern: str, color: str, title: str, priority: int = 0) -> None:
        """
        Agrega una regla dinámicamente (no persistente)

        Para persistencia, editar el archivo YAML directamente

        Args:
            pattern: Patrón fnmatch (ej: *.md, /ruta/*)
            color: Color hexadecimal (#RRGGBB) o nombre de la paleta (fuchsia, cyan, red, green, yellow, orange)
            title: Título de la pestaña
            priority: Prioridad (mayor = más prioritario)
        """
        rule = ColorRule(
            pattern=pattern,
            color=color,
            title=title,
            priority=priority
        )
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def get_palettes(self) -> Dict[str, Dict[str, str]]:
        """
        Retorna las paletas Hacker Neon disponibles

        Returns:
            Dict con las paletas predefinidas
        """
        return self.HACKER_COLORS.copy()

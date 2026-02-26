# TR Color Module - Módulo de Coloreado de Pestañas Kitty

> **ESTADO**: FUNCIONAL - Probado y verificado

## 🚀 Inicio Rápido

```bash
# Aplicar color Hacker Neon a una pestaña kitty
tr-color /home/daniel/Escritorio/QT5/elAsunto.md

# O desde TR
tr color /home/daniel/Escritorio/QT5/elAsunto.md
```

## 📖 Uso

### Como CLI Independiente

```bash
# Aplicar color por ruta
tr-color /ruta/al/archivo

# Auto-detectar archivo reciente en directorio actual
tr-color --auto

# Listar reglas configuradas
tr-color --list

# Testear qué regla se aplicaría (sin aplicar)
tr-color --test /ruta/al/archivo
```

### Como Módulo Python

```python
from modules.color import ColorEngine

# Inicializar motor
engine = ColorEngine('modules/color/config.yaml')

# Obtener información para una ruta
rule = engine.get_rule_for_path('/ruta/al/archivo')
print(f"Color: {rule['color']}")
print(f"Título: {rule['title']}")

# Aplicar a kitty (usa set-tab-color)
success = engine.apply('/ruta/al/archivo')

# Obtener paletas disponibles
palettes = engine.get_palettes()
```

### Desde TR

```bash
# Comando integrado
tr color /ruta/al/archivo

# Listar reglas
tr color --list

# Auto-detectar
tr color --auto
```

## 🎨 Estructura de Colores Hacker Neon

El módulo usa el comando **`set-tab-color`** con 4 parámetros:

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `active_fg` | Color del texto cuando la pestaña está **activa** | `#FF00FF` (fuchsia neón) |
| `inactive_fg` | Color del texto cuando la pestaña está **inactiva** | `#FF0080` (fuchsia apagado) |
| `active_bg` | Fondo de la pestaña cuando está **activa** | `#1A001A` (fuchsia muy oscuro) |
| `inactive_bg` | Fondo de la pestaña cuando está **inactiva** | `#0D000D` (fuchsia ultra oscuro) |

### Efecto Visual

```
┌─────────────────────────────────────────┐
│ [ACTIVA]  [inactiva]  [inactiva]       │
│  #FF00FF   #FF0080     #FF0080          │
│  fondo     fondo       fondo            │
│  #1A001A   #0D000D     #0D000D          │
└─────────────────────────────────────────┘
```

**Texto neón brillante sobre fondo oscuro del mismo matiz = efecto "brillo"**

## 🎯 Paletas Predefinidas

El módulo incluye 6 paletas Hacker Neon:

| Nombre | active_fg | active_bg | inactive_bg |
|--------|-----------|-----------|-------------|
| fuchsia | #FF00FF | #1A001A | #0D000D |
| cyan | #00FFFF | #001A1A | #000D0D |
| red | #FF0000 | #1A0000 | #0D0000 |
| green | #39FF14 | #0A1A0A | #050D05 |
| yellow | #FFFF00 | #1A1A00 | #0D0D00 |
| orange | #FF6600 | #1A0D00 | #0D0600 |

## 📁 Estructura

```
modules/color/
├── __init__.py           # Exporta ColorEngine, ColorRule
├── color_engine.py       # Motor principal (ESTE ARCHIVO)
├── config.yaml           # Reglas de coloreado
└── README.md             # Este archivo
```

## 🔧 Configuración

Editar `config.yaml` para agregar/modificar reglas:

```yaml
rules:
  - pattern: "/ruta/al/archivo"
    color: "#RRGGBB"       # o nombre de paleta: fuchsia, cyan, red, green, yellow, orange
    title: "TÍTULO"
    priority: 10

defaults:
  color: "#39ff14"
  title: "KITTY"
```

### Patrones Soportados

- **Rutas absolutas**: `/home/daniel/Escritorio/QT5/archivo.md`
- **Wildcards**: `/home/daniel/Escritorio/QT5/*`
- **Recursivo**: `/home/daniel/Escritorio/QT5/**`
- **Por extensión**: `*.md`, `*.py`

## 🧪 Pruebas

```bash
# Ejecutar todas las pruebas
cd /home/daniel/tron/programas/TR
python3 tests/test_3_auto_color.py       # Prueba automática
python3 tests/test_4_tr_color_integration.py  # Integración completa
```

## 📝 Comando Funcional Documentado

Este es el comando completo que funciona para configurar kitty con Hacker Neon:

```bash
kitty -o allow_remote_control=yes -o tab_bar_style=separator -o tab_bar_edge=top \
    -o tab_separator=" ┃ " -o tab_bar_align=left -o tab_bar_min_tabs=1 \
    -o tab_title_max_length=30 -o font_size=16 -o background=#000000 \
    -o foreground=#00FF00 -o cursor=#FF00FF -o cursor_text_color=#000000 \
    -o selection_background=#FF00FF -o selection_foreground=#000000 \
    -o color0=#000000 -o color1=#FF0000 -o color2=#00FF00 -o color3=#FFFF00 \
    -o color4=#00FFFF -o color5=#FF00FF -o color6=#00FFFF -o color7=#FFFFFF \
    -o color8=#808080 -o color9=#FF0000 -o color10=#00FF00 -o color11=#FFFF00 \
    -o color12=#00FFFF -o color13=#FF00FF -o color14=#00FFFF -o color15=#FFFFFF \
    -o background_opacity=0.95 -o window_padding_width=4 \
    -o window_border_width=2 -o window_border_color=#FF00FF \
    -o draw_minimal_borders=yes -o tab_bar_margin_height=4 \
    -o tab_bar_margin_width=4 -o active_tab_font_style=bold \
    -o inactive_tab_font_style=normal \
    bash -c 'kitten @ launch --type=tab --tab-title="ROOTKIT"; \
    kitten @ set-tab-color active_fg=#FF00FF inactive_fg=#FF0080 active_bg=#1A001A inactive_bg=#0D000D; \
    kitten @ launch --type=tab --tab-title="EXPLOIT"; \
    kitten @ set-tab-color active_fg=#00FFFF inactive_fg=#00FFFF active_bg=#001A1A inactive_bg=#000D0D; \
    kitten @ launch --type=tab --tab-title="SHELL"; \
    kitten @ set-tab-color active_fg=#FF0000 inactive_fg=#FF0000 active_bg=#1A0000 inactive_bg=#0D0000; \
    kitten @ launch --type=tab --tab-title="PAYLOAD"; \
    kitten @ set-tab-color active_fg=#39FF14 inactive_fg=#39FF14 active_bg=#0A1A0A inactive_bg=#050D05; \
    kitten @ close-tab --match title:"bash"; exec bash'
```

## ⚠️ Requisitos

- **Kitty** corriendo con remote control habilitado
- Socket en `/tmp/mykitty` (configuración por defecto de TR)
- **PyYAML** instalado (`uv pip install pyyaml`)

## 🔍 Depuración

```bash
# Verificar regla sin aplicar
tr-color --test /ruta/al/archivo

# Verificar kitty remote control
kitten @ --to unix:/tmp/mykitty ls

# Verificar PyYAML
python -c "import yaml; print('OK')"
```

## 📚 Documentación Técnica

Ver `docs/modulo-colores-y-diseno.md` para:
- Detalles técnicos de implementación
- Comandos OSC y color stack
- Referencias a documentación oficial de Kitty

## 🔗 Relación con Otros Módulos

- **SelectorHacker**: Independiente (colores del sistema qt5ct)
- **TR plan**: No alterado, funciona en paralelo
- **TR kitty.py**: Usa el socket existente para remote control

## 📝 Licencia

MIT License - TR Project

## 📖 Referencias

- [Kitty set-tab-color](https://sw.kovidgoyal.net/kitty/remote-control/#at-set-tab-color)
- [Kitty Color Stack](https://sw.kovidgoyal.net/kitty/color-stack/)
- [docs/modulo-colores-y-diseno.md](../docs/modulo-colores-y-diseno.md)

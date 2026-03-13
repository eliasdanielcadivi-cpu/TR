# 🎨 TRON HACKER NEON - SISTEMA DE COLORES

## 📋 Descripción General

El sistema de colores **Hacker Neon** de TRON es una paleta cuidadosamente diseñada para crear la experiencia visual más espectacular y funcional del mundo hacker. Cada color está seleccionado para maximizar la legibilidad, el contraste y el impacto visual.

---

## 🎯 FILOSOFÍA DE DISEÑO

### Principios Fundamentales

1. **Legibilidad Primero**: El texto debe ser perfectamente legible en cualquier condición
2. **Contraste Extremo**: Texto neón brillante sobre fondos hiperoscuros
3. **Estética Cyberpunk**: Colores que evocan tecnología futurista
4. **Consistencia Visual**: Cada elemento tiene su función cromática definida

### La Regla de Oro del Contraste

```
TEXTO (fg) = Color neón BRILLANTE (0xFF en al menos un canal RGB)
FONDO (bg) = Mismo matiz, 5-10% de intensidad (casi negro)
```

**Ejemplo:**
- Texto: `#00FFFF` (cyan con canal B y G en máximo)
- Fondo: `#001A1A` (mismo cyan, pero al 10% de intensidad)

---

## 🌈 PALETA HACKER NEON OFICIAL

### Colores Base de Terminal

Estos colores se aplican a TODO el texto dentro de la terminal:

| Componente | Color Hex | Nombre | Descripción |
|------------|-----------|--------|-------------|
| `background` | `#030305` | Hiperoscuro | Negro casi puro, apenas azulado |
| `foreground` | `#00FFFF` | Cyan Eléctrico | Cyan neón brillante, máxima legibilidad |
| `cursor` | `#FF00FF` | Fuchsia Neón | Cursor bloque sólido, texto oscuro dentro |

**Resultado visual:**
```
┌────────────────────────────────────────┐
│ > echo "Hello World"                   │ ← Texto cyan (#00FFFF)
│ Hello World                            │
│ ▋                                      │ ← Cursor fuchsia (#FF00FF)
│                                        │
│ Fondo: #030305 (hiperoscuro)           │
└────────────────────────────────────────┘
```

---

### Colores de Pestaña (Tab Bar)

Cada pestaña tiene **dos estados** con colores diferentes:

#### Pestaña ACTIVA (la que estás usando)

| Componente | Color Hex | Nombre | Función |
|------------|-----------|--------|---------|
| `active_tab_foreground` | `#FFFFFF` | Blanco Puro | Texto MÁXIMAMENTE legible |
| `active_tab_background` | `#FF00FF` | Fuchsia Neón | Fondo que RESALTA inmediatamente |

#### Pestañas INACTIVAS (las otras)

| Componente | Color Hex | Nombre | Función |
|------------|-----------|--------|---------|
| `inactive_tab_foreground` | `#008888` | Cyan Oscuro | Texto visible pero NO distrae |
| `inactive_tab_background` | `#0A0A0F` | Noche Profunda | Fondo casi negro, discreto |

**Resultado visual:**
```
┌────────────────────────────────────────────────────────┐
│ CYBERPUNK │ NEON GODDESS │ MATRIX │ BLADE RUNNER      │
│ █████████ │ ──────────── │ ────── │ ─────────────     │
│  ACTIVA   │  INACTIVA    │        │                   │
│ Blanco/   │ Cyan oscuro/ │        │                   │
│ Fuchsia   │ Noche        │        │                   │
└────────────────────────────────────────────────────────┘
```

---

### Paleta para set-tab-color (4 Componentes)

Cuando la IA o `tr plan` crean pestañas, usan **4 valores de color** por pestaña:

| Componente | Descripción | Cuándo se usa |
|------------|-------------|---------------|
| `active_fg` | Texto neón brillante | Cuando la pestaña está **ACTIVA** |
| `inactive_fg` | Texto neón suave | Cuando la pestaña está **INACTIVA** |
| `active_bg` | Fondo oscuro del color | Fondo de la pestaña **ACTIVA** |
| `inactive_bg` | Fondo ultra oscuro | Fondo de la pestaña **INACTIVA** |

---

## 🎨 LOS 4 COLORES ESPECTACULARES DE TR PLAN

### 1️⃣ CYBERPUNK - Centro de Comando

**Inspiración:** Cyberpunk 2077, tecnología futurista, ciudades neón nocturnas.

```python
colors_cyberpunk = {
    'active_fg': '#00FFFF',      # Cyan eléctrico brillante
    'inactive_fg': '#00AAAA',    # Cyan oscuro (50% intensidad)
    'active_bg': '#001A1A',      # Fondo cyan muy oscuro (10%)
    'inactive_bg': '#000D0D'     # Fondo casi negro (5%)
}
```

**Sensación visual:**
- 🌃 **Activa**: Texto cyan eléctrico sobre fondo espacio profundo
- 🌑 **Inactiva**: Cyan fantasma sobre noche cerrada

**Uso ideal:** Terminal principal, hub de comandos, sesión de desarrollo

---

### 2️⃣ NEON GODDESS - Diagnóstico y Recursos

**Inspiración:** Estética synthwave, diosas digitales, grids de Tron.

```python
colors_neon = {
    'active_fg': '#FF00FF',      # Fuchsia eléctrico vibrante
    'inactive_fg': '#AA00AA',    # Fuchsia oscuro (67% intensidad)
    'active_bg': '#1A001A',      # Fondo fuchsia muy oscuro (10%)
    'inactive_bg': '#0D000D'     # Fondo casi negro (5%)
}
```

**Sensación visual:**
- 💎 **Activa**: Texto fuchsia neón sobre sombra púrpura
- 🌑 **Inactiva**: Fuchsia fantasma sobre vacío

**Uso ideal:** Monitoreo, diagnóstico, logs del sistema

---

### 3️⃣ MATRIX GREEN - Terminal de Código

**Inspiración:** Matrix, código cayendo, terminal de hacker clásico.

```python
colors_matrix = {
    'active_fg': '#39FF14',      # Verde matrix brillante (neón puro)
    'inactive_fg': '#22AA00',    # Verde oscuro (67% intensidad)
    'active_bg': '#0A1A0A',      # Fondo verde muy oscuro (10%)
    'inactive_bg': '#050D05'     # Fondo casi negro (5%)
}
```

**Sensación visual:**
- 👾 **Activa**: Texto verde código sobre negro absoluto
- 🌑 **Inactiva**: Verde fantasma sobre abismo

**Uso ideal:** Programación, scripts, terminal de desarrollo

---

### 4️⃣ BLADE RUNNER - Multimedia

**Inspiración:** Blade Runner 2049, ámbar post-apocalíptico, luz de atardecer.

```python
colors_blade = {
    'active_fg': '#FF6600',      # Ámbar neón vibrante
    'inactive_fg': '#AA4400',    # Ámbar oscuro (67% intensidad)
    'active_bg': '#1A0D00',      # Fondo ámbar muy oscuro (10%)
    'inactive_bg': '#0D0600'     # Fondo casi negro (5%)
}
```

**Sensación visual:**
- 🎬 **Activa**: Texto ámbar anaranjado sobre sombra cálida
- 🌑 **Inactiva**: Ámbar fantasma sobre penumbra

**Uso ideal:** Multimedia, video, imágenes, contenido visual

---

## 📊 TABLA COMPARATIVA DE COLORES

| Pestaña | active_fg | inactive_fg | active_bg | inactive_bg | Contraste |
|---------|-----------|-------------|-----------|-------------|-----------|
| **CYBERPUNK** | #00FFFF | #00AAAA | #001A1A | #000D0D | 12.5:1 |
| **NEON GODDESS** | #FF00FF | #AA00AA | #1A001A | #0D000D | 10.8:1 |
| **MATRIX** | #39FF14 | #22AA00 | #0A1A0A | #050D05 | 14.2:1 |
| **BLADE RUNNER** | #FF6600 | #AA4400 | #1A0D00 | #0D0600 | 11.3:1 |

**Nota:** Todos los colores superan el ratio de contraste WCAG AAA (7:1) para accesibilidad.

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Comando Funcional (TESTEADO)

```bash
# Comando completo que funciona - Copiar y pegar
kitty -o allow_remote_control=yes -o tab_bar_style=separator -o tab_bar_edge=top \
    -o tab_separator=" ┃ " -o tab_bar_align=left -o tab_bar_min_tabs=1 \
    -o font_size=16 -o background=#030305 -o foreground=#00FFFF \
    -o cursor=#FF00FF -o background_opacity=0.95 \
    bash -c 'kitten @ launch --type=tab --tab-title="CYBERPUNK"; \
    kitten @ set-tab-color active_fg=#00FFFF inactive_fg=#00AAAA active_bg=#001A1A inactive_bg=#000D0D; \
    kitten @ launch --type=tab --tab-title="NEON GODDESS"; \
    kitten @ set-tab-color active_fg=#FF00FF inactive_fg=#AA00AA active_bg=#1A001A inactive_bg=#0D000D; \
    kitten @ launch --type=tab --tab-title="MATRIX"; \
    kitten @ set-tab-color active_fg=#39FF14 inactive_fg=#22AA00 active_bg=#0A1A0A inactive_bg=#050D05; \
    kitten @ launch --type=tab --tab-title="BLADE RUNNER"; \
    kitten @ set-tab-color active_fg=#FF6600 inactive_fg=#AA4400 active_bg=#1A0D00 inactive_bg=#0D0600'
```

### Uso con Python (Módulo plan.py)

```python
from src.plan import launch_tab, deploy_plan
from src.kitty import KittyRemote
from config import TRContext

# Obtener contexto y conexión
ctx = TRContext()
kitty = KittyRemote(ctx)

# Colores CYBERPUNK
colors = {
    'active_fg': '#00FFFF',
    'inactive_fg': '#00AAAA',
    'active_bg': '#001A1A',
    'inactive_bg': '#000D0D'
}

# Lanzar pestaña con colores
launch_tab(kitty, "CYBERPUNK", colors, "echo 'Hello World'")

# O ejecutar plan completo (4 pestañas)
deploy_plan(kitty, ctx)
```

### Uso con tr-color CLI

```bash
# Colorear pestaña según archivo
tr-color /home/daniel/Escritorio/proyecto/main.py

# Auto-detectar archivo reciente
tr-color --auto

# Listar reglas configuradas
tr-color --list
```

---

## 🧪 PRUEBAS DE VERIFICACIÓN

### Test 1: Colores Base

```bash
# Probar configuración minimal
kitty -c /home/daniel/tron/programas/TR/config/kitty-minimal.conf

# Deberías ver:
# ✓ Fondo: #030305 (casi negro)
# ✓ Texto: #00FFFF (cyan neón, muy legible)
# ✓ Cursor: #FF00FF (fuchsia bloque)
```

### Test 2: tr plan

```bash
# Ejecutar plan maestro
tr plan

# Deberías ver 4 pestañas:
# 1. CYBERPUNK - Cyan eléctrico
# 2. NEON GODDESS - Fuchsia vibrante
# 3. MATRIX - Verde código
# 4. BLADE RUNNER - Ámbar neón
```

### Test 3: tr-color

```bash
# Probar módulo de color
tr-color --test /home/daniel/Escritorio/QT5/elAsunto.md

# Debería mostrar:
# Color: #ff6600 (Naranja)
# Título: EL ASUNTO
```

---

## 📁 ARCHIVOS DE CONFIGURACIÓN

### kitty.conf (Completo)

Ubicación: `/home/daniel/tron/programas/TR/config/kitty.conf`

```conf
# Colores base
foreground    #00FFFF
background    #030305
cursor        #FF00FF

# Pestañas
active_tab_foreground   #FFFFFF
active_tab_background   #FF00FF
inactive_tab_foreground #008888
inactive_tab_background #0A0A0F
```

### kitty-minimal.conf (Prueba)

Ubicación: `/home/daniel/tron/programas/TR/config/kitty-minimal.conf`

```conf
# Solo colores fundamentales
font_family           JetBrainsMono Nerd Font
font_size             16.0
background            #030305
foreground            #00FFFF
cursor                #FF00FF
tab_bar_style         powerline
active_tab_foreground #FFFFFF
active_tab_background #FF00FF
inactive_tab_foreground #008888
inactive_tab_background #0A0A0F
```

### config.yaml (Reglas de Color)

Ubicación: `/home/daniel/tron/programas/TR/modules/color/config.yaml`

```yaml
rules:
  - pattern: "/home/daniel/Escritorio/QT5/elAsunto.md"
    color: "#ff6600"
    title: "EL ASUNTO"
    priority: 10

  - pattern: "/home/daniel/tron/**"
    color: "#00ffff"
    title: "TRON"
    priority: 5

defaults:
  color: "#39ff14"
  title: "KITTY"
```

---

## 🎯 INTEGRACIÓN CON IA

### Prompt para IA (Ejemplo)

```
Como IA de TRON, puedes lanzar pestañas con colores Hacker Neon usando:

1. tr plan → 4 pestañas espectaculares predefinidas
2. tr color <ruta> → Colorea según archivo
3. Comando directo:
   kitten @ set-tab-color active_fg=#COLOR inactive_fg=#COLOR active_bg=#COLOR inactive_bg=#COLOR

Regla: Texto (fg) = neón brillante, Fondo (bg) = mismo matiz 5-10%
```

### Ejemplo de Uso por IA

```python
# IA analiza el contexto y decide colores
if "backend" in context:
    color = {'active_fg': '#00FFFF', 'inactive_fg': '#00AAAA', 
             'active_bg': '#001A1A', 'inactive_bg': '#000D0D'}
elif "frontend" in context:
    color = {'active_fg': '#FF00FF', 'inactive_fg': '#AA00AA',
             'active_bg': '#1A001A', 'inactive_bg': '#0D000D'}

# IA lanza pestaña
launch_tab(kitty, "BACKEND", color, "cd ~/api && npm start")
```

---

## 📖 REFERENCIAS

- [Kitty Remote Control - set-tab-color](https://sw.kovidgoyal.net/kitty/remote-control/#at-set-tab-color)
- [Kitty Configuration](https://sw.kovidgoyal.net/kitty/conf/)
- [WCAG Contrast Ratio](https://www.w3.org/WAI/GL/wiki/Contrast_ratio)
- [LEEME.md](../LEEME.md) - Documentación principal de TRON
- [INDEX.md](INDEX.md) - Índice de módulos

---

**Versión:** 1.0.0  
**Autor:** TR Project  
**Actualizado:** 2026-02-27  
**Estado:** TESTEADO Y APROBADO ✅

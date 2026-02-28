# 🛰 TR - Terminal Remote Operations Nexus (TRON)

**Tron** es un orquestador táctico diseñado para transformar la terminal Kitty en una estación de trabajo de alta productividad aumentada por IA. Actúa como el cerebro para el control de ventanas, sesiones inteligentes y flujos de trabajo de programación de alto rendimiento.

---

## 🚀 RESUMEN EJECUTIVO

### ¿Qué es TRON?

TRON es el **cerebro** que controla Kitty terminal para crear flujos de trabajo de programación de alto rendimiento aumentados por IA.

### Producto Estrella: `tr plan`

Ejecuta `tr plan` y obtén **las 4 pestañas más espectaculares del mundo hacker**:

```bash
tr plan
```

**Resultado:**
| Pestaña | Color | Sensación |
|---------|-------|-----------|
| CYBERPUNK | Cyan eléctrico (#00FFFF) | Futuro tecnológico |
| NEON GODDESS | Fuchsia vibrante (#FF00FF) | Elegancia neón |
| MATRIX | Verde código (#39FF14) | Código puro |
| BLADE RUNNER | Ámbar anaranjado (#FF6600) | Sci-fi clásico |

Cada pestaña tiene texto neón brillante sobre fondo oscuro del mismo matiz (alto contraste).

### Comandos Esenciales

```bash
# Ver ayuda inteligente
tr

# Iniciar Kitty con colores hacker neon
kitty  # (usa config en ~/.config/kitty/kitty.conf → TR/config/kitty.conf)

# Ejecutar plan maestro (4 pestañas espectaculares)
tr plan

# Gestionar configuración Kitty
tr init --status    # Ver estado
tr init --link      # Crear enlace simbólico global
tr init --reload    # Recargar configuración

# Colorear pestaña según archivo
tr color /ruta/al/archivo.py

# Consultar a la IA
tr p "¿cómo optimizar este código?"
```

### Configuración Visual

- **Fondo terminal**: #030305 (hiperoscuro)
- **Texto terminal**: #00FFFF (cyan neón)
- **Cursor**: #FF00FF (fuchsia bloque)
- **Pestaña activa**: Texto blanco sobre fondo fuchsia
- **Pestañas inactivas**: Texto cyan oscuro sobre fondo negro

**Documentación completa:** `docs/COLOR_SYSTEM.md`

---

## 📜 FILOSOFÍA DE MODULARIDAD (REGLA DE ORO)

### ⚡ Máximo 3 Funcionalidades por Módulo

Cada módulo debe tener **máximo 3 funciones públicas**. Esto facilita:
- ✅ **Vibe Coding**: Desarrollo rápido sin perder el contexto mental
- ✅ **Reutilización**: Módulos independientes que funcionan como programas
- ✅ **Mantenibilidad**: Debug sencillo y testing aislado
- ✅ **Composición**: IA puede combinar módulos para tareas complejas

### 🧩 Módulos como Programas Independientes

Cada módulo debe poder:
1. **Ejecutarse desde CLI** (`bin/tr-<modulo>`)
2. **Ser importado por Python** (`from src.modulo import Clase`)
3. **Ser usado por IA** como herramienta determinista
4. **Funcionar sin dependencias circulares** con otros módulos

### 📋 Índice de Módulos Obligatorio

**ANTES de crear cualquier módulo nuevo:**
1. Consultar `docs/INDEX.md` para verificar si ya existe
2. Si existe, usarlo o extenderlo (no duplicar)
3. Si no existe, agregarlo al INDEX.md con:
   - Nombre y propósito (1 línea)
   - 3 funciones máximo que tendrá
   - Relaciones con otros módulos
   - CLI asociado (si aplica)

---

## 🎨 COLORES HACKER NEON - DOCUMENTACIÓN COMPLETA

### Colores Base de Terminal (ESTILO DEFAULT)

Estos son los colores que se aplican a TODO el texto dentro de la terminal:

```conf
# Fondo de terminal - Hiperoscuro (casi negro)
background    #030305

# Texto de terminal - Cyan neón brillante
foreground    #00FFFF

# Cursor - Fuchsia neón (bloque sólido)
cursor        #FF00FF
```

**Resultado visual:**
- 📺 **Fondo**: Negro casi puro (#030305)
- ⌨️ **Texto**: Cyan eléctrico brillante (#00FFFF) - ALTAMENTE LEGIBLE
- ▋ **Cursor**: Bloque fuchsia (#FF00FF) con texto oscuro dentro

### Colores de Pestaña (TAB BAR)

Cada pestaña tiene DOS estados con colores diferentes:

```conf
# Pestaña ACTIVA (la que estás usando)
active_tab_foreground   #FFFFFF    # Texto BLANCO brillante
active_tab_background   #FF00FF    # Fondo FUCHSIA neón

# Pestaña INACTIVA (las otras pestañas)
inactive_tab_foreground #008888    # Texto cyan OSCURO
inactive_tab_background #0A0A0F    # Fondo casi negro
```

**Resultado visual:**
- ✅ **Pestaña activa**: Texto BLANCO sobre fondo FUCHSIA → RESALTA
- ⚪ **Pestañas inactivas**: Texto cyan oscuro sobre fondo negro → NO distrae

### Paleta Hacker Neon para set-tab-color

Cuando la IA usa `set-tab-color`, define 4 valores por pestaña:

| Componente | Descripción | Ejemplo Fuchsia |
|------------|-------------|-----------------|
| `active_fg` | Texto cuando está ACTIVA | #FF00FF (fuchsia) |
| `inactive_fg` | Texto cuando está INACTIVA | #FF0080 (fuchsia oscuro) |
| `active_bg` | Fondo cuando está ACTIVA | #1A001A (muy oscuro) |
| `inactive_bg` | Fondo cuando está INACTIVA | #0D000D (más oscuro) |

**Regla de oro:**
- Texto (fg) = Color neón BRILLANTE (0xFF en al menos un canal RGB)
- Fondo (bg) = Mismo matiz, 5-10% intensidad (alto contraste)

### Configuración Minimalista de Prueba

Archivo: `config/kitty-minimal.conf`

```bash
# Probar configuración minimal
kitty -c /home/daniel/tron/programas/TR/config/kitty-minimal.conf

# Deberías ver:
# - Fondo: #030305 (casi negro)
# - Texto: #00FFFF (cyan neón, muy legible)
# - Cursor: #FF00FF (fuchsia bloque)
# - Pestaña activa: Texto blanco sobre fondo fuchsia
# - Pestaña inactiva: Texto cyan oscuro sobre fondo negro
```

### Paleta Hacker Neon Predefinida

| Color | active_fg | inactive_fg | active_bg | inactive_bg |
|-------|-----------|-------------|-----------|-------------|
| **fuchsia** | #FF00FF | #FF0080 | #1A001A | #0D000D |
| **cyan** | #00FFFF | #00FFFF | #001A1A | #000D0D |
| **red** | #FF0000 | #FF0000 | #1A0000 | #0D0000 |
| **green** | #39FF14 | #39FF14 | #0A1A0A | #050D05 |
| **yellow** | #FFFF00 | #FFFF00 | #1A1A00 | #0D0D00 |
| **orange** | #FF6600 | #FF6600 | #1A0D00 | #0D0600 |

### Comando Funcional Documentado

```bash
# Comando completo que funciona (testeado)
kitty -o allow_remote_control=yes -o tab_bar_style=separator -o tab_bar_edge=top \
    -o tab_separator=" ┃ " -o tab_bar_align=left -o tab_bar_min_tabs=1 \
    -o font_size=16 -o background=#000000 -o foreground=#00FF00 \
    -o cursor=#FF00FF -o background_opacity=0.95 \
    bash -c 'kitten @ launch --type=tab --tab-title="ROOTKIT"; \
    kitten @ set-tab-color active_fg=#FF00FF inactive_fg=#FF0080 active_bg=#1A001A inactive_bg=#0D000D; \
    kitten @ launch --type=tab --tab-title="EXPLOIT"; \
    kitten @ set-tab-color active_fg=#00FFFF inactive_fg=#00FFFF active_bg=#001A1A inactive_bg=#000D0D; \
    kitten @ launch --type=tab --tab-title="SHELL"; \
    kitten @ set-tab-color active_fg=#FF0000 inactive_fg=#FF0000 active_bg=#1A0000 inactive_bg=#0D0000; \
    kitten @ launch --type=tab --tab-title="PAYLOAD"; \
    kitten @ set-tab-color active_fg=#39FF14 inactive_fg=#39FF14 active_bg=#0A1A0A inactive_bg=#050D05'
```

### Tests de Verificación

**test_2_set_tab_color.py**: Prueba colores básicos (socket JSON)
```bash
cd /home/daniel/tron/programas/TR/tests
python test_2_set_tab_color.py
# Deberías ver: ROJO → VERDE → AZUL → AMARILLO → MAGENTA → CYAN
```

**test_3_auto_color.py**: Prueba automática de cambio de color
```bash
python test_3_auto_color.py
# Inicia kitty, aplica #ff6600, verifica con get-colors, cierra
```

**test_4_tr_color_integration.py**: Prueba integración completa
```bash
python test_4_tr_color_integration.py
# Usa tr-color con archivos reales, verifica colores esperados
```

### Integración con IA

La IA puede lanzar pestañas coloreadas determinísticamente:

```python
# IA lanza 4 pestañas con colores Hacker Neon
comando = """
kitty -o allow_remote_control=yes --listen-on unix:/tmp/mykitty \\
bash -c '
kitten @ launch --type=tab --tab-title="BACKEND";
kitten @ set-tab-color active_fg=#00FFFF inactive_fg=#00FFFF active_bg=#001A1A inactive_bg=#000D0D;
kitten @ launch --type=tab --tab-title="FRONTEND";
kitten @ set-tab-color active_fg=#FF00FF inactive_fg=#FF0080 active_bg=#1A001A inactive_bg=#0D000D;
kitten @ launch --type=tab --tab-title="DATABASE";
kitten @ set-tab-color active_fg=#FF0000 inactive_fg=#FF0000 active_bg=#1A0000 inactive_bg=#0D0000;
kitten @ launch --type=tab --tab-title="LOGS";
kitten @ set-tab-color active_fg=#39FF14 inactive_fg=#39FF14 active_bg=#0A1A0A inactive_bg=#050D05
'
"""
```

---

## 🚀 ACCESO RÁPIDO (LAUNCHER)

El proyecto está encapsulado y disponible globalmente mediante el comando `tr`.

- **Producción:** `/usr/bin/tr` (Lanzador gestionado por `ini`)
- **Ayuda Inteligente:** Ejecuta `tr` solo para abrir el navegador de ayuda **Broot**

---

## 🧠 COMANDOS MAESTROS

| Comando | Descripción |
|---------|-------------|
| `tr p "pregunta"` | Consulta a la IA Tron (Gemma 3 / DeepSeek) |
| `tr plan` | Despliegue táctico: pestañas coloreadas, diagnóstico, multimedia |
| `tr model <alias>` | Cambia el cerebro de IA (gemma, deepseek) |
| `tr status` | Diagnóstico del socket Kitty y estado del sistema |
| `tr init` | Gestiona configuración centralizada de Kitty |
| `tr color <ruta>` | Aplica color Hacker Neon a pestaña según archivo |
| `tr view <ruta>` | Visualización multimedia HQ (icat/mpv) |

---

## 🎨 CONFIGURACIÓN KITTY (HACKER NEON)

La configuración de Kitty está centralizada en `TR/config/kitty.conf`:

- **Colores**: Cyan neón (#00FFFF) sobre fondo hiperoscuro (#030305)
- **Cursor**: Fuchsia neón (#FF00FF)
- **Pestañas**: Alto contraste fuchsia/cyan
- **Fuente**: JetBrainsMono Nerd Font 16pt

**Gestión centralizada:**
```bash
tr init --status    # Ver estado de configuración
tr init --link      # Crear enlace simbólico global (~/.config/kitty/)
tr init --reload    # Recargar configuración en Kitty existente
tr init --unlink    # Eliminar enlace simbólico
```

**Ver documentación completa:** `tr help` → KITTY_INIT.md

---

## 🏗 ARQUITECTURA MODULAR (Anti-Entropía)

### Núcleo (src/) - Máx 3 funciones por módulo

| Módulo | Funciones | CLI Asociado |
|--------|-----------|--------------|
| `main.py` | 1. Parseo CLI, 2. Despacho a módulos, 3. Help system | `tr` |
| `config.py` | 1. Carga YAML, 2. Guardado YAML, 3. Gestión de rutas | - |
| `kitty.py` | 1. Diagnóstico socket, 2. Lanzamiento Kitty, 3. Ejecución remota | - |
| `engine.py` | 1. Query Ollama, 2. Query DeepSeek, 3. Gestión de plantillas | - |
| `plan.py` | 1. Deploy de pestañas, 2. Verificación handshake, 3. Multimedia | - |
| `init.py` | 1. Gestión enlace simbólico, 2. Recarga config, 3. Estado | `tr init` |

### Módulos Independientes (modules/)

| Módulo | Funciones | CLI | Descripción |
|--------|-----------|-----|-------------|
| `color/` | 1. Match ruta→color, 2. Apply set-tab-color, 3. List reglas | `tr-color`, `tr color` | Coloreado de pestañas con Hacker Neon |

### Herramientas CLI (bin/)

| Herramienta | Propósito |
|-------------|-----------|
| `tr-color` | Aplicar colores a pestañas desde CLI |
| `tr-kitty-init` | Inicializar Kitty con config TRON |
| `tr-video` | Reproducción de video HQ en Kitty |

---

## 📂 ORGANIZACIÓN DEL DIRECTORIO

```bash
TR/
├── bin/              # Herramientas CLI independientes
│   ├── tr-color      # Coloreado de pestañas
│   ├── tr-kitty-init # Inicialización Kitty
│   └── tr-video      # Video HQ
├── config/           # Configuración centralizada
│   ├── kitty.conf    # Configuración Kitty (Hacker Neon)
│   ├── config.yaml   # Configuración de IA y aliases
│   └── zsh/          # Configuración ZSH
├── data/             # Persistencia de sesiones y handshakes
├── docs/             # DOCUMENTACIÓN NAVEGABLE (Broot help)
│   ├── INDEX.md      # ÍNDICE DE MÓDULOS (consultar antes de crear)
│   ├── MANUAL.md     # Guía de operaciones
│   ├── KITTY_INIT.md # Configuración centralizada Kitty
│   ├── COLOR_MODULE.md # Módulo de coloreado
│   └── ...
├── modules/          # Módulos independientes (usables como programas)
│   └── color/        # Módulo de coloreado de pestañas
├── src/              # Código fuente modular (máx 3 funciones/módulo)
│   ├── main.py       # Despachador CLI
│   ├── config.py     # Gestión de configuración
│   ├── kitty.py      # Control remoto Kitty
│   ├── engine.py     # Motores de IA
│   ├── plan.py       # Orquestador táctico
│   └── init.py       # Gestión de inicialización
├── tests/            # Pruebas automatizadas
└── venv/             # Entorno virtual Python (Visible/UV)
```

---

## 🧩 ARQUITECTURA DE CONTROL PARA IA (PRÓXIMA ETAPA)

### Objetivo: Control Determinista de Ventanas/Pestañas/Colores

La IA debe poder **orquestar Kitty de manera precisa y reproducible**:

#### 1. Lanzamiento de Ventana con Configuración Específica

```python
# La IA puede lanzar Kitty con:
- Configuración de colores (texto neón + fondo contraste)
- Tamaño de fuente (16pt estándar TRON)
- Atajos de teclado personalizados
- Socket de control remoto habilitado
```

#### 2. Creación de Pestañas con Colores y Comandos

```python
# Por pestaña, la IA define:
{
    "tab_title": "BACKEND",
    "colors": {
        "text_neon": "#00FFFF",      # Cyan brillante
        "bg_contrast": "#001A1A"     # Cyan muy oscuro (alto contraste)
    },
    "commands": [
        "cd ~/project/api",
        "uv run python server.py"
    ]
}
```

**Regla de colores Hacker Neon:**
- **Texto**: Color neón brillante (RGB con al menos un canal en 0xFF)
- **Fondo**: Mismo matiz, 5-10% de intensidad (alto contraste)

#### 3. Control de Múltiples Pestañas/Ventanas

```python
# La IA mantiene estado y controla:
{
    "window_id": "main",
    "tabs": [
        {"id": 1, "title": "BACKEND", "color": "#00FFFF", "active": True},
        {"id": 2, "title": "FRONTEND", "color": "#FF00FF", "active": False},
        {"id": 3, "title": "LOGS", "color": "#39FF14", "active": False}
    ],
    "layout": "tall"  # tall, stack, fat, horizontal
}
```

#### 4. Envío de Comandos a Pestañas Específicas

```python
# La IA envía comandos determinísticamente:
kitty_remote.send_to_tab(tab_id=1, command="npm install")
kitty_remote.send_to_tab(tab_id=2, command="npm run dev")
```

#### 5. Layouts Predefinidos para Flujos de Trabajo

| Layout | Descripción | Uso |
|--------|-------------|-----|
| `tr plan` | 4 pestañas: BACKEND, FRONTEND, DB, LOGS | Desarrollo full-stack |
| `tr debug` | 3 pestañas: CODE, TEST, OUTPUT | Depuración |
| `tr monitor` | 2 pestañas: LOGS, METRICS | Monitoreo |

---

## 📋 PRÓXIMOS PASOS (ROADMAP)

### Fase 1: Prueba tr plan con Colores ✅

- [x] Configuración Kitty Hacker Neon centralizada
- [x] Enlace simbólico global creado
- [x] Módulo de color funcional (`tr-color`, `tr color`)
- [ ] **PENDIENTE**: `tr plan` ejecuta pestañas con colores automáticos

### Fase 2: Módulos de Control de Ventanas y Pestañas

- [ ] `src/window.py` (3 funciones):
  1. `create_window(config)` → Crea ventana con configuración
  2. `get_window_state()` → Obtiene estado JSON
  3. `close_window(id)` → Cierra ventana

- [ ] `src/tabs.py` (3 funciones):
  1. `create_tab(title, colors, commands)` → Crea pestaña coloreada
  2. `send_command(tab_id, command)` → Ejecuta comando en pestaña
  3. `get_tab_info(tab_id)` → Obtiene info de pestaña

- [ ] `src/layout.py` (3 funciones):
  1. `apply_layout(window_id, layout_name)` → Aplica layout
  2. `list_layouts()` → Lista layouts disponibles
  3. `create_layout(name, config)` → Crea layout personalizado

### Fase 3: Integración con IA (Orquestador Determinista)

- [ ] IA puede leer `docs/INDEX.md` antes de crear módulos
- [ ] IA usa módulos como herramientas composicionales
- [ ] IA lanza `tr plan` con pestañas en colores Hacker Neon
- [ ] IA controla ventanas/pestañas de manera determinista

### Fase 4: Herramientas Avanzadas

- [ ] `bin/tr-layout` → CLI para gestión de layouts
- [ ] `bin/tr-session` → CLI para guardar/cargar sesiones
- [ ] `modules/session/` → Módulo de persistencia de sesiones
- [ ] `modules/layout/` → Módulo de layouts personalizados

---

## 📄 DOCUMENTACIÓN TÉCNICA (docs/)

**ÍNDICE OBLIGATORIO:** Antes de crear módulos, consultar `docs/INDEX.md`

| Documento | Propósito |
|-----------|-----------|
| `INDEX.md` | **ÍNDICE DE MÓDULOS** - Consultar antes de crear nuevos |
| `MANUAL.md` | Guía de operaciones y comandos |
| `KITTY_INIT.md` | Configuración centralizada de Kitty |
| `COLOR_MODULE.md` | Documentación del módulo de coloreado |
| `Shortcuts.md` | Tabla de atajos de teclado |
| `Requerimientos.md` | Bitácora de 150+ tareas de desarrollo |
| `ZSH/Trucos.md` | Optimización del shell y plugins |
| `modulo-colores-y-diseno.md` | Diseño de colores Hacker Neon |
| `Ollama-API.md` | Integración con Ollama |
| `Apideepseek.md` | Integración con DeepSeek |

---

## ⌨️ ATAJOS CLAVE (WOW FACTOR)

| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+T` | Nueva Pestaña |
| `Ctrl+Shift+W` | Cerrar Pestaña |
| `Ctrl+Shift+PgUp/PgDn` | Navegar pestañas |
| `Ctrl+Shift+C/V` | Copiar y Pegar |
| `Ctrl+Alt+R` | Recargar configuración Kitty |
| **Mouse** | Soporte completo habilitado |

---

## 🎯 PRINCIPIOS DE DISEÑO

1. **Modularidad**: Máximo 3 funciones por módulo
2. **Independencia**: Cada módulo es un programa usable por CLI e IA
3. **Documentación**: INDEX.md actualizado antes de crear módulos
4. **Determinismo**: IA controla Kitty de manera reproducible
5. **Estética**: Colores neón de alto contraste (Hacker Neon)
6. **Centralización**: Configuración única en `TR/config/`

---

*Tron: Smart Always. Boba Nunca.*

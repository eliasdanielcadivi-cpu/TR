# TR - ÍNDICE DE MÓDULOS Y COMPONENTES

**⚠️ REGLA DE ORO:** Consultar este índice ANTES de crear cualquier módulo nuevo.  
**📋 MÁXIMO 3 FUNCIONES** por módulo (filosofía TRON de modularidad).

**Última actualización:** 2026-02-27  
**Versión:** 1.0.0

---

## 🛠 NÚCLEO (src/)

### main.py - Orquestador CLI
**Propósito:** Punto de entrada único, despacho de comandos, help system.  
**Funciones públicas:**
1. `cli()` - Grupo de comandos Click, invoke sin subcomando → help
2. `dispatch()` - Despacha a módulos según comando (status, init, color, plan, etc.)
3. `show_help()` - Muestra ayuda navegable con Broot en `docs/`

**CLI:** `tr`, `tr <comando>`, `tr help`  
**Relaciones:** Importa todos los módulos del núcleo, no tiene lógica de negocio.  
**Documentación:** `LEEME.md`

---

### config.py - Gestión de Configuración
**Propósito:** Carga, guardado y gestión de rutas de configuración YAML.  
**Funciones públicas:**
1. `load_config(path)` - Carga configuración desde YAML
2. `save_config(path, config)` - Guarda configuración a YAML
3. `get_tr_context()` - Retorna contexto con rutas base, socket, handshake

**CLI:** Ninguno (módulo de soporte)  
**Relaciones:** Usado por todos los módulos que necesitan configuración.  
**Documentación:** Interna (código auto-documentado)

---

### kitty.py - Control Remoto de Kitty
**Propósito:** Socket remote control, diagnóstico y ejecución de comandos.  
**Funciones públicas (KittyRemote class):**
1. `is_running()` - Verifica si Kitty está corriendo con socket
2. `launch_hub()` - Lanza Kitty con configuración TRON
3. `run(cmd_args)` - Ejecuta comando remoto (kitten @)

**CLI:** Ninguno (módulo de soporte)  
**Relaciones:** Usado por `plan.py`, `init.py`, módulos de control.  
**Documentación:** `docs/Controlar a Kitty desde scripts.md`

---

### engine.py - Motores de IA
**Propósito:** Conectores Ollama y DeepSeek, plantillas de prompt.  
**Funciones públicas (AIEngine class):**
1. `query_ollama(prompt, model)` - Query a Ollama local
2. `query_deepseek(prompt, model, api_key)` - Query a DeepSeek API
3. `apply_template(template_name, context)` - Aplica plantilla de prompt

**CLI:** `tr p "pregunta"`  
**Relaciones:** Usado por `main.py` para comando `p`, futuros agentes IA.  
**Documentación:** `docs/Ollama-API.md`, `docs/Apideepseek.md`

---

### plan.py - Orquestador Táctico de Pestañas
**Propósito:** Despliegue de flujos de trabajo con pestañas coloreadas Hacker Neon.  
**Funciones públicas:**
1. `launch_tab(kitty_remote, title, colors, command)` - Lanza pestaña con colores
2. `deploy_plan(kitty_remote, ctx)` - Ejecuta plan maestro (4 pestañas)
3. `verify_handshake(handshake_file)` - Verifica que todo esté online

**CLI:** `tr plan`  
**Relaciones:** Usa `kitty.py`, colores de `docs/COLOR_SYSTEM.md`.  
**Documentación:** `docs/COLOR_SYSTEM.md` (sección "Implementación Técnica")

**Colores de las 4 pestañas espectaculares:**
| Pestaña | active_fg | inactive_fg | active_bg | inactive_bg |
|---------|-----------|-------------|-----------|-------------|
| CYBERPUNK | #00FFFF | #00AAAA | #001A1A | #000D0D |
| NEON GODDESS | #FF00FF | #AA00AA | #1A001A | #0D000D |
| MATRIX | #39FF14 | #22AA00 | #0A1A0A | #050D05 |
| BLADE RUNNER | #FF6600 | #AA4400 | #1A0D00 | #0D0600 |

---

### init.py - Gestión de Inicialización
**Propósito:** Configuración centralizada de Kitty, enlace simbólico, recarga.  
**Funciones públicas:**
1. `create_symlink(tr_config, user_config)` - Crea enlace simbólico
2. `reload_config(socket_path, config_path)` - Recarga configuración en Kitty
3. `get_status(tr_config, user_config, socket_path)` - Retorna estado
4. `unlink_config(user_config)` - Elimina enlace simbólico

**CLI:** `tr init --status`, `tr init --link`, `tr init --reload`, `tr init --unlink`  
**Relaciones:** Usa `kitty.py` para verificar socket, `config.py` para rutas.  
**Documentación:** `docs/KITTY_INIT.md`

---

## 🧩 MÓDULOS INDEPENDIENTES (modules/)

### color/ - Coloreado de Pestañas Hacker Neon
**Propósito:** Match ruta→color, apply set-tab-color, list reglas.  
**Funciones principales (ColorEngine class):**
1. `match(path)` - Encuentra regla de color para ruta (fnmatch)
2. `apply(path, socket_path)` - Aplica color y título vía set-tab-color
3. `list_rules()` - Lista todas las reglas configuradas

**CLI:** `bin/tr-color`, `tr color <ruta>`  
**Archivos:**
- `modules/color/color_engine.py` - Motor principal
- `modules/color/config.yaml` - Reglas de coloreado
- `modules/color/__init__.py` - Exporta ColorEngine, ColorRule
- `docs/COLOR_MODULE.md` - Documentación técnica
- `docs/COLOR_SYSTEM.md` - Sistema de colores completo

**Relaciones:** Usado por `plan.py` para colorear pestañas, IA puede usar directamente.

**Reglas configuradas (ejemplos):**
| Patrón | Color | Título | Prioridad |
|--------|-------|--------|-----------|
| `/home/daniel/Escritorio/QT5/elAsunto.md` | #ff6600 | EL ASUNTO | 10 |
| `/home/daniel/tron/**` | #00ffff | TRON | 5 |
| `*.py` | #ffcc00 | PYTHON | 2 |

---

## 🔧 HERRAMIENTAS CLI (bin/)

### tr-color
**Propósito:** Aplicar colores a pestañas desde CLI (headless).  
**Funciones:**
1. `apply_color(ruta)` - Aplica color según reglas YAML
2. `auto_detect()` - Detecta archivo reciente en PWD y colorea
3. `list_rules()` - Lista reglas configuradas

**Comandos:**
```bash
tr-color /ruta/al/archivo.py    # Aplica color
tr-color --auto                 # Auto-detecta archivo
tr-color --list                 # Lista reglas
tr-color --test /ruta           # Testea sin aplicar
```

**Relaciones:** Usa `modules/color/color_engine.py`.  
**Documentación:** `docs/COLOR_MODULE.md`

---

### tr-kitty-init
**Propósito:** Inicializar Kitty con configuración TRON.  
**Funciones:**
1. `launch_kitty()` - Inicia Kitty con config TRON
2. `create_symlink()` - Crea enlace en ~/.config/kitty/
3. `reload_config()` - Recarga configuración existente

**Comandos:**
```bash
tr-kitty-init                   # Inicia Kitty
tr-kitty-init --link            # Crea enlace simbólico
tr-kitty-init --reload          # Recarga config
tr-kitty-init --status          # Verifica estado
```

**Relaciones:** Independiente, no usa módulos TR.  
**Documentación:** `docs/KITTY_INIT.md`

---

### tr-video
**Propósito:** Reproducción de video HQ en Kitty (icat/mpv).  
**Funciones:**
1. `play_video(ruta)` - Reproduce video con mpv embed
2. `show_image(ruta)` - Muestra imagen con icat
3. `get_media_info(ruta)` - Obtiene info del archivo

**Comandos:**
```bash
tr-video /ruta/al/video.mp4     # Reproduce video
tr-video --image /ruta/img.png  # Muestra imagen
```

**Relaciones:** Usado por `plan.py` para multimedia.  
**Documentación:** Interna (código auto-documentado)

---

## 📄 DOCUMENTACIÓN (docs/)

| Archivo | Propósito | Relación con módulos |
|---------|-----------|---------------------|
| `INDEX.md` | **ÍNDICE DE MÓDULOS** - Consultar antes de crear nuevos | Todos |
| `LEEME.md` | Filosofía, arquitectura, próximos pasos | Todos |
| `MANUAL.md` | Guía de operaciones y comandos | Todos |
| `KITTY_INIT.md` | Configuración centralizada de Kitty | `init.py`, `tr-kitty-init` |
| `COLOR_MODULE.md` | Documentación del módulo de coloreado | `modules/color/`, `tr-color` |
| `COLOR_SYSTEM.md` | Sistema completo de colores Hacker Neon | `plan.py`, `modules/color/` |
| `modulo-colores-y-diseno.md` | Diseño de colores, comandos testeado | `plan.py`, `modules/color/` |
| `Shortcuts.md` | Tabla de atajos de teclado | `kitty.py`, `config/kitty.conf` |
| `Requerimientos.md` | Bitácora de 150+ tareas | Todos |
| `ZSH/Trucos.md` | Optimización del shell | Futuros módulos ZSH |
| `Ollama-API.md` | Integración con Ollama | `engine.py` |
| `Apideepseek.md` | Integración con DeepSeek | `engine.py` |
| `Controlar a Kitty desde scripts.md` | Manual de remote control | `kitty.py`, `plan.py` |

---

## 📋 PRÓXIMOS MÓDULOS (PENDIENTES)

### window.py - Control de Ventanas
**Propósito:** Crear, obtener estado, cerrar ventanas Kitty.  
**Funciones (máx 3):**
1. `create_window(config)` - Crea ventana con configuración
2. `get_window_state(window_id)` - Obtiene estado JSON
3. `close_window(window_id)` - Cierra ventana

**CLI:** `bin/tr-window` (pendiente)  
**Relaciones:** Usa `kitty.py`, usado por `plan.py`, IA.  
**Documentación:** (pendiente)

---

### tabs.py - Control de Pestañas
**Propósito:** Crear pestañas coloreadas, enviar comandos, obtener info.  
**Funciones (máx 3):**
1. `create_tab(title, colors, commands)` - Crea pestaña con color Hacker Neon
2. `send_command(tab_id, command)` - Ejecuta comando en pestaña
3. `get_tab_info(tab_id)` - Obtiene info de pestaña (título, color, activo)

**CLI:** `bin/tr-tabs` (pendiente)  
**Relaciones:** Usa `kitty.py`, `modules/color/`, usado por IA.  
**Documentación:** (pendiente)

---

### layout.py - Gestión de Layouts
**Propósito:** Aplicar, listar, crear layouts de ventanas.  
**Funciones (máx 3):**
1. `apply_layout(window_id, layout_name)` - Aplica layout (tall, stack, fat)
2. `list_layouts()` - Lista layouts disponibles
3. `create_layout(name, config)` - Crea layout personalizado

**CLI:** `bin/tr-layout` (pendiente)  
**Relaciones:** Usa `kitty.py`, `window.py`.  
**Documentación:** (pendiente)

---

### session.py - Persistencia de Sesiones
**Propósito:** Guardar, cargar, listar sesiones de trabajo.  
**Funciones (máx 3):**
1. `save_session(name, state)` - Guarda sesión en `data/sessions/`
2. `load_session(name)` - Carga sesión y restaura estado
3. `list_sessions()` - Lista sesiones guardadas

**CLI:** `bin/tr-session` (pendiente)  
**Relaciones:** Usa `config.py`, `window.py`, `tabs.py`.  
**Documentación:** (pendiente)

---

## 🎯 REGLAS DE MODULARIDAD

1. **Máximo 3 funciones públicas** por módulo
2. **Cada módulo es un programa** - usable desde CLI e IA
3. **Sin dependencias circulares** - grafo dirigido acíclico
4. **INDEX.md actualizado** - antes de crear módulo nuevo
5. **Documentación en docs/** - cada módulo tiene su archivo .md
6. **CLI en bin/** - cada módulo independiente tiene su herramienta

---

## 📊 DIAGRAMA DE RELACIONES

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                    (Orquestador CLI)                        │
└─────────────┬───────────────────────┬───────────────────────┘
              │                       │
              ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐
    │   init.py       │     │   plan.py       │
    │  (Gestión       │     │ (Orquestador    │
    │   Kitty)        │     │  Pestañas)      │
    └────────┬────────┘     └────────┬────────┘
             │                       │
             ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐
    │   kitty.py      │◄────│  modules/color/ │
    │ (Remote Ctrl)   │     │  (ColorEngine)  │
    └─────────────────┘     └─────────────────┘
             │                       │
             ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐
    │  engine.py      │     │  bin/tr-color   │
    │   (IA)          │     │  (CLI Color)    │
    └─────────────────┘     └─────────────────┘
```

---

**Nota:** Este índice debe actualizarse CADA VEZ que se crea o modifica un módulo.

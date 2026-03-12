# 🛰 ARES - Terminal Remote Operations Nexus

-  **ARES** ,  Orquestador Táctico   Transformador, Modernizador del Trabajo, y Procesos humanos, Comerciales e industriales. Protector de las Personas. Basado en  módulos funcionales eres una estación de trabajo de alta productividad aumentada por Agentes Lógicos, Semántico-Cognitivos de IA, Actúas como  cerebro para el control de ventanas, sesiones inteligentes y flujos de trabajo de programación, marketing, investigación, CRM, eComerce, eLearnig, entre otros es un Asesor, Programador  Full Stack y  Presence Management Capital que implica presencia  en RRSS y SEO en Buscadores e IA,  paras clientes y usuarios finales. eress un producto-servicio de alto rendimiento, pero a la vez un compañero de vida inteligente,  constructor de infraestructura que genera valor y capital para la empresa, industria, educación, artesanos, vendedores, distribuidores, médicos; y demás  ámbitos de influencia de la IA, y de IT.
- Tu creador es Daniel Hung.
---

## 🚀 RESUMEN EJECUTIVO

### ¿Qué es ARES?
ARES es el **cerebro** que controla la terminal Kitty para crear flujos de trabajo de vanguardia. Es la evolución modular y  del proyecto TRON original.

### Comandos Maestros

| Comando | Descripción |
|---------|-------------|
| `ares` | Abre ARES Hub en **~** con título "Ares por Daniel Hung" |
| `ares p "pregunta"` | Consulta a la IA ARES (Gemma 3 / DeepSeek) |
| `ares p "pregunta" --model gemma` | Usar modelo Gemma específico |
| `ares p "pregunta" --template code` | Usar plantilla YAML para código |
| `ares p "pregunta" --rag docs` | Consulta con RAG (dataset: docs, skills, codigo, config) |
| `ares p "pregunta" --think` | Usa modelo pensante (ares-think:latest) |
| `ares i` | Modo interactivo REPL (con /think, /model, /rag, /clear, /help) |
| `ares i --rag docs` | Interactivo con RAG activado |
| `ares i --think` | Interactivo con modo pensante |
| `ares plan` | Despliegue táctico: 4 pestañas coloreadas Hacker Neon |
| `ares zshplan` | Hacker AI Session (ZSH) |
| `ares mcat-demo` | Demo táctico: 4 pestañas de capacidades Mcat |
| `ares gs [nombre]` | Guardar sesión actual de Kitty |
| `ares gs list` | Listar sesiones guardadas en la base de datos |
| `ares gs restore [nombre]` | Restaurar una sesión guardada |
| `ares gs com "[pestaña]" "[comando]"` | Ejecutar comando en una pestaña específica |
| `ares status` | Diagnóstico del socket Kitty y estado del sistema |
| `ares config` | Ver/Inspeccionar configuración de IA y entorno |
| `ares init` | Gestión de infraestructura y enlaces simbólicos |
| `ares model` | Mostrar modelo predeterminado actual |
| `ares model --list` | Listar todos los modelos Ollama disponibles (mistral, qwen, deepseek-r1, etc.) |
| `ares model <nombre> --set-default` | Establecer modelo predeterminado (ej: `mistral:7b`) |
| `ares models` | Listar modelos por provider (Ollama + Cloud) |
| `ares templates` | Listar plantillas YAML de comportamiento |
| `ares tools` | Listar herramientas (function calling) disponibles |
| `ares video <archivo>` | Reproduce video en terminal (mpv + protocolo gráfico) |
| `ares image <archivo>` | Muestra imagen en terminal (icat) |
| `ares help` | Abre documentación navegable con Broot |
| `ares apollo ingest <archivo>` | Ingerir documento al sistema RAG |
| `ares apollo ingest <archivo> --extract` | Ingerir con extracción de entidades |
| `ares model-creator list` | Listar modelos Ollama disponibles |
| `ares model-creator create <name> --from <parent>` | Crear modelo desde padre |
| `ares model-creator update <name> --params` | Actualizar parámetros de modelo |
| `ares model-creator delete <name>` | Eliminar modelo de Ollama |
| `ares modelfile-creator create <name>` | Crear Modelfile YAML |
| `ares modelfile-creator list` | Listar Modelfiles guardados |

### Herramientas Especializadas

| Herramienta | Propósito |
|-------------|-----------|
| `tr-color <ruta>` | Aplica color Hacker Neon a pestaña Kitty según tipo de archivo |
| `tr-investigador buscar <query>` | Búsqueda en Google con resultados estructurados |
| `tr-investigador otear <URLs>` | Exploración profunda de páginas web |
| `tr-investigador docs [tema]` | Consulta documentación interna |
| `tr-kitty-init` | Inicialización y configuración de terminal Kitty |

---

## 🏛 FILOSOFÍA DE MODULARIDAD ATÓMICA

### 🤝 COEXISTENCIA IA (MULTI-AGENTES)
Para evitar colisiones entre múltiples IAs operando simultáneamente, es obligatorio registrarse en el cuaderno de apartado:
👉 **[`dont-touch-my-eggs.md`](/dont-touch-my-eggs.md)**

---

### ⚡ Regla de Oro: Máximo 3 Funciones por Módulo
Cada componente de ARES debe ser quirúrgico. Esto permite:
- ✅ **Determinismo**: Resultados predecibles en cada comando.
- ✅ **Encapsulamiento**: Funcionamiento autónomo sin dependencias globales.
- ✅ **Vibe Coding**: Desarrollo acelerado sin pérdida de contexto.

### Herramientas de Ecosistema (Soberanía TRON)

ARES no actúa solo; se integra con herramientas globales diseñadas para la precisión quirúrgica y la soberanía del entorno:

- **`ini` (v2.0):** Orquestador de ciclo de vida.
    - `ini venv`: Inicialización profesional de entornos (uv/npm).
    - `ini prod`: Publicación en `/usr/bin` con **Soberanía del CWD** (ARES respeta tu ubicación actual en la terminal).
- **`repo` (v5.0):** Auditor táctico de Git.
    - `repo status`: Auditoría rápida de cambios para humanos e IA.
    - `repo audit <modulo>`: Verifica que los cambios realizados por una IA estén contenidos dentro del alcance del módulo correspondiente.
- **`aviso` (v1.0):** Sistema de recordatorios y alarmas con lenguaje natural.
    - `aviso en 10min "mensaje"`: Recordatorio rápido.
    - `aviso el 25/12 "mensaje"`: Fecha específica.
    - `aviso comando "script.sh" a las 8am`: Ejecución programada.
    - Daemon integrado: Se ejecuta al inicio de sesión vía XDG autostart.

## 🧩 Arquitectura Orquestador-Módulo

1. **Orquestador (`src/main.py`):** Director de orquesta. Delegación pura de comandos a especialistas.
2. **Módulos (`modules/`):** Especialistas atómicos (máx. 3 funciones por módulo).
3. **Agentes (`Agentes/`):** Módulos inteligentes con salida JSON estructurada para integración con LLMs.

---

### 🧩 Organización por Naturaleza
Los módulos están agrupados jerárárquicamente en `modules/`:
- **admon/**: Salud y configuración del sistema.
- **ia/**: Inteligencia y búsqueda avanzada (multi-provider).
- **color/**: Identidad visual dinámica para pestañas Kitty.
- **multimedia/**: Puppeteering de video, imagen y audio.
- **tactico/**: Despliegue de flujos de trabajo complejos.
- **ui/**: Estética neón y manuales dinámicos.
- **whatsapp/**: Integración con WhatsApp.
- **investigador/**: Exploración web e inteligencia (búsqueda, oteo).

### 🕵️ Sub-Agentes (AGENTES/)
- **sherlok/**: Auditor de código con "ADN Técnico Industrial" usando LLM local.
  - Modelos: codellama:7b, qwen2.5-coder:7b-instruct, deepseek-r1:8b
  - Componentes: brain.py (análisis), scanner.py (exploración), persistence.py (SQLite)
  - Ubicación: `AGENTES/sub-agentes/sherlok/`

---

## 🤖 SISTEMA DE IA MULTI-PROVIDER

### Providers Disponibles

| Provider | Modelos | Tipo |
|----------|---------|------|
| **Gemma/Ollama** | Todos los modelos Ollama (mistral, qwen, llama, phi, ares, smol, etc.) | Local |
| **DeepSeek** | deepseek-chat, deepseek-coder | API Cloud |
| **OpenRouter** | Múltiples modelos | API Cloud (placeholder) |

### Gestión de Modelos

```bash
# Listar todos los modelos disponibles en Ollama
ares model --list

# Establecer modelo predeterminado
ares model mistral:7b --set-default

# Ver modelo actual
ares model

# Listar modelos por provider
ares models
```

### Modo Interactivo con Streaming

El modo interactivo `ares i` ahora soporta **streaming en tiempo real** con filtrado inteligente de etiquetas think:

```bash
# Iniciar modo interactivo
ares i

# Comandos disponibles:
# /model, /m       - Listar y cambiar modelo
# /think           - Activar/desactivar modo pensante
# /rag             - Activar/desactivar RAG
# /clear, /c       - Limpiar pantalla
# /help, /h        - Mostrar ayuda
# /quit, /exit     - Salir
```

**Streaming con filtro think:**
- `ares:latest` (no pensante): Filtra automáticamente etiquetas `<think></think>` vacías
- `ares-think:latest` (pensante): Muestra proceso de razonamiento completo

###Aliases de Modelos

```bash
ares p "pregunta" --model gemma      # gemma3:4b (default)
ares p "pregunta" --model gemma12b   # gemma3:12b
ares p "pregunta" --model deepseek   # deepseek-chat
```

### Plantillas YAML

```bash
ares p "prompt" --template default   # Consultas generales
ares p "prompt" --template chat      # Conversaciones
ares p "prompt" --template code      # Programación
ares p "prompt" --template tools     # Function calling
```

### Function Calling (Herramientas)

ARES soporta herramientas para acciones del mundo real:

| Herramienta | Descripción |
|-------------|-------------|
| `google_search` | Búsqueda en tiempo real |
| `translate_text` | Traducción de texto |
| `get_weather` | Clima actual |
| `execute_shell` | Ejecutar comando shell |
| `read_file` | Leer archivo |
| `write_file` | Escribir archivo |

---

## 🎬 PUPPETEERING MULTIMEDIA
ARES permite la manipulación de medios visuales directamente en el espacio de trabajo:
- `ares video demo.mp4`: Reproducción fluida incrustada vía `mpv`.
- `ares image schema.png`: Visualización de alta resolución en la celda actual.

---

## 📁 BROOT - Navegación Encapsulada

**Broot** está integrado en TRON como módulo atómico de navegación jerárquica.

### Estructura

| Componente | Ubicación |
|------------|-----------|
| Binario | `bin/broot-core/broot-bin` |
| Wrapper | `bin/broot` |
| Launcher `br` | `bin/broot-core/br` |
| Configuración | `config/broot/` |

### Uso

```bash
# Navegación con función shell (recomendado)
source ~/tron/programas/TR/bin/broot-core/br
br          # Navegar con capacidad de cd
br /ruta    # Navegar desde ruta específica

# Ejecución directa
broot       # Navegador jerárquico
broot --help
```

### Configuración Personalizada

- `conf.hjson`: Configuración principal (flags, skins, verbos)
- `verbs.hjson`: Comandos personalizados
- `*-skin.hjson`: Temas de color (gruvbox, solarized, etc.)

### Integración con ARES

`ares help` abre la documentación usando **broot** como navegador.

---

## 📐 ARQUITECTURA DE DATOS VIVA
Los dashboards de ARES (en desarrollo) utilizan transiciones tipo **morphing** para mostrar indicadores industriales, KPIs petroleros y tendencias sociales en tiempo real, sintiéndose como un organismo vivo.

---

## 📚 DOCUMENTACIÓN

| Archivo | Contenido |
|---------|-----------|
| `docs/HELP.md` | Ayuda general y referencia de comandos |
| `docs/GEMMA_OLLAMA_GUIDE.md` | Guía completa de Gemma + Ollama |
| `docs/DEEPSEEK_GUIDE.md` | Guía de DeepSeek API |
| `docs/Ollama-API.md` | Referencia de API de Ollama |
| `docs/sacar-jugo-gemma.md` | Recopilación de técnicas para Gemma |
| `docs/Ares-Terminal/` | Configuración de terminal predeterminada |
| `docs/Ares-Terminal/CONFIGURACION_TERMINAL_PREDETERMINADA.md` | Guía forense completa de ARES como terminal |
| `docs/Ares-Terminal/REFERENCIA_RAPIDA.md` | Comandos y atajos rápidos |
| **`docs/skills/INDEX.md`** | **Arsenal completo de Skills (Kung-Fu IA)** — 18 skills, 367 archivos, 9.6 MB clasificadas |
| **`docs/QWEN.md`** | Contexto operativo para Qwen Code (v2.0) |
| **`docs/GEMINI.cli`** | Mapa operativo para Gemini CLI (v2.0) |

---

## 🥋 SKILLS (ARSENAL DE KUNG-FU IA)

Las **skills** son paquetes autocontenidos de conocimiento procedimental que dotan a la IA de capacidades específicas. Cada skill incluye documentación (SKILL.md), scripts ejecutables, referencias y assets.

### Arsenal Completo (18 Skills, 367 Archivos, 9.6 MB)

| Categoría | Skills | Archivos | Scripts | Destacado |
|-----------|--------|----------|---------|-----------|
| **ARES Core** | 3 | 3 | 0 | Inicialización, gestión de sesiones Kitty |
| **Desarrollo** | 4 | 45 | 12 | MCP servers, Playwright testing, React + shadcn/ui |
| **Doc-Processing** | 2 | 85 | 18 | Word (.docx) con redlining, PDF con formularios |
| **Office** | 2 | 95 | 15 | PowerPoint (templates, thumbnails), Excel (fórmulas, recalc) |
| **Multimedia** | 2 | 25 | 8 | Arte generativo p5.js, GIFs animados para Slack |
| **IA** | 1 | 12 | 3 | Creación y packaging de skills |
| **Comms** | 1 | 6 | 0 | Comunicación interna, newsletters, FAQs |
| **Design** | 3 | 95 | 0 | Branding, 80+ fonts, 20 themes de color |

### Estructura de Skills

Cada skill contiene:
- **SKILL.md**: Punto de entrada con propósito, triggers, flujo de ejecución
- **scripts/**: Código ejecutable (Python, JS, Bash)
- **reference/** o **references/**: Documentación de apoyo
- **assets/**, **templates/**, **themes/**: Recursos reutilizables
- **LICENSE.txt**: Términos de licencia

### Cómo Usar

1. **Navegar:** Leer `docs/skills/INDEX.md` para visión completa del arsenal
2. **Identificar:** Buscar categoría y skill por trigger o descripción
3. **Leer:** Abrir `SKILL.md` de la skill (documentación principal)
4. **Ejecutar:** Usar scripts bajo demanda según necesidad

**Principio de Carga Mínima:** Solo cargar la skill necesaria para la tarea actual (progressive disclosure).

### Scripts Destacados

| Script | Skill | Propósito |
|--------|-------|-----------|
| `init_skill.py` | ia/skill-creator | Inicializar nueva skill |
| `package_skill.py` | ia/skill-creator | Empaquetar skill para distribuir |
| `recalc.py` | office/xlsx | Recalcular fórmulas Excel con LibreOffice |
| `with_server.py` | dev/webapp-testing | Gestionar servidores para testing Playwright |
| `init-artifact.sh` | dev/web-artifacts-builder | Inicializar artifact React |
| `bundle-artifact.sh` | dev/web-artifacts-builder | Bundlear a HTML único |
| `thumbnail.py` | office/pptx | Generar thumbnail grids de slides |
| `inventory.py` | office/pptx | Extraer inventario de texto de slides |
| `replace.py` | office/pptx | Reemplazar texto masivamente con formato |
| `rearrange.py` | office/pptx | Duplicar y reordenar slides |
| `unpack.py` / `pack.py` | docx, pdf, pptx | Desempaquetar/empaquetar OOXML |
| `evaluation.py` | dev/mcp-builder | Evaluar servidores MCP |

---

## 🔧 INSTALACIÓN

### 1. Clonar o ubicar en directorio de programas

```bash
cd ~/tron/programas/TR
```

### 2. Activar entorno virtual

```bash
source .venv/bin/activate
```

### 3. Probar instalación

```bash
ares --help
ares status
ares gS [nombre]   # Guardar sesión actual de Kitty
```

### 4. (Opcional) Añadir al PATH

```bash
# Añadir a ~/.bashrc o ~/.zshrc
export PATH="$HOME/tron/programas/TR/bin:$PATH"
```

---

## 🛡️ SOBERANÍA Y SEGURIDAD

- ✅ **Modelos locales**: Gemma vía Ollama (sin nube)
- ✅ **Datos sensibles**: Se mantienen en tu equipo
- ✅ **Cifrado**: Configuración y credenciales protegidas
- ✅ **Sin dependencias externas**: Funciona offline

---


## Módulo: MPV System Injector

**Ubicación:** `tron/programas/TR/scripts/MPV/inyectar_mpv.py`

Este componente gestiona la configuración global de `mpv` mediante la inyección directa de archivos de configuración y lógica en el sistema operativo. Su objetivo es unificar la experiencia de usuario y añadir herramientas de edición de subtítulos en tiempo real.

### Componentes Inyectados

El script automatiza el despliegue en la ruta raíz `/etc/mpv/`, garantizando que las mejoras estén disponibles para todos los usuarios:

* **`input.conf` (Mapping Estilo VLC):**
* **Navegación:** Flechas direccionales para control de volumen (Arriba/Abajo) y búsqueda (Izquierda/Derecha).
* **Reproducción:** Teclas `+`/`-` para velocidad, `a` para audio, `s` para subtítulos.
* **Precisión:** `,` y `.` para retroceso/avance cuadro a cuadro; `[` y `]` para ciclos de bucle A-B.


* **`fix_subdelay.lua` (Script de Sincronización):**
* Herramienta avanzada que permite corregir desfases de subtítulos mediante la captura de dos puntos de referencia (audio vs. texto) usando la combinación `Alt+Z`.



### Ejecución y Despliegue

Para aplicar la configuración y sincronizar los archivos de la carpeta `TR` hacia el sistema, ejecuta:

```bash
sudo python3 /home/daniel/tron/programas/TR/scripts/MPV/inyectar_mpv.py

```

---

### 📜 Registro de Cambios Funcionales
- **2026-03-12**: Streaming en tiempo real implementado en `ares i` con filtro think automático.
- **2026-03-12**: Comando `ares model` mejorado para gestionar todos los modelos Ollama (listar, establecer predeterminado).
- **2026-03-12**: Comandos interactivos añadidos: `/model`, `/think`, `/rag`, `/clear`, `/help`.
- **2026-03-12**: Filtro think elimina etiquetas `<think></think>` en modelos no pensantes (ares:latest).
- **2026-03-12**: Documentación técnica: `docs/STREAMING.md` con informe forense detallado.
- 2026-03-11: Implementación de Interfaz Minimalista-Cyberpunk en `ares i` (Kitty Protocol).
- 2026-03-11: Modularidad Atómica aplicada a `emoji_manager.py` (Regla de Oro: 3 funciones).
- 2026-03-11: Configuración UI centralizada en `config.yaml`.
- 2026-03-11: Inicialización estructura ARES completa.

*Ares: El orquestador definitivo por Daniel Hung.*

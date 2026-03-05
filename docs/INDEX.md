# 🛰️ ARES - ÍNDICE DE MÓDULOS Y COMPONENTES (v2.0)

**⚠️ REGLA DE ORO:** Consultar este índice ANTES de crear cualquier módulo nuevo.  
**📋 MÁXIMO 3 FUNCIONES** por módulo (filosofía ARES de modularidad atómica).

---

## 🏛️ NÚCLEO (root / config)

### main.py - Despachador Puro
**Propósito:** Punto de entrada único. No contiene lógica de negocio, solo orquestación de comandos.
**Relaciones:** Importa dinámicamente de `modules/`.

### config/ - Gestión de Entorno
- `config.yaml`: Única fuente de verdad para identidad (Ares), rutas y sockets.
- `kitty_remote.py`: Motor de bajo nivel para control de la terminal. (Funciones: `is_running`, `launch_hub`, `run`).

---

## 🧩 JERARQUÍA DE MÓDULOS (modules/)

### admon/ - Gestión de Sistema
**Propósito:** Mantenimiento y diagnóstico de la salud de ARES.
- `diag_manager.py`: Diagnóstico visual de sockets y pestañas.
- `init_manager.py`: Gestión de enlaces simbólicos y recarga de configuración.

### ia/ - Cerebro Agéntico
**Propósito:** Conectividad con modelos de lenguaje y lógica de prompts.
- `ai_engine.py`: Conector multi-provider para Ollama, DeepSeek y OpenRouter.
- `investigador/`: Módulo especializado en exploración web e inteligencia.
  - **CLI**: `tr-investigador buscar|otear|docs` | **Tipo**: Herramienta CLI (Tipo 2)
  - **Funciones**: `investigar()` (Google), `otear()` (URLs), `consultar_docs()`

### ui/ - Interfaz y Estética
**Propósito:** Control visual y documentación interactiva.
- `help_manager.py`: Visualización de manuales neón y orquestación de IA en terminal.

### color/ - Identidad Visual Dinámica
**Propósito:** Motor de coloreado de pestañas Kitty con identidad Hacker Neon.
- `color_engine.py`: Aplicación de paletas de colores por tipo de archivo.
- **CLI**: `tr-color <ruta>` | **Tipo**: Herramienta CLI (Tipo 2)
- **Docs**: `docs/COLOR_MODULE.md`, `docs/COLOR_SYSTEM.md`

### multimedia/ - Puppeteering de Medios
**Propósito:** Integración de video, imagen y audio en la terminal.
- `media_manager.py`: Control de `mpv` (IPC) y `icat` para renderizado de alta fidelidad.

### tactico/ - Orquestación de Flujos
**Propósito:** Despliegue de entornos de trabajo predefinidos.
- `plan_manager.py`: Ejecución de `arn plan` y verificación de handshake.
- `zsh_plan_manager.py`: Ejecución de `ares zshPlan` para sesiones de IA en Zsh.

### whatsapp/ - Comunicaciones Externas
**Propósito:** Puente entre ARES y la red de mensajería para distribución de datos.

---

## 🕵️ AGENTES (AGENTES/)

### sub-agentes/sherlok/ - Auditor de Código con IA
**Propósito:** Auditoría de programas con "ADN Técnico Industrial" usando LLM local.
- **Ubicación**: `AGENTES/sub-agentes/sherlok/`
- **Modelos**: codellama:7b, qwen2.5-coder:7b-instruct, deepseek-r1:8b
- **Componentes**: `brain.py` (análisis), `scanner.py` (exploración), `persistence.py` (SQLite)
- **Tipo**: Agente con LLM (Tipo 4) - JSON output en desarrollo
- **Configuración**: `AGENTES/sub-agentes/sherlok/config.yaml`

---

## 🔧 BINARIOS GLOBALES (bin/)

| Binario | Propósito | Módulo Origen |
|---------|-----------|---------------|
| `ares` | Lanzador maestro (Abre ARES Hub) | `src/main.py` |
| `tr-color` | Coloreado de pestañas Kitty | `modules/color/` |
| `tr-image` | Visualización de imágenes | `modules/multimedia/` |
| `tr-investigador` | Búsqueda web y oteo de URLs | `modules/investigador/` |
| `tr-kitty-init` | Inicialización de terminal Kitty | `scripts/` |
| `tr-video` | Reproducción de video en terminal | `modules/multimedia/` |
| `broot` | Navegador jerárquico encapsulado | `bin/broot-core/` |
| `br` | Función shell para navegación con `cd` | `bin/broot-core/` |

---

## 📁 BROOT - Navegación Jerárquica

**Ubicación:** `bin/broot-core/`, `config/broot/`

### Componentes
| Archivo | Propósito |
|---------|-----------|
| `broot-bin` | Binario estático (12MB, sin dependencias) |
| `broot` | Wrapper con path a config TRON |
| `br` | Función shell para `cd` post-navegación |
| `conf.hjson` | Configuración principal (flags, skins) |
| `verbs.hjson` | Comandos personalizados (backup, edit, rg) |

### Integración
- `ares help` usa broot para navegación de documentación
- Configuración personalizada: Hacker Neon skin, verbos TRON

---
*Filosofía ARES: Orden Paranoico. Modularidad Atómica. Excelencia Técnica.*

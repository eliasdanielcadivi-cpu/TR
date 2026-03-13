# 🛰️ ARES - ÍNDICE DE MÓDULOS Y COMPONENTES (v2.1)

**⚠️ REGLA DE ORO:** Consultar este índice ANTES de crear cualquier módulo nuevo.
**📋 MÁXIMO 3 FUNCIONES** por módulo (filosofía ARES de modularidad atómica).

**Última actualización:** 2026-03-13
**Estado:** Verificado con estructura real de `/modules/`

---

## 🏛️ NÚCLEO (root / config)

### main.py - Despachador Puro
**Propósito:** Punto de entrada único. No contiene lógica de negocio, solo orquestación de comandos.
**Relaciones:** Importa dinámicamente de `modules/`.
**Comandos:** `ares`, `ares p`, `ares i`, `ares plan`, `ares zshplan`, `ares model`, `ares models`

### config/ - Gestión de Entorno
| Archivo | Propósito |
|---------|-----------|
| `config.yaml` | Única fuente de verdad para identidad (Ares), rutas y sockets |
| `kitty.conf` | Configuración Kitty Hacker Neon (colores, atajos, remote control) |
| `kitty-minimal.conf` | Configuración mínima para pruebas |
| `kitty_remote.py` | Motor de bajo nivel para control de terminal (funciones: `is_running`, `launch_hub`, `run`) |
| `layout_config.yaml` | Configuración de layouts de ventanas |

---

## 🧩 JERARQUÍA DE MÓDULOS (modules/)

### admon/ - Gestión de Sistema
**Propósito:** Mantenimiento y diagnóstico de la salud de ARES.

| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `boot_manager.py` | Lanzamiento de ventana ARES con título soberano | ✅ Activo |
| `diag_manager.py` | Diagnóstico visual de sockets y pestañas | ✅ Activo |
| `init_manager.py` | Gestión de enlaces simbólicos y recarga de configuración | ✅ Activo |
| `init_manager_logic.py` | Lógica de inicialización (separada de CLI) | ✅ Activo |
| `session_manager.py` | Captura y persistencia de sesiones de Kitty (JSON) | ✅ Activo |

**Funciones clave:** `capture_and_save()`, `list_sessions()`, `load_session_data()`

---

### ia/ - Cerebro Agéntico
**Propósito:** Conectividad con modelos de lenguaje y lógica de prompts.

| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `ai_engine.py` | Conector multi-provider (Ollama, DeepSeek, OpenRouter) | ✅ Activo |
| `providers/` | Providers multi-modelo | ✅ Activo |
| `templates/` | Gestión de plantillas YAML | ✅ Activo |
| `tools/` | Function calling y herramientas | ✅ Activo |
| `apollo/` | Sistema RAG + CRM (FASE 0-2 COMPLETADO) | ✅ Activo |

#### ai_engine.py - Funciones Principales
- `ask()` - Consulta bloqueante
- `ask_stream()` - Streaming en tiempo real con filtro think opcional
- `chat()` - Chat con contexto
- `_filter_think_chunk()` - Elimina etiquetas `<think></think>` en streaming
- `_resolve_provider_and_model()` - Detección automática de modelos

**Modelos soportados:** `gemma`, `ares`, `mistral`, `qwen`, `llama`, `phi`, `smol`, `deepseek`

#### providers/ - Providers Multi-Modelo
| Archivo | Propósito |
|---------|-----------|
| `base_provider.py` | Interfaz abstracta (generate, chat, list_models) |
| `gemma_provider.py` | Ollama local con streaming (`generate_stream()`) |
| `deepseek_provider.py` | API DeepSeek cloud |
| `openrouter_provider.py` | API OpenRouter (placeholder) |

#### templates/ - Gestión de Plantillas YAML
| Archivo | Funciones |
|---------|-----------|
| `manager.py` | `TemplateManager` con `apply()`, `get_config()`, `list_templates()` |

#### tools/ - Function Calling
| Archivo | Propósito |
|---------|-----------|
| `tool_registry.py` | Registro de herramientas (google_search, translate, weather, shell, file ops) |

#### apollo/ - Sistema RAG + CRM (9 módulos)
| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `apollo_db.py` | `init_db()`, `get_connection()`, `close_db()`, `db_context()` | ✅ FASE 0 |
| `embeddings.py` | `embed_text()`, `embed_documents()`, `quantize_embeddings()` | ✅ FASE 0 |
| `ingest.py` | `semantic_chunk()`, `ingest_file()`, `ingest_directory()` | ✅ FASE 1 |
| `extraction.py` | `extract_entities_relations()`, `store_entities()`, `store_relations()` | ✅ FASE 2 |
| `retrieval.py` | `retrieve()`, `_vector_search()`, `_graph_search()`, `_relational_search()` | ✅ FASE 2 |
| `compression.py` | `compress_context()`, `_select_relevant_docs()`, `_extract_key_sentences()` | ✅ FASE 2 |
| `generation.py` | `generate_answer()`, `generate_citations()`, `detect_hallucination()`, `apply_post_process()` | ✅ FASE 2 |
| `emoji_manager.py` | `show_emoji()`, `format_output_with_emoji()`, `get_emoji_path()` | ✅ FASE 2 |
| `cli_ingest.py` | CLI de ingesta (`python -m modules.ia.apollo.cli_ingest`) | ✅ FASE 1 |
| `init_apollo_db.py` | Inicialización de BDs (`python -m modules.ia.apollo.init_apollo_db`) | ✅ FASE 0 |

**Bases de datos:** `knowledge.db`, `users.db` (SQLite + sqlite-vec)
**Modelo de embeddings:** `mxbai-embed-large:335m`

---

### investigador/ - Exploración Web e Inteligencia
**Propósito:** Búsqueda web, oteo de URLs y consulta de documentación.

| Módulo | Tipo | CLI |
|--------|------|-----|
| `__init__.py` | Módulo | - |
| `investigador.py` | Herramienta CLI (Tipo 2) | `tr-investigador buscar|otear|docs` |

**Funciones:** `investigar()` (Google), `otear()` (URLs), `consultar_docs()`

---

### ui/ - Interfaz y Estética
**Propósito:** Control visual y documentación interactiva.

| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `help_manager.py` | `show_enhanced_help()`, `query_ai()`, `list_models()`, `list_templates()`, `list_tools()`, `show_config()` | ✅ Activo |
| `chat_interface.py` | `start_interactive_chat()`, `_list_models_and_switch()`, `_show_help()` | ✅ Activo |
| `layout_engine.py` | Motor de layouts de ventanas | 🆕 Nuevo |
| `mcat_render.py` | Renderizado de demo Mcat | ✅ Activo |

#### chat_interface.py - Modo Interactivo REPL
**Comandos interactivos:**
| Comando | Función |
|---------|---------|
| `/model`, `/m` | Cambiar modelo |
| `/think` | Toggle modo pensante |
| `/rag` | Toggle RAG |
| `/clear`, `/c` | Limpiar pantalla |
| `/help`, `/h` | Mostrar ayuda |
| `/quit`, `/exit` | Salir |

**Características:**
- Streaming en tiempo real con `click.secho()` + `sys.stdout.flush()`
- Filtro think para modelos no pensantes (`ares:latest`)
- Baja latencia (<500ms primer token)

---

### color/ - Identidad Visual Dinámica
**Propósito:** Motor de coloreado de pestañas Kitty con identidad Hacker Neon.

| Módulo | Tipo | CLI |
|--------|------|-----|
| `color_engine.py` | Motor de matching y aplicación | `tr-color <ruta>` |
| `config.yaml` | Reglas de coloreado (ruta → color/título) | - |

**CLI:** `tr-color <ruta>` | **Tipo:** Herramienta CLI (Tipo 2)

**Reglas configuradas:**
- Archivos específicos QT5 (Prioridad: 10)
- Directorios (Prioridad: 5)
- Extensiones (Prioridad: 2)

**Docs relacionados:** `docs/COLOR_MODULE.md`, `docs/COLOR_SYSTEM.md`

---

### multimedia/ - Puppeteering de Medios
**Propósito:** Integración de video, imagen y audio en la terminal.

| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `media_manager.py` | Control de `mpv` (IPC) y `icat` para renderizado | ✅ Activo |

**Binarios:** `tr-video`, `tr-image`

---

### tactico/ - Orquestación de Flujos
**Propósito:** Despliegue de entornos de trabajo predefinidos.

| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `plan_manager.py` | Ejecución de `ares plan` y verificación de handshake | ✅ Activo |
| `zsh_plan_manager.py` | Ejecución de `ares zshPlan` para sesiones de IA en Zsh | ✅ Activo |
| `mcat_demo.py` | Demo táctico de capacidades de Mcat (4 pestañas) | ✅ Activo |
| `orchestrator.py` | Orquestación de sesiones desde JSON (FASE 1.1) | ✅ Activo |
| `SUCCESS-orchestrator-generic-v2.py` | Versión genérica testeada | 📦 Backup |
| `SUCCESS-orchestrator-resilient-v3.py` | Versión resiliente testeada | 📦 Backup |

**Comandos:**
- `ares plan` - Despliegue táctico (4 pestañas Hacker Neon)
- `ares zshplan` - Hacker AI Session (ZSH)
- `ares mcat-demo` - Demo táctico (4 pestañas)

**Bases de datos:** `db/*.json` (sesiones)

---

### whatsapp/ - Comunicaciones Externas
**Propósito:** Puente entre ARES y la red de mensajería para distribución de datos.

**Estado:** 🚧 En desarrollo

---

### aviso/ - Sistema de Notificaciones
**Propósito:** Notificaciones internas del sistema.

**Estado:** 🚧 En desarrollo

---

## 🕵️ AGENTES (AGENTES/)

### sub-agentes/sherlok/ - Auditor de Código con IA
**Propósito:** Auditoría de programas con "ADN Técnico Industrial" usando LLM local.

| Componente | Función |
|------------|---------|
| `brain.py` | Análisis de código |
| `scanner.py` | Exploración de repositorios |
| `persistence.py` | Persistencia SQLite |
| `config.yaml` | Configuración de modelos |

**Modelos:** `codellama:7b`, `qwen2.5-coder:7b-instruct`, `deepseek-r1:8b`
**Tipo:** Agente con LLM (Tipo 4) - JSON output en desarrollo

---

## 🔧 BINARIOS GLOBALES (bin/)

| Binario | Propósito | Módulo Origen |
|---------|-----------|---------------|
| `ares` | Lanzador maestro (Abre ARES Hub) | `src/main.py` |
| `tr-color` | Coloreado de pestañas Kitty | `modules/color/` |
| `tr-image` | Visualización de imágenes | `modules/multimedia/` |
| `tr-investigador` | Búsqueda web y oteo de URLs | `modules/investigador/` |
| `tr-kitty-init` | Inicialización de terminal Kitty | `bin/tr-kitty-init` |
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
| `broot` | Wrapper con path a config TR |
| `br` | Función shell para `cd` post-navegación |
| `conf.hjson` | Configuración principal (flags, skins) |
| `verbs.hjson` | Comandos personalizados (backup, edit, rg) |

### Integración
- `ares help` usa broot para navegación de documentación
- Configuración personalizada: Hacker Neon skin, verbos TRON

---

## 📊 ESTADO DE MÓDULOS

| Módulo | Estado | Tests | Docs |
|--------|--------|-------|------|
| `admon/` | ✅ Activo | ✅ | ✅ |
| `ia/` | ✅ Activo | ✅ | ✅ |
| `investigador/` | ✅ Activo | ✅ | ✅ |
| `ui/` | ✅ Activo | ✅ | ✅ |
| `color/` | ✅ Activo | ✅ | ✅ |
| `multimedia/` | ✅ Activo | ✅ | ✅ |
| `tactico/` | ✅ Activo | ✅ | ✅ |
| `whatsapp/` | 🚧 Desarrollo | ⏳ | ⏳ |
| `aviso/` | 🚧 Desarrollo | ⏳ | ⏳ |

---

## 📚 DOCUMENTACIÓN RELACIONADA

### Módulos y Problemas
| Documento | Propósito |
|-----------|-----------|
| `BITACORA-GUERRA-ORQUESTADOR.md` | Retos técnicos de orquestación |
| `COLOR_MODULE.md` | Documentación técnica de color |
| `COLOR_SYSTEM.md` | Sistema de colores Hacker Neon |
| `INDEX-TESTS.md` | Índice de pruebas y logros experimentales |
| `KITTY_INIT-INICIA-KITTY-HACKER-NEON.md` | Inicialización de Kitty |
| `modulo-colores-y-diseno.md` | Módulo de colores y diseño |
| `STREAMING.md` | Implementación de streaming en tiempo real |
| `VENTANA_VS_PESTANA.md` | Diferenciación crítica ventana vs pestaña |

### Arquitectura
| Documento | Propósito |
|-----------|-----------|
| `ArquitecturadeMódulosOrientadaaIA/` | Arquitectura orientada a módulos IA |
| `PARA-DESARROLLAR-SKILL-sistema-trabajo-estructura.md` | Sistema de trabajo para skills |
| `VersionIaArquitecturadeMódulosOrientadaaIA.md` | Versión IA de arquitectura |

---

*Filosofía ARES: Orden Paranoico. Modularidad Atómica. Excelencia Técnica.*
*"1 Programador, 1 IA, actuando al unísono"*

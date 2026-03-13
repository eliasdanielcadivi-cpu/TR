# 🛰️ ARES - ÍNDICE DE MÓDULOS Y COMPONENTES

> **Verificado con estructura real:** `/home/daniel/tron/programas/TR/modules/`  
> **Última actualización:** 2026-03-13  
> **Filosofía:** Máximo 3 funciones por módulo (modularidad atómica)

---

## 🏛️ NÚCLEO

### `src/main.py` - Despachador Puro
**Propósito:** Punto de entrada único. Orquestación de comandos, sin lógica de negocio.

**Comandos:** `ares`, `ares p`, `ares i`, `ares plan`, `ares zshplan`, `ares model`, `ares models`

### `config/` - Gestión de Entorno
| Archivo | Propósito |
|---------|-----------|
| `config.yaml` | Identidad (Ares), rutas, sockets |
| `kitty.conf` | Configuración Hacker Neon |
| `kitty-minimal.conf` | Configuración mínima pruebas |
| `kitty_remote.py` | Control de terminal (`is_running`, `launch_hub`, `run`) |
| `layout_config.yaml` | Layouts de ventanas |

---

## 🧩 MÓDULOS (`modules/`)

### `admon/` - Gestión de Sistema
| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `boot_manager.py` | Lanzamiento ventana ARES | ✅ |
| `diag_manager.py` | Diagnóstico sockets/pestañas | ✅ |
| `init_manager.py` | Enlaces simbólicos, recarga config | ✅ |
| `session_manager.py` | Captura/persistencia sesiones Kitty (JSON) | ✅ |

**Funciones clave:** `capture_and_save()`, `list_sessions()`, `load_session_data()`

---

### `ia/` - Cerebro Agéntico

#### Core
| Módulo | Funciones |
|--------|-----------|
| `ai_engine.py` | `ask()`, `ask_stream()`, `chat()`, `_filter_think_chunk()`, `_resolve_provider_and_model()` |

**Modelos soportados:** `gemma`, `ares`, `mistral`, `qwen`, `llama`, `phi`, `smol`, `deepseek`

#### `providers/`
| Archivo | Propósito |
|---------|-----------|
| `base_provider.py` | Interfaz abstracta |
| `gemma_provider.py` | Ollama local con `generate_stream()` |
| `deepseek_provider.py` | API DeepSeek cloud |
| `openrouter_provider.py` | API OpenRouter |

#### `templates/`
| Archivo | Funciones |
|---------|-----------|
| `manager.py` | `TemplateManager`: `apply()`, `get_config()`, `list_templates()` |

#### `tools/`
| Archivo | Propósito |
|---------|-----------|
| `tool_registry.py` | Registro: google_search, translate, weather, shell, file ops |

#### `apollo/` - RAG + CRM (9 módulos, FASE 0-2 COMPLETADO)
| Módulo | Funciones | Fase |
|--------|-----------|------|
| `apollo_db.py` | `init_db()`, `get_connection()`, `close_db()`, `db_context()` | 0 |
| `embeddings.py` | `embed_text()`, `embed_documents()`, `quantize_embeddings()` | 0 |
| `ingest.py` | `semantic_chunk()`, `ingest_file()`, `ingest_directory()` | 1 |
| `extraction.py` | `extract_entities_relations()`, `store_entities()`, `store_relations()` | 2 |
| `retrieval.py` | `retrieve()`, `_vector_search()`, `_graph_search()`, `_relational_search()` | 2 |
| `compression.py` | `compress_context()`, `_select_relevant_docs()` | 2 |
| `generation.py` | `generate_answer()`, `generate_citations()`, `detect_hallucination()` | 2 |
| `emoji_manager.py` | `show_emoji()`, `format_output_with_emoji()` | 2 |
| `cli_ingest.py` | CLI: `python -m modules.ia.apollo.cli_ingest` | 1 |

**BDs:** `knowledge.db`, `users.db` (SQLite + sqlite-vec)  
**Embeddings:** `mxbai-embed-large:335m`

---

### `investigador/` - Exploración Web
| Tipo | CLI | Funciones |
|------|-----|-----------|
| Herramienta CLI (Tipo 2) | `tr-investigador buscar|otear|docs` | `investigar()`, `otear()`, `consultar_docs()` |

---

### `ui/` - Interfaz y Estética
| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `help_manager.py` | `show_enhanced_help()`, `query_ai()`, `list_models()`, `list_tools()` | ✅ |
| `chat_interface.py` | `start_interactive_chat()`, `_list_models_and_switch()` | ✅ |
| `layout_engine.py` | Motor de layouts | 🆕 |
| `mcat_render.py` | Renderizado demo Mcat | ✅ |

**Comandos interactivos (`ares i`):** `/model`, `/think`, `/rag`, `/clear`, `/help`, `/quit`

**Características:**
- Streaming en tiempo real
- Filtro think para modelos no pensantes
- Baja latencia (<500ms primer token)

---

### `color/` - Identidad Visual Hacker Neon
| Módulo | Tipo | CLI |
|--------|------|-----|
| `color_engine.py` | Motor de matching | `tr-color <ruta>` |
| `config.yaml` | Reglas: ruta → color/título | - |

**Docs:** `docs/Modulos-y-Sus-Problemas/COLOR_MODULE.md`, `COLOR_SYSTEM.md`

---

### `multimedia/` - Puppeteering de Medios
| Módulo | Funciones |
|--------|-----------|
| `media_manager.py` | Control de `mpv` (IPC) y `icat` |

**Binarios:** `tr-video`, `tr-image`

---

### `tactico/` - Orquestación de Flujos
| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `plan_manager.py` | `ares plan` (4 pestañas) | ✅ |
| `zsh_plan_manager.py` | `ares zshplan` | ✅ |
| `mcat_demo.py` | `ares mcat-demo` | ✅ |
| `orchestrator.py` | Despliegue desde JSON (`db/*.json`) | ✅ |

**Backups:** `SUCCESS-orchestrator-generic-v2.py`, `SUCCESS-orchestrator-resilient-v3.py`

---

### `whatsapp/` - Comunicaciones Externas
**Estado:** 🚧 En desarrollo

---

### `aviso/` - Notificaciones
**Estado:** 🚧 En desarrollo

---

## 🕵️ AGENTES (`AGENTES/`)

### `sub-agentes/sherlok/` - Auditor de Código
| Componente | Función |
|------------|---------|
| `brain.py` | Análisis de código |
| `scanner.py` | Exploración de repositorios |
| `persistence.py` | Persistencia SQLite |
| `config.yaml` | Configuración de modelos |

**Modelos:** `codellama:7b`, `qwen2.5-coder:7b-instruct`, `deepseek-r1:8b`

---

## 🔧 BINARIOS (`bin/`)

| Binario | Propósito | Origen |
|---------|-----------|--------|
| `ares` | Lanzador maestro | `src/main.py` |
| `tr-color` | Coloreado de pestañas | `modules/color/` |
| `tr-image` | Visualización de imágenes | `modules/multimedia/` |
| `tr-investigador` | Búsqueda web | `modules/investigador/` |
| `tr-kitty-init` | Inicialización Kitty | `bin/tr-kitty-init` |
| `tr-video` | Reproducción de video | `modules/multimedia/` |
| `broot` | Navegador jerárquico | `bin/broot-core/` |
| `br` | Función shell para `cd` | `bin/broot-core/` |

---

## 📁 BROOT (`bin/broot-core/`, `config/broot/`)

| Archivo | Propósito |
|---------|-----------|
| `broot-bin` | Binario estático (12MB) |
| `broot` | Wrapper con config TR |
| `br` | Función shell para `cd` |
| `conf.hjson` | Configuración principal |
| `verbs.hjson` | Comandos personalizados |

---

## 📊 ESTADO DE MÓDULOS

| Módulo | Estado | Tests | Docs |
|--------|--------|-------|------|
| `admon/` | ✅ | ✅ | ✅ |
| `ia/` | ✅ | ✅ | ✅ |
| `investigador/` | ✅ | ✅ | ✅ |
| `ui/` | ✅ | ✅ | ✅ |
| `color/` | ✅ | ✅ | ✅ |
| `multimedia/` | ✅ | ✅ | ✅ |
| `tactico/` | ✅ | ✅ | ✅ |
| `whatsapp/` | 🚧 | ⏳ | ⏳ |
| `aviso/` | 🚧 | ⏳ | ⏳ |

---

## 📚 DOCUMENTACIÓN RELACIONADA

### Bitácora Técnica
| Documento | Propósito |
|-----------|-----------|
| `Modulos-y-Sus-Problemas/BITACORA-GUERRA-ORQUESTADOR.md` | Retos de orquestación |
| `Modulos-y-Sus-Problemas/COLOR_MODULE.md` | Módulo de color |
| `Modulos-y-Sus-Problemas/COLOR_SYSTEM.md` | Sistema Hacker Neon |
| `Modulos-y-Sus-Problemas/INDEX-TESTS.md` | Pruebas y logros |
| `Modulos-y-Sus-Problemas/STREAMING.md` | Streaming en tiempo real |
| `Modulos-y-Sus-Problemas/VENTANA_VS_PESTANA.md` | Diferenciación crítica |

### Arquitectura
| Documento | Propósito |
|-----------|-----------|
| `ArquitecturadeMódulosOrientadaaIA/` | Arquitectura orientada a módulos IA |
| `PASOS-SIGUIENTES/VISION_ARES.md` | Visión estratégica (nivel industrial) |

---

*Filosofía ARES: Orden Paranoico. Modularidad Atómica. Excelencia Técnica.*  
*"1 Programador, 1 IA, actuando al unísono"*

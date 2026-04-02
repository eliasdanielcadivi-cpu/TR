# 🛰️ ARES - ÍNDICE DE MÓDULOS Y COMPONENTES

> **Verificado con estructura real:** `/home/daniel/tron/programas/TR/modules/`
> **Última actualización:** 2026-04-02
> **Filosofía:** Máximo 3 funciones por módulo (modularidad atómica)

---

## 🧠 CRITERIO DE ACTIVACIÓN DE MÓDULOS (Para IAs)

**Importante:** Este índice distingue entre módulos **ACTIVOS** (llamados desde `main.py` directa o transitivamente) y módulos **INACTIVOS/INCOMPLETOS** (existen pero no se usan).

### Cómo determinar si un módulo está activo:
1. **Activo Directo:** Importado en `src/main.py`
2. **Activo por Transitividad:** Llamado desde un módulo activo (ej: `main.py` → `ai_engine.py` → `providers/*`)
3. **Inactivo/Incompleto:** Existe en `modules/` pero no hay ruta de llamada desde `main.py`

**Regla de indexación:** Solo los módulos activos deben considerarse funcionales para producción. Los inactivos son WIP (Work In Progress).

---

## 🏛️ NÚCLEO

### `src/main.py` - Despachador Puro
**Propósito:** Punto de entrada único. Orquestación de comandos, sin lógica de negocio.

**Comandos:**
- Core: `ares`, `ares p`, `ares i`, `ares help`
- IA: `ares apollo`, `ares model-creator`, `ares modelfile-creator`, `ares models`, `ares templates`, `ares tools`
- Gestión: `ares gs`, `ares gs save`, `ares gs list`, `ares gs restore`, `ares gs deploy`, `ares gs com`, `ares gs edit`
- Alias diarios: `ares diario`, `ares diario-edit`
- Táctico: `ares plan`, `ares zshplan`, `ares mcat-demo`
- Multimedia: `ares video`, `ares image`
- Sistema: `ares status`, `ares config`, `ares init`, `ares socket-check`

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

**Estado:** ✅ ACTIVO (5 módulos)
**Uso en main.py:** `from modules.admon.boot_manager import launch_ares`, `from modules.admon.init_manager import manage_config`, `from modules.admon.diag_manager import show_status`, `from modules.admon import session_manager`

| Módulo | Funciones | Estado | Uso en main.py |
|--------|-----------|--------|----------------|
| `boot_manager.py` | `launch_ares()` - Lanzamiento ventana ARES | ✅ Activo | ✅ SÍ (directo) |
| `diag_manager.py` | `show_status()` - Diagnóstico sockets/pestañas | ✅ Activo | ✅ SÍ (directo) |
| `init_manager.py` | `manage_config()` - Enlaces simbólicos, recarga config | ✅ Activo | ✅ SÍ (directo) |
| `session_manager.py` | `capture_and_save()`, `list_sessions()`, `restore_session()`, `send_command_to_tab()` | ✅ Activo | ✅ SÍ (directo) |
| `session_editor.py` | `edit_session_interactive()` - Edición de sesiones db/*.json | ✅ Activo | ✅ SÍ (directo) |

**Comandos relacionados:**
- `ares gs edit <nombre>` - Edita sesión en micro editor
- `ares diario-edit` - Alias para editar sesión diaria
- `ares status` - Diagnóstico del sistema
- `ares init` - Gestión de infraestructura

---

### `ia/` - Cerebro Agéntico

**Estado:** ✅ ACTIVO (4 subdirectorios + apollo)
**Uso en main.py:** `from modules.ia.ai_engine import AIEngine`, `from modules.ia.apollo import retrieve, compress_context, generate_answer, generate_answer_stream`

#### Core
| Módulo | Funciones | Estado | Uso |
|--------|-----------|--------|-----|
| `ai_engine.py` | `ask()`, `ask_stream()`, `chat()`, `_filter_think_chunk()`, `_resolve_provider_and_model()` | ✅ Activo | ✅ SÍ (directo) |
| `ai_engine_filter.py` | Filtro de pensamiento para streaming | ✅ Activo | Sí (transitivo) |

**Modelos soportados:** `gemma`, `ares`, `mistral`, `qwen`, `llama`, `phi`, `smol`, `deepseek`, `ares-think`

#### `providers/`
| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `base_provider.py` | Interfaz abstracta | ✅ Activo |
| `gemma_provider.py` | Ollama local con `generate_stream()` | ✅ Activo |
| `deepseek_provider.py` | API DeepSeek cloud | ✅ Activo |
| `openrouter_provider.py` | API OpenRouter | ✅ Activo |

#### `templates/`
| Archivo | Funciones | Estado |
|---------|-----------|--------|
| `manager.py` | `TemplateManager`: `apply()`, `get_config()`, `list_templates()` | ✅ Activo |

**Plantillas:** `default`, `chat`, `code`, `tools`
**Comando:** `ares templates`

#### `tools/`
| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `tool_registry.py` | Registro: google_search, translate, weather, shell, file_ops | ✅ Activo |

**Comando:** `ares tools`

#### `apollo/` - RAG + CRM (FASE 0-2 COMPLETADO)

**Estado:** ✅ ACTIVO (12 módulos atómicos)
**Uso en main.py:** `from modules.ia.apollo import retrieve, compress_context, generate_answer, generate_answer_stream`

| Módulo | Funciones | Estado | Uso en main.py |
|--------|-----------|--------|----------------|
| `apollo_db.py` | `init_db()`, `get_connection()`, `close_db()`, `db_context()` | ✅ Activo | Sí (transitivo) |
| `embeddings.py` | `embed_text()`, `embed_documents()`, `quantize_embeddings()` | ✅ Activo | Sí (transitivo) |
| `ingest.py` | `semantic_chunk()`, `ingest_file()`, `ingest_directory()` | ✅ Activo | Sí (transitivo) |
| `retrieval.py` | `retrieve()`, `_vector_search()`, `_graph_search()`, `_relational_search()` | ✅ Activo | ✅ SÍ (directo) |
| `compression.py` | `compress_context()`, `_select_relevant_docs()` | ✅ Activo | ✅ SÍ (directo) |
| `generation.py` | `generate_answer()`, `generate_answer_stream()`, `generate_citations()` | ✅ Activo | ✅ SÍ (directo) |
| `extraction.py` | `extract_entities_relations()`, `store_entities()`, `store_relations()` | ⚠️ Incompleto | No (WIP) |
| `emoji_manager.py` | `show_emoji()`, `format_output_with_emoji()` | ⚠️ Incompleto | No (WIP) |
| `cli_ingest.py` | CLI: `python -m modules.ia.apollo.cli_ingest` | ⚠️ Incompleto | No (WIP) |
| `init_apollo_db.py` | Inicialización de BD Apollo | ⚠️ Incompleto | No (WIP) |

**BDs:** `knowledge.db`, `users.db` (SQLite + sqlite-vec)
**Embeddings:** `mxbai-embed-large:335m`
**Comandos:** `ares p "consulta" --rag`, `ares i --rag`

---

### `rag/` - Sistema RAG Híbrido V3 (Zero-Hallucination)

**Estado:** ✅ ACTIVO (8 subdirectorios, 20+ módulos)
**Uso en main.py:** `from modules.rag import RAGOrchestrator`
**Comandos:** `ares rag status`, `ares rag ingest`, `ares rag cartografo`, `ares p "consulta" --rag`, `ares i --rag`

**Arquitectura:** 5 niveles T0-T4 (Cache → SQL → Vector → Graph → Reasoning)
**Validación:** Sistema C1-C4 (Descriptivo → Operacional → Integridad → Seguridad)
**Tecnologías:** SQLite + sqlite-vec + Kùzu + Ollama/DeepSeek
**Características:** Zero-hallucination, agnosticismo estructural ($MAP pointers), inmutabilidad por sesión

#### `core/` - Núcleo del Sistema (✅ ACTIVO)
| Módulo | Funciones | Estado | Uso |
|--------|-----------|--------|-----|
| `rag_orchestrator.py` | `RAGOrchestrator`: `retrieve()`, `ingest_document()`, `get_status()`, `run_cartografo()` | ✅ Activo | ✅ SÍ (directo) |
| `tier_router.py` | `TieredRAGRouter`: `retrieve()`, routing T0-T4, lazy loading | ✅ Activo | Sí (transitivo) |
| `tier_logic.py` | Lógica de routing por niveles | ✅ Activo | Sí (transitivo) |
| `test_rag_full_atomic.py` | Tests del sistema RAG | 🧪 Test | No |

#### `engines/` - Motores Especializados (✅ ACTIVO)
| Motor | Tecnología | Funciones | Estado |
|-------|------------|-----------|--------|
| `sql_engine.py` | SQLite3 + FTS5 | `keyword_search()`, `entity_search()`, `hybrid_search()` (T1) | ✅ Activo |
| `vector_engine.py` | sqlite-vec + Ollama embeddings | `embed_text()`, `similarity_search()`, `hybrid_rerank()` (T2) | ✅ Activo |
| `graph_engine.py` | Kùzu graph database | `traverse()`, `find_relationships()`, `expand_neighborhood()` (T3) | ✅ Activo |
| `llm_engine.py` | Ollama/DeepSeek + Chain-of-Thought | `reason()`, `reason_async()`, `get_status()` (T4) | ✅ Activo |
| `graph/*` | Submódulos de grafo | Varios | ✅ Activo |
| `sql/*` | Submódulos SQL | Varios | ✅ Activo |
| `vector/*` | Submódulos vectoriales | Varios | ✅ Activo |

#### `ingestion/` - Procesamiento de Documentos (✅ ACTIVO)
| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `file_reader.py` | Lectura de archivos | ✅ Activo |
| `chunker.py` | Chunking inteligente | ✅ Activo |
| `entity_extractor.py` | Extracción de entidades | ✅ Activo |
| `graph_linker.py` | Vinculación con grafo | ✅ Activo |
| `test_ingestion_atomic.py` | Tests | 🧪 Test |

#### `ingestors/` - Ingestores Especializados (✅ ACTIVO)
| Ingestor | Formatos | Características | Estado |
|----------|----------|-----------------|--------|
| `file_ingestor.py` | `.txt`, `.md`, `.py`, `.json`, `.yaml` | Chunking inteligente, metadata extraction | ✅ Activo |
| `code_ingestor.py` | `.py` (Python) | Análisis AST, extracción de entidades y relaciones | ✅ Activo |
| `graph_builder.py` | Construcción de grafo | Vinculación de entidades | ✅ Activo |

#### `validators/` - Validación C1-C4 (✅ ACTIVO)
| Módulo | Funciones | Niveles | Estado |
|--------|-----------|---------|--------|
| `relation_guard.py` | `validate()`, `can_execute()`, `get_pending()` | C1 (Descriptivo) → C4 (Seguridad) | ✅ Activo |

#### `skills/` - Habilidades Especializadas (✅ ACTIVO)
| Skill | Propósito | Comandos | Estado |
|-------|-----------|----------|--------|
| `cartografo.py` | Gestión conversacional del grafo | `mapear`, `validar`, `conectar`, `grafo`, `salir` | ✅ Activo |

#### `storage/` - Capa de Almacenamiento (✅ ACTIVO)
| Módulo | Propósito | Estado |
|--------|-----------|--------|
| `sqlite_conn.py` | Conexión SQLite (documentos, entidades) | ✅ Activo |
| `kuzu_conn.py` | Conexión Kùzu (grafo de conocimiento) | ✅ Activo |
| `ollama_client.py` | Cliente Ollama (embeddings) | ✅ Activo |

#### `utils/` - Utilidades (✅ ACTIVO)
| Módulo | Funciones | Estado |
|--------|-----------|--------|
| `text_cleaner.py` | `normalize_text()`, `extract_keywords_clean()` | ✅ Activo |

**Bases de datos:**
- `db/rag/rag_sqlite.db` - Documentos y entidades (SQLite)
- `db/rag/rag_vector.db` - Embeddings (sqlite-vec)
- `db/rag/rag_graph.kuzu/` - Grafo de conocimiento (Kùzu)
- `db/rag/rag_core.sqlite` - Validaciones C1-C4 (RelationGuard)

**Documentación técnica:** `docs/RAG-TECNICO/RAG-MODULO-V3-IMPLEMENTACION-TECNICA.md`

---

### `investigador/` - Exploración Web

**Estado:** ✅ ACTIVO
**Binario:** `tr-investigador` en `bin/`

| Tipo | CLI | Funciones | Estado |
|------|-----|-----------|--------|
| Herramienta CLI | `tr-investigador buscar\|otear\|docs` | `investigar()`, `otear()`, `consultar_docs()` | ✅ Activo |

---

### `multimedia/` - Puppeteering de Medios

**Estado:** ✅ ACTIVO
**Uso en main.py:** `from modules.multimedia.media_manager import MediaManager`
**Binarios:** `tr-video`, `tr-image`

| Módulo | Funciones | Estado | Uso |
|--------|-----------|--------|-----|
| `media_manager.py` | `play_video()`, `show_image()` - Control de `mpv` (IPC) y `icat` | ✅ Activo | ✅ SÍ (directo) |

**Comandos:**
- `ares video <archivo>` - Reproduce video en terminal
- `ares image <archivo>` - Muestra imagen en terminal

---

### `tactico/` - Orquestación de Flujos

**Estado:** ✅ ACTIVO (4 módulos)
**Uso en main.py:** `from modules.tactico.plan_manager import deploy_plan`, `from modules.tactico.zsh_plan_manager import deploy_zsh_plan`, `from modules.tactico.mcat_demo import deploy_mcat_demo`, `from modules.tactico.orchestrator import KittyOrchestrator`

| Módulo | Funciones | Estado | Uso en main.py |
|--------|-----------|--------|----------------|
| `plan_manager.py` | `deploy_plan()` - 4 pestañas Hacker Neon | ✅ Activo | ✅ SÍ (directo) |
| `zsh_plan_manager.py` | `deploy_zsh_plan()` - Sesión ZSH | ✅ Activo | ✅ SÍ (directo) |
| `mcat_demo.py` | `deploy_mcat_demo()` - Demo táctico | ✅ Activo | ✅ SÍ (directo) |
| `orchestrator.py` | `KittyOrchestrator`: `deploy_session_from_db()` | ✅ Activo | ✅ SÍ (directo) |

**Comandos:**
- `ares plan` - Despliegue táctico (4 pestañas)
- `ares zshplan` - Hacker AI Session (ZSH)
- `ares mcat-demo` - Demo táctico
- `ares gs deploy <nombre>` - Despliega sesión desde JSON

**Backups:** `SUCCESS-orchestrator-generic-v2.py`, `SUCCESS-orchestrator-resilient-v3.py`

---

### `color/` - Identidad Visual Hacker Neon

**Estado:** ✅ ACTIVO
**Binario:** `tr-color`

| Módulo | Tipo | CLI | Estado |
|--------|------|-----|--------|
| `color_engine.py` | Motor de matching | `tr-color <ruta>` | ✅ Activo |
| `config.yaml` | Reglas: ruta → color/título | - | ✅ Activo |

**Docs:** `docs/Modulos-y-Sus-Problemas/COLOR_MODULE.md`, `COLOR_SYSTEM.md`

---

### `utils/` - Utilidades Atómicas

**Estado:** ✅ ACTIVO
**Uso en main.py:** `from modules.utils import messenger`

| Módulo | Funciones | Estado | Uso |
|--------|-----------|--------|-----|
| `messenger.py` | `warn()`, `error()`, `success()`, `info()` | ✅ Activo | ✅ SÍ (directo) |
| `text_cleaner.py` | `normalize_text()`, `extract_keywords_clean()` | ✅ Activo | Sí (transitivo) |

---

### `core/` - Núcleo Transversal

**Estado:** ✅ ACTIVO
**Uso en main.py:** `from modules.core.session_manager import init_db`, `from modules.core.window_registry import init_db`, `from modules.core.socket_manager import cleanup_orphan_socket, generate_unique_socket, get_socket_info`

| Módulo | Funciones | Estado | Uso |
|--------|-----------|--------|-----|
| `session_manager.py` | `init_db()` - Inicialización DB de sesiones | ✅ Activo | ✅ SÍ (directo) |
| `window_registry.py` | `init_db()`, `list_active_windows()`, `cleanup_stale_windows()` | ✅ Activo | ✅ SÍ (directo) |
| `socket_manager.py` | `cleanup_orphan_socket()`, `generate_unique_socket()`, `get_socket_info()` | ✅ Activo | ✅ SÍ (directo) |

**Comandos:**
- `ares windows` - Lista ventanas Kitty gestionadas
- `ares windows --cleanup` - Limpia ventanas huérfanas
- `ares socket-check` - Verifica estado de sockets

---

### `whatsapp/` - Comunicaciones Externas

**Estado:** 🚧 EN DESARROLLO (INACTIVO)
**Uso en main.py:** No se usa

| Módulo | Propósito | Estado |
|--------|-----------|--------|
| (pendiente) | Integración WhatsApp Business API | 🚧 WIP |

---

### `aviso/` - Notificaciones (Base para Carita de Ares)

**Estado:** 🚧 EN DESARROLLO (INACTIVO)
**Uso en main.py:** No se usa

| Módulo | Propósito | Estado |
|--------|-----------|--------|
| `ui_messenger.py` | Interfaz visual de avisos | 🚧 WIP |

**Nota:** El sistema de avisos existe como concepto pero no está integrado en main.py.

---

## 🕵️ AGENTES (`AGENTES/`)

### `sub-agentes/sherlok/` - Auditor de Código

**Estado:** ✅ ACTIVO
**Uso en main.py:** Sí (vía `ares agente sherlok`)
**Comando:** `ares agente sherlok`

| Componente | Función | Estado |
|------------|---------|--------|
| `brain.py` | Análisis de código con LLM | ✅ Activo |
| `scanner.py` | Exploración de repositorios | ✅ Activo |
| `persistence.py` | Persistencia SQLite | ✅ Activo |
| `config.yaml` | Configuración de modelos | ✅ Activo |
| `main.py` | Punto de entrada | ✅ Activo |

**Modelos:** `codellama:7b`, `qwen2.5-coder:7b-instruct`, `deepseek-r1:8b`

---

### `sub-agentes/Agente-De-Cambio-Estable/` - Orquestador Cognitivo Adaptativo

**Estado:** ✅ ACTIVO (HITO 2 COMPLETADO)
**Uso en main.py:** Sí (vía `modules.ui.agente_de_cambio`)
**Comando:** `ares agente AgenteDeCambio run`

**Módulos principales:**
- `cognitive-need-detector/` - Detección de necesidad cognitiva
- `mode-transition-engine/` - Motor de transición chat/cuestionario
- `questionnaire-engine/` - Generación de cuestionarios
- `session-manager/` - Gestión de sesiones
- `prompt-engine/` - Generación de prompts vivos

**Características:**
- Interfaz TUI híbrida (90% Textual + 10% Ratatui)
- Cambio automático entre chat y cuestionario
- Métricas de deriva cognitiva

---

### `sub-agentes/TRON/` - Orquestador de Modelos Cloud

**Estado:** ✅ ACTIVO
**Uso en main.py:** Sí (vía `ares agente tron`)
**Comando:** `ares agente tron`

**Providers:**
- DeepSeek (deepseek-chat, deepseek-coder)
- OpenRouter (múltiples modelos)

---

## 📊 ESTADO DE MÓDULOS (RESUMEN)

| Módulo | Estado | Tests | Docs | Uso en main.py |
|--------|--------|-------|------|----------------|
| `admon/` | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `ia/` (core+providers) | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `ia/apollo/` | ✅ Activo (6/12) | ⏳ | ✅ | ✅ Directo (3) |
| `rag/` | ✅ Activo | 🧪 | ✅ | ✅ Directo |
| `ui/` | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `investigador/` | ✅ Activo | ✅ | ✅ | ✅ Binario |
| `color/` | ✅ Activo | ✅ | ✅ | ✅ Binario |
| `multimedia/` | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `tactico/` | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `utils/` | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `core/` | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `whatsapp/` | 🚧 WIP | ⏳ | ⏳ | ❌ No |
| `aviso/` | 🚧 WIP | ⏳ | ⏳ | ❌ No |
| `AGENTES/sherlok/` | ✅ Activo | ✅ | ✅ | ✅ Sub-comando |
| `AGENTES/AgenteDeCambio/` | ✅ Activo | ✅ | ✅ | ✅ Directo |
| `AGENTES/TRON/` | ✅ Activo | ✅ | ✅ | ✅ Sub-comando |

---

## 🔧 BINARIOS (`bin/`)

| Binario | Propósito | Origen | Estado |
|---------|-----------|--------|--------|
| `ares` | Lanzador maestro | `src/main.py` | ✅ Activo |
| `tr-color` | Coloreado de pestañas | `modules/color/` | ✅ Activo |
| `tr-image` | Visualización de imágenes | `modules/multimedia/` | ✅ Activo |
| `tr-investigador` | Búsqueda web | `modules/investigador/` | ✅ Activo |
| `tr-kitty-init` | Inicialización Kitty | `bin/tr-kitty-init` | ✅ Activo |
| `tr-video` | Reproducción de video | `modules/multimedia/` | ✅ Activo |
| `broot` | Navegador jerárquico | `bin/broot-core/` | ✅ Activo |
| `br` | Función shell para `cd` | `bin/broot-core/` | ✅ Activo |
| `agenda` | Sistema de agenda táctica | `AGENDA/` | ✅ Activo |
| `ini` | Ciclo de vida (venv, prod) | `TRON/` | ✅ Activo (externo) |
| `aviso` | Recordatorios | `TRON/` | ✅ Activo (externo) |

---

## 📁 BROOT (`bin/broot-core/`, `config/broot/`)

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `broot-bin` | Binario estático (12MB) | ✅ Activo |
| `broot` | Wrapper con config TR | ✅ Activo |
| `br` | Función shell para `cd` | ✅ Activo |
| `conf.hjson` | Configuración principal | ✅ Activo |
| `verbs.hjson` | Comandos personalizados | ✅ Activo |

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

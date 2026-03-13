# 🧠 TODO: SISTEMA APOLLO — RAG HÍBRIDO ULTRALIGERO (SQLite + Vector + Grafo)

**Fecha:** 2026-03-09
**Estado:** FASE 0 ✅ | FASE 1 ✅ | FASE 2 ✅ | FASE 3 (Modelos + Assets) EN PROGRESO
**Prioridad:** FASE 3 (Imitamos — Model Creator + Assets + Post-procesamiento)

---

## 📊 ESTADO ACTUAL (2026-03-09 23:00)

### ✅ FASE 0 (Gateamos) — COMPLETADA

| Componente | Estado | Notas |
|------------|--------|-------|
| sqlite-vec instalado | ✅ v0.1.6 | Vía uv add |
| chromadb instalado | ✅ v1.5.4 | Backup |
| mxbai-embed-large:335m | ✅ Descargado | 669 MB |
| smollm3:latest | ✅ Descargado | 1.9 GB |
| bd/apollo/ creada | ✅ | knowledge.db + users.db |
| Schema RAG | ✅ | 5 tablas + índices |
| Schema CRM | ✅ | 4 tablas + índices |
| apollo_db.py | ✅ | 284 líneas, 4 funciones públicas |
| init_apollo_db.py | ✅ | Ejecutable y validado |

**Documentación:** `docs/FASE0-COMPLETADA-APOLLO-DB.md`

### ✅ FASE 1 (Caminamos — Ingesta) — COMPLETADA

| Componente | Estado | Notas |
|------------|--------|-------|
| embeddings.py | ✅ 139 líneas | `embed_text`, `embed_documents`, `quantize_embeddings` |
| ingest.py | ✅ 238 líneas | `semantic_chunk`, `ingest_file`, `ingest_directory` |
| extraction.py | ✅ 229 líneas | `extract_entities_relations`, `store_entities`, `store_relations` |
| cli_ingest.py | ✅ 189 líneas | CLI de ingesta funcional |
| Ingesta validada | ✅ | FASE0-COMPLETADA-APOLLO-DB.md (6 chunks, 615 tokens) |
| Búsqueda vectorial | ✅ | Distancia coseno 0.37-0.45 para queries relevantes |

**Documentación:** `docs/FASE1-COMPLETADA-APOLLO-INGESTA.md`

### ✅ FASE 2 (Corremos — Retrieval + Generation) — COMPLETADA

| Componente | Estado | Funciones Públicas | Notas |
|------------|--------|-------------------|-------|
| retrieval.py | ✅ 311 líneas | `retrieve()`, `_vector_search()`, `_graph_search()`, `_relational_search()`, `_rrf()` | Búsqueda híbrida con RRF |
| compression.py | ✅ 189 líneas | `compress_context()`, `_select_relevant_docs()`, `_extract_key_sentences()` | Compresión 50-75% tokens |
| generation.py | ✅ 201 líneas | `generate_answer()`, `generate_citations()`, `detect_hallucination()` | Respuestas con fuentes |
| config.yaml | ✅ Actualizado | 5 datasets (default, docs, skills, codigo, config) + alias smollm3 |
| ares i | ✅ Nuevo comando | Modo interactivo REPL con /model, /rag, /clear, /help |
| ares p --rag | ✅ Nuevo flag | `ares p "pregunta" --rag <dataset>` inyecta contexto RAG |

**Documentación:** Pendiente (FASE2)

---

## 📋 FASE 3 EN PROGRESO (Modelos + Assets + Post-procesamiento + CRM)

### 3.1 Assets y Emojis en Terminal (OBLIGATORIO)

- [x] **Instalar term-image** — `uv add term-image` para mostrar imágenes PNG en terminal
- [x] **Crear assets/ares/** — Carpeta con emoji fijo de ARES (tron-uprising-.png)
- [x] **Crear assets/user/** — Carpeta con emoji de usuario (luke-skywalker-.png)
- [x] **Módulo emoji_manager.py** — Funciones para mostrar emojis con term-image
- [ ] **Instalar mcat** — Ejecutar `bash scripts/install_mcat.sh` (obligatorio para visualización alternativa)
- [ ] **Integración en ares i** — Emojis en prompt y respuestas (COMPLETADO)

### 3.2 Model Creator (CLI con flags)

- [ ] **model_creator.py** — `list`, `create`, `update`, `delete` modelos Ollama
  - `ares model-creator list` — Listar modelos disponibles (ollama list)
  - `ares model-creator create <name> --from <parent> --params ...` — Crear modelo desde padre
  - `ares model-creator update <name> --params ...` — Actualizar parámetros
  - `ares model-creator delete <name>` — Eliminar modelo de Ollama
  - `ares model-creator show <name>` — Mostrar Modelfile asociado

### 3.3 Modelfile Creator (CLI con flags)

- [ ] **modelfile_creator.py** — `create`, `update`, `delete`, `list` Modelfiles
  - `ares modelfile-creator create <name> --from <parent> --system "..." --params ...`
  - `ares modelfile-creator update <name> --system "..." --params ...`
  - `ares modelfile-creator delete <name>`
  - `ares modelfile-creator list` — Listar Modelfiles guardados
  - `ares modelfile-creator show <name>` — Mostrar contenido

### 3.4 Persistencia de Modelfiles

- [ ] **bd/apollo/modelfiles.yaml** — Base de datos YAML con Modelfiles
  - Estructura: `{model_name: {parent, system, parameters, template, created_at}}`
  - Backup automático en cada modificación

### 3.5 Post-procesamiento Configurable

- [ ] **config.yaml** — Lista de post-procesamiento por modelo
  ```yaml
  post_processing:
    ares:
      strip_think_tags: true  # Eliminar <think></think>
    ares-think:
      strip_think_tags: false  # Mantener etiquetas
    smollm3:
      strip_think_tags: true
  ```
- [ ] **generation.py** — Aplicar post-procesamiento según modelo

### 3.6 Flags Think en Comandos

- [ ] **main.py** — `ares i --think` y `ares p --think`
  - `--think` fuerza uso de modelo pensante (ares-think)
  - Sin `--think` usa modelo normal (ares)
  - Prioridad: flag > config > default

### 3.7 Documentación de Modelos

- [ ] **docs/MODELOS-ARES.md** — Documentación completa
  - Lista de modelos disponibles
  - Modelfiles originales (padres)
  - Parámetros configurados
  - Instrucciones de recreación

---

### 3.8 Módulo CRM Básico (MANTENER - Original)

- [ ] **crm.py** — `create_client()`, `update_client()`, `search_clients()`
- [ ] **interactions.py** — `log_interaction()`, `get_client_history()`, `get_follow_ups()`
- [ ] **whatsapp_integration.py** — `import_whatsapp_chat()`, `link_client_to_documents()`, `generate_client_summary()`

### 3.9 CLI de CRM (MANTENER - Original)

- [ ] **ares apollo crm** — Subcomandos: `list`, `view`, `add`, `interact`, `followups`, `import-whatsapp`

### 3.10 Integración con WhatsApp (MANTENER - Original)

- [ ] Parser de exportaciones TXT de WhatsApp
- [ ] Detección automática de clientes por número
- [ ] Registro de mensajes como interacciones

---

## 📚 COMANDOS DISPONIBLES (ACTUALIZADO)

### Ingesta

```bash
# Ingestar archivo individual
python -m modules.ia.apollo.cli_ingest <archivo.md>

# Ingestar con extracción de entidades
python -m modules.ia.apollo.cli_ingest <archivo.md> --extract --model smollm3

# Ingestar directorio completo
python -m modules.ia.apollo.cli_ingest <directorio/> --json
```

### Consulta RAG

```bash
# Consulta con RAG (dataset específico)
ares p "¿Qué es Apollo?" --rag docs
ares p "¿Cómo usar skills?" --rag skills
ares p "Explica este código" --rag codigo

# Con modo think (usa ares-think)
ares p "¿Quién eres?" --rag docs --think

# Modo interactivo
ares i                      # Sin RAG
ares i --rag docs           # Con RAG en dataset docs
ares i --rag skills --model gemma3:4b
ares i --think              # Con modo pensante
```

### Comandos Interactivos (/help)

```
/quit, /exit  - Salir
/model <nombre> - Cambiar modelo LLM
/rag <dataset>  - Cambiar dataset (default, docs, skills, codigo, config)
/think          - Activar/desactivar modo pensante
/clear          - Limpiar pantalla
/help           - Ayuda
```

### Model Creator (NUEVO)

```bash
# Listar modelos
ares model-creator list

# Crear modelo desde padre
ares model-creator create ares-custom --from alibayram/smollm3:latest \
  --temperature 0.4 --top_p 0.9 --num_predict 2048

# Actualizar parámetros
ares model-creator update ares-custom --temperature 0.7

# Eliminar modelo
ares model-creator delete ares-custom

# Mostrar Modelfile
ares model-creator show ares
```

### Modelfile Creator (NUEVO)

```bash
# Crear Modelfile
ares modelfile-creator create ares-think --from alibayram/smollm3:latest \
  --system "Eres ARES, orquestador táctico..." \
  --param temperature 0.4 --param top_p 0.9

# Actualizar Modelfile
ares modelfile-creator update ares-think --system "Nuevo system prompt..."

# Eliminar Modelfile
ares modelfile-creator delete ares-think

# Listar Modelfiles guardados
ares modelfile-creator list

# Mostrar Modelfile
ares modelfile-creator show ares-think
```

---

## 📊 ANÁLISIS DE PERSISTENCIA ACTUAL

### Estado Actual (db/)

| Archivo | Tipo | Contenido | Multiusuario | Escalable |
|---------|------|-----------|--------------|-----------|
| `avisos.db` | SQLite | Recordatorios, alarmas, comandos programados | ❌ Single-user | ⚠️ Limitada |
| `*.json` | JSON | Sesiones de Kitty (ultima.json, diaria.json, etc.) | ❌ Single-user | ❌ No |
| `Construccion-Ares.json` | JSON | Datos de construcción del proyecto | ❌ Single-user | ❌ No |

### Características del Sistema Actual

**✅ Lo que SÍ es persistente:**
- Sesiones de Kitty se guardan en `db/{nombre}.json` con estructura completa (tabs, títulos, comandos, layout)
- Avisos/recordatorios en SQLite con schema definido (id, mensaje, fecha, ejecutado)
- Los archivos JSON sobreviven a reinicios del sistema

**❌ Lo que NO es persistente:**
- Historial de consultas `ares p` (prompts → respuestas) NO se guarda
- No hay tracking de conversaciones por usuario
- No hay contexto acumulativo entre sesiones
- No hay base de conocimiento indexada (vectores, embeddings, grafo)

**⚠️ Multiusuario:**
- **NO hay separación por usuario** — todo va a `db/` sin prefijo de usuario
- **NO hay autenticación** — cualquiera con acceso al filesystem puede leer/reescribir
- **NO hay aislamiento** — sesiones y avisos son compartidos

### Decisión: ¿Reutilizar o Crear Persistencia Aparte?

**DECISIÓN: Crear persistencia SEPARADA pero integrada**

**Razones:**
1. **Separación de responsabilidades**: `db/` actual es para sesiones Kitty y avisos (operativo). RAG/CRM requiere schema relacional + vectorial complejo.
2. **Escalabilidad**: SQLite con sqlite-vec requiere configuración específica (BLOBs, tablas virtuales vec0)
3. **Multiusuario**: CRM requiere tablas `users`, `clients`, `interactions` con foreign keys
4. **Filosofía TRON**: Cada módulo atómico tiene SU propia persistencia (ver `modules/aviso/aviso_db.py`)

**Implementación:**
- **Nueva carpeta**: `data/apollo/` (o `data/knowledge/`)
- **Archivos**:
  - `knowledge.db` — SQLite principal (chunks, embeddings, entities, relations)
  - `knowledge_graph.db` — Kuzu embebido (grafo de conocimiento)
  - `users.db` — SQLite para usuarios y CRM (o integrar en knowledge.db)
- **Módulo**: `modules/ia/apollo/` con submódulos atómicos

---

## 🎯 FASE 0: GATEAMOS — Fundamentos (Semana 1)

### 0.1 Análisis y Decisión de Arquitectura
- [ ] **Leer informe técnico completo**: `docs/INFORME-TECNICO-ARQUITECTURA-RAG-HIBRIDA-ULTRALIGERA-DE-ALTA-EFICACIA.md`
- [ ] **Validar stack tecnológico** para entorno minimalista (Lubuntu + Openbox + 8GB RAM):
  - [ ] SQLite + sqlite-vec (¿disponible en Ubuntu repos?)
  - [ ] Kuzu (¿pip installable? ¿dependencias C++?)
  - [ ] Ollama embeddings (`embeddinggemma` o `all-minilm`)
  - [ ] hnswlib/Annoy (¿necesario para >10k vectores?)
- [ ] **Definir límites de Fase 0**: Solo persistencia básica, SIN RAG activo aún

### 0.2 Infraestructura de Persistencia
- [ ] **Crear estructura de carpetas**:
  ```
  data/apollo/
  ├── knowledge.db          # SQLite principal
  ├── knowledge_graph.db    # Kuzu (si se usa)
  ├── users.db              # Usuarios + CRM
  └── README.md             # Schema documentation
  ```
- [ ] **Módulo de persistencia atómico**: `modules/ia/apollo/apollo_db.py`
  - [ ] Máximo 3 funciones públicas: `init_db()`, `get_connection()`, `close_db()`
  - [ ] Carga lazy de sqlite-vec (solo si existe)
  - [ ] Schema mínimo viable (tablas vacías, listas para ingestar)

### 0.3 Schema SQLite para RAG + CRM
- [ ] **Tablas RAG (knowledge.db)**:
  ```sql
  -- Documentos fuente
  CREATE TABLE documents (
      id TEXT PRIMARY KEY,
      title TEXT,
      source TEXT,  -- ruta archivo o URL
      ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      metadata JSON
  );

  -- Chunks de texto
  CREATE TABLE chunks (
      id TEXT PRIMARY KEY,
      document_id TEXT REFERENCES documents(id),
      chunk_index INTEGER,
      text TEXT,
      tokens INTEGER,
      parent_chunk_id TEXT REFERENCES chunks(id)  -- jerarquía
  );

  -- Embeddings (sqlite-vec)
  CREATE VIRTUAL TABLE embeddings USING vec0(
      chunk_id TEXT PRIMARY KEY,
      vector FLOAT[384],  -- 384 dims para all-MiniLM-L6-v2
      document_id TEXT,
      chunk_index INTEGER
  );

  -- Entidades extraídas (grafo relacional)
  CREATE TABLE entities (
      id TEXT PRIMARY KEY,
      name TEXT,
      type TEXT,  -- Persona, Organización, Concepto, Producto, Lugar
      description TEXT,
      embedding FLOAT[384]  -- para búsqueda semántica de entidades
  );

  -- Relaciones entre entidades
  CREATE TABLE relations (
      id TEXT PRIMARY KEY,
      subject_id TEXT REFERENCES entities(id),
      predicate TEXT,  -- "trabaja_en", "creó", "es_tipo_de"
      object_id TEXT REFERENCES entities(id),
      chunk_id TEXT REFERENCES chunks(id),  -- fuente de la relación
      confidence FLOAT DEFAULT 1.0
  );
  ```

- [ ] **Tablas CRM (users.db o knowledge.db)**:
  ```sql
  -- Usuarios del sistema ARES
  CREATE TABLE users (
      id TEXT PRIMARY KEY,  -- UUID o username
      name TEXT,
      email TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      last_active TIMESTAMP,
      preferences JSON  -- provider preferido, modelo, templates
  );

  -- Clientes (decantados de múltiples fuentes)
  CREATE TABLE clients (
      id TEXT PRIMARY KEY,
      name TEXT,
      type TEXT,  -- empresa, individuo, lead, partner
      source TEXT,  -- "whatsapp", "email", "web", "import"
      status TEXT,  -- "active", "inactive", "lead", "converted"
      metadata JSON,  -- datos custom por fuente
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP
  );

  -- Interacciones con clientes
  CREATE TABLE interactions (
      id TEXT PRIMARY KEY,
      client_id TEXT REFERENCES clients(id),
      user_id TEXT REFERENCES users(id),
      type TEXT,  -- "chat", "email", "call", "meeting", "note"
      channel TEXT,  -- "whatsapp", "email", "phone", "in_person"
      summary TEXT,  -- resumen ejecutivo
      full_content TEXT,  -- contenido completo (transcripción, email, etc.)
      sentiment TEXT,  -- "positive", "neutral", "negative"
      action_items JSON,  -- lista de follow-ups
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  -- Relaciones cliente-documento (para RAG específico por cliente)
  CREATE TABLE client_documents (
      client_id TEXT REFERENCES clients(id),
      document_id TEXT REFERENCES documents(id),
      relevance_score FLOAT,
      PRIMARY KEY (client_id, document_id)
  );
  ```

### 0.4 Scripts de Inicialización
- [ ] **Script CLI**: `scripts/init_apollo_db.py`
  - [ ] Crea `data/apollo/` directorio
  - [ ] Inicializa `knowledge.db` con schema RAG
  - [ ] Inicializa `users.db` con schema CRM
  - [ ] Crea usuario por defecto (daniel) si no existe
  - [ ] Output: `✅ Apollo DB inicializada en data/apollo/`

---

## 🚶 FASE 1: CAMINAMOS — Ingesta Básica (Semana 2-3)

### 1.1 Sistema de Embeddings
- [ ] **Módulo**: `modules/ia/apollo/embeddings.py`
  - [ ] Función 1: `embed_text(text: str, model: str = "embeddinggemma") -> np.ndarray`
    - Usa Ollama API (`ollama.embed()`)
    - Batch processing para múltiples textos
    - Retorna numpy array float32 (384 dims)
  - [ ] Función 2: `embed_documents(file_paths: List[str]) -> Dict[str, np.ndarray]`
    - Lee archivos de texto
    - Chunking semántico (por oraciones, 512 tokens)
    - Genera embeddings por chunk
    - Retorna dict {chunk_id: embedding}
  - [ ] Función 3: `quantize_embeddings(vectors: np.ndarray, bits: int = 8) -> Tuple[np.ndarray, np.ndarray, np.ndarray]`
    - Cuantización INT8/INT4 para reducir memoria 50-75%
    - Retorna (quantized, scales, zero_points)

### 1.2 Ingesta de Documentos
- [ ] **Módulo**: `modules/ia/apollo/ingest.py`
  - [ ] Función 1: `ingest_file(file_path: str, user_id: str = "daniel") -> Dict`
    - Lee archivo (texto, markdown, PDF si es posible)
    - Chunking semántico
    - Genera embeddings
    - Inserta en SQLite (documents, chunks, embeddings)
    - Retorna metadata (chunks_count, tokens_total, file_size)
  - [ ] Función 2: `ingest_directory(dir_path: str, patterns: List[str] = ["*.md", "*.txt"]) -> Dict`
    - Recorre directorio recursivamente
    - Filtra por patrones
    - Llama a `ingest_file()` por cada archivo
    - Retorna resumen (files_ingested, total_chunks, total_tokens)
  - [ ] Función 3: `semantic_chunk(text: str, max_tokens: int = 512) -> List[str]`
    - Divide por oraciones (regex: `(?<=[.!?])\s+`)
    - Agrupa hasta max_tokens
    - Mantiene coherencia semántica (no corta párrafos)

### 1.3 Extracción de Entidades y Relaciones
- [ ] **Módulo**: `modules/ia/apollo/extraction.py`
  - [ ] Función 1: `extract_entities_relations(text: str, model: str = "gemma3:4b") -> ExtractionResult`
    - Usa Gemma3 con structured output (JSON schema)
    - Extrae entidades: (nombre, tipo)
    - Extrae relaciones: (sujeto, predicado, objeto)
    - Retorna Pydantic model
  - [ ] Función 2: `store_entities(entities: List[Entity], chunk_id: str) -> int`
    - Inserta entidades en SQLite
    - Genera embeddings para entidades
    - Retorna count de entidades guardadas
  - [ ] Función 3: `store_relations(relations: List[Relation], chunk_id: str) -> int`
    - Inserta relaciones en SQLite
    - Valida foreign keys (subject_id, object_id existen)
    - Retorna count de relaciones guardadas

### 1.4 CLI de Ingesta
- [ ] **Comando ARES**: `ares apollo ingest <ruta>`
  - [ ] Si es archivo: ingesta单个
  - [ ] Si es directorio: ingesta masiva
  - [ ] Opciones:
    - `--user <id>`: Usuario propietario (default: daniel)
    - `--model <embedding>`: Modelo de embeddings (default: embeddinggemma)
    - `--chunk-size <tokens>`: Tamaño de chunk (default: 512)
    - `--quantize <bits>`: Cuantización (default: 8, opciones: 4, 8, none)
    - `--json`: Output en JSON para piping
  - [ ] Output ejemplo:
    ```
    ✅ Ingestado: documento.md
       Chunks: 15 | Tokens: 7,500 | Embeddings: 384 dims
       Entidades: 23 | Relaciones: 18
       Tiempo: 12.3s
    ```

---

## 🏃 FASE 2: CORREMOS — Recuperación Híbrida (Semana 4-5)

### 2.1 Sistema de Recuperación
- [ ] **Módulo**: `modules/ia/apollo/retrieval.py`
  - [ ] Función 1: `retrieve(query: str, k: int = 5, mode: str = "fused") -> RetrievalResult`
    - Orquesta los 3 tipos de búsqueda (vectorial, grafo, relacional)
    - Fusiona resultados con RRF (Reciprocal Rank Fusion)
    - Retorna resultados con scores y fuentes
  - [ ] Función 2: `vector_search(query: str, k: int) -> List[ChunkResult]`
    - Genera embedding de query
    - Búsqueda KNN en sqlite-vec (distancia coseno)
    - Retorna chunks ordenados por similitud
  - [ ] Función 3: `graph_search(query: str, k: int) -> List[EntityResult]`
    - Extrae entidades de query
    - Busca vecinos en grafo (1-2 hops)
    - Retorna entidades relacionadas con paths

### 2.2 Compresión Contextual
- [ ] **Módulo**: `modules/ia/apollo/compression.py`
  - [ ] Función 1: `compress_context(documents: List[str], query: str, max_tokens: int = 2000) -> str`
    - Selección binaria (documento relevante/irrelevante con Gemma3)
    - Extracción de oraciones clave (top 3 por documento)
    - Truncamiento preservando oraciones completas
    - Retorna contexto comprimido
  - [ ] Función 2: `select_relevant_docs(docs: List[str], query: str) -> List[str]`
    - Gemma3 clasifica cada doc como relevante/irrelevante
    - Filtra docs irrelevantes
    - Retorna solo relevantes
  - [ ] Función 3: `extract_key_sentences(doc: str, query: str, top_n: int = 3) -> List[str]`
    - Embedding de oraciones vs query
    - Similaridad coseno
    - Retorna top_n oraciones más similares

### 2.3 Generación de Respuestas
- [ ] **Módulo**: `modules/ia/apollo/generation.py`
  - [ ] Función 1: `generate_answer(query: str, context: str, model: str = "gemma3:4b") -> str`
    - Prompt template con contexto + pregunta
    - Instrucción estricta: "Responde SOLO con información del contexto"
    - Temperature baja (0.1) para precisión
    - Retorna respuesta generada
  - [ ] Función 2: `generate_citations(answer: str, sources: List[Chunk]) -> str`
    - Añade referencias a fuentes al final
    - Formato: `[1] documento.md:chunk_3`
    - Retorna respuesta con citas
  - [ ] Función 3: `detect_hallucination(answer: str, context: str) -> float`
    - Score de confianza (0-1)
    - Verifica que cada afirmación esté en contexto
    - Retorna score (1 = totalmente fundamentado)

### 2.4 CLI de Consulta
- [ ] **Comando ARES**: `ares apollo query "<pregunta>"`
  - [ ] Opciones:
    - `--mode <tipo>`: Tipo de búsqueda (vector, graph, relational, fused)
    - `--model <llm>`: Modelo para generación (default: gemma3:4b)
    - `--top-k <n>`: Cantidad de resultados (default: 5)
    - `--compress`: Activar compresión contextual
    - `--json`: Output en JSON
    - `--stream`: Streaming de respuesta (si el modelo soporta)
  - [ ] Output ejemplo:
    ```
    🧠 Pregunta: ¿Qué es la arquitectura RAG?

    📝 Respuesta:
    La arquitectura RAG (Retrieval-Augmented Generation) combina recuperación
    de información con generación de lenguaje natural para producir respuestas
    precisas y fundamentadas...

    📚 Fuentes:
    [1] INFORME-TECNICO-RAG.md:chunk_7 (score: 0.89)
    [2] Documento de Inicio.md:chunk_23 (score: 0.76)

    ⚡ Tokens contexto: 1,847 | Tiempo: 3.2s
    ```

---

## 🎭 FASE 3: IMITAMOS — CRM de Clientes (Semana 6-7)

### 3.1 Gestión de Clientes
- [ ] **Módulo**: `modules/ia/apollo/crm.py`
  - [ ] Función 1: `create_client(name: str, type: str, source: str, metadata: Dict = None) -> str`
    - Crea cliente en SQLite
    - Genera ID único (UUID)
    - Retorna client_id
  - [ ] Función 2: `update_client(client_id: str, updates: Dict) -> bool`
    - Actualiza campos del cliente
    - Actualiza `updated_at` timestamp
    - Retorna success/failure
  - [ ] Función 3: `search_clients(query: str, status: str = None, type: str = None) -> List[Dict]`
    - Búsqueda semántica (nombre, metadata)
    - Filtros opcionales (status, type)
    - Retorna lista de clientes matching

### 3.2 Registro de Interacciones
- [ ] **Módulo**: `modules/ia/apollo/interactions.py`
  - [ ] Función 1: `log_interaction(client_id: str, type: str, summary: str, user_id: str = "daniel", **kwargs) -> str`
    - Registra interacción en SQLite
    - Extrae action_items automáticamente (con Gemma3)
    - Analiza sentimiento (positive/neutral/negative)
    - Retorna interaction_id
  - [ ] Función 2: `get_client_history(client_id: str, limit: int = 50) -> List[Dict]`
    - Obtiene todas las interacciones de un cliente
    - Ordena cronológicamente (más reciente primero)
    - Retorna historial completo
  - [ ] Función 3: `get_follow_ups(user_id: str = "daniel", status: str = "pending") -> List[Dict]`
    - Extrae action_items de todas las interacciones
    - Filtra por status (pending, completed, overdue)
    - Retorna lista de follow-ups pendientes

### 3.3 Integración con WhatsApp
- [ ] **Módulo**: `modules/ia/apollo/whatsapp_integration.py`
  - [ ] Función 1: `import_whatsapp_chat(export_file: str, client_phone: str) -> Dict`
    - Parsea exportación de WhatsApp (texto)
    - Identifica mensajes por número
    - Crea/actualiza cliente por phone number
    - Registra mensajes como interacciones
    - Retorna resumen (messages_imported, date_range)
  - [ ] Función 2: `link_client_to_documents(client_id: str, document_ids: List[str]) -> int`
    - Asocia documentos específicos a cliente
    - Permite RAG personalizado por cliente
    - Retorna count de documentos vinculados
  - [ ] Función 3: `generate_client_summary(client_id: str) -> str`
    - Gemma3 genera resumen ejecutivo del cliente
    - Incluye: historial, preferencias, action_items, sentiment_trend
    - Retorna resumen en texto natural

### 3.4 CLI de CRM
- [ ] **Comando ARES**: `ares apollo crm <subcomando>`
  - [ ] Subcomandos:
    - `list [--status <status>] [--type <type>]`: Lista clientes
    - `view <client_id>`: Ver historial completo
    - `add <name> [--type <type>] [--source <source>]`: Crear cliente
    - `interact <client_id> <summary> [--type <type>]`: Registrar interacción
    - `followups [--user <user_id>]`: Ver follow-ups pendientes
    - `import-whatsapp <export_file> <client_phone>`: Importar chat
  - [ ] Output ejemplo:
    ```
    👥 Clientes (3 encontrados):

    1. Empresa XYZ (empresa, active)
       Última interacción: 2026-03-08 (meeting)
       Follow-ups: 2 pendientes

    2. Juan Pérez (individuo, lead)
       Última interacción: 2026-03-05 (call)
       Follow-ups: 1 pendiente

    3. Tech Solutions (empresa, converted)
       Última interacción: 2026-03-01 (email)
       Follow-ups: 0 pendientes
    ```

---

## 🚀 FASE 4: IGUALAMOS — RAG en Producción (Semana 8-9)

### 4.1 Integración con `ares p`
- [ ] **Módulo**: `modules/ia/apollo/ares_integration.py`
  - [ ] Función 1: `inject_rag_context(prompt: str, user_id: str = "daniel") -> str`
    - Detecta si prompt requiere contexto (keywords: "mi cliente", "documento", "proyecto")
    - Recupera contexto relevante (RAG híbrido)
    - Inyecta contexto en prompt antes de enviar a LLM
    - Retorna prompt enriquecido
  - [ ] Función 2: `log_query_response(query: str, response: str, user_id: str) -> str`
    - Guarda query y respuesta en SQLite
    - Vincula a usuario
    - Permite historial de consultas
    - Retorna log_id
  - [ ] Función 3: `suggest_follow_up(client_interactions: List[Dict]) -> str`
    - Analiza historial de cliente
    - Gemma3 sugiere próximo paso (email, call, meeting)
    - Retorna sugerencia en texto natural

### 4.2 Dashboard de Conocimiento
- [ ] **Módulo**: `modules/ia/apollo/dashboard.py`
  - [ ] Función 1: `generate_knowledge_stats(user_id: str = "daniel") -> Dict`
    - Cuenta: documentos, chunks, entidades, relaciones, clientes
    - Calcula: total_tokens, avg_chunk_size, top_entity_types
    - Retorna estadísticas completas
  - [ ] Función 2: `generate_client_activity_report(days: int = 30) -> str`
    - Últimas interacciones por cliente
    - Follow-ups completados vs pendientes
    - Sentiment trends (gráfico ASCII si es posible)
    - Retorna reporte en texto
  - [ ] Función 3: `visualize_knowledge_graph(limit: int = 50) -> str`
    - Extrae top N entidades y relaciones
    - Genera grafo ASCII (o DOT para Graphviz)
    - Retorna visualización

### 4.3 CLI de Dashboard
- [ ] **Comando ARES**: `ares apollo dashboard`
  - [ ] Subcomandos:
    - `stats`: Estadísticas de conocimiento
    - `activity [--days <n>]`: Actividad reciente de clientes
    - `graph [--limit <n>]`: Visualización de grafo
  - [ ] Output ejemplo:
    ```
    📊 APOLLO DASHBOARD — daniel

    📚 Conocimiento:
       Documentos: 127 | Chunks: 1,843 | Tokens: 945,000
       Entidades: 456 | Relaciones: 892

    👥 Clientes:
       Activos: 12 | Leads: 5 | Inactivos: 3
       Interacciones (30 días): 47
       Follow-ups pendientes: 8

    🔥 Top Entidades:
       Persona: 234
       Organización: 128
       Concepto: 94
    ```

---

## 🌟 FASE 5: SUPERAMOS — Optimización y Multiusuario (Semana 10+)

### 5.1 Multiusuario Real
- [ ] **Módulo**: `modules/ia/apollo/auth.py`
  - [ ] Función 1: `create_user(username: str, name: str, email: str) -> str`
    - Crea usuario con UUID
    - Hash de password (si se implementa auth)
    - Retorna user_id
  - [ ] Función 2: `authenticate_user(username: str, password: str) -> Tuple[bool, str]`
    - Verifica credenciales
    - Retorna (success, token o error)
  - [ ] Función 3: `get_user_preferences(user_id: str) -> Dict`
    - Obtiene provider preferido, modelo, templates
    - Retorna preferencias

### 5.2 Aislamiento de Datos
- [ ] **Módulo**: `modules/ia/apollo/isolation.py`
  - [ ] Función 1: `get_user_data_scope(user_id: str) -> Dict`
    - Obtiene todos los datos de un usuario (documentos, clientes, interacciones)
    - Retorna scope completo
  - [ ] Función 2: `share_document(owner_id: str, document_id: str, target_user_id: str, permissions: str) -> bool`
    - Comparte documento con otro usuario
    - Permissions: read, write, admin
    - Retorna success/failure
  - [ ] Función 3: `create_team(team_name: str, owner_id: str, member_ids: List[str]) -> str`
    - Crea equipo con miembros
    - Retorna team_id
    - Permite compartir datos por equipo

### 5.3 Optimización de Memoria
- [ ] **Módulo**: `modules/ia/apollo/optimization.py`
  - [ ] Función 1: `optimize_embeddings_memory(bits: int = 8) -> Dict`
    - Aplica cuantización a todos los embeddings
    - Reduce memoria 50-75%
    - Retorna ahorro (original_size, optimized_size, savings_percent)
  - [ ] Función 2: `prune_old_data(retention_days: int = 365) -> int`
    - Elimina datos más antiguos que retention_days
    - Mantiene integridad referencial
    - Retorna count de registros eliminados
  - [ ] Función 3: `vacuum_database(db_path: str) -> int`
    - Ejecuta VACUUM en SQLite
    - Reclama espacio en disco
    - Retorna tamaño antes/después

### 5.4 Exportación e Importación
- [ ] **Módulo**: `modules/ia/apollo/export_import.py`
  - [ ] Función 1: `export_user_data(user_id: str, output_path: str) -> str`
    - Exporta todos los datos de usuario a JSON/SQLite
    - Formato portable (backup o migración)
    - Retorna ruta de archivo exportado
  - [ ] Función 2: `import_user_data(export_file: str, target_user_id: str) -> Dict`
    - Importa datos exportados
    - Maneja conflictos (IDs duplicados)
    - Retorna resumen (records_imported, conflicts_resolved)
  - [ ] Función 3: `migrate_from_json_to_sqlite(json_dir: str, db_path: str) -> Dict`
    - Migración desde sistema JSON actual a SQLite
    - Preserva todos los datos
    - Retorna resumen de migración

---

## 📋 CRITERIOS DE ACEPTACIÓN POR FASE

### Fase 0 (Gateamos)
- [ ] `data/apollo/` existe con `knowledge.db` y `users.db` inicializados
- [ ] Schema RAG + CRM creado y validado (sin datos)
- [ ] Script `init_apollo_db.py` ejecutable y funcional

### Fase 1 (Caminamos)
- [ ] `ares apollo ingest <archivo>` funciona y muestra estadísticas
- [ ] Embeddings generados con Ollama y almacenados en sqlite-vec
- [ ] Entidades y relaciones extraídas con Gemma3

### Fase 2 (Corremos)
- [ ] `ares apollo query "<pregunta>"` responde con contexto recuperado
- [ ] Compresión contextual reduce tokens 50%+ sin perder calidad
- [ ] Citas de fuentes incluidas en respuestas

### Fase 3 (Imitamos)
- [ ] CRM funcional: crear, ver, actualizar clientes
- [ ] Interacciones registradas con action_items y sentimiento
- [ ] Importación de WhatsApp funcional

### Fase 4 (Igualamos)
- [ ] `ares p` inyecta contexto RAG automáticamente
- [ ] Dashboard muestra estadísticas y grafo de conocimiento
- [ ] Historial de queries guardado por usuario

### Fase 5 (Superamos)
- [ ] Múltiples usuarios con datos aislados
- [ ] Compartir documentos entre usuarios
- [ ] Cuantización de embeddings reduce memoria 50%+
- [ ] Exportación/importación de datos funcional

---

## 🔗 DEPENDENCIAS EXTERNAS

| Dependencia | Versión | Propósito | Instalación |
|-------------|---------|-----------|-------------|
| `sqlite-vec` | >=0.1.0 | Búsqueda vectorial en SQLite | `pip install sqlite-vec` |
| `kuzu` | >=0.5.0 | Graph database embebida | `pip install kuzu` |
| `hnswlib` | >=0.8.0 | Indexación HNSW (opcional) | `pip install hnswlib` |
| `numpy` | >=1.24.0 | Arrays para embeddings | `pip install numpy` |
| `pydantic` | >=2.0.0 | Validación de datos | `pip install pydantic` |
| `requests` | >=2.31.0 | HTTP para Ollama API | `pip install requests` |

---

## 📊 MÉTRICAS DE ÉXITO

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Latencia de consulta** | <3s para RAG híbrido | `time ares apollo query "..."` |
| **Precisión de respuestas** | >90% fundamentadas | `detect_hallucination()` score |
| **Compresión de contexto** | 50-75% reducción tokens | `len(context) / len(original_docs)` |
| **Memoria de embeddings** | <500MB para 10k vectores | `du -sh data/apollo/knowledge.db` |
| **Clientes gestionados** | >50 en primer mes | `SELECT COUNT(*) FROM clients` |
| **Usuarios concurrentes** | 2-5 sin degradación | Testing manual multiusuario |

---

## ⚠️ RIESGOS Y MITIGACIONES

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|--------------|------------|
| sqlite-vec no disponible en Ubuntu repos | Alto | Media | Compilar desde fuente o usar wheel |
| Kuzu consume demasiada memoria | Medio | Baja | Usar solo SQLite con relaciones si es necesario |
| Ollama embeddings lento (>1s por chunk) | Alto | Media | Batch processing + cuantización |
| Multiusuario requiere autenticación compleja | Medio | Media | Empezar con user_id en requests, sin auth real |
| WhatsApp export format cambia | Bajo | Baja | Parser flexible, documentar formato esperado |

---

*Este TODO es un documento vivo. Actualizar después de cada fase completada.*

**Próximo paso inmediato:** Comenzar Fase 0 — Validar disponibilidad de sqlite-vec y Kuzu en el entorno actual.

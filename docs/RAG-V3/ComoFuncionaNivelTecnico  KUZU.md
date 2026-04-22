
    🗺️ 1. Base de Datos de Grafo: Relaciones en Kùzu

    Schema del Grafo
    El grafo se almacena en db/rag/rag_graph.kuzu/ usando Kùzu graph database.

    Nodos: Tabla `Entity`

    ┌────────────┬─────────┬───────────────────────────────────────────────────────┐
    │ Campo      │ Tipo    │ Restricciones                                         │
    ├────────────┼─────────┼───────────────────────────────────────────────────────┤
    │ name       │ STRING  │ PRIMARY KEY                                           │
    │ type       │ STRING  │ "function", "class", "concept", "heading", "document" │
    │ source_doc │ STRING  │ ID del documento origen                               │
    │ validated  │ BOOLEAN │ default false                                         │
    └────────────┴─────────┴───────────────────────────────────────────────────────┘


    3 Tablas de Relaciones (edges tipados):


    ┌────────────┬───────────────────────┬────────────────────────────────────────┐
    │ Relación   │ Propósito             │ Propiedades                            │
    ├────────────┼───────────────────────┼────────────────────────────────────────┤
    │ `REQUIRES` │ Dependencia/ejecución │ weight, criticality (C1-C4), validated │
    │`RELATES_TO`│ Asociación semántica  │ relation_type, confidence, context     │
    │ `PART_OF`  │ Jerarquía/contención  │ order_idx                              │
    └────────────┴───────────────────────┴────────────────────────────────────────┘


    Cómo se crean las relaciones

    Extracción automática (2 vías):

     1. RAG Module (reglas): FileIngestor extrae funciones/clases vía regex/AST, luego GraphBuilder crea edges RELATES_TO entre entidades
        consecutivas del mismo documento (co-ocurrencia, confianza 0.7)

     2. Apollo Module (LLM): Usa smollm3:latest vía Ollama para extraer entidades y relaciones en JSON estructurado. Tipos válidos: Persona,
        Organizacion, Concepto, Producto, Lugar, Evento, Fecha, Tecnologia

    Cómo el usuario puede modificar el grafo

    Skill Cartógrafo (ares rag cartografo):


    ┌────────────────────┬───────────────────────────────────────────────────┐
    │ Comando            │ Acción                                            │
    ├────────────────────┼───────────────────────────────────────────────────┤
    │ mapear [archivo]   │ Analiza y propone entidades/relaciones            │
    │ validar pendientes │ Muestra relaciones C2-C4 pendientes de aprobación │
    │ conectar X con Y   │ Propone relación específica entre entidades       │
    │ grafo de [entidad] │ Visualiza vecindario 2-hop desde una entidad      │
    │ salir              │ Sale del modo cartógrafo                          │
    └────────────────────┴───────────────────────────────────────────────────┘


    RelationGuard (sistema de validación):
     - C1 (Descriptivo): Auto-aprobado si confianza > 0.95
     - C2 (Operacional): Requiere validación o fuente verificada
     - C3 (Integridad datos): Requiere aprobación explícita
     - C4 (Seguridad): Nunca auto-ejecuta, siempre requiere validación explícita

    El flujo es: propuesta → cola de validación → approve/reject → aplicación transaccional

    ---

    🗄️ 2. SQLite: Estructura y Almacenamiento

    El sistema RAG usa 3 bases de datos separadas:

    rag_core.sqlite (Metadatos + FTS)


    ┌────────────────────┬─────────────────────────┬─────────────────────────────────────────────────────────────────┐
    │ Tabla              │ Propósito               │ Columnas clave                                                  │
    ├────────────────────┼─────────────────────────┼─────────────────────────────────────────────────────────────────┤
    │ documents          │ Contenedores            │ doc_id, source_path, doc_type, title, summary, chunk_count      │
    │ chunks             │ Fragmentos de contenido │ doc_id, chunk_index, content, start_line, end_line, char_count  │
    │ entities           │ Entidades extraídas     │ name, entity_type, source_doc_id, source_chunk_id, confidence   │
    │ relation_proposals │ Relaciones pendientes   │ subject_entity, relation_verb, object_entity,criticality,status │
    │ chunks_fts         │ Virtual FTS5            │ content (indexado por BM25)                                     │
    └────────────────────┴─────────────────────────┴─────────────────────────────────────────────────────────────────┘


    rag_vectors.sqlite (Vectores)


    ┌────────────┬───────────────────┬────────────────────────────────────────────────┐
    │ Tabla      │ Tipo              │ Contenido                                      │
    ├────────────┼───────────────────┼────────────────────────────────────────────────┤
    │ embeddings │ vec0 (sqlite-vec) │chunk_id, embedding[1024], +doc_id, +entity_tags│
    └────────────┴───────────────────┴────────────────────────────────────────────────┘


    rag_graph.kuzu/ (Grafo)
    Ya descrito arriba.

    ---

    🔍 3. Filtrado ANTES de Búsqueda Vectorial

    El sistema aplica múltiples capas de filtro antes del search vectorial:

    T0: Cache (hash-based)
     - Lookup por hash de query, confianza 0.95, LRU 1000 entradas

    T1: SQL Pre-filtrado (antes de vectores)
     1. Extracción de entidades de la query (palabras capitalizadas, acrónimos)
     2. LIKE filtering en tabla chunks con keywords filtradas (stop-words eliminadas)
     3. FTS5 BM25 sobre chunks_fts con MATCH '"kw1" OR "kw2"'
     4. Entity table search con WHERE name LIKE '%entidad%'
     5. Metadata filtering sobre documents.title y documents.summary

    Umbral T1: confianza >= 0.90 → retorna resultados SQL sin ir a vectores

    Filtros por Dataset (Apollo)

    ┌─────────┬───────────────────────────────┐
    │ Dataset │ Patrón SQL                    │
    ├─────────┼───────────────────────────────┤
    │ docs    │ source LIKE '%/docs/%'        │
    │ skills  │ source LIKE '%/docs/skills/%' │
    │ codigo  │ source LIKE '%.py'            │
    │ config  │ source LIKE '%/config/%'      │
    └─────────┴───────────────────────────────┘


    FTS5 vs LIKE fallback
     - FTS5 usa BM25 (rank más bajo = mejor), score = 0.8 / (1 + |rank/10|) + 0.1
     - LIKE es fallback cuando FTS5 falla, con WHERE content LIKE '%kw%'

    ---

    🧱 4. Unidad Mínima de Información y Clasificación

    Jerarquía completa (de menor a mayor):


    ┌───────┬──────────┬───────────────────────────────────────────┬──────────────────────────────────────────┐
    │ Nivel │ Unidad   │ Descripción                               │ Ejemplo                                  │
    ├───────┼──────────┼───────────────────────────────────────────┼──────────────────────────────────────────┤
    │ 1     │ Token    │ Palabra individual                        │ def, calculate_total                     │
    │ 2     │ Chunk    │ ⭐ UNIDAD MÍNIMA - Fragmento de contenido │ Una función completa, un párrafo de docs │
    │ 3     │ Entity   │ Extracción nombrada de un chunk           │ class Foo, import bar                    │
    │ 4     │ Document │ Contenedor de chunks                      │ Un archivo .py o .md                     │
    │ 5     │ Dataset  │ Colección de documentos                   │ docs, skills, codigo                     │
    └───────┴──────────┴───────────────────────────────────────────┴──────────────────────────────────────────┘


    Cómo se crea un Chunk (la unidad mínima)

    Python (AST-based):
     - Usa ast module para respetar boundaries de funciones/clases
     - Cada función/método = 1 chunk con start_line, end_line

    Markdown (heading-based):
     - Cada sección entre headings = 1 chunk
     - Code blocks se respetan como boundaries

    Texto genérico (sliding window):
     - ~1000 caracteres por chunk, 200 chars de overlap

    Apollo (semantic chunking):
     - Split por oraciones, agrupadas hasta ~256 tokens, 25 tokens de overlap

    Cómo se clasifica a partir del chunk

     1 Chunk (texto)
     2   ├──→ Entity extraction → nodos Entity en Kuzu (type: function/class/concept)
     3   ├──→ Embedding → vector[1024] en sqlite-vec
     4   ├──→ FTS5 index → chunks_fts virtual table
     5   └──→ Graph linking → RELATES_TO entre entidades consecutivas del chunk

    Cada chunk tiene:
     - ID único (integer en RAG, {file_id}_{index} en Apollo)
     - Referencia al documento padre (doc_id)
     - Posición (chunk_index, start_line, end_line)
     - Contenido (content/text)
     - Embedding (1024 dims, mxbai-embed-large)
     - Entidades extraídas (functions, classes, headings, acronyms)
     - Relaciones de grafo (co-ocurrencia con entidades vecinas)

    ---

    📊 Diagrama del Pipeline Completo

      1 INGESTA:
      2   Archivo → Detectar tipo → Chunking inteligente → Chunks
      3                                       ↓
      4                         ┌─────────────┼─────────────┐
      5                         ↓             ↓             ↓
      6                   SQLite Core    sqlite-vec     Kuzu Graph
      7                 (docs, chunks,   (embeddings   (Entity nodes
      8                  entities, FTS5)   1024-dim)    + 3 edge types)
      9
     10
     11 CONSULTA:
     12   Query → T0 Cache → T1 SQL(FTS5/LIKE) → T2 Vector(sqlite-vec) → T3 Graph(Kuzu) → T4 LLM
     13           ↑              ↑                      ↑                     ↑
     14       hash(query)   entities+keywords      KNN search          Cypher traverse
     15       conf≥0.95     conf≥0.90              conf≥0.75           conf≥0.70

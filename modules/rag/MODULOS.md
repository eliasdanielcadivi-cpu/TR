# 🗂️ Índice de Módulos RAG

La estructura se divide en subcarpetas lógicas con archivos de máximo 3 funciones.

## 1. core/ (Orquestación)
- `tier_logic.py`: Definición de niveles T0-T4.
- `orchestrator.py`: Coordinación de flujo principal.
- `session_manager.py`: Contexto y estado de la consulta.

## 2. storage/ (Conexiones y Primitivas de DB)
- `sqlite_conn.py`: Gestión de conexión y salud de SQLite.
- `kuzu_conn.py`: Gestión de conexión y salud de Grafo.
- `ollama_client.py`: Interfaz mínima con el servidor de embeddings.

## 3. engines/ (Motores de Recuperación)
### sql/
- `fts5_manager.py`: Inicialización y mantenimiento del índice FTS5.
- `keyword_searcher.py`: Búsqueda determinista por términos.
- `sql_scorer.py`: Algoritmo de relevancia BM25/Personalizado.
### graph/
- `node_checker.py`: Validación de existencia de entidades.
- `hop_traverser.py`: Navegación de un solo salto (1-hop).
- `cypher_builder.py`: Generador de queries recursivas (N-hops).
### vector/
- `embedding_provider.py`: Generación de vectores (con fallback).
- `knn_searcher.py`: Búsqueda por similitud coseno/L2.

## 4. ingestion/ (Procesamiento de Datos)
- `file_reader.py`: Lectura y detección de tipos.
- `chunker.py`: División inteligente de texto.
- `entity_extractor.py`: Extracción granular de entidades.
- `graph_linker.py`: Creación de relaciones en Kùzu.

## 5. utils/ (Helpers)
- `text_cleaner.py`: Normalización de texto y acentos.
- `config_loader.py`: Carga segura de rag.yaml.

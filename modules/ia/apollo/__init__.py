"""Apollo: Sistema RAG + CRM para ARES.

Submódulos:
- apollo_db: Persistencia SQLite + sqlite-vec
- embeddings: Generación de embeddings vía Ollama
- ingest: Ingesta de documentos
- extraction: Extracción de entidades y relaciones
- retrieval: Recuperación híbrida (vectorial + grafo + relacional)
- compression: Compresión contextual
- generation: Generación de respuestas
- crm: Gestión de clientes e interacciones
"""

from .apollo_db import (
    init_db,
    get_connection,
    close_db,
    db_context,
    KNOWLEDGE_DB,
    USERS_DB,
    APOLLO_DIR,
)

from .embeddings import (
    embed_text,
    embed_documents,
    quantize_embeddings,
    dequantize_embeddings,
)

from .ingest import (
    semantic_chunk,
    ingest_file,
    ingest_directory,
)

from .extraction import (
    extract_entities_relations,
    store_entities,
    store_relations,
    ExtractionResult,
)

from .retrieval import (
    retrieve,
)

from .compression import (
    compress_context,
)

from .generation import (
    generate_answer,
    generate_citations,
    detect_hallucination,
)

__all__ = [
    # DB
    "init_db",
    "get_connection",
    "close_db",
    "db_context",
    "KNOWLEDGE_DB",
    "USERS_DB",
    "APOLLO_DIR",
    # Embeddings
    "embed_text",
    "embed_documents",
    "quantize_embeddings",
    "dequantize_embeddings",
    # Ingest
    "semantic_chunk",
    "ingest_file",
    "ingest_directory",
    # Extraction
    "extract_entities_relations",
    "store_entities",
    "store_relations",
    "ExtractionResult",
    # Retrieval
    "retrieve",
    # Compression
    "compress_context",
    # Generation
    "generate_answer",
    "generate_citations",
    "detect_hallucination",
]

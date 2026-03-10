"""Apollo Ingest: Ingesta de documentos con chunking semántico.

Módulo atómico que procesa archivos de texto, realiza chunking
semántico por oraciones, y almacena en SQLite con embeddings.

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .apollo_db import get_connection, db_context
from .embeddings import embed_text, embed_documents


# Configuración por defecto (desde config.yaml)
# Nota: mxbai-embed-large tiene límite de ~2048 tokens (~8000 chars)
DEFAULT_MAX_TOKENS = 256  # Más conservador para evitar exceder límite
DEFAULT_OVERLAP_TOKENS = 25


def semantic_chunk(
    text: str,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS
) -> List[str]:
    """Dividir texto en chunks semánticos por oraciones.

    Args:
        text: Texto completo a dividir.
        max_tokens: Máximo de tokens por chunk (default: 512).
        overlap_tokens: Tokens de solapamiento entre chunks (default: 50).

    Returns:
        Lista de chunks de texto (oraciones agrupadas).

    Nota: No corta párrafos ni oraciones. Usa aproximación 4 chars/token.
    """
    # Dividir por oraciones (respetando puntos decimales y abreviaturas)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        if not sentence.strip():
            continue

        # Aproximación: ~4 caracteres por token
        sentence_tokens = len(sentence) // 4

        # Si chunk actual + oración excede límite, guardar y comenzar nuevo
        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunks.append(' '.join(current_chunk))

            # Overlap: mantener últimas oraciones para contexto
            overlap = []
            overlap_tokens_count = 0
            for s in reversed(current_chunk):
                overlap_tokens_count += len(s) // 4
                if overlap_tokens_count > overlap_tokens:
                    break
                overlap.insert(0, s)

            current_chunk = overlap
            current_tokens = overlap_tokens_count
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    # Chunk final
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def ingest_file(
    file_path: str,
    user_id: str = "daniel",
    max_tokens: int = DEFAULT_MAX_TOKENS,
    quantize: Optional[int] = None
) -> Dict[str, Any]:
    """Ingestar archivo individual al sistema RAG.

    Args:
        file_path: Ruta del archivo a ingerir.
        user_id: Usuario propietario (default: daniel).
        max_tokens: Tamaño máximo de chunks.
        quantize: Bits para cuantización (4, 8, o None para sin cuantizar).

    Returns:
        Diccionario con metadata:
        - file_id: ID único del documento
        - chunks_count: Cantidad de chunks creados
        - tokens_total: Total de tokens aproximados
        - embeddings_dim: Dimensiones de embeddings (1024)
        - quantized: Si se aplicó cuantización

    Nota: Lee archivos .txt, .md, .py. Para otros formatos, intentar como texto.
    """
    path = Path(file_path)

    if not path.exists():
        return {"error": f"Archivo no encontrado: {file_path}"}

    # Leer contenido
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        return {"error": f"Archivo no es texto plano: {file_path}"}

    # Generar ID único (hash de ruta + contenido)
    file_id = hashlib.sha256(f"{path.absolute()}:{text[:1000]}".encode()).hexdigest()[:16]

    # Chunking semántico
    chunks = semantic_chunk(text, max_tokens)

    if not chunks:
        return {"error": "Archivo vacío o sin contenido procesable"}

    # Generar embeddings
    chunk_embeddings = embed_documents(chunks)

    # Conectar a DB
    with db_context("knowledge") as conn:
        cursor = conn.cursor()

        # Insertar documento
        cursor.execute("""
            INSERT OR REPLACE INTO documents (id, title, source, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            file_id,
            path.name,
            str(path.absolute()),
            f'{{"user_id": "{user_id}", "ingested_at": "{datetime.now().isoformat()}"}}'
        ))

        # Insertar chunks y embeddings
        for i, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
            chunk_id = f"{file_id}_{i}"

            # Insertar chunk
            cursor.execute("""
                INSERT OR REPLACE INTO chunks (id, document_id, chunk_index, text, tokens)
                VALUES (?, ?, ?, ?, ?)
            """, (
                chunk_id,
                file_id,
                i,
                chunk,
                len(chunk) // 4  # Aproximación tokens
            ))

            # Insertar embedding (sqlite-vec serializa automáticamente)
            cursor.execute("""
                INSERT OR REPLACE INTO embeddings (chunk_id, vector, document_id, chunk_index)
                VALUES (?, ?, ?, ?)
            """, (chunk_id, embedding.tobytes(), file_id, i))

        conn.commit()

    return {
        "file_id": file_id,
        "chunks_count": len(chunks),
        "tokens_total": sum(len(c) // 4 for c in chunks),
        "embeddings_dim": len(chunk_embeddings[0]),
        "quantized": quantize is not None,
        "file_path": str(path.absolute())
    }


def ingest_directory(
    dir_path: str,
    patterns: List[str] = None,
    user_id: str = "daniel",
    max_tokens: int = DEFAULT_MAX_TOKENS
) -> Dict[str, Any]:
    """Ingestar directorio completo de documentos.

    Args:
        dir_path: Ruta del directorio a ingerir.
        patterns: Patrones de archivos (default: ["*.md", "*.txt", "*.py"]).
        user_id: Usuario propietario.
        max_tokens: Tamaño máximo de chunks.

    Returns:
        Diccionario con resumen:
        - files_ingested: Cantidad de archivos procesados
        - total_chunks: Total de chunks creados
        - total_tokens: Total de tokens aproximados
        - errors: Lista de archivos con error

    Nota: Recorre recursivamente. Excluye directorios ocultos y __pycache__.
    """
    if patterns is None:
        patterns = ["*.md", "*.txt", "*.py"]

    dir_path = Path(dir_path)

    if not dir_path.exists():
        return {"error": f"Directorio no encontrado: {dir_path}"}

    results = {
        "files_ingested": 0,
        "total_chunks": 0,
        "total_tokens": 0,
        "errors": []
    }

    # Recorrer directorio recursivamente
    for pattern in patterns:
        for file_path in dir_path.rglob(pattern):
            # Excluir directorios ocultos y cache
            if any(part.startswith('.') or part == '__pycache__' for part in file_path.parts):
                continue

            # Ingestar archivo
            result = ingest_file(str(file_path), user_id, max_tokens)

            if "error" in result:
                results["errors"].append({
                    "file": str(file_path),
                    "error": result["error"]
                })
            else:
                results["files_ingested"] += 1
                results["total_chunks"] += result["chunks_count"]
                results["total_tokens"] += result["tokens_total"]

    return results

"""Apollo Compression: Compresión contextual de documentos.

Módulo atómico que reduce tokens enviados al LLM manteniendo
calidad semántica mediante selección extractiva.

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import re
from typing import List, Dict, Any
from .embeddings import embed_text
from .apollo_db import db_context

import numpy as np


def compress_context(
    documents: List[Dict[str, Any]],
    query: str,
    max_tokens: int = 2000
) -> str:
    """Comprimir contexto de documentos para LLM.

    Args:
        documents: Lista de chunks con texto y metadata.
        query: Pregunta original del usuario.
        max_tokens: Máximo de tokens en contexto comprimido.

    Returns:
        Contexto comprimido (oraciones clave seleccionadas).

    Nota: Proceso en 2 pasadas:
          1. Selección binaria (documento relevante/irrelevante)
          2. Extracción de oraciones clave por documento
    """
    if not documents:
        return ""

    # Paso 1: Seleccionar documentos relevantes
    selected = _select_relevant_docs(documents, query)

    if not selected:
        # Si ningún documento pasa el filtro, usar el top 1
        selected = documents[:1] if documents else []

    # Paso 2: Extraer oraciones clave de cada documento
    compressed_parts = []
    for doc in selected:
        key_sentences = _extract_key_sentences(doc, query, top_n=3)
        if key_sentences:
            compressed_parts.append(" ".join(key_sentences))

    # Unir contexto comprimido
    context = "\n\n".join(compressed_parts)

    # Truncar si excede límite (preservando oraciones)
    if _estimate_tokens(context) > max_tokens:
        context = _truncate_preserve_sentences(context, max_tokens)

    return context


def _select_relevant_docs(
    documents: List[Dict[str, Any]],
    query: str,
    threshold: float = 0.3
) -> List[Dict[str, Any]]:
    """Seleccionar documentos relevantes por similitud.

    Args:
        documents: Lista de chunks.
        query: Pregunta original.
        threshold: Umbral de similitud (default: 0.3).

    Returns:
        Lista de documentos que superan el umbral.
    """
    if not documents:
        return []

    # Generar embedding de query
    query_vec = embed_text(query)

    selected = []
    for doc in documents:
        # Calcular similitud coseno
        if "text" not in doc:
            continue

        doc_vec = embed_text(doc["text"][:500])  # Truncar para velocidad
        similarity = _cosine_similarity(query_vec, doc_vec)

        if similarity >= threshold:
            doc_copy = doc.copy()
            doc_copy["relevance_score"] = similarity
            selected.append(doc_copy)

    # Ordenar por relevancia
    selected.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    return selected


def _extract_key_sentences(
    doc: Dict[str, Any],
    query: str,
    top_n: int = 3
) -> List[str]:
    """Extraer oraciones clave de un documento.

    Args:
        doc: Chunk con texto y metadata.
        query: Pregunta original.
        top_n: Cantidad de oraciones a extraer.

    Returns:
        Lista de oraciones más relevantes.
    """
    text = doc.get("text", "")
    if not text:
        return []

    # Dividir en oraciones
    sentences = _split_sentences(text)

    if len(sentences) <= top_n:
        return sentences

    # Generar embedding de query
    query_vec = embed_text(query)

    # Puntuar cada oración por similitud
    scored_sentences = []
    for sent in sentences:
        if len(sent.split()) < 5:  # Ignorar oraciones muy cortas
            continue

        sent_vec = embed_text(sent)
        similarity = _cosine_similarity(query_vec, sent_vec)
        scored_sentences.append((sent, similarity))

    # Ordenar por similitud y tomar top_n
    scored_sentences.sort(key=lambda x: x[1], reverse=True)

    return [sent for sent, _ in scored_sentences[:top_n]]


def _split_sentences(text: str) -> List[str]:
    """Dividir texto en oraciones.

    Args:
        text: Texto completo.

    Returns:
        Lista de oraciones.
    """
    # Split por puntos, exclamaciones, interrogaciones
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcular similitud coseno entre dos vectores.

    Args:
        vec1: Primer vector.
        vec2: Segundo vector.

    Returns:
        Similitud coseno (0-1).
    """
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(vec1, vec2) / (norm1 * norm2))


def _estimate_tokens(text: str) -> int:
    """Estimar cantidad de tokens (aproximación).

    Args:
        text: Texto a estimar.

    Returns:
        Cantidad aproximada de tokens (~4 chars/token).
    """
    return len(text) // 4


def _truncate_preserve_sentences(text: str, max_tokens: int) -> str:
    """Truncar texto preservando oraciones completas.

    Args:
        text: Texto completo.
        max_tokens: Máximo de tokens.

    Returns:
        Texto truncado en límite de oración.
    """
    max_chars = max_tokens * 4

    if len(text) <= max_chars:
        return text

    # Cortar en el último punto antes del límite
    cutoff = text[:max_chars].rfind('.')

    if cutoff > 0:
        return text[:cutoff + 1]

    return text[:max_chars]

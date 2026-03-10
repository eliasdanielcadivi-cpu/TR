"""Apollo Retrieval: Recuperación híbrida de documentos.

Módulo atómico que orquesta búsqueda vectorial, en grafo,
y relacional con fusión RRF (Reciprocal Rank Fusion).

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

from .apollo_db import db_context
from .embeddings import embed_text


def retrieve(
    query: str,
    k: int = 5,
    mode: str = "fused",
    dataset: str = "default",
    filters: Optional[Dict] = None
) -> Dict[str, Any]:
    """Recuperar documentos relevantes para una query.

    Args:
        query: Pregunta o búsqueda del usuario.
        k: Cantidad de resultados (default: 5).
        mode: Tipo de búsqueda (vector, graph, relational, fused).
        dataset: Etiqueta de datos (default, docs, skills, codigo, config).
        filters: Filtros adicionales opcionales.

    Returns:
        Diccionario con resultados por modo y fused:
        - semantic: Lista de chunks por similitud vectorial
        - graph: Lista de entidades relacionadas
        - relational: Lista de chunks por FTS
        - fused: Resultados fusionados con RRF

    Nota: Si mode != "fused", solo retorna ese modo específico.
    """
    # Generar embedding de query
    query_vec = embed_text(query)

    results = {}

    with db_context("knowledge") as conn:
        # 1. Búsqueda vectorial
        semantic_results = _vector_search(conn, query_vec, k * 2, dataset, filters)
        results["semantic"] = semantic_results

        # 2. Búsqueda en grafo (entidades relacionadas)
        graph_results = _graph_search(conn, query, k * 2)
        results["graph"] = graph_results

        # 3. Búsqueda relacional (FTS en texto)
        relational_results = _relational_search(conn, query, k * 2, dataset, filters)
        results["relational"] = relational_results

        # 4. Fusión RRF (Reciprocal Rank Fusion)
        if mode == "fused":
            fused = _reciprocal_rank_fusion(
                {
                    "semantic": [r["chunk_id"] for r in semantic_results],
                    "graph": [r.get("chunk_id") for r in graph_results if r.get("chunk_id")],
                    "relational": [r["chunk_id"] for r in relational_results]
                },
                k=k
            )
            results["fused"] = fused
        else:
            results["fused"] = results.get(mode, semantic_results)

    return results


def _vector_search(
    conn: sqlite3.Connection,
    query_vec: Any,
    k: int,
    dataset: str = "default",
    filters: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    """Búsqueda vectorial con sqlite-vec.

    Args:
        conn: Conexión a knowledge.db.
        query_vec: Embedding de la query (numpy array).
        k: Cantidad de resultados.
        dataset: Etiqueta para filtrar por fuente.
        filters: Filtros adicionales.

    Returns:
        Lista de chunks con score de similitud.
    """
    # Construir WHERE clause para dataset
    where_clause = _build_dataset_filter(dataset, filters, "c")

    cursor = conn.execute(f"""
        SELECT e.chunk_id, e.document_id, e.chunk_index,
               vec_distance_cosine(e.vector, ?) as distance,
               c.text, c.tokens, d.title, d.source
        FROM embeddings e
        JOIN chunks c ON e.chunk_id = c.id
        JOIN documents d ON e.document_id = d.id
        {where_clause}
        ORDER BY distance ASC
        LIMIT ?
    """, (query_vec.tobytes(), k))

    results = []
    for row in cursor.fetchall():
        results.append({
            "chunk_id": row[0],
            "document_id": row[1],
            "chunk_index": row[2],
            "score": 1 - row[3],  # Convertir distancia a similitud
            "text": row[4],
            "tokens": row[5],
            "title": row[6],
            "source": row[7]
        })

    return results


def _graph_search(
    conn: sqlite3.Connection,
    query: str,
    k: int
) -> List[Dict[str, Any]]:
    """Búsqueda en grafo de entidades.

    Args:
        conn: Conexión a knowledge.db.
        query: Pregunta para extraer entidades clave.
        k: Cantidad de resultados.

    Returns:
        Lista de entidades relacionadas con paths.
    """
    # Extraer palabras clave de la query (simplificado)
    keywords = [w.lower() for w in query.split() if len(w) > 3]

    if not keywords:
        return []

    # Buscar entidades que mencionen keywords
    placeholders = ",".join("?" * len(keywords))
    cursor = conn.execute(f"""
        SELECT DISTINCT e.id, e.name, e.type, e.description,
               (SELECT COUNT(*) FROM relations r
                WHERE r.subject_id = e.id OR r.object_id = e.id) as rel_count
        FROM entities e
        WHERE LOWER(e.name) IN ({placeholders})
           OR LOWER(e.description) LIKE ?
        ORDER BY rel_count DESC
        LIMIT ?
    """, (*keywords, f"%{keywords[0]}%" if keywords else "%", k))

    results = []
    for row in cursor.fetchall():
        # Obtener relaciones de la entidad
        rels = conn.execute("""
            SELECT r.predicate, r.object_id, e2.name
            FROM relations r
            JOIN entities e2 ON r.object_id = e2.id
            WHERE r.subject_id = ?
            LIMIT 5
        """, (row[0],)).fetchall()

        results.append({
            "entity_id": row[0],
            "name": row[1],
            "type": row[2],
            "description": row[3],
            "relation_count": row[4],
            "relations": [{"predicate": r[0], "object": r[1], "object_name": r[2]} for r in rels]
        })

    return results


def _relational_search(
    conn: sqlite3.Connection,
    query: str,
    k: int,
    dataset: str = "default",
    filters: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    """Búsqueda relacional (LIKE en texto).

    Args:
        conn: Conexión a knowledge.db.
        query: Términos de búsqueda.
        k: Cantidad de resultados.
        dataset: Etiqueta para filtrar.
        filters: Filtros adicionales.

    Returns:
        Lista de chunks que contienen los términos.
    """
    # Dividir query en palabras clave
    keywords = query.split()

    if not keywords:
        return []

    # LIKE para cada keyword
    like_clauses = " OR ".join(["c.text LIKE ?" for _ in keywords])
    params = [f"%{kw}%" for kw in keywords]

    # Construir WHERE clause para dataset
    dataset_filter = _build_dataset_filter(dataset, filters, "c")

    # Combinar filtros
    if dataset_filter:
        # dataset_filter ya incluye "WHERE ..."
        where_clause = dataset_filter + " AND (" + like_clauses + ")"
    else:
        where_clause = "WHERE " + like_clauses

    cursor = conn.execute(f"""
        SELECT c.id, c.document_id, c.chunk_index, c.text, c.tokens,
               d.title, d.source
        FROM chunks c
        JOIN documents d ON c.document_id = d.id
        {where_clause}
        LIMIT ?
    """, (*params, k))

    results = []
    for row in cursor.fetchall():
        results.append({
            "chunk_id": row[0],
            "document_id": row[1],
            "chunk_index": row[2],
            "text": row[3],
            "tokens": row[4],
            "title": row[5],
            "source": row[6]
        })

    return results


def _reciprocal_rank_fusion(
    results_dict: Dict[str, List[str]],
    k: int = 60
) -> List[Dict[str, Any]]:
    """Fusionar rankings múltiples con RRF.

    Args:
        results_dict: Diccionario modo -> lista de chunk_ids.
        k: Constante RRF (default: 60).

    Returns:
        Lista de chunk_ids ordenados por score RRF.
    """
    fused_scores = defaultdict(float)

    for mode, doc_list in results_dict.items():
        if not doc_list:
            continue
        for rank, chunk_id in enumerate(doc_list, start=1):
            if chunk_id:
                fused_scores[chunk_id] += 1.0 / (k + rank)

    # Ordenar por score RRF
    sorted_docs = sorted(
        fused_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [{"chunk_id": chunk_id, "rrf_score": score} for chunk_id, score in sorted_docs]


def _build_dataset_filter(
    dataset: str,
    filters: Optional[Dict],
    alias: str = "c"
) -> str:
    """Construir cláusula WHERE para filtrar por dataset.

    Args:
        dataset: Etiqueta de dataset (default, docs, skills, etc.).
        filters: Filtros adicionales.
        alias: Alias de tabla para chunks.

    Returns:
        Cláusula WHERE o string vacío.
    """
    # Mapeo de datasets a patrones de fuente (usar % para ruta absoluta)
    dataset_patterns = {
        "default": None,
        "docs": "%/docs/%",
        "skills": "%/docs/skills/%",
        "codigo": "%.py",
        "config": "%/config/%"
    }

    pattern = dataset_patterns.get(dataset)

    if pattern:
        return f"WHERE d.source LIKE '{pattern}'"
    elif filters and "source_pattern" in filters:
        return f"WHERE d.source LIKE '{filters['source_pattern']}'"

    return ""

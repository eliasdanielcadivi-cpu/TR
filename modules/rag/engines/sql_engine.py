#!/usr/bin/env python3
"""
Motor de búsqueda SQL (T1).

Búsqueda determinista por palabras clave, metadatos y entidades.
Usa la base rag_core.sqlite para búsquedas exactas y semántica ligera.
"""

import sqlite3
import re
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SQLSearchResult:
    """Resultado de búsqueda SQL."""
    doc_id: str
    chunk_id: Optional[int]
    content: str
    relevance_score: float
    match_type: str  # 'exact', 'fuzzy', 'entity', 'metadata'
    source_path: Optional[str] = None
    entity_tags: List[str] = None


class SQLEngine:
    """
    Motor de búsqueda determinista T1.

    Características:
    - Búsqueda exacta por palabras clave
    - Búsqueda de entidades nombradas
    - Filtrado por metadatos (doc_type, title, etc.)
    - Ranking por TF-IDF simplificado
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = None

    @property
    def conn(self):
        """Conexión lazy a SQLite."""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def search(self, query: str, limit: int = 10,
               min_confidence: float = 0.5) -> List[SQLSearchResult]:
        """
        Búsqueda principal en documentos y chunks.

        Estrategia:
        1. Extraer entidades y keywords de la query
        2. Buscar en entities table
        3. Buscar en chunks content (exact + fuzzy)
        4. Buscar en documents metadata
        5. Combinar y rankear resultados
        """
        start_time = time.time()

        # Extraer componentes de la query
        keywords = self._extract_keywords(query)
        potential_entities = self._extract_potential_entities(query)

        results = []

        # 1. Búsqueda por entidades
        if potential_entities:
            entity_results = self._search_by_entities(potential_entities, limit)
            results.extend(entity_results)

        # 2. Búsqueda por keywords en chunks
        if keywords:
            keyword_results = self._search_by_keywords(keywords, limit)
            results.extend(keyword_results)

        # 3. Búsqueda en metadata de documentos
        metadata_results = self._search_metadata(keywords, limit)
        results.extend(metadata_results)

        # 4. Eliminar duplicados y rankear
        ranked_results = self._rank_results(results, query)

        # 5. Limitar y calcular scores finales
        final_results = ranked_results[:limit]

        # Ajustar scores basado en tiempo de respuesta
        elapsed = (time.time() - start_time) * 1000
        if elapsed < 10:  # Bonus por respuesta rápida
            for result in final_results:
                result.relevance_score *= 1.05

        return final_results

    def _extract_keywords(self, query: str) -> List[str]:
        """Extraer palabras clave significativas de la query."""
        # Palabras comunes a ignorar
        stop_words = {'el', 'la', 'los', 'las', 'de', 'en', 'y', 'o', 'a', 'que', 'se'}

        # Limpiar y tokenizar
        words = re.findall(r'\w+', query.lower())
        keywords = [w for w in words if len(w) > 2 and w not in stop_words]

        # Mantener orden pero eliminar duplicados
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)

        return unique_keywords

    def _extract_potential_entities(self, query: str) -> List[str]:
        """Extraer posibles nombres de entidades (capitalización, patrones)."""
        # Patrones simples para entidades
        patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Títulos con mayúsculas
            r'\b[A-Z]{2,}\b',  # Acrónimos
        ]

        entities = []
        for pattern in patterns:
            matches = re.findall(pattern, query)
            entities.extend(matches)

        return list(set(entities))

    def _search_by_entities(self, entities: List[str], limit: int) -> List[SQLSearchResult]:
        """Buscar documentos y chunks relacionados con entidades."""
        results = []

        for entity in entities:
            c = self.conn.cursor()

            # Buscar en tabla entities
            c.execute("""
                SELECT e.name, e.entity_type, e.source_doc_id, e.source_chunk_id,
                       d.title, d.source_path
                FROM entities e
                LEFT JOIN documents d ON e.source_doc_id = d.doc_id
                WHERE e.name LIKE ? OR e.name LIKE ?
                ORDER BY e.confidence DESC
                LIMIT ?
            """, (f'%{entity}%', f'{entity}%', limit))

            for row in c.fetchall():
                # Obtener chunk content si hay chunk_id
                content = ""
                chunk_id = None
                if row['source_chunk_id']:
                    c2 = self.conn.cursor()
                    c2.execute("SELECT content FROM chunks WHERE id = ?",
                              (row['source_chunk_id'],))
                    chunk_row = c2.fetchone()
                    if chunk_row:
                        content = chunk_row['content']
                        chunk_id = row['source_chunk_id']

                result = SQLSearchResult(
                    doc_id=row['source_doc_id'],
                    chunk_id=chunk_id,
                    content=content or f"Entidad: {row['name']} ({row['entity_type']})",
                    relevance_score=0.85,  # Score base para entidades
                    match_type='entity',
                    source_path=row['source_path'],
                    entity_tags=[row['name']]
                )
                results.append(result)

        return results

    def _search_by_keywords(self, keywords: List[str], limit: int) -> List[SQLSearchResult]:
        """Búsqueda de keywords en contenido de chunks."""
        if not keywords:
            return []

        results = []

        # Construir query dinámica para múltiples keywords
        placeholders = ', '.join(['?'] * len(keywords))
        keyword_patterns = [f'%{kw}%' for kw in keywords]

        c = self.conn.cursor()
        c.execute(f"""
            SELECT c.id, c.doc_id, c.content, c.chunk_index,
                   d.title, d.source_path
            FROM chunks c
            JOIN documents d ON c.doc_id = d.doc_id
            WHERE {' OR '.join(['c.content LIKE ?'] * len(keywords))}
            ORDER BY c.chunk_index
            LIMIT ?
        """, keyword_patterns + [limit * 3])  # Obtener más para ranking

        for row in c.fetchall():
            # Calcular score basado en matches de keywords
            content_lower = row['content'].lower()
            matches = sum(1 for kw in keywords if kw in content_lower)
            score = matches / len(keywords) * 0.8  # Max 0.8 para contenido

            result = SQLSearchResult(
                doc_id=row['doc_id'],
                chunk_id=row['id'],
                content=row['content'],
                relevance_score=score,
                match_type='exact' if matches == len(keywords) else 'fuzzy',
                source_path=row['source_path'],
                entity_tags=[]
            )
            results.append(result)

        return results

    def _search_metadata(self, keywords: List[str], limit: int) -> List[SQLSearchResult]:
        """Búsqueda en metadatos de documentos (título, tipo, etc.)."""
        if not keywords:
            return []

        results = []
        keyword_patterns = [f'%{kw}%' for kw in keywords]

        c = self.conn.cursor()
        c.execute(f"""
            SELECT doc_id, title, source_path, doc_type, summary
            FROM documents
            WHERE {' OR '.join(['title LIKE ?'] * len(keywords))}
               OR {' OR '.join(['summary LIKE ?'] * len(keywords))}
            LIMIT ?
        """, keyword_patterns * 2 + [limit])

        for row in c.fetchall():
            # Score basado en si match en título (mayor) o summary
            title_match = any(kw in (row['title'] or '').lower() for kw in keywords)
            summary_match = any(kw in (row['summary'] or '').lower() for kw in keywords)

            score = 0.7 if title_match else 0.5 if summary_match else 0.3

            result = SQLSearchResult(
                doc_id=row['doc_id'],
                chunk_id=None,
                content=f"Documento: {row['title'] or row['source_path']}\n"
                       f"Tipo: {row['doc_type']}\n"
                       f"Resumen: {row['summary'] or 'Sin resumen'}",
                relevance_score=score,
                match_type='metadata',
                source_path=row['source_path'],
                entity_tags=[]
            )
            results.append(result)

        return results

    def _rank_results(self, results: List[SQLSearchResult],
                     original_query: str) -> List[SQLSearchResult]:
        """Ranking combinado de resultados."""
        if not results:
            return []

        # Calcular scores finales con pesos
        for result in results:
            base_score = result.relevance_score

            # Bonificaciones
            bonuses = 0.0

            # Bonus por match exacto en título/entidad
            if result.match_type in ['exact', 'entity']:
                bonuses += 0.1

            # Bonus por contenido largo (más contexto)
            if result.content and len(result.content) > 100:
                bonuses += 0.05

            # Penalización por contenido muy corto
            if result.content and len(result.content) < 20:
                bonuses -= 0.1

            result.relevance_score = min(0.95, base_score + bonuses)

        # Ordenar por score descendente
        results.sort(key=lambda x: x.relevance_score, reverse=True)

        return results

    def get_document_info(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Obtener información completa de un documento."""
        c = self.conn.cursor()
        c.execute("""
            SELECT doc_id, source_path, doc_type, title, summary,
                   chunk_count, last_indexed, validation_status
            FROM documents
            WHERE doc_id = ?
        """, (doc_id,))

        row = c.fetchone()
        if not row:
            return None

        # Obtener chunks
        c.execute("""
            SELECT id, chunk_index, content, start_line, end_line
            FROM chunks
            WHERE doc_id = ?
            ORDER BY chunk_index
        """, (doc_id,))

        chunks = [dict(chunk) for chunk in c.fetchall()]

        return {
            'metadata': dict(row),
            'chunks': chunks,
            'chunk_count': len(chunks)
        }

    def close(self):
        """Cerrar conexión a la base de datos."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __del__(self):
        self.close()
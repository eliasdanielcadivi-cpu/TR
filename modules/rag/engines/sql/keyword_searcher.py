import re
from typing import List
from ...utils.text_cleaner import normalize_text, extract_keywords_clean

def run_fts5_query(conn, terms: List[str], limit: int = 10):
    """Ejecuta la búsqueda MATCH en FTS5 con términos normalizados."""
    if not terms: return []
    
    # Normalizar términos para la query
    normalized_terms = [normalize_text(t) for t in terms]
    formatted_query = " OR ".join([f'"{t}"' for t in normalized_terms])
    
    try:
        c = conn.cursor()
        c.execute("""
            SELECT c.id, c.doc_id, c.content, d.source_path, f.rank
            FROM chunks_fts f
            JOIN chunks c ON f.rowid = c.id
            JOIN documents d ON c.doc_id = d.doc_id
            WHERE chunks_fts MATCH ?
            ORDER BY rank ASC
            LIMIT ?
        """, (formatted_query, limit))
        return [dict(row) for row in c.fetchall()]
    except Exception:
        return []

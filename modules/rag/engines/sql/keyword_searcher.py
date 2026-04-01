import re
from typing import List

def extract_search_terms(query: str) -> List[str]:
    """
    Limpia y extrae términos significativos de la query.
    Atomicidad: Limpieza de caracteres, tokenización básica.
    """
    # Eliminar puntuación común
    clean = re.sub(r'[¿?¡!(),.;:]', ' ', query.lower())
    # Tokenizar y filtrar palabras cortas
    terms = [w for w in clean.split() if len(w) > 2]
    return list(set(terms))

def run_fts5_query(conn, terms: List[str], limit: int = 10):
    """Ejecuta la búsqueda MATCH en FTS5."""
    if not terms: return []
    
    formatted_query = " OR ".join([f'"{t}"' for w in terms for t in [w, w.replace('ó','o').replace('á','a').replace('é','e').replace('í','i').replace('ú','u')]])
    # Simplificado: si un término tiene acento, buscamos ambos.
    
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

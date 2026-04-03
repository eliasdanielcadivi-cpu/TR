
import sys
import os

# Añadir raíz del proyecto al path
project_root = "/home/daniel/tron/programas/TR"
sys.path.insert(0, project_root)

from modules.rag.storage.sqlite_conn import get_sqlite_conn
from modules.rag.engines.sql.fts5_setup import init_fts5_index, rebuild_fts5_index
from modules.rag.engines.sql.keyword_searcher import extract_search_terms, run_fts5_query
from modules.rag.engines.sql.sql_scorer import calculate_bm25_relevance

db_path = "/home/daniel/tron/programas/TR/db/rag/rag_core.sqlite"

def test_sql_atomic_flow():
    print("🧪 Probando Flujo Atómico SQL...")
    
    # 1. Conexión
    conn = get_sqlite_conn(db_path)
    if not conn:
        print("❌ Fallo en storage/sqlite_conn")
        return

    # 2. Setup
    if init_fts5_index(conn):
        print("✅ FTS5 Setup OK")
        rebuild_fts5_index(conn)
    
    # 3. Search
    query = "¿Qué secciones debe tener un skill?"
    terms = extract_search_terms(query)
    print(f"🔍 Términos extraídos: {terms}")
    
    results = run_fts5_query(conn, terms)
    print(f"📊 Resultados encontrados: {len(results)}")
    
    # 4. Scoring
    for res in results[:2]:
        score = calculate_bm25_relevance(res['rank'], len(terms), len(terms))
        print(f"🔸 Chunk ID {res['id']} - Score: {score:.4f}")
        print(f"   Fragmento: {res['content'][:100]}...")

    conn.close()

if __name__ == "__main__":
    test_sql_atomic_flow()

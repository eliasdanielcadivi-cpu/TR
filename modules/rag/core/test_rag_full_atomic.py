
import sys
import os

# Añadir raíz del proyecto al path
project_root = "/home/daniel/tron/programas/TR"
sys.path.insert(0, project_root)

from modules.rag.storage.sqlite_conn import get_sqlite_conn
from modules.rag.storage.kuzu_conn import get_kuzu_db, get_kuzu_conn
from modules.rag.core.tier_logic import run_t1_sql_pipeline, run_t3_graph_pipeline

db_sql_path = "/home/daniel/tron/programas/TR/db/rag/rag_core.sqlite"
db_graph_root = "/home/daniel/tron/programas/TR/db/rag/rag_graph.kuzu"

def test_full_rag_connectivity():
    query = "¿Cuál es el propósito del archivo SKILL.md?"
    print(f"🤔 PROBANDO PREGUNTA: '{query}'\n")
    
    # 1. Preparar Conexiones
    sql_conn = get_sqlite_conn(db_sql_path)
    kdb = get_kuzu_db(db_graph_root)
    k_conn = get_kuzu_conn(kdb)
    
    # 2. Ejecutar T1 SQL
    print("--- [T1 SQL RAW OUTPUT] ---")
    t1_res = run_t1_sql_pipeline(sql_conn, query)
    print(f"Confianza: {t1_res['confidence']:.4f}")
    print(f"Éxito (>=0.70): {t1_res['success']}")
    if t1_res['matches']:
        print(f"Top Match: {t1_res['matches'][0]['content'][:150]}...")
    
    # 3. Ejecutar T3 Grafo
    print("\n--- [T3 GRAFO RAW OUTPUT] ---")
    t3_res = run_t3_graph_pipeline(k_conn, query)
    print(f"Confianza: {t3_res['confidence']:.4f}")
    print(f"Éxito (>=0.70): {t3_res['success']}")
    if t3_res['summary']:
        print(f"Resumen: {t3_res['summary']}")

    sql_conn.close()

if __name__ == "__main__":
    test_full_rag_connectivity()

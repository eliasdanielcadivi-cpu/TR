
import sys
import os

# Añadir raíz del proyecto al path
project_root = "/home/daniel/tron/programas/TR"
sys.path.insert(0, project_root)

from modules.rag.storage.kuzu_conn import get_kuzu_db, get_kuzu_conn
from modules.rag.engines.graph.node_checker import find_entity_nodes
from modules.rag.engines.graph.hop_traverser import get_neighbors
from modules.rag.engines.graph.path_summarizer import summarize_graph_paths, calculate_graph_confidence

db_path = "/home/daniel/tron/programas/TR/db/rag/rag_graph.kuzu"

def test_graph_atomic_flow():
    print("🧪 Probando Flujo Atómico Grafo (Kùzu)...")
    
    # 1. Conexión
    db = get_kuzu_db(db_path)
    conn = get_kuzu_conn(db)
    if not conn:
        print("❌ Fallo en storage/kuzu_conn")
        return
    print("✅ Conexión Kùzu OK")

    # 2. Node Check
    term = "skill"
    print(f"🔍 Buscando nodos relacionados con: '{term}'")
    nodes = find_entity_nodes(conn, term, exact=False)
    print(f"📊 Nodos encontrados: {len(nodes)}")
    
    # 3. Hop Traversal
    neighbors = []
    if nodes:
        best_node = nodes[0]['name']
        print(f"🚀 Explorando vecinos de: '{best_node}'")
        neighbors = get_neighbors(conn, best_node)
        print(f"🔗 Vecinos encontrados: {len(neighbors)}")
    
    # 4. Summarize & Confidence
    if nodes:
        summary = summarize_graph_paths(nodes[0]['name'], neighbors)
        conf = calculate_graph_confidence(nodes, neighbors)
        print(f"\n📝 Resumen:\n{summary}")
        print(f"🔸 Confianza: {conf:.4f}")

if __name__ == "__main__":
    test_graph_atomic_flow()

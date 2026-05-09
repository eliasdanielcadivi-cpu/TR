import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
from modules.rag_mengraph.core.retriever import MengraphRetrieverV9

def test_v9_retrieval():
    db = MemgraphDriver()
    retriever = MengraphRetrieverV9(db)
    
    print("🚀 Iniciando Test NODO [D.2] - Recuperación V9")
    
    # 1. Búsqueda Determinista (Léxica)
    print("\n🔍 Probando búsqueda determinista (Léxica)...")
    res_det = retriever.query_deterministic("Gemini")
    
    if res_det and any(r['concept'] == 'GeminiProvider' for r in res_det):
        print(f"✅ PASSED: Concepto detectado via léxico: {res_det[0]}")
    else:
        print("❌ FAILED: No se encontró el concepto via léxico.")
        sys.exit(1)

    # 2. Búsqueda Híbrida (Semántica Fallback)
    print("\n🔍 Probando búsqueda híbrida...")
    res_hyb = retriever.query_hybrid("proveedor de google")
    
    if res_hyb:
        print(f"✅ PASSED: Resultados híbridos obtenidos: {len(res_hyb)}")
    else:
        print("⚠️ WARNING: Búsqueda híbrida no retornó resultados (esperado si no hay embeddings similares).")

    db.close()

if __name__ == "__main__":
    test_v9_retrieval()

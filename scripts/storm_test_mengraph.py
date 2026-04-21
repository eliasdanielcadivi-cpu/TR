import sys
import os
from pathlib import Path

# Fix de rutas para ARES
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from config import TRContext
from modules.rag_mengraph.core.orchestrator import MengraphRAGOrchestrator
from modules.rag_mengraph.core.retriever import MengraphRetriever
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver

def storm_test():
    print("\033[1;35m🚀 INICIANDO STORM TEST: SISTEMA RAG MENGRAPH\033[0m")
    
    # 1. Preparar Contexto
    obj = TRContext()
    orch = MengraphRAGOrchestrator(obj)
    
    # 2. Ingesta de Prueba (Manual de Gurú Táctico)
    test_text = "El Cierre de Doble Lazo es la herramienta definitiva del Agente Publicador para calificar a un Lead VIP."
    print("\n\033[1;34m📥 FASE 1: INGESTA TÁCTICA\033[0m")
    orch.ingest_text(test_text, source_doc="STORM_TEST_V1.txt")
    
    # 3. Verificación en Grafo
    print("\n\033[1;34m🕸️  FASE 2: VERIFICACIÓN FÍSICA EN GRAFO\033[0m")
    db = MemgraphDriver()
    nodes = db.execute_query("MATCH (n) WHERE n.trojan_id IS NOT NULL RETURN labels(n), n.text")
    for n in nodes:
        print(f"  [Node] {n['labels(n)'][0]}: {n['n.text']}")
    
    rels = db.execute_query("MATCH ()-[r]->() WHERE r.evidence_hash IS NOT NULL RETURN type(r), r.confianza")
    for r in rels:
        print(f"  [Rel] -[{r['type(r)']}]-> (Conf: {r['r.confianza']})")
    
    # 4. Recuperación Semántica
    print("\n\033[1;34m🔍 FASE 3: RECUPERACIÓN HÍBRIDA (GURÚ)\033[0m")
    retriever = MengraphRetriever(db, orch.ontology_path)
    query = "¿Cuál es la herramienta del Agente Publicador para calificar?"
    results = retriever.retrieve(query)
    
    for i, res in enumerate(results):
        print(f"  [{i+1}] {res['contexto']}")
    
    # 5. Cierre
    db.close()
    orch.close()
    print("\n\033[1;32m✅ STORM TEST COMPLETADO CON ÉXITO\033[0m")

if __name__ == "__main__":
    storm_test()

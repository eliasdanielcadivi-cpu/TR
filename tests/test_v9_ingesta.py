import sys
import os
from pathlib import Path

# Fix paths
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
from modules.rag_mengraph.storage.ingestor import MengraphIngestorV9

def test_v9_ingestion():
    db = MemgraphDriver()
    ingestor = MengraphIngestorV9(db)
    
    # Structure test
    test_taxonomy = {
        "domain": "PRODUCCION_IA",
        "categories": [
            {
                "name": "ORQUESTACION",
                "topics": [
                    {
                        "name": "PROVIDERS",
                        "concepts": [{"name": "GeminiProvider"}]
                    }
                ]
            }
        ]
    }
    
    print("🚀 Iniciando Test NODO [D.2] - Ingesta V9")
    
    # 1. Ingestar Taxonomía
    ingestor.ingest_taxonomy(test_taxonomy)
    
    # 2. Ingestar Chunk (Puntero Físico)
    test_chunk = {
        "file": "modules/ia/providers/gemini_provider.py",
        "start_line": 1,
        "end_line": 10,
        "text": "class GeminiProvider(BaseProvider): Integration for gemini-cli"
    }
    ingestor.ingest_chunk("GeminiProvider", test_chunk)
    
    # 3. Verificación Sonda (Cypher Real)
    print("\n🔍 Verificando rastro físico en Memgraph...")
    res = db.execute_query("""
        MATCH (d:Domain {name: 'PRODUCCION_IA'})-[:HAS_CATEGORY]->(c)-[:HAS_TOPIC]->(t)-[:HAS_CONCEPT]->(con)-[:REPRESENTED_BY]->(ch)
        RETURN d.name, c.name, t.name, con.name, ch.file, ch.lines
    """)
    
    if res:
        print("✅ TEST PASSED: Jerarquía V9 detectada en producción.")
        print(f"Resultado: {res[0]}")
    else:
        print("❌ TEST FAILED: No se encontró el rastro físico.")
        sys.exit(1)
        
    db.close()

if __name__ == "__main__":
    test_v9_ingestion()

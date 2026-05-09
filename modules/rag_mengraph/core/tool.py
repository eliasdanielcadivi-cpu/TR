"""
ARES RAG Tool Interface V9.
Punto de entrada universal para que IAs externas consulten el Grafo de Conocimiento.
Soporta el Switche Determinista-Inferencial (Híbrido).
"""
import json
from typing import List, Dict, Any
from modules.rag_mengraph.core.retriever import MengraphRetrieverV9
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver

class MengraphTool:
    """Herramienta de consulta al grafo V9 para agentes externos."""

    def __init__(self, ontology_path: str = ""):
        self.ontology_path = ontology_path

    def query_json(self, query_text: str, top_k: int = 5, mode: str = "hybrid") -> str:
        """
        Consulta el grafo V9 y devuelve una cadena JSON.
        """
        db = MemgraphDriver()
        try:
            retriever = MengraphRetrieverV9(db)
            if mode == "deterministic":
                results = retriever.query_deterministic(query_text, top_k=top_k)
            else:
                results = retriever.query_hybrid(query_text, top_k=top_k)
                
            return json.dumps({"status": "success", "mode": mode, "data": results}, indent=2)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        finally:
            db.close()

    def get_schema_summary(self) -> str:
        """Devuelve el esquema MAGE del grafo."""
        db = MemgraphDriver()
        try:
            res = db.execute_query("CALL llm_util.schema('prompt_ready') YIELD schema RETURN schema")
            schema_str = res[0]['schema'] if res else "No schema found"
            return json.dumps({"status": "success", "schema": schema_str})
        except:
            return json.dumps({"status": "error", "message": "MAGE llm_util module not found"})
        finally:
            db.close()

    def quick_stats(self) -> str:
        """Estadísticas rápidas de la taxonomía V9."""
        db = MemgraphDriver()
        try:
            domains = db.execute_query("MATCH (n:Domain) RETURN count(n) as c")[0]['c']
            concepts = db.execute_query("MATCH (n:Concept) RETURN count(n) as c")[0]['c']
            chunks = db.execute_query("MATCH (n:Chunk) RETURN count(n) as c")[0]['c']
            return json.dumps({
                "status": "success", 
                "nodes": {"domains": domains, "concepts": concepts, "chunks": chunks}
            })
        finally:
            db.close()

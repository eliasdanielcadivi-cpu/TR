"""
ARES RAG Tool Interface.
Punto de entrada universal para que IAs externas consulten el Grafo de Conocimiento.
Salida: JSON Puro.
"""
import json
from typing import List, Dict, Any
from modules.rag_mengraph.core.retriever import MengraphRetriever
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver

class MengraphTool:
    """Herramienta de consulta al grafo para agentes externos."""

    def __init__(self, ontology_path: str):
        self.ontology_path = ontology_path

    def query_json(self, query_text: str, top_k: int = 5) -> str:
        """
        Consulta el grafo y devuelve una cadena JSON con los resultados.
        Función diseñada para ser llamada por 'ares rag query'.
        """
        db = MemgraphDriver()
        try:
            retriever = MengraphRetriever(db, self.ontology_path)
            results = retriever.retrieve(query_text, top_k=top_k)
            # Limpiar para JSON
            clean_results = [
                {
                    "ancla": r['ancla'],
                    "trojan": r['trojan'],
                    "relacionado": r['relacionado'],
                    "trojan_rel": r['trojan_rel'],
                    "relevancia": r['similarity']
                } for r in results
            ]
            return json.dumps({"status": "success", "data": clean_results}, indent=2)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        finally:
            db.close()

    def get_schema_summary(self) -> str:
        """
        Devuelve el esquema actual del grafo en formato texto para que la IA sepa qué preguntar.
        """
        db = MemgraphDriver()
        try:
            # Usar la capacidad nativa de Memgraph MAGE si está disponible
            res = db.execute_query("CALL llm_util.schema('prompt_ready') YIELD schema RETURN schema")
            schema_str = res[0]['schema'] if res else "No schema found"
            return json.dumps({"status": "success", "schema": schema_str})
        except:
            return json.dumps({"status": "error", "message": "MAGE llm_util module not found"})
        finally:
            db.close()

    def quick_stats(self) -> str:
        """
        Muestra estadísticas rápidas de nodos y relaciones.
        """
        db = MemgraphDriver()
        try:
            nodes = db.execute_query("MATCH (n:ARES_ENTITY) RETURN count(n) as count")[0]['count']
            rels = db.execute_query("MATCH ()-[r:NEXT|PERMITTED_RELATION]->() RETURN count(r) as count")[0]['count']
            return json.dumps({"status": "success", "nodes": nodes, "relations": rels})
        finally:
            db.close()

import logging
from typing import List, Dict, Any
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
from modules.ia.embeddings_utils import embed_text

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Retriever")

class MengraphRetriever:
    def __init__(self, db_driver: MemgraphDriver, ontology_path: str):
        """
        Inicializa el recuperador híbrido.
        """
        self.db = db_driver
        with open(ontology_path, 'r', encoding='utf-8') as f:
            self.ontology = json.load(f)
        self.labels = list(self.ontology.get("sustantivos", {}).keys())

    def retrieve(self, query: str, top_k: int = 5, min_confidence: float = 0.5, min_verb_confidence: float = 0.8) -> List[Dict[str, Any]]:
        """
        Realiza búsqueda vectorial + traversal con poda determinista por Adverbios.
        """
        logger.info(f"Iniciando recuperación para: '{query}' (Threshold: {min_confidence})")
        
        try:
            query_embedding = embed_text(query).tolist()
        except Exception as e:
            logger.error(f"Error generando embedding de consulta: {e}")
            return []

        all_results = []

        for label in self.labels:
            index_name = f"index_{label.lower()}_vector"
            # Query: Vector Search + BFS para expansión de contexto (Estándar Memgraph)
            cypher = f"""
            CALL vector_search.search($index_name, $top_k, $embedding) YIELD node, similarity
            WITH node, similarity
            WHERE similarity >= $min_confidence
            MATCH path=(node)-[:NEXT|PERMITTED_RELATION *bfs 0..2]-(neighbor)
            WHERE neighbor:ARES_ENTITY
            RETURN 
                node.text as ancla, 
                node.trojan_id as trojan,
                neighbor.text as relacionado,
                neighbor.trojan_id as trojan_rel,
                similarity
            ORDER BY similarity DESC
            LIMIT 20
            """
            
            params = {
                "index_name": index_name,
                "top_k": top_k,
                "embedding": query_embedding,
                "min_confidence": min_confidence,
                "min_verb_conf": min_verb_confidence
            }
            
            try:
                res = self.db.execute_query(cypher, params)
                all_results.extend(res)
            except Exception as e:
                logger.warning(f"Error en búsqueda vectorial para {label}: {e}")

        return self._format_results(all_results)

    def _format_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Limpia y estructura los resultados del BFS para el LLM.
        """
        unique_results = []
        seen = set()
        
        for r in results:
            pair = (r['ancla'], r['relacionado'])
            if pair not in seen:
                seen.add(pair)
                unique_results.append({
                    "contexto": f"Entidad: {r['ancla']} [{r['trojan']}] -> Conectado a: {r['relacionado']} [{r['trojan_rel']}]",
                    "relevancia": round(r['similarity'], 4)
                })
                
        return unique_results

if __name__ == "__main__":
    # Prueba del Recuperador
    try:
        db = MemgraphDriver()
        ONTOLOGY = "/home/daniel/tron/programas/TR/config/rag_mengraph/ontology_master.json"
        retriever = MengraphRetriever(db, ONTOLOGY)
        
        test_query = "Cierre de Doble Lazo"
        print(f"--- Prueba de Recuperación Híbrida (Con Poda Determinista) ---")
        context = retriever.retrieve(test_query, min_confidence=0.3, min_verb_confidence=0.9)
        
        for i, c in enumerate(context):
            print(f"[{i+1}] [Sim: {c['relevancia']}] {c['contexto']}")
            print(f"    Evidencia: {c['evidencia']}")
            
        db.close()
    except Exception as e:
        print(f"❌ Error en prueba de Retriever: {e}")

"""MengraphRetriever V9: Búsqueda Híbrida y Switche Determinista.

Implementa la búsqueda léxica y semántica sobre la jerarquía V9.

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import logging
import json
from typing import List, Dict, Any, Optional
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
from modules.ia.embeddings_utils import embed_text

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-G-Retriever-V9")

class MengraphRetrieverV9:
    def __init__(self, db_driver: MemgraphDriver):
        """Inicializar el recuperador V9."""
        self.db = db_driver

    def query_deterministic(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Búsqueda léxica (Determinista) sobre Conceptos y Chunks.
        """
        logger.info(f"Ejecutando búsqueda determinista para: {query_text}")
        
        keywords = [k.lower() for k in query_text.split() if len(k) > 2]
        if not keywords:
            keywords = [query_text.lower()]

        cypher = """
        MATCH (con:Concept)-[:REPRESENTED_BY]->(ch:Chunk)
        WHERE any(k IN $keywords WHERE toLower(con.name) CONTAINS k)
           OR any(k IN $keywords WHERE k CONTAINS toLower(con.name))
        RETURN con.name as concept, ch.file as file, ch.lines as lines, id(ch) as chunk_id
        LIMIT $top_k
        """
        
        raw_results = self.db.execute_query(cypher, {"keywords": keywords, "top_k": top_k})
        return self._flatten_results(raw_results)

    def query_hybrid(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Búsqueda Híbrida (Semántica + Grafo).
        """
        logger.info(f"Ejecutando búsqueda híbrida para: {query_text}")
        
        try:
            query_vector = embed_text(query_text).tolist()
        except:
            query_vector = []

        if not query_vector:
            return self.query_deterministic(query_text, top_k)

        # Búsqueda Vectorial con umbral relajado (0.1) para depuración
        cypher = """
        MATCH (ch:Chunk)
        WITH ch, vector_search.cosine_similarity(ch.embedding, $vector) as score
        WHERE score > 0.1
        MATCH (con:Concept)-[:REPRESENTED_BY]->(ch)
        RETURN con.name as concept, ch.file as file, ch.lines as lines, score
        ORDER BY score DESC
        LIMIT $top_k
        """
        
        try:
            raw_results = self.db.execute_query(cypher, {"vector": query_vector, "top_k": top_k})
            res = self._flatten_results(raw_results)
            if not res:
                return self.query_deterministic(query_text, top_k)
            return res
        except Exception as e:
            logger.warning(f"Fallo búsqueda vectorial: {e}")
            return self.query_deterministic(query_text, top_k)

    def _flatten_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Asegura que los resultados sean diccionarios planos, manejando anidamiento del driver."""
        flattened = []
        for res in results:
            # Si el driver anida el resultado (ej: {'con.name': 'X'}), lo dejamos igual.
            # Pero si anida TODO el objeto (ej: {'c': {'name': 'X'}}), lo extraemos.
            if len(res) == 1 and isinstance(list(res.values())[0], dict):
                flattened.append(list(res.values())[0])
            else:
                flattened.append(res)
        return flattened

    def get_full_context(self, concept_name: str) -> str:
        """Recupera toda la sabiduría cristalizada de un concepto."""
        cypher = """
        MATCH (con:Concept {name: $name})-[:REPRESENTED_BY]->(ch:Chunk)
        RETURN ch.file, ch.lines
        """
        results = self.db.execute_query(cypher, {"name": concept_name})
        
        context_parts = []
        for res in results:
            context_parts.append(f"Referencia: {res['ch.file']} (Líneas {res['ch.lines']})")
            
        return "\n".join(context_parts)

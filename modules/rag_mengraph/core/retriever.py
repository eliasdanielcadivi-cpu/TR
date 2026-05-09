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
        
        Args:
            query_text: Término de búsqueda.
            top_k: Máximo de resultados.
        """
        logger.info(f"Ejecutando búsqueda determinista para: {query_text}")
        
        cypher = """
        MATCH (con:Concept)
        WHERE con.name CONTAINS $query OR con.description CONTAINS $query
        MATCH (con)-[:REPRESENTED_BY]->(ch:Chunk)
        RETURN con.name as concept, ch.file as file, ch.lines as lines, id(ch) as chunk_id
        LIMIT $top_k
        """
        
        return self.db.execute_query(cypher, {"query": query_text, "top_k": top_k})

    def query_hybrid(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Búsqueda Híbrida (Semántica + Grafo).
        
        Nota: Por ahora usa una aproximación de búsqueda por embedding si está disponible.
        """
        logger.info(f"Ejecutando búsqueda híbrida para: {query_text}")
        
        try:
            query_vector = embed_text(query_text).tolist()
        except:
            query_vector = []

        if not query_vector:
            return self.query_deterministic(query_text, top_k)

        # Búsqueda Vectorial HNSW (Si el índice existe, fallback a léxico si falla)
        cypher = """
        MATCH (ch:Chunk)
        WITH ch, community.vector.cosine_similarity(ch.embedding, $vector) as score
        WHERE score > 0.7
        MATCH (con:Concept)-[:REPRESENTED_BY]->(ch)
        RETURN con.name as concept, ch.file as file, ch.lines as lines, score
        ORDER BY score DESC
        LIMIT $top_k
        """
        
        try:
            return self.db.execute_query(cypher, {"vector": query_vector, "top_k": top_k})
        except Exception as e:
            logger.warn(f"Fallo búsqueda vectorial (posible falta de índice): {e}")
            return self.query_deterministic(query_text, top_k)

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

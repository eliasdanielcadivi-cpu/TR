"""MengraphIngestor V9: Ingesta Ontológica y Jerárquica.

Implementa el descenso granular: (:Domain) -> (:Category) -> (:Topic) -> (:Concept) -> (:Chunk)
con punteros físicos deterministas.

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import logging
import hashlib
from typing import List, Dict, Any, Optional
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
from modules.ia.embeddings_utils import embed_text

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-G-Ingestor-V9")

class MengraphIngestorV9:
    def __init__(self, db_driver: MemgraphDriver):
        """Inicializar el inyector V9."""
        self.db = db_driver

    def ingest_taxonomy(self, structure: Dict[str, Any]):
        """
        Inyecta la jerarquía taxonómica (Domain -> Category -> Topic -> Concept).
        
        Args:
            structure: Dict con la jerarquía completa.
        """
        logger.info("Ingestando jerarquía taxonómica V9...")
        
        domain_name = structure.get("domain")
        categories = structure.get("categories", [])

        # 1. Crear Dominio Raíz
        self.db.execute_query(
            "MERGE (d:Domain {name: $name}) ON CREATE SET d.created_at = timestamp()",
            {"name": domain_name}
        )

        for cat in categories:
            cat_name = cat.get("name")
            # 2. Vincular Categoría
            self.db.execute_query(
                """
                MATCH (d:Domain {name: $domain})
                MERGE (c:Category {name: $cat_name})
                MERGE (d)-[:HAS_CATEGORY]->(c)
                """,
                {"domain": domain_name, "cat_name": cat_name}
            )

            for topic in cat.get("topics", []):
                topic_name = topic.get("name")
                # 3. Vincular Topic
                self.db.execute_query(
                    """
                    MATCH (c:Category {name: $cat_name})
                    MERGE (t:Topic {name: $topic_name})
                    MERGE (c)-[:HAS_TOPIC]->(t)
                    """,
                    {"cat_name": cat_name, "topic_name": topic_name}
                )

                for concept in topic.get("concepts", []):
                    # 4. Vincular Concepto
                    self._ingest_concept(topic_name, concept)

    def ingest_chunk(self, concept_name: str, chunk_data: Dict[str, Any]):
        """
        Inyecta un puntero físico (:Chunk) vinculado a un Concepto.
        
        Args:
            concept_name: Nombre del concepto padre.
            chunk_data: Dict con 'file', 'start_line', 'end_line', 'text'.
        """
        text = chunk_data.get("text", "")
        evidence_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        
        try:
            embedding = embed_text(text).tolist()
        except Exception as e:
            logger.error(f"Error generando embedding para chunk: {e}")
            embedding = []

        query = """
        MATCH (con:Concept {name: $concept_name})
        MERGE (ch:Chunk {hash: $hash})
        ON CREATE SET 
            ch.file = $file,
            ch.lines = $lines,
            ch.embedding = $embedding,
            ch.created_at = timestamp()
        MERGE (con)-[:REPRESENTED_BY]->(ch)
        """
        
        params = {
            "concept_name": concept_name,
            "hash": evidence_hash,
            "file": chunk_data.get("file"),
            "lines": f"{chunk_data.get('start_line')}-{chunk_data.get('end_line')}",
            "embedding": embedding
        }
        
        self.db.execute_query(query, params)
        logger.info(f"Chunk inyectado para concepto: {concept_name}")

    def _ingest_concept(self, topic_name: str, concept_data: Dict[str, Any]):
        """Helper interno para inyectar conceptos."""
        concept_name = concept_data.get("name")
        self.db.execute_query(
            """
            MATCH (t:Topic {name: $topic_name})
            MERGE (con:Concept {name: $concept_name})
            ON CREATE SET con.created_at = timestamp()
            MERGE (t)-[:HAS_CONCEPT]->(con)
            """,
            {"topic_name": topic_name, "concept_name": concept_name}
        )

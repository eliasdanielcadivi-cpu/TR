import logging
import hashlib
import json
from typing import List, Dict, Any
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
from modules.ia.apollo.embeddings import embed_text

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Ingestor")

class MengraphIngestor:
    def __init__(self, db_driver: MemgraphDriver):
        """
        Inicializa el inyector de Memgraph.
        """
        self.db = db_driver

    def _generate_evidence_hash(self, content: str) -> str:
        """
        Genera un hash SHA-256 para trazabilidad de evidencia.
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def ingest_entities(self, entities: List[Dict[str, Any]], source_doc: str = "unknown"):
        """
        Inyecta entidades con encadenamiento secuencial (:NEXT) y modo analítico.
        """
        logger.info(f"Ingestando {len(entities)} entidades con encadenamiento :NEXT...")
        
        # 1. Activar modo analítico para velocidad (Estándar Memgraph)
        try:
            self.db.execute_query("STORAGE MODE IN_MEMORY_ANALYTICAL")
        except:
            pass

        last_node_id = None
        
        for ent in entities:
            label = ent['label']
            text = ent['text']
            trojan_id = ent['id']
            
            try:
                embedding = embed_text(text).tolist()
            except:
                embedding = []

            # MERGE con etiqueta raíz ARES_ENTITY (Corregido: SET dentro de bloques ON)
            query = f"""
            MERGE (n:{label} {{text: $text}})
            ON CREATE SET 
                n:ARES_ENTITY,
                n.trojan_id = $trojan_id,
                n.source_doc = $source_doc,
                n.embedding = $embedding,
                n.created_at = timestamp()
            ON MATCH SET
                n:ARES_ENTITY,
                n.embedding = $embedding,
                n.last_seen = timestamp()
            RETURN id(n) as node_id
            """
            
            res = self.db.execute_query(query, {
                "text": text, "trojan_id": trojan_id, 
                "source_doc": source_doc, "embedding": embedding
            })
            
            current_node_id = res[0]['node_id'] if res else None

            # 2. Crear relación secuencial :NEXT (Encadenamiento Lógico)
            if last_node_id is not None and current_node_id is not None:
                self.db.execute_query(
                    "MATCH (a), (b) WHERE id(a) = $id1 AND id(b) = $id2 MERGE (a)-[:NEXT]->(b)",
                    {"id1": last_node_id, "id2": current_node_id}
                )
            
            last_node_id = current_node_id

        # Retornar a modo transaccional
        try:
            self.db.execute_query("STORAGE MODE IN_MEMORY_TRANSACTIONAL")
        except:
            pass

    def ingest_relationships(self, relations: List[Dict[str, Any]], source_text: str = ""):
        """
        Inyecta relaciones (Verbos) entre entidades existentes.
        Incluye Adverbio de Evidencia (Hash).
        """
        logger.info(f"Ingestando {len(relations)} relaciones...")
        evidence_hash = self._generate_evidence_hash(source_text)
        
        for rel in relations:
            # Query Cypher: Vincular nodos existentes por texto
            query = f"""
            MATCH (a {{text: $origen}})
            MATCH (b {{text: $destino}})
            MERGE (a)-[r:{rel['verbo']}]->(b)
            ON CREATE SET
                r.confianza = $confianza,
                r.evidence_hash = $evidence_hash,
                r.razonamiento = $razonamiento,
                r.created_at = timestamp()
            """
            
            params = {
                "origen": rel['origen'],
                "destino": rel['destino'],
                "confianza": rel.get('confianza', 1.0),
                "evidence_hash": evidence_hash,
                "razonamiento": rel.get('razonamiento', "")
            }
            
            try:
                self.db.execute_query(query, params)
            except Exception as e:
                logger.error(f"Error inyectando relación '{rel['verbo']}': {e}")

if __name__ == "__main__":
    # Prueba del Ingestor
    try:
        db = MemgraphDriver()
        ingestor = MengraphIngestor(db)
        
        # Simulación de salida de spaCy + Serendipia
        test_entities = [
            {"text": "Cierre de Doble Lazo", "label": "PROMPT_TEMPLATE", "id": "ARES|HORMOZI"},
            {"text": "Agente Publicador", "label": "AI_SKILL", "id": "ARES|CORE"}
        ]
        
        test_relations = [
            {"origen": "Agente Publicador", "verbo": "USA_PROMPT", "destino": "Cierre de Doble Lazo", "confianza": 0.99}
        ]
        
        print("--- Prueba de MengraphIngestor ---")
        ingestor.ingest_entities(test_entities, source_doc="manual_hormozi.txt")
        ingestor.ingest_relationships(test_relations, source_text="El Agente usa el cierre...")
        
        db.close()
    except Exception as e:
        print(f"❌ Error en prueba de Ingestor: {e}")

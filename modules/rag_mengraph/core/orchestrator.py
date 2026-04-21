import logging
from typing import List, Dict, Any
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
from modules.rag_mengraph.ingestion.spacy_engine import SpacyEngine
from modules.rag_mengraph.core.serendipia_engine import SerendipiaEngine
from modules.rag_mengraph.validators.relation_guard import RelationGuard
from modules.rag_mengraph.validators.quarantine_manager import QuarantineManager
from modules.rag_mengraph.storage.ingestor import MengraphIngestor
from modules.ia.ai_engine import AIEngine

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Orchestrator")

class MengraphRAGOrchestrator:
    def __init__(self, obj):
        """
        Inicializa el orquestador completo con todas las piezas del sistema.
        """
        self.obj = obj
        self.db = MemgraphDriver()
        self.ontology_path = f"{obj.base_path}/config/rag_mengraph/ontology_master.json"
        
        # 1. Motores de Ingesta
        self.spacy = SpacyEngine(self.ontology_path)
        self.ai_engine = AIEngine(obj.config['ai'], str(obj.base_path))
        self.serendipia = SerendipiaEngine(self.ai_engine, None) # Se inicializa lazy en ingesta si falta weaver
        
        # 2. Motores de Validación y Almacén
        self.guard = RelationGuard(self.db)
        self.quarantine = QuarantineManager()
        self.ingestor = MengraphIngestor(self.db)

    def ingest_text(self, text: str, source_doc: str = "manual_ares.txt"):
        """
        Ejecuta el ciclo STORM de ingesta completa.
        """
        logger.info(f"--- Iniciando Ciclo STORM para: {source_doc} ---")
        
        # Fase 1: Extracción Determinista (Anclas spaCy)
        results = list(self.spacy.process_stream([text]))
        entities = results[0]['entities']
        
        if not entities:
            logger.warning("No se detectaron entidades conocidas. Abortando ingesta física.")
            return

        # Fase 2: Inyección de Sustantivos
        self.ingestor.ingest_entities(entities, source_doc=source_doc)

        # Fase 3: Inferencia de Verbos (Tejedor Lógico)
        # Re-inicializamos serendipia con el weaver real para Micro-RAG
        from modules.rag_mengraph.core.schema_weaver import SchemaWeaver
        weaver = SchemaWeaver(self.db)
        self.serendipia.weaver = weaver
        
        inferred_rels = self.serendipia.infer_relationships(text, entities)

        # Fase 4: RelationGuard (Seguridad C1-C4)
        validation = self.guard.validate_relationships(inferred_rels)
        
        approved = validation['APPROVED']
        to_quarantine = validation['QUARANTINE']

        # Fase 5: Inyección Directa (Aprobados)
        if approved:
            self.ingestor.ingest_relationships(approved, source_text=text)
            logger.info(f"Inyectadas {len(approved)} relaciones directamente.")

        # Fase 6: Enrutamiento a Cuarentena (Críticos/Serendipia)
        if to_quarantine:
            # Añadir metadatos de contexto antes de guardar
            for item in to_quarantine:
                item["source_doc"] = source_doc
                item["original_text"] = text
            self.quarantine.add_to_quarantine(to_quarantine)
            logger.info(f"Desviadas {len(to_quarantine)} relaciones a zona de Cuarentena.")

        logger.info("--- Ciclo STORM Finalizado ---")

    def close(self):
        self.db.close()

if __name__ == "__main__":
    # Prueba del Orquestador (Requiere contexto ARES)
    print("--- Orquestador STORM listo para integración ---")

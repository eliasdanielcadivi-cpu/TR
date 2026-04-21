import spacy
from spacy.pipeline import EntityRuler
import logging
from typing import Iterable, List, Dict
from modules.rag_mengraph.ingestion.pattern_compiler import compile_ontology_to_spacy

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-spaCy")

class SpacyEngine:
    def __init__(self, ontology_path: str, model: str = "es_core_news_sm"):
        """
        Inicializa el motor de spaCy con optimización Anti-Bloat.
        """
        logger.debug(f"Cargando modelo spaCy: {model}")
        try:
            # Desactivamos componentes pesados para velocidad y ahorro de RAM
            self.nlp = spacy.load(model, disable=["parser", "ner", "lemmatizer", "attribute_ruler"])
            
            # Agregamos EntityRuler
            self.ruler = self.nlp.add_pipe("entity_ruler")
            
            # Compilamos y cargamos patrones desde la ontología
            patterns = compile_ontology_to_spacy(ontology_path)
            self.ruler.add_patterns(patterns)
            logger.info(f"Pipeline spaCy listo con {len(patterns)} patrones deterministas.")
            
        except Exception as e:
            logger.error(f"Error al inicializar SpacyEngine: {e}")
            raise

    def process_stream(self, texts: Iterable[str], batch_size: int = 50) -> Iterable[Dict]:
        """
        Procesa un flujo de textos con limpieza agresiva de memoria.
        """
        import gc
        try:
            import torch
            has_torch = True
        except ImportError:
            has_torch = False

        for doc in self.nlp.pipe(texts, batch_size=batch_size):
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "id": ent.ent_id_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            yield {"text": doc.text, "entities": entities}
            
            # Limpieza proactiva (Estándar Industrial)
            del doc
            gc.collect()
            if has_torch and torch.cuda.is_available():
                torch.cuda.empty_cache()

if __name__ == "__main__":
    # Prueba del motor
    ONTOLOGY = "/home/daniel/tron/programas/TR/config/rag_mengraph/ontology_master.json"
    engine = SpacyEngine(ONTOLOGY)
    
    test_texts = [
        "El Agente Publicador usó el Cierre de Doble Lazo.",
        "Necesitamos calificar a este Lead VIP hoy mismo."
    ]
    
    print("--- Resultados de Ingesta Semántica ---")
    for res in engine.process_stream(test_texts):
        print(f"Doc: {res['text']}")
        for e in res['entities']:
            print(f"  -> [{e['label']}] {e['text']} (ID: {e['id']})")

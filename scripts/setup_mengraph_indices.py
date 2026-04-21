import logging
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver
import json

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Setup")

def setup_vector_indices(ontology_path: str):
    """
    Crea índices vectoriales para cada Label definido en la ontología.
    """
    db = MemgraphDriver()
    
    with open(ontology_path, 'r', encoding='utf-8') as f:
        ontology = json.load(f)
        
    sustantivos = ontology.get("sustantivos", {}).keys()
    
    logger.info(f"Configurando índices vectoriales para: {list(sustantivos)}")
    
    for label in sustantivos:
        # mxbai-embed-large tiene 1024 dimensiones
        db.init_vector_index(label, dimension=1024)
        
    db.close()
    logger.info("Configuración de índices completada.")

if __name__ == "__main__":
    ONTOLOGY = "/home/daniel/tron/programas/TR/config/rag_mengraph/ontology_master.json"
    setup_vector_indices(ONTOLOGY)

import logging
from typing import List, Dict
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Weaver")

class SchemaWeaver:
    def __init__(self, db_driver: MemgraphDriver):
        """
        Inicializa el tejedor de esquemas con acceso a la DB.
        """
        self.db = db_driver

    def get_allowed_schema(self, labels: List[str]) -> str:
        """
        Consulta Memgraph para obtener las relaciones permitidas y el esquema vivo.
        """
        # 1. Esquema Ontológico (JSON Master + Seeding)
        query_permitted = """
        MATCH (n1:OntologyNode)-[r:PERMITTED_RELATION]->(n2:OntologyNode)
        WHERE n1.label IN $labels AND n2.label IN $labels
        RETURN n1.label as origen, r.verb as verbo, n2.label as destino, r.criticidad as criticidad
        """
        
        # 2. Esquema Vivo (Realidad física de Memgraph)
        query_live = "SHOW SCHEMA INFO"
        
        try:
            permitted_results = self.db.execute_query(query_permitted, {"labels": labels})
            # El resultado de live requiere parsing especial de JSON en Memgraph
            # (Omitimos por ahora el parsing complejo para no romper la atomización, 
            #  pero usamos permitted_results como base de verdad).
            
            if not permitted_results:
                return "No hay relaciones predefinidas. Consulta libre al grafo permitida."
            
            schema_lines = ["--- ESQUEMA ONTOLÓGICO AUTORIZADO ---"]
            for res in permitted_results:
                schema_lines.append(
                    f"- ({res['origen']}) -[{res['verbo']}]-> ({res['destino']}) [Criticidad: {res['criticidad']}]"
                )
            schema_lines.append("--------------------------------------")
            
            return "\n".join(schema_lines)
            
        except Exception as e:
            logger.error(f"Error al obtener esquema: {e}")
            return "Error al recuperar el esquema."

if __name__ == "__main__":
    # Prueba del tejedor
    try:
        db = MemgraphDriver()
        weaver = SchemaWeaver(db)
        
        # Simulación de etiquetas detectadas por spaCy
        test_labels = ["AI_SKILL", "PROMPT_TEMPLATE", "LEAD_CRM"]
        
        print(f"--- Prueba de Micro-RAG de Esquema ---")
        schema_text = weaver.get_allowed_schema(test_labels)
        print(schema_text)
        
        db.close()
    except Exception as e:
        print(f"❌ Error en prueba de Weaver: {e}")

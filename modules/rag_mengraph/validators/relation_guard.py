import logging
from typing import List, Dict, Any
from modules.rag_mengraph.storage.memgraph_db import MemgraphDriver

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Guard")

class RelationGuard:
    def __init__(self, db_driver: MemgraphDriver):
        """
        Inicializa el RelationGuard con acceso a la DB ontológica.
        """
        self.db = db_driver

    def validate_relationships(self, relations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Clasifica las relaciones en 'APPROVED' (C1/C2) y 'QUARANTINE' (C3/C4 o Nuevas).
        """
        approved = []
        quarantine = []

        # Obtener mapa de criticidad actual desde la DB
        query = """
        MATCH (n1:OntologyNode)-[r:PERMITTED_RELATION]->(n2:OntologyNode)
        RETURN r.verb as verbo, r.criticidad as criticidad
        """
        results = self.db.execute_query(query)
        criticidad_map = {res['verbo']: res['criticidad'] for res in results}

        for rel in relations:
            verbo = rel.get("verbo")
            criticidad = criticidad_map.get(verbo)

            if not criticidad:
                # Serendipia: Verbo nuevo detectado
                logger.warning(f"Serendipia detectada: Verbo '{verbo}' no mapeado. Enviando a Cuarentena.")
                rel["criticidad"] = "NEW_VERB"
                rel["reason"] = "Verbo no mapeado en ontología (Serendipia)"
                quarantine.append(rel)
            elif criticidad in ["C3", "C4"]:
                # Crítico: Requiere aprobación humana
                logger.info(f"Relación crítica detectada: '{verbo}' ({criticidad}). Enviando a Cuarentena.")
                rel["criticidad"] = criticidad
                rel["reason"] = f"Nivel de criticidad elevado: {criticidad}"
                quarantine.append(rel)
            else:
                # Rutinario: Inyección directa
                rel["criticidad"] = criticidad
                approved.append(rel)

        return {
            "APPROVED": approved,
            "QUARANTINE": quarantine
        }

if __name__ == "__main__":
    # Prueba del Guard
    try:
        db = MemgraphDriver()
        guard = RelationGuard(db)
        
        test_rels = [
            {"origen": "Skill_1", "verbo": "USA_PROMPT", "destino": "Prompt_1"},
            {"origen": "Skill_1", "verbo": "PUBLICA_EN_REDES", "destino": "Doc_1"},
            {"origen": "Skill_1", "verbo": "INVENTA_ESTRATEGIA", "destino": "Guru_1"} # Nuevo
        ]
        
        print("--- Prueba de RelationGuard ---")
        results = guard.validate_relationships(test_rels)
        print(f"Aprobados: {len(results['APPROVED'])}")
        print(f"En Cuarentena: {len(results['QUARANTINE'])}")
        
        for q in results['QUARANTINE']:
            print(f"  [!] {q['verbo']} -> {q['reason']}")
            
        db.close()
    except Exception as e:
        print(f"❌ Error en prueba de RelationGuard: {e}")

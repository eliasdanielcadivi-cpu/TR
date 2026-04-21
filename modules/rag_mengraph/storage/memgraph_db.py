from neo4j import GraphDatabase
import logging
import os

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-DB")

class MemgraphDriver:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "", password: str = ""):
        """
        Inicializa el driver de Memgraph (Neo4j compatible).
        """
        logger.debug(f"Conectando a Memgraph en {uri}")
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            logger.info("Conexión con Memgraph establecida y verificada.")
        except Exception as e:
            logger.error(f"Error al conectar con Memgraph: {e}")
            raise

    def close(self):
        """
        Cierra la conexión con el driver.
        """
        if self.driver:
            self.driver.close()
            logger.debug("Conexión con Memgraph cerrada.")

    def execute_query(self, query: str, parameters: dict = None):
        """
        Ejecuta una consulta Cypher y retorna los resultados.
        """
        with self.driver.session() as session:
            try:
                result = session.run(query, parameters)
                return [record.data() for record in result]
            except Exception as e:
                logger.error(f"Error ejecutando consulta Cypher: {e}")
                raise

    def init_vector_index(self, label: str, dimension: int = 1024, metric: str = "cos"):
        """
        Crea un índice vectorial HNSW para una etiqueta específica si no existe.
        """
        index_name = f"index_{label.lower()}_vector"
        query = f"""
        CREATE VECTOR INDEX {index_name} ON :{label}(embedding)
        WITH CONFIG {{
            "dimension": {dimension},
            "metric": "{metric}",
            "capacity": 5000
        }};
        """
        logger.debug(f"Inicializando índice vectorial: {index_name} para {label}")
        try:
            # Primero verificamos si ya existe (podría fallar si ya existe)
            self.execute_query(query)
            logger.info(f"Índice vectorial {index_name} creado con éxito.")
        except Exception as e:
            if "already exists" in str(e).lower():
                logger.info(f"El índice vectorial {index_name} ya existe.")
            else:
                logger.warning(f"No se pudo crear el índice {index_name}: {e}")

    def init_ontology_db(self, ontology_path: str):
        """
        Siembra la estructura de la ontología en Memgraph como nodos de control.
        """
        import json
        with open(ontology_path, 'r', encoding='utf-8') as f:
            ontology = json.load(f)
            
        logger.info("Sembrando ontología en Memgraph...")
        
        # Limpiar ontología previa
        self.execute_query("MATCH (n:OntologyNode) DETACH DELETE n")
        
        # Crear nodos de Sustantivos
        for label, info in ontology.get("sustantivos", {}).items():
            self.execute_query(
                "CREATE (:OntologyNode {label: $label, desc: $desc})",
                {"label": label, "desc": info.get("desc", "")}
            )
            
        # Crear relaciones (Verbos permitidos)
        for verb, info in ontology.get("verbos_permitidos", {}).items():
            self.execute_query(
                """
                MATCH (a:OntologyNode {label: $origen})
                MATCH (b:OntologyNode {label: $destino})
                CREATE (a)-[:PERMITTED_RELATION {verb: $verb, criticidad: $criticidad}]->(b)
                """,
                {
                    "origen": info["origen"],
                    "destino": info["destino"],
                    "verb": verb,
                    "criticidad": info["criticidad"]
                }
            )
        logger.info("Ontología sembrada con éxito.")

if __name__ == "__main__":
    # Prueba rápida de conexión
    try:
        db = MemgraphDriver()
        ONTOLOGY = "/home/daniel/tron/programas/TR/config/rag_mengraph/ontology_master.json"
        db.init_ontology_db(ONTOLOGY)
        
        # Verificar siembra
        res = db.execute_query("MATCH (n1:OntologyNode)-[r:PERMITTED_RELATION]->(n2:OntologyNode) RETURN n1.label, r.verb, n2.label")
        print(f"--- Estructura Ontológica en DB ---")
        for row in res:
            print(f"  {row['n1.label']} -[{row['r.verb']}]-> {row['n2.label']}")
        
        db.close()
    except Exception as e:
        print(f"❌ Error en prueba de DB: {e}")

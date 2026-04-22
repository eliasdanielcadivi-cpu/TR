"""
Módulo Negociador - ARES-TRON.
Intercepción de disidencia y navegación de Rutas Nombradas (Crystallized Wisdom).
Regla: Máximo 3 funciones principales.
"""
from neo4j import GraphDatabase
import hjson
import os

class Negotiator:
    def __init__(self, uri="bolt://127.0.0.1:7687", user="", password=""):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def handle_rejection(self, user_input: str) -> dict:
        """
        Intercepta rechazos (R, No, Mal) y busca alternativas deterministas en el grafo.
        """
        rejection_signals = ["R", "no", "mal", "incorrecto", "rechazo", "dissent"]
        if user_input.strip().lower() in rejection_signals:
            return self.get_named_route("FALLBACK_ESTRATÉGICO")
        return None

    def get_named_route(self, route_name: str) -> dict:
        """
        Recupera una 'Ruta Nombrada' desde Memgraph.
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (r:RutaNombrada {nombre: $name}) RETURN r.prompt_sistema AS prompt, r.metadata AS meta",
                name=route_name
            )
            record = result.single()
            if record:
                return {"status": "success", "prompt": record["prompt"], "meta": record["meta"]}
            return {"status": "error", "message": f"Ruta '{route_name}' no encontrada."}

    def crystallize_wisdom(self, name: str, prompt: str, metadata: str):
        """
        Crea una nueva Ruta Nombrada (Crystallized Wisdom) en el grafo.
        """
        with self.driver.session() as session:
            session.run(
                "MERGE (r:RutaNombrada {nombre: $name}) "
                "SET r.prompt_sistema = $prompt, r.metadata = $metadata, r.timestamp = datetime()",
                name=name, prompt=prompt, metadata=metadata
            )
            return True

def get_system_load_route():
    """Retorna la ruta de carga inicial del sistema."""
    neg = Negotiator()
    route = neg.get_named_route("CARGA_SISTEMA")
    neg.close()
    return route

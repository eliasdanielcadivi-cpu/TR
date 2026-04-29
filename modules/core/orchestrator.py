"""
ARES Orchestrator - Órgano de Despacho Táctico.
Filosofía: Máximo 3 funciones.
"""
from modules.core.runtime import AresRuntime
import click

def run_lifecycle_phase(phase_id: str):
    """Orquesta la ejecución de una fase recuperando su lógica del grafo."""
    runtime = AresRuntime()
    
    # 1. Recuperar info del nodo (Forensia)
    query = f"MATCH (n {{id: '{phase_id}'}}) RETURN n.id AS id, n.nombre AS name, n.desc AS desc, n.objective AS objective"
    phase_info = runtime._run_cypher(query, None)
    
    if not phase_info:
        return None, f"❌ El nodo '{phase_id}' no existe en el grafo."

    # 2. Ensamblar Datos de Ejecución (DSL Dinámico)
    fase_data = _assemble_know_how_dsl(phase_id)
    
    # 3. Ejecutar
    resultados = runtime.execute_phase(fase_data)
    runtime.close()
    return resultados, phase_info[0]

def _assemble_know_how_dsl(phase_id: str):
    """Construye el DSL de ejecución basado en el Núcleo."""
    return {
        "id": phase_id,
        "steps": [
            {
                "id": "recolectar_principios",
                "type": "cypher",
                "query": f"MATCH (n {{id: '{phase_id}'}})-[:SE_RIGE_POR|REQUIERE]->(pr) RETURN pr.nombre AS principio"
            },
            {
                "id": "ejecucion_soberana",
                "type": "llm",
                "prompt": f"Actúa como el Arquitecto de ARES. Contexto: {phase_id}. Define pasos a seguir."
            }
        ]
    }

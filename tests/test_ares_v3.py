"""
Test Headless ARES v3.
Siembra + Ejecución de Fase basada en Grafo.
"""
from scripts.seed_ontology import seed
from modules.core.runtime import AresRuntime
import json

def test_discovery():
    # 1. Sembrar el subgrafo base
    seed()
    
    runtime = AresRuntime()
    
    # 2. Definición de la Fase (DSL inline para la prueba)
    fase_descubrimiento = {
        "id": "descubrimiento_principios",
        "objective": "Extraer los principios que rigen el modo INIT",
        "steps": [
            {
                "id": "query_grafo",
                "type": "cypher",
                "query": "MATCH (m:Modo {id: 'INIT'})-[:SE_RIGE_POR]->(p) RETURN p.nombre AS principio"
            },
            {
                "id": "analisis_llm",
                "type": "llm",
                "prompt": "Basado en estos principios extraídos del grafo, dime cómo debe comportarse ARES en modo INIT."
            }
        ]
    }
    
    # 3. Ejecución
    print("\n--- INICIANDO MOTOR ARES v3 ---")
    resultados = runtime.execute_phase(fase_descubrimiento)
    
    print("\n--- RESULTADOS DEL GRAFO ---")
    print(json.dumps(resultados["query_grafo"], indent=2))
    
    print("\n--- RESPUESTA INFERENCIAL (LLM) ---")
    print(resultados["analisis_llm"])
    
    runtime.close()

if __name__ == "__main__":
    test_discovery()

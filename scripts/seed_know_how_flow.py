"""
ARES-TRON: Siembra del Flujo Maestro de Creación de Software.
Sintaxis corregida para Memgraph.
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"

def seed_know_how():
    try:
        driver = GraphDatabase.driver(URI, auth=("", ""))
        with driver.session() as session:
            # 1. Crear Fases
            session.run("""
                MERGE (f:Flow {id: 'software_lifecycle', name: 'Ciclo de Vida de Software ARES'})
                MERGE (p1:Phase {id: 'INIT', name: 'Inicialización', objective: 'Estructuración y Contratos'})
                MERGE (p2:Phase {id: 'DEV', name: 'Desarrollo', objective: 'Fase Forense y Escritura Quirúrgica'})
                MERGE (p3:Phase {id: 'MAINT', name: 'Mantenimiento', objective: 'Adaptación y División'})
                MERGE (p4:Phase {id: 'PROD', name: 'Producción', objective: 'Auditoría y Despliegue'})
                
                MERGE (f)-[:HAS_PHASE {order: 1}]->(p1)
                MERGE (f)-[:HAS_PHASE {order: 2}]->(p2)
                MERGE (f)-[:HAS_PHASE {order: 3}]->(p3)
                MERGE (f)-[:HAS_PHASE {order: 4}]->(p4)
            """)
            
            # 2. Conectar Principios (En transacciones separadas para evitar errores de orden)
            session.run("""
                MATCH (p_forense:Principio {id: 'principio_02'})
                MATCH (phase_dev:Phase {id: 'DEV'})
                MERGE (phase_dev)-[:REQUIERE]->(p_forense)
            """)
            
            session.run("""
                MATCH (p_atomic:Principio {id: 'principio_01'})
                MATCH (phase_maint:Phase {id: 'MAINT'})
                MERGE (phase_maint)-[:SE_RIGE_POR]->(p_atomic)
            """)
            
            print("✅ Flujo 'Know-How' sembrado correctamente.")
        driver.close()
    except Exception as e:
        print(f"❌ Error sembrando flujo: {e}")

if __name__ == "__main__":
    seed_know_how()

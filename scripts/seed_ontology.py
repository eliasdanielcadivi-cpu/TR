"""
ARES-TRON: Siembra Ontológica Inicial.
Propósito: Crear el Subgrafo Raíz con sintaxis Cypher correcta.
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"

def seed():
    try:
        driver = GraphDatabase.driver(URI, auth=("", ""))
        with driver.session() as session:
            # 1. Limpieza Táctica
            session.run("MATCH (n) DETACH DELETE n")

            # 2. Creación del Subgrafo Raíz (Sintaxis Corregida //)
            session.run("""
                CREATE (a:Identidad {id: 'ares', nombre: 'ARES-TRON', alma: 'Soberanía'})
                CREATE (m1:Modo {id: 'INIT', desc: 'Fase Crítica de Estructura'})
                CREATE (m2:Modo {id: 'DEV', desc: 'Fase de Construcción Activa'})
                CREATE (p1:Principio {nombre: 'Atomicidad Paranoica', id: 'principio_01'})
                CREATE (p2:Principio {nombre: 'Fase Forense Obligatoria', id: 'principio_02'})
                
                // Relaciones de Poder
                CREATE (a)-[:OPERA_EN]->(m1)
                CREATE (a)-[:OPERA_EN]->(m2)
                CREATE (m1)-[:SE_RIGE_POR]->(p1)
                CREATE (m1)-[:SE_RIGE_POR]->(p2)
                CREATE (m2)-[:SE_RIGE_POR]->(p1)
                
                // Conexión a Documentos (Conocimiento)
                CREATE (d1:Documento {id: 'doc_nucleo', ruta: 'docs/ArquitecturadeModulosOrientadaaIA/NUCLEO DE CREACION DE SOFTWARE KNOW-HOW ARES-TRON.md'})
                CREATE (p1)-[:INSTRUYE_A]->(d1)
            """)
            
            # Verificación Forense 1: Conteo de Nodos
            count = session.run("MATCH (n) RETURN count(n) AS total").single()["total"]
            print(f"📊 Verificación 1 (Conteo): {count} nodos creados.")
            
            # Verificación Forense 2: Existencia de la Identidad
            identity = session.run("MATCH (a:Identidad) RETURN a.nombre AS nombre").single()["nombre"]
            print(f"🛰️  Verificación 2 (Identidad): {identity} está vivo en el grafo.")

        driver.close()
        return True
    except Exception as e:
        print(f"❌ Error crítico en la siembra: {e}")
        return False

if __name__ == "__main__":
    seed()

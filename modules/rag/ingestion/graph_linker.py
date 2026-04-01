import logging
from ..storage.kuzu_conn import get_kuzu_conn

logger = logging.getLogger(__name__)

def link_entities_in_graph(db, entities: list, source_doc: str):
    """
    Crea nodos y relaciones básicas (co-ocurrencia) en Kùzu.
    Atomicidad: No hace chunking ni lectura, solo Graph DB.
    """
    conn = get_kuzu_conn(db)
    if not conn: return False
    
    # 1. Crear Nodos
    for ent in entities:
        try:
            name = ent['name'].replace("'", "\\'")
            etype = ent.get('type', 'concept')
            query = f"MERGE (e:Entity {{name: '{name}'}}) SET e.type = '{etype}', e.source_doc = '{source_doc}'"
            conn.execute(query)
        except Exception as e:
            logger.debug(f"Fallo MERGE nodo: {e}")

    # 2. Crear Relaciones (Secuenciales en el documento)
    if len(entities) > 1:
        for i in range(len(entities) - 1):
            try:
                name1 = entities[i]['name'].replace("'", "\\'")
                name2 = entities[i+1]['name'].replace("'", "\\'")
                query = f"""
                    MATCH (a:Entity {{name: '{name1}'}}), (b:Entity {{name: '{name2}'}})
                    CREATE (a)-[:RELATES_TO {{relation_type: 'co_occur', confidence: 0.7}}]->(b)
                """
                conn.execute(query)
            except Exception as e:
                logger.debug(f"Fallo CREATE relación: {e}")
    
    return True

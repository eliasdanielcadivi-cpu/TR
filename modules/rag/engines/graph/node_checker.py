import logging

logger = logging.getLogger(__name__)

def find_entity_nodes(conn, name: str, exact: bool = False):
    """
    Busca nodos por nombre usando coincidencia parcial o exacta.
    """
    try:
        if exact:
            query = "MATCH (e:Entity) WHERE e.name = $name RETURN e.name, e.type, e.source_doc"
            params = {"name": name}
        else:
            # Kuzu usa CONTAINS para búsqueda parcial
            query = "MATCH (e:Entity) WHERE e.name CONTAINS $name_part RETURN e.name, e.type, e.source_doc"
            params = {"name_part": name}
            
        result = conn.execute(query, params)
        nodes = []
        while result.has_next():
            row = result.get_next()
            nodes.append({
                'name': row[0],
                'type': row[1],
                'source_doc': row[2]
            })
        return nodes
    except Exception as e:
        logger.error(f"Error en find_entity_nodes: {e}")
        return []

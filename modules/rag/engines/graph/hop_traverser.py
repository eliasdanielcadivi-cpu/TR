import logging

logger = logging.getLogger(__name__)

def get_neighbors(conn, start_node_name: str, limit: int = 10):
    """
    Obtiene los vecinos directos (1-hop) de una entidad.
    """
    try:
        # En Kùzu, es más seguro no usar TYPE() en la query si no se está seguro de la versión.
        # El label de la relación se puede obtener consultando por tablas o usando label() si está disponible.
        query = """
            MATCH (a:Entity)-[r]->(b:Entity)
            WHERE a.name = $name
            RETURN b.name, b.type
            LIMIT $limit
        """
        result = conn.execute(query, {"name": start_node_name, "limit": limit})
        neighbors = []
        while result.has_next():
            row = result.get_next()
            neighbors.append({
                'name': row[0],
                'type': row[1],
                'relation': 'RELATES_TO' # Fallback simplificado para T3 inicial
            })
        return neighbors
    except Exception as e:
        logger.error(f"Error en get_neighbors: {e}")
        return []

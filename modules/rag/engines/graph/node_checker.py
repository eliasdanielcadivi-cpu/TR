import logging
from ...utils.text_cleaner import normalize_text

logger = logging.getLogger(__name__)

def find_entity_nodes(conn, name: str, exact: bool = False):
    """
    Busca nodos por nombre usando coincidencia parcial o exacta.
    Normaliza la entrada para evitar fallos por acentos.
    """
    try:
        clean_name = normalize_text(name)
        if exact:
            query = "MATCH (e:Entity) WHERE e.name = $name RETURN e.name, e.type, e.source_doc"
            params = {"name": clean_name}
        else:
            query = "MATCH (e:Entity) WHERE e.name CONTAINS $name_part RETURN e.name, e.type, e.source_doc"
            params = {"name_part": clean_name}
...
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

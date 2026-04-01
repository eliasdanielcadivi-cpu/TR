def summarize_graph_paths(start_node: str, connections: list) -> str:
    """
    Convierte una lista de conexiones en un resumen de texto natural.
    """
    if not connections:
        return f"No se encontraron relaciones directas para '{start_node}'."
    
    summary = f"La entidad '{start_node}' está relacionada con:\n"
    for conn in connections:
        summary += f"  - {conn['name']} (Tipo: {conn['type']}, Relación: {conn['relation']})\n"
    
    return summary

def calculate_graph_confidence(nodes_found: list, neighbors_found: list) -> float:
    """Calcula confianza basada en la densidad de información encontrada."""
    score = 0.0
    if nodes_found: score += 0.4
    if neighbors_found: score += 0.5
    return min(0.99, score)

"""
Strategy Selector - ARES-TRON.
Decide la mezcla óptima de recuperación (Grafo, Vectorial, Keyword).
Filosofía: Sistema Híbrido Workflow + Búsqueda Inteligente.
"""

def select_search_strategy(query: str, phase: str) -> dict:
    """
    Analiza la consulta y la fase para seleccionar los motores de recuperación.
    """
    # Palabras clave para búsqueda por ruta/workflow
    workflow_keywords = ["inicializa", "crea", "despliega", "instala", "limpia"]
    
    # Decisión basada en la fase
    if phase == "INIT":
        return {
            "engines": ["GRAFO_RUTA", "KEYWORD"],
            "depth": 1,
            "reason": "Fase crítica de estructura, se requiere precisión determinista."
        }
    
    # Decisión basada en la consulta
    is_workflow = any(word in query.lower() for word in workflow_keywords)
    
    if is_workflow:
        return {
            "engines": ["GRAFO_RUTA", "SEMANTIC"],
            "depth": 2,
            "reason": "Acción de flujo detectada, combinando ruta con contexto semántico."
        }
    
    # Búsqueda híbrida por defecto para Desarrollo
    return {
        "engines": ["VECTORIAL", "GRAFO_RELACIONAL", "SEMANTIC"],
        "depth": 1,
        "reason": "Modo exploración/desarrollo activo."
    }

def get_inference_parameters(strategy: dict) -> dict:
    """
    Ajusta temperatura y límites del LLM según la estrategia.
    """
    if "GRAFO_RUTA" in strategy["engines"]:
        return {"temperature": 0.1, "max_tokens": 1000} # Determinista
    return {"temperature": 0.7, "max_tokens": 2000} # Creativo/Informativo

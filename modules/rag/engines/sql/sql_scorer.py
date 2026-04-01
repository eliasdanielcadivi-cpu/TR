import math

def calculate_bm25_relevance(raw_rank: float, matches: int, total_terms: int) -> float:
    """
    Normaliza el rank de FTS5 a un score de 0.0 a 1.0.
    Heurística BM25 + Bonus por match exacto.
    """
    # FTS5 rank suele ir de -10 a 0.
    # Score base: 0.1 a 0.8
    score = 0.8 / (1.0 + abs(raw_rank/10.0)) + 0.1
    
    # Bonus por cobertura de términos
    coverage = matches / total_terms if total_terms > 0 else 0
    score += coverage * 0.1
    
    return min(0.99, score)

def get_best_confidence(results: list) -> float:
    """Extrae el score máximo de una lista de resultados."""
    if not results: return 0.0
    return max([r.get('relevance_score', 0.0) for r in results])

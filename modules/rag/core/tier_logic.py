import logging
from ..engines.sql.keyword_searcher import run_fts5_query
from ..engines.sql.sql_scorer import calculate_bm25_relevance, get_best_confidence
from ..engines.graph.node_checker import find_entity_nodes
from ..engines.graph.hop_traverser import get_neighbors
from ..engines.graph.path_summarizer import summarize_graph_paths, calculate_graph_confidence
from ..utils.text_cleaner import extract_keywords_clean

logger = logging.getLogger(__name__)

def run_t1_sql_pipeline(sqlite_conn, query: str, threshold: float = 0.70):
    """
    Ejecuta la capa T1 SQL de manera aislada.
    """
    terms = extract_keywords_clean(query)
    raw_results = run_fts5_query(sqlite_conn, terms)
    
    scored_results = []
    for res in raw_results:
        res['relevance_score'] = calculate_bm25_relevance(res['rank'], len(terms), len(terms))
        scored_results.append(res)
        
    confidence = get_best_confidence(scored_results)
    success = confidence >= threshold
    
    return {
        'tier': 'T1_SQL',
        'success': success,
        'confidence': confidence,
        'matches': scored_results[:5]
    }

def run_t3_graph_pipeline(kuzu_conn, query: str, threshold: float = 0.70):
    """
    Ejecuta la capa T3 Grafo de manera aislada.
    """
    # Extraer términos para buscar nodos
    terms = extract_keywords_clean(query)
    all_found_nodes = []
    all_neighbors = []
    
    for term in terms:
        nodes = find_entity_nodes(kuzu_conn, term)
        all_found_nodes.extend(nodes)
        if nodes:
            # Explorar vecinos del primer nodo encontrado por término
            neighbors = get_neighbors(kuzu_conn, nodes[0]['name'])
            all_neighbors.extend(neighbors)
            
    confidence = calculate_graph_confidence(all_found_nodes, all_neighbors)
    success = confidence >= threshold
    
    summary = ""
    if all_found_nodes:
        summary = summarize_graph_paths(all_found_nodes[0]['name'], all_neighbors)
        
    return {
        'tier': 'T3_GRAPH',
        'success': success,
        'confidence': confidence,
        'summary': summary,
        'nodes': all_found_nodes[:5]
    }

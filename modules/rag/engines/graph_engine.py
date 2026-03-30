#!/usr/bin/env python3
"""
Motor de traversia de grafo (T3).

Navegación por grafo de conocimiento usando Kùzu.
Extrae entidades de la query y realiza traversia para encontrar relaciones relevantes.
"""

import re
import time
import logging
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TraversalDirection(Enum):
    """Dirección de traversia en el grafo."""
    FORWARD = "forward"      # Desde entidad origen
    BACKWARD = "backward"    # Hacia entidad origen
    BIDIRECTIONAL = "bidirectional"  # Ambas direcciones


@dataclass
class GraphNode:
    """Nodo en el grafo de conocimiento."""
    name: str
    type: str
    validated: bool
    source_doc: Optional[str] = None
    properties: Dict[str, Any] = None


@dataclass
class GraphRelationship:
    """Relación entre nodos en el grafo."""
    from_node: str
    to_node: str
    relation_type: str
    weight: float
    criticality: str
    validated: bool
    context: Optional[str] = None


@dataclass
class GraphTraversalResult:
    """Resultado de traversia de grafo."""
    path_nodes: List[GraphNode]
    path_relationships: List[GraphRelationship]
    relevance_score: float
    traversal_depth: int
    query_coverage: float  # % de entidades de la query cubiertas


class GraphEngine:
    """
    Motor de traversia de grafo T3.

    Características:
    - Extracción de entidades de queries naturales
    - Traversia de grafo con múltiples estrategias
    - Filtrado por criticidad y validación
    - Búsqueda de caminos relevantes
    """

    def __init__(self, db_path: str, max_hops: int = 3):
        self.db_path = db_path
        self.max_hops = max_hops
        self._db = None
        self._conn = None

    @property
    def conn(self):
        """Conexión lazy a Kùzu."""
        if self._conn is None:
            try:
                import kuzu
                # Kùzu usa directorio, no archivo
                if not self.db_path.endswith('.kuzu'):
                    self.db_path = self.db_path + '.kuzu'

                self._db = kuzu.Database(self.db_path)
                self._conn = kuzu.Connection(self._db)
                logger.info(f"✅ Conexión Kùzu establecida a {self.db_path}")
            except ImportError as e:
                logger.error(f"❌ kuzu no está instalado: {e}")
                raise
            except Exception as e:
                logger.error(f"❌ Error conectando a Kùzu: {e}")
                raise
        return self._conn

    def traverse(self, query: str, max_hops: Optional[int] = None,
                min_relevance: float = 0.5) -> List[GraphTraversalResult]:
        """
        Traversia principal del grafo basada en la query.

        Args:
            query: Consulta del usuario
            max_hops: Máxima profundidad de traversia (default: self.max_hops)
            min_relevance: Score mínimo de relevancia

        Returns:
            Lista de caminos relevantes ordenados por score
        """
        start_time = time.time()
        max_hops = max_hops or self.max_hops

        try:
            # 1. Extraer entidades de la query
            query_entities = self._extract_entities_from_query(query)
            logger.debug(f"Entidades extraídas de query: {query_entities}")

            if not query_entities:
                logger.info("No se encontraron entidades en la query")
                return []

            # 2. Buscar nodos correspondientes en el grafo
            graph_nodes = self._find_nodes_for_entities(query_entities)
            logger.debug(f"Nodos encontrados en grafo: {[n.name for n in graph_nodes]}")

            if not graph_nodes:
                logger.info("No se encontraron nodos correspondientes en el grafo")
                return []

            # 3. Realizar traversia desde cada nodo
            all_paths = []
            for start_node in graph_nodes:
                paths = self._traverse_from_node(
                    start_node.name, max_hops, query_entities
                )
                all_paths.extend(paths)

            # 4. Filtrar, rankear y combinar resultados
            ranked_paths = self._rank_and_filter_paths(
                all_paths, query_entities, min_relevance
            )

            elapsed = (time.time() - start_time) * 1000
            logger.info(f"Graph traversal completed in {elapsed:.1f}ms, found {len(ranked_paths)} paths")

            return ranked_paths

        except Exception as e:
            logger.error(f"Error en traversia de grafo: {e}", exc_info=True)
            return []

    def _extract_entities_from_query(self, query: str) -> List[str]:
        """Extraer posibles nombres de entidades de una query natural."""
        entities = []

        # Patrones para identificar entidades
        patterns = [
            # Nombres propios (inician con mayúscula, siguen con minúsculas)
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
            # Acrónimos (múltiples mayúsculas)
            r'\b[A-Z]{2,}\b',
            # Términos entre comillas
            r'"([^"]+)"',
            # Términos específicos del dominio (ajustar según necesidad)
        ]

        # Buscar con cada patrón
        for pattern in patterns:
            matches = re.findall(pattern, query)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]  # Para grupos de captura
                if len(match) > 2:  # Ignorar strings muy cortos
                    entities.append(match)

        # También considerar palabras sustantivas (simplificado)
        # Esto es básico, en producción usar NER
        words = query.split()
        for i, word in enumerate(words):
            # Palabras que podrían ser entidades (sustantivos)
            if (len(word) > 3 and word.isalpha() and
                not word.lower() in {'con', 'para', 'desde', 'hacia', 'sobre'}):
                # Si la palabra anterior es un artículo, podría ser entidad
                if i > 0 and words[i-1].lower() in {'el', 'la', 'los', 'las', 'un', 'una'}:
                    entities.append(word)

        # Eliminar duplicados manteniendo orden
        seen = set()
        unique_entities = []
        for ent in entities:
            if ent not in seen:
                seen.add(ent)
                unique_entities.append(ent)

        return unique_entities

    def _find_nodes_for_entities(self, entities: List[str]) -> List[GraphNode]:
        """Buscar nodos en el grafo que correspondan a las entidades."""
        nodes = []

        for entity in entities:
            # Búsqueda exacta
            exact_nodes = self._find_nodes_by_name(entity, exact=True)
            if exact_nodes:
                nodes.extend(exact_nodes)
                continue

            # Búsqueda parcial (LIKE)
            partial_nodes = self._find_nodes_by_name(entity, exact=False)
            nodes.extend(partial_nodes)

        # Eliminar duplicados por nombre
        seen_names = set()
        unique_nodes = []
        for node in nodes:
            if node.name not in seen_names:
                seen_names.add(node.name)
                unique_nodes.append(node)

        return unique_nodes

    def _find_nodes_by_name(self, name: str, exact: bool = True) -> List[GraphNode]:
        """Buscar nodos por nombre en la base de datos Kùzu."""
        try:
            if exact:
                query = """
                    MATCH (e:Entity)
                    WHERE e.name = $name
                    RETURN e.name, e.type, e.validated, e.source_doc
                """
                params = {"name": name}
            else:
                query = """
                    MATCH (e:Entity)
                    WHERE e.name CONTAINS $name_part
                    RETURN e.name, e.type, e.validated, e.source_doc
                """
                params = {"name_part": name}

            result = self.conn.execute(query, params)

            nodes = []
            while result.has_next():
                row = result.get_next()
                node = GraphNode(
                    name=row[0],
                    type=row[1] or "unknown",
                    validated=bool(row[2]),
                    source_doc=row[3]
                )
                nodes.append(node)

            return nodes

        except Exception as e:
            logger.error(f"Error buscando nodos por nombre '{name}': {e}")
            return []

    def _traverse_from_node(self, start_node_name: str, max_hops: int,
                          query_entities: List[str]) -> List[GraphTraversalResult]:
        """Realizar traversia desde un nodo específico."""
        paths = []

        try:
            # Cypher query para traversia de hasta max_hops saltos
            query = """
                MATCH path = (start:Entity {name: $start_name})-[*1..$max_hops]-(end:Entity)
                UNWIND relationships(path) as rel
                RETURN
                    nodes(path) as nodes_list,
                    collect(DISTINCT rel) as rels_list,
                    length(path) as path_length
                ORDER BY path_length ASC
                LIMIT 20
            """

            result = self.conn.execute(query, {
                "start_name": start_node_name,
                "max_hops": max_hops
            })

            while result.has_next():
                row = result.get_next()
                nodes_list = row[0]
                rels_list = row[1]
                path_length = row[2]

                # Convertir nodos Kùzu a GraphNode
                graph_nodes = []
                for kuzu_node in nodes_list:
                    node = GraphNode(
                        name=kuzu_node['name'],
                        type=kuzu_node.get('type', 'unknown'),
                        validated=bool(kuzu_node.get('validated', False)),
                        source_doc=kuzu_node.get('source_doc')
                    )
                    graph_nodes.append(node)

                # Convertir relaciones Kùzu a GraphRelationship
                graph_rels = []
                for kuzu_rel in rels_list:
                    rel = GraphRelationship(
                        from_node=kuzu_rel['_src']['name'],
                        to_node=kuzu_rel['_dst']['name'],
                        relation_type=kuzu_rel.get('_label', 'RELATES_TO'),
                        weight=float(kuzu_rel.get('weight', 1.0)),
                        criticality=kuzu_rel.get('criticality', 'C1'),
                        validated=bool(kuzu_rel.get('validated', False)),
                        context=kuzu_rel.get('context')
                    )
                    graph_rels.append(rel)

                # Calcular relevancia para este path
                relevance = self._calculate_path_relevance(
                    graph_nodes, graph_rels, query_entities, path_length
                )

                # Crear resultado
                traversal_result = GraphTraversalResult(
                    path_nodes=graph_nodes,
                    path_relationships=graph_rels,
                    relevance_score=relevance,
                    traversal_depth=path_length,
                    query_coverage=self._calculate_query_coverage(graph_nodes, query_entities)
                )

                paths.append(traversal_result)

            return paths

        except Exception as e:
            logger.error(f"Error en traversia desde nodo '{start_node_name}': {e}")
            return []

    def _calculate_path_relevance(self, nodes: List[GraphNode],
                                rels: List[GraphRelationship],
                                query_entities: List[str],
                                path_length: int) -> float:
        """Calcular score de relevancia para un camino."""
        if not nodes or not rels:
            return 0.0

        base_score = 0.5  # Score base

        # 1. Bonus por nodos validados
        validated_nodes = sum(1 for n in nodes if n.validated)
        base_score += validated_nodes * 0.05

        # 2. Bonus por relaciones validadas
        validated_rels = sum(1 for r in rels if r.validated)
        base_score += validated_rels * 0.03

        # 3. Bonus por criticidad alta (C3, C4)
        high_crit_rels = sum(1 for r in rels if r.criticality in ['C3', 'C4'])
        base_score += high_crit_rels * 0.02

        # 4. Penalización por path muy largo (sobreajuste)
        if path_length > self.max_hops:
            base_score -= (path_length - self.max_hops) * 0.1

        # 5. Bonus por cobertura de entidades de la query
        query_coverage = self._calculate_query_coverage(nodes, query_entities)
        base_score += query_coverage * 0.2

        # 6. Bonus por diversidad de tipos de relación
        rel_types = set(r.relation_type for r in rels)
        base_score += len(rel_types) * 0.01

        return max(0.0, min(1.0, base_score))

    def _calculate_query_coverage(self, nodes: List[GraphNode],
                                query_entities: List[str]) -> float:
        """Calcular % de entidades de la query cubiertas por los nodos del path."""
        if not query_entities:
            return 0.0

        node_names = set(n.name.lower() for n in nodes)
        covered = 0

        for entity in query_entities:
            entity_lower = entity.lower()
            # Check exact match o partial match
            if entity_lower in node_names:
                covered += 1
            else:
                # Check si algún nodo contiene la entidad
                for node_name in node_names:
                    if entity_lower in node_name:
                        covered += 0.5  # Partial match
                        break

        return covered / len(query_entities)

    def _rank_and_filter_paths(self, paths: List[GraphTraversalResult],
                             query_entities: List[str],
                             min_relevance: float) -> List[GraphTraversalResult]:
        """Rankear y filtrar caminos por relevancia."""
        if not paths:
            return []

        # Filtrar por relevancia mínima
        filtered = [p for p in paths if p.relevance_score >= min_relevance]

        # Ordenar por score descendente
        filtered.sort(key=lambda x: x.relevance_score, reverse=True)

        # Eliminar caminos duplicados o muy similares
        unique_paths = []
        seen_node_sets = set()

        for path in filtered:
            # Crear firma del path (conjunto ordenado de nodos)
            node_signature = tuple(sorted(n.name for n in path.path_nodes))

            if node_signature not in seen_node_sets:
                seen_node_sets.add(node_signature)
                unique_paths.append(path)

            # Limitar número de resultados
            if len(unique_paths) >= 10:
                break

        return unique_paths

    def add_entity(self, name: str, entity_type: str = "unknown",
                  source_doc: Optional[str] = None,
                  validated: bool = False) -> bool:
        """Agregar una nueva entidad al grafo."""
        try:
            query = """
                CREATE (e:Entity {
                    name: $name,
                    type: $type,
                    source_doc: $source_doc,
                    validated: $validated
                })
            """

            self.conn.execute(query, {
                "name": name,
                "type": entity_type,
                "source_doc": source_doc or "",
                "validated": validated
            })

            logger.debug(f"Entidad creada: {name}")
            return True

        except Exception as e:
            logger.error(f"Error creando entidad '{name}': {e}")
            return False

    def add_relationship(self, from_entity: str, to_entity: str,
                        relation_type: str, weight: float = 1.0,
                        criticality: str = "C1", validated: bool = False,
                        context: Optional[str] = None) -> bool:
        """Agregar una nueva relación al grafo."""
        try:
            # Asegurar que existan los nodos
            self._ensure_entity_exists(from_entity)
            self._ensure_entity_exists(to_entity)

            # Determinar tabla de relación basada en el tipo
            rel_table = self._get_relation_table(relation_type)

            query = f"""
                MATCH (a:Entity {{name: $from_name}}), (b:Entity {{name: $to_name}})
                CREATE (a)-[:{rel_table} {{
                    weight: $weight,
                    criticality: $criticality,
                    validated: $validated,
                    context: $context
                }}]->(b)
            """

            self.conn.execute(query, {
                "from_name": from_entity,
                "to_name": to_entity,
                "weight": weight,
                "criticality": criticality,
                "validated": validated,
                "context": context or ""
            })

            logger.debug(f"Relación creada: {from_entity} -[{relation_type}]-> {to_entity}")
            return True

        except Exception as e:
            logger.error(f"Error creando relación '{from_entity} → {to_entity}': {e}")
            return False

    def _ensure_entity_exists(self, entity_name: str):
        """Asegurar que una entidad exista en el grafo."""
        try:
            query = """
                MERGE (e:Entity {name: $name})
                RETURN e.name
            """
            self.conn.execute(query, {"name": entity_name})
        except Exception as e:
            logger.error(f"Error asegurando entidad '{entity_name}': {e}")
            raise

    def _get_relation_table(self, relation_type: str) -> str:
        """Mapear tipo de relación a tabla de relación Kùzu."""
        # Mapeo de tipos de relación comunes a tablas definidas
        relation_map = {
            "REQUIRES": "REQUIRES",
            "DEPENDE_DE": "REQUIRES",
            "USA": "REQUIRES",
            "RELATES_TO": "RELATES_TO",
            "SIMILAR_A": "RELATES_TO",
            "PART_OF": "PART_OF",
            "CONTIENE": "PART_OF",
        }
        return relation_map.get(relation_type.upper(), "RELATES_TO")

    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del grafo."""
        try:
            stats = {}

            # Contar nodos
            result = self.conn.execute("MATCH (e:Entity) RETURN COUNT(e) as count")
            if result.has_next():
                stats['total_nodes'] = result.get_next()[0]

            # Contar relaciones por tipo
            result = self.conn.execute("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, COUNT(r) as count
                ORDER BY count DESC
            """)

            rel_counts = {}
            while result.has_next():
                row = result.get_next()
                rel_counts[row[0]] = row[1]
            stats['relationship_counts'] = rel_counts

            # Nodos validados vs no validados
            result = self.conn.execute("""
                MATCH (e:Entity)
                RETURN e.validated as validated, COUNT(e) as count
            """)

            validation_stats = {'validated': 0, 'unvalidated': 0}
            while result.has_next():
                row = result.get_next()
                if row[0]:
                    validation_stats['validated'] = row[1]
                else:
                    validation_stats['unvalidated'] = row[1]
            stats['validation_stats'] = validation_stats

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo stats del grafo: {e}")
            return {'error': str(e)}

    def close(self):
        """Cerrar conexión a Kùzu."""
        if self._conn:
            self._conn.close()
            self._conn = None
            self._db = None

    def __del__(self):
        self.close()
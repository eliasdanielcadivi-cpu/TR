#!/usr/bin/env python3
"""
Motor de recuperación por capas (T0-T4).

Diseñado para latencia ≈ 0 en T0-T3, T4 bajo demanda explícita.
Implementa la estrategia de recuperación progresiva del blueprint SISTEMA-V3.
"""

import time
import sqlite3
import hashlib
import os
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from functools import lru_cache
import json


class Tier(Enum):
    """Niveles de recuperación del sistema RAG."""
    T0_CACHE = auto()      # Cache en memoria (latencia ≈ 0)
    T1_SQL = auto()        # Búsqueda determinista SQL (latencia < 10ms)
    T2_VECTOR = auto()     # Búsqueda semántica por embeddings (latencia < 50ms)
    T3_GRAPH = auto()      # Traversia de grafo de conocimiento (latencia < 100ms)
    T4_REASONING = auto()  # Razonamiento profundo con LLM (latencia 1-10s)

    @property
    def value(self) -> int:
        """Valor numérico para comparación de tiers."""
        return {
            Tier.T0_CACHE: 0,
            Tier.T1_SQL: 1,
            Tier.T2_VECTOR: 2,
            Tier.T3_GRAPH: 3,
            Tier.T4_REASONING: 4
        }[self]

    @property
    def name(self) -> str:
        """Nombre legible del tier."""
        return {
            Tier.T0_CACHE: "T0_CACHE",
            Tier.T1_SQL: "T1_SQL",
            Tier.T2_VECTOR: "T2_VECTOR",
            Tier.T3_GRAPH: "T3_GRAPH",
            Tier.T4_REASONING: "T4_REASONING"
        }[self]


@dataclass
class RetrievalResult:
    """Resultado de una recuperación RAG."""
    data: Any                    # Datos recuperados (depende del tier)
    tier: Tier                   # Tier que produjo el resultado
    confidence: float            # Confianza (0.0-1.0)
    latency_ms: float            # Latencia en milisegundos
    sources: List[Dict] = field(default_factory=list)  # Fuentes/citas
    requires_t4: bool = False    # Indica que se necesita T4 para mejor respuesta
    t4_context: Optional[Dict] = None  # Contexto para T4 si se solicita


class TieredRAGRouter:
    """
    Router principal que implementa la estrategia de recuperación progresiva.
    Cada tier es un callable que retorna Optional[RetrievalResult].

    Args:
        config_path: Ruta al archivo de configuración rag.yaml
    """

    # Triggers semánticos para T4 (razonamiento profundo)
    T4_TRIGGERS = {
        'piensa', 'piénsalo', 'analiza profundo', 'deep dive',
        'modo pensamiento', 'razona paso a paso', 'think'
    }

    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.cache = {}  # T0: Simple dict, LRU por tamaño
        self.cache_max_size = self.config.get('tiers', {}).get('t0_cache', {}).get('max_size', 1000)

        # Inicializar rutas de bases de datos
        project_root = os.environ.get('TR_PROJECT_ROOT', os.path.expanduser('~/tron/programas/TR'))
        db_root = self.config.get('db_root', 'db/rag')
        db_root = os.path.join(project_root, db_root)

        self.db_paths = {
            'core': os.path.join(db_root, self.config.get('databases', {}).get('core', 'rag_core.sqlite')),
            'vectors': os.path.join(db_root, self.config.get('databases', {}).get('vectors', 'rag_vectors.sqlite')),
            'graph': os.path.join(db_root, self.config.get('databases', {}).get('graph', 'rag_graph.kuzu'))
        }

        # Motores lazy (se inicializan cuando se necesitan)
        self._sql_engine = None
        self._vector_engine = None
        self._graph_engine = None
        self._llm_engine = None

        # Tier handlers registrados
        self.tier_handlers: Dict[Tier, Callable] = {
            Tier.T0_CACHE: self._t0_cache_lookup,
            Tier.T1_SQL: self._t1_sql_search,
            Tier.T2_VECTOR: self._t2_vector_search,
            Tier.T3_GRAPH: self._t3_graph_traversal,
            Tier.T4_REASONING: self._t4_llm_reasoning,
        }

    @property
    def sql_engine(self):
        """Motor SQL lazy para T1."""
        if self._sql_engine is None:
            from ..engines.sql_engine import SQLEngine
            self._sql_engine = SQLEngine(self.db_paths['core'])
        return self._sql_engine

    @property
    def vector_engine(self):
        """Motor vectorial lazy para T2."""
        if self._vector_engine is None:
            from ..engines.vector_engine import VectorEngine
            embeddings_config = self.config.get('embeddings', {})
            self._vector_engine = VectorEngine(
                db_path=self.db_paths['vectors'],
                embedding_model=embeddings_config.get('model', 'nomic-embed-text:latest'),
                dimensions=embeddings_config.get('dimensions', 768),
                metric=embeddings_config.get('metric', 'cosine')
            )
        return self._vector_engine

    @property
    def graph_engine(self):
        """Motor de grafo lazy para T3."""
        if self._graph_engine is None:
            from ..engines.graph_engine import GraphEngine
            max_hops = self.config.get('tiers', {}).get('t3_graph', {}).get('max_hops', 3)
            self._graph_engine = GraphEngine(self.db_paths['graph'], max_hops=max_hops)
        return self._graph_engine

    @property
    def llm_engine(self):
        """Motor LLM lazy para T4."""
        if self._llm_engine is None:
            from ..engines.llm_engine import LLMEngine, ReasoningContext
            self._llm_engine = LLMEngine(self.config)
        return self._llm_engine

    def _load_config(self, path: str) -> dict:
        """Cargar configuración YAML."""
        try:
            import yaml
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️  Error cargando configuración {path}: {e}")
            return {}

    def is_t4_trigger(self, query: str) -> bool:
        """Detecta si el usuario solicita explícitamente razonamiento profundo."""
        query_lower = query.lower()
        triggers = self.config.get('t4_triggers', self.T4_TRIGGERS)
        return any(trigger in query_lower for trigger in triggers)

    def retrieve(self, query: str,
                 max_tier: Tier = Tier.T4_REASONING,
                 force_t4: bool = False,
                 session_context: Optional[Dict] = None) -> RetrievalResult:
        """
        Pipeline de recuperación progresiva T0 → T4.

        Args:
            query: Consulta del usuario
            max_tier: Tier máximo permitido (para ares p, default T3)
            force_t4: Si True, salta directo a T4 (solo para ares i con trigger)
            session_context: Datos de sesión (PID, proyecto actual, etc.)

        Returns:
            RetrievalResult con datos y metadatos
        """
        start_time = time.time()
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]

        # T4 forzado: bypass de T0-T3 (solo si max_tier permite T4)
        if force_t4 and max_tier.value >= Tier.T4_REASONING.value:
            return self._execute_t4(query, session_context, start_time)

        # Pipeline progresivo T0 → T3
        for tier in [Tier.T0_CACHE, Tier.T1_SQL, Tier.T2_VECTOR, Tier.T3_GRAPH]:
            if tier.value > max_tier.value:
                break

            handler = self.tier_handlers[tier]
            result = handler(query, query_hash, session_context)

            if result and result.confidence >= self._tier_threshold(tier):
                result.latency_ms = (time.time() - start_time) * 1000
                return result

        # T3 insuficiente: ofrecer T4 (pero no ejecutar)
        if Tier.T4_REASONING.value <= max_tier.value:
            t3_partial = self._t3_graph_traversal(query, query_hash, session_context)
            return RetrievalResult(
                data=t3_partial.data if t3_partial else {"insufficient_data": True},
                tier=Tier.T3_GRAPH,
                confidence=t3_partial.confidence if t3_partial else 0.5,
                latency_ms=(time.time() - start_time) * 1000,
                requires_t4=True,
                t4_context=self._prepare_t4_context(query, t3_partial, session_context)
            )

        # Fallback: nada encontrado
        return RetrievalResult(
            data={"error": "No se encontró información relevante"},
            tier=Tier.T3_GRAPH,
            confidence=0.0,
            latency_ms=(time.time() - start_time) * 1000
        )

    def _tier_threshold(self, tier: Tier) -> float:
        """Umbrales de confianza mínima por tier."""
        tier_configs = self.config.get('tiers', {})
        thresholds = {
            Tier.T0_CACHE: tier_configs.get('t0_cache', {}).get('confidence_threshold', 0.95),
            Tier.T1_SQL: tier_configs.get('t1_sql', {}).get('confidence_threshold', 0.90),
            Tier.T2_VECTOR: tier_configs.get('t2_vector', {}).get('confidence_threshold', 0.75),
            Tier.T3_GRAPH: tier_configs.get('t3_graph', {}).get('confidence_threshold', 0.70),
        }
        return thresholds.get(tier, 0.0)

    # ========== IMPLEMENTACIÓN DE TIERS ==========

    def _t0_cache_lookup(self, query: str, query_hash: str,
                        ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T0: Cache en memoria (LRU simple)."""
        if query_hash in self.cache:
            cached = self.cache[query_hash]
            # Mover al final (LRU)
            self.cache.pop(query_hash)
            self.cache[query_hash] = cached

            return RetrievalResult(
                data=cached['data'],
                tier=Tier.T0_CACHE,
                confidence=0.98,  # Alta confianza por ser exacto
                latency_ms=0,
                sources=cached.get('sources', [])
            )

        # Cache miss
        if len(self.cache) >= self.cache_max_size:
            # Eliminar el más antiguo (primero en dict)
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)

        return None

    def _t1_sql_search(self, query: str, query_hash: str,
                      ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T1: Búsqueda exacta y semántica ligera en SQL."""
        try:
            results = self.sql_engine.search(query, limit=10)

            if not results:
                return None

            # Calcular confianza promedio de los resultados
            avg_confidence = sum(r.relevance_score for r in results) / len(results)

            # Convertir a formato de fuentes
            sources = []
            for result in results[:5]:  # Limitar a 5 fuentes principales
                source = {
                    'type': 'sql',
                    'doc_id': result.doc_id,
                    'content': result.content[:500],  # Truncar
                    'relevance': result.relevance_score,
                    'match_type': result.match_type,
                    'source_path': result.source_path
                }
                if result.entity_tags:
                    source['entity_tags'] = result.entity_tags
                sources.append(source)

            # Preparar datos para respuesta
            data = {
                'summary': f"Encontrada información en {len(results)} documentos",
                'top_matches': [r.content[:200] for r in results[:3]],
                'total_results': len(results)
            }

            return RetrievalResult(
                data=data,
                tier=Tier.T1_SQL,
                confidence=avg_confidence,
                latency_ms=0,  # Se ajustará después
                sources=sources
            )

        except Exception as e:
            print(f"⚠️  Error en búsqueda SQL T1: {e}")
            return None

    def _t2_vector_search(self, query: str, query_hash: str,
                         ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T2: Búsqueda por similitud de embeddings (sqlite-vec)."""
        try:
            # Obtener umbral de similitud de configuración
            similarity_threshold = self.config.get('tiers', {}).get('t2_vector', {}).get('similarity_threshold', 0.7)

            results = self.vector_engine.search(
                query, limit=10, min_similarity=similarity_threshold
            )

            if not results:
                return None

            # Calcular confianza promedio (ajustada por similitud)
            avg_similarity = sum(r.similarity_score for r in results) / len(results)

            # Convertir a formato de fuentes
            sources = []
            for result in results[:5]:  # Limitar a 5 fuentes principales
                source = {
                    'type': 'vector',
                    'chunk_id': result.chunk_id,
                    'doc_id': result.doc_id,
                    'content': result.content[:500],  # Truncar
                    'similarity': result.similarity_score,
                    'embedding_model': result.embedding_model
                }
                if result.entity_tags:
                    source['entity_tags'] = result.entity_tags
                if result.metadata:
                    source['metadata'] = result.metadata
                sources.append(source)

            # Preparar datos para respuesta
            data = {
                'summary': f"Encontrados {len(results)} chunks semánticamente similares",
                'avg_similarity': avg_similarity,
                'top_matches': [r.content[:200] for r in results[:3]],
                'embedding_model': results[0].embedding_model if results else 'unknown'
            }

            return RetrievalResult(
                data=data,
                tier=Tier.T2_VECTOR,
                confidence=avg_similarity,  # Usar similitud como confianza
                latency_ms=0,  # Se ajustará después
                sources=sources
            )

        except Exception as e:
            print(f"⚠️  Error en búsqueda vectorial T2: {e}")
            return None

    def _t3_graph_traversal(self, query: str, query_hash: str,
                           ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T3: Navegación por grafo de conocimiento (Kùzu)."""
        try:
            # Obtener umbral de confianza de configuración
            confidence_threshold = self.config.get('tiers', {}).get('t3_graph', {}).get('confidence_threshold', 0.7)

            paths = self.graph_engine.traverse(query, min_relevance=confidence_threshold)

            if not paths:
                return None

            # Tomar el mejor camino (mayor relevancia)
            best_path = paths[0]

            # Convertir a formato de fuentes
            sources = []
            for i, node in enumerate(best_path.path_nodes[:5]):  # Limitar nodos
                source = {
                    'type': 'graph_node',
                    'entity_name': node.name,
                    'entity_type': node.type,
                    'validated': node.validated,
                    'source_doc': node.source_doc,
                    'relevance': best_path.relevance_score * (0.9 ** i)  # Decreciente por posición
                }
                sources.append(source)

            # Agregar relaciones como fuentes adicionales
            for i, rel in enumerate(best_path.path_relationships[:3]):
                source = {
                    'type': 'graph_relationship',
                    'from': rel.from_node,
                    'to': rel.to_node,
                    'relation_type': rel.relation_type,
                    'criticality': rel.criticality,
                    'validated': rel.validated,
                    'weight': rel.weight,
                    'relevance': best_path.relevance_score * (0.8 ** i)
                }
                if rel.context:
                    source['context'] = rel.context[:200]
                sources.append(source)

            # Preparar datos para respuesta
            data = {
                'summary': f"Traversia de grafo con {len(best_path.path_nodes)} nodos y {len(best_path.path_relationships)} relaciones",
                'query_coverage': best_path.query_coverage,
                'traversal_depth': best_path.traversal_depth,
                'path_summary': f"{best_path.path_nodes[0].name} → ... → {best_path.path_nodes[-1].name}" if best_path.path_nodes else "empty",
                'available_entities': [n.name for n in best_path.path_nodes]
            }

            return RetrievalResult(
                data=data,
                tier=Tier.T3_GRAPH,
                confidence=best_path.relevance_score,
                latency_ms=0,  # Se ajustará después
                sources=sources
            )

        except Exception as e:
            print(f"⚠️  Error en traversia de grafo T3: {e}")
            return None

    def _t4_llm_reasoning(self, query: str, ctx: Optional[Dict],
                         start_time: float) -> RetrievalResult:
        """T4: Razonamiento profundo con LLM local (Ollama/DeepSeek)."""
        try:
            from ..engines.llm_engine import ReasoningContext

            # Preparar contexto de razonamiento
            reasoning_context = ReasoningContext(
                original_query=query,
                t3_partial_data=ctx.get('t3_partial_data') if ctx else None,
                session_project=ctx.get('session_project') if ctx else None,
                available_entities=ctx.get('available_entities', []) if ctx else [],
                suggested_reasoning_path=ctx.get('suggested_reasoning_path', 'Análisis profundo') if ctx else 'Análisis profundo',
                user_constraints=ctx.get('user_constraints') if ctx else None,
                max_token_limit=self.config.get('t4', {}).get('max_tokens', 4096)
            )

            # Ejecutar razonamiento
            result = self.llm_engine.reason(reasoning_context)

            # Convertir a formato RetrievalResult
            sources = []
            for i, step in enumerate(result.reasoning_steps):
                source = {
                    'type': 'reasoning_step',
                    'step': step.step.value,
                    'content': step.content[:300],
                    'confidence': step.confidence,
                    'order': i
                }
                sources.append(source)

            # Agregar fuentes citadas
            for i, citation in enumerate(result.sources_cited):
                source = {
                    'type': 'citation',
                    'source': citation.get('source', 'unknown'),
                    'reference': citation.get('reference', ''),
                    'relevance': citation.get('relevance', 0.5)
                }
                sources.append(source)

            return RetrievalResult(
                data={
                    'answer': result.answer,
                    'reasoning_summary': f"{len(result.reasoning_steps)} pasos de razonamiento",
                    'confidence_breakdown': {
                        'overall': result.confidence,
                        'provider': result.provider_used,
                        'latency_ms': result.latency_ms
                    }
                },
                tier=Tier.T4_REASONING,
                confidence=result.confidence,
                latency_ms=result.latency_ms,
                sources=sources
            )

        except Exception as e:
            print(f"⚠️  Error en razonamiento T4: {e}")
            # Fallback a implementación básica
            return RetrievalResult(
                data={"reasoning": f"Error en razonamiento profundo: {str(e)[:100]}"},
                tier=Tier.T4_REASONING,
                confidence=0.3,
                latency_ms=(time.time() - start_time) * 1000
            )

    def _prepare_t4_context(self, query: str, t3_result: Optional[RetrievalResult],
                           session_ctx: Optional[Dict]) -> Dict:
        """Prepara el contexto enriquecido para T4."""
        # Extraer entidades del resultado T3 si está disponible
        available_entities = []
        if t3_result and t3_result.sources:
            # Extraer nombres de entidades de fuentes T3
            for source in t3_result.sources:
                if source.get('type') == 'graph_node':
                    available_entities.append(source.get('entity_name', ''))
                elif source.get('type') == 'sql' and source.get('entity_tags'):
                    available_entities.extend(source.get('entity_tags', []))

        # Eliminar duplicados
        available_entities = list(set(filter(None, available_entities)))

        # Determinar camino de razonamiento sugerido basado en la query
        suggested_path = self._suggest_reasoning_path(query, t3_result)

        return {
            "original_query": query,
            "t3_partial_data": t3_result.data if t3_result else None,
            "session_project": session_ctx.get('project') if session_ctx else None,
            "available_entities": available_entities,
            "suggested_reasoning_path": suggested_path,
            "user_constraints": {
                "max_tokens": self.config.get('t4', {}).get('max_tokens', 4096),
                "require_citations": True
            }
        }

    def _suggest_reasoning_path(self, query: str, t3_result: Optional[RetrievalResult]) -> str:
        """Sugerir un camino de razonamiento basado en la query y resultados T3."""
        query_lower = query.lower()

        # Patrones en la query
        if any(word in query_lower for word in ['cómo', 'como funciona', 'funcionamiento']):
            return "Análisis de mecanismos y procesos involucrados"
        elif any(word in query_lower for word in ['por qué', 'porque', 'razón', 'causa']):
            return "Análisis causal y de razones fundamentales"
        elif any(word in query_lower for word in ['comparar', 'diferencias', 'similaridades']):
            return "Análisis comparativo y de contrastes"
        elif any(word in query_lower for word in ['implementar', 'construir', 'crear']):
            return "Análisis de implementación y consideraciones prácticas"
        elif any(word in query_lower for word in ['problema', 'error', 'solucionar']):
            return "Análisis de problemas y estrategias de solución"
        elif t3_result and t3_result.data and t3_result.data.get('available_entities'):
            return f"Análisis de relaciones entre {len(t3_result.data.get('available_entities', []))} entidades identificadas"
        else:
            return "Análisis profundo de contexto y relaciones"

    def _execute_t4(self, query: str, ctx: Optional[Dict],
                   start_time: float) -> RetrievalResult:
        """Ejecución completa de T4 con streaming de progreso."""
        # TODO: Integrar con LLMEngine con streaming
        return self._t4_llm_reasoning(query, ctx, start_time)

    # ========== MÉTODOS DE GESTIÓN DE CACHE ==========

    def add_to_cache(self, query: str, result: RetrievalResult) -> None:
        """Agregar resultado al cache T0."""
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
        self.cache[query_hash] = {
            'data': result.data,
            'sources': result.sources,
            'timestamp': time.time()
        }

    def clear_cache(self) -> None:
        """Limpiar cache T0."""
        self.cache.clear()
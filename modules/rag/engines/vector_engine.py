#!/usr/bin/env python3
"""
Motor de búsqueda vectorial (T2).

Búsqueda semántica por similitud de embeddings usando sqlite-vec.
Genera embeddings de la query y busca chunks similares en la base de datos.
"""

import sqlite3
import time
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class VectorSearchResult:
    """Resultado de búsqueda vectorial."""
    chunk_id: int
    doc_id: str
    content: str
    similarity_score: float
    embedding_model: str
    entity_tags: List[str] = None
    metadata: Dict[str, Any] = None


class VectorEngine:
    """
    Motor de búsqueda semántica T2.

    Características:
    - Generación de embeddings para queries
    - Búsqueda por similitud coseno
    - Filtrado híbrido (semántica + keywords)
    - Cache de embeddings frecuentes
    """

    def __init__(self, db_path: str, embedding_model: str = "nomic-embed-text:latest",
                 dimensions: int = 768, metric: str = "cosine"):
        self.db_path = db_path
        self.embedding_model = embedding_model
        self.dimensions = dimensions
        self.metric = metric
        self._conn = None
        self._embedding_cache = {}  # Cache simple de embeddings
        self._model_initialized = False

    @property
    def conn(self):
        """Conexión lazy a SQLite con extensión sqlite-vec."""
        if self._conn is None:
            try:
                import sqlite_vec
                self._conn = sqlite3.connect(self.db_path)
                self._conn.enable_load_extension(True)
                sqlite_vec.load(self._conn)
                self._conn.enable_load_extension(False)
                self._conn.row_factory = sqlite3.Row
                logger.info(f"✅ Conexión sqlite-vec establecida a {self.db_path}")
            except ImportError as e:
                logger.error(f"❌ sqlite-vec no está instalado: {e}")
                raise
            except Exception as e:
                logger.error(f"❌ Error conectando a {self.db_path}: {e}")
                raise
        return self._conn

    def search(self, query: str, limit: int = 10,
               min_similarity: float = 0.7) -> List[VectorSearchResult]:
        """
        Búsqueda semántica principal.

        Args:
            query: Texto de consulta
            limit: Máximo de resultados
            min_similarity: Umbral mínimo de similitud (0.0-1.0)

        Returns:
            Lista de resultados ordenados por similitud descendente
        """
        start_time = time.time()

        try:
            # 1. Generar embedding de la query
            query_embedding = self._generate_embedding(query)
            if query_embedding is None:
                logger.warning("No se pudo generar embedding, fallback a búsqueda por keywords")
                return self._fallback_search(query, limit)

            # 2. Buscar chunks similares en la base de datos
            results = self._vector_search(query_embedding, limit * 2, min_similarity)

            # 3. Post-procesamiento y ranking
            processed_results = self._process_results(results, query, query_embedding)

            # 4. Filtrar por umbral y limitar
            final_results = [r for r in processed_results if r.similarity_score >= min_similarity]
            final_results = final_results[:limit]

            elapsed = (time.time() - start_time) * 1000
            logger.debug(f"Vector search completed in {elapsed:.1f}ms, found {len(final_results)} results")

            return final_results

        except Exception as e:
            logger.error(f"Error en búsqueda vectorial: {e}", exc_info=True)
            return self._fallback_search(query, limit)

    def _generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """Generar embedding para texto usando Ollama local."""
        # Cache lookup
        cache_key = text[:100]  # Primeros 100 chars como clave
        if cache_key in self._embedding_cache:
            return self._embedding_cache[cache_key]

        try:
            # Intento 1: Ollama local
            embedding = self._generate_embedding_ollama(text)
            if embedding is not None:
                self._embedding_cache[cache_key] = embedding
                # Limitar tamaño del cache
                if len(self._embedding_cache) > 100:
                    oldest_key = next(iter(self._embedding_cache))
                    del self._embedding_cache[oldest_key]
                return embedding

            # Intento 2: Fallback a modelo simple (TODO: implementar)
            logger.warning("Ollama no disponible, usando embedding dummy para desarrollo")
            # Embedding dummy para desarrollo
            embedding = np.random.randn(self.dimensions).astype(np.float32)
            embedding = embedding / np.linalg.norm(embedding)  # Normalizar
            self._embedding_cache[cache_key] = embedding
            return embedding

        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            return None

    def _generate_embedding_ollama(self, text: str) -> Optional[np.ndarray]:
        """Generar embedding usando Ollama."""
        try:
            import requests
            import json

            # Ollama API endpoint
            url = "http://localhost:11434/api/embeddings"

            payload = {
                "model": self.embedding_model,
                "prompt": text
            }

            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                embedding = np.array(result["embedding"], dtype=np.float32)

                # Verificar dimensiones
                if len(embedding) != self.dimensions:
                    logger.warning(f"Dimensión de embedding incorrecta: {len(embedding)} != {self.dimensions}")
                    # Ajustar si es necesario (padding o truncamiento)
                    if len(embedding) < self.dimensions:
                        padding = np.zeros(self.dimensions - len(embedding), dtype=np.float32)
                        embedding = np.concatenate([embedding, padding])
                    else:
                        embedding = embedding[:self.dimensions]

                return embedding
            else:
                logger.warning(f"Ollama API error: {response.status_code}")
                return None

        except ImportError:
            logger.warning("requests no instalado, no se puede usar Ollama")
            return None
        except Exception as e:
            logger.warning(f"Error llamando a Ollama: {e}")
            return None

    def _vector_search(self, query_embedding: np.ndarray,
                      limit: int, min_similarity: float) -> List[Tuple]:
        """Buscar embeddings similares en la base de datos."""
        # Convertir embedding a lista para SQLite
        embedding_list = query_embedding.tolist()

        c = self.conn.cursor()

        # Búsqueda por similitud usando sqlite-vec
        # La función vec_distance_l2 calcula distancia L2, menor = más similar
        # Para coseno, asumimos embeddings normalizados: distancia L2 ≈ sqrt(2 - 2*cos_sim)
        c.execute("""
            SELECT chunk_id, doc_id, entity_tags,
                   vec_distance_l2(embedding, ?) as distance
            FROM embeddings
            WHERE distance IS NOT NULL
            ORDER BY distance ASC
            LIMIT ?
        """, (embedding_list, limit))

        results = []
        for row in c.fetchall():
            # Convertir distancia L2 a similitud coseno (asumiendo embeddings normalizados)
            # cos_sim = 1 - distance^2 / 2
            distance = row['distance']
            if distance is not None:
                similarity = max(0.0, 1.0 - (distance ** 2) / 2.0)

                if similarity >= min_similarity:
                    # Obtener contenido del chunk
                    c2 = self.conn.cursor()
                    c2.execute("""
                        SELECT c.content, d.source_path, d.title
                        FROM chunks c
                        JOIN documents d ON c.doc_id = d.doc_id
                        WHERE c.id = ?
                    """, (row['chunk_id'],))

                    content_row = c2.fetchone()
                    if content_row:
                        # Parsear entity_tags
                        entity_tags = []
                        if row['entity_tags']:
                            try:
                                entity_tags = json.loads(row['entity_tags'])
                            except:
                                entity_tags = [row['entity_tags']]

                        results.append((
                            row['chunk_id'],
                            row['doc_id'],
                            content_row['content'],
                            similarity,
                            entity_tags,
                            {
                                'source_path': content_row['source_path'],
                                'title': content_row['title']
                            }
                        ))

        return results

    def _process_results(self, raw_results: List[Tuple], query: str,
                        query_embedding: np.ndarray) -> List[VectorSearchResult]:
        """Post-procesamiento y enriquecimiento de resultados."""
        processed = []

        for chunk_id, doc_id, content, similarity, entity_tags, metadata in raw_results:
            # Calcular score ajustado
            adjusted_score = self._adjust_similarity_score(
                similarity, content, query, entity_tags
            )

            result = VectorSearchResult(
                chunk_id=chunk_id,
                doc_id=doc_id,
                content=content,
                similarity_score=adjusted_score,
                embedding_model=self.embedding_model,
                entity_tags=entity_tags,
                metadata=metadata
            )
            processed.append(result)

        # Ordenar por score ajustado
        processed.sort(key=lambda x: x.similarity_score, reverse=True)
        return processed

    def _adjust_similarity_score(self, base_score: float, content: str,
                                query: str, entity_tags: List[str]) -> float:
        """Ajustar score de similitud basado en factores adicionales."""
        adjusted = base_score

        # Bonus por presencia de palabras clave de la query
        query_words = set(query.lower().split())
        content_lower = content.lower()
        keyword_matches = sum(1 for word in query_words if len(word) > 3 and word in content_lower)

        if keyword_matches > 0:
            adjusted += min(0.15, keyword_matches * 0.03)

        # Bonus por entidades relevantes
        if entity_tags:
            # Verificar si alguna entidad aparece en la query
            for entity in entity_tags:
                if isinstance(entity, str) and entity.lower() in query.lower():
                    adjusted += 0.05
                    break

        # Penalización por contenido muy corto
        if len(content) < 50:
            adjusted -= 0.1

        # Asegurar que esté en rango [0, 1]
        return max(0.0, min(1.0, adjusted))

    def _fallback_search(self, query: str, limit: int) -> List[VectorSearchResult]:
        """Fallback a búsqueda por keywords cuando falla la búsqueda vectorial."""
        logger.info(f"Usando fallback search para: {query}")

        try:
            # Conectar a core DB para búsqueda por keywords
            core_db_path = self.db_path.replace('_vectors.sqlite', '_core.sqlite')
            import sys
            sys.path.append('/home/daniel/tron/programas/TR/modules/rag/engines')
            from sql_engine import SQLEngine

            sql_engine = SQLEngine(core_db_path)
            sql_results = sql_engine.search(query, limit=limit * 2)

            # Convertir resultados SQL a formato vectorial
            vector_results = []
            for sql_result in sql_results[:limit]:
                vector_result = VectorSearchResult(
                    chunk_id=sql_result.chunk_id or 0,
                    doc_id=sql_result.doc_id,
                    content=sql_result.content,
                    similarity_score=sql_result.relevance_score * 0.8,  # Escalar
                    embedding_model="keyword_fallback",
                    entity_tags=sql_result.entity_tags,
                    metadata={'source_path': sql_result.source_path}
                )
                vector_results.append(vector_result)

            sql_engine.close()
            return vector_results

        except Exception as e:
            logger.error(f"Error en fallback search: {e}")
            return []

    def index_chunk(self, chunk_id: int, doc_id: str, content: str,
                   embedding: Optional[np.ndarray] = None,
                   entity_tags: List[str] = None) -> bool:
        """
        Indexar un chunk en la base de datos vectorial.

        Args:
            chunk_id: ID único del chunk
            doc_id: ID del documento padre
            content: Contenido del chunk
            embedding: Embedding pre-calculado (opcional)
            entity_tags: Lista de etiquetas de entidades

        Returns:
            True si se indexó correctamente
        """
        try:
            # Generar embedding si no se proporciona
            if embedding is None:
                embedding = self._generate_embedding(content)
                if embedding is None:
                    logger.error(f"No se pudo generar embedding para chunk {chunk_id}")
                    return False

            # Convertir a lista
            embedding_list = embedding.tolist()

            # Convertir entity_tags a JSON string
            tags_json = json.dumps(entity_tags or [])

            c = self.conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO embeddings (chunk_id, embedding, doc_id, entity_tags)
                VALUES (?, ?, ?, ?)
            """, (chunk_id, embedding_list, doc_id, tags_json))

            self.conn.commit()
            logger.debug(f"Indexado chunk {chunk_id} en base vectorial")
            return True

        except Exception as e:
            logger.error(f"Error indexando chunk {chunk_id}: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la base de datos vectorial."""
        try:
            c = self.conn.cursor()
            c.execute("SELECT COUNT(*) as count FROM embeddings")
            count_row = c.fetchone()
            count = count_row['count'] if count_row else 0

            c.execute("SELECT COUNT(DISTINCT doc_id) as doc_count FROM embeddings")
            doc_row = c.fetchone()
            doc_count = doc_row['doc_count'] if doc_row else 0

            return {
                'total_embeddings': count,
                'unique_documents': doc_count,
                'embedding_dimensions': self.dimensions,
                'embedding_model': self.embedding_model,
                'cache_size': len(self._embedding_cache)
            }
        except Exception as e:
            logger.error(f"Error obteniendo stats: {e}")
            return {'error': str(e)}

    def close(self):
        """Cerrar conexión a la base de datos."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __del__(self):
        self.close()


# Import json para serialización
import json
#!/usr/bin/env python3
"""
GraphBuilder: Construye grafo de conocimiento desde documentos procesados.

Extrae entidades y relaciones, las convierte en nodos y aristas del grafo.
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class GraphBuilder:
    """
    Constructor de grafos de conocimiento.
    
    Convierte entidades y relaciones extraídas por los ingestores
    en nodos y aristas de la base de datos Kùzu.
    """
    
    def __init__(self, db_path: str):
        """
        Inicializar GraphBuilder.
        
        Args:
            db_path: Ruta a la base de datos Kùzu
        """
        self.db_path = db_path
        self._db = None
        self._conn = None
    
    def _get_connection(self):
        """Obtener conexión lazy a la base de datos."""
        if self._conn is None:
            try:
                import kuzu
                # db_path es 'db/rag/rag_graph.kuzu', necesitamos 'db/rag/rag_graph.kuzu/db'
                self._db = kuzu.Database(str(Path(self.db_path) / "db"))
                self._conn = kuzu.Connection(self._db)
            except ImportError as e:
                logger.error(f"Kuzu no disponible: {e}")
                raise
        return self._conn
    
    def add_entity(self, name: str, entity_type: str, 
                   source_doc: str, validated: bool = False) -> bool:
        """
        Agregar nodo de entidad al grafo.
        
        Args:
            name: Nombre de la entidad
            entity_type: Tipo de entidad (function, class, concept, etc.)
            source_doc: Documento fuente
            validated: Si la entidad está validada
            
        Returns:
            True si se agregó exitosamente
        """
        try:
            conn = self._get_connection()
            # Usar MERGE para evitar duplicados (upsert de Cypher)
            query = """
                MERGE (e:Entity {name: $name})
                SET e.type = $type,
                    e.source_doc = $source_doc,
                    e.validated = $validated
                RETURN count(e)
            """
            params = {
                'name': name,
                'type': entity_type,
                'source_doc': source_doc,
                'validated': validated
            }
            result = conn.execute(query, params)
            return result.has_next()
        except Exception as e:
            # Puede fallar si la entidad ya existe (PRIMARY KEY)
            logger.debug(f"Entidad ya existe o error: {e}")
            return False
    
    def add_relation(self, subject: str, relation: str, 
                     object_: str, **properties) -> bool:
        """
        Agregar relación entre entidades.
        
        Usa MATCH para encontrar los nodos y CREATE para la relación.
        
        Args:
            subject: Entidad sujeto
            relation: Tipo de relación (REQUIRES, RELATES_TO, PART_OF)
            object_: Entidad objeto
            properties: Propiedades adicionales de relación
            
        Returns:
            True si se agregó exitosamente
        """
        try:
            conn = self._get_connection()
            
            # Mapear tablas
            rel_table = relation.upper()
            if rel_table not in ['REQUIRES', 'RELATES_TO', 'PART_OF']:
                rel_table = 'RELATES_TO'

            # Construir query según la tabla
            if rel_table == 'REQUIRES':
                query = """
                    MATCH (a:Entity {name: $subject}), (b:Entity {name: $object})
                    CREATE (a)-[:REQUIRES {
                        weight: $weight,
                        criticality: $criticality,
                        validated: $validated
                    }]->(b)
                """
                params = {
                    'subject': subject,
                    'object': object_,
                    'weight': float(properties.get('weight', 1.0)),
                    'criticality': str(properties.get('criticality', 'C2')),
                    'validated': bool(properties.get('validated', False))
                }
            elif rel_table == 'RELATES_TO':
                query = """
                    MATCH (a:Entity {name: $subject}), (b:Entity {name: $object})
                    CREATE (a)-[:RELATES_TO {
                        relation_type: $relation_type,
                        confidence: $confidence,
                        context: $context
                    }]->(b)
                """
                params = {
                    'subject': subject,
                    'object': object_,
                    'relation_type': str(properties.get('relation_type', 'related')),
                    'confidence': float(properties.get('confidence', 0.8)),
                    'context': str(properties.get('context', ''))
                }
            elif rel_table == 'PART_OF':
                query = """
                    MATCH (a:Entity {name: $subject}), (b:Entity {name: $object})
                    CREATE (a)-[:PART_OF {
                        order_idx: $order_idx
                    }]->(b)
                """
                params = {
                    'subject': subject,
                    'object': object_,
                    'order_idx': float(properties.get('order_idx', 0.0))
                }

            conn.execute(query, params)
            return True
            
        except Exception as e:
            logger.debug(f"Error agregando relación {subject} -> {object}: {e}")
            return False
    
    def process_entities(self, entities: List[Dict[str, Any]], 
                        source_doc: str) -> Dict[str, Any]:
        """
        Procesar lista de entidades y agregarlas al grafo.
        
        Args:
            entities: Lista de entidades (formato del ingestor)
            source_doc: Documento fuente
            
        Returns:
            Estadísticas del procesamiento
        """
        stats = {
            'added': 0,
            'skipped': 0,
            'errors': 0
        }
        
        for entity in entities:
            try:
                name = entity.get('name', '')
                entity_type = entity.get('entity_type', 'concept')
                
                if not name:
                    stats['skipped'] += 1
                    continue
                
                success = self.add_entity(
                    name=name,
                    entity_type=entity_type,
                    source_doc=source_doc,
                    validated=False  # Nuevo, requiere validación
                )
                
                if success:
                    stats['added'] += 1
                else:
                    stats['skipped'] += 1
                    
            except Exception as e:
                logger.error(f"Error procesando entidad {entity}: {e}")
                stats['errors'] += 1
        
        return stats
    
    def extract_and_link_entities(self, processed_doc) -> Dict[str, Any]:
        """
        Extraer entidades de un documento procesado y crear relaciones.
        
        Args:
            processed_doc: Documento procesado (ProcessedDocument)
            
        Returns:
            Estadísticas del procesamiento
        """
        stats = {
            'entities': {'added': 0, 'skipped': 0, 'errors': 0},
            'relations': {'added': 0, 'skipped': 0, 'errors': 0}
        }
        
        # Agregar entidades
        if processed_doc.entities:
            stats['entities'] = self.process_entities(
                processed_doc.entities,
                processed_doc.doc_id
            )
        
        # Crear relaciones implícitas entre entidades del mismo documento
        if processed_doc.entities and len(processed_doc.entities) > 1:
            # Relacionar entidades consecutivas (RELATES_TO)
            for i in range(len(processed_doc.entities) - 1):
                ent1 = processed_doc.entities[i]
                ent2 = processed_doc.entities[i + 1]
                
                if ent1.get('name') and ent2.get('name'):
                    success = self.add_relation(
                        subject=ent1['name'],
                        relation='RELATES_TO',
                        object_=ent2['name'],
                        relation_type='co_occur',
                        confidence=0.7,
                        context=f"Both in {processed_doc.title}"
                    )
                    
                    if success:
                        stats['relations']['added'] += 1
                    else:
                        stats['relations']['skipped'] += 1
        
        return stats
    
    def query_neighborhood(self, entity_name: str, 
                          max_hops: int = 2) -> List[Dict[str, Any]]:
        """
        Consultar vecindario de una entidad.
        
        Args:
            entity_name: Nombre de la entidad centro
            max_hops: Máximo número de saltos
            
        Returns:
            Lista de nodos y relaciones en el vecindario
        """
        try:
            conn = self._get_connection()
            
            # Query simplificada para Kuzu
            query = """
                MATCH (center:Entity)-[r*1..2]-(neighbor:Entity)
                WHERE center.name = ?
                RETURN center.name, type(r), neighbor.name, neighbor.type
                LIMIT 50
            """
            
            result = conn.execute(query, [entity_name])
            neighborhood = []
            
            while result.has_next():
                row = result.get_next()
                neighborhood.append({
                    'center': row[0],
                    'relation': row[1],
                    'neighbor': row[2],
                    'neighbor_type': row[3]
                })
            
            return neighborhood
            
        except Exception as e:
            logger.error(f"Error consultando vecindario: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del grafo."""
        try:
            conn = self._get_connection()
            
            stats = {}
            
            # Contar nodos
            result = conn.execute("MATCH (n:Entity) RETURN count(n) as count")
            if result.has_next():
                stats['nodes'] = result.get_next()[0]
            else:
                stats['nodes'] = 0
            
            # Contar relaciones por tipo
            for rel_type in ['REQUIRES', 'RELATES_TO', 'PART_OF']:
                try:
                    query = f"MATCH (a)-[r:{rel_type}]->(b) RETURN count(r) as count"
                    result = conn.execute(query)
                    if result.has_next():
                        stats[f'relations_{rel_type.lower()}'] = result.get_next()[0]
                    else:
                        stats[f'relations_{rel_type.lower()}'] = 0
                except Exception:
                    stats[f'relations_{rel_type.lower()}'] = 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {'nodes': 0, 'relations': 0}
    
    def close(self):
        """Cerrar conexión a la base de datos."""
        if self._conn:
            self._conn.close()
            self._conn = None
        if self._db:
            self._db.close()
            self._db = None

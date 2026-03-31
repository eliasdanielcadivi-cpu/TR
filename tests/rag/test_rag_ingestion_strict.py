#!/usr/bin/env python3
"""
Prueba Headless de Ingesta RAG - Análisis Riguroso Multi-Perspectiva

Propósito: Verificar la ingesta de documentos con análisis profundo de datos reales
desde múltiples perspectivas para evitar alucinaciones.

Métodos de verificación:
1. Verificación directa de datos en las 3 bases de datos
2. Verificación de integridad referencial
3. Verificación de contenido de chunks
4. Verificación de entidades extraídas
5. Verificación de embeddings (si Ollama disponible)

Uso:
    cd /home/daniel/tron/programas/TR
    python tests/rag/test_rag_ingestion_strict.py
"""

import os
import sys
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime

# Añadir ruta del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
os.environ['TR_PROJECT_ROOT'] = str(project_root)


@dataclass
class VerificationResult:
    """Resultado de una verificación."""
    test_name: str
    passed: bool
    data_points: Dict[str, Any]
    raw_data: Any
    errors: List[str]
    warnings: List[str]


class RAGIngestionVerifier:
    """Verificador riguroso de ingesta RAG."""
    
    def __init__(self):
        self.db_root = project_root / "db/rag"
        self.results: List[VerificationResult] = []
        
    def verify_all(self) -> bool:
        """Ejecutar todas las verificaciones."""
        print("\n" + "="*80)
        print("🔍 VERIFICACIÓN RIGUROSA DE INGESTA RAG")
        print("="*80)
        print(f"📁 DB Root: {self.db_root}")
        print(f"🕐 Timestamp: {datetime.now().isoformat()}")
        
        # Verificaciones en orden
        self.verify_db_existence()
        self.verify_core_documents()
        self.verify_core_chunks()
        self.verify_core_entities()
        self.verify_vector_embeddings()
        self.verify_graph_nodes()
        self.verify_referential_integrity()
        self.verify_content_samples()
        
        # Resumen
        self.print_summary()
        
        return all(r.passed for r in self.results)
    
    def verify_db_existence(self):
        """Verificación 1: Existencia de archivos de base de datos."""
        print("\n" + "-"*80)
        print("📊 VERIFICACIÓN 1: Existencia de Bases de Datos")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        
        # Core SQLite
        core_db = self.db_root / "rag_core.sqlite"
        core_exists = core_db.exists()
        core_size = core_db.stat().st_size if core_exists else 0
        data['core_db'] = {'exists': core_exists, 'size_bytes': core_size}
        
        if not core_exists:
            errors.append(f"❌ rag_core.sqlite no existe")
        elif core_size == 0:
            errors.append(f"❌ rag_core.sqlite está vacío (0 bytes)")
        else:
            print(f"✅ rag_core.sqlite: {core_size:,} bytes")
        
        # Vector SQLite
        vec_db = self.db_root / "rag_vectors.sqlite"
        vec_exists = vec_db.exists()
        vec_size = vec_db.stat().st_size if vec_exists else 0
        data['vector_db'] = {'exists': vec_exists, 'size_bytes': vec_size}
        
        if not vec_exists:
            errors.append(f"❌ rag_vectors.sqlite no existe")
        elif vec_size == 0:
            errors.append(f"❌ rag_vectors.sqlite está vacío (0 bytes)")
        else:
            print(f"✅ rag_vectors.sqlite: {vec_size:,} bytes")
        
        # Graph Kuzu
        graph_dir = self.db_root / "rag_graph.kuzu"
        graph_exists = graph_dir.exists()
        graph_files = list(graph_dir.glob("*")) if graph_exists else []
        data['graph_db'] = {'exists': graph_exists, 'files': len(graph_files)}
        
        if not graph_exists:
            errors.append(f"❌ rag_graph.kuzu no existe")
        else:
            print(f"✅ rag_graph.kuzu: {len(graph_files)} archivos")
            for f in graph_files[:5]:
                print(f"   - {f.name}: {f.stat().st_size:,} bytes")
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="DB_Existence",
            passed=passed,
            data_points=data,
            raw_data={'files': [str(f) for f in graph_files]},
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(err)
    
    def verify_core_documents(self):
        """Verificación 2: Documentos en SQLite core."""
        print("\n" + "-"*80)
        print("📄 VERIFICACIÓN 2: Documentos en SQLite Core")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        raw_docs = []
        
        core_db = self.db_root / "rag_core.sqlite"
        if not core_db.exists():
            errors.append("Base de datos core no existe")
            self.results.append(VerificationResult(
                test_name="Core_Documents",
                passed=False,
                data_points={},
                raw_data=[],
                errors=errors,
                warnings=warnings
            ))
            return
        
        conn = sqlite3.connect(str(core_db))
        
        try:
            # Contar documentos
            cursor = conn.execute("SELECT COUNT(*) FROM documents")
            doc_count = cursor.fetchone()[0]
            data['document_count'] = doc_count
            print(f"📊 Total documentos: {doc_count}")
            
            if doc_count == 0:
                warnings.append("⚠️  No hay documentos indexados")
            
            # Obtener todos los documentos
            cursor = conn.execute("""
                SELECT doc_id, source_path, doc_type, title, summary, 
                       chunk_count, last_indexed, validation_status
                FROM documents
                ORDER BY last_indexed DESC
            """)
            
            docs = cursor.fetchall()
            for doc in docs:
                doc_data = {
                    'doc_id': doc[0],
                    'source_path': doc[1],
                    'doc_type': doc[2],
                    'title': doc[3],
                    'summary': doc[4],
                    'chunk_count': doc[5],
                    'last_indexed': doc[6],
                    'validation_status': doc[7]
                }
                raw_docs.append(doc_data)
                
                print(f"\n📄 Documento:")
                print(f"   - ID: {doc[0][:32]}...")
                print(f"   - Ruta: {doc[1]}")
                print(f"   - Tipo: {doc[2]}")
                print(f"   - Título: {doc[3]}")
                print(f"   - Chunks: {doc[5]}")
                print(f"   - Indexado: {doc[6]}")
                print(f"   - Estado: {doc[7]}")
                
                # Verificar integridad del documento
                if not doc[0]:
                    errors.append(f"Documento sin doc_id")
                if not doc[1]:
                    errors.append(f"Documento sin source_path")
                if not doc[5] or doc[5] == 0:
                    warnings.append(f"Documento sin chunks: {doc[3]}")
            
            data['documents'] = raw_docs
            
        except Exception as e:
            errors.append(f"Error consultando documentos: {e}")
        finally:
            conn.close()
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="Core_Documents",
            passed=passed,
            data_points=data,
            raw_data=raw_docs,
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(f"❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"⚠️  {warn}")
    
    def verify_core_chunks(self):
        """Verificación 3: Chunks en SQLite core."""
        print("\n" + "-"*80)
        print("🧩 VERIFICACIÓN 3: Chunks en SQLite Core")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        raw_chunks = []
        
        core_db = self.db_root / "rag_core.sqlite"
        if not core_db.exists():
            errors.append("Base de datos core no existe")
            self.results.append(VerificationResult(
                test_name="Core_Chunks",
                passed=False,
                data_points={},
                raw_data=[],
                errors=errors,
                warnings=warnings
            ))
            return
        
        conn = sqlite3.connect(str(core_db))
        
        try:
            # Contar chunks
            cursor = conn.execute("SELECT COUNT(*) FROM chunks")
            chunk_count = cursor.fetchone()[0]
            data['chunk_count'] = chunk_count
            print(f"📊 Total chunks: {chunk_count}")
            
            if chunk_count == 0:
                warnings.append("⚠️  No hay chunks indexados")
            
            # Obtener chunks por documento
            cursor = conn.execute("""
                SELECT c.doc_id, COUNT(*) as chunk_count,
                       MIN(c.start_line) as first_line,
                       MAX(c.end_line) as last_line,
                       SUM(c.char_count) as total_chars
                FROM chunks c
                GROUP BY c.doc_id
            """)
            
            chunks_by_doc = cursor.fetchall()
            for row in chunks_by_doc:
                print(f"\n📄 Doc {row[0][:16]}...:")
                print(f"   - Chunks: {row[1]}")
                print(f"   - Líneas: {row[2]}-{row[3]}")
                print(f"   - Caracteres: {row[4]:,}")
                
                raw_chunks.append({
                    'doc_id': row[0],
                    'chunk_count': row[1],
                    'first_line': row[2],
                    'last_line': row[3],
                    'total_chars': row[4]
                })
            
            # Verificar chunks huérfanos
            cursor = conn.execute("""
                SELECT COUNT(*) FROM chunks c
                LEFT JOIN documents d ON c.doc_id = d.doc_id
                WHERE d.doc_id IS NULL
            """)
            orphan_chunks = cursor.fetchone()[0]
            data['orphan_chunks'] = orphan_chunks
            
            if orphan_chunks > 0:
                errors.append(f"❌ {orphan_chunks} chunks huérfanos encontrados")
            else:
                print(f"\n✅ No hay chunks huérfanos")
            
            # Mostrar muestra de contenido de chunks
            cursor = conn.execute("""
                SELECT c.id, c.content, c.start_line, c.end_line
                FROM chunks c
                LIMIT 3
            """)
            
            samples = cursor.fetchall()
            if samples:
                print(f"\n📝 Muestra de contenido (primeros 3 chunks):")
                for i, chunk in enumerate(samples):
                    chunk_id = chunk[0]
                    content = chunk[1]
                    start_line = chunk[2]
                    end_line = chunk[3]
                    
                    content_preview = content[:200].replace('\n', ' ')
                    print(f"\n   Chunk {i+1}:")
                    print(f"   - ID: {chunk_id}")
                    print(f"   - Líneas: {start_line}-{end_line}")
                    print(f"   - Preview: {content_preview}...")
                    
                    # Verificar que el contenido no esté vacío
                    if not content or len(content.strip()) == 0:
                        errors.append(f"Chunk {chunk_id} tiene contenido vacío")
            
            data['chunk_samples'] = [{'id': s[0], 'content': s[1]} for s in samples]
            
        except Exception as e:
            errors.append(f"Error consultando chunks: {e}")
        finally:
            conn.close()
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="Core_Chunks",
            passed=passed,
            data_points=data,
            raw_data=raw_chunks,
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(f"❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"⚠️  {warn}")
    
    def verify_core_entities(self):
        """Verificación 4: Entidades en SQLite core."""
        print("\n" + "-"*80)
        print("🏷️  VERIFICACIÓN 4: Entidades Extraídas")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        raw_entities = []
        
        core_db = self.db_root / "rag_core.sqlite"
        if not core_db.exists():
            errors.append("Base de datos core no existe")
            self.results.append(VerificationResult(
                test_name="Core_Entities",
                passed=False,
                data_points={},
                raw_data=[],
                errors=errors,
                warnings=warnings
            ))
            return
        
        conn = sqlite3.connect(str(core_db))
        
        try:
            # Contar entidades
            cursor = conn.execute("SELECT COUNT(*) FROM entities")
            entity_count = cursor.fetchone()[0]
            data['entity_count'] = entity_count
            print(f"📊 Total entidades: {entity_count}")
            
            if entity_count == 0:
                warnings.append("⚠️  No hay entidades extraídas")
            
            # Obtener entidades por tipo
            cursor = conn.execute("""
                SELECT entity_type, COUNT(*) as count
                FROM entities
                GROUP BY entity_type
            """)
            
            by_type = cursor.fetchall()
            data['by_type'] = {}
            for row in by_type:
                print(f"   - {row[0]}: {row[1]}")
                data['by_type'][row[0]] = row[1]
            
            # Obtener muestra de entidades
            cursor = conn.execute("""
                SELECT name, entity_type, source_doc_id, confidence
                FROM entities
                LIMIT 20
            """)
            
            entities = cursor.fetchall()
            for row in entities:
                print(f"   • {row[0]} ({row[1]}) - conf: {row[3]}")
                raw_entities.append({
                    'name': row[0],
                    'type': row[1],
                    'source': row[2],
                    'confidence': row[3]
                })
            
            # Verificar entidades sin nombre
            cursor = conn.execute("""
                SELECT COUNT(*) FROM entities
                WHERE name IS NULL OR name = ''
            """)
            empty_names = cursor.fetchone()[0]
            
            if empty_names > 0:
                errors.append(f"❌ {empty_names} entidades sin nombre")
            
            data['empty_names'] = empty_names
            
        except Exception as e:
            errors.append(f"Error consultando entidades: {e}")
        finally:
            conn.close()
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="Core_Entities",
            passed=passed,
            data_points=data,
            raw_data=raw_entities,
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(f"❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"⚠️  {warn}")
    
    def verify_vector_embeddings(self):
        """Verificación 5: Embeddings en SQLite vec."""
        print("\n" + "-"*80)
        print("🔢 VERIFICACIÓN 5: Embeddings Vectoriales")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        raw_data = {}
        
        vec_db = self.db_root / "rag_vectors.sqlite"
        if not vec_db.exists():
            errors.append("Base de datos vector no existe")
            self.results.append(VerificationResult(
                test_name="Vector_Embeddings",
                passed=False,
                data_points={},
                raw_data={},
                errors=errors,
                warnings=warnings
            ))
            return
        
        try:
            import sqlite_vec
        except ImportError as e:
            errors.append(f"sqlite-vec no instalado: {e}")
            self.results.append(VerificationResult(
                test_name="Vector_Embeddings",
                passed=False,
                data_points={},
                raw_data={},
                errors=errors,
                warnings=warnings
            ))
            return
        
        conn = sqlite3.connect(str(vec_db))
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        
        try:
            # Contar embeddings
            cursor = conn.execute("SELECT COUNT(*) FROM embeddings")
            emb_count = cursor.fetchone()[0]
            data['embedding_count'] = emb_count
            print(f"📊 Total embeddings: {emb_count}")
            
            if emb_count == 0:
                warnings.append("⚠️  No hay embeddings almacenados")
                print("\n⚠️  Posibles causas:")
                print("   - Ollama no está disponible")
                print("   - Error generando embeddings")
                print("   - Ingesta no completó fase de embeddings")
            
            # Verificar dimensionalidad
            if emb_count > 0:
                cursor = conn.execute("SELECT embedding FROM embeddings LIMIT 1")
                row = cursor.fetchone()
                if row and row[0]:
                    blob_size = len(row[0])
                    dimensions = blob_size // 4  # float32 = 4 bytes
                    data['embedding_dimensions'] = dimensions
                    data['blob_size'] = blob_size
                    print(f"\n📏 Dimensiones: {dimensions}")
                    print(f"📏 Tamaño BLOB: {blob_size} bytes")
                    
                    # Verificar dimensiones esperadas (768 para nomic-embed-text)
                    if dimensions not in [384, 512, 768, 1024]:
                        warnings.append(f"Dimensiones inusuales: {dimensions}")
            
            # Verificar embeddings huérfanos (solo si hay embeddings)
            if emb_count > 0:
                try:
                    cursor = conn.execute("""
                        SELECT COUNT(*) FROM embeddings e
                        LEFT JOIN documents d ON e.doc_id = d.doc_id
                        WHERE d.doc_id IS NULL
                    """)
                    orphan_embs = cursor.fetchone()[0]
                    data['orphan_embeddings'] = orphan_embs
                    
                    if orphan_embs > 0:
                        errors.append(f"❌ {orphan_embs} embeddings huérfanos")
                    else:
                        print(f"\n✅ No hay embeddings huérfanos")
                except sqlite3.OperationalError:
                    # La tabla documents no existe en esta DB
                    data['orphan_embeddings'] = 'N/A'
                    warnings.append("⚠️  No se puede verificar integridad referencial (documents no existe en esta DB)")
            else:
                data['orphan_embeddings'] = 0
            
        except Exception as e:
            errors.append(f"Error verificando embeddings: {e}")
            import traceback
            traceback.print_exc()
        finally:
            conn.close()
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="Vector_Embeddings",
            passed=passed,
            data_points=data,
            raw_data=raw_data,
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(f"❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"⚠️  {warn}")
    
    def verify_graph_nodes(self):
        """Verificación 6: Nodos en grafo Kùzu."""
        print("\n" + "-"*80)
        print("🕸️  VERIFICACIÓN 6: Grafo de Conocimiento (Kùzu)")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        raw_data = {'nodes': [], 'relations': []}
        
        graph_dir = self.db_root / "rag_graph.kuzu"
        if not graph_dir.exists():
            errors.append("Directorio graph no existe")
            self.results.append(VerificationResult(
                test_name="Graph_Nodes",
                passed=False,
                data_points={},
                raw_data={},
                errors=errors,
                warnings=warnings
            ))
            return
        
        try:
            import kuzu
        except ImportError as e:
            errors.append(f"Kuzu no instalado: {e}")
            self.results.append(VerificationResult(
                test_name="Graph_Nodes",
                passed=False,
                data_points={},
                raw_data={},
                errors=errors,
                warnings=warnings
            ))
            return
        
        try:
            db = kuzu.Database(str(graph_dir / "db"))
            conn = kuzu.Connection(db)
            
            # Contar nodos Entity
            result = conn.execute("MATCH (n:Entity) RETURN count(n) as count")
            if result.has_next():
                node_count = result.get_next()[0]
                data['node_count'] = node_count
                print(f"📊 Total nodos Entity: {node_count}")
                
                if node_count == 0:
                    warnings.append("⚠️  No hay nodos en el grafo")
            else:
                data['node_count'] = 0
                warnings.append("⚠️  No se pudo contar nodos")
            
            # Mostrar muestra de nodos
            result = conn.execute("MATCH (n:Entity) RETURN n.name, n.type LIMIT 20")
            nodes = []
            while result.has_next():
                row = result.get_next()
                nodes.append({'name': row[0], 'type': row[1]})
                print(f"   • {row[0]} ({row[1]})")
            
            raw_data['nodes'] = nodes
            
            # Contar relaciones por tipo
            for rel_type in ['REQUIRES', 'RELATES_TO', 'PART_OF']:
                try:
                    query = f"MATCH (a)-[r:{rel_type}]->(b) RETURN count(r) as count"
                    result = conn.execute(query)
                    if result.has_next():
                        rel_count = result.get_next()[0]
                        data[f'relations_{rel_type.lower()}'] = rel_count
                        print(f"   - {rel_type}: {rel_count}")
                except Exception:
                    data[f'relations_{rel_type.lower()}'] = 0
            
            conn.close()
            
        except Exception as e:
            errors.append(f"Error verificando grafo: {e}")
            import traceback
            traceback.print_exc()
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="Graph_Nodes",
            passed=passed,
            data_points=data,
            raw_data=raw_data,
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(f"❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"⚠️  {warn}")
    
    def verify_referential_integrity(self):
        """Verificación 7: Integridad referencial."""
        print("\n" + "-"*80)
        print("🔗 VERIFICACIÓN 7: Integridad Referencial")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        
        core_db = self.db_root / "rag_core.sqlite"
        if not core_db.exists():
            errors.append("Base de datos core no existe")
            self.results.append(VerificationResult(
                test_name="Referential_Integrity",
                passed=False,
                data_points={},
                raw_data={},
                errors=errors,
                warnings=warnings
            ))
            return
        
        conn = sqlite3.connect(str(core_db))
        
        try:
            # Chunks sin documento padre
            cursor = conn.execute("""
                SELECT COUNT(*) FROM chunks c
                LEFT JOIN documents d ON c.doc_id = d.doc_id
                WHERE d.doc_id IS NULL
            """)
            orphan_chunks = cursor.fetchone()[0]
            data['orphan_chunks'] = orphan_chunks
            print(f"📊 Chunks huérfanos: {orphan_chunks}")
            if orphan_chunks > 0:
                errors.append(f"❌ {orphan_chunks} chunks sin documento padre")
            
            # Entidades sin documento padre
            cursor = conn.execute("""
                SELECT COUNT(*) FROM entities e
                LEFT JOIN documents d ON e.source_doc_id = d.doc_id
                WHERE d.doc_id IS NULL
            """)
            orphan_entities = cursor.fetchone()[0]
            data['orphan_entities'] = orphan_entities
            print(f"📊 Entidades huérfanas: {orphan_entities}")
            if orphan_entities > 0:
                errors.append(f"❌ {orphan_entities} entidades sin documento padre")
            
            # Documentos sin chunks
            cursor = conn.execute("""
                SELECT COUNT(*) FROM documents d
                LEFT JOIN chunks c ON d.doc_id = c.doc_id
                WHERE c.doc_id IS NULL
            """)
            docs_without_chunks = cursor.fetchone()[0]
            data['docs_without_chunks'] = docs_without_chunks
            print(f"📊 Documentos sin chunks: {docs_without_chunks}")
            if docs_without_chunks > 0:
                warnings.append(f"⚠️  {docs_without_chunks} documentos sin chunks")
            
            if len(errors) == 0:
                print("\n✅ Integridad referencial correcta")
            
        except Exception as e:
            errors.append(f"Error verificando integridad: {e}")
        finally:
            conn.close()
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="Referential_Integrity",
            passed=passed,
            data_points=data,
            raw_data={},
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(f"❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"⚠️  {warn}")
    
    def verify_content_samples(self):
        """Verificación 8: Muestras de contenido."""
        print("\n" + "-"*80)
        print("📝 VERIFICACIÓN 8: Muestras de Contenido")
        print("-"*80)
        
        errors = []
        warnings = []
        data = {}
        raw_samples = []
        
        core_db = self.db_root / "rag_core.sqlite"
        if not core_db.exists():
            errors.append("Base de datos core no existe")
            self.results.append(VerificationResult(
                test_name="Content_Samples",
                passed=False,
                data_points={},
                raw_data=[],
                errors=errors,
                warnings=warnings
            ))
            return
        
        conn = sqlite3.connect(str(core_db))
        
        try:
            # Obtener muestra de chunks con su documento
            cursor = conn.execute("""
                SELECT d.title, c.id, c.content, c.start_line, c.end_line
                FROM chunks c
                JOIN documents d ON c.doc_id = d.doc_id
                ORDER BY RANDOM()
                LIMIT 3
            """)
            
            samples = cursor.fetchall()
            
            if not samples:
                warnings.append("⚠️  No hay muestras para mostrar")
            else:
                print(f"\n📊 Muestra aleatoria de {len(samples)} chunks:")
                
                for i, chunk in enumerate(samples):
                    title = chunk[0]
                    chunk_id = chunk[1]
                    content = chunk[2]
                    start_line = chunk[3]
                    end_line = chunk[4]
                    
                    # Análisis del contenido
                    char_count = len(content)
                    word_count = len(content.split())
                    line_count = content.count('\n') + 1
                    
                    print(f"\n   Muestra {i+1}:")
                    print(f"   - Documento: {title}")
                    print(f"   - Chunk ID: {chunk_id}")
                    print(f"   - Líneas: {start_line}-{end_line}")
                    print(f"   - Caracteres: {char_count:,}")
                    print(f"   - Palabras: {word_count:,}")
                    print(f"   - Líneas contenido: {line_count}")
                    
                    # Verificar contenido
                    if char_count < 50:
                        warnings.append(f"Chunk muy corto ({char_count} chars)")
                    
                    if not content.strip():
                        errors.append(f"Chunk vacío")
                    
                    # Mostrar preview
                    preview = content[:300].replace('\n', '\\n')
                    print(f"   - Preview: {preview}...")
                    
                    raw_samples.append({
                        'title': title,
                        'chunk_id': chunk_id,
                        'content': content,
                        'char_count': char_count,
                        'word_count': word_count
                    })
            
            data['samples'] = raw_samples
            
        except Exception as e:
            errors.append(f"Error obteniendo muestras: {e}")
        finally:
            conn.close()
        
        passed = len(errors) == 0
        
        self.results.append(VerificationResult(
            test_name="Content_Samples",
            passed=passed,
            data_points=data,
            raw_data=raw_samples,
            errors=errors,
            warnings=warnings
        ))
        
        if errors:
            for err in errors:
                print(f"❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"⚠️  {warn}")
    
    def print_summary(self):
        """Imprimir resumen final."""
        print("\n" + "="*80)
        print("📊 RESUMEN DE VERIFICACIÓN")
        print("="*80)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print(f"\n📈 Resultados: {passed}/{total} verificaciones exitosas")
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"   {status}: {result.test_name}")
        
        # Errores totales
        total_errors = sum(len(r.errors) for r in self.results)
        total_warnings = sum(len(r.warnings) for r in self.results)
        
        print(f"\n❌ Errores: {total_errors}")
        print(f"⚠️  Advertencias: {total_warnings}")
        
        if failed == 0:
            print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        else:
            print(f"\n⚠️  {failed} verificación(es) fallaron")


def main():
    """Función principal."""
    print("="*80)
    print("🧪 PRUEBA HEADLESS DE INGESTA RAG - VERIFICACIÓN RIGUROSA")
    print("="*80)
    
    verifier = RAGIngestionVerifier()
    success = verifier.verify_all()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

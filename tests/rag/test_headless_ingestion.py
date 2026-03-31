#!/usr/bin/env python3
"""
Prueba headless de ingesta RAG - Sistema V3

Propósito: Probar la ingesta de documentos sin interfaz interactiva
para el comando 'ares p --rag'

Uso:
    cd /home/daniel/tron/programas/TR
    python tests/rag/test_headless_ingestion.py
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('rag_test')

# Añadir ruta del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Establecer variable de entorno
os.environ['TR_PROJECT_ROOT'] = str(project_root)


def test_file_ingestor_basic():
    """Prueba 1: FileIngestor básico"""
    print("\n" + "="*80)
    print("🧪 PRUEBA 1: FileIngestor Básico")
    print("="*80)
    
    from modules.rag.ingestors.file_ingestor import FileIngestor
    
    # Documento de prueba
    test_doc = project_root / "docs/ArquitecturadeModulosOrientadaaIA/ArquitecturadeMódulosOrientadaaIA.md"
    
    if not test_doc.exists():
        print(f"❌ Documento no encontrado: {test_doc}")
        return False
    
    print(f"📄 Documento: {test_doc}")
    print(f"📏 Tamaño: {test_doc.stat().st_size} bytes")
    
    # Crear ingestor
    ingestor = FileIngestor(chunk_size=1000, chunk_overlap=200)
    
    # Verificar que puede procesar el archivo
    if not ingestor.can_process(str(test_doc)):
        print(f"❌ El ingestor no puede procesar este archivo")
        return False
    
    print("✅ El ingestor puede procesar este archivo")
    
    # Procesar documento
    try:
        processed = ingestor.process(str(test_doc))
        
        print(f"\n📊 Resultados del procesamiento:")
        print(f"   - Doc ID: {processed.doc_id[:16]}...")
        print(f"   - Tipo: {processed.doc_type}")
        print(f"   - Título: {processed.title}")
        print(f"   - Chunks: {processed.total_chunks}")
        print(f"   - Entidades: {len(processed.entities) if processed.entities else 0}")
        
        if processed.processing_errors:
            print(f"   - Errores: {len(processed.processing_errors)}")
            for err in processed.processing_errors:
                print(f"     ⚠️  {err}")
        
        # Mostrar primeros chunks
        print(f"\n📝 Primeros 3 chunks:")
        for i, chunk in enumerate(processed.chunks[:3]):
            print(f"\n   Chunk {i}:")
            print(f"   - ID: {chunk.chunk_id[:24]}...")
            print(f"   - Líneas: {chunk.start_line}-{chunk.end_line}")
            print(f"   - Caracteres: {chunk.char_count}")
            print(f"   - Preview: {chunk.content[:100]}...")
        
        print("\n✅ PRUEBA 1: EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ PRUEBA 1: FALLIDA - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_orchestrator_ingestion():
    """Prueba 2: RAGOrchestrator - Ingesta completa"""
    print("\n" + "="*80)
    print("🧪 PRUEBA 2: RAGOrchestrator - Ingesta Completa")
    print("="*80)
    
    from modules.rag.core.rag_orchestrator import RAGOrchestrator
    
    # Documento de prueba
    test_doc = project_root / "docs/ArquitecturadeModulosOrientadaaIA/ArquitecturadeMódulosOrientadaaIA.md"
    
    if not test_doc.exists():
        print(f"❌ Documento no encontrado: {test_doc}")
        return False
    
    # Crear orquestador
    try:
        print("🔧 Inicializando RAGOrchestrator...")
        rag = RAGOrchestrator()
        print("✅ RAGOrchestrator inicializado")
        
        # Ingerir documento
        print(f"\n📥 Ingestando documento: {test_doc}")
        result = rag.ingest_document(str(test_doc))
        
        print(f"\n📊 Resultados de ingesta:")
        for key, value in result.items():
            print(f"   - {key}: {value}")
        
        print("\n✅ PRUEBA 2: EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ PRUEBA 2: FALLIDA - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sqlite_storage():
    """Prueba 3: Verificar almacenamiento en SQLite"""
    print("\n" + "="*80)
    print("🧪 PRUEBA 3: Verificar Almacenamiento en SQLite")
    print("="*80)
    
    import sqlite3
    
    db_path = project_root / "db/rag/rag_core.sqlite"
    
    if not db_path.exists():
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    print(f"📊 Conectando a: {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Contar documentos
        cursor = conn.execute("SELECT COUNT(*) as count FROM documents")
        doc_count = cursor.fetchone()[0]
        print(f"   - Documentos indexados: {doc_count}")
        
        # Contar chunks
        cursor = conn.execute("SELECT COUNT(*) as count FROM chunks")
        chunk_count = cursor.fetchone()[0]
        print(f"   - Chunks almacenados: {chunk_count}")
        
        # Contar entidades
        cursor = conn.execute("SELECT COUNT(*) as count FROM entities")
        entity_count = cursor.fetchone()[0]
        print(f"   - Entidades extraídas: {entity_count}")
        
        # Mostrar último documento
        if doc_count > 0:
            cursor = conn.execute("""
                SELECT doc_id, source_path, doc_type, title, chunk_count 
                FROM documents 
                ORDER BY last_indexed DESC 
                LIMIT 1
            """)
            doc = cursor.fetchone()
            print(f"\n   📄 Último documento:")
            print(f"      - ID: {doc[0][:16]}...")
            print(f"      - Ruta: {doc[1]}")
            print(f"      - Tipo: {doc[2]}")
            print(f"      - Título: {doc[3]}")
            print(f"      - Chunks: {doc[4]}")
        
        # Verificar chunks del último documento
        if doc_count > 0:
            cursor = conn.execute("""
                SELECT chunk_id, chunk_index, start_line, end_line, char_count
                FROM chunks
                WHERE doc_id = (SELECT doc_id FROM documents ORDER BY last_indexed DESC LIMIT 1)
                LIMIT 5
            """)
            chunks = cursor.fetchall()
            if chunks:
                print(f"\n   📝 Primeros {len(chunks)} chunks:")
                for chunk in chunks:
                    print(f"      - {chunk[0][:24]}... (líneas {chunk[2]}-{chunk[3]}, {chunk[4]} chars)")
        
        conn.close()
        
        if doc_count > 0:
            print("\n✅ PRUEBA 3: EXITOSA")
            return True
        else:
            print("\n⚠️  PRUEBA 3: BASE DE DATOS VACÍA")
            return False
        
    except Exception as e:
        print(f"\n❌ PRUEBA 3: FALLIDA - {e}")
        import traceback
        traceback.print_exc()
        conn.close()
        return False


def test_vector_embeddings():
    """Prueba 4: Verificar embeddings en sqlite-vec"""
    print("\n" + "="*80)
    print("🧪 PRUEBA 4: Verificar Embeddings Vectoriales")
    print("="*80)
    
    try:
        import sqlite3
        import sqlite_vec
    except ImportError as e:
        print(f"❌ sqlite-vec no disponible: {e}")
        return False
    
    db_path = project_root / "db/rag/rag_vectors.sqlite"
    
    if not db_path.exists():
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    print(f"📊 Conectando a: {db_path}")
    
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    
    try:
        # Contar embeddings
        cursor = conn.execute("SELECT COUNT(*) FROM embeddings")
        emb_count = cursor.fetchone()[0]
        print(f"   - Embeddings almacenados: {emb_count}")
        
        # Verificar dimensionalidad
        if emb_count > 0:
            cursor = conn.execute("SELECT embedding FROM embeddings LIMIT 1")
            row = cursor.fetchone()
            if row and row[0]:
                # sqlite-vec almacena como BLOB
                blob_size = len(row[0])
                dimensions = blob_size // 4  # 4 bytes por float32
                print(f"   - Tamaño del embedding: {blob_size} bytes")
                print(f"   - Dimensiones estimadas: {dimensions}")
        
        conn.close()
        
        if emb_count > 0:
            print("\n✅ PRUEBA 4: EXITOSA")
            return True
        else:
            print("\n⚠️  PRUEBA 4: SIN EMBEDDINGS")
            return False
        
    except Exception as e:
        print(f"\n❌ PRUEBA 4: FALLIDA - {e}")
        import traceback
        traceback.print_exc()
        conn.close()
        return False


def test_graph_storage():
    """Prueba 5: Verificar grafo en Kùzu"""
    print("\n" + "="*80)
    print("🧪 PRUEBA 5: Verificar Grafo de Conocimiento")
    print("="*80)
    
    try:
        import kuzu
    except ImportError as e:
        print(f"❌ Kuzu no disponible: {e}")
        return False
    
    db_path = project_root / "db/rag/rag_graph.kuzu"
    
    if not db_path.exists():
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    print(f"📊 Conectando a: {db_path}")
    
    try:
        db = kuzu.Database(str(db_path / "db"))
        conn = kuzu.Connection(db)
        
        # Contar nodos Entity
        result = conn.execute("MATCH (n:Entity) RETURN count(n) as count")
        if result.has_next():
            node_count = result.get_next()[0]
            print(f"   - Nodos Entity: {node_count}")
        else:
            print(f"   - Nodos Entity: 0")
        
        # Contar relaciones
        for rel_name in ['REQUIRES', 'RELATES_TO', 'PART_OF']:
            try:
                result = conn.execute(f"MATCH (a)-[r:{rel_name}]->(b) RETURN count(r) as count")
                if result.has_next():
                    rel_count = result.get_next()[0]
                    print(f"   - Relaciones {rel_name}: {rel_count}")
            except Exception:
                print(f"   - Relaciones {rel_name}: No existe")
        
        # Mostrar primeros nodos
        result = conn.execute("MATCH (n:Entity) RETURN n.name, n.type LIMIT 5")
        nodes = []
        while result.has_next():
            row = result.get_next()
            nodes.append((row[0], row[1]))
        
        if nodes:
            print(f"\n   📄 Primeros nodos:")
            for name, type_ in nodes:
                print(f"      - {name} ({type_})")
        
        print("\n✅ PRUEBA 5: EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ PRUEBA 5: FALLIDA - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_code_ingestor():
    """Prueba 6: CodeIngestor con análisis AST"""
    print("\n" + "="*80)
    print("🧪 PRUEBA 6: CodeIngestor con Análisis AST")
    print("="*80)
    
    from modules.rag.ingestors.code_ingestor import CodeIngestor
    
    # Archivo de prueba
    test_file = project_root / "modules/rag/ingestors/file_ingestor.py"
    
    if not test_file.exists():
        print(f"❌ Archivo no encontrado: {test_file}")
        return False
    
    print(f"📄 Archivo: {test_file}")
    print(f"📏 Tamaño: {test_file.stat().st_size} bytes")
    
    # Crear ingestor
    ingestor = CodeIngestor()
    
    # Procesar archivo
    try:
        processed = ingestor.process(str(test_file))
        
        print(f"\n📊 Resultados del procesamiento:")
        print(f"   - Doc ID: {processed.doc_id[:16]}...")
        print(f"   - Tipo: {processed.doc_type}")
        print(f"   - Título: {processed.title}")
        print(f"   - Chunks: {processed.total_chunks}")
        print(f"   - Entidades: {len(processed.entities) if processed.entities else 0}")
        
        # Mostrar entidades de código
        if processed.entities:
            print(f"\n   🔍 Entidades de código:")
            for ent in processed.entities[:10]:
                print(f"      - {ent['name']} ({ent['entity_type']})")
        
        print("\n✅ PRUEBA 6: EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ PRUEBA 6: FALLIDA - {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*80)
    print("🚀 PRUEBAS HEADLESS DE INGESTA RAG - SISTEMA V3")
    print("="*80)
    print(f"📁 Project Root: {project_root}")
    print(f"📂 DB Root: {project_root}/db/rag")
    
    results = {
        'FileIngestor Básico': test_file_ingestor_basic(),
        'RAGOrchestrator Ingesta': test_rag_orchestrator_ingestion(),
        'SQLite Storage': test_sqlite_storage(),
        'Vector Embeddings': test_vector_embeddings(),
        'Graph Storage': test_graph_storage(),
        'CodeIngestor AST': test_code_ingestor(),
    }
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {name}")
    
    print(f"\n📈 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        return True
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

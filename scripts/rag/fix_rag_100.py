#!/usr/bin/env python3
"""
Script de Reparación RAG V3 - 100% Funcional

Repara:
1. sqlite-vec binding (usa serialize_float32)
2. GraphBuilder (agrega entidades correctamente)
3. Re-ingesta completa con embeddings

Uso:
    cd /home/daniel/tron/programas/TR
    python scripts/rag/fix_rag_100.py
"""

import os
import sys
import sqlite3
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
os.environ['TR_PROJECT_ROOT'] = str(project_root)

from sqlite_vec import serialize_float32
import numpy as np


def fix_vector_engine_binding():
    """Arreglar el problema de binding en vector_engine.py"""
    print("\n" + "="*80)
    print("🔧 ARREGLANDO: sqlite-vec binding en vector_engine.py")
    print("="*80)
    
    vector_engine_path = project_root / "modules/rag/engines/vector_engine.py"
    
    with open(vector_engine_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Arreglar: agregar import de serialize_float32
    if "from sqlite_vec import serialize_float32" not in content:
        # Buscar la línea de imports
        old_import = "import sqlite3"
        new_import = "import sqlite3\nfrom sqlite_vec import serialize_float32"
        content = content.replace(old_import, new_import)
        print("✅ Agregado: from sqlite_vec import serialize_float32")
    
    # Arreglar: usar serialize_float32 en _vector_search
    old_search = """        c.execute(\"\"\"
            SELECT chunk_id, doc_id, entity_tags,
                   vec_distance_l2(embedding, ?) as distance
            FROM embeddings
            WHERE distance IS NOT NULL
            ORDER BY distance ASC
            LIMIT ?
        \"\"\", (embedding_list, limit))"""
    
    new_search = """        # Serializar embedding correctamente para sqlite-vec
        embedding_blob = serialize_float32(query_embedding)
        
        c.execute(\"\"\"
            SELECT chunk_id, doc_id, entity_tags,
                   vec_distance_l2(embedding, ?) as distance
            FROM embeddings
            WHERE embedding MATCH ?
            ORDER BY distance ASC
            LIMIT ?
        \"\"\", (embedding_blob, embedding_blob, limit))"""
    
    if old_search in content:
        content = content.replace(old_search, new_search)
        print("✅ Arreglado: _vector_search usa serialize_float32 y MATCH")
    else:
        print("⚠️  No se encontró el código exacto, revisión manual requerida")
    
    with open(vector_engine_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Guardado: {vector_engine_path}")


def fix_graph_builder():
    """Arreglar GraphBuilder para que agregue entidades"""
    print("\n" + "="*80)
    print("🔧 ARREGLANDO: GraphBuilder para agregar entidades")
    print("="*80)
    
    graph_builder_path = project_root / "modules/rag/ingestors/graph_builder.py"
    
    with open(graph_builder_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # El problema es que add_entity usa INSERT INTO Entity VALUES pero Kuzu requiere sintaxis especial
    # Vamos a simplificar usando MERGE (upsert de Cypher)
    
    # Buscar y reemplazar el método add_entity
    import re
    
    # Patrón para encontrar el método add_entity
    old_pattern = r'''    def add_entity\(self, name: str, entity_type: str, 
                   source_doc: str, validated: bool = False\) -> bool:
        """
        Agregar nodo de entidad al grafo\.[\s\S]*?logger\.debug\(f"Entidad ya existe o error: \{e\}"\)
        return False'''
    
    new_add_entity = '''    def add_entity(self, name: str, entity_type: str, 
                   source_doc: str, validated: bool = False) -> bool:
        """
        Agregar nodo de entidad al grafo usando MERGE (Cypher upsert).

        Args:
            name: Nombre de la entidad
            entity_type: Tipo de entidad
            source_doc: Documento fuente
            validated: Si la entidad está validada

        Returns:
            True si se agregó exitosamente
        """
        try:
            conn = self._get_connection()
            # Usar MERGE para evitar duplicados (upsert)
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
            logger.debug(f"Entidad ya existe o error: {e}")
            return False'''
    
    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_add_entity, content)
        print("✅ Arreglado: add_entity usa MERGE (Cypher upsert)")
    else:
        print("⚠️  No se encontró add_entity exacto")
    
    with open(graph_builder_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Guardado: {graph_builder_path}")


def reingest_documents():
    """Re-ingerir documentos con todo funcional"""
    print("\n" + "="*80)
    print("📥 RE-INGESTA: Documentos con embeddings y grafo")
    print("="*80)
    
    from modules.rag.core.rag_orchestrator import RAGOrchestrator
    
    # Limpiar bases de datos primero
    print("🗑️  Limpiando bases de datos...")
    db_root = project_root / "db/rag"
    
    # Guardar grafo (solo limpiar datos, no esquema)
    try:
        import kuzu
        graph_db = kuzu.Database(str(db_root / "rag_graph.kuzu" / "db"))
        graph_conn = kuzu.Connection(graph_db)
        # Eliminar todos los datos
        graph_conn.execute("MATCH (n:Entity) DELETE n")
        graph_conn.execute("MATCH ()-[r]->() DELETE r")
        print("✅ Grafo limpiado")
        graph_db.close()
    except Exception as e:
        print(f"⚠️  Error limpiando grafo: {e}")
    
    # Reiniciar vectores
    vec_db = db_root / "rag_vectors.sqlite"
    if vec_db.exists():
        vec_db.unlink()
        print("✅ Vectores eliminados (se recrearán)")
    
    # Reiniciar core (eliminar tablas)
    core_db = db_root / "rag_core.sqlite"
    if core_db.exists():
        conn = sqlite3.connect(str(core_db))
        conn.execute("DELETE FROM entities")
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM documents")
        conn.commit()
        conn.close()
        print("✅ Core limpiado")
    
    # Re-inicializar vectores
    print("\n🔧 Re-inicializando vectores...")
    from modules.rag.init_rag_db import init_vectors_db
    init_vectors_db(vec_db)
    
    # Ingerir documento
    print("\n📥 Ingestando documento...")
    test_doc = project_root / "docs/ArquitecturadeModulosOrientadaaIA/ArquitecturadeMódulosOrientadaaIA.md"
    
    rag = RAGOrchestrator()
    result = rag.ingest_document(str(test_doc))
    
    print("\n📊 RESULTADOS DE RE-INGESTA:")
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    return result


def verify_100_percent():
    """Verificar que todo está al 100%"""
    print("\n" + "="*80)
    print("✅ VERIFICACIÓN 100% FUNCIONAL")
    print("="*80)
    
    db_root = project_root / "db/rag"
    
    # Verificar Core
    core_db = sqlite3.connect(str(db_root / "rag_core.sqlite"))
    cursor = core_db.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    
    cursor = core_db.execute("SELECT COUNT(*) FROM chunks")
    chunk_count = cursor.fetchone()[0]
    
    cursor = core_db.execute("SELECT COUNT(*) FROM entities")
    entity_count = cursor.fetchone()[0]
    
    core_db.close()
    
    # Verificar Vector
    vec_db = sqlite3.connect(str(db_root / "rag_vectors.sqlite"))
    vec_db.enable_load_extension(True)
    import sqlite_vec
    sqlite_vec.load(vec_db)
    
    cursor = vec_db.execute("SELECT COUNT(*) FROM embeddings")
    embedding_count = cursor.fetchone()[0]
    
    vec_db.close()
    
    # Verificar Graph
    import kuzu
    graph_db = kuzu.Database(str(db_root / "rag_graph.kuzu" / "db"))
    graph_conn = kuzu.Connection(graph_db)
    
    result = graph_conn.execute("MATCH (n:Entity) RETURN count(n) as count")
    graph_nodes = result.get_next()[0] if result.has_next() else 0
    
    result = graph_conn.execute("MATCH ()-[r]->() RETURN count(r) as count")
    graph_rels = result.get_next()[0] if result.has_next() else 0
    
    graph_db.close()
    
    print("\n📊 ESTADO DEL SISTEMA:")
    print(f"   📄 Documentos: {doc_count}")
    print(f"   🧩 Chunks: {chunk_count}")
    print(f"   🏷️  Entidades: {entity_count}")
    print(f"   🔢 Embeddings: {embedding_count}")
    print(f"   🕸️  Nodos Grafo: {graph_nodes}")
    print(f"   🔗 Relaciones Grafo: {graph_rels}")
    
    # Calcular porcentajes
    embedding_coverage = (embedding_count / chunk_count * 100) if chunk_count > 0 else 0
    
    print(f"\n📈 COBERTURA:")
    print(f"   - Embeddings: {embedding_coverage:.1f}% ({embedding_count}/{chunk_count})")
    print(f"   - Grafo: {graph_nodes} nodos, {graph_rels} relaciones")
    
    # Verificar 100%
    all_good = (
        doc_count > 0 and
        chunk_count > 0 and
        entity_count > 0 and
        embedding_coverage == 100.0 and
        graph_nodes > 0
    )
    
    if all_good:
        print("\n🎉 ¡SISTEMA 100% FUNCIONAL!")
    else:
        print("\n⚠️  Algunos componentes requieren atención:")
        if embedding_coverage < 100:
            print(f"   - Embeddings: {embedding_coverage:.1f}% (falta {(100 - embedding_coverage):.1f}%)")
        if graph_nodes == 0:
            print(f"   - Grafo: vacío (GraphBuilder no agregó nodos)")
    
    return all_good


def main():
    """Función principal"""
    print("="*80)
    print("🚀 REPARACIÓN RAG V3 - 100% FUNCIONAL")
    print("="*80)
    
    # Paso 1: Arreglar vector_engine
    fix_vector_engine_binding()
    
    # Paso 2: Arreglar GraphBuilder
    fix_graph_builder()
    
    # Paso 3: Re-ingerir documentos
    reingest_documents()
    
    # Paso 4: Verificar 100%
    success = verify_100_percent()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

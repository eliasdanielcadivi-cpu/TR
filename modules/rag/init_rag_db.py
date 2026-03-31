#!/usr/bin/env python3
"""
Script de inicialización de bases de datos RAG.

Crea las tres bases de datos:
  1. rag_core.sqlite - Metadatos y control
  2. rag_vectors.sqlite - Embeddings (sqlite-vec)
  3. rag_graph.kuzu - Grafo de conocimiento

Uso:
    python init_rag_db.py
"""

import os
import sqlite3
import sys
from pathlib import Path

# Añadir ruta del proyecto a sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def init_core_db(db_path: Path) -> None:
    """Inicializar base de datos core (metadatos y control)."""
    print(f"📦 Inicializando {db_path.name}...")

    conn = sqlite3.connect(db_path)

    # Tabla de documentos indexados
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            doc_id TEXT UNIQUE NOT NULL,
            source_path TEXT NOT NULL,
            doc_type TEXT,
            title TEXT,
            summary TEXT,
            chunk_count INTEGER,
            last_indexed TIMESTAMP,
            validation_status TEXT DEFAULT 'pending'
        )
    """)

    # Tabla de chunks
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            doc_id TEXT REFERENCES documents(doc_id),
            chunk_index INTEGER,
            content TEXT,
            start_line INTEGER,
            end_line INTEGER,
            char_count INTEGER
        )
    """)

    # Tabla de entidades extraídas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            entity_type TEXT,
            source_doc_id TEXT,
            source_chunk_id INTEGER,
            confidence REAL
        )
    """)

    # Tabla de relaciones propuestas (C1-C4)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relation_proposals (
            id INTEGER PRIMARY KEY,
            subject_entity TEXT,
            relation_verb TEXT,
            object_entity TEXT,
            criticality TEXT CHECK(criticality IN ('C1','C2','C3','C4')),
            confidence REAL,
            proposed_by TEXT,
            status TEXT DEFAULT 'pending',
            proposed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            validated_by TEXT,
            validated_at TIMESTAMP,
            context_snapshot TEXT
        )
    """)

    # Tabla de índice de skills
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rag_skills_index (
            id INTEGER PRIMARY KEY,
            skill_name TEXT,
            skill_path TEXT,
            embedding_model TEXT,
            last_synced TIMESTAMP
        )
    """)

    # Índices para rendimiento
    conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_doc_id ON documents(doc_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON chunks(doc_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_relations_status ON relation_proposals(status, criticality)")

    conn.commit()
    conn.close()
    print(f"✅ {db_path.name} inicializada correctamente.")

def init_vectors_db(db_path: Path) -> None:
    """Inicializar base de datos de vectores (sqlite-vec)."""
    print(f"🔢 Inicializando {db_path.name}...")

    try:
        import sqlite_vec
    except ImportError:
        print("❌ sqlite-vec no está instalado. Instala con: pip install sqlite-vec")
        return

    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    # Tabla virtual para embeddings (1024 dimensiones para mxbai-embed-large)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS embeddings USING vec0(
            chunk_id INTEGER PRIMARY KEY,
            embedding float[1024],
            +doc_id TEXT,
            +entity_tags TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ {db_path.name} inicializada correctamente.")

def init_graph_db(db_path: Path) -> None:
    """Inicializar base de datos de grafo (Kùzu)."""
    print(f"🕸️  Inicializando {db_path.name}...")

    try:
        import kuzu
    except ImportError:
        print("❌ kuzu no está instalado. Instala con: pip install kuzu")
        return

    # Kùzu usa un directorio (eliminar si existe como archivo)
    db_dir = db_path.parent / "rag_graph.kuzu"
    if db_dir.exists() and db_dir.is_file():
        db_dir.unlink()
    db_dir.mkdir(exist_ok=True)

    # Kuzu >= 0.11 usa path como archivo dentro del directorio
    db = kuzu.Database(str(db_dir / "db"))
    conn = kuzu.Connection(db)

    # Nodos Entity
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Entity(
            name STRING,
            type STRING,
            source_doc STRING,
            validated BOOLEAN DEFAULT false,
            PRIMARY KEY (name)
        )
    """)

    # Relaciones
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS REQUIRES(
            FROM Entity TO Entity,
            weight DOUBLE DEFAULT 1.0,
            criticality STRING DEFAULT 'C2',
            validated BOOLEAN DEFAULT false
        )
    """)

    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS RELATES_TO(
            FROM Entity TO Entity,
            relation_type STRING,
            confidence DOUBLE,
            context STRING
        )
    """)

    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS PART_OF(
            FROM Entity TO Entity,
            order_idx DOUBLE
        )
    """)

    print(f"✅ {db_path.name} inicializada correctamente.")

def main():
    """Función principal."""
    project_root = Path(__file__).parent.parent.parent
    db_root = project_root / "db" / "rag"

    print("🚀 Inicializando bases de datos RAG...")
    print(f"📁 Directorio: {db_root}")

    # Crear directorio si no existe
    db_root.mkdir(parents=True, exist_ok=True)

    # Inicializar las tres bases
    init_core_db(db_root / "rag_core.sqlite")
    init_vectors_db(db_root / "rag_vectors.sqlite")
    init_graph_db(db_root / "rag_graph.kuzu")

    print("\n🎉 Todas las bases de datos RAG han sido inicializadas.")
    print("💡 Ahora puedes ejecutar: python -m modules.rag.cli.rag_cli --help")

if __name__ == "__main__":
    main()
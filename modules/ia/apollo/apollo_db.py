"""Apollo DB: Persistencia unificada para RAG + CRM.

Módulo atómico que gestiona conexiones SQLite con extensión sqlite-vec
para búsqueda vectorial de bajo consumo (<100MB RAM).

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import sqlite3
import sqlite_vec
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


# Rutas de bases de datos
# __file__ = modules/ia/apollo/apollo_db.py
# parent.parent.parent = modules/
# parent.parent.parent.parent = TR (root)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
APOLLO_DIR = PROJECT_ROOT / "bd" / "apollo"
KNOWLEDGE_DB = APOLLO_DIR / "knowledge.db"
USERS_DB = APOLLO_DIR / "users.db"

# Cache de conexiones (lazy loading)
_connections = {
    "knowledge": None,
    "users": None
}


def init_db(db_type: str = "knowledge") -> bool:
    """Inicializar base de datos Apollo con schema RAG + CRM.

    Args:
        db_type: "knowledge" para RAG, "users" para CRM.

    Returns:
        True si exitoso, False si error.
    """
    try:
        # Asegurar directorio existe
        APOLLO_DIR.mkdir(parents=True, exist_ok=True)

        # Determinar ruta de DB
        db_path = KNOWLEDGE_DB if db_type == "knowledge" else USERS_DB

        # Conectar y cargar sqlite-vec
        conn = sqlite3.connect(str(db_path))
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

        # Crear schema según tipo
        if db_type == "knowledge":
            _create_rag_schema(conn)
        else:
            _create_crm_schema(conn)

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ Error inicializando {db_type}: {e}")
        return False


def get_connection(db_type: str = "knowledge") -> Optional[sqlite3.Connection]:
    """Obtener conexión a base de datos Apollo.

    Args:
        db_type: "knowledge" para RAG, "users" para CRM.

    Returns:
        Conexión SQLite con sqlite-vec cargado, o None si error.
    """
    global _connections

    # Verificar cache
    if _connections.get(db_type) is not None:
        return _connections[db_type]

    try:
        # Determinar ruta de DB
        db_path = KNOWLEDGE_DB if db_type == "knowledge" else USERS_DB

        # Verificar que DB existe
        if not db_path.exists():
            print(f"⚠️  {db_type}.db no existe. Ejecutar init_db('{db_type}') primero.")
            return None

        # Conectar y cargar sqlite-vec
        conn = sqlite3.connect(str(db_path))
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        conn.row_factory = sqlite3.Row

        # Cachear conexión
        _connections[db_type] = conn

        return conn

    except Exception as e:
        print(f"❌ Error conectando a {db_type}: {e}")
        return None


def close_db(db_type: Optional[str] = None) -> None:
    """Cerrar conexiones a bases de datos Apollo.

    Args:
        db_type: "knowledge", "users", o None para cerrar todas.
    """
    global _connections

    if db_type is None:
        # Cerrar todas
        for key in list(_connections.keys()):
            if _connections[key] is not None:
                _connections[key].close()
                _connections[key] = None
    else:
        # Cerrar específica
        if _connections.get(db_type) is not None:
            _connections[db_type].close()
            _connections[db_type] = None


@contextmanager
def db_context(db_type: str = "knowledge"):
    """Context manager para conexiones Apollo.

    Args:
        db_type: "knowledge" para RAG, "users" para CRM.

    Yields:
        Conexión SQLite.

    Ejemplo:
        with db_context("knowledge") as conn:
            conn.execute("SELECT * FROM documents")
    """
    conn = get_connection(db_type)
    if conn is None:
        raise RuntimeError(f"No se pudo conectar a {db_type}.db")
    try:
        yield conn
    finally:
        # No cerrar en context manager (se reutiliza cache)
        pass


def _create_rag_schema(conn: sqlite3.Connection) -> None:
    """Crear schema RAG en knowledge.db.

    Tablas: documents, chunks, embeddings (vec0), entities, relations.
    """
    # Documentos fuente
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            title TEXT,
            source TEXT,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSON
        )
    """)

    # Chunks de texto
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            document_id TEXT REFERENCES documents(id),
            chunk_index INTEGER,
            text TEXT,
            tokens INTEGER,
            parent_chunk_id TEXT REFERENCES chunks(id)
        )
    """)

    # Embeddings con sqlite-vec (tabla virtual)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS embeddings USING vec0(
            chunk_id TEXT PRIMARY KEY,
            vector FLOAT[1024],
            document_id TEXT,
            chunk_index INTEGER
        )
    """)

    # Entidades extraídas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            description TEXT,
            embedding BLOB
        )
    """)

    # Relaciones entre entidades
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relations (
            id TEXT PRIMARY KEY,
            subject_id TEXT REFERENCES entities(id),
            predicate TEXT,
            object_id TEXT REFERENCES entities(id),
            chunk_id TEXT REFERENCES chunks(id),
            confidence FLOAT DEFAULT 1.0
        )
    """)

    # Índices para rendimiento
    conn.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(document_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_relations_subject ON relations(subject_id)")


def _create_crm_schema(conn: sqlite3.Connection) -> None:
    """Crear schema CRM en users.db.

    Tablas: users, clients, interactions, client_documents.
    """
    # Usuarios del sistema ARES
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP,
            preferences JSON
        )
    """)

    # Clientes (decantados de múltiples fuentes)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            source TEXT,
            status TEXT,
            metadata JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Interacciones con clientes
    conn.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id TEXT PRIMARY KEY,
            client_id TEXT REFERENCES clients(id),
            user_id TEXT REFERENCES users(id),
            type TEXT,
            channel TEXT,
            summary TEXT,
            full_content TEXT,
            sentiment TEXT,
            action_items JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Relaciones cliente-documento (para RAG específico por cliente)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS client_documents (
            client_id TEXT REFERENCES clients(id),
            document_id TEXT REFERENCES documents(id),
            relevance_score FLOAT,
            PRIMARY KEY (client_id, document_id)
        )
    """)

    # Índices para rendimiento
    conn.execute("CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_interactions_client ON interactions(client_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_client_docs ON client_documents(client_id)")

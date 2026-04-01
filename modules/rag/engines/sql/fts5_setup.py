import logging

logger = logging.getLogger(__name__)

def init_fts5_index(conn):
    """
    Crea la tabla virtual FTS5 si no existe.
    Punto de fallo: Versión de SQLite antigua.
    """
    try:
        c = conn.cursor()
        c.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                content,
                content='chunks',
                content_rowid='id'
            )
        """)
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"FTS5 no soportado o error: {e}")
        return False

def rebuild_fts5_index(conn):
    """Sincroniza el índice con los datos reales."""
    try:
        c = conn.cursor()
        c.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error rebuild FTS5: {e}")
        return False

import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

def get_sqlite_conn(db_path: str, row_factory=sqlite3.Row):
    """
    Obtiene una conexión pura a SQLite.
    Puntos de fallo: Ruta inválida, DB corrupta, permisos.
    """
    try:
        if not os.path.exists(db_path):
            logger.warning(f"La base de datos no existe en: {db_path}")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = row_factory
        return conn
    except Exception as e:
        logger.error(f"Error conectando a SQLite ({db_path}): {e}")
        return None

def check_sqlite_health(conn) -> bool:
    """Verifica si la conexión está activa."""
    try:
        conn.execute("SELECT 1")
        return True
    except:
        return False

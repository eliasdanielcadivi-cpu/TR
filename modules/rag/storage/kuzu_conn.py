import kuzu
import os
import logging

logger = logging.getLogger(__name__)

def get_kuzu_db(db_root_path: str):
    """
    Inicializa el objeto Database de Kùzu.
    """
    try:
        db_path = db_root_path
        if not db_path.endswith('.kuzu'):
            db_path = db_path + '.kuzu'
            
        # IMPORTANTE: En esta versión, parece que debemos apuntar al archivo 'db' interno
        final_path = os.path.join(db_path, "db")
        return kuzu.Database(final_path)
    except Exception as e:
        logger.error(f"Error inicializando Kuzu Database en {db_root_path}: {e}")
        return None

def get_kuzu_conn(db):
    """Obtiene una conexión desde un objeto Database."""
    try:
        if db is None: return None
        return kuzu.Connection(db)
    except Exception as e:
        logger.error(f"Error obteniendo Kuzu Connection: {e}")
        return None

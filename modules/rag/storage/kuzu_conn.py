import kuzu
import os
import logging

logger = logging.getLogger(__name__)

def get_kuzu_db(db_root_path: str):
    """
    Inicializa el objeto Database de Kùzu.
    Puntos de fallo: Directorio bloqueado, falta de memoria.
    """
    try:
        # Asegurar que apuntamos al archivo interno 'db' si es necesario
        # o al directorio raíz según la versión.
        db_path = db_root_path
        if not db_path.endswith('.kuzu'):
            db_path = db_path + '.kuzu'
            
        # IMPORTANTE: KuzuDatabase espera una carpeta.
        return kuzu.Database(db_path)
    except Exception as e:
        logger.error(f"Error inicializando Kuzu Database: {e}")
        return None

def get_kuzu_conn(db):
    """Obtiene una conexión desde un objeto Database."""
    try:
        if db is None: return None
        return kuzu.Connection(db)
    except Exception as e:
        logger.error(f"Error obteniendo Kuzu Connection: {e}")
        return None

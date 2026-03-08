"""
Aviso DB - Gestión de base de datos de recordatorios
=====================================================

Módulo atómico para operaciones SQLite de avisos.
Máximo 3 funciones principales.

Ubicación DB: ~/tron/programas/TR/db/avisos.db
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass

# Configuración de logging
LOG_PATH = Path.home() / "tron/programas/TR/logs/aviso.log"
DEBUG_ENABLED = Path.home() / "tron/programas/TR/logs/aviso.debug"
DEBUG_PATH = DEBUG_ENABLED  # Alias para compatibilidad

def setup_logging():
    """Configurar logging según exista archivo .debug"""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    level = logging.DEBUG if DEBUG_ENABLED.exists() else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(LOG_PATH),
        ]
    )
    return logging.getLogger('aviso.db')

logger = setup_logging()

DB_PATH = Path.home() / "tron/programas/TR/db/avisos.db"


@dataclass
class Aviso:
    """Registro de aviso"""
    id: Optional[int]
    mensaje: str
    fecha_hora: str  # ISO format: YYYY-MM-DD HH:MM
    comando: str     # Comando a ejecutar o 'zenity'
    creado: str
    estado: str = 'pendiente'  # pendiente, ejecutado, cancelado


def init_db() -> sqlite3.Connection:
    """
    Inicializar base de datos y retornar conexión.
    Crea tabla si no existe.
    """
    logger.debug(f"Inicializando DB en {DB_PATH}")
    
    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avisos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mensaje TEXT NOT NULL,
                fecha_hora TEXT NOT NULL,
                comando TEXT NOT NULL,
                creado TEXT NOT NULL,
                estado TEXT DEFAULT 'pendiente'
            )
        ''')
        conn.commit()
        logger.info("DB inicializada correctamente")
        return conn
    except Exception as e:
        logger.error(f"Error inicializando DB: {e}")
        raise


def guardar_aviso(mensaje: str, fecha_hora: str, comando: str = 'zenity') -> int:
    """
    Guardar un nuevo aviso en la base de datos.
    Retorna el ID del aviso creado.
    """
    logger.debug(f"Guardando aviso: mensaje='{mensaje}', fecha='{fecha_hora}', comando='{comando}'")
    
    try:
        conn = init_db()
        cursor = conn.cursor()
        creado = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO avisos (mensaje, fecha_hora, comando, creado, estado)
            VALUES (?, ?, ?, ?, 'pendiente')
        ''', (mensaje, fecha_hora, comando, creado))
        conn.commit()
        aviso_id = cursor.lastrowid
        conn.close()
        logger.info(f"Aviso guardado con ID={aviso_id}")
        return aviso_id
    except Exception as e:
        logger.error(f"Error guardando aviso: {e}")
        raise


def listar_avisos(estado: str = 'pendiente') -> List[Aviso]:
    """
    Listar avisos filtrados por estado.
    Retorna lista de objetos Aviso.
    """
    logger.debug(f"Listando avisos con estado='{estado}'")
    
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, mensaje, fecha_hora, comando, creado, estado
            FROM avisos
            WHERE estado = ?
            ORDER BY fecha_hora ASC
        ''', (estado,))
        avisos = [Aviso(
            id=row['id'],
            mensaje=row['mensaje'],
            fecha_hora=row['fecha_hora'],
            comando=row['comando'],
            creado=row['creado'],
            estado=row['estado']
        ) for row in cursor.fetchall()]
        conn.close()
        logger.info(f"Listados {len(avisos)} avisos")
        return avisos
    except Exception as e:
        logger.error(f"Error listando avisos: {e}")
        raise


def borrar_aviso(aviso_id: int) -> bool:
    """
    Borrar un aviso por ID.
    Retorna True si se borró, False si no existía.
    """
    logger.debug(f"Borrando aviso ID={aviso_id}")
    
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM avisos WHERE id = ?', (aviso_id,))
        borrado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        logger.info(f"Aviso {aviso_id} {'borrado' if borrado else 'no encontrado'}")
        return borrado
    except Exception as e:
        logger.error(f"Error borrando aviso: {e}")
        raise


def actualizar_estado(aviso_id: int, estado: str) -> bool:
    """
    Actualizar estado de un aviso.
    Retorna True si se actualizó.
    """
    logger.debug(f"Actualizando aviso ID={aviso_id} a estado='{estado}'")
    
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE avisos SET estado = ? WHERE id = ?
        ''', (estado, aviso_id))
        actualizado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        logger.info(f"Aviso {aviso_id} actualizado a '{estado}'")
        return actualizado
    except Exception as e:
        logger.error(f"Error actualizando estado: {e}")
        raise


def obtener_pendientes() -> List[Aviso]:
    """
    Obtener todos los avisos pendientes.
    Usado por el daemon para verificar qué ejecutar.
    """
    logger.debug("Obteniendo avisos pendientes")
    return listar_avisos('pendiente')


def limpiar_logs():
    """Limpiar archivo de log (para debugging)"""
    if LOG_PATH.exists():
        LOG_PATH.unlink()
        logger.info("Log limpiado")


def toggle_debug():
    """Activar/desactivar modo debug"""
    if DEBUG_ENABLED.exists():
        DEBUG_ENABLED.unlink()
        logger.info("Debug DESACTIVADO")
    else:
        DEBUG_ENABLED.touch()
        logger.info("Debug ACTIVADO")

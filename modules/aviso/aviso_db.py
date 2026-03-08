"""
Aviso DB - Gestión de base de datos de recordatorios
=====================================================

Módulo atómico para operaciones SQLite de avisos.
Máximo 3 funciones principales.

Ubicación DB: ~/tron/programas/TR/db/avisos.db
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass

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
    return conn


def guardar_aviso(mensaje: str, fecha_hora: str, comando: str = 'zenity') -> int:
    """
    Guardar un nuevo aviso en la base de datos.
    Retorna el ID del aviso creado.
    """
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
    return aviso_id


def listar_avisos(estado: str = 'pendiente') -> List[Aviso]:
    """
    Listar avisos filtrados por estado.
    Retorna lista de objetos Aviso.
    """
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
    return avisos


def borrar_aviso(aviso_id: int) -> bool:
    """
    Borrar un aviso por ID.
    Retorna True si se borró, False si no existía.
    """
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM avisos WHERE id = ?', (aviso_id,))
    borrado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return borrado


def actualizar_estado(aviso_id: int, estado: str) -> bool:
    """
    Actualizar estado de un aviso.
    Retorna True si se actualizó.
    """
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE avisos SET estado = ? WHERE id = ?
    ''', (estado, aviso_id))
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


def obtener_pendientes() -> List[Aviso]:
    """
    Obtener todos los avisos pendientes.
    Usado por el daemon para verificar qué ejecutar.
    """
    return listar_avisos('pendiente')

"""
Session DB Manager - ARES-TRON.
Persistencia soberana de sesiones de Gemini (Hash-Based).
Filosofía: Máximo 3 funciones principales.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = "db/ares_sessions.db"

def init_db():
    """Inicializa la base de datos de sesiones si no existe."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gemini_sessions (
            hash TEXT PRIMARY KEY,
            titulo TEXT,
            proyecto TEXT,
            fecha_registro TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def register_session(hash_id: str, titulo: str, proyecto: str = "ARES"):
    """Registra o actualiza una sesión en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO gemini_sessions (hash, titulo, proyecto, fecha_registro)
        VALUES (?, ?, ?, ?)
    """, (hash_id, titulo, proyecto, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_ares_sessions():
    """Retorna la lista de sesiones registradas en ARES."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gemini_sessions ORDER BY fecha_registro DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

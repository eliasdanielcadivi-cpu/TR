"""
Window Registry - Registro de Ventanas Kitty y sus Sockets

Módulo atómico (≤3 funciones públicas) - Filosofía ARES

Funcionalidades:
1. register_window - Registra una ventana con su socket y sesión
2. get_window_by_session - Obtiene ventana por nombre de sesión
3. get_session_by_window - Obtiene sesión por ID de ventana
4. list_active_windows - Lista todas las ventanas registradas
5. unregister_window - Elimina ventana del registro
6. cleanup_stale_windows - Limpia ventanas cuyo socket ya no existe

Flujo de Datos:
- Entrada: session_name, socket_path, window_id (opcional)
- Procesamiento: SQLite para persistencia
- Salida: Información de ventanas y sockets mapeados

Ejemplo de Uso:
```python
from modules.core.window_registry import (
    register_window,
    get_window_by_session,
    list_active_windows,
    unregister_window
)

# Ejemplo 1: Registrar ventana nueva
register_window(
    session_name="diaria",
    socket_path="/tmp/ares_session_diaria_1710604800_a3f2",
    window_id=1
)

# Ejemplo 2: Buscar ventana por sesión
window = get_window_by_session("diaria")
print(window["socket_path"])  # "/tmp/ares_session_..."
print(window["window_id"])    # 1

# Ejemplo 3: Listar todas las ventanas activas
windows = list_active_windows()
for w in windows:
    print(f"{w['session_name']} → {w['socket_path']}")

# Ejemplo 4: Limpiar ventanas huérfanas
cleanup_stale_windows()
```
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


# ============================================================================
# CONSTANTES
# ============================================================================

DB_PATH = Path.home() / ".tron" / "ares" / "window_registry.db"
"""Ruta a la base de datos SQLite para registro de ventanas"""


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def _get_connection() -> sqlite3.Connection:
    """
    Obtiene conexión SQLite con row factory.

    Returns:
        Conexión a la base de datos
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Inicializa base de datos de registro de ventanas.

    Crea la tabla si no existe.
    """
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS window_registry (
            session_name TEXT PRIMARY KEY,
            socket_path TEXT NOT NULL,
            window_id INTEGER,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()


# ============================================================================
# FUNCIONES EXPORTADAS (API PÚBLICA)
# ============================================================================

def register_window(
    session_name: str,
    socket_path: str,
    window_id: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Registra una ventana Kitty con su socket y sesión asociada.

    Si la sesión ya existe, actualiza el registro (upsert).

    Args:
        session_name: Nombre identificador de la sesión (ej. "diaria", "proyecto-x")
        socket_path: Ruta completa del socket UNIX (ej. "/tmp/ares_session_diaria_123_abc")
        window_id: ID de ventana Kitty (opcional, se puede obtener después con kitty @ ls)
        metadata: Metadatos adicionales en JSON (opcional)

    Returns:
        True si se registró exitosamente

    Example:
        # Registrar ventana nueva
        register_window(
            session_name="diaria",
            socket_path="/tmp/ares_session_diaria_1710604800_a3f2",
            window_id=1
        )

        # Registrar sin window_id (se actualiza después)
        register_window(
            session_name="proyecto-x",
            socket_path="/tmp/ares_session_proyecto_x_1710604900_b7e1"
        )
    """
    now = datetime.now().isoformat()
    metadata_json = json.dumps(metadata) if metadata else None

    conn = _get_connection()
    conn.execute("""
        INSERT OR REPLACE INTO window_registry 
        (session_name, socket_path, window_id, created_at, updated_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_name,
        socket_path,
        window_id,
        now,
        now,  # created_at = updated_at en inserción nueva
        metadata_json
    ))
    conn.commit()
    conn.close()

    return True


def get_window_by_session(session_name: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene información de una ventana por nombre de sesión.

    Args:
        session_name: Nombre de la sesión a buscar

    Returns:
        Dict con información de la ventana o None si no existe

    Example:
        window = get_window_by_session("diaria")
        if window:
            print(f"Socket: {window['socket_path']}")
            print(f"Window ID: {window['window_id']}")
    """
    conn = _get_connection()
    cursor = conn.execute(
        "SELECT * FROM window_registry WHERE session_name = ?",
        (session_name,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "session_name": row["session_name"],
        "socket_path": row["socket_path"],
        "window_id": row["window_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "metadata": json.loads(row["metadata"]) if row["metadata"] else None
    }


def get_session_by_window(window_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene información de sesión por ID de ventana Kitty.

    Args:
        window_id: ID de ventana Kitty

    Returns:
        Dict con información de la sesión o None si no existe

    Example:
        session = get_session_by_window(1)
        if session:
            print(f"Sesión: {session['session_name']}")
            print(f"Socket: {session['socket_path']}")
    """
    conn = _get_connection()
    cursor = conn.execute(
        "SELECT * FROM window_registry WHERE window_id = ?",
        (window_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "session_name": row["session_name"],
        "socket_path": row["socket_path"],
        "window_id": row["window_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "metadata": json.loads(row["metadata"]) if row["metadata"] else None
    }


def list_active_windows() -> List[Dict[str, Any]]:
    """
    Lista todas las ventanas registradas actualmente.

    Returns:
        Lista de dicts con información de cada ventana

    Example:
        windows = list_active_windows()
        for w in windows:
            print(f"{w['session_name']} → {w['socket_path']} (ID: {w['window_id']})")
    """
    conn = _get_connection()
    cursor = conn.execute("SELECT * FROM window_registry ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "session_name": row["session_name"],
            "socket_path": row["socket_path"],
            "window_id": row["window_id"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "metadata": json.loads(row["metadata"]) if row["metadata"] else None
        }
        for row in rows
    ]


def unregister_window(session_name: str) -> bool:
    """
    Elimina una ventana del registro.

    Usar cuando una sesión/ventana se cierra definitivamente.

    Args:
        session_name: Nombre de la sesión a eliminar

    Returns:
        True si se eliminó, False si no existía

    Example:
        deleted = unregister_window("diaria")
        print(deleted)  # True si existía
    """
    conn = _get_connection()
    cursor = conn.execute(
        "DELETE FROM window_registry WHERE session_name = ?",
        (session_name,)
    )
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return deleted


def update_window_id(session_name: str, window_id: int) -> bool:
    """
    Actualiza el window_id de una sesión registrada.

    Útil cuando se registra primero el socket y después se obtiene el window_id.

    Args:
        session_name: Nombre de la sesión
        window_id: Nuevo ID de ventana

    Returns:
        True si se actualizó, False si no existía

    Example:
        # Registrar socket primero
        register_window("diaria", "/tmp/ares_session_diaria_...")
        
        # Después de lanzar Kitty, actualizar con window_id
        update_window_id("diaria", window_id=1)
    """
    now = datetime.now().isoformat()
    conn = _get_connection()
    cursor = conn.execute("""
        UPDATE window_registry 
        SET window_id = ?, updated_at = ?
        WHERE session_name = ?
    """, (window_id, now, session_name))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return updated


def cleanup_stale_windows() -> List[str]:
    """
    Limpia registros de ventanas cuyos sockets ya no existen.

    Verifica cada socket registrado y elimina los que no existen físicamente.

    Returns:
        Lista de session_names eliminados

    Example:
        removed = cleanup_stale_windows()
        print(f"Ventanas huérfanas limpiadas: {removed}")
    """
    import os

    windows = list_active_windows()
    removed = []

    for window in windows:
        socket_path = window["socket_path"]
        # Quitar prefijo 'unix:' si existe
        clean_path = socket_path.replace('unix:', '')
        
        if not os.path.exists(clean_path):
            unregister_window(window["session_name"])
            removed.append(window["session_name"])

    return removed


def find_window_by_socket(socket_path: str) -> Optional[Dict[str, Any]]:
    """
    Busca una ventana por su ruta de socket.

    Args:
        socket_path: Ruta del socket a buscar

    Returns:
        Dict con información de la ventana o None si no existe

    Example:
        window = find_window_by_socket("/tmp/ares_session_diaria_...")
        if window:
            print(f"Sesión: {window['session_name']}")
    """
    conn = _get_connection()
    cursor = conn.execute(
        "SELECT * FROM window_registry WHERE socket_path = ?",
        (socket_path,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "session_name": row["session_name"],
        "socket_path": row["socket_path"],
        "window_id": row["window_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "metadata": json.loads(row["metadata"]) if row["metadata"] else None
    }


def get_registry_stats() -> Dict[str, Any]:
    """
    Obtiene estadísticas del registro de ventanas.

    Returns:
        Dict con count, sockets_existentes, sockets_huerfanos

    Example:
        stats = get_registry_stats()
        print(f"Total: {stats['count']}")
        print(f"Activas: {stats['sockets_existentes']}")
        print(f"Huérfanas: {stats['sockets_huerfanos']}")
    """
    import os

    conn = _get_connection()
    cursor = conn.execute("SELECT COUNT(*) as count FROM window_registry")
    count = cursor.fetchone()["count"]
    conn.close()

    windows = list_active_windows()
    existentes = 0
    huerfanos = 0

    for w in windows:
        clean_path = w["socket_path"].replace('unix:', '')
        if os.path.exists(clean_path):
            existentes += 1
        else:
            huerfanos += 1

    return {
        "count": count,
        "sockets_existentes": existentes,
        "sockets_huerfanos": huerfanos,
        "timestamp": datetime.now().isoformat()
    }

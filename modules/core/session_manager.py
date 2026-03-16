"""
Session Manager - Módulo para gestión de sesiones de conversación

Módulo atómico (≤3 funciones) - Filosofía ARES

Funcionalidades:
1. create_session - Crea nueva sesión con valores por defecto
2. get_session - Obtiene sesión existente por ID
3. update_session - Actualiza campos de sesión (parcial)
4. delete_session - Elimina sesión permanentemente
5. list_sessions - Lista todos los IDs de sesiones activas
6. get_session_stats - Obtiene estadísticas del almacenamiento

Flujo de Datos:
- Entrada: ID de sesión (opcional para crear) + actualizaciones parciales
- Procesamiento: Almacenamiento en memoria (Map)
- Salida: Objetos Session completos o booleanos de éxito

Ejemplo de Uso:
```python
# Ejemplo 1: Crear sesión
session = create_session()
print(session["id"])  # 'sess_1234567890_abc'
print(len(session["messages"]))  # 0

# Ejemplo 2: Obtener sesión
retrieved = get_session(session["id"])
print(retrieved["system_prompt"])  # Prompt por defecto

# Ejemplo 3: Actualizar sesión
update_session(session["id"], {
    "system_prompt": "Nuevo prompt personalizado",
    "objectives": ["Objetivo 1", "Objetivo 2"]
})

# Ejemplo 4: Listar sesiones
all_sessions = list_sessions()
print(all_sessions)  # ['sess_...']

# Ejemplo 5: Eliminar sesión
deleted = delete_session(session["id"])
print(deleted)  # True
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

DB_PATH = Path.home() / ".tron" / "agente_de_cambio" / "sessions.db"
"""Ruta a la base de datos SQLite para persistencia de sesiones"""


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def _get_connection() -> sqlite3.Connection:
    """
    Obtiene conexión SQLite con row factory.
    
    Returns:
        Conexión a la base de datos
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Inicializa base de datos de sesiones.
    
    Crea la tabla si no existe.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            system_prompt TEXT,
            objectives TEXT,
            messages TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# ============================================================================
# FUNCIONES EXPORTADAS (API PÚBLICA DEL MÓDULO)
# ============================================================================

def create_session(session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Crea una nueva sesión de conversación.
    
    Inicializa una sesión con valores por defecto:
    - system_prompt: Prompt base de extracción cognitiva
    - messages: Array vacío
    - objectives: Array vacío
    
    Args:
        session_id: ID opcional para la sesión
                   (genera uno automático si no se proporciona)
    
    Returns:
        La nueva sesión creada
    
    Example:
        # Crear con ID automático
        session = create_session()
        print(session["id"])  # 'sess_1708819200000_xyz'
    
    Example:
        # Crear con ID personalizado
        session = create_session("mi-sesion-123")
        print(session["id"])  # 'mi-sesion-123'
    """
    import secrets
    
    session_id = session_id or f"sess_{int(datetime.now().timestamp() * 1000)}_{secrets.token_hex(4)}"
    
    session = {
        "id": session_id,
        "system_prompt": """Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente.""",
        "messages": [],
        "objectives": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Guardar en SQLite
    conn = _get_connection()
    conn.execute(
        "INSERT INTO sessions (id, system_prompt, objectives, messages, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (
            session["id"],
            session["system_prompt"],
            json.dumps(session["objectives"]),
            json.dumps(session["messages"]),
            session["created_at"],
            session["updated_at"]
        )
    )
    conn.commit()
    conn.close()
    
    return session


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene una sesión por su ID.
    
    Recupera una sesión previamente creada del almacenamiento.
    Retorna None si la sesión no existe.
    
    Args:
        session_id: ID de la sesión a recuperar
    
    Returns:
        Dict de sesión o None si no existe
    
    Example:
        session = create_session()
        retrieved = get_session(session["id"])
        print(retrieved["id"] == session["id"])  # True
        
        not_found = get_session("id-inexistente")
        print(not_found)  # None
    """
    conn = _get_connection()
    cursor = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        "id": row["id"],
        "system_prompt": row["system_prompt"],
        "messages": json.loads(row["messages"]),
        "objectives": json.loads(row["objectives"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }


def update_session(session_id: str, updates: Dict[str, Any]) -> bool:
    """
    Actualiza una sesión existente.
    
    Modifica los campos especificados de una sesión y actualiza el timestamp.
    Los campos no especificados mantienen su valor actual.
    
    Args:
        session_id: ID de la sesión a actualizar
        updates: Campos a actualizar (dict parcial)
    
    Returns:
        True si se actualizó, False si la sesión no existe
    
    Example:
        session = create_session()
        
        # Actualizar system prompt
        success = update_session(session["id"], {
            "system_prompt": "Nuevo prompt personalizado"
        })
        print(success)  # True
        
        # Actualizar con mensaje
        update_session(session["id"], {
            "messages": [...session["messages"], new_message]
        })
    
    Example:
        # Intentar actualizar sesión inexistente
        result = update_session("id-inexistente", {"system_prompt": "nuevo"})
        print(result)  # False
    """
    conn = _get_connection()
    
    # Verificar existencia
    cursor = conn.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
    if not cursor.fetchone():
        conn.close()
        return False
    
    # Construir UPDATE dinámico
    fields = []
    values = []
    
    for key, value in updates.items():
        if key in ["system_prompt", "objectives", "messages"]:
            fields.append(f"{key} = ?")
            values.append(json.dumps(value) if isinstance(value, list) else value)
        elif key in ["created_at", "updated_at"]:
            fields.append(f"{key} = ?")
            values.append(value if isinstance(value, str) else datetime.now().isoformat())
    
    if not fields:
        conn.close()
        return False
    
    # Añadir updated_at y session_id
    fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())
    values.append(session_id)
    
    query = f"UPDATE sessions SET {', '.join(fields)} WHERE id = ?"
    conn.execute(query, values)
    conn.commit()
    conn.close()
    
    return True


def delete_session(session_id: str) -> bool:
    """
    Elimina una sesión del almacenamiento.
    
    Remueve permanentemente una sesión del sistema.
    Usar con precaución - no hay recuperación.
    
    Args:
        session_id: ID de la sesión a eliminar
    
    Returns:
        True si se eliminó, False si no existía
    
    Example:
        session = create_session()
        deleted = delete_session(session["id"])
        print(deleted)  # True
        print(get_session(session["id"]))  # None
    """
    conn = _get_connection()
    cursor = conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return deleted


def list_sessions() -> List[str]:
    """
    Lista todos los IDs de sesiones activas.
    
    Retorna un array con los IDs de todas las sesiones actualmente en memoria.
    Útil para debugging y administración.
    
    Returns:
        Array de IDs de sesiones
    
    Example:
        create_session("session-1")
        create_session("session-2")
        
        all_sessions = list_sessions()
        print(all_sessions)  # ['session-1', 'session-2']
    """
    conn = _get_connection()
    cursor = conn.execute("SELECT id FROM sessions ORDER BY updated_at DESC")
    ids = [row["id"] for row in cursor.fetchall()]
    conn.close()
    
    return ids


def get_session_stats() -> Dict[str, Any]:
    """
    Obtiene estadísticas del almacenamiento de sesiones.
    
    Retorna información sobre el estado actual del almacenamiento:
    - Cantidad de sesiones activas
    - Timestamp de esta consulta
    
    Returns:
        Dict con count y timestamp
    
    Example:
        create_session()
        create_session()
        
        stats = get_session_stats()
        print(stats["count"])  # 2
        print(stats["timestamp"])  # Date
    """
    conn = _get_connection()
    cursor = conn.execute("SELECT COUNT(*) as count FROM sessions")
    count = cursor.fetchone()["count"]
    conn.close()
    
    return {
        "count": count,
        "timestamp": datetime.now().isoformat()
    }

"""
Socket Lifecycle Manager - Gestión segura de sockets UNIX para Kitty

Módulo atómico (≤3 funciones públicas) - Filosofía ARES

Funcionalidades:
1. validate_socket_path - Valida ruta y permisos del socket
2. cleanup_orphan_socket - Limpia sockets huérfanos automáticamente
3. wait_for_socket_ready - Espera con timeout y validación activa
4. generate_unique_socket - Genera nombre único con timestamp

Flujo de Datos:
- Entrada: Ruta de socket (con o sin prefijo 'unix:')
- Procesamiento: Validación de existencia, permisos y estado del proceso
- Salida: Booleanos de éxito + mensajes de error descriptivos

Ejemplo de Uso:
```python
from modules.core.socket_manager import (
    validate_socket_path,
    cleanup_orphan_socket,
    wait_for_socket_ready,
    generate_unique_socket
)

# Ejemplo 1: Validar socket
valid, error = validate_socket_path("/tmp/mykitty")
if not valid:
    print(f"Socket inválido: {error}")

# Ejemplo 2: Limpiar socket huérfano
if cleanup_orphan_socket("/tmp/mykitty"):
    print("Socket limpio, listo para usar")

# Ejemplo 3: Esperar socket ready
success, msg = wait_for_socket_ready("unix:/tmp/mykitty", timeout=15)
if success:
    print(f"Socket listo: {msg}")

# Ejemplo 4: Generar socket único
socket_name = generate_unique_socket("ares_session_diaria")
# Resultado: "/tmp/ares_session_diaria_1710604800_a3f2"
```
"""

import os
import time
import subprocess
from pathlib import Path
from typing import Tuple, Optional


# ============================================================================
# CONSTANTES
# ============================================================================

DEFAULT_SOCKET_DIR = Path("/tmp")
"""Directorio por defecto para sockets UNIX"""

DEFAULT_POLL_INTERVAL = 0.3
"""Intervalo de polling en segundos para wait_for_socket_ready"""

DEFAULT_SOCKET_TIMEOUT = 15
"""Timeout por defecto en segundos para wait_for_socket_ready"""


# ============================================================================
# FUNCIONES AUXILIARES (PRIVADAS)
# ============================================================================

def _normalize_socket_path(socket_path: str) -> str:
    """
    Normaliza ruta de socket removiendo prefijo 'unix:' si existe.
    
    Args:
        socket_path: Ruta del socket (ej. "unix:/tmp/mykitty" o "/tmp/mykitty")
    
    Returns:
        Ruta normalizada sin prefijo
    
    Example:
        _normalize_socket_path("unix:/tmp/mykitty")  # "/tmp/mykitty"
        _normalize_socket_path("/tmp/mykitty")       # "/tmp/mykitty"
    """
    return socket_path.replace('unix:', '')


def _format_socket_address(socket_path: str) -> str:
    """
    Formatea ruta para uso con kitty @ --to (añade 'unix:' si no existe).
    
    Args:
        socket_path: Ruta del socket
    
    Returns:
        Ruta con prefijo 'unix:' para comandos kitty
    
    Example:
        _format_socket_address("/tmp/mykitty")    # "unix:/tmp/mykitty"
        _format_socket_address("unix:/tmp/mykitty") # "unix:/tmp/mykitty"
    """
    normalized = _normalize_socket_path(socket_path)
    return f"unix:{normalized}"


def _is_socket_orphan(socket_path: str) -> bool:
    """
    Verifica si un socket está huérfano (sin proceso Kitty escuchando).
    
    Un socket se considera huérfano si:
    - El archivo existe pero ningún proceso responde
    - El comando kitty @ falla o timeout
    
    Args:
        socket_path: Ruta del socket (con o sin 'unix:')
    
    Returns:
        True si está huérfano o no existe, False si hay Kitty activo
    
    Example:
        _is_socket_orphan("/tmp/mykitty")  # True si no hay Kitty escuchando
    """
    normalized = _normalize_socket_path(socket_path)
    
    if not os.path.exists(normalized):
        return True  # No existe, técnicamente "huérfano"
    
    try:
        address = _format_socket_address(normalized)
        result = subprocess.run(
            ["kitty", "@", "--to", address, "ls"],
            capture_output=True,
            timeout=2
        )
        # Si kitty responde OK, NO está huérfano
        return result.returncode != 0
    except subprocess.TimeoutExpired:
        return True  # Timeout = huérfano
    except FileNotFoundError:
        return True  # Kitty no instalado
    except Exception:
        return True  # Cualquier error = asumimos huérfano


# ============================================================================
# FUNCIONES EXPORTADAS (API PÚBLICA)
# ============================================================================

def validate_socket_path(socket_path: str) -> Tuple[bool, str]:
    """
    Valida que la ruta del socket sea válida y tenga permisos.
    
    Verificaciones realizadas:
    1. Directorio padre existe
    2. Directorio tiene permisos de escritura
    3. Ruta no está en uso por otro proceso Kitty
    
    Args:
        socket_path: Ruta del socket (ej. "/tmp/mykitty" o "unix:/tmp/mykitty")
    
    Returns:
        Tupla (es_valido, mensaje_error):
        - (True, "") si es válido
        - (False, "mensaje descriptivo") si hay problema
    
    Example:
        valid, error = validate_socket_path("/tmp/mykitty")
        if not valid:
            print(f"Error: {error}")
        
        # También funciona con prefijo 'unix:'
        valid, error = validate_socket_path("unix:/tmp/mykitty")
    """
    normalized = _normalize_socket_path(socket_path)
    
    # Verificar que la ruta no esté vacía
    if not normalized:
        return False, "Ruta de socket vacía"
    
    # Verificar directorio padre
    parent_dir = Path(normalized).parent
    
    if not parent_dir.exists():
        return False, f"Directorio no existe: {parent_dir}"
    
    if not os.access(parent_dir, os.W_OK):
        return False, f"Sin permisos de escritura en: {parent_dir}"
    
    # Verificar si ya existe un socket
    if os.path.exists(normalized):
        # Verificar tipo de archivo (debe ser socket)
        if not os.path.isfile(normalized) and not os.path.islink(normalized):
            # Podría ser directorio u otro tipo
            pass
        
        # Verificar si está en uso
        if not _is_socket_orphan(normalized):
            return False, f"Socket en uso por otro proceso Kitty: {normalized}"
    
    return True, ""


def cleanup_orphan_socket(socket_path: str, force: bool = False) -> Tuple[bool, str]:
    """
    Limpia socket huérfano si existe.
    
    Comportamiento:
    - Si el socket NO existe: retorna True (ya está "limpio")
    - Si el socket existe y está huérfano: lo elimina y retorna True
    - Si el socket existe y está EN USO:
      - force=False: retorna False (no tocar)
      - force=True: intenta eliminar igual
    
    Args:
        socket_path: Ruta del socket (ej. "/tmp/mykitty")
        force: Si True, elimina incluso si parece estar en uso
    
    Returns:
        Tupla (exitoso, mensaje):
        - (True, "mensaje") si se limpió o no existía
        - (False, "mensaje") si estaba en uso y force=False
    
    Example:
        # Limpieza segura (no fuerza)
        success, msg = cleanup_orphan_socket("/tmp/mykitty")
        if success:
            print(f"Socket limpio: {msg}")
        
        # Limpieza forzada
        success, msg = cleanup_orphan_socket("/tmp/mykitty", force=True)
    """
    normalized = _normalize_socket_path(socket_path)
    
    # Si no existe, ya está "limpio"
    if not os.path.exists(normalized):
        return True, "Socket no existía"
    
    # Verificar si está huérfano
    is_orphan = _is_socket_orphan(normalized)
    
    if not is_orphan and not force:
        return False, f"Socket en uso por Kitty activo (usa --force para eliminar)"
    
    # Intentar eliminar
    try:
        os.remove(normalized)
        return True, "Socket huérfano eliminado"
    except OSError as e:
        return False, f"Error al eliminar socket: {e}"
    except PermissionError as e:
        return False, f"Sin permisos para eliminar socket: {e}"


def wait_for_socket_ready(socket_path: str, timeout: int = DEFAULT_SOCKET_TIMEOUT, 
                          poll_interval: float = DEFAULT_POLL_INTERVAL) -> Tuple[bool, str]:
    """
    Espera a que el socket esté listo y responsivo.
    
    Realiza polling activo verificando:
    1. Existencia física del archivo socket
    2. Capacidad de respuesta a comandos kitty @
    
    Args:
        socket_path: Ruta del socket (ej. "/tmp/mykitty" o "unix:/tmp/mykitty")
        timeout: Tiempo máximo de espera en segundos (default: 15)
        poll_interval: Intervalo entre intentos en segundos (default: 0.3)
    
    Returns:
        Tupla (exitoso, mensaje):
        - (True, "Socket ready") si está operativo
        - (False, "Timeout...") si excedió tiempo de espera
    
    Example:
        # Espera con timeout por defecto (15s)
        success, msg = wait_for_socket_ready("unix:/tmp/mykitty")
        if success:
            print("✅ Socket listo para usar")
        
        # Espera con timeout personalizado
        success, msg = wait_for_socket_ready("/tmp/mykitty", timeout=30)
    """
    normalized = _normalize_socket_path(socket_path)
    address = _format_socket_address(normalized)
    
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < timeout:
        attempts += 1
        
        # Verificar existencia física
        if os.path.exists(normalized):
            # Verificar respuesta activa
            try:
                result = subprocess.run(
                    ["kitty", "@", "--to", address, "ls"],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return True, "Socket ready"
            except subprocess.TimeoutExpired:
                pass  # Reintentar
            except FileNotFoundError:
                return False, "Comando 'kitty' no encontrado"
            except Exception as e:
                pass  # Reintentar
        
        # Esperar antes del próximo intento
        time.sleep(poll_interval)
    
    elapsed = time.time() - start_time
    return False, f"Timeout ({elapsed:.1f}s) esperando socket: {normalized}"


def generate_unique_socket(base_name: str = "ares_session") -> str:
    """
    Genera nombre de socket único con timestamp y hash aleatorio.
    
    Formato: /tmp/{base_name}_{timestamp}_{random_hex}
    
    El timestamp permite identificar cuándo se creó la sesión.
    El hash aleatorio (4 caracteres hex) previene colisiones incluso
    dentro del mismo segundo.
    
    Args:
        base_name: Nombre base para el socket (default: "ares_session")
    
    Returns:
        Ruta completa del socket único
    
    Example:
        # Generar socket único
        socket_path = generate_unique_socket("ares_session_diaria")
        # Resultado: "/tmp/ares_session_diaria_1710604800_a3f2"
        
        # Usar con nombre por defecto
        socket_path = generate_unique_socket()
        # Resultado: "/tmp/ares_session_1710604800_b7e1"
    """
    import secrets
    
    timestamp = int(time.time())
    random_suffix = secrets.token_hex(2)  # 4 caracteres hex
    
    # Sanitizar nombre base (solo caracteres alfanuméricos y guiones)
    safe_base = "".join(c if c.isalnum() or c in '-_' else '_' for c in base_name)
    
    return f"/tmp/{safe_base}_{timestamp}_{random_suffix}"


def get_socket_info(socket_path: str) -> dict:
    """
    Obtiene información detallada sobre un socket.
    
    Args:
        socket_path: Ruta del socket
    
    Returns:
        Diccionario con información:
        - exists: bool - Si el archivo existe
        - is_socket: bool - Si es un socket UNIX
        - is_orphan: bool - Si está huérfano
        - is_responsive: bool - Si responde a comandos
        - permissions: str - Permisos del archivo (ej. "srwxr-xr-x")
        - owner_uid: int - UID del propietario
        - error: str - Mensaje de error si aplica
    
    Example:
        info = get_socket_info("/tmp/mykitty")
        print(f"Existe: {info['exists']}")
        print(f"Responsivo: {info['is_responsive']}")
    """
    import stat
    
    normalized = _normalize_socket_path(socket_path)
    info = {
        "exists": False,
        "is_socket": False,
        "is_orphan": True,
        "is_responsive": False,
        "permissions": None,
        "owner_uid": None,
        "error": None
    }
    
    # Verificar existencia
    if not os.path.exists(normalized):
        info["error"] = "Socket no existe"
        return info
    
    info["exists"] = True
    
    try:
        file_stat = os.stat(normalized)
        mode = file_stat.st_mode
        
        # Verificar si es socket
        info["is_socket"] = stat.S_ISSOCK(mode)
        
        # Permisos en formato legible
        info["permissions"] = stat.filemode(mode).strip()
        info["owner_uid"] = file_stat.st_uid
        
        # Verificar si responde
        address = _format_socket_address(normalized)
        try:
            result = subprocess.run(
                ["kitty", "@", "--to", address, "ls"],
                capture_output=True,
                timeout=2
            )
            info["is_responsive"] = (result.returncode == 0)
            info["is_orphan"] = not info["is_responsive"]
        except:
            info["is_orphan"] = True
            
    except OSError as e:
        info["error"] = str(e)
    
    return info

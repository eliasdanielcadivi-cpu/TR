"""
AgenteDeCambio Core - Módulos de lógica de negocio

Módulos atómicos (≤3 funciones cada uno) - Filosofía ARES

Módulos disponibles:
- deepseek_connector: Conexión con DeepSeek API (2 funciones)
- delta_calculator: Cálculo de deriva de prompts (4 funciones)
- prompt_engine: Gestión de system prompts (4 funciones)
- session_manager: Gestión de sesiones (6 funciones)
- socket_manager: Gestión de sockets UNIX (4 funciones)

Ejemplo de Uso:
```python
from modules.core import (
    create_completion,
    create_completion_stream,
    calculate,
    compare,
    threshold,
    requires_approval,
    build_system_prompt,
    update_prompt,
    negotiate_change,
    get_default_prompt,
    create_session,
    get_session,
    update_session,
    delete_session,
    list_sessions,
    get_session_stats,
    # Socket Manager
    validate_socket_path,
    cleanup_orphan_socket,
    wait_for_socket_ready,
    generate_unique_socket,
    get_socket_info
)
```
"""

from .deepseek_connector import (
    create_completion,
    create_completion_stream,
    DEEPSEEK_API_URL
)

from .delta_calculator import (
    calculate,
    compare,
    threshold,
    requires_approval,
    DeltaComparison,
    DEFAULT_THRESHOLD
)

from .prompt_engine import (
    build_system_prompt,
    update_prompt,
    negotiate_change,
    get_default_prompt,
    BuildPromptParams,
    PromptUpdateResult,
    NegotiationResult,
    DEFAULT_SYSTEM_PROMPT
)

from .session_manager import (
    create_session,
    get_session,
    update_session,
    delete_session,
    list_sessions,
    get_session_stats,
    init_db,
    DB_PATH
)

from .socket_manager import (
    validate_socket_path,
    cleanup_orphan_socket,
    wait_for_socket_ready,
    generate_unique_socket,
    get_socket_info,
    DEFAULT_SOCKET_TIMEOUT,
    DEFAULT_POLL_INTERVAL
)

from .window_registry import (
    register_window,
    get_window_by_session,
    get_session_by_window,
    list_active_windows,
    unregister_window,
    update_window_id,
    cleanup_stale_windows,
    find_window_by_socket,
    get_registry_stats,
    init_db as init_window_db
)

__all__ = [
    # deepseek_connector
    "create_completion",
    "create_completion_stream",
    "DEEPSEEK_API_URL",

    # delta_calculator
    "calculate",
    "compare",
    "threshold",
    "requires_approval",
    "DeltaComparison",
    "DEFAULT_THRESHOLD",

    # prompt_engine
    "build_system_prompt",
    "update_prompt",
    "negotiate_change",
    "get_default_prompt",
    "BuildPromptParams",
    "PromptUpdateResult",
    "NegotiationResult",
    "DEFAULT_SYSTEM_PROMPT",

    # session_manager
    "create_session",
    "get_session",
    "update_session",
    "delete_session",
    "list_sessions",
    "get_session_stats",
    "init_db",
    "DB_PATH",

    # socket_manager
    "validate_socket_path",
    "cleanup_orphan_socket",
    "wait_for_socket_ready",
    "generate_unique_socket",
    "get_socket_info",
    "DEFAULT_SOCKET_TIMEOUT",
    "DEFAULT_POLL_INTERVAL",

    # window_registry
    "register_window",
    "get_window_by_session",
    "get_session_by_window",
    "list_active_windows",
    "unregister_window",
    "update_window_id",
    "cleanup_stale_windows",
    "find_window_by_socket",
    "get_registry_stats",
    "init_window_db"
]

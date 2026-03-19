# Agente de Cambio - Módulos Reutilizables

## Módulo: AgenteDeCambio Core (traducción TypeScript → Python)

---

## 1. Problema Detectado

**Síntoma:** Módulos de Agente-De-Cambio-STABLE están en TypeScript/Node.js → no reutilizables desde Python/ARES.

**Necesidad:** Traducir módulos clave a Python manteniendo:
- Máximo 3 funciones por módulo (modularidad atómica ARES)
- Mismas firmas y comportamiento
- Documentación granular para referencia futura

---

## 2. Causa Raíz

Arquitectura original diseñada para web:
- TypeScript para type safety en frontend/backend
- npm workspaces para módulos compartidos
- Socket.IO para comunicación en tiempo real

**Para CLI/ARES:**
- Python nativo (mismo ecosistema que ARES)
- SQLite para persistencia (en lugar de memoria)
- Unix sockets o polling asíncrono

---

## 3. API Disponible (Módulos a Traducir)

### 3.1 deepseek-connector

**Original TypeScript (2 funciones):**
```typescript
createCompletion(request: DeepSeekCompletionRequest): Promise<DeepSeekCompletionResponse>
createCompletionStream(request: DeepSeekCompletionRequest): AsyncGenerator<DeepSeekStreamChunk>
```

**Traducción Python:**
```python
# modules/core/deepseek_connector.py

import httpx
from typing import List, Dict, AsyncGenerator

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

def create_completion(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "deepseek-chat",
    temperature: float = 0.7,
    max_tokens: int = 4096
) -> Dict:
    """
    Solicita completación síncrona a DeepSeek API.
    
    Args:
        messages: Lista de mensajes [{role, content}, ...]
        api_key: API Key de DeepSeek
        model: Modelo a usar (deepseek-chat o deepseek-reasoner)
        temperature: 0.0-2.0 (0.7 default)
        max_tokens: Máximo tokens a generar (4096 default)
    
    Returns:
        Dict con respuesta completa:
        {
            "id": "chatcmpl-...",
            "choices": [{"message": {"role": "assistant", "content": "..."}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 50, "total_tokens": 60}
        }
    
    Raises:
        httpx.HTTPStatusError: Si API retorna error (401, 429, 5xx)
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    
    response = httpx.post(
        DEEPSEEK_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    response.raise_for_status()
    return response.json()


async def create_completion_stream(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "deepseek-chat",
    temperature: float = 0.7,
    max_tokens: int = 4096
) -> AsyncGenerator[str, None]:
    """
    Generator asíncrono para streaming de respuesta (SSE).
    
    Args:
        messages: Lista de mensajes
        api_key: API Key de DeepSeek
        model: Modelo a usar
        temperature: 0.0-2.0
        max_tokens: Máximo tokens
    
    Yields:
        Chunks de texto (caracteres o palabras parciales)
    
    Example:
        async for chunk in create_completion_stream(messages, api_key):
            print(chunk, end="", flush=True)
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }
    
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            DEEPSEEK_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "text/event-stream"
            },
            json=payload
        ) as response:
            response.raise_for_status()
            buffer = ""
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        return
                    
                    try:
                        chunk = httpx.get("data", lambda: json.loads(data))
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
```

---

### 3.2 delta-calculator

**Original TypeScript (4 funciones):**
```typescript
calculate(oldPrompt: str, newPrompt: str) -> float
compare(oldPrompt: str, newPrompt: str) -> DeltaComparison
threshold() -> float
requiresApproval(deltaScore: float) -> bool
```

**Traducción Python:**
```python
# modules/core/delta_calculator.py

import os
from typing import Dict, NamedTuple

DEFAULT_THRESHOLD = 0.3

class DeltaComparison(NamedTuple):
    """Resultado detallado de comparación de prompts"""
    delta_score: float
    threshold: float
    requires_approval: bool
    changes: Dict[str, int]


def calculate(old_prompt: str, new_prompt: str) -> float:
    """
    Calcula deriva entre dos prompts (0.0 a 1.0).
    
    Algoritmo: Diferencia de longitud normalizada.
    TODO: Implementar cosine similarity para análisis semántico.
    
    Args:
        old_prompt: Versión anterior del prompt
        new_prompt: Nueva versión del prompt
    
    Returns:
        Score de deriva (0.0 = sin cambios, 1.0 = cambio total)
    
    Example:
        delta = calculate("prompt corto", "prompt mucho más largo")
        print(f"Deriva: {delta * 100:.2f}%")
    """
    if not old_prompt or not new_prompt:
        return 1.0
    
    length_diff = abs(len(new_prompt) - len(old_prompt))
    max_length = max(len(old_prompt), len(new_prompt), 1)
    return length_diff / max_length


def compare(old_prompt: str, new_prompt: str) -> DeltaComparison:
    """
    Compara dos prompts y retorna métricas detalladas.
    
    Args:
        old_prompt: Versión anterior
        new_prompt: Nueva versión
    
    Returns:
        DeltaComparison con:
        - delta_score: Score de deriva
        - threshold: Umbral configurado
        - requires_approval: Si excede umbral
        - changes: {additions, deletions, semantic_shift}
    """
    delta_score = calculate(old_prompt, new_prompt)
    threshold_value = threshold()
    
    length_diff = len(new_prompt) - len(old_prompt)
    additions = max(0, length_diff)
    deletions = max(0, -length_diff)
    
    return DeltaComparison(
        delta_score=delta_score,
        threshold=threshold_value,
        requires_approval=delta_score > threshold_value,
        changes={
            "additions": additions,
            "deletions": deletions,
            "semantic_shift": delta_score
        }
    )


def threshold() -> float:
    """
    Obtiene umbral configurado para aprobación de cambios.
    
    Lee variable de entorno PROMPT_DELTA_THRESHOLD o retorna default.
    
    Returns:
        Umbral de 0.0 a 1.0 (default: 0.3)
    """
    env_threshold = os.getenv("PROMPT_DELTA_THRESHOLD")
    if env_threshold:
        try:
            parsed = float(env_threshold)
            if 0 <= parsed <= 1:
                return parsed
        except ValueError:
            pass
    return DEFAULT_THRESHOLD


def requires_approval(delta_score: float) -> bool:
    """
    Determina si un cambio requiere aprobación.
    
    Args:
        delta_score: Score de deriva (0.0-1.0)
    
    Returns:
        True si requiere aprobación, False si es cambio menor
    """
    return delta_score > threshold()
```

---

### 3.3 prompt-engine

**Original TypeScript (4 funciones):**
```typescript
buildSystemPrompt(params: BuildPromptParams) -> str
updatePrompt(session: Session, newPrompt: str, force: bool) -> PromptUpdateResult
negotiateChange(oldPrompt: str, newPrompt: str) -> NegotiationResult
getDefaultPrompt() -> str
```

**Traducción Python:**
```python
# modules/core/prompt_engine.py

from typing import List, Dict, NamedTuple, Optional
from dataclasses import dataclass
from datetime import datetime

DEFAULT_SYSTEM_PROMPT = """Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente."""


@dataclass
class BuildPromptParams:
    """Parámetros para construir system prompt"""
    base_prompt: Optional[str] = None
    objectives: Optional[List[str]] = None
    mode: str = "chat"  # "chat" o "questionnaire"


@dataclass
class PromptUpdateResult:
    """Resultado de actualización de prompt"""
    success: bool
    requires_approval: bool
    delta_score: float
    mutation: Optional[Dict] = None


def build_system_prompt(params: BuildPromptParams) -> str:
    """
    Construye system prompt con contexto adicional.
    
    Combina prompt base con:
    - Objetivos activos del usuario
    - Instrucciones específicas del modo
    
    Args:
        params: Parámetros (base_prompt, objectives, mode)
    
    Returns:
        System prompt completo construido
    
    Example:
        prompt = build_system_prompt(BuildPromptParams(
            base_prompt="Eres un asistente de código",
            objectives=["Ayudar con Python", "Enseñar buenas prácticas"],
            mode="chat"
        ))
    """
    base = params.base_prompt or DEFAULT_SYSTEM_PROMPT
    
    # Contexto de objetivos
    if params.objectives:
        objectives_context = "\n\nOBJETIVOS ACTIVOS:\n" + "\n".join(
            f"- {obj}" for obj in params.objectives
        )
    else:
        objectives_context = ""
    
    # Instrucciones por modo
    if params.mode == "questionnaire":
        mode_instruction = "\n\nMODO CUESTIONARIO: Estructura tu respuesta como una pregunta con opciones claras. Usa formato JSON para las opciones."
    else:
        mode_instruction = "\n\nMODO CHAT: Responde de manera conversacional y natural."
    
    return f"{base}{objectives_context}{mode_instruction}"


def update_prompt(
    session: Dict,
    new_prompt: str,
    force: bool = False
) -> PromptUpdateResult:
    """
    Actualiza system prompt de sesión con validación de deriva.
    
    Args:
        session: Dict de sesión (de session_manager)
        new_prompt: Nuevo contenido del prompt
        force: Si True, omite validación de aprobación
    
    Returns:
        PromptUpdateResult con éxito, delta, y mutación si aplica
    """
    from delta_calculator import calculate, requires_approval
    
    old_prompt = session.get("system_prompt", "")
    delta_score = calculate(old_prompt, new_prompt)
    needs_approval = requires_approval(delta_score)
    
    if needs_approval and not force:
        return PromptUpdateResult(
            success=False,
            requires_approval=True,
            delta_score=delta_score,
            mutation=None
        )
    
    # Aplicar actualización
    session["system_prompt"] = new_prompt
    session["updated_at"] = datetime.now().isoformat()
    
    mutation = {
        "id": f"mut_{int(datetime.now().timestamp() * 1000)}",
        "timestamp": datetime.now().isoformat(),
        "change": f"Prompt actualizado ({len(new_prompt) - len(old_prompt)} chars)",
        "reason": "Update via prompt engine",
        "delta_impact": delta_score,
        "approved": not needs_approval or force
    }
    
    return PromptUpdateResult(
        success=True,
        requires_approval=False,
        delta_score=delta_score,
        mutation=mutation
    )


def negotiate_change(old_prompt: str, new_prompt: str) -> Dict:
    """
    Negocia un cambio de prompt propuesto.
    
    Analiza magnitud del cambio y determina recomendación.
    
    Args:
        old_prompt: Prompt actual
        new_prompt: Prompt propuesto
    
    Returns:
        Dict con:
        - delta_score: 0.0-1.0
        - recommendation: "ACCEPT" | "REVIEW" | "REJECT"
        - reason: Explicación
        - negotiable: Si se puede negociar
    """
    from delta_calculator import compare
    
    comparison = compare(old_prompt, new_prompt)
    
    # Determinar recomendación
    if comparison.delta_score < 0.1:
        recommendation = "ACCEPT"
        reason = "Cambio menor, seguro para aplicar automáticamente"
    elif comparison.delta_score < comparison.threshold:
        recommendation = "REVIEW"
        reason = "Cambio moderado, revisar antes de aplicar"
    elif comparison.delta_score < 0.7:
        recommendation = "REVIEW"
        reason = "Cambio significativo, requiere aprobación explícita"
    else:
        recommendation = "REJECT"
        reason = "Cambio demasiado drástico, puede desviar el objetivo"
    
    return {
        "delta_score": comparison.delta_score,
        "threshold": comparison.threshold,
        "requires_approval": comparison.requires_approval,
        "recommendation": recommendation,
        "reason": reason,
        "negotiable": comparison.delta_score < 0.7,
        "changes": comparison.changes
    }


def get_default_prompt() -> str:
    """
    Obtiene el prompt por defecto.
    
    Returns:
        System prompt base (DEFAULT_SYSTEM_PROMPT)
    """
    return DEFAULT_SYSTEM_PROMPT
```

---

### 3.4 session-manager

**Original TypeScript (6 funciones):**
```typescript
createSession(sessionId?: str) -> Session
getSession(sessionId: str) -> Session | undefined
updateSession(sessionId: str, updates: Partial<Session>) -> bool
deleteSession(sessionId: str) -> bool
listSessions() -> str[]
getSessionStats() -> SessionStats
```

**Traducción Python (con SQLite):**
```python
# modules/core/session_manager.py

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

DB_PATH = Path.home() / ".tron" / "agente_de_cambio" / "sessions.db"

def _get_connection() -> sqlite3.Connection:
    """Obtiene conexión SQLite con row factory"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Inicializa base de datos de sesiones"""
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


def create_session(session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Crea nueva sesión de conversación.
    
    Args:
        session_id: ID opcional (genera automático si no se proporciona)
    
    Returns:
        Dict de sesión con campos inicializados
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
    Obtiene sesión existente por ID.
    
    Args:
        session_id: ID de sesión a recuperar
    
    Returns:
        Dict de sesión o None si no existe
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
    Actualiza campos de sesión (parcial).
    
    Args:
        session_id: ID de sesión a actualizar
        updates: Campos a actualizar (dict parcial)
    
    Returns:
        True si se actualizó, False si no existe
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
    Elimina sesión permanentemente.
    
    Args:
        session_id: ID de sesión a eliminar
    
    Returns:
        True si se eliminó, False si no existía
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
    
    Returns:
        Lista de IDs de sesiones
    """
    conn = _get_connection()
    cursor = conn.execute("SELECT id FROM sessions ORDER BY updated_at DESC")
    ids = [row["id"] for row in cursor.fetchall()]
    conn.close()
    
    return ids


def get_session_stats() -> Dict[str, Any]:
    """
    Obtiene estadísticas del almacenamiento.
    
    Returns:
        Dict con count y timestamp
    """
    conn = _get_connection()
    cursor = conn.execute("SELECT COUNT(*) as count FROM sessions")
    count = cursor.fetchone()["count"]
    conn.close()
    
    return {
        "count": count,
        "timestamp": datetime.now().isoformat()
    }
```

---

## 4. Solución Implementada

### Estructura de Módulos Python

```
modules/core/
├── __init__.py              # Re-exports
├── deepseek_connector.py    # 2 funciones (streaming)
├── delta_calculator.py      # 4 funciones (deriva)
├── prompt_engine.py         # 4 funciones (gestión prompts)
└── session_manager.py       # 6 funciones (SQLite)
```

### Dependencias

```python
# requirements.txt
httpx>=0.25.0        # Cliente HTTP asíncrono
sqlite3              # Incluído en stdlib
```

---

## 5. Flujo de Trabajo (Ejemplo Completo)

```python
from modules.core import (
    create_session,
    get_session,
    update_session,
    build_system_prompt,
    create_completion_stream,
    calculate_delta,
    requires_approval
)

async def ejemplo_completo():
    # 1. Crear sesión
    session = create_session()
    print(f"Sesión creada: {session['id']}")
    
    # 2. Añadir mensaje de usuario
    user_message = {"role": "user", "content": "¿Qué es TypeScript?"}
    session["messages"].append(user_message)
    update_session(session["id"], {"messages": session["messages"]})
    
    # 3. Construir system prompt con contexto
    prompt = build_system_prompt(BuildPromptParams(
        objectives=["Enseñar TypeScript", "Explicar tipos"],
        mode="chat"
    ))
    
    # 4. Preparar mensajes para DeepSeek
    messages = [
        {"role": "system", "content": prompt},
        *session["messages"][-10:]  # Últimos 10 para contexto
    ]
    
    # 5. Stream de respuesta
    api_key = os.getenv("DEEPSEEK_API_KEY")
    full_response = ""
    
    async for chunk in create_completion_stream(messages, api_key):
        print(chunk, end="", flush=True)
        full_response += chunk
    
    # 6. Añadir respuesta a sesión
    assistant_message = {"role": "assistant", "content": full_response}
    session["messages"].append(assistant_message)
    update_session(session["id"], {"messages": session["messages"]})
    
    # 7. Calcular delta del prompt
    old_prompt = session["system_prompt"]
    delta = calculate_delta(old_prompt, full_response)
    
    if requires_approval(delta):
        print(f"\n⚠️  Deriva {delta*100:.2f}% excede umbral - requiere aprobación")
    else:
        print(f"\n✅ Deriva {delta*100:.2f}% - cambio menor")
```

---

## 6. Checklist Debug

| Problema | Síntoma | Solución |
|----------|---------|----------|
| `httpx` no encontrado | ImportError | `pip install httpx` |
| SQLite locked | `sqlite3.OperationalError: database is locked` | Usar `check_same_thread=False` |
| Streaming no funciona | Texto aparece de una vez | Verificar `stream: True` en payload |
| Delta siempre 0 | Prompts idénticos | Debug: `print(repr(old_prompt), repr(new_prompt))` |
| API Key inválida | `httpx.HTTPStatusError: 401` | Verificar `DEEPSEEK_API_KEY` en `.env` |

---

## 7. Referencias

### Archivos Originales (TypeScript)

| Módulo | Ruta Original |
|--------|---------------|
| deepseek-connector | `modules/deepseek-connector/actions.ts` |
| delta-calculator | `modules/delta-calculator/actions.ts` |
| prompt-engine | `modules/prompt-engine/actions.ts` |
| session-manager | `modules/session-manager/actions.ts` |

### Documentación Relacionada

- `ARQUITECTURA-AGENTE-CAMBIO-15-03-2026.md` - Visión general del sistema
- `FLUJOS-INTERACCION-15-03-2026.md` - Flujos chat/cuestionario (próximo)

---

*Documento creado: 15-03-2026*  
*Última actualización: 15-03-2026*  
*Estado: [OK] - Módulos traducidos Python*

"""
DeepSeek Connector - Módulo para conexión con DeepSeek API

Módulo atómico (≤3 funciones) - Filosofía ARES

Funcionalidades:
1. create_completion - Solicita completación síncrona a DeepSeek API
2. create_completion_stream - Stream de respuesta en tiempo real (SSE)

Flujo de Datos:
- Entrada: Array de mensajes + API Key + configuración
- Procesamiento: HTTP POST a https://api.deepseek.com/chat/completions
- Salida: Respuesta JSON con contenido generado + estadísticas de tokens

Ejemplo de Uso:
```python
# Ejemplo 1: Completación síncrona
response = create_completion(
    messages=[
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola"}
    ],
    api_key="sk-..."
)
print(response["choices"][0]["message"]["content"])

# Ejemplo 2: Streaming
async for chunk in create_completion_stream(messages, api_key):
    print(chunk, end="", flush=True)
```
"""

import httpx
from typing import List, Dict, AsyncGenerator, Optional


# ============================================================================
# CONSTANTES
# ============================================================================

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
"""URL base de la API de DeepSeek"""


# ============================================================================
# FUNCIONES EXPORTADAS (API PÚBLICA DEL MÓDULO)
# ============================================================================

def create_completion(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "deepseek-chat",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    stream: bool = False
) -> Dict:
    """
    Solicita completación síncrona a DeepSeek API.
    
    Args:
        messages: Lista de mensajes [{role, content}, ...]
            - role: "system", "user", o "assistant"
            - content: Contenido textual del mensaje
        api_key: API Key de DeepSeek (obtener de https://platform.deepseek.com/api_keys)
        model: Modelo a usar (default: "deepseek-chat")
            - "deepseek-chat": Modo sin pensamiento (respuestas directas)
            - "deepseek-reasoner": Modo de pensamiento (razonamiento explícito)
        temperature: Creatividad de la respuesta (0.0-2.0, default: 0.7)
            - Valores bajos = más determinista
            - Valores altos = más creativo
        max_tokens: Máximo tokens a generar (default: 4096)
        stream: Habilitar streaming (default: False)
    
    Returns:
        Dict con respuesta completa:
        {
            "id": "chatcmpl-...",
            "choices": [{
                "message": {"role": "assistant", "content": "..."},
                "finish_reason": "stop",
                "index": 0
            }],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 50,
                "total_tokens": 60
            }
        }
    
    Raises:
        httpx.HTTPStatusError: Si la API retorna error (401, 429, 5xx)
    
    Nota: Comentar solo lo complejo o costoso de resolver.
        - La API de DeepSeek soporta caché de contexto (reduce costos)
        - Los campos prompt_cache_hit_tokens pueden estar presentes
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
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
        messages: Lista de mensajes [{role, content}, ...]
        api_key: API Key de DeepSeek
        model: Modelo a usar (default: "deepseek-chat")
        temperature: Creatividad de la respuesta (0.0-2.0, default: 0.7)
        max_tokens: Máximo tokens a generar (default: 4096)
    
    Yields:
        Chunks de texto (caracteres o palabras parciales)
    
    Example:
        async for chunk in create_completion_stream(messages, api_key):
            print(chunk, end="", flush=True)
    
    Nota: Comentar solo lo complejo o costoso de resolver.
        - Utiliza Server-Sent Events (SSE) para recibir respuesta
        - Los chunks se reciben en orden secuencial
        - La transmisión termina cuando se recibe "data: [DONE]"
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
                        chunk = httpx.get("data", lambda: __import__('json').loads(data))
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
                    except __import__('json').JSONDecodeError:
                        continue

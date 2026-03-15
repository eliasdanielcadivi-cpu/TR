# Agente de Cambio - Flujos de Interacción

## Módulo: Protocolos de Comunicación Chat/Cuestionario

---

## 1. Problema Detectado

**Síntoma:** Agente de Cambio original usa Socket.IO para comunicación en tiempo real → necesita adaptación para CLI TUI.

**Necesidad:** Definir flujos de interacción para:
- Modo chat (conversación fluida)
- Modo cuestionario (preguntas estructuradas)
- Transiciones entre modos
- Streaming carácter por carácter
- Edición de prompt en tiempo real

---

## 2. Causa Raíz

**Arquitectura Web Original:**
- Cliente: React + Socket.IO (WebSocket)
- Servidor: Node.js + Express + Socket.IO
- Eventos bidireccionales en tiempo real

**Arquitectura CLI Propuesta:**
- TUI: Python + textual/rich (o Ratatui Rust)
- Backend: Python nativo
- Comunicación: JSON vía Unix sockets o polling asíncrono

---

## 3. API Disponible (Eventos Socket.IO Originales)

### 3.1 Cliente → Servidor

| Evento | Payload | Descripción |
|--------|---------|-------------|
| `session:init` | `sessionId: string` | Inicializa o recupera sesión |
| `message:send` | `content, mode, context` | Envía mensaje del usuario |
| `prompt:update` | `content: string` | Actualiza system prompt manualmente |
| `option:select` | `questionId, optionId, comment` | Selecciona opción en cuestionario |
| `mode:set` | `mode: 'chat' | 'questionnaire'` | Cambia modo de interacción |
| `reasoning:toggle` | `isReasoning: boolean` | Activa/desactiva modo reasoning |

### 3.2 Servidor → Cliente

| Evento | Payload | Descripción |
|--------|---------|-------------|
| `message:stream` | `text: string` | Chunk de texto streaming |
| `message:complete` | `ChatMessage` | Mensaje completo del assistant |
| `prompt:mutation` | `PromptMutation` | Cambio registrado en prompt |
| `question:next` | `Question` | Nueva pregunta en cuestionario |
| `delta:update` | `DeltaMetrics` | Actualización métricas de deriva |
| `mode:switch` | `mode: string` | Confirmación de cambio de modo |
| `error` | `message: string` | Error ocurrido |

---

## 4. Solución Implementada (Flujos CLI)

### 4.1 Flujo Modo Chat

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario escribe mensaje en input TUI                     │
│    chat_widget.py: add_message("user", "¿Qué es TypeScript?")│
│    ↓                                                        │
│ 2. Widget emite JSON evento                                 │
│    {"widget_id": "chat_001", "evento": "input",             │
│     "datos": {"content": "¿Qué es TypeScript?",             │
│               "mode": "chat"}}                              │
│    ↓                                                        │
│ 3. Orquestador recibe evento                                │
│    main.py: handle_chat_event(event)                        │
│    ↓                                                        │
│ 4. Construye system prompt con contexto                     │
│    prompt_engine.build_system_prompt(params)                │
│    ↓                                                        │
│ 5. Prepara mensajes para DeepSeek (últimos 10)              │
│    messages = [system_prompt, *session.messages[-10:]]      │
│    ↓                                                        │
│ 6. Inicia streaming desde DeepSeek                          │
│    async for chunk in create_completion_stream(messages):   │
│    ↓                                                        │
│ 7. Cada chunk se envía al chat_widget                       │
│    json_protocol.emit("chat", "stream", {"chunk": text})    │
│    ↓                                                        │
│ 8. Widget renderiza carácter por carácter                   │
│    chat_widget.stream_text(chunk)                           │
│    ↓                                                        │
│ 9. Calcula delta del prompt                                 │
│    delta = calculate_delta(old_prompt, new_prompt)          │
│    ↓                                                        │
│ 10. Actualiza gauge widget                                  │
│    gauge_widget.set_value(delta)                            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Flujo Modo Cuestionario

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Orquestador cambia modo                                  │
│    tabs_widget.set_mode("questionnaire")                    │
│    json_protocol.emit("tabs", "switch", {"mode": "questionnaire"})│
│    ↓                                                        │
│ 2. table_widget muestra opciones                            │
│    rows = [                                                 │
│      ["Opción 1", "Profundizar en este tema"],              │
│      ["Opción 2", "Cambiar a otro aspecto"],                │
│      ["Opción 3", "Resumir lo aprendido"]                   │
│    ]                                                        │
│    ↓                                                        │
│ 3. Usuario selecciona opción (flechas + Enter)              │
│    table_widget.select_row(1)                               │
│    ↓                                                        │
│ 4. Widget emite JSON evento                                 │
│    {"widget_id": "table_001", "evento": "select",           │
│     "datos": {"row_id": "1", "value": "switch"}}            │
│    ↓                                                        │
│ 5. Orquestador procesa selección                            │
│    handle_option_select(question_id, option_id, comment)    │
│    ↓                                                        │
│ 6. Solicita siguiente pregunta a DeepSeek                   │
│    messages = [system_prompt, *conversation_history]        │
│    messages.append({"role": "system",                       │
│                     "content": "Genera siguiente pregunta"})│
│    ↓                                                        │
│ 7. DeepSeek genera pregunta JSON                            │
│    {                                                        │
│      "type": "single_choice",                               │
│      "question": "¿Cuál es el siguiente paso?",             │
│      "options": [...]                                       │
│    }                                                        │
│    ↓                                                        │
│ 8. table_widget actualiza filas                             │
│    table_widget.set_rows(new_question.options)              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Flujo Edición de Prompt

```
┌─────────────────────────────────────────────────────────────┐
│ 1. prompt_editor muestra system prompt actual               │
│    editor.set_text(session.system_prompt)                   │
│    ↓                                                        │
│ 2. Usuario edita texto (modo edición TUI)                   │
│    editor.handle_keypress(key)                              │
│    ↓                                                        │
│ 3. Widget emite JSON evento (cada cambio)                   │
│    {"widget_id": "editor_001", "evento": "edit",            │
│     "datos": {"text": "nuevo prompt..."}}                   │
│    ↓                                                        │
│ 4. Orquestador calcula delta                                │
│    delta = calculate_delta(old_prompt, new_prompt)          │
│    ↓                                                        │
│ 5. Si delta > threshold (0.3):                              │
│    dialog_widget.show_confirm(                              │
│      f"Deriva {delta*100:.2f}% - ¿Aprobar cambio?"          │
│    )                                                        │
│    ↓                                                        │
│ 6a. Usuario aprueba                                         │
│     update_session(session_id, {"system_prompt": new})      │
│     prompt_engine.update_prompt(session, new_prompt, force) │
│     ↓                                                       │
│     Registra mutación                                       │
│     mutation = {...}                                        │
│     json_protocol.emit("editor", "mutation", mutation)      │
│    ↓                                                        │
│ 6b. Usuario rechaza                                         │
│     editor.revert()  # Vuelve al prompt anterior            │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Qué Deberías Ver (Interfaz TUI por Modo)

### Modo Chat

```
┌───────────────────────────────────────────────────────────┐
│ Agente de Cambio  [Chat ▼]  [Reasoning: ON]  [Δ: 0.15]   │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ SYSTEM PROMPT (editable - click para editar)          │ │
│ │ Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.│ │
│ │ Tu misión es capturar la esencia de las ideas...      │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                           │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ Chat                                                  │ │
│ │                                                       │ │
│ │ ╭───────────────────────────────────────────────────╮ │ │
│ │ │ [User] 14:30                                    │ │ │
│ │ │ ¿Qué es TypeScript?                             │ │ │
│ │ ╰───────────────────────────────────────────────────╯ │ │
│ │                                                       │ │
│ │ ╭───────────────────────────────────────────────────╮ │ │
│ │ │ [Assistant] 14:30                               │ │ │
│ │ │ TypeScript es un lenguaje de programación       │ │ │
│ │ │ desarrollado por Microsoft. Es un superconjunto │ │ │
│ │ │ de JavaScript que añade tipado estático...      │ │ │
│ │ ╰───────────────────────────────────────────────────╯ │ │
│ │                                                       │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                           │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ Mensaje: ¿Cómo instalo TypeScript?____________ [Enviar]│ │
│ └───────────────────────────────────────────────────────┘ │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Modo Cuestionario

```
┌───────────────────────────────────────────────────────────┐
│ Agente de Cambio  [Cuestionario ▼]  [Reasoning: OFF]     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ Pregunta 3 de 5                                       │ │
│ │                                                       │ │
│ │ ¿Cuál es tu objetivo principal con TypeScript?        │ │
│ │                                                       │ │
│ │   ○ Mejorar la calidad del código                     │ │
│ │   ● Prevenir errores en tiempo de ejecución  ← SELECT │ │
│ │   ○ Facilitar el mantenimiento                        │ │
│ │   ○ Trabajar con frameworks modernos                  │ │
│ │                                                       │ │
│ │ Comentario adicional:                                 │ │
│ │ [_________________________________________________]   │ │
│ │                                                       │ │
│ │           [Anterior]      [Siguiente →]               │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                           │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ Progreso: [████████░░░░░░░░] 3/5 (60%)               │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Diálogo de Confirmación (Delta > Threshold)

```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│    ╔═══════════════════════════════════════════════════╗  │
│    ║  ⚠️  Cambio de Prompt Detectado                  ║  │
│    ║                                                   ║  │
│    ║  Deriva: 0.45 (45%)                              ║  │
│    ║  Umbral:  0.30 (30%)                              ║  │
│    ║                                                   ║  │
│    ║  El cambio excede el umbral permitido.           ║  │
│    ║  ¿Deseas aprobar esta modificación?              ║  │
│    ║                                                   ║  │
│    ║          [Aprobar]          [Rechazar]            ║  │
│    ╚═══════════════════════════════════════════════════╝  │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## 6. Patrones Extraídos (Código de Tutoriales)

### 6.1 Patrón Streaming (Python + httpx)

```python
import httpx
import asyncio
from typing import AsyncGenerator, List, Dict

async def stream_response(
    messages: List[Dict[str, str]],
    api_key: str
) -> AsyncGenerator[str, None]:
    """
    Generator asíncrono para streaming SSE.
    
    Patrón extraído de: DeepSeek API documentation
    """
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "text/event-stream"
            },
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "stream": True
            }
        ) as response:
            response.raise_for_status()
            buffer = ""
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        return
                    
                    try:
                        chunk = json.loads(data)
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
```

### 6.2 Patrón Widget con Protocolo JSON

```python
from dataclasses import dataclass
from typing import Dict, Any, Callable, Optional
from enum import Enum

class WidgetType(Enum):
    CHAT = "chat"
    GAUGE = "gauge"
    TABLE = "table"
    TABS = "tabs"
    EDITOR = "editor"

class WidgetAction(Enum):
    RENDER = "render"
    UPDATE = "update"
    CLEAR = "clear"
    EVENT = "event"

@dataclass
class WidgetEvent:
    """Evento JSON estandarizado para widgets"""
    widget_id: str
    tipo: WidgetType
    accion: WidgetAction
    datos: Dict[str, Any]
    timestamp: str

class BaseWidget:
    """Clase base para todos los widgets"""
    
    def __init__(self, widget_id: str, protocol: "JsonProtocol"):
        self.widget_id = widget_id
        self.protocol = protocol
    
    def emit(self, accion: WidgetAction, datos: Dict[str, Any]) -> WidgetEvent:
        """Emite evento JSON al orquestador"""
        event = WidgetEvent(
            widget_id=self.widget_id,
            tipo=self._get_widget_type(),
            accion=accion,
            datos=datos,
            timestamp=datetime.now().isoformat()
        )
        return self.protocol.emit(event)
    
    def _get_widget_type(self) -> WidgetType:
        raise NotImplementedError
    
    def render(self, area: "Rect") -> None:
        """Renderiza widget en área dada"""
        raise NotImplementedError
    
    def handle_event(self, event: WidgetEvent) -> None:
        """Maneja evento entrante"""
        raise NotImplementedError
```

### 6.3 Patrón Diálogo Modal

```python
from typing import Optional, Callable, List

class DialogWidget(BaseWidget):
    """Diálogo modal con botones"""
    
    def __init__(self, protocol: "JsonProtocol"):
        super().__init__("dialog_001", protocol)
        self.title = ""
        self.message = ""
        self.buttons: List[str] = []
        self.on_confirm: Optional[Callable] = None
        self.on_cancel: Optional[Callable] = None
    
    def show_confirm(
        self,
        title: str,
        message: str,
        buttons: List[str] = ["Aprobar", "Rechazar"],
        on_confirm: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None
    ) -> None:
        """Muestra diálogo de confirmación"""
        self.title = title
        self.message = message
        self.buttons = buttons
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        # Emitir evento al orquestador
        self.emit(WidgetAction.UPDATE, {
            "title": title,
            "message": message,
            "buttons": buttons,
            "visible": True
        })
    
    def handle_keypress(self, key: str) -> bool:
        """
        Maneja teclas para navegación en diálogo.
        
        Returns:
            True si el diálogo manejó la tecla, False si no
        """
        if key == "left":
            # Mover selección izquierda
            return True
        elif key == "right":
            # Mover selección derecha
            return True
        elif key == "enter":
            # Confirmar selección
            selected_button = self.buttons[self.selected_index]
            if selected_button == "Aprobar" and self.on_confirm:
                self.on_confirm()
            elif selected_button == "Rechazar" and self.on_cancel:
                self.on_cancel()
            self.emit(WidgetAction.CLEAR, {})
            return True
        return False
    
    def render(self, area: "Rect") -> None:
        """Renderiza diálogo modal centrado"""
        # Calcular posición centrada
        dialog_width = 60
        dialog_height = 10
        x = (area.width - dialog_width) // 2
        y = (area.height - dialog_height) // 2
        
        # Dibujar borde
        # Dibujar título
        # Dibujar mensaje
        # Dibujar botones
        pass
```

---

## 7. Checklist Debug

| Problema | Síntoma | Solución |
|----------|---------|----------|
| Streaming intermitente | Texto aparece en bloques | Buffer SSE incompleto → acumular líneas hasta `\n\n` |
| Diálogo no responde | Teclas no capturadas | Verificar `handle_keypress()` retorna `True` |
| Delta no se actualiza | Gauge muestra 0 siempre | Llamar `calculate_delta()` después de cada mensaje |
| Modo no cambia | Tabs no reflejan cambio | Emitir `mode:switch` evento después de `mode:set` |
| Prompt no se guarda | Cambios se pierden | Llamar `update_session()` antes de cerrar |

---

## 8. Referencias

### Archivos Originales (Socket.IO)

| Archivo | Ruta |
|---------|------|
| Server index | `apps/server/src/index.ts` |
| Chat store | `apps/web/app/store/chatStore.ts` |
| Socket handlers | (vacío en original, lógica en index.ts) |

### Eventos Socket.IO (Referencia)

```typescript
// Server → Client
socket.emit("message:stream", text)
socket.emit("message:complete", assistantMessage)
socket.emit("prompt:mutation", mutation)
socket.emit("question:next", nextQuestion)
socket.emit("delta:update", deltaMetrics)
socket.emit("mode:switch", mode)
socket.emit("error", errorMessage)

// Client → Server
socket.on("session:init", (sessionId) => {...})
socket.on("message:send", (content, mode, context) => {...})
socket.on("prompt:update", (content) => {...})
socket.on("option:select", (questionId, optionId, comment) => {...})
socket.on("mode:set", (mode) => {...})
socket.on("reasoning:toggle", (isReasoning) => {...})
```

---

*Documento creado: 15-03-2026*  
*Última actualización: 15-03-2026*  
*Estado: [OK] - Flujos documentados*

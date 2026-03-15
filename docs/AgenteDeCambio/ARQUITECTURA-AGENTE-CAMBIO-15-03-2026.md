# Agente de Cambio - Arquitectura del Sistema

## Módulo: AgenteDeCambio CLI (TR/AGENTES/sub-agentes/AgenteDeCambio)

---

## 1. Problema Detectado

**Síntoma:** Agente de Cambio STABLE existe como aplicación web (Next.js + Socket.IO) pero no está disponible como herramienta CLI reutilizable dentro del ecosistema TRON/ARES.

**Necesidad:** Transformar funcionalidades web en módulos CLI con interfaz Ratatui (o alternativa Python), manteniendo modularidad atómica (≤3 funciones/módulo) y comunicación JSON.

---

## 2. Causa Raíz

El sistema actual está diseñado para navegador:
- Frontend: React/Next.js con componentes visuales (burbujas chat, glassmorphism)
- Backend: Node.js + Express + Socket.IO
- Estado: Zustand con persistencia localStorage

**Para CLI necesitamos:**
- TUI framework: Ratatui (Rust) o textual/rich (Python)
- Backend: Python nativo (integración con ARES)
- Estado: SQLite + sockets Unix
- Protocolo: JSON para widgets ↔ orquestador

---

## 3. API Disponible (Módulos Existentes)

### 3.1 deepseek-connector (2 funciones)

```typescript
// Función 1: Completación síncrona
createCompletion(request: DeepSeekCompletionRequest): Promise<DeepSeekCompletionResponse>

// Función 2: Streaming en tiempo real
createCompletionStream(request: DeepSeekCompletionRequest): AsyncGenerator<DeepSeekStreamChunk>
```

**Traducción Python:**
```python
def create_completion(messages: List[Dict], api_key: str, **kwargs) -> Dict:
    """Solicitud síncrona a DeepSeek API"""
    pass

def create_completion_stream(messages: List[Dict], api_key: str, **kwargs):
    """Generator SSE chunks"""
    yield chunk  # Texto incremental
```

### 3.2 delta-calculator (4 funciones)

```typescript
calculate(oldPrompt: str, newPrompt: str) -> float  # 0.0-1.0
compare(oldPrompt: str, newPrompt: str) -> DeltaComparison
threshold() -> float  # 0.3 por defecto
requiresApproval(deltaScore: float) -> bool
```

**Algoritmo actual:** Diferencia de longitud normalizada
```python
def calculate_delta(old_prompt: str, new_prompt: str) -> float:
    length_diff = abs(len(new_prompt) - len(old_prompt))
    max_length = max(len(old_prompt), len(new_prompt), 1)
    return length_diff / max_length
```

### 3.3 prompt-engine (4 funciones)

```typescript
buildSystemPrompt(params: BuildPromptParams) -> str
updatePrompt(session: Session, newPrompt: str, force: bool) -> PromptUpdateResult
negotiateChange(oldPrompt: str, newPrompt: str) -> NegotiationResult
getDefaultPrompt() -> str
```

### 3.4 session-manager (6 funciones)

```typescript
createSession(sessionId?: str) -> Session
getSession(sessionId: str) -> Session | undefined
updateSession(sessionId: str, updates: Partial<Session>) -> bool
deleteSession(sessionId: str) -> bool
listSessions() -> str[]
getSessionStats() -> SessionStats
```

**Almacenamiento:** Map en memoria → Migrar a SQLite para CLI

---

## 4. Solución Implementada (Arquitectura CLI)

### 4.1 Estructura Propuesta

```
AGENTES/sub-agentes/AgenteDeCambio/
├── src/
│   └── main.py              # Orquestador (despachador puro)
├── modules/
│   ├── core/                # Lógica de negocio (traducción TypeScript → Python)
│   │   ├── deepseek_connector.py   # 2 funciones
│   │   ├── delta_calculator.py     # 4 funciones
│   │   ├── prompt_engine.py        # 4 funciones
│   │   └── session_manager.py      # 6 funciones (SQLite)
│   ├── ui/                  # Interfaz TUI
│   │   ├── widgets/         # Widgets atómicos (≤3 funciones cada uno)
│   │   │   ├── chat_widget.py      # Burbujas conversación
│   │   │   ├── gauge_widget.py     # Medidor delta (0-1)
│   │   │   ├── table_widget.py     # Tabla cuestionario
│   │   │   ├── tabs_widget.py      # Pestañas chat/cuestionario
│   │   │   └── prompt_editor.py    # Editor prompt editable
│   │   ├── dashboard.py            # Composición widgets
│   │   └── dialog.py               # Diálogos modales JSON
│   └── comms/
│       ├── socket_handler.py       # Socket.IO o Unix sockets
│       └── json_protocol.py        # Protocolo JSON widgets
├── config/
│   └── config.yaml
└── tests/
```

### 4.2 Protocolo JSON para Widgets

**Widget → Orquestador:**
```json
{
  "widget_id": "chat_001",
  "tipo": "chat|gauge|table|tabs|editor",
  "accion": "render|update|clear|event",
  "datos": {...},
  "timestamp": "2026-03-15T14:30:00Z"
}
```

**Orquestador → Widget:**
```json
{
  "widget_id": "chat_001",
  "evento": "click|select|input|stream",
  "datos": {
    "content": "texto del usuario",
    "mode": "chat"
  }
}
```

### 4.3 Flujo de Streaming

```
Usuario → chat_widget.py → json_protocol.py → deepseek_connector.py
                                                    ↓
                                              DeepSeek API
                                                    ↓
                                         AsyncGenerator chunks
                                                    ↓
chat_widget.py ← json_protocol.py ← socket_handler.py
    ↓
render carácter por carácter (TUI)
```

---

## 5. Flujo de Trabajo (Modos de Operación)

### 5.1 Modo Chat

```
1. Usuario escribe mensaje en chat_widget
2. Widget emite JSON: {"evento": "input", "datos": {"content": "..."}}
3. Orquestador recibe, construye system prompt (prompt_engine.buildSystemPrompt)
4. deepseek_connector.create_completion_stream() → Generator
5. Chunks se envían vía JSON al chat_widget
6. Widget renderiza carácter por carácter
7. delta_calculator.calculate() compara prompt anterior vs nuevo
8. gauge_widget actualiza medidor delta (0-1)
```

### 5.2 Modo Cuestionario

```
1. Orquestador cambia modo: tabs_widget.set_mode('questionnaire')
2. table_widget muestra opciones (radio|check|yesno)
3. Usuario selecciona opción → JSON evento
4. Orquestador procesa selección (socket.on('option:select'))
5. Siguiente pregunta generada por DeepSeek
6. table_widget actualiza filas
```

### 5.3 Edición de Prompt

```
1. prompt_editor muestra system prompt actual
2. Usuario edita texto
3. delta_calculator.compare(oldPrompt, newPrompt)
4. Si delta > threshold (0.3):
   - dialog_widget muestra confirmación
   - Usuario aprueba/rechaza
5. Si aprobado: prompt_engine.updatePrompt()
6. prompt_mutations se registran en SQLite
```

---

## 6. Qué Deberías Ver (Interfaz TUI)

### Layout Principal

```
┌─────────────────────────────────────────────────────────────┐
│  Agente de Cambio  [Chat ▼]  [Reasoning: ON]  [Δ: 0.25]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SYSTEM PROMPT (editable)                            │   │
│  │ Eres un sistema de EXTRACCIÓN COGNITIVA...          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Chat                                                │   │
│  │                                                     │   │
│  │ [User] Hola, ¿puedes ayudarme con TypeScript?      │   │
│  │                                                     │   │
│  │ [Assistant] Claro, soy un sistema de extracción... │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Mensaje: [____________________________] [Enviar]    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Gauge de Deriva Delta

```
Deriva del Prompt: [████████░░] 0.25/0.30 (OK)
                   ↑
              Umbral (0.3)
```

---

## 7. Patrones Extraídos (Código Clave)

### 7.1 Streaming SSE (Python)

```python
import httpx

async def stream_completion(messages: List[Dict], api_key: str):
    """Generator asíncrono para streaming SSE"""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            'POST',
            'https://api.deepseek.com/chat/completions',
            headers={'Authorization': f'Bearer {api_key}'},
            json={
                'model': 'deepseek-chat',
                'messages': messages,
                'stream': True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        return
                    chunk = json.loads(data)
                    yield chunk['choices'][0]['delta']['content']
```

### 7.2 Widget con Protocolo JSON

```python
class ChatWidget:
    """Widget atómico para conversación"""
    
    def __init__(self, json_protocol):
        self.protocol = json_protocol
        self.messages = []
    
    def render(self, area: Rect) -> None:
        """Renderiza burbujas de conversación"""
        pass  # ≤3 funciones por módulo
    
    def add_message(self, role: str, content: str) -> Dict:
        """Añade mensaje, retorna JSON evento"""
        self.messages.append({'role': role, 'content': content})
        return self.protocol.emit('chat', 'update', {'messages': self.messages})
    
    def stream_text(self, chunk: str) -> Dict:
        """Stream carácter por carácter"""
        pass
```

### 7.3 Delta Calculator (Python)

```python
def calculate_delta(old_prompt: str, new_prompt: str) -> float:
    """Calcula deriva entre prompts (0.0-1.0)"""
    if not old_prompt or not new_prompt:
        return 1.0
    
    length_diff = abs(len(new_prompt) - len(old_prompt))
    max_length = max(len(old_prompt), len(new_prompt), 1)
    return length_diff / max_length

def requires_approval(delta: float, threshold: float = 0.3) -> bool:
    """Determina si cambio requiere aprobación"""
    return delta > threshold
```

---

## 8. Widgets Modulares (C → JSON)

**Nota:** Usaremos Python + textual/rich en lugar de Rust C para integración nativa con ARES.

### Widget Registry

| Widget | Funciones | JSON Input | JSON Output |
|--------|-----------|------------|-------------|
| `ChatWidget` | render, add_message, stream_text | `{evento: "input", datos: {content}}` | `{tipo: "chat", datos: {messages}}` |
| `GaugeWidget` | render, set_value, set_threshold | `{evento: "update", datos: {value}}` | `{tipo: "gauge", datos: {value, threshold}}` |
| `TableWidget` | render, set_rows, select_row | `{evento: "select", datos: {row_id}}` | `{tipo: "table", datos: {selected}}` |
| `TabsWidget` | render, set_mode, switch | `{evento: "switch", datos: {mode}}` | `{tipo: "tabs", datos: {active_mode}}` |
| `PromptEditor` | render, edit, validate | `{evento: "edit", datos: {text}}` | `{tipo: "editor", datos: {prompt}}` |

---

## 9. Checklist Debug

### Problemas Comunes y Soluciones

| Problema | Síntoma | Solución |
|----------|---------|----------|
| Streaming no funciona | Texto aparece de una vez | Verificar `stream: true` en request, async generator |
| Delta siempre 0 | Prompts idénticos | Debug: print(old_prompt, new_prompt) |
| Widgets no responden | JSON mal formado | Validar con `json.loads()` antes de emitir |
| Socket.IO desconecta | CORS mal configurado | Verificar `origin: clientUrl` en server |
| SQLite locked | Múltiples writers | Usar `check_same_thread=False` en conexión |

---

## 10. Referencias

### Archivos Clave en Agente-De-Cambio-STABLE

| Ruta | Propósito |
|------|-----------|
| `modules/deepseek-connector/actions.ts` | Conexión API DeepSeek (streaming) |
| `modules/delta-calculator/actions.ts` | Cálculo de deriva (0.0-1.0) |
| `modules/prompt-engine/actions.ts` | Gestión system prompts |
| `modules/session-manager/actions.ts` | Gestión sesiones (memoria) |
| `apps/server/src/index.ts` | Servidor Socket.IO principal |
| `apps/web/app/store/chatStore.ts` | Estado global Zustand |

### Documentación Original

- README.md: Visión general, instalación, estructura
- docs/proyecto.md: Etapas de implementación, roadmap
- modules/*/INDEX.md: Documentación de cada módulo

---

## 11. Próximos Pasos (FASE 2)

1. **Analizar Ratatui** en `/home/daniel/borrar/ratatui/`
   - Widgets disponibles (Block, Paragraph, List, Chart, Gauge, Table, Tabs)
   - Backends (crossterm, termion, termwiz)
   - Ejemplos en `ratatui-widgets/examples/`

2. **Evaluar alternativas Python**
   - textual: TUI moderno con CSS-like styling
   - rich: Console output con styling
   - urwid: TUI clásico (installer Ubuntu)

3. **Decidir stack tecnológico**
   - ¿Rust (Ratatui) + binario separado?
   - ¿Python (textual) + integración nativa ARES?

---

*Documento creado: 15-03-2026*  
*Última actualización: 15-03-2026*  
*Estado: [OK] - FASE 1 completada*

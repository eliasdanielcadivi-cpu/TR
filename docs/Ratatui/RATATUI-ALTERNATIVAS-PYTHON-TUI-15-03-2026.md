# Ratatui y Alternativas Python para TUI

## Módulo: Evaluación de Frameworks TUI para AgenteDeCambio CLI

---

## 1. Problema Detectado

**Síntoma:** Necesitamos decidir stack tecnológico para interfaz TUI de AgenteDeCambio CLI.

**Pregunta:** ¿Usar Ratatui (Rust) o alternativa Python (textual, rich, urwid)?

**Contexto:**
- AgenteDeCambio debe integrarse con ARES (Python)
- Necesita widgets interactivos (chat, gauge, table, tabs, editor)
- Comunicación JSON con módulos core
- Streaming en tiempo real

---

## 2. Causa Raíz

**Ratatui (Rust):**
- ✅ Widgets maduros, rendimiento excelente
- ✅ Backend múltiple (crossterm, termion, termwiz)
- ❌ Requiere binario separado
- ❌ Comunicación JSON vía stdin/stdout (overhead)
- ❌ Curva de aprendizaje Rust

**Python TUI:**
- ✅ Integración nativa con ARES (mismo venv)
- ✅ Mismo lenguaje que módulos core
- ✅ Menor complejidad de deployment
- ❌ Rendimiento inferior (pero aceptable para TUI)
- ❌ Madurez variable según framework

---

## 3. API Disponible (Ratatui Widgets)

### 3.1 Widgets Principales (Rust)

**Gauge (Barra de Progreso):**
```rust
use ratatui::widgets::{Gauge, LineGauge};
use ratatui::style::{Style, Modifier};

// Gauge tradicional
let gauge = Gauge::default()
    .gauge_style(Style::new().blue().on_black())
    .label("Year Progress")
    .percent(80);

// LineGauge (compacto)
let line_gauge = LineGauge::default()
    .filled_style(Style::new().white().on_red().bold())
    .ratio(0.42)
    .label("❤️ HP");
```

**Table (Tabla con Navegación):**
```rust
use ratatui::widgets::{Table, Row, TableState};
use ratatui::layout::Constraint;

let mut table_state = TableState::default();
table_state.select_first();

let header = Row::new(["Ingredient", "Quantity", "Macros"])
    .style(Style::new().bold());

let rows = vec![
    Row::new(["Eggplant", "1 medium", "25 kcal, 6g carbs"]),
    Row::new(["Tomato", "2 large", "44 kcal, 10g carbs"]),
];

let table = Table::new(rows, [Constraint::Percentage(30), ...])
    .header(header)
    .row_highlight_style(Style::new().on_black().bold())
    .highlight_symbol("🍴 ");

frame.render_stateful_widget(table, area, &mut table_state);
```

**Tabs (Pestañas):**
```rust
use ratatui::widgets::Tabs;
use ratatui::symbols;

let tabs = Tabs::new(vec!["Tab1", "Tab2", "Tab3"])
    .style(Color::White)
    .highlight_style(Style::default().magenta().on_black().bold())
    .select(selected_tab)
    .divider(symbols::DOT)
    .padding(" ", " ");
```

**Paragraph (Texto/Burbujas Chat):**
```rust
use ratatui::widgets::Paragraph;
use ratatui::layout::Alignment;

let paragraph = Paragraph::new("Hello World!")
    .alignment(Alignment::Center)
    .block(Block::bordered()
        .title("Chat")
        .style(Style::new().blue()));
```

### 3.2 Patrón de Renderizado (Rust)

```rust
use ratatui::{Frame, DefaultTerminal};
use crossterm::event;

fn main() -> Result<()> {
    ratatui::run(|terminal| {
        loop {
            terminal.draw(render)?;  // Callback de renderizado
            
            // Manejo de eventos
            if let Some(key) = event::read()?.as_key_press_event() {
                match key.code {
                    KeyCode::Char('q') => return Ok(()),  // Quit
                    KeyCode::Up => table_state.select_previous(),
                    KeyCode::Down => table_state.select_next(),
                    _ => {}
                }
            }
        }
    })
}

fn render(frame: &mut Frame) {
    let area = frame.area();
    
    // Layout
    let layout = Layout::vertical([
        Constraint::Length(1),  // Header
        Constraint::Fill(1),    // Content
        Constraint::Length(3),  // Footer
    ]);
    let [header, content, footer] = area.layout(&layout);
    
    // Render widgets
    frame.render_widget(title, header);
    frame.render_stateful_widget(table, content, &mut table_state);
    frame.render_widget(tabs, footer);
}
```

---

## 4. Solución Implementada (Evaluación Python)

### 4.1 Textual (Recomendado)

**Descripción:** Framework TUI moderno construido sobre Rich, con modelo event-driven asíncrono.

**Widgets Disponibles:**

| Widget | Propósito | Equivalente Ratatui |
|--------|-----------|---------------------|
| `Static` | Texto estático | `Paragraph` |
| `Button` | Botones interactivos | N/A (custom) |
| `Input` | Campos de texto | N/A (custom) |
| `Tree` | Árbol jerárquico | N/A |
| `TabbedContent` | Pestañas | `Tabs` |
| `Sparkline` | Mini histograma | `Sparkline` |
| `Switch` | Toggle on/off | N/A |
| `Digits` | Números grandes | N/A |
| `Footer` | Footer con atajos | N/A |

**Ejemplo Chat Dashboard:**
```python
from textual.app import App
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Input, Button, Static, Footer

class ChatDashboard(App):
    CSS_PATH = "chat.tcss"
    BINDINGS = [("q", "quit", "Quit")]
    
    def compose(self):
        with Vertical():
            # Header
            yield Static("🤖 ARES Chat Dashboard", id="header")
            
            # Chat messages (scrollable)
            with VerticalScroll(id="chat-area"):
                yield Static("Bot: Hello!", classes="message")
            
            # Input area
            with Horizontal(id="input-area"):
                yield Input(placeholder="Type message...", id="chat-input")
                yield Button("Send", id="send-btn")
            
            yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#chat-input", Input)
        chat_area = self.query_one("#chat-area", VerticalScroll)
        
        # Add user message
        message = Static(f"User: {input_widget.value}", classes="message user")
        chat_area.mount(message)
        
        input_widget.value = ""

if __name__ == "__main__":
    app = ChatDashboard()
    app.run()
```

**TCSS (Styling):**
```css
/* chat.tcss */
#header {
    background: $primary;
    color: $text;
    padding: 1;
    text-align: center;
}

#chat-area {
    height: 1fr;
    border: solid $secondary;
    padding: 1;
}

.message {
    padding: 1;
    margin: 1 0;
}

.message.user {
    background: $secondary;
    align: right;
}

#input-area {
    dock: bottom;
    height: 3;
}
```

**Pros:**
- ✅ Integración nativa Python/ARES
- ✅ Widgets interactivos (buttons, inputs)
- ✅ CSS-like styling (TCSS)
- ✅ Async/await nativo
- ✅ Hot-reload para TCSS
- ✅ Accesibilidad (screen readers, themes)

**Contras:**
- ❌ Python 3.8+ requerido
- ❌ Curva de aprendizaje (eventos, DOM queries)
- ❌ Menor rendimiento que Rust (pero aceptable)

---

### 4.2 Rich (Solo Output)

**Descripción:** Biblioteca para formateo de texto con estilo, NO es framework TUI interactivo.

**Widgets:**

| Widget | Propósito |
|--------|-----------|
| `Table` | Tablas con estilo |
| `Progress` | Barras de progreso |
| `Spinner` | Spinners de estado |
| `Tree` | Árboles jerárquicos |
| `Columns` | Columnas tipo ls |
| `Markdown` | Renderizado Markdown |
| `Syntax` | Highlight de código |
| `Panel` | Cajas con borde |

**Ejemplo:**
```python
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

# Tabla
table = Table(title="Agente de Cambio - Metrics")
table.add_column("Metric", style="cyan")
table.add_column("Value", style="green")
table.add_row("Delta Score", "0.25")
table.add_row("Threshold", "0.30")
console.print(table)

# Progreso
for step in track(range(100), description="Processing..."):
    do_step(step)
```

**Pros:**
- ✅ Simple, drop-in replacement de print()
- ✅ Excelente para output estático
- ✅ Tracebacks bonitos
- ✅ Markdown/syntax highlighting

**Contras:**
- ❌ NO es interactivo (sin eventos, sin inputs)
- ❌ Solo output unidireccional
- ❌ No sirve para dashboards interactivos

**Veredicto:** Usar como complemento de Textual, NO como reemplazo.

---

### 4.3 Urwid (Clásico)

**Descripción:** Framework TUI clásico (usado en installer de Ubuntu), más bajo nivel.

**Ejemplo:**
```python
import urwid

class ChatWidget(urwid.Widget):
    def __init__(self):
        self.messages = []
        self.listbox = urwid.ListBox(
            urwid.SimpleFocusListWalker(self.messages)
        )
    
    def render(self, size, focus=False):
        return self.listbox.render(size, focus)

# Loop principal
widget = ChatWidget()
loop = urwid.MainLoop(widget, unhandled_input=lambda key: None)
loop.run()
```

**Pros:**
- ✅ Maduro, estable
- ✅ Usado en producción (installer Ubuntu)
- ✅ Bajo consumo de recursos

**Contras:**
- ❌ API verbosa, menos intuitiva
- ❌ Sin CSS-like styling
- ❌ Menos widgets modernos
- ❌ Curva de aprendizaje pronunciada

**Veredicto:** Demasiado bajo nivel para AgenteDeCambio.

---

## 5. Flujo de Trabajo (Comparativa)

### Ratatui (Rust)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. main.rs: ratatui::run(|terminal| {...})                 │
│ 2. terminal.draw(render) → callback                         │
│ 3. render() construye widgets Rust                          │
│ 4. frame.render_widget(widget, area)                        │
│ 5. event::read() → KeyCode                                  │
│ 6. match key.code { ... }                                   │
│ 7. Para comunicación con Python:                            │
│    - Binario separado                                        │
│    - JSON vía stdin/stdout                                   │
│    - Overhead de IPC                                         │
└─────────────────────────────────────────────────────────────┘
```

### Textual (Python)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. app.py: class ChatDashboard(App)                         │
│ 2. def compose(self): yield widgets                         │
│ 3. def on_button_pressed(self, event): ...                  │
│ 4. self.query_one("#widget-id", Widget)                     │
│ 5. widget.update("new value")                               │
│ 6. Integración nativa con módulos core:                     │
│    - from modules.core import create_completion_stream      │
│    - Mismo proceso, mismo venv                              │
│    - Sin overhead de IPC                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Qué Deberías Ver (Ejemplos)

### Ratatui (Rust)

```
┌───────────────────────────────────────────────────────────┐
│ Gauge Widget (Press 'q' to quit)                          │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ Year Progress [████████████████████░░░░░░░░░░] 80%       │
│                                                           │
│ ❤️ HP [██████████░░░░░░░░░░░░░░░░] 0.42                  │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Textual (Python)

```
┌───────────────────────────────────────────────────────────┐
│ 🤖 ARES Chat Dashboard                              ▀ X   │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ ╭─────────────────────────────────────────────────────╮  │
│ │ Bot: Hello! How can I help you today?              │  │
│ ╰─────────────────────────────────────────────────────╯  │
│ ╭─────────────────────────────────────────────────────╮  │
│ │           User: ¿Qué es TypeScript?                │  │
│ ╰─────────────────────────────────────────────────────╯  │
│                                                           │
│ ┌─────────────────────────────────────────────────────┐  │
│ │ Type your message...                    [Send]      │  │
│ └─────────────────────────────────────────────────────┘  │
│                                                           │
│  ^Q Quit                                                  │
└───────────────────────────────────────────────────────────┘
```

---

## 7. Patrones Extraídos (Código Clave)

### 7.1 Patrón Streaming (Textual + httpx)

```python
from textual.app import App
from textual.widgets import Static, Input, Button
from textual.containers import Vertical, VerticalScroll
import httpx

class ChatApp(App):
    def compose(self):
        with Vertical():
            yield VerticalScroll(id="chat-area")
            yield Input(id="input")
            yield Button("Send")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#input", Input)
        chat_area = self.query_one("#chat-area", VerticalScroll)
        
        # User message
        user_msg = Static(f"User: {input_widget.value}", classes="user")
        chat_area.mount(user_msg)
        
        # Bot response (streaming)
        bot_msg = Static("Bot: ", classes="bot")
        chat_area.mount(bot_msg)
        
        # Stream from DeepSeek
        async for chunk in self.stream_deepseek(input_widget.value):
            bot_msg.update(f"Bot: {bot_msg.plain + chunk}")
        
        input_widget.value = ""
    
    async def stream_deepseek(self, prompt: str):
        """Generator asíncrono para streaming SSE"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "https://api.deepseek.com/chat/completions",
                json={"messages": [{"role": "user", "content": prompt}], "stream": True},
                headers={"Authorization": f"Bearer {API_KEY}"}
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        chunk = json.loads(line[6:])
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
```

### 7.2 Patrón Gauge Widget (Textual)

```python
from textual.widgets import Static
from textual.reactive import reactive

class GaugeWidget(Static):
    """Widget gauge personalizado para delta metrics"""
    
    value = reactive(0.0)  # 0.0 a 1.0
    threshold = reactive(0.3)
    
    DEFAULT_CSS = """
    GaugeWidget {
        height: 3;
        background: $surface;
        border: solid $primary;
    }
    """
    
    def render(self) -> str:
        """Renderiza gauge como barra de progreso"""
        filled = int(self.value * 40)
        total = 40
        bar = "█" * filled + "░" * (total - filled)
        
        status = "OK" if self.value < self.threshold else "⚠️ "
        
        return f"""
Deriva: [{bar}] {self.value*100:.1f}%/{self.threshold*100:.1f}% {status}
""".strip()
    
    def watch_value(self, new_value: float) -> None:
        """Callback cuando value cambia"""
        self.refresh()  # Re-render
```

### 7.3 Patrón JSON Protocol

```python
import json
from typing import Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class WidgetEvent:
    widget_id: str
    tipo: str  # "chat", "gauge", "table", etc.
    accion: str  # "render", "update", "event"
    datos: Dict[str, Any]
    timestamp: str

class JsonProtocol:
    """Protocolo JSON para comunicación widgets ↔ orquestador"""
    
    def emit(self, event: WidgetEvent) -> str:
        """Emite evento JSON"""
        return json.dumps(asdict(event))
    
    def parse(self, json_str: str) -> WidgetEvent:
        """Parsea evento JSON"""
        data = json.loads(json_str)
        return WidgetEvent(**data)

# Uso en widget
protocol = JsonProtocol()

event = WidgetEvent(
    widget_id="chat_001",
    tipo="chat",
    accion="update",
    datos={"messages": [...]},
    timestamp=datetime.now().isoformat()
)

json_str = protocol.emit(event)
# {"widget_id": "chat_001", "tipo": "chat", "accion": "update", ...}
```

---

## 8. Checklist Debug

| Problema | Síntoma | Solución |
|----------|---------|----------|
| Textual no renderiza | Pantalla vacía | Verificar `app.run()` en `if __name__ == "__main__"` |
| Widgets no responden | Eventos no capturados | Implementar `on_button_pressed`, `on_key` handlers |
| TCSS no aplica | Widgets sin estilo | Verificar `CSS_PATH = "file.tcss"` o `BINDINGS` |
| Streaming bloquea UI | Congelamiento | Usar `async def` + `await` en handlers |
| Rich + Textual conflicto | Errores de console | No usar `rich.live()` dentro de Textual app |

---

## 9. Referencias

### Ratatui (Rust)

| Recurso | URL |
|---------|-----|
| Repo GitHub | https://github.com/ratatui/ratatui |
| Docs | https://docs.rs/ratatui |
| Widget Examples | `/home/daniel/borrar/ratatui/ratatui-widgets/examples/` |
| App Examples | `/home/daniel/borrar/ratatui/examples/apps/` |
| Architecture | `ARCHITECTURE.md` (crate organization) |

### Textual (Python)

| Recurso | URL |
|---------|-----|
| Docs | https://textual.textualize.io |
| Widget Reference | https://textual.textualize.io/widget_reference/ |
| Real Python Tutorial | https://realpython.com/python-textual/ |
| GitHub | https://github.com/Textualize/textual |

### Rich (Python)

| Recurso | URL |
|---------|-----|
| Docs | https://rich.readthedocs.io |
| GitHub | https://github.com/Textualize/rich |
| CLI | `python -m rich` (test en terminal) |

---

## 10. Decisión Recomendada

### Stack Tecnológico para AgenteDeCambio CLI

**Recomendación:** **Textual (Python)**

**Razones:**

1. **Integración Nativa con ARES:**
   - Mismo lenguaje (Python)
   - Mismo entorno virtual
   - Sin overhead de IPC (stdin/stdout)

2. **Widgets Interactivos:**
   - Buttons, Inputs, Tabs nativos
   - Event-driven architecture
   - Async/await para streaming

3. **Desarrollo Ágil:**
   - TCSS (CSS-like) para styling
   - Hot-reload para cambios visuales
   - Menor curva de aprendizaje que Rust

4. **Módulos Core Python:**
   - `deepseek_connector.py` → Textual app
   - `delta_calculator.py` → Gauge widget
   - Sin traducción Rust ↔ Python

5. **Recursos Suficientes:**
   - 18 widgets en `ratatui-widgets/examples/`
   - Documentación completa de Textual
   - Comunidad activa (Textualize.io)

**Arquitectura Propuesta:**
```
AGENTES/sub-agentes/AgenteDeCambio/
├── src/
│   └── main.py              # Textual App
├── modules/
│   ├── core/                # Python modules (deepseek, delta, etc.)
│   └── ui/
│       ├── widgets/         # Textual widgets personalizados
│       │   ├── chat_widget.py
│       │   ├── gauge_widget.py
│       │   └── ...
│       └── styles/          # TCSS files
│           └── chat.tcss
└── config/
    └── config.yaml
```

---

*Documento creado: 15-03-2026*  
*Última actualización: 15-03-2026*  
*Estado: [OK] - Decisión: Textual (Python)*

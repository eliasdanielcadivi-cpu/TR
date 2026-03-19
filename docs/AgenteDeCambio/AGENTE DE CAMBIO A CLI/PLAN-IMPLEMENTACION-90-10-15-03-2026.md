# PLAN DE IMPLEMENTACIÓN - AgenteDeCambio CLI (Híbrido Textual + Ratatui)

## Módulo: Estrategia 90/10 para TUI Perfecta

---

## 1. Estrategia Híbrida 90/10

### Filosofía
```
┌─────────────────────────────────────────────────────────────┐
│                    TEXTUAL (90%)                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ - Orquestación general de la app                    │   │
│  │ - Lógica de negocio (modules/core/)                 │   │
│  │ - Comunicación con DeepSeek/ARES                    │   │
│  │ - Widgets interactivos (buttons, inputs, tabs)      │   │
│  │ - Screens, navegación, command palette              │   │
│  │ - TCSS styling, layouts                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         RATATUI (10%) - Componentes Visuales        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │  Gauge   │  │ Sparkline│  │  Chart   │         │   │
│  │  │  Widget  │  │  Widget  │  │  Widget  │         │   │
│  │  └──────────┘  └──────────┘  └──────────┘         │   │
│  │  (Render ASCII/Unicode que Textual puede mostrar)  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### ¿Por qué Híbrido?

**Textual (90%) - Ventajas:**
- ✅ Python nativo (integración con ARES)
- ✅ Widgets interactivos completos
- ✅ CSS-like styling (TCSS)
- ✅ Async/await para streaming
- ✅ Dev console, testing
- ✅ Screens, navegación, modales

**Ratatui (10%) - Ventajas:**
- ✅ Gauges visualmente hermosos (mejor que Textual)
- ✅ Sparklines de alta calidad
- ✅ Charts profesionales
- ✅ Tablas con rendering avanzado
- ✅ Canvas para dibujo personalizado

**Combinación:**
- Textual maneja la lógica y estructura
- Ratatui renderiza componentes visuales específicos
- Output de Ratatui se muestra en Textual como texto formateado

---

## 2. Arquitectura Propuesta

### 2.1 Estructura de Carpetas

```
AGENTES/sub-agentes/AgenteDeCambio/
├── src/
│   └── main.py              # App principal (Textual 90%)
├── modules/
│   ├── core/                # Lógica de negocio (Python)
│   │   ├── deepseek_connector.py   # Streaming DeepSeek API
│   │   ├── delta_calculator.py     # Métricas de deriva
│   │   ├── prompt_engine.py        # Gestión de prompts
│   │   └── session_manager.py      # SQLite sessions
│   ├── ui/
│   │   ├── textual_widgets/       # Widgets Textual custom
│   │   │   ├── chat_widget.py     # Burbujas de chat
│   │   │   ├── gauge_widget.py    # Delta gauge (Textual)
│   │   │   ├── questionnaire.py   # Modo cuestionario
│   │   │   └── config_panel.py    # Panel configuración
│   │   ├── ratatui_components/    # Componentes Ratatui (Rust)
│   │   │   ├── src/
│   │   │   │   ├── lib.rs         # Lib principal
│   │   │   │   ├── gauge.rs       # Gauge widget (bonito)
│   │   │   │   ├── sparkline.rs   # Sparkline widget
│   │   │   │   └── chart.rs       # Chart widget
│   │   │   ├── Cargo.toml
│   │   │   └── target/release/libratatui_components.so
│   │   └── hybrid_renderer.py     # Puente Python ↔ Rust
│   └── comms/
│       ├── socket_handler.py      # Socket.IO / Unix sockets
│       └── json_protocol.py       # Protocolo JSON
├── config/
│   └── config.yaml
├── docs/
│   └── AGENTE-CAMBIO-README.md
└── tests/
    └── test_chat_dashboard.py
```

### 2.2 Flujo de Comunicación

```
┌─────────────────────────────────────────────────────────────┐
│  main.py (Textual App)                                      │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Chat      │  │   Tabs      │  │   Input     │        │
│  │   Widget    │  │   Widget    │  │   Widget    │        │
│  │  (Textual)  │  │  (Textual)  │  │  (Textual)  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│         ↓                ↓                ↓                 │
│  ┌──────────────────────────────────────────────────┐      │
│  │          hybrid_renderer.py (Puente)             │      │
│  │  - Carga libratui_components.so vía ctypes       │      │
│  │  - Convierte datos Python → structs Rust         │      │
│  │  - Renderiza a string Unicode/ASCII              │      │
│  │  - Retorna string formateado a Textual           │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
│         ↓ (llamada FFI)                                     │
│  ┌──────────────────────────────────────────────────┐      │
│  │     libratui_components.so (Rust/Ratatui)        │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │      │
│  │  │  Gauge   │  │ Sparkline│  │  Chart   │       │      │
│  │  │  render  │  │  render  │  │  render  │       │      │
│  │  └──────────┘  └──────────┘  └──────────┘       │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Componentes Ratatui (10%)

### 3.1 Gauge Widget (Rust)

```rust
// src/gauge.rs
use ratatui::{
    Frame,
    layout::Rect,
    style::{Style, Color},
    widgets::{Gauge, LineGauge},
};

/// Renderiza gauge de deriva (0.0 - 1.0)
pub fn render_delta_gauge(
    frame: &mut Frame,
    area: Rect,
    delta: f64,
    threshold: f64,
) -> String {
    // Determinar color según delta
    let (gauge_style, label_color) = if delta < threshold {
        (Style::new().green(), Color::Green)
    } else if delta < 0.7 {
        (Style::new().yellow(), Color::Yellow)
    } else {
        (Style::new().red(), Color::Red)
    };
    
    // Gauge tradicional
    let gauge = Gauge::default()
        .gauge_style(gauge_style)
        .label(format!("Δ: {:.1}%", delta * 100.0))
        .ratio(delta);
    
    // Renderizar a buffer
    let mut buffer = ratatui::buffer::Buffer::empty(area);
    gauge.render(area, &mut buffer);
    
    // Convertir a string (Unicode/ASCII)
    buffer_to_string(&buffer)
}

/// Renderiza line gauge (compacto)
pub fn render_line_gauge(
    delta: f64,
    threshold: f64,
    width: usize,
) -> String {
    use ratatui::symbols::line;
    
    let filled = (delta * width as f64) as usize;
    let bar = "█".repeat(filled) + &"░".repeat(width - filled);
    
    let status = if delta < threshold {
        "✓ OK"
    } else if delta < 0.7 {
        "⚠ REVIEW"
    } else {
        "✗ REJECT"
    };
    
    format!(
        "Deriva: [{}] {:.1}%/{:.1}% {}",
        bar,
        delta * 100.0,
        threshold * 100.0,
        status
    )
}
```

### 3.2 Sparkline Widget (Rust)

```rust
// src/sparkline.rs
use ratatui::{
    layout::Rect,
    style::Style,
    widgets::Sparkline,
};

/// Renderiza sparkline de métricas
pub fn render_metrics_sparkline(
    data: &[f64],
    width: usize,
    height: usize,
) -> String {
    let sparkline = Sparkline::default()
        .block(Block::default().title("Delta History"))
        .style(Style::new().blue())
        .data(data.iter().map(|&x| x as u64).collect::<Vec<_>>());
    
    let area = Rect::new(0, 0, width as u16, height as u16);
    let mut buffer = ratatui::buffer::Buffer::empty(area);
    sparkline.render(area, &mut buffer);
    
    buffer_to_string(&buffer)
}
```

### 3.3 Puente Python (hybrid_renderer.py)

```python
"""
Puente Python ↔ Rust para componentes Ratatui
"""
import ctypes
from pathlib import Path
from typing import List, Optional

# Cargar librería compartida
LIB_PATH = Path(__file__).parent / "ratatui_components" / "target" / "release" / "libratatui_components.so"

class RatatuiRenderer:
    """Renderer híbrido para componentes Ratatui en Textual"""
    
    def __init__(self):
        self.lib = ctypes.CDLL(str(LIB_PATH))
        
        # Configurar funciones Rust
        # render_line_gauge(delta: f64, threshold: f64, width: usize) -> *mut c_char
        self.lib.render_line_gauge.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_size_t]
        self.lib.render_line_gauge.restype = ctypes.c_char_p
        
        # render_sparkline(data: *mut f64, len: usize, width: usize, height: usize) -> *mut c_char
        self.lib.render_sparkline.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t
        ]
        self.lib.render_sparkline.restype = ctypes.c_char_p
    
    def render_gauge(self, delta: float, threshold: float, width: int = 40) -> str:
        """
        Renderiza gauge de deriva usando Ratatui
        
        Args:
            delta: Score de deriva (0.0 - 1.0)
            threshold: Umbral de aprobación (default: 0.3)
            width: Ancho del gauge en caracteres
        
        Returns:
            String formateado con gauge Unicode/ASCII
        """
        result = self.lib.render_line_gauge(
            ctypes.c_double(delta),
            ctypes.c_double(threshold),
            ctypes.c_size_t(width)
        )
        return result.decode('utf-8')
    
    def render_sparkline(self, data: List[float], width: int = 40, height: int = 5) -> str:
        """
        Renderiza sparkline de métricas usando Ratatui
        
        Args:
            data: Lista de valores para graficar
            width: Ancho del sparkline
            height: Alto del sparkline
        
        Returns:
            String formateado con sparkline Unicode
        """
        data_array = (ctypes.c_double * len(data))(*data)
        
        result = self.lib.render_sparkline(
            data_array,
            ctypes.c_size_t(len(data)),
            ctypes.c_size_t(width),
            ctypes.c_size_t(height)
        )
        return result.decode('utf-8')


# Uso en widget Textual
from textual.widgets import Static

class HybridDeltaGauge(Static):
    """Widget híbrido: Textual + Ratatui para gauge"""
    
    delta = reactive(0.0)
    threshold = reactive(0.3)
    history = reactive([])  # Para sparkline
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer = RatatuiRenderer()
    
    def render(self) -> str:
        """Renderiza gauge usando Ratatui"""
        # Gauge principal
        gauge_str = self.renderer.render_gauge(
            self.delta,
            self.threshold,
            width=40
        )
        
        # Sparkline de historial (si hay datos)
        if self.history:
            sparkline_str = self.renderer.render_sparkline(
                self.history[-20:],  # Últimos 20 valores
                width=40,
                height=3
            )
            return f"{gauge_str}\n{sparkline_str}"
        
        return gauge_str
    
    def watch_delta(self, new_value: float) -> None:
        """Actualizar cuando delta cambia"""
        # Añadir a historial
        if hasattr(self, 'history'):
            self.history.append(new_value)
            if len(self.history) > 100:
                self.history = self.history[-100:]
        
        self.refresh()  # Re-render
```

---

## 4. Implementación Textual (90%)

### 4.1 App Principal (main.py)

```python
"""
AgenteDeCambio CLI - App Principal
90% Textual + 10% Ratatui para visuales
"""
from __future__ import annotations
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button, Footer, Header, Input, Label,
    TabbedContent, TabPane, RichLog
)

from modules.core import (
    create_session,
    get_session,
    update_session,
    build_system_prompt,
    create_completion_stream,
    calculate_delta,
)
from modules.ui.textual_widgets import ChatMessage, QuestionnaireWidget
from modules.ui.hybrid_renderer import HybridDeltaGauge


class AgenteDeCambioApp(App):
    """
    Agente de Cambio CLI - Interfaz híbrida Textual/Ratatui
    """
    
    CSS_PATH = "chat_dashboard.tcss"
    
    BINDINGS = [
        Binding("ctrl+s", "save_session", "Save"),
        Binding("ctrl+l", "toggle_logs", "Logs"),
        Binding("ctrl+d", "toggle_dark", "Dark"),
        Binding("f1", "help", "Help"),
        Binding("ctrl+q", "quit", "Quit"),
    ]
    
    # Estado reactivo
    connected = reactive(False)
    streaming = reactive(False)
    delta_score = reactive(0.0)
    session_id = reactive(None)
    
    def compose(self) -> ComposeResult:
        """Componer UI completa"""
        yield Header()
        
        with TabbedContent(initial="chat"):
            # Pestaña CHAT
            with TabPane("💬 Chat", id="chat"):
                with Vertical():
                    # Header con métricas (Ratatui)
                    with Horizontal(id="metrics-bar"):
                        yield HybridDeltaGauge(id="delta-gauge")
                        yield Label("", id="connection-status")
                    
                    # Área de chat (Textual)
                    with VerticalScroll(id="chat-area"):
                        yield ChatMessage(
                            "assistant",
                            "🤖 Hola, soy Agente de Cambio. ¿En qué puedo ayudarte hoy?"
                        )
                    
                    # Input area (Textual)
                    with Horizontal(id="input-area"):
                        yield Input(
                            placeholder="Escribe tu mensaje...",
                            id="chat-input"
                        )
                        yield Button("Enviar", id="send-btn", variant="primary")
            
            # Pestaña CUESTIONARIO (Textual)
            with TabPane("📋 Cuestionario", id="questionnaire"):
                yield QuestionnaireWidget(id="questionnaire-widget")
            
            # Pestaña CONFIG (Textual)
            with TabPane("⚙️ Config", id="config"):
                with VerticalScroll():
                    yield Label("Configuración de DeepSeek API")
                    yield Input(
                        placeholder="DeepSeek API Key",
                        id="api-key-input",
                        password=True
                    )
                    yield Label("Threshold de deriva: 0.3")
                    yield Label("Modelo: deepseek-chat")
        
        # Panel de logs (Textual RichLog)
        yield RichLog(id="log-panel", highlight=True, markup=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Inicializar app"""
        # Crear sesión
        session = create_session()
        self.session_id = session["id"]
        
        # Conectar
        self.connect_to_server()
    
    def watch_connected(self, connected: bool) -> None:
        """Actualizar estado de conexión"""
        status = self.query_one("#connection-status", Label)
        if connected:
            status.update("🟢 Conectado")
            status.add_class("connected")
        else:
            status.update("🔴 Desconectado")
            status.remove_class("connected")
    
    def watch_delta_score(self, score: float) -> None:
        """Actualizar gauge de delta"""
        gauge = self.query_one("#delta-gauge", HybridDeltaGauge)
        gauge.delta = score
    
    @on(Button.Pressed, "#send-btn")
    def on_send_pressed(self, event: Button.Pressed) -> None:
        """Enviar mensaje"""
        self.send_message()
    
    @on(Input.Submitted, "#chat-input")
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter en input"""
        self.send_message()
    
    def send_message(self) -> None:
        """Enviar mensaje al servidor"""
        input_widget = self.query_one("#chat-input", Input)
        message = input_widget.value.strip()
        
        if not message:
            return
        
        chat_area = self.query_one("#chat-area", VerticalScroll)
        
        # Añadir mensaje de usuario
        user_msg = ChatMessage("user", message)
        chat_area.mount(user_msg)
        
        # Limpiar input
        input_widget.value = ""
        
        # Iniciar streaming
        self.stream_response(message)
    
    @work(exclusive=True)
    async def stream_response(self, user_message: str) -> None:
        """Worker para streaming de respuesta"""
        self.streaming = True
        
        chat_area = self.query_one("#chat-area", VerticalScroll)
        
        # Crear mensaje de bot vacío
        bot_msg = ChatMessage("assistant", "🤖 ")
        chat_area.mount(bot_msg)
        
        # Obtener sesión
        session = get_session(self.session_id)
        
        # Construir system prompt
        prompt = build_system_prompt(BuildPromptParams(
            objectives=session.get("objectives", []),
            mode="chat"
        ))
        
        # Preparar mensajes
        messages = [
            {"role": "system", "content": prompt},
            *session["messages"][-10:]  # Últimos 10 para contexto
        ]
        
        # Stream desde DeepSeek
        api_key = self.get_api_key()  # Desde config
        full_response = ""
        
        async for chunk in create_completion_stream(messages, api_key):
            full_response += chunk
            bot_msg.update(f"🤖 {full_response}")
            await asyncio.sleep(0.05)
        
        # Calcular delta
        old_prompt = session["system_prompt"]
        delta = calculate_delta(old_prompt, full_response)
        self.delta_score = delta
        
        # Actualizar sesión
        session["messages"].append({"role": "assistant", "content": full_response})
        update_session(self.session_id, {"messages": session["messages"]})
        
        self.streaming = False
        chat_area.scroll_end(animate=False)
    
    def get_api_key(self) -> str:
        """Obtener API key de configuración"""
        # Implementar: leer de config.yaml o variable de entorno
        return os.getenv("DEEPSEEK_API_KEY", "")
    
    def action_save_session(self) -> None:
        """Guardar sesión"""
        self.notify("Sesión guardada!", severity="information")
    
    def action_toggle_logs(self) -> None:
        """Mostrar/ocultar logs"""
        log_panel = self.query_one("#log-panel", RichLog)
        log_panel.display = not log_panel.display
    
    def action_toggle_dark(self) -> None:
        """Toggle dark mode"""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
    
    def action_help(self) -> None:
        """Mostrar ayuda"""
        from textual.screen import ModalScreen
        
        class HelpScreen(ModalScreen):
            def compose(self) -> ComposeResult:
                yield Static("""
╔═══════════════════════════════════════════╗
║  AgenteDeCambio CLI - Ayuda               ║
╠═══════════════════════════════════════════╣
║  Ctrl+S  - Guardar sesión                 ║
║  Ctrl+L  - Toggle logs                    ║
║  Ctrl+D  - Toggle dark mode               ║
║  F1      - Esta ayuda                     ║
║  Enter   - Enviar mensaje                 ║
║  Ctrl+Q  - Salir                          ║
╚═══════════════════════════════════════════╝
                """)
        
        self.push_screen(HelpScreen())


if __name__ == "__main__":
    app = AgenteDeCambioApp()
    app.run()
```

---

## 5. TCSS (chat_dashboard.tcss)

```css
/* chat_dashboard.tcss */

Screen {
    overflow: hidden;
}

/* Metrics bar */
#metrics-bar {
    height: 8;
    align: center middle;
    padding: 1;
}

#delta-gauge {
    width: 80%;
    height: 100%;
}

#connection-status {
    width: 20%;
    content-align: right middle;
    text-align: right;
    padding-left: 2;
}

#connection-status.connected {
    color: $success;
    text-style: bold;
}

/* Chat area */
#chat-area {
    height: 1fr;
    border: solid $secondary;
    padding: 1;
    margin: 1 0;
    scrollbar-gutter: stable;
}

/* Input area */
#input-area {
    height: 3;
    dock: bottom;
    padding: 0 1;
}

#chat-input {
    width: 3fr;
    height: 100%;
}

#send-btn {
    width: 1fr;
    height: 100%;
    margin-left: 1;
}

/* Log panel */
#log-panel {
    display: none;
    height: 10;
    dock: bottom;
    border: solid $warning;
    background: $surface;
}

/* Mensajes de chat */
.message-user {
    background: $secondary;
    color: $text;
    padding: 1 2;
    margin: 1 0;
    align: right;
    text-align: right;
    border: round $primary;
}

.message-assistant {
    background: $surface;
    color: $text;
    padding: 1 2;
    margin: 1 0;
    align: left;
    text-align: left;
    border: round $success;
}

/* Cuestionario */
#questionnaire-widget {
    height: 1fr;
}

/* Config */
#config Label {
    padding: 1 0;
}

#api-key-input {
    width: 100%;
    margin: 1 0;
}

/* Botones */
Button {
    margin: 1 0;
}

Button.primary {
    background: $primary;
}

/* Pestañas */
TabbedContent {
    height: 1fr;
}

TabPane {
    padding: 1;
}
```

---

## 6. Hitos de Implementación

### Fase 3A: Estructura Base (Textual 100%)
- [ ] Crear estructura de carpetas
- [ ] Implementar modules/core/ (deepseek, delta, prompt, session)
- [ ] Implementar widgets Textual básicos (ChatMessage, QuestionnaireWidget)
- [ ] TCSS completo
- [ ] App principal funcional

### Fase 3B: Componentes Ratatui (10%)
- [ ] Configurar proyecto Rust en `modules/ui/ratatui_components/`
- [ ] Implementar `render_line_gauge()` en Rust
- [ ] Implementar `render_sparkline()` en Rust
- [ ] Crear puente Python (hybrid_renderer.py) con ctypes
- [ ] Integrar HybridDeltaGauge en app Textual

### Fase 3C: Integración y Testing
- [ ] Tests unitarios para modules/core/
- [ ] Tests de integración Textual
- [ ] Tests de componentes Ratatui
- [ ] Validar streaming en tiempo real
- [ ] Validar protocolo JSON
- [ ] Documentación final

---

## 7. Comandos de Desarrollo

### Instalar dependencias
```bash
# Python
cd AGENTES/sub-agentes/AgenteDeCambio
pip install textual textual-dev httpx rich

# Rust (para componentes Ratatui)
cd modules/ui/ratatui_components
cargo build --release
```

### Correr app
```bash
# Modo desarrollo (Textual)
textual run --dev src/main.py

# Modo producción
python src/main.py
```

### Tests
```bash
# Tests Python
pytest tests/

# Tests Rust
cd modules/ui/ratatui_components
cargo test
```

---

*Documento creado: 15-03-2026*  
*Estado: [OK] - Plan de implementación listo*

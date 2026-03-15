# TEXTUAL - Patrones Avanzados y Código Clave

## Módulo: Patrones de Diseño para AgenteDeCambio CLI

---

## 1. Patrón Chat Dashboard (Base para AgenteDeCambio)

```python
"""
Chat Dashboard - Base para AgenteDeCambio CLI
Patrón completo con streaming, gauge de delta y pestañas
"""
from __future__ import annotations
import asyncio
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widgets import (
    Button, Digits, Footer, Header, Input, Label,
    ProgressBar, RichLog, Sparkline, Static, TabbedContent, TabPane
)

if TYPE_CHECKING:
    from textual.widgets._tabbed_content import TabbedContent


class DeltaGauge(Static):
    """
    Widget personalizado para mostrar métricas de deriva (0.0 - 1.0)
    Similar a Gauge de Ratatui pero en Textual
    """
    
    # Reactivos para delta y threshold
    delta = reactive(0.0)
    threshold = reactive(0.3)
    
    DEFAULT_CSS = """
    DeltaGauge {
        height: 3;
        background: $surface;
        border: solid $primary;
        padding: 0 1;
        margin: 1 0;
    }
    
    DeltaGauge.ok {
        border: solid $success;
    }
    
    DeltaGauge.warning {
        border: solid $warning;
    }
    
    DeltaGauge.error {
        border: solid $error;
    }
    """
    
    def render(self) -> str:
        """Renderiza gauge como barra de progreso ASCII"""
        filled = int(self.delta * 40)
        bar = "█" * filled + "░" * (40 - filled)
        
        # Determinar estado
        if self.delta < self.threshold:
            status = "✓ OK"
            self.add_class("ok")
            self.remove_class("warning", "error")
        elif self.delta < 0.7:
            status = "⚠ REVIEW"
            self.add_class("warning")
            self.remove_class("ok", "error")
        else:
            status = "✗ REJECT"
            self.add_class("error")
            self.remove_class("ok", "warning")
        
        return (
            f"Deriva: [{bar}] {self.delta*100:.1f}%/{self.threshold*100:.1f}% {status}"
        )
    
    def watch_delta(self, new_value: float) -> None:
        """Callback cuando delta cambia - auto refresh"""
        self.refresh()


class ChatMessage(Static):
    """Widget para burbuja de chat individual"""
    
    def __init__(self, role: str, content: str, **kwargs) -> None:
        """
        Args:
            role: "user" o "assistant"
            content: Contenido del mensaje
        """
        super().__init__(content, **kwargs)
        self.role = role
        self.add_class(f"message-{role}")
    
    DEFAULT_CSS = """
    .message-user {
        background: $secondary;
        color: $text;
        padding: 1 2;
        margin: 1 0;
        align: right;
        text-align: right;
    }
    
    .message-assistant {
        background: $surface;
        color: $text;
        padding: 1 2;
        margin: 1 0;
        align: left;
        text-align: left;
    }
    """


class ChatDashboard(App):
    """
    Dashboard principal para AgenteDeCambio CLI
    
    Features:
    - Chat con streaming
    - Gauge de delta en tiempo real
    - Pestañas Chat/Cuestionario/Config
    - RichLog para logs
    """
    
    CSS_PATH = "chat_dashboard.tcss"
    
    BINDINGS = [
        Binding("ctrl+s", "save_session", "Save"),
        Binding("ctrl+l", "toggle_logs", "Logs"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("f1", "help", "Help"),
    ]
    
    # Estado reactivo
    connected = reactive(False)
    streaming = reactive(False)
    delta_score = reactive(0.0)
    
    def compose(self) -> ComposeResult:
        """Componer UI completa"""
        yield Header()
        
        with TabbedContent(initial="chat"):
            # Pestaña CHAT
            with TabPane("💬 Chat", id="chat"):
                with Vertical():
                    # Header con métricas
                    with Horizontal(id="metrics-bar"):
                        yield DeltaGauge(id="delta-gauge")
                        yield Label("", id="connection-status")
                    
                    # Área de chat (scrollable)
                    with VerticalScroll(id="chat-area"):
                        yield Static("🤖 Bot: Hello! How can I help you today?", classes="message-assistant")
                    
                    # Input area
                    with Horizontal(id="input-area"):
                        yield Input(
                            placeholder="Type your message...",
                            id="chat-input"
                        )
                        yield Button("Send", id="send-btn", variant="primary")
            
            # Pestaña CUESTIONARIO
            with TabPane("📋 Cuestionario", id="questionnaire"):
                yield Static("Questionnaire view - coming soon", id="questionnaire-placeholder")
            
            # Pestaña CONFIG
            with TabPane("⚙️ Config", id="config"):
                with VerticalScroll():
                    yield Label("API Configuration")
                    yield Input(placeholder="DeepSeek API Key", id="api-key-input", password=True)
                    yield Label("Threshold: 0.3")
                    yield Label("Model: deepseek-chat")
        
        # Panel de logs (oculto por defecto)
        yield RichLog(id="log-panel", highlight=True, markup=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Inicializar app"""
        # Iniciar conexión
        self.connect_to_server()
    
    def watch_connected(self, connected: bool) -> None:
        """Actualizar estado de conexión"""
        status_label = self.query_one("#connection-status", Label)
        if connected:
            status_label.update("🟢 Connected")
            status_label.add_class("connected")
        else:
            status_label.update("🔴 Disconnected")
            status_label.remove_class("connected")
    
    def watch_streaming(self, streaming: bool) -> None:
        """Actualizar estado de streaming"""
        input_widget = self.query_one("#chat-input", Input)
        send_btn = self.query_one("#send-btn", Button)
        
        if streaming:
            input_widget.disabled = True
            send_btn.disabled = True
            send_btn.label = "Streaming..."
        else:
            input_widget.disabled = False
            send_btn.disabled = False
            send_btn.label = "Send"
            input_widget.focus()
    
    def watch_delta_score(self, score: float) -> None:
        """Actualizar gauge de delta"""
        gauge = self.query_one("#delta-gauge", DeltaGauge)
        gauge.delta = score
    
    @on(Button.Pressed, "#send-btn")
    def on_send_pressed(self, event: Button.Pressed) -> None:
        """Manejar envío de mensaje"""
        self.send_message()
    
    @on(Input.Submitted, "#chat-input")
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Manejar Enter en input"""
        self.send_message()
    
    def send_message(self) -> None:
        """Enviar mensaje al servidor (simulado)"""
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
        
        # Iniciar streaming de respuesta
        self.stream_response(message)
    
    @work(exclusive=True)
    async def stream_response(self, user_message: str) -> None:
        """
        Worker asíncrono para streaming de respuesta
        
        Uses @work decorator para correr en background
        exclusive=True cancela workers previos
        """
        self.streaming = True
        
        chat_area = self.query_one("#chat-area", VerticalScroll)
        
        # Crear mensaje de bot vacío
        bot_msg = ChatMessage("assistant", "🤖 Bot: ")
        chat_area.mount(bot_msg)
        
        # Simular streaming (reemplazar con llamada real a DeepSeek)
        response = await self.call_deepseek(user_message)
        
        # Stream carácter por carácter
        full_text = "🤖 Bot: "
        for chunk in response:
            full_text += chunk
            bot_msg.update(full_text)
            await asyncio.sleep(0.05)  # Simular delay
        
        # Calcular delta
        self.delta_score = 0.25  # Simulado
        
        self.streaming = False
        
        # Scroll al final
        chat_area.scroll_end(animate=False)
    
    async def call_deepseek(self, message: str) -> str:
        """
        Llamar a DeepSeek API (simulado)
        
        En producción: usar modules/core/deepseek_connector.py
        """
        await asyncio.sleep(0.5)  # Simular network delay
        
        # Generator para streaming
        sample_response = "This is a simulated response from DeepSeek. " \
                         "In production, this would stream real tokens from the API."
        
        for word in sample_response.split():
            yield word + " "
            await asyncio.sleep(0.1)
    
    @work
    async def connect_to_server(self) -> None:
        """Worker para conectar al servidor"""
        await asyncio.sleep(1)  # Simular conexión
        self.connected = True
    
    def action_save_session(self) -> None:
        """Guardar sesión"""
        self.notify("Session saved!", severity="information")
    
    def action_toggle_logs(self) -> None:
        """Mostrar/ocultar panel de logs"""
        log_panel = self.query_one("#log-panel", RichLog)
        log_panel.display = not log_panel.display
    
    def action_help(self) -> None:
        """Mostrar ayuda"""
        from textual.screen import ModalScreen
        
        class HelpScreen(ModalScreen):
            def compose(self) -> ComposeResult:
                yield Static("""
╔═══════════════════════════════════════════╗
║  AgenteDeCambio CLI - Help                ║
╠═══════════════════════════════════════════╣
║  Ctrl+S  - Save session                   ║
║  Ctrl+L  - Toggle logs                    ║
║  Ctrl+Q  - Quit                           ║
║  F1      - This help                      ║
║  Enter   - Send message                   ║
║  Esc     - Close dialogs                  ║
╚═══════════════════════════════════════════╝
                """)
        
        self.push_screen(HelpScreen())


if __name__ == "__main__":
    app = ChatDashboard()
    app.run()
```

---

## 2. TCSS para Chat Dashboard

```css
/* chat_dashboard.tcss */

/* Layout principal */
Screen {
    overflow: hidden;
}

/* Metrics bar */
#metrics-bar {
    height: 5;
    align: center middle;
}

#delta-gauge {
    width: 80%;
}

#connection-status {
    width: 20%;
    content-align: right middle;
    text-align: right;
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

/* Pestañas */
TabbedContent {
    height: 1fr;
}

TabPane {
    padding: 1;
}

/* Placeholder */
#questionnaire-placeholder {
    content-align: center middle;
    text-align: center;
    color: $text-muted;
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

/* Variantes de botones */
Button {
    margin: 1 0;
}

Button.primary {
    background: $primary;
}

Button.success {
    background: $success;
}

Button.warning {
    background: $warning;
}

Button.error {
    background: $error;
}

/* Input fields */
Input {
    border: solid $primary;
}

Input:focus {
    border: solid $success;
    background: $surface;
}

/* Labels */
Label {
    padding: 1 0;
}

/* Sparkline widget */
Sparkline {
    height: 5;
    margin: 1 0;
}

/* Progress bar */
ProgressBar {
    height: 3;
    margin: 1 0;
}

/* DataTable */
DataTable {
    height: 1fr;
    border: solid $secondary;
}

/* Tree widget */
Tree {
    width: 30%;
    dock: left;
    border: solid $secondary;
}

/* TextArea */
TextArea {
    height: 10;
    border: solid $primary;
}

/* Modal screens */
ModalScreen {
    align: center middle;
}

ModalScreen > Static {
    background: $surface;
    border: solid $primary;
    padding: 2 4;
    width: 80%;
    height: auto;
}
```

---

## 3. Patrón Worker Asíncrono (Streaming)

```python
"""
Patrón para workers asíncronos con streaming
Esencial para llamadas a APIs de IA
"""
from textual import work
from textual.app import App
from textual.widgets import RichLog, Button
import asyncio


class StreamingApp(App):
    """App que demuestra streaming con workers"""
    
    def compose(self):
        yield RichLog(id="log")
        yield Button("Start Stream", id="start")
    
    @on(Button.Pressed, "#start")
    def start_stream(self):
        """Iniciar worker de streaming"""
        self.do_stream()
    
    @work(exclusive=True)  # Cancela workers previos
    async def do_stream(self):
        """
        Worker asíncrono para streaming
        
        exclusive=True: Cancela ejecución previa si se llama de nuevo
        """
        log = self.query_one("#log", RichLog)
        log.write("Starting stream...")
        
        # Simular llamada API con streaming
        async for chunk in self.stream_data():
            log.write(f"Received: {chunk}")
            await asyncio.sleep(0.1)
        
        log.write("Stream complete!")
    
    async def stream_data(self):
        """Generator asíncrono para datos"""
        for i in range(10):
            yield f"Chunk {i}"
            await asyncio.sleep(0.5)
```

---

## 4. Patrón Reactive Avanzado

```python
"""
Patrones reactivos avanzados para estado complejo
"""
from textual.reactive import reactive, var
from textual.app import App
from textual.widgets import Label, Input


class ReactiveApp(App):
    """Demo de patrones reactivos"""
    
    # var: Variable interna (no dispara watch)
    counter_internal = var(0)
    
    # reactive: Dispara watch_* y compute_*
    counter = reactive(0)
    
    # reactive con compute
    doubled = reactive(0)
    
    def compute_doubled(self) -> int:
        """Calculado automáticamente cuando counter cambia"""
        return self.counter * 2
    
    def watch_counter(self, value: int) -> None:
        """Callback cuando counter cambia"""
        self.notify(f"Counter changed to {value}")
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Actualizar reactivo"""
        self.counter = int(event.value)
        # doubled se actualiza automáticamente
```

---

## 5. Patrón Custom Widget

```python
"""
Crear widgets personalizados desde cero
"""
from textual.widget import Widget
from textual.message import Message
from textual.events import Click


class CustomWidget(Widget):
    """Widget personalizado con eventos custom"""
    
    # Mensaje custom
    class Changed(Message):
        def __init__(self, value: str):
            self.value = value
            super().__init__()
    
    DEFAULT_CSS = """
    CustomWidget {
        height: 3;
        background: $primary;
        color: $text;
        content-align: center middle;
    }
    
    CustomWidget:hover {
        background: $secondary;
    }
    """
    
    def __init__(self, label: str, **kwargs):
        super().__init__(**kwargs)
        self.label = label
    
    def render(self) -> str:
        """Renderizar widget"""
        return f"[ {self.label} ]"
    
    def on_click(self, event: Click) -> None:
        """Emitir mensaje custom"""
        self.post_message(self.Changed("clicked!"))
```

---

## 6. Patrón Screen con Resultado

```python
"""
Screens que retornan resultados (como modales)
"""
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.containers import Vertical


class InputScreen(ModalScreen[str]):
    """Modal que retorna un string"""
    
    def compose(self):
        with Vertical():
            yield Label("Enter value:")
            yield Input(id="input")
            yield Button("OK", id="ok")
            yield Button("Cancel", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            input_val = self.query_one("#input", Input)
            self.dismiss(input_val.value)  # Retorna valor
        else:
            self.dismiss(None)  # Cancela


# Uso en app principal
class MainApp(App):
    def on_mount(self):
        # Abrir modal y esperar resultado
        def on_result(result: str):
            if result:
                self.notify(f"Received: {result}")
        
        self.push_screen(InputScreen(), on_result)
```

---

## 7. Patrón Command Palette Custom

```python
"""
Comandos custom para Command Palette (Ctrl+P)
"""
from textual.command import Provider, Hit, Hits
from textual.app import App


class CustomCommands(Provider):
    """Proveedor de comandos custom"""
    
    async def search(self, query: str) -> Hits:
        """Buscar comandos"""
        matcher = self.matcher(query)
        
        # Comandos disponibles
        commands = [
            ("save", "Save Session", self.app.action_save),
            ("load", "Load Session", self.app.action_load),
            ("clear", "Clear Chat", self.app.action_clear),
        ]
        
        for name, help_text, action in commands:
            score = matcher.match(name)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(name),
                    action,
                    help=help_text,
                )


class AppWithCommands(App):
    """App con command palette custom"""
    
    COMMANDS = [CustomCommands]
    
    def action_save(self):
        self.notify("Saving...")
    
    def action_load(self):
        self.notify("Loading...")
    
    def action_clear(self):
        self.notify("Clearing...")
```

---

## 8. Patrón Testing

```python
"""
Tests para apps Textual
"""
import pytest
from textual.testing import run_test
from textual.app import App
from textual.widgets import Button, Label


class TestApp(App):
    def compose(self):
        yield Button("Click me", id="btn")
        yield Label("0", id="count")
    
    def on_button_pressed(self):
        label = self.query_one("#count", Label)
        label.update(str(int(label.renderable) + 1))


async def test_button_increments_counter():
    """Test que presiona botón y verifica contador"""
    async with run_test(TestApp()) as pilot:
        app = pilot.app
        
        # Estado inicial
        assert app.query_one("#count", Label).renderable == "0"
        
        # Presionar botón
        await pilot.click("#btn")
        await pilot.pause()  # Esperar actualización
        
        # Verificar
        assert app.query_one("#count", Label).renderable == "1"
        
        # Presionar de nuevo
        await pilot.click("#btn")
        await pilot.pause()
        
        assert app.query_one("#count", Label).renderable == "2"
```

---

*Documento creado: 15-03-2026*  
*Estado: [OK] - Patrones avanzados listos*

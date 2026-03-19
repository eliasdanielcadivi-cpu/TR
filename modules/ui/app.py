"""
AgenteDeCambio App - Interfaz TUI principal

Módulo atómico (≤3 funciones) - Filosofía ARES

Funcionalidades:
1. create_app - Crea y configura la aplicación Textual
2. run_app - Ejecuta la aplicación en modo interactivo
3. demo_app - Ejecuta demo de componentes

Flujo de Datos:
- Entrada: Comandos de línea (run, demo, test)
- Procesamiento: Textual App con widgets
- Salida: Interfaz TUI interactiva

Ejemplo de Uso:
```python
# Ejemplo 1: Ejecutar app completa
run_app()

# Ejemplo 2: Ejecutar demo
demo_app()

# Ejemplo 3: Desde CLI
ares agente AgenteDeCambio run
```
"""

import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, Label
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.binding import Binding
from textual.reactive import reactive

from ..core import (
    create_session, get_session, update_session,
    create_completion_stream, calculate, compare, threshold,
    build_system_prompt, BuildPromptParams
)


# ============================================================================
# WIDGETS PERSONALIZADOS
# ============================================================================

class ChatMessage(Static):
    """
    Widget para burbuja de chat individual
    
    Attributes:
        role: "user" o "assistant"
        content: Contenido del mensaje
    """
    
    DEFAULT_CSS = """
    ChatMessage {
        padding: 1 2;
        margin: 1 0;
        width: 100%;
    }
    
    ChatMessage.user {
        background: $secondary;
        color: $text;
        align: right middle;
        text-align: right;
    }
    
    ChatMessage.assistant {
        background: $surface;
        color: $text;
        align: left middle;
        text-align: left;
    }
    """
    
    def __init__(self, role: str, content: str, **kwargs) -> None:
        """
        Inicializar mensaje de chat
        
        Args:
            role: "user" o "assistant"
            content: Contenido del mensaje
        """
        super().__init__(content, **kwargs)
        self.role = role
        self.add_class(role)


class DeltaDisplay(Static):
    """
    Widget para mostrar métrica de deriva delta
    
    Attributes:
        delta: Score de deriva (0.0 - 1.0)
        threshold: Umbral de aprobación (default: 0.3)
    """
    
    delta = reactive(0.0)
    threshold = reactive(0.3)
    
    DEFAULT_CSS = """
    DeltaDisplay {
        padding: 0 1;
        margin: 0 1;
        width: auto;
    }
    
    DeltaDisplay.ok {
        color: $success;
    }
    
    DeltaDisplay.warning {
        color: $warning;
    }
    
    DeltaDisplay.error {
        color: $error;
    }
    """
    
    def render(self) -> str:
        """
        Renderizar display de delta
        
        Returns:
            String formateado con delta y estado
        """
        if self.delta < self.threshold:
            status = "✓"
            self.add_class("ok")
            self.remove_class("warning", "error")
        elif self.delta < 0.7:
            status = "⚠"
            self.add_class("warning")
            self.remove_class("ok", "error")
        else:
            status = "✗"
            self.add_class("error")
            self.remove_class("ok", "warning")
        
        return f"Δ: {self.delta*100:.0f}% {status}"
    
    def watch_delta(self, new_value: float) -> None:
        """Callback cuando delta cambia"""
        self.refresh()


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

class AgenteDeCambioApp(App):
    """
    Aplicación principal de AgenteDeCambio CLI
    
    Attributes:
        session_id: ID de sesión actual
        delta_score: Score de deriva actual
        streaming: Estado de streaming
    """
    
    CSS = """
    Screen {
        background: $background;
    }
    
    #chat-area {
        height: 1fr;
        border: solid $secondary;
        padding: 1;
        margin: 1 0;
    }
    
    #input-area {
        height: 3;
        dock: bottom;
        padding: 0 1;
    }
    
    #chat-input {
        width: 3fr;
    }
    
    #send-btn {
        width: 1fr;
        margin-left: 1;
    }
    
    #metrics-bar {
        height: 3;
        background: $panel;
        padding: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Salir"),
        Binding("ctrl+s", "save_session", "Guardar"),
        Binding("f1", "help", "Ayuda"),
    ]
    
    # Estado reactivo
    session_id = reactive(None)
    delta_score = reactive(0.0)
    streaming = reactive(False)
    
    def compose(self) -> ComposeResult:
        """
        Componer UI completa
        
        Yields:
            Widgets de la interfaz
        """
        yield Header()
        
        # Barra de métricas
        with Horizontal(id="metrics-bar"):
            yield Static("🤖 AgenteDeCambio", id="title")
            yield DeltaDisplay(id="delta-display")
            yield Static("", id="status")
        
        # Área de chat
        with ScrollableContainer(id="chat-area"):
            yield ChatMessage("assistant", "🤖 Hola, soy AgenteDeCambio. ¿En qué puedo ayudarte hoy?")
        
        # Área de input
        with Horizontal(id="input-area"):
            yield Input(placeholder="Escribe tu mensaje...", id="chat-input")
            yield Button("Enviar", id="send-btn", variant="primary")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """
        Inicializar app al montar
        
        Crea sesión y configura estado inicial
        """
        # Inicializar base de datos
        from ..core import init_db
        init_db()
        
        # Crear sesión
        session = create_session()
        self.session_id = session["id"]
        
        # Actualizar título
        self.title = "AgenteDeCambio CLI"
        self.sub_title = f"Sesión: {self.session_id[-8:]} | Δ: {self.delta_score*100:.0f}%"
        
        # Configurar display de delta
        self.update_delta_display()
    
    def watch_delta_score(self, new_value: float) -> None:
        """Callback cuando delta cambia"""
        self.sub_title = f"Sesión: {self.session_id[-8:]} | Δ: {new_value*100:.0f}%"
        self.update_delta_display()
    
    def update_delta_display(self) -> None:
        """Actualizar display de delta"""
        try:
            delta_display = self.query_one("#delta-display", DeltaDisplay)
            delta_display.delta = self.delta_score
        except Exception:
            pass  # Widget no existe aún
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Manejar Enter en input
        
        Args:
            event: Evento de input submit
        """
        if event.input.id == "chat-input":
            self.send_message()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Manejar click en botón
        
        Args:
            event: Evento de botón presionado
        """
        if event.button.id == "send-btn":
            self.send_message()
    
    def send_message(self) -> None:
        """
        Enviar mensaje del usuario
        
        Obtiene texto del input, crea mensaje y procesa respuesta
        con streaming desde DeepSeek API
        """
        input_widget = self.query_one("#chat-input", Input)
        message = input_widget.value.strip()
        
        if not message:
            return
        
        chat_area = self.query_one("#chat-area", ScrollableContainer)
        
        # Añadir mensaje de usuario
        user_msg = ChatMessage("user", message)
        chat_area.mount(user_msg)
        
        # Limpiar input
        input_widget.value = ""
        input_widget.disabled = True
        
        # Crear mensaje de bot vacío para streaming
        bot_msg = ChatMessage("assistant", "🤖 ")
        chat_area.mount(bot_msg)
        
        # Iniciar streaming
        self.stream_response(message, bot_msg)
    
    async def stream_response(self, user_message: str, bot_msg: ChatMessage) -> None:
        """
        Stream de respuesta desde DeepSeek API
        
        Args:
            user_message: Mensaje del usuario
            bot_msg: Widget de mensaje del bot a actualizar
        """
        try:
            # Obtener API Key
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                bot_msg.update("🤖 ⚠️ Error: DEEPSEEK_API_KEY no configurada")
                self.notify("Configura DEEPSEEK_API_KEY en tu entorno", severity="error")
                return
            
            # Obtener sesión
            session = get_session(self.session_id)
            if not session:
                session = create_session(self.session_id)
            
            # Añadir mensaje de usuario a sesión
            session["messages"].append({"role": "user", "content": user_message})
            
            # Construir system prompt
            prompt = build_system_prompt(BuildPromptParams(
                base_prompt=session["system_prompt"],
                objectives=session.get("objectives", []),
                mode="chat"
            ))
            
            # Preparar mensajes para API
            messages = [
                {"role": "system", "content": prompt},
                *session["messages"][-10:]  # Últimos 10 para contexto
            ]
            
            # Stream desde DeepSeek
            full_response = "🤖 "
            async for chunk in create_completion_stream(messages, api_key):
                full_response += chunk
                bot_msg.update(full_response)
                self.streaming = True
            
            # Streaming completado
            self.streaming = False
            input_widget.disabled = False
            input_widget.focus()
            
            # Guardar respuesta en sesión
            session["messages"].append({"role": "assistant", "content": full_response[4:]})  # Quitar "🤖 "
            update_session(self.session_id, {"messages": session["messages"]})
            
            # Calcular delta
            old_prompt = session["system_prompt"]
            delta = calculate(old_prompt, full_response[4:])
            self.delta_score = delta
            
            # Scroll al final
            chat_area = self.query_one("#chat-area", ScrollableContainer)
            chat_area.scroll_end(animate=False)
            
        except Exception as e:
            bot_msg.update(f"🤖 ⚠️ Error: {str(e)}")
            self.streaming = False
            input_widget.disabled = False
            input_widget.focus()
            self.notify(f"Error en streaming: {str(e)}", severity="error")
    
    def action_save_session(self) -> None:
        """Guardar sesión actual"""
        session = get_session(self.session_id)
        if session:
            msg_count = len(session.get("messages", []))
            self.notify(f"Sesión guardada ({msg_count} mensajes)", severity="information")
        else:
            self.notify("Error: Sesión no encontrada", severity="error")
    
    def action_help(self) -> None:
        """Mostrar ayuda"""
        help_text = (
            "Atajos de teclado:\n"
            "  Ctrl+Q: Salir\n"
            "  Ctrl+S: Guardar sesión\n"
            "  Enter: Enviar mensaje\n"
            "  F1: Esta ayuda"
        )
        self.notify(help_text, severity="information", timeout=10)


# ============================================================================
# FUNCIONES EXPORTADAS (API PÚBLICA DEL MÓDULO)
# ============================================================================

def create_app() -> AgenteDeCambioApp:
    """
    Crea y configura la aplicación Textual
    
    Returns:
        Instancia de AgenteDeCambioApp configurada
    
    Example:
        app = create_app()
        app.run()
    """
    return AgenteDeCambioApp()


def run_app() -> None:
    """
    Ejecuta la aplicación en modo interactivo
    
    Example:
        run_app()
    """
    print("Creando app...")
    app = create_app()
    print(f"App creada: {app}")
    print(f"App title: {app.title}")
    print("Iniciando Textual run()...")
    try:
        app.run()
        print("App finalizada")
    except Exception as e:
        print(f"Error en app.run(): {e}")
        import traceback
        traceback.print_exc()
        raise


def demo_app() -> None:
    """
    Ejecuta demo de componentes
    
    Muestra widgets básicos sin funcionalidad completa
    
    Example:
        demo_app()
    """
    from textual.app import App, ComposeResult
    from textual.widgets import Header, Footer, Label
    from textual.containers import Container
    
    class DemoApp(App):
        def compose(self) -> ComposeResult:
            yield Header()
            with Container():
                yield Label("🤖 AgenteDeCambio Demo")
                yield Label("Componentes básicos funcionando")
            yield Footer()
    
    app = DemoApp()
    app.run()

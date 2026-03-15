# TEXTUAL - Cuaderno de Apuntes IA Definitivo

## Módulo: Framework TUI Moderno para Python

> **"If you want people to build things, make it fun."** — Will McGugan (creador de Rich y Textual)

---

## 1. Problema Detectado

**Síntoma:** Necesitamos construir interfaces CLI profesionales para AgenteDeCambio CLI con:
- Dashboards interactivos
- Chat en tiempo real
- Formularios complejos
- Visualización de datos (gauges, tablas, sparklines)
- Streaming de texto
- Navegación por pestañas

**Necesidad:** Dominar Textual al máximo nivel para crear la **mejor interfaz TUI posible** que sirva como base para todas las herramientas CLI de TRON/ARES.

---

## 2. Causa Raíz

**Textual es:**
- Framework TUI moderno para Python (3.9+)
- Construido sobre Rich (rich text formatting)
- Asíncrono nativo (asyncio)
- Multiplataforma (Windows, macOS, Linux)
- Funciona en terminal **Y** navegador web (textual serve)
- 50+ widgets builtin
- CSS-like styling (TCSS)
- Command Palette fuzzy search (Ctrl+P)
- Dev Console para debugging
- Testing framework integrado

**Versión actual:** 8.1.1 (poetry)

---

## 3. API Disponible (Arquitectura)

### 3.1 Estructura del Proyecto

```
textual/
├── src/textual/              # Código fuente principal
│   ├── app.py                # Clase App base
│   ├── widget.py             # Clase Widget base
│   ├── widgets/              # Widgets builtin (59 archivos)
│   │   ├── __init__.py       # Exports públicos
│   │   ├── _button.py        # Button widget
│   │   ├── _data_table.py    # DataTable widget
│   │   ├── _input.py         # Input widget
│   │   ├── _label.py         # Label widget
│   │   ├── _progress_bar.py  # ProgressBar widget
│   │   ├── _sparkline.py     # Sparkline widget
│   │   ├── _static.py        # Static widget
│   │   ├── _tabs.py          # Tabs widget
│   │   ├── _text_area.py     # TextArea widget
│   │   ├── _tree.py          # Tree widget
│   │   └── ... (40+ widgets más)
│   ├── containers.py         # Container widgets
│   │   ├── Container
│   │   ├── Horizontal
│   │   ├── Vertical
│   │   ├── HorizontalScroll
│   │   ├── VerticalScroll
│   │   ├── Grid
│   │   └── ContentSwitcher
│   ├── css/                  # Sistema de estilos
│   │   ├── stylesheet.py
│   │   └── ...
│   ├── layouts/              # Layout engines
│   ├── events.py             # Sistema de eventos
│   ├── binding.py            # Key bindings
│   ├── reactive.py           # Reactive attributes
│   ├── compose.py            # Composition pattern
│   └── ... (80+ módulos)
├── examples/                 # Ejemplos completos
│   ├── clock.py              # Reloj digital
│   ├── calculator.py         # Calculadora macOS-style
│   ├── code_browser.py       # Navegador de código
│   ├── five_by_five.py       # Juego de puzzle
│   └── ...
├── docs/                     # Documentación offline
│   ├── examples/             # Ejemplos de docs
│   ├── guide/                # Guías
│   ├── widgets/              # Referencia de widgets
│   └── ...
└── tests/                    # Tests unitarios
```

### 3.2 Imports Principales

```python
# Imports básicos
from textual.app import App, ComposeResult
from textual.widgets import (
    Button, Checkbox, DataTable, Digits, Footer, Header,
    Input, Label, ListView, OptionList, ProgressBar,
    RichLog, Select, Sparkline, Static, Switch,
    TabbedContent, Tabs, TextArea, Tree
)
from textual.containers import (
    Container, Horizontal, Vertical,
    HorizontalScroll, VerticalScroll, Grid
)
from textual.binding import Binding
from textual.reactive import reactive, var
from textual.on import on

# Imports avanzados
from textual.screen import Screen, ModalScreen
from textual.widget import Widget
from textual.css.query import NoMatches
from textual.events import Event, Key, Click, Focus, Blur
from textual.message import Message
from textual.signal import Signal
from textual.command import Provider, CommandPalette
from textual.worker import Worker, run_worker
```

---

## 4. Solución Implementada (Patrones y Código)

### 4.1 Patrón App Mínima

```python
"""
An App to show the current time.
"""
from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Digits


class ClockApp(App):
    CSS = """
    Screen { align: center middle; }
    Digits { width: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Digits("")

    def on_ready(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")


if __name__ == "__main__":
    app = ClockApp()
    app.run()
```

**Conceptos clave:**
- `CSS`: Stylesheet inline (también puede ser `CSS_PATH = "app.tcss"`)
- `compose()`: Generator que yield widgets
- `on_ready()`: Callback después de mount
- `set_interval()`: Timer asíncrono
- `query_one()`: CSS selector para widgets

---

### 4.2 Patrón Code Browser (App Completa)

```python
"""
Code browser example.
Run with: python code_browser.py PATH
"""
from __future__ import annotations
import sys
from pathlib import Path
from rich.traceback import Traceback

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.highlight import highlight
from textual.reactive import reactive, var
from textual.widgets import DirectoryTree, Footer, Header, Static


class CodeBrowser(App):
    """Textual code browser app."""

    CSS_PATH = "code_browser.tcss"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
    ]

    show_tree = var(True)
    path: reactive[str | None] = reactive(None)

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        yield Header()
        with Container():
            yield DirectoryTree(path, id="tree-view")
            with VerticalScroll(id="code-view"):
                yield Static(id="code", expand=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when user clicks file in directory tree."""
        event.stop()
        self.path = str(event.path)

    def watch_path(self, path: str | None) -> None:
        """Called when path changes."""
        code_view = self.query_one("#code", Static)
        if path is None:
            code_view.update("")
            return
        try:
            code = Path(path).read_text(encoding="utf-8")
            syntax = highlight(code, path=path)
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = path

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree


if __name__ == "__main__":
    CodeBrowser().run()
```

**TCSS (code_browser.tcss):**
```css
Screen {
    &:inline {
        height: 50vh;
    }
}

#tree-view {
    display: none;
    scrollbar-gutter: stable;
    overflow: auto;
    width: auto;
    height: 100%;
    dock: left;
}

CodeBrowser.-show-tree #tree-view {
    display: block;
    max-width: 50%;
}

#code-view {
    overflow: auto scroll;
    min-width: 100%;
    hatch: right $panel;
}

#code {
    width: auto;
    padding: 0 1;
    background: $surface;
}
```

**Conceptos clave:**
- `var()`: Variable reactiva (cambia estado interno)
- `reactive()`: Reactivo que dispara `watch_*`
- `watch_*()`: Callbacks automáticos cuando cambia reactivo
- `BINDINGS`: Lista de (tecla, acción, descripción)
- `action_*()`: Métodos de acción para bindings
- `on_*()`: Handlers de eventos
- `event.stop()`: Detiene propagación de evento
- `with Container()`: Context manager para composición

---

### 4.3 Patrón Calculator (Grid Layout + Lógica)

```python
"""
Classic calculator with macOS-inspired layout.
"""
from decimal import Decimal
from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Button, Digits


class CalculatorApp(App):
    """A working 'desktop' calculator."""

    CSS_PATH = "calculator.tcss"

    numbers = var("0")
    show_ac = var(True)
    left = var(Decimal("0"))
    right = var(Decimal("0"))
    value = var("")
    operator = var("plus")

    NAME_MAP = {
        "asterisk": "multiply",
        "slash": "divide",
        "underscore": "plus-minus",
        "full_stop": "point",
        "plus_minus_sign": "plus-minus",
        "percent_sign": "percent",
        "equals_sign": "equals",
        "minus": "minus",
        "plus": "plus",
    }

    def watch_numbers(self, value: str) -> None:
        """Called when numbers is updated."""
        self.query_one("#numbers", Digits).update(value)

    def compute_show_ac(self) -> bool:
        """Compute switch to show AC or C button"""
        return self.value in ("", "0") and self.numbers == "0"

    def watch_show_ac(self, show_ac: bool) -> None:
        """Called when show_ac changes."""
        self.query_one("#c").display = not show_ac
        self.query_one("#ac").display = show_ac

    def compose(self) -> ComposeResult:
        """Add our buttons."""
        with Container(id="calculator"):
            yield Digits(id="numbers")
            yield Button("AC", id="ac", variant="primary")
            yield Button("C", id="c", variant="primary")
            yield Button("+/-", id="plus-minus", variant="primary")
            yield Button("%", id="percent", variant="primary")
            yield Button("÷", id="divide", variant="warning")
            yield Button("7", id="number-7", classes="number")
            yield Button("8", id="number-8", classes="number")
            yield Button("9", id="number-9", classes="number")
            yield Button("×", id="multiply", variant="warning")
            yield Button("4", id="number-4", classes="number")
            yield Button("5", id="number-5", classes="number")
            yield Button("6", id="number-6", classes="number")
            yield Button("-", id="minus", variant="warning")
            yield Button("1", id="number-1", classes="number")
            yield Button("2", id="number-2", classes="number")
            yield Button("3", id="number-3", classes="number")
            yield Button("+", id="plus", variant="warning")
            yield Button("0", id="number-0", classes="number")
            yield Button(".", id="point")
            yield Button("=", id="equals", variant="warning")

    def on_key(self, event: events.Key) -> None:
        """Called when user presses a key."""
        def press(button_id: str) -> None:
            """Press a button, should it exist."""
            try:
                self.query_one(f"#{button_id}", Button).press()
            except NoMatches:
                pass

        key = event.key
        if key.isdecimal():
            press(f"number-{key}")
        elif key == "c":
            press("c")
            press("ac")
        else:
            button_id = self.NAME_MAP.get(key)
            if button_id is not None:
                press(self.NAME_MAP.get(key, key))

    @on(Button.Pressed, ".number")
    def number_pressed(self, event: Button.Pressed) -> None:
        """Pressed a number."""
        assert event.button.id is not None
        number = event.button.id.partition("-")[-1]
        self.numbers = self.value = self.value.lstrip("0") + number

    @on(Button.Pressed, "#plus-minus")
    def plus_minus_pressed(self) -> None:
        """Pressed + / -"""
        self.numbers = self.value = str(Decimal(self.value or "0") * -1)

    @on(Button.Pressed, "#percent")
    def percent_pressed(self) -> None:
        """Pressed %"""
        self.numbers = self.value = str(Decimal(self.value or "0") / Decimal(100))

    @on(Button.Pressed, "#point")
    def pressed_point(self) -> None:
        """Pressed ."""
        if "." not in self.value:
            self.numbers = self.value = (self.value or "0") + "."

    @on(Button.Pressed, "#ac")
    def pressed_ac(self) -> None:
        """Pressed AC"""
        self.value = ""
        self.left = self.right = Decimal(0)
        self.operator = "plus"
        self.numbers = "0"

    @on(Button.Pressed, "#c")
    def pressed_c(self) -> None:
        """Pressed C"""
        self.value = ""
        self.numbers = "0"

    def _do_math(self) -> None:
        """Does the math: LEFT OPERATOR RIGHT"""
        try:
            if self.operator == "plus":
                self.left += self.right
            elif self.operator == "minus":
                self.left -= self.right
            elif self.operator == "divide":
                self.left /= self.right
            elif self.operator == "multiply":
                self.left *= self.right
            self.numbers = str(self.left)
            self.value = ""
        except Exception:
            self.numbers = "Error"

    @on(Button.Pressed, "#plus,#minus,#divide,#multiply")
    def pressed_op(self, event: Button.Pressed) -> None:
        """Pressed one of the arithmetic operations."""
        self.right = Decimal(self.value or "0")
        self._do_math()
        assert event.button.id is not None
        self.operator = event.button.id

    @on(Button.Pressed, "#equals")
    def pressed_equals(self) -> None:
        """Pressed ="""
        if self.value:
            self.right = Decimal(self.value)
        self._do_math()


if __name__ == "__main__":
    CalculatorApp().run(inline=True)
```

**TCSS (calculator.tcss):**
```css
Screen {
    overflow: auto;
}

#calculator {
    layout: grid;
    grid-size: 4;
    grid-gutter: 1 2;
    grid-columns: 1fr;
    grid-rows: 2fr 1fr 1fr 1fr 1fr 1fr;
    margin: 1 2;
    min-height: 25;
    min-width: 26;
    height: 100%;

    &:inline {
        margin: 0 2;
    }
}

Button {
    width: 100%;
    height: 100%;
}

#numbers {
    column-span: 4;
    padding: 0 1;
    height: 100%;
    background: $panel;
    color: $text;
    content-align: center middle;
    text-align: right;
}

#number-0 {
    column-span: 2;
}
```

**Conceptos clave:**
- `layout: grid`: Grid layout system
- `grid-size: 4`: 4 columnas
- `grid-gutter`: Espacio entre celdas
- `column-span`: Celdas que ocupa un widget
- `@on()`: Decorador para handlers de eventos
- `event.stop()`: Detener propagación
- `inline=True`: Modo inline (terminal no ocupa toda la pantalla)

---

### 4.4 Patrón Five by Five (Juego Completo con Screens)

```python
"""Simple version of 5x5 puzzle game."""
from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING, cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.css.query import DOMQuery
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Footer, Label, Markdown

if TYPE_CHECKING:
    from typing_extensions import Final


class Help(Screen):
    """The help screen for the application."""

    BINDINGS = [("escape,space,q,question_mark", "app.pop_screen", "Close")]

    def compose(self) -> ComposeResult:
        """Compose the game's help."""
        yield Markdown(Path(__file__).with_suffix(".md").read_text())


class WinnerMessage(Label):
    """Widget to tell the user they have won."""

    MIN_MOVES: Final = 14

    @staticmethod
    def _plural(value: int) -> str:
        return "" if value == 1 else "s"

    def show(self, moves: int) -> None:
        """Show the winner message."""
        self.update(
            "W I N N E R !\n\n\n"
            f"You solved the puzzle in {moves} move{self._plural(moves)}."
            + (
                (
                    f" It is possible to solve the puzzle in {self.MIN_MOVES}, "
                    f"you were {moves - self.MIN_MOVES} move{self._plural(moves - self.MIN_MOVES)} over."
                )
                if moves > self.MIN_MOVES
                else " Well done! That's the minimum number of moves!"
            )
        )
        self.add_class("visible")

    def hide(self) -> None:
        """Hide the winner message."""
        self.remove_class("visible")


class GameHeader(Widget):
    """Header for the game."""

    moves = reactive(0)
    filled = reactive(0)

    def compose(self) -> ComposeResult:
        """Compose the game header."""
        with Horizontal():
            yield Label(self.app.title, id="app-title")
            yield Label(id="moves")
            yield Label(id="progress")

    def watch_moves(self, moves: int):
        """Watch the moves reactive and update when it changes."""
        self.query_one("#moves", Label).update(f"Moves: {moves}")

    def watch_filled(self, filled: int):
        """Watch the on-count reactive and update when it changes."""
        self.query_one("#progress", Label).update(f"Filled: {filled}")


class GameCell(Button):
    """Individual playable cell in the game."""

    @staticmethod
    def at(row: int, col: int) -> str:
        """Get the ID of the cell at the given location."""
        return f"cell-{row}-{col}"

    def __init__(self, row: int, col: int) -> None:
        """Initialise the game cell."""
        super().__init__("", id=self.at(row, col))
        self.row = row
        self.col = col


class GameGrid(Widget):
    """The main playable grid of game cells."""

    def compose(self) -> ComposeResult:
        """Compose the game grid."""
        for row in range(Game.SIZE):
            for col in range(Game.SIZE):
                yield GameCell(row, col)


class Game(Screen):
    """Main 5x5 game grid screen."""

    SIZE: Final = 5

    BINDINGS = [
        Binding("n", "new_game", "New Game"),
        Binding("question_mark", "app.push_screen('help')", "Help", key_display="?"),
        Binding("q", "app.quit", "Quit"),
        Binding("up,w,k", "navigate(-1,0)", "Move Up", False),
        Binding("down,s,j", "navigate(1,0)", "Move Down", False),
        Binding("left,a,h", "navigate(0,-1)", "Move Left", False),
        Binding("right,d,l", "navigate(0,1)", "Move Right", False),
        Binding("space", "move", "Toggle", False),
    ]

    @property
    def filled_cells(self) -> DOMQuery[GameCell]:
        """The collection of cells that are currently turned on."""
        return cast(DOMQuery[GameCell], self.query("GameCell.filled"))

    @property
    def filled_count(self) -> int:
        """The number of cells that are currently filled."""
        return len(self.filled_cells)

    @property
    def all_filled(self) -> bool:
        """Are all the cells filled?"""
        return self.filled_count == self.SIZE * self.SIZE

    def game_playable(self, playable: bool) -> None:
        """Mark the game as playable, or not."""
        self.query_one(GameGrid).disabled = not playable

    def cell(self, row: int, col: int) -> GameCell:
        """Get the cell at a given location."""
        return self.query_one(f"#{GameCell.at(row,col)}", GameCell)

    def compose(self) -> ComposeResult:
        """Compose the game screen."""
        yield GameHeader()
        yield GameGrid()
        yield Footer()
        yield WinnerMessage()

    def toggle_cell(self, row: int, col: int) -> None:
        """Toggle an individual cell, but only if it's in bounds."""
        if 0 <= row <= (self.SIZE - 1) and 0 <= col <= (self.SIZE - 1):
            self.cell(row, col).toggle_class("filled")

    _PATTERN: Final = (-1, 1, 0, 0, 0)

    def toggle_cells(self, cell: GameCell) -> None:
        """Toggle a 5x5 pattern around the given cell."""
        for row, col in zip(self._PATTERN, reversed(self._PATTERN)):
            self.toggle_cell(cell.row + row, cell.col + col)
        self.query_one(GameHeader).filled = self.filled_count

    def make_move_on(self, cell: GameCell) -> None:
        """Make a move on the given cell."""
        self.toggle_cells(cell)
        self.query_one(GameHeader).moves += 1
        if self.all_filled:
            self.query_one(WinnerMessage).show(self.query_one(GameHeader).moves)
            self.game_playable(False)

    def on_button_pressed(self, event: GameCell.Pressed) -> None:
        """React to a press of a button on the game grid."""
        self.make_move_on(cast(GameCell, event.button))

    def action_new_game(self) -> None:
        """Start a new game."""
        self.query_one(GameHeader).moves = 0
        self.filled_cells.remove_class("filled")
        self.query_one(WinnerMessage).hide()
        middle = self.cell(self.SIZE // 2, self.SIZE // 2)
        self.toggle_cells(middle)
        self.set_focus(middle)
        self.game_playable(True)

    def action_navigate(self, row: int, col: int) -> None:
        """Navigate to a new cell by the given offsets."""
        if isinstance(self.focused, GameCell):
            self.set_focus(
                self.cell(
                    (self.focused.row + row) % self.SIZE,
                    (self.focused.col + col) % self.SIZE,
                )
            )

    def action_move(self) -> None:
        """Make a move on the current cell."""
        if isinstance(self.focused, GameCell):
            self.focused.press()

    def on_mount(self) -> None:
        """Get the game started when we first mount."""
        self.action_new_game()


class FiveByFive(App[None]):
    """Main 5x5 application class."""

    CSS_PATH = "five_by_five.tcss"
    SCREENS = {"help": Help}
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle Dark Mode")]
    TITLE = "5x5 -- A little annoying puzzle"

    def on_mount(self) -> None:
        """Set up the application on startup."""
        self.push_screen(Game())


if __name__ == "__main__":
    FiveByFive().run()
```

**Conceptos clave:**
- `Screen`: Pantallas separadas (como páginas web)
- `push_screen()`: Navegar a otra pantalla
- `pop_screen()`: Volver a pantalla anterior
- `SCREENS`: Diccionario de screens disponibles
- `Widget`: Clase base para widgets personalizados
- `toggle_class()`: Añadir/quitar clase CSS
- `disabled`: Propiedad para deshabilitar widget
- `set_focus()`: Mover foco a widget
- `self.focused`: Widget con foco actual

---

## 5. Widgets Builtin (Catálogo Completo)

### 5.1 Widgets Principales (59 total)

| Widget | Propósito | Ejemplo Uso |
|--------|-----------|-------------|
| `Button` | Botón con variantes (default, primary, success, warning, error) | Formularios, acciones |
| `Checkbox` | Checkbox individual | Opciones booleanas |
| `Collapsible` | Contenido colapsable | FAQs, detalles |
| `ContentSwitcher` | Contenedor para cambiar entre widgets | Pestañas manuales |
| `DataTable` | Tabla de datos con cursores | Dashboards, datos |
| `Digits` | Números en formato grande | Relojes, contadores |
| `DirectoryTree` | Árbol de directorios | Navegador archivos |
| `Footer` | Footer con bindings | Navegación |
| `Header` | Header con título | App header |
| `HelpPanel` | Panel de ayuda contextual | Help |
| `Input` | Campo de texto | Formularios |
| `KeyPanel` | Panel de teclas | Shortcuts |
| `Label` | Texto estático | Etiquetas |
| `Link` | Enlace clicable | URLs |
| `ListItem` | Item de lista | ListViews |
| `ListView` | Lista vertical | Menús |
| `LoadingIndicator` | Animación de carga | Loading |
| `Log` | Viewer de logs | Debugging |
| `Markdown` | Viewer de Markdown | Docs |
| `MarkdownViewer` | Markdown con TOC | Docs completas |
| `MaskedInput` | Input con máscara | Teléfonos, fechas |
| `OptionList` | Lista de opciones | Menús desplegables |
| `Placeholder` | Placeholder de diseño | Prototipado |
| `Pretty` | Pretty print Python | Debugging |
| `ProgressBar` | Barra de progreso | Tareas largas |
| `RadioButton` | Radio button | Opciones únicas |
| `RadioSet` | Conjunto de radio buttons | Formularios |
| `RichLog` | Log con formato | Logs enriquecidos |
| `Rule` | Línea horizontal | Separadores |
| `Select` | Dropdown select | Formularios |
| `SelectionList` | Lista selección múltiple | Checkboxes en lista |
| `Sparkline` | Mini gráfico de datos | Métricas |
| `Static` | Texto estático | Base para widgets |
| `Switch` | Toggle on/off | Configuración |
| `Tab` | Pestaña individual | Tabs |
| `TabbedContent` | Contenido con pestañas | Navegación |
| `TabPane` | Panel de pestaña | Tabs |
| `Tabs` | Fila de pestañas | Navegación |
| `TextArea` | Editor de texto multilínea | Código, texto largo |
| `Text

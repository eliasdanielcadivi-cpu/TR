# TEXTUAL - Índice de Ejemplos y Referencia Rápida

## Módulo: Catálogo de Ejemplos del Repositorio Oficial

---

## 1. Ejemplos Principales (/examples)

### 1.1 clock.py - Reloj Digital
**Archivo:** `/home/daniel/borrar/textual/examples/clock.py`

```python
"""App más simple posible - muestra tiempo actual"""
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
```

**Conceptos:**
- `set_interval()`: Timer asíncrono
- `query_one()`: Selector CSS
- `on_ready()`: Callback post-mount

---

### 1.2 code_browser.py - Navegador de Código
**Archivo:** `/home/daniel/borrar/textual/examples/code_browser.py`

**Features:**
- DirectoryTree widget
- Syntax highlighting
- Reactive path
- CSS dinámico (toggle files)

**Código clave:**
```python
show_tree = var(True)
path: reactive[str | None] = reactive(None)

def watch_show_tree(self, show_tree: bool) -> None:
    self.set_class(show_tree, "-show-tree")

def on_directory_tree_file_selected(
    self, event: DirectoryTree.FileSelected
) -> None:
    event.stop()
    self.path = str(event.path)
```

---

### 1.3 calculator.py - Calculadora
**Archivo:** `/home/daniel/borrar/textual/examples/calculator.py`

**Features:**
- Grid layout (4 columnas)
- Lógica de calculator real
- Mapeo teclado → botones
- Variantes de botones

**Código clave:**
```python
CSS_PATH = "calculator.tcss"

numbers = var("0")
show_ac = var(True)
left = var(Decimal("0"))
right = var(Decimal("0"))
value = var("")
operator = var("plus")

@on(Button.Pressed, ".number")
def number_pressed(self, event: Button.Pressed) -> None:
    number = event.button.id.partition("-")[-1]
    self.numbers = self.value = self.value.lstrip("0") + number
```

**TCSS Grid:**
```css
#calculator {
    layout: grid;
    grid-size: 4;
    grid-gutter: 1 2;
    grid-columns: 1fr;
    grid-rows: 2fr 1fr 1fr 1fr 1fr 1fr;
}

#number-0 {
    column-span: 2;
}
```

---

### 1.4 five_by_five.py - Juego de Puzzle
**Archivo:** `/home/daniel/borrar/textual/examples/five_by_five.py`

**Features:**
- Múltiples screens (Help, Game)
- Widget personalizado (GameCell)
- Navegación con teclado
- Estado de juego

**Código clave:**
```python
SCREENS = {"help": Help}

class Game(Screen):
    SIZE: Final = 5
    
    BINDINGS = [
        Binding("n", "new_game", "New Game"),
        Binding("question_mark", "app.push_screen('help')", "Help"),
        Binding("up,w,k", "navigate(-1,0)", "Move Up", False),
    ]
    
    @property
    def filled_cells(self) -> DOMQuery[GameCell]:
        return cast(DOMQuery[GameCell], self.query("GameCell.filled"))
```

---

## 2. Ejemplos de Widgets (/docs/examples/widgets)

### 2.1 Button
**Archivo:** `button.py`
```python
from textual.app import App, ComposeResult
from textual.widgets import Button

class ButtonApp(App):
    def compose(self) -> ComposeResult:
        yield Button("Default", variant="default")
        yield Button("Primary", variant="primary")
        yield Button("Success", variant="success")
        yield Button("Warning", variant="warning")
        yield Button("Error", variant="error")
```

**Variantes:** default, primary, success, warning, error

---

### 2.2 DataTable
**Archivo:** `data_table.py`

```python
from textual.widgets import DataTable

data_table = DataTable()
data_table.add_columns("A", "B", "C")
data_table.add_row("1", "2", "3")
data_table.add_row("4", "5", "6")
```

**Features:**
- Cursores (fila, columna, celda)
- Ordenamiento
- Fixed rows/columns
- Renderables en celdas

---

### 2.3 Sparkline
**Archivo:** `sparkline.py`

```python
from textual.widgets import Sparkline

# Datos simples
yield Sparkline(data=[1, 2, 5, 3, 7, 9, 4])

# Con colores
yield Sparkline(
    data=[10, 20, 30, 40, 50],
    color="$success"
)
```

**Uso:** Métricas, tendencias, datos en tiempo real

---

### 2.4 ProgressBar
**Archivo:** `progress_bar.py`

```python
from textual.widgets import ProgressBar

# Simple
yield ProgressBar(total=100)

# Con gradient
yield ProgressBar(
    total=100,
    gradient=True
)

# Actualizar
progress = self.query_one(ProgressBar)
progress.update(progress=50)  # 50%
```

---

### 2.5 TextArea
**Archivo:** `text_area_example.py`

```python
from textual.widgets import TextArea

# Básico
yield TextArea()

# Con lenguaje
yield TextArea.language("python")

# Con tema
yield TextArea.theme("monokai")

# Leer contenido
text_area = self.query_one(TextArea)
content = text_area.text
```

**Languages:** python, javascript, rust, go, java, etc.  
**Themes:** monokai, github-dark, dracula, etc.

---

### 2.6 Tree
**Archivo:** `tree.py`

```python
from textual.widgets import Tree

# Árbol simple
tree = Tree("Root")
tree.root.add("Child 1")
tree.root.add("Child 2")

# Con nodos
child = tree.root.add("Parent")
child.add("Grandchild 1")
child.add("Grandchild 2")
```

---

### 2.7 TabbedContent
**Archivo:** `tabbed_content.py`

```python
from textual.widgets import TabbedContent, TabPane

with TabbedContent(initial="tab1"):
    with TabPane("Tab 1", id="tab1"):
        yield Static("Content 1")
    with TabPane("Tab 2", id="tab2"):
        yield Static("Content 2")
```

---

### 2.8 Select
**Archivo:** `select_widget.py`

```python
from textual.widgets import Select

# Opciones simples
yield Select([("Option 1", 1), ("Option 2", 2)])

# Con valor por defecto
yield Select(
    [("A", 1), ("B", 2)],
    value=1
)
```

---

### 2.9 Input
**Archivo:** `input.py`

```python
from textual.widgets import Input

# Texto simple
yield Input(placeholder="Enter text")

# Password
yield Input(password=True)

# Tipos
yield Input(type="integer")
yield Input(type="number")
yield Input(type="email")

# Validación
yield Input(validators=[MyValidator()])
```

---

### 2.10 Markdown
**Archivo:** `markdown.py`

```python
from textual.widgets import Markdown

# Desde string
yield Markdown("# Hello\nWorld")

# Desde archivo
yield Markdown.from_path("README.md")
```

---

## 3. TCSS - Referencia de Estilos

### 3.1 Selectores

```css
/* Por ID */
#my-widget {
    background: $primary;
}

/* Por clase */
.my-class {
    color: $text;
}

/* Por tipo */
Button {
    margin: 1 0;
}

/* Descendiente */
Container Button {
    width: 100%;
}

/* Pseudo-clases */
Button:hover {
    background: $secondary;
}

Input:focus {
    border: solid $success;
}

/* Estado */
Widget:disabled {
    opacity: 0.5;
}

Widget:focus {
    border: solid $accent;
}
```

---

### 3.2 Propiedades Comunes

```css
/* Layout */
Widget {
    layout: horizontal;  /* horizontal, vertical, grid */
    width: 100%;         /* %, fr, auto, número */
    height: 1fr;         /* fr = fraction */
    margin: 1;           /* top right bottom left */
    padding: 1 2;        /* vertical horizontal */
}

/* Grid */
Widget {
    grid-size: 4;              /* 4 columnas */
    grid-gutter: 1 2;          /* espacio entre celdas */
    grid-columns: 1fr 2fr;     /* tamaño columnas */
    grid-rows: auto;           /* tamaño filas */
    column-span: 2;            /* ocupa 2 columnas */
}

/* Docking */
Widget {
    dock: top;      /* top, right, bottom, left */
    dock: left;
}

/* Overflow */
Widget {
    overflow: hidden;    /* hidden, auto, scroll */
    overflow-x: scroll;
    overflow-y: auto;
}

/* Bordes */
Widget {
    border: solid $primary;
    border: round $success;
    border: double $warning;
    border-radius: 1;
}

/* Background */
Widget {
    background: $surface;
    background: $primary;
    background: red;
    background: #ff0000;
}

/* Color */
Widget {
    color: $text;
    color: $text-muted;
    color: white;
}

/* Alineación */
Widget {
    text-align: left;    /* left, center, right */
    content-align: center middle;  /* horizontal vertical */
    align: right;        /* para widgets en container */
}

/* Display */
Widget {
    display: block;      /* visible */
    display: none;       /* oculto */
}

/* Estilo de texto */
Widget {
    text-style: bold;
    text-style: italic;
    text-style: underline;
    text-style: overline;
    text-style: strike;
}
```

---

### 3.3 Variables de Color

```css
/* Colores semánticos */
$primary       /* Color primario (azul) */
$secondary     /* Color secundario (verde) */
$success       /* Éxito (verde) */
$warning       /* Advertencia (amarillo) */
$error         /* Error (rojo) */

/* Colores de superficie */
$surface       /* Fondo de widgets */
$panel         /* Fondo de paneles */
$background    /* Fondo de pantalla */

/* Colores de texto */
$text          /* Texto normal */
$text-muted    /* Texto atenuado */
$text-inverse  /* Texto inverso */

/* Colores de acento */
$accent        /* Color de acento */
$foreground    /* Color de primer plano */
```

---

## 4. Bindings - Atajos de Teclado

### 4.1 Teclas Especiales

```python
BINDINGS = [
    ("ctrl+q", "quit", "Quit"),
    ("ctrl+s", "save", "Save"),
    ("ctrl+p", "command_palette", "Commands"),
    ("f1", "help", "Help"),
    ("escape", "escape", "Escape"),
    ("tab", "focus_next", "Next"),
    ("shift+tab", "focus_previous", "Previous"),
    ("up,w,k", "navigate_up", "Up"),
    ("down,s,j", "navigate_down", "Down"),
    ("left,a,h", "navigate_left", "Left"),
    ("right,d,l", "navigate_right", "Right"),
]
```

### 4.2 Combinaciones Múltiples

```python
BINDINGS = [
    ("escape,space,q,question_mark", "app.pop_screen", "Close"),
    # Múltiples teclas para misma acción
]
```

---

## 5. Eventos - Referencia

### 5.1 Eventos de Input

```python
def on_key(self, event: events.Key) -> None:
    """Tecla presionada"""
    if event.key == "q":
        self.app.quit()

def on_click(self, event: events.Click) -> None:
    """Click de mouse"""
    pass

def on_focus(self, event: events.Focus) -> None:
    """Widget recibe foco"""
    self.add_class("focused")

def on_blur(self, event: events.Blur) -> None:
    """Widget pierde foco"""
    self.remove_class("focused")
```

---

### 5.2 Eventos de Widget

```python
@on(Button.Pressed)
def on_button_pressed(self, event: Button.Pressed) -> None:
    """Botón presionado"""
    pass

@on(Input.Changed)
def on_input_changed(self, event: Input.Changed) -> None:
    """Input cambió"""
    pass

@on(Input.Submitted)
def on_input_submitted(self, event: Input.Submitted) -> None:
    """Enter en input"""
    pass

@on(Select.Changed)
def on_select_changed(self, event: Select.Changed) -> None:
    """Selección cambió"""
    pass
```

---

### 5.3 Eventos de Screen

```python
def on_mount(self) -> None:
    """Widget montado en DOM"""
    pass

def on_unmount(self) -> None:
    """Widget desmontado"""
    pass

def on_resize(self, event: events.Resize) -> None:
    """Pantalla redimensionada"""
    pass

def on_ready(self) -> None:
    """App lista (después de mount)"""
    pass
```

---

## 6. Decoradores @on

### 6.1 Selector por ID

```python
@on(Button.Pressed, "#my-button")
def on_my_button(self, event: Button.Pressed) -> None:
    """Solo para botón con id='my-button'"""
    pass
```

### 6.2 Selector por Clase

```python
@on(Button.Pressed, ".number")
def on_number_button(self, event: Button.Pressed) -> None:
    """Solo para botones con class='number'"""
    pass
```

### 6.3 Múltiples Selectores

```python
@on(Button.Pressed, "#plus,#minus,#divide,#multiply")
def on_operator(self, event: Button.Pressed) -> None:
    """Cualquiera de los operadores"""
    pass
```

---

## 7. Utilidades

### 7.1 notify()

```python
self.notify("Message saved!", severity="information")
self.notify("Error occurred", severity="error")
self.notify("Warning", severity="warning")
```

### 7.2 set_interval()

```python
# Ejecutar cada 1 segundo
self.set_interval(1, self.update_clock)

# Ejecutar 5 veces
self.set_interval(1, self.countdown, repeat=5)
```

### 7.3 call_later()

```python
# Ejecutar después de 2 segundos
self.call_later(2, self.my_function)
```

### 7.4 query_one()

```python
# Por ID
widget = self.query_one("#my-widget", Widget)

# Por clase
buttons = self.query_all(".number", Button)

# Por tipo
labels = self.query(Label)
```

---

## 8. Comandos de Desarrollo

### 8.1 Instalar

```bash
pip install textual textual-dev
```

### 8.2 Dev Console

```bash
# Conectar dev console
textual console

# Correr app con dev tools
textual run --dev my_app.py

# Hot-reload para TCSS
textual run my_app.py  # Auto detecta cambios en .tcss
```

### 8.3 Demo

```bash
# Ver demo builtin
python -m textual

# Ver widgets
python -m textual.widgets
```

---

## 9. Recursos del Repositorio

### 9.1 Rutas Clave

| Ruta | Contenido |
|------|-----------|
| `/home/daniel/borrar/textual/src/textual/widgets/` | 59 widgets builtin |
| `/home/daniel/borrar/textual/examples/` | 24 ejemplos completos |
| `/home/daniel/borrar/textual/docs/examples/` | 89 ejemplos de docs |
| `/home/daniel/borrar/textual/docs/widgets/` | Referencia de widgets |
| `/home/daniel/borrar/textual/docs/guide/` | Guías oficiales |

### 9.2 Widgets Disponibles (59 total)

**Básicos:**
- Static, Label, Button, Input, Checkbox, Switch

**Contenedores:**
- Container, Horizontal, Vertical, Grid, ContentSwitcher

**Listas:**
- ListView, ListItem, OptionList, SelectionList

**Tablas/Árboles:**
- DataTable, Tree, DirectoryTree

**Texto:**
- TextArea, Markdown, MarkdownViewer, RichLog, Log

**Navegación:**
- Tabs, TabbedContent, Tab, TabPane, Footer, Header

**Datos:**
- ProgressBar, Sparkline, Digits, LoadingIndicator

**Selectores:**
- Select, RadioButton, RadioSet

**Utilidades:**
- Placeholder, Rule, Collapsible, Tooltip, Toast

**Especiales:**
- HelpPanel, KeyPanel, Link, Welcome

---

*Documento creado: 15-03-2026*  
*Estado: [OK] - Índice de ejemplos completo*

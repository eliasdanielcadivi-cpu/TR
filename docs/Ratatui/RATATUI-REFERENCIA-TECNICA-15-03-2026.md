# Ratatui - Referencia Técnica

## Módulo: Arquitectura y Widgets (Rust)

---

## 1. Problema Detectado

**Síntoma:** Ratatui es framework Rust maduro para TUI pero requiere binario separado si se usa con ARES (Python).

**Necesidad:** Documentar arquitectura y widgets de Ratatui para:
- Entender patrones de diseño aplicables
- Extraer código de ejemplos para referencia
- Comparar con alternativas Python (textual, rich)
- Decidir stack tecnológico para AgenteDeCambio CLI

---

## 2. Causa Raíz

**Ratatui (Rust):**
- Nació de `tui-rs` (floriandehau) en 2023
- Arquitectura modular (workspace con crates separados)
- Backend múltiple (crossterm, termion, termwiz)
- 18+ widgets en `ratatui-widgets/examples/`
- 32+ aplicaciones ejemplo en `examples/apps/`

**Para CLI Python:**
- Requiere FFI o binario separado
- Overhead de comunicación JSON
- Curva de aprendizaje Rust

---

## 3. API Disponible (Arquitectura Modular)

### 3.1 Organización de Crates (v0.30.0+)

```
ratatui (workspace)
├── ratatui              # Main crate (re-exports todo)
├── ratatui-core         # Tipos y traits fundamentales
├── ratatui-widgets      # Implementación de widgets
├── ratatui-crossterm    # Backend cross-platform
├── ratatui-termion      # Backend Unix
├── ratatui-termwiz      # Backend avanzado
└── ratatui-macros       # Macros utilitarios
```

**Dependencias:**
```text
ratatui
├── ratatui-core
├── ratatui-widgets → ratatui-core
├── ratatui-crossterm → ratatui-core
├── ratatui-termion → ratatui-core
└── ratatui-termwiz → ratatui-core
```

### 3.2 Main Crate (ratatui)

**Uso típico:**
```rust
use ratatui::{
    widgets::{Block, Paragraph, List, Table, Gauge, Tabs},
    layout::{Layout, Constraint, Rect},
    style::{Color, Style, Modifier, Stylize},
    text::{Text, Line, Span},
    Frame, Terminal,
};
```

**Re-exports:**
- Todo de `ratatui-core` (traits, tipos base)
- Todo de `ratatui-widgets` (widgets concretos)
- Todo de backends (crossterm, termion, termwiz)
- Features experimentales (`WidgetRef`, `StatefulWidgetRef`)

### 3.3 Core Traits (ratatui-core)

**Widget Trait:**
```rust
pub trait Widget {
    fn render(self, area: Rect, buf: &mut Buffer);
}

// Uso
impl Widget for &str {
    fn render(self, area: Rect, buf: &mut Buffer) {
        // Renderiza string en buffer
    }
}
```

**StatefulWidget Trait:**
```rust
pub trait StatefulWidget {
    type State;
    fn render(self, area: Rect, buf: &mut Buffer, state: &mut Self::State);
}

// Uso para widgets con estado (Table, List)
let mut table_state = TableState::default();
table_state.select(Some(0));  // Selecciona primera fila

frame.render_stateful_widget(table, area, &mut table_state);
```

---

## 4. Solución Implementada (Widgets Principales)

### 4.1 Block (Contenedor con Borde)

```rust
use ratatui::widgets::Block;
use ratatui::style::{Color, Style};

let block = Block::bordered()
    .title("Mi Widget")
    .title_style(Style::new().bold().magenta())
    .border_style(Style::new().blue())
    .style(Style::new().on_black());

frame.render_widget(block, area);
```

**Tipos de Borde:**
```rust
use ratatui::symbols::border;

// Bordes predefinidos
Block::default()
    .borders(Borders::ALL)
    .border_type(BorderType::Rounded)  // o Plain, Double, Thick, QuadrantInside

// Bordes personalizados
Block::default().border_set(border::THICK);
```

---

### 4.2 Paragraph (Texto con Estilo)

```rust
use ratatui::widgets::Paragraph;
use ratatui::layout::Alignment;
use ratatui::text::{Text, Line, Span};

// Texto simple
let paragraph = Paragraph::new("Hello World!")
    .alignment(Alignment::Center)
    .block(Block::bordered().title("Info"));

// Texto con estilo (Spans)
let text = Text::from(Line::from(vec![
    Span::raw("Hello "),
    Span::styled("World", Style::new().bold().red()),
    Span::raw("!"),
]));

let paragraph = Paragraph::new(text)
    .wrap(ratatui::widgets::Wrap { trim: true });

frame.render_widget(paragraph, area);
```

**Para Chat (Burbujas):**
```rust
fn render_chat_message(frame: &mut Frame, area: Rect, message: &ChatMessage) {
    let text = match message.role {
        "user" => Line::from(Span::styled(
            format!("User: {}", message.content),
            Style::new().blue().bold()
        )),
        "assistant" => Line::from(Span::styled(
            format!("Bot: {}", message.content),
            Style::new().green()
        )),
        _ => Line::from(message.content.as_str()),
    };
    
    let paragraph = Paragraph::new(text)
        .block(Block::bordered().title(&message.role));
    
    frame.render_widget(paragraph, area);
}
```

---

### 4.3 Gauge (Barra de Progreso)

```rust
use ratatui::widgets::{Gauge, LineGauge};
use ratatui::style::{Style, Modifier};

// Gauge tradicional
let gauge = Gauge::default()
    .gauge_style(Style::new().blue().on_black())
    .label(Span::styled("Progress", Style::new().bold()))
    .percent(80);

frame.render_widget(gauge, area);

// LineGauge (compacto, tipo línea)
use ratatui::symbols::line;

let line_gauge = LineGauge::default()
    .filled_style(Style::new().white().on_red().bold())
    .unfilled_style(Style::new().gray().on_black())
    .label("❤️ HP")
    .ratio(0.42)
    .filled_symbol(line::THICK_HORIZONTAL)
    .unfilled_symbol(line::THICK_HORIZONTAL);

frame.render_widget(line_gauge, area);
```

**Para Delta Metrics:**
```rust
fn render_delta_gauge(frame: &mut Frame, area: Rect, delta: f64, threshold: f64) {
    let gauge_style = if delta > threshold {
        Style::new().red().on_black()  // Alerta
    } else {
        Style::new().green().on_black()  // OK
    };
    
    let label = format!("Deriva: {:.1}%/{:.1}%", delta * 100.0, threshold * 100.0);
    
    let gauge = Gauge::default()
        .gauge_style(gauge_style)
        .label(label)
        .ratio(delta);
    
    frame.render_widget(gauge, area);
}
```

---

### 4.4 Table (Tabla con Navegación)

```rust
use ratatui::widgets::{Table, Row, TableState};
use ratatui::layout::Constraint;

// Estado de la tabla (selección, scroll)
let mut table_state = TableState::default();
table_state.select(Some(0));  // Selecciona primera fila
table_state.select_first_column();

// Header
let header = Row::new(["Nombre", "Valor", "Descripción"])
    .style(Style::new().bold().white())
    .bottom_margin(1);

// Rows
let rows = vec![
    Row::new(["Delta", "0.25", "Score de deriva actual"]),
    Row::new(["Threshold", "0.30", "Umbral de aprobación"]),
    Row::new(["Mode", "chat", "Modo de interacción"]),
];

// Construir tabla
let table = Table::new(rows, [
        Constraint::Percentage(30),
        Constraint::Percentage(20),
        Constraint::Percentage(50),
    ])
    .header(header)
    .column_spacing(2)
    .row_highlight_style(Style::new().on_black().bold())
    .highlight_symbol("🍴 ")
    .column_highlight_style(Style::new().gray())
    .cell_highlight_style(Style::new().reversed().yellow());

// Render con estado
frame.render_stateful_widget(table, area, &mut table_state);
```

**Manejo de Eventos:**
```rust
match key.code {
    KeyCode::Char('j') | KeyCode::Down => table_state.select_next(),
    KeyCode::Char('k') | KeyCode::Up => table_state.select_previous(),
    KeyCode::Char('l') | KeyCode::Right => table_state.select_next_column(),
    KeyCode::Char('h') | KeyCode::Left => table_state.select_previous_column(),
    KeyCode::Char('g') => table_state.select_first(),
    KeyCode::Char('G') => table_state.select_last(),
    _ => {}
}
```

---

### 4.5 Tabs (Pestañas)

```rust
use ratatui::widgets::Tabs;
use ratatui::style::{Color, Style};
use ratatui::symbols;

let tabs = Tabs::new(vec!["Chat", "Cuestionario", "Config"])
    .style(Color::White)
    .highlight_style(Style::default().magenta().on_black().bold())
    .select(selected_tab)  // Índice de pestaña activa
    .divider(symbols::DOT)
    .padding(" ", " ");

frame.render_widget(tabs, area);
```

**Cambio de Pestañas:**
```rust
let mut selected_tab = 0;

match key.code {
    KeyCode::Char('l') | KeyCode::Right => {
        selected_tab = (selected_tab + 1) % 3;  // Ciclar
    }
    KeyCode::Char('h') | KeyCode::Left => {
        selected_tab = (selected_tab + 2) % 3;  // Ciclar inverso
    }
    _ => {}
}
```

**Contenido por Pestaña:**
```rust
fn render_content(frame: &mut Frame, area: Rect, selected_tab: usize) {
    let text = match selected_tab {
        0 => "Vista de Chat",
        1 => "Vista de Cuestionario",
        2 => "Configuración",
        _ => unreachable!(),
    };
    
    let paragraph = Paragraph::new(text)
        .alignment(Alignment::Center)
        .block(Block::bordered().title("Contenido"));
    
    frame.render_widget(paragraph, area);
}
```

---

### 4.6 List (Lista con Items)

```rust
use ratatui::widgets::{List, ListItem, ListState};

// Estado
let mut list_state = ListState::default();
list_state.select(Some(0));

// Items
let items = vec![
    ListItem::new("Opción 1"),
    ListItem::new("Opción 2"),
    ListItem::new("Opción 3"),
];

// Lista
let list = List::new(items)
    .block(Block::bordered().title("Opciones"))
    .highlight_style(Style::new().on_black().bold())
    .highlight_symbol("▶ ");

frame.render_stateful_widget(list, area, &mut list_state);
```

---

### 4.7 Canvas (Dibujo Personalizado)

```rust
use ratatui::widgets::canvas::{Canvas, Rectangle, Circle};
use ratatui::style::Color;

let canvas = Canvas::default()
    .block(Block::bordered().title("Canvas"))
    .background_color(Color::Black)
    .x_bounds([0.0, 100.0])
    .y_bounds([0.0, 100.0])
    .layer(Rectangle {
        x: 10.0,
        y: 10.0,
        width: 20.0,
        height: 10.0,
        color: Color::Red,
    })
    .layer(Circle {
        x: 50.0,
        y: 50.0,
        radius: 15.0,
        color: Color::Blue,
    });

frame.render_widget(canvas, area);
```

---

### 4.8 Chart (Gráficos)

```rust
use ratatui::widgets::{Chart, Dataset, GraphType};
use ratatui::style::Color;

let datasets = vec![
    Dataset::default()
        .name("Datos")
        .marker(ratatui::symbols::Marker::Dot)
        .graph_type(GraphType::Line)
        .style(Color::Yellow)
        .data(&[
            (0.0, 0.0),
            (10.0, 20.0),
            (20.0, 50.0),
            (30.0, 80.0),
        ]),
];

let chart = Chart::new(datasets)
    .block(Block::bordered().title("Gráfico"))
    .x_axis(
        Axis::default()
            .title("Tiempo")
            .style(Color::White)
            .bounds([0.0, 30.0])
    )
    .y_axis(
        Axis::default()
            .title("Valor")
            .style(Color::White)
            .bounds([0.0, 100.0])
    );

frame.render_widget(chart, area);
```

---

## 5. Flujo de Trabajo (Patrón Principal)

### 5.1 Estructura Básica

```rust
use ratatui::{DefaultTerminal, Frame};
use crossterm::event::{self, KeyCode};
use color_eyre::Result;

fn main() -> Result<()> {
    color_eyre::install()?;  // Error handling
    ratatui::run(run)
}

fn run(terminal: &mut DefaultTerminal) -> Result<()> {
    loop {
        terminal.draw(render)?;  // Callback de renderizado
        
        // Manejo de eventos
        if should_quit()? {
            break Ok(());
        }
    }
}

fn render(frame: &mut Frame) {
    let area = frame.area();
    
    // Layout
    let layout = Layout::vertical([
        Constraint::Length(1),   // Header
        Constraint::Fill(1),     // Content
        Constraint::Length(3),   // Footer
    ]);
    let [header, content, footer] = area.layout(&layout);
    
    // Render widgets
    render_header(frame, header);
    render_content(frame, content);
    render_footer(frame, footer);
}

fn should_quit() -> Result<bool> {
    if event::poll(Duration::from_millis(250))? {
        if let Event::Key(key) = event::read()? {
            return Ok(key.code == KeyCode::Char('q'));
        }
    }
    Ok(false)
}
```

### 5.2 Layout System

```rust
use ratatui::layout::{Layout, Constraint, Direction, Rect};

// Layout vertical
let vertical = Layout::vertical([
    Constraint::Length(1),    // 1 línea fija
    Constraint::Fill(1),      // Todo el espacio restante
    Constraint::Percentage(20), // 20% del área
]);

// Layout horizontal
let horizontal = Layout::horizontal([
    Constraint::Percentage(30),  // 30% ancho
    Constraint::Percentage(70),  // 70% ancho
]);

// Espaciado entre elementos
let layout = Layout::vertical(constraints).spacing(1);  // 1 espacio entre cada

// División de área
let areas = area.layout(&layout);
let [header, content, footer] = areas[..] else { unreachable!() };

// Offset (para superposición)
let offset_area = area + Offset::new(1, 1);  // Mueve 1 abajo, 1 derecha
```

---

## 6. Qué Deberías Ver (Ejemplos Visuales)

### Hello World

```
┌─────────────────────────────────────────┐
│                                         │
│         Hello World!                    │
│         (press 'q' to quit)             │
│                                         │
└─────────────────────────────────────────┘
```

### Gauge Widget

```
┌─────────────────────────────────────────┐
│ Gauge Widget (Press 'q' to quit)        │
├─────────────────────────────────────────┤
│                                         │
│ Year Progress [████████████████░░░░] 80%│
│                                         │
│ ❤️ HP [██████████░░░░░░░░░░░░] 0.42    │
│                                         │
└─────────────────────────────────────────┘
```

### Table Widget

```
┌─────────────────────────────────────────────────────┐
│ Table Widget (arrows to navigate, 'q' to quit)     │
├─────────────────────────────────────────────────────┤
│ Ingredient     │ Quantity    │ Macros               │
├─────────────────────────────────────────────────────┤
│ 🍴 Eggplant    │ 1 medium    │ 25 kcal, 6g carbs    │
│   Tomato       │ 2 large     │ 44 kcal, 10g carbs   │
│   Zucchini     │ 1 medium    │ 33 kcal, 7g carbs    │
│   Bell Pepper  │ 1 medium    │ 24 kcal, 6g carbs    │
└─────────────────────────────────────────────────────┘
```

### Tabs Widget

```
┌─────────────────────────────────────────┐
│ Tabs Widget (arrows to switch tabs)    │
├─────────────────────────────────────────┤
│        Tab1 · Tab2 · Tab3               │
├─────────────────────────────────────────┤
│                                         │
│   Great terminal interfaces start       │
│   with a single widget.                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 7. Patrones Extraídos (Código de Ejemplos)

### 7.1 Patrón App Completa

```rust
//! Hello World Ratatui App

use std::time::Duration;
use color_eyre::Result;
use crossterm::event::{self, Event, KeyCode};
use ratatui::widgets::Paragraph;
use ratatui::{DefaultTerminal, Frame};

fn main() -> Result<()> {
    color_eyre::install()?;
    ratatui::run(run)
}

fn run(terminal: &mut DefaultTerminal) -> Result<()> {
    loop {
        terminal.draw(render)?;
        if should_quit()? {
            break Ok(());
        }
    }
}

fn render(frame: &mut Frame) {
    let greeting = Paragraph::new("Hello World! (press 'q' to quit)");
    frame.render_widget(greeting, frame.area());
}

fn should_quit() -> Result<bool> {
    if event::poll(Duration::from_millis(250))? {
        if let Event::Key(key) = event::read()? {
            return Ok(key.code == KeyCode::Char('q'));
        }
    }
    Ok(false)
}
```

### 7.2 Patrón Widget con Estado

```rust
use ratatui::widgets::{Table, TableState};

// En main loop
let mut table_state = TableState::default();
table_state.select(Some(0));

// En render
fn render(frame: &mut Frame, area: Rect, state: &mut TableState) {
    let table = Table::new(rows, widths)
        .row_highlight_style(Style::new().on_black().bold())
        .highlight_symbol("🍴 ");
    
    frame.render_stateful_widget(table, area, state);
}

// En event loop
match key.code {
    KeyCode::Down => table_state.select_next(),
    KeyCode::Up => table_state.select_previous(),
    _ => {}
}
```

### 7.3 Patrón Múltiples Vistas

```rust
enum View {
    Chat,
    Questionnaire,
    Settings,
}

struct App {
    current_view: View,
    chat_state: ChatState,
    questionnaire_state: QuestionnaireState,
}

fn render(frame: &mut Frame) {
    match app.current_view {
        View::Chat => render_chat(frame, &mut app.chat_state),
        View::Questionnaire => render_questionnaire(frame, &mut app.questionnaire_state),
        View::Settings => render_settings(frame),
    }
}

fn handle_key(app: &mut App, key: KeyCode) {
    match app.current_view {
        View::Chat => handle_chat_key(&mut app.chat_state, key),
        View::Questionnaire => handle_questionnaire_key(&mut app.questionnaire_state, key),
        _ => {}
    }
}
```

---

## 8. Checklist Debug

| Problema | Síntoma | Solución |
|----------|---------|----------|
| Widgets no se renderizan | Pantalla vacía | Verificar `frame.render_widget()` se llama |
| Estado no persiste | Selección se resetea | Usar `render_stateful_widget()` con `&mut state` |
| Layout roto | Widgets superpuestos | Verificar `Constraint` suma ≤ 100% o usar `Fill` |
| Eventos no capturados | Teclas no responden | `event::poll()` con timeout adecuado (250ms) |
| Terminal no restaura | Pantalla queda rota | Usar `ratatui::run()` o `ratatui::restore()` en drop |

---

## 9. Referencias

### Archivos en Repositorio Local

| Ruta | Contenido |
|------|-----------|
| `/home/daniel/borrar/ratatui/ARCHITECTURE.md` | Arquitectura modular (crates) |
| `/home/daniel/borrar/ratatui/ratatui-widgets/examples/` | 18 ejemplos de widgets |
| `/home/daniel/borrar/ratatui/examples/apps/` | 32 aplicaciones completas |

### Recursos Externos

| Recurso | URL |
|---------|-----|
| GitHub Repo | https://github.com/ratatui/ratatui |
| Docs.rs | https://docs.rs/ratatui |
| Widget Examples | https://github.com/ratatui/ratatui/tree/main/ratatui-widgets/examples |
| App Examples | https://github.com/ratatui/ratatui/tree/main/examples/apps |

---

## 10. Conclusión (Decisión Tecnológica)

**Ratatui es excelente para:**
- ✅ Aplicaciones TUI complejas en Rust
- ✅ Máximo rendimiento
- ✅ Backend múltiple (crossterm, termion, termwiz)

**Pero para AgenteDeCambio CLI:**
- ❌ Requiere binario separado (Python ↔ Rust IPC)
- ❌ Overhead de comunicación JSON
- ❌ Curva de aprendizaje Rust

**Recomendación:** **Textual (Python)**
- ✅ Integración nativa con ARES
- ✅ Mismo lenguaje que módulos core
- ✅ Widgets interactivos suficientes
- ✅ Menor complejidad

**Ver:** `RATATUI-ALTERNATIVAS-PYTHON-TUI-15-03-2026.md` para comparativa completa.

---

*Documento creado: 15-03-2026*  
*Última actualización: 15-03-2026*  
*Estado: [OK] - Referencia técnica completada*

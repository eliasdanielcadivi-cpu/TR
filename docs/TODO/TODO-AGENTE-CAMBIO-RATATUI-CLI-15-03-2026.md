# TODO-AGENTE-CAMBIO-RATATUI-CLI-15-03-2026

## Meta-Objetivo
Transformar "Agente de Cambio STABLE" (actualmente Next.js + Socket.IO + DeepSeek) en una aplicación CLI con interfaz Ratatui, integrada como sub-agente dentro del ecosistema ARES-TRON, con modularidad reutilizable y comunicación JSON.

---

## Análisis de Intención (Causa-Efecto)

### Causa Raíz
- Existe "Agente de Cambio STABLE" con funcionalidades valiosas (prompt vivo, métricas de deriva, modo dual chat/cuestionario)
- Actualmente es aplicación web (Next.js) → no reutilizable desde terminal
- TRON/ARES necesita estas capacidades como herramienta CLI nativa

### Efecto Deseado
1. **AgenteDeCambio CLI** con interfaz Ratatui (dashboards, diálogos, informes)
2. **Módulos reutilizables** en `/modules/` (filosofía TRON: ≤3 funciones/módulo)
3. **Sistema widget-based** con comunicación JSON (widgets responden JSON, dashboard interactúa JSON)
4. **Integración total con ARES** (RAG, modelos Ollama/DeepSeek, sesiones Kitty)

### Dependencias Lógicas
```
FASE 1: Documentar Agente de Cambio (QUÉ hace)
    ↓
FASE 2: Documentar Ratatui (CÓMO hacerlo)
    ↓
FASE 3: Implementar AgenteDeCambio CLI (integración)
```

### Riesgos Identificados
| Riesgo | Mitigación |
|--------|------------|
| Ratatui es Rust (¿bindings Python?) | Evaluar: textual, rich, urwid como alternativas Python |
| Complejidad widgets interactivos JSON | Diseñar protocolo JSON simple: `{tipo, datos, accion}` |
| Mantener modularidad atómica en UI | Cada widget = módulo independiente en `modules/ui/widgets/` |
| Streaming en tiempo real | Usar sockets Unix (como ARES) o polling asíncrono |

---

## FASE 1: Documentación Agente de Cambio STABLE

### Objetivo
Crear referencia técnica concisa en `docs/` que capture arquitectura, módulos y flujos de Agente de Cambio para posterior traducción a CLI.

### Tareas
- [ ] **1.1** Leer estructura completa de `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/`
  - Analizar `modules/` (deepseek-connector, delta-calculator, prompt-engine, session-manager, etc.)
  - Analizar `apps/server/` (Socket.IO handlers, servicios)
  - Analizar `apps/web/` (componentes React, Zustand store)
  
- [ ] **1.2** Crear documento de arquitectura en `docs/AgenteDeCambio/ARQUITECTURA-AGENTE-CAMBIO-15-03-2026.md`
  - Extracto de módulos clave (máximo 3 funciones por módulo)
  - Diagrama de flujo: usuario → prompt → DeepSeek → respuesta → métricas
  - Protocolo de comunicación: eventos Socket.IO (message:stream, prompt:mutation, delta:update)
  
- [ ] **1.3** Crear documento de módulos reutilizables en `docs/AgenteDeCambio/MODULOS-REUTILIZABLES-15-03-2026.md`
  - deepseek-connector: conexión API, streaming, caché de contexto
  - delta-calculator: métricas de deriva (score 0-1, umbral 0.3)
  - prompt-engine: system prompt editable, negociación de cambios
  - session-manager: persistencia de objetivos, memoria de sesión
  - state-manager: estado global (modo chat/cuestionario)
  
- [ ] **1.4** Crear documento de flujos de interacción en `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md`
  - Modo chat: flujo conversacional fluido
  - Modo cuestionario: preguntas estructuradas con opciones (radio, check, yesno)
  - Transiciones entre modos
  - Manejo de streaming carácter por carácter

### Criterios de Aceptación
- [ ] Documentos en `docs/AgenteDeCambio/` (carpeta nueva)
- [ ] Cada documento sigue protocolo de cuaderno de apuntes IA (conciso, granular, táctico)
- [ ] Extracto de código clave (snippets Python/Node) para referencia futura
- [ ] Diagramas ASCII o descripciones de flujo claras

---

## FASE 2: Documentación Ratatui (y alternativas Python)

### Objetivo
Crear referencia técnica de Ratatui (Rust) y evaluar alternativas Python para implementación CLI.

### Tareas
- [ ] **2.1** Analizar repositorio `/home/daniel/borrar/ratatui/`
  - Leer `ARCHITECTURE.md` (modularidad: ratatui-core, ratatui-widgets, backends)
  - Explorar `ratatui-widgets/examples/` (widgets disponibles: Block, Paragraph, List, Chart, Gauge, Table, Tabs, etc.)
  - Explorar `examples/apps/` (aplicaciones completas de referencia)
  
- [ ] **2.2** Crear documento `docs/Ratatui/RATATUI-REFERENCIA-15-03-2026.md`
  - Arquitectura modular (crate organization)
  - Widgets disponibles con ejemplos de código Rust
  - Backends: crossterm (cross-platform), termion (Unix), termwiz (avanzado)
  - Patrón de renderizado: `terminal.draw(render)?`
  - Gestión de eventos: `event::read()` con Key, Mouse, Resize
  
- [ ] **2.3** Evaluar alternativas Python para TUI
  - **textual**: TUI moderno con React-like components (Python 3.7+)
    - Widgets: Button, Input, DataTable, ProgressBar, Tabs
    - CSS-like styling, reactive state
    - Asíncrono nativo (asyncio)
  - **rich**: Console output con styling, progress bars, tables
    - Menos interactivo, más para output estático
  - **urwid**: TUI clásico (usado en installer de Ubuntu)
    - Widgets: ListBox, Edit, Button, ProgressBar
    - Más bajo nivel, más verboso
  - **blessed**: Wrapper de curses con API amigable
    - Bueno para forms simples, no dashboards complejos
  
- [ ] **2.4** Crear documento `docs/Ratatui/ALTERNATIVAS-PYTHON-TUI-15-03-2026.md`
  - Comparativa: textual vs rich vs urwid vs blessed
  - Recomendación basada en:
    - Complejidad de Agente de Cambio (dashboards + forms + streaming)
    - Integración con ARES (Python ya establecido)
    - Curva de aprendizaje
    - Rendimiento en terminales limitados
  
- [ ] **2.5** Decidir stack tecnológico
  - Opción A: Ratatui (Rust) → binario separado, comunicación JSON vía stdin/stdout
  - Opción B: textual (Python) → integración nativa con ARES, mismo venv
  - Opción C: rich + curses híbrido → más control, más complejidad

### Criterios de Aceptación
- [ ] Documentos en `docs/Ratatui/` (carpeta nueva)
- [ ] Tabla comparativa de alternativas Python
- [ ] Decisión justificada de stack tecnológico
- [ ] Snippets de ejemplo para widgets clave (chat, gauge, table, tabs)

---

## FASE 3: Implementación AgenteDeCambio CLI

### Objetivo
Crear sub-agente en `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/AgenteDeCambio/` con modularidad controlada y documentación completa.

### Tareas
- [ ] **3.1** Crear estructura de carpetas siguiendo metodología ARES
  ```
  AGENTES/sub-agentes/AgenteDeCambio/
  ├── src/
  │   └── main.py              # Orquestador (despachador puro)
  ├── modules/
  │   ├── ui/                  # Widgets TUI
  │   │   ├── widgets/         # Cada widget = módulo atómico
  │   │   │   ├── chat_widget.py
  │   │   │   ├── gauge_widget.py
  │   │   │   ├── table_widget.py
  │   │   │   └── tabs_widget.py
  │   │   ├── dashboard.py     # Composición de widgets
  │   │   └── dialog.py        # Diálogos modales (JSON input/output)
  │   ├── core/                # Lógica de Agente de Cambio
  │   │   ├── deepseek_connector.py
  │   │   ├── delta_calculator.py
  │   │   ├── prompt_engine.py
  │   │   └── session_manager.py
  │   └── comms/               # Comunicación
  │       ├── socket_handler.py  # Socket.IO o Unix sockets
  │       └── json_protocol.py   # Protocolo JSON para widgets
  ├── config/
  │   └── config.yaml          # Configuración (modelo, umbral delta, etc.)
  ├── docs/                    # Documentación específica del agente
  │   └── AGENTE-CAMBIO-README.md
  └── tests/                   # Tests de módulos
  ```

- [ ] **3.2** Implementar módulos core (traducción desde Agente-De-Cambio-STABLE)
  - `deepseek_connector.py`: Conexión API DeepSeek, streaming
  - `delta_calculator.py`: Métricas de deriva (score 0-1, umbral configurable)
  - `prompt_engine.py`: System prompt editable, negociación de cambios
  - `session_manager.py`: Persistencia SQLite (objetivos, memoria)
  - **Regla de oro**: Máximo 3 funciones por módulo

- [ ] **3.3** Implementar sistema de widgets TUI (protocolo JSON)
  - Cada widget responde JSON: `{tipo: "chat|gauge|table", datos: {...}, accion: "render|update|clear"}`
  - Cada elemento de dashboard recibe JSON e interactúa: `{evento: "click|select|input", datos: {...}}`
  - Widgets atómicos en `modules/ui/widgets/`:
    - `chat_widget.py`: Burbujas de conversación, streaming carácter por carácter
    - `gauge_widget.py`: Medidor de deriva delta (0-1) con umbral visual
    - `table_widget.py`: Tabla para modo cuestionario (opciones)
    - `tabs_widget.py`: Pestañas para cambiar chat/cuestionario
    - `prompt_editor.py`: Editor de system prompt editable

- [ ] **3.4** Implementar orquestador (`src/main.py`)
  - Modo interactivo: `agente-cambio i`
  - Modo consulta: `agente-cambio p "pregunta"`
  - Modo dashboard: `agente-cambio dashboard`
  - Integración con ARES: usar mismos modelos, RAG, sesiones Kitty

- [ ] **3.5** Implementar comunicación JSON (`modules/comms/json_protocol.py`)
  - Protocolo simple: `{widget_id, tipo, accion, datos, timestamp}`
  - Widgets se registran con orquestador
  - Eventos se propagan vía JSON (ej: gauge supera umbral → notificar)

- [ ] **3.6** Crear documentación del agente
  - `docs/AGENTE-CAMBIO-README.md`: Propósito, uso, ejemplos
  - `docs/MODULOS-AGENTE-CAMBIO.md`: Lista de módulos con funciones
  - Actualizar `LEEME.md` de TR: añadir AgenteDeCambio a lista de agentes

- [ ] **3.7** Tests y validación
  - Tests unitarios para cada módulo core
  - Tests de integración para widgets TUI
  - Validar streaming en tiempo real
  - Validar protocolo JSON

### Criterios de Aceptación
- [ ] Estructura de carpetas creada en `AGENTES/sub-agentes/AgenteDeCambio/`
- [ ] Módulos core implementados (≤3 funciones cada uno)
- [ ] Widgets TUI implementados con protocolo JSON
- [ ] Orquestador funcional con modos interactivo/consulta/dashboard
- [ ] Documentación completa en `docs/`
- [ ] Tests passing
- [ ] Integración con ARES verificada

---

## Flujo de Trabajo Detallado

### Paso 0: Análisis y TODO (ACTUAL)
- [x] Analizar intención del usuario
- [x] Reflexionar sobre causa-efecto
- [x] Organizar por puntos lógicos
- [x] Crear TODO físico en `/home/daniel/tron/programas/TR/docs/TODO/`

### Paso 1: Documentar Agente de Cambio
- [ ] Leer repositorio completo
- [ ] Extraer módulos clave
- [ ] Crear 3 documentos en `docs/AgenteDeCambio/`
- [ ] Validar con `git diff`

### Paso 2: Documentar Ratatui y alternativas
- [ ] Analizar `/home/daniel/borrar/ratatui/`
- [ ] Evaluar alternativas Python (textual, rich, urwid)
- [ ] Crear 2 documentos en `docs/Ratatui/`
- [ ] Decidir stack tecnológico
- [ ] Validar con `git diff`

### Paso 3: Implementar AgenteDeCambio CLI
- [ ] Crear estructura de carpetas
- [ ] Implementar módulos core
- [ ] Implementar widgets TUI + protocolo JSON
- [ ] Implementar orquestador
- [ ] Crear documentación
- [ ] Tests y validación
- [ ] Integración con ARES
- [ ] Validar con `git diff`

---

## Recursos y Referencias

### Repositorios a Analizar
- `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/` (origen funcional)
- `/home/daniel/borrar/ratatui/` (referencia TUI)

### Documentación TR/ARES a Leer
- `/home/daniel/tron/programas/TR/LEEME.md` (metodología ARES)
- `/home/daniel/tron/programas/TR/docs/ArquitecturadeMódulosOrientadaaIA/PARA-DESARROLLAR-SKILL-sistema-trabajo-estructura.md` (skills)
- `/home/daniel/tron/programas/TR/docs/Protocolos/dont-touch-my-eggs.md` (coexistencia multi-IA)
- `/home/daniel/tron/programas/TR/docs/Protocolos/Protocolo-Cuadreno-Apuntes-IA.md` (protocolo cuaderno)

### Herramientas TRON a Usar
- `ini`: Para globalizar scripts en `/usr/bin`
- `repo`: Para auditoría git (`repo status`, `repo audit AgenteDeCambio`)
- `ares p`: Para consultas a IA durante desarrollo
- `ares i`: Modo interactivo para testing

---

## Métricas de Éxito

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| Modularidad | ≤3 funciones/módulo | Contar `def ...` en cada módulo |
| Documentación | 100% de módulos documentados | Verificar docs/ por cada módulo |
| Streaming | <100ms latencia | Medir tiempo entre chunks |
| Protocolo JSON | Widgets intercambian datos sin acoplamiento | Test de integración |
| Integración ARES | Usa mismos modelos, RAG, sesiones | Test end-to-end |

---

## Próximos Pasos Inmediatos

1. **Ejecutar FASE 1**: Documentar Agente de Cambio STABLE
   - Carpeta destino: `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/`
   - Documentos: ARQUITECTURA, MODULOS-REUTILIZABLES, FLUJOS-INTERACCION
   - Timestamp esperado: 15-03-2026

2. **Reservar módulos en `dont-touch-my-eggs.md`** antes de comenzar FASE 2
   - Evitar colisiones con otras IAs

3. **Ejecutar FASE 2**: Documentar Ratatui y decidir stack
   - Carpeta destino: `/home/daniel/tron/programas/TR/docs/Ratatui/`
   - Decisión crítica: ¿Rust (Ratatui) o Python (textual/rich)?

4. **Ejecutar FASE 3**: Implementar AgenteDeCambio CLI
   - Carpeta destino: `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/AgenteDeCambio/`
   - Validar con `repo audit AgenteDeCambio`

---

## Notas de Diseño

- **Pragmatismo radical**: No construir catedrales, navaja suiza bien afilada
- **Belleza funcional**: Interfaz que comunica profesionalismo
- **Adaptación perfecta**: Como Google Lens, la herramienta desaparece
- **Filosofía TRON**: Modularidad atómica, documentación granular, soberanía tecnológica

---

*Documento creado: 15-03-2026*  
*Última actualización: 15-03-2026*  
*Estado: [DEV] - Pendiente de ejecución FASE 1*

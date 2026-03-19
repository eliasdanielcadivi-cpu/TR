# PLAN DE IMPLEMENTACIÓN - AgenteDeCambio CLI (TRON/ARES)

## Módulo: Traducción de Propósito Web → CLI (Filosofía Google Lens)

**Fecha:** 16-03-2026  
**Versión:** 2.0 (Post-análisis documentos originales)  
**Estado:** [PENDIENTE DE REVISIÓN Y EDICIÓN]

---

## 0. ANÁLISIS DEL PROPÓSITO (Post-Lectura Completa)

### 0.1 ¿Qué ES AgenteDeCambio? (Esencia, no implementación)

**NO es:** "Una web con Next.js", "Un dashboard bonito", "React + Framer Motion"

**SÍ es:**
> "Una entidad servidor cognitivo que conduce al usuario hacia sus objetivos mediante prompts vivos que se adaptan en tiempo real, con métricas de deriva negociadas y mínima fricción de escritura"

**Propósito real (ListaRequerimientos.md #1.5):**
> "Crear un sistema cognitivo de alto valor que conduzca al éxito rotundo de la persona (objetivos, metas, fechas) mediante una interacción fluida donde la IA negocia y adapta su prompt sin perder el rumbo"

### 0.2 Filosofía "Google Lens" Aplicada a CLI

| Principio Web | Traducción CLI |
|---------------|----------------|
| "Herramienta desaparece, resultado visible" | Terminal limpia, sin decoraciones innecesarias |
| "Pragmatismo radical: navaja suiza" | Textual (Python) + Rust solo donde brilla |
| "No sobra ni falta nada" | Solo widgets que cumplen función crítica |
| "Ratio utilidad/esfuerzo" | Máximo impacto con mínimo código |
| "Adaptación perfecta a necesidad" | CLI que se siente como extensión del pensamiento |

### 0.3 Los 27 Requerimientos → Funcionalidades CLI

| # | Requerimiento Original | Traducción CLI |
|---|------------------------|----------------|
| 1 | Filosofía Google Lens | Terminal limpia, sin "sancocho" visual |
| 2 | Servidor cognitivo ("una cosa") | `ares agente AgenteDeCambio` (sub-agente standalone) |
| 3 | DeepSeek API | Ya integrado en ARES (mismo motor) |
| 4 | Prompt vivo y mutante | Editor de prompt en tiempo real (TextArea) |
| 5 | Negociación de deriva | Gauge delta + diálogo de confirmación |
| 6 | Interfaz híbrida (botones + comentario) | Botones Textual + Input adicional |
| 7 | Memoria permanente de objetivos | SQLite + inyección en prompt |
| 8 | Doble instancia (Arquitecto/Ejecutor) | Módulo delta_calculator + prompt_engine |
| 10 | Tecnología "navaja suiza" | Textual (90%) + Ratatui (10%) |
| 11 | Optimización Note 8/Termux | CLI nativa, sin web, mínimo RAM |
| 12 | Métrica de deriva (0-1) | Gauge Ratatui + umbral 0.3 |
| 14 | Reducción fricción cognitiva | Botones predefinidos + auto-complete |
| 20 | Eficacia y eficiencia | ≤3 funciones/módulo (ARES) |
| 21 | Logging y diagnóstico | RichLog + modo debug |
| 22 | Variables de entorno | Config.yaml + .env (ARES) |
| 24 | Accesibilidad CLI | Contrastes, tamaños, teclado |
| 25 | Sin mocks, conexión real | DeepSeek API directa (ya en ARES) |
| 27 | Estilo comunicativo determinista | Mensajes claros, concisos, precisos |

---

## 1. ARQUITECTURA REVISADA (Post-Análisis)

### 1.1 Lo que SÍ necesitamos

```
┌─────────────────────────────────────────────────────────────┐
│  ARES (orquestador)                                         │
│    └── agente AgenteDeCambio [accion]                       │
│         ├── run     → Interfaz TUI completa                 │
│         ├── test    → Tests componentes                     │
│         ├── install → Compilar Rust                         │
│         └── status  → Verificar instalación                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  AgenteDeCambio TUI (Textual 90% + Ratatui 10%)             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ZONA-A: Header                                        │ │
│  │  [🤖 AgenteDeCambio] [Chat▼] [Reasoning:ON] [Δ:0.25] │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ZONA-B: Prompt Editor (editable, tiempo real)         │ │
│  │  "Eres un sistema de EXTRACCIÓN COGNITIVA..."         │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ZONA-C: Chat Area (scrollable)                        │ │
│  │  ╭─────────────────────────────────────────────────╮  │ │
│  │  │ [User] ¿Qué es TypeScript?                      │  │ │
│  │  ╰─────────────────────────────────────────────────╯  │ │
│  │  ╭─────────────────────────────────────────────────╮  │ │
│  │  │ [Bot] TypeScript es un lenguaje...              │  │ │
│  │  ╰─────────────────────────────────────────────────╯  │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ZONA-D: Input + Botones                               │ │
│  │  [Escribe aquí...]  [▲] [▼] [Enviar]                  │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ZONA-E: Footer (atajos)                               │ │
│  │  q:Quit  ↑↓:Nav  Enter:Send  /:Help                   │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Lo que NO necesitamos (de la web)

| Componente Web | ¿Por qué NO en CLI? | Alternativa CLI |
|----------------|---------------------|-----------------|
| Next.js 14 + App Router | Overhead innecesario | Textual App nativa |
| React 18 + TypeScript | Complejidad añadida | Python puro |
| Tailwind CSS + Framer Motion | Solo web | TCSS (Textual CSS) |
| Socket.IO | WebSocket para web | Unix sockets o polling |
| Zustand | Estado en navegador | SQLite + memoria |
| Glassmorphism | Efecto visual web | Contrastes ASCII/Unicode |
| Burbujas animadas | Animaciones web | Texto estático claro |

---

## 2. MÓDULOS ESENCIALES (Traducción Funcional)

### 2.1 Módulos Core (Python) - YA EXISTEN EN STABLE

| Módulo Original (TypeScript) | Traducción Python | Estado |
|------------------------------|-------------------|--------|
| `deepseek-connector/actions.ts` | `modules/core/deepseek_connector.py` | ✅ YA TRADUCIDO |
| `delta-calculator/actions.ts` | `modules/core/delta_calculator.py` | ✅ YA TRADUCIDO |
| `prompt-engine/actions.ts` | `modules/core/prompt_engine.py` | ✅ YA TRADUCIDO |
| `session-manager/actions.ts` | `modules/core/session_manager.py` | ✅ YA TRADUCIDO |

**Funciones por módulo (≤3 - Filosofía ARES):**

```python
# deepseek_connector.py (2 funciones)
def create_completion(messages, api_key, **kwargs) -> Dict
async def create_completion_stream(messages, api_key, **kwargs) -> AsyncGenerator

# delta_calculator.py (4 funciones)
def calculate(old_prompt, new_prompt) -> float
def compare(old_prompt, new_prompt) -> DeltaComparison
def threshold() -> float
def requires_approval(delta_score) -> bool

# prompt_engine.py (4 funciones)
def build_system_prompt(params) -> str
def update_prompt(session, new_prompt, force=False) -> PromptUpdateResult
def negotiate_change(old_prompt, new_prompt) -> NegotiationResult
def get_default_prompt() -> str

# session_manager.py (6 funciones)
def create_session(session_id=None) -> Dict
def get_session(session_id) -> Optional[Dict]
def update_session(session_id, updates) -> bool
def delete_session(session_id) -> bool
def list_sessions() -> List[str]
def get_session_stats() -> Dict
```

### 2.2 Widgets TUI (Textual + Ratatui)

| Widget | Implementación | Complejidad |
|--------|----------------|-------------|
| **Header** | Textual Static + Labels | Simple |
| **PromptEditor** | Textual TextArea | Simple |
| **ChatArea** | Textual VerticalScroll + Statics | Media |
| **ChatMessage** | Textual Static (custom class) | Simple |
| **InputArea** | Textual Input + Button | Simple |
| **DeltaGauge** | Ratatui (Rust) + Textual wrapper | Compleja |
| **ModeSwitcher** | Textual Tabs o Select | Simple |
| **Footer** | Textual Footer widget | Simple |

---

## 3. FLUJOS DE INTERACCIÓN (Traducción Web → CLI)

### 3.1 Modo Chat (Web → CLI)

| Web (Socket.IO) | CLI (Textual) |
|-----------------|---------------|
| `socket.emit('message:send', content)` | `on_button_pressed()` → Input value |
| `socket.on('message:stream', chunk)` | `async for chunk in stream:` → update() |
| `socket.on('delta:update', metrics)` | `watch_delta()` → gauge.refresh() |

**Flujo CLI:**
```
1. Usuario escribe en Input
2. Presiona Enter o botón "Enviar"
3. on_input_submitted() captura texto
4. Crea mensaje usuario → ChatArea.mount()
5. Llama a create_completion_stream()
6. Stream carácter por carácter → bot_msg.update()
7. Calcula delta → gauge.refresh()
8. Si delta > threshold → Dialog de confirmación
```

### 3.2 Modo Cuestionario (Web → CLI)

| Web (React) | CLI (Textual) |
|-------------|---------------|
| `<Questionnaire options={...} />` | `OptionList` widget |
| `onClick(option)` | `on_option_list_option_selected()` |
| `comment: string` | `Input(placeholder="Comentario adicional")` |

**Flujo CLI:**
```
1. Bot genera pregunta con opciones (JSON)
2. OptionList monta opciones (radio/check)
3. Usuario selecciona con flechas + Enter
4. on_option_selected() captura selección
5. Input adicional para comentario
6. Envía selección + comentario
7. Siguiente pregunta (o finaliza)
```

### 3.3 Edición de Prompt (Web → CLI)

| Web (PromptEditor.tsx) | CLI (Textual TextArea) |
|------------------------|------------------------|
| `contentEditable` div | `TextArea` widget |
| `onChange` handler | `TextArea.Changed` event |
| Real-time preview | Live update del gauge |

**Flujo CLI:**
```
1. Usuario hace click en PromptEditor
2. TextArea se vuelve editable (modo insert)
3. on_text_area_changed() captura cambios
4. calculate_delta() en tiempo real
5. Gauge actualiza color (verde/amarillo/rojo)
6. Si delta > 0.3 → muestra advertencia
7. Usuario confirma o revierte
```

---

## 4. TECNOLOGÍAS SELECCIONADAS (Navaja Suiza)

### 4.1 Stack Tecnológico CLI

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| **Framework TUI** | Textual 8.1.1 | Python nativo, widgets interactivos, TCSS |
| **Render Visual** | Ratatui 0.30 (Rust) | Gauges/sparklines de alta calidad |
| **HTTP Cliente** | httpx 0.28+ | Async streaming para DeepSeek API |
| **Base de Datos** | SQLite (stdlib) | Persistencia de sesiones, objetivos |
| **Configuración** | YAML (pyyaml) | Config.yaml de ARES |
| **Logging** | Rich + RichLog | Logs enriquecidos en TUI |

### 4.2 ¿Por qué NO Rust para todo?

| Criterio | Textual (Python) | Ratatui (Rust) | Decisión |
|----------|------------------|----------------|----------|
| Integración ARES | ✅ Nativa | ❌ Requiere FFI | Textual |
| Widgets interactivos | ✅ Buttons, Inputs | ❌ Solo render | Textual |
| Curva aprendizaje | ✅ Python simple | ❌ Rust complejo | Textual |
| Gauges visuales | ⚠️ Aceptable | ✅ Excelente | Ratatui |
| Sparklines | ⚠️ Básico | ✅ Alta calidad | Ratatui |
| Charts | ⚠️ Limitado | ✅ Profesional | Ratatui |

**Conclusión:** 90% Textual (lógica, estructura) + 10% Ratatui (visuales críticos)

---

## 5. ETAPAS DE IMPLEMENTACIÓN (Revisadas)

### Etapa 1: Núcleo Funcional (Día 1-2)
- [x] Módulos core Python (deepseek, delta, prompt, session)
- [ ] App Textual mínima (Header, Footer, ChatArea, Input)
- [ ] Streaming DeepSeek funcional
- [ ] Gauge delta básico (ASCII fallback)

### Etapa 2: Widgets Críticos (Día 3-4)
- [ ] DeltaGauge Ratatui integrado
- [ ] Sparkline historial
- [ ] PromptEditor (TextArea editable)
- [ ] ModeSwitcher (Chat/Cuestionario)

### Etapa 3: Flujos Completos (Día 5-6)
- [ ] Modo chat completo (input → stream → delta)
- [ ] Modo cuestionario (OptionList + comentario)
- [ ] Edición de prompt en tiempo real
- [ ] Confirmación de cambios (delta > threshold)

### Etapa 4: Pulido y Testing (Día 7)
- [ ] Tests unitarios módulos core
- [ ] Tests integración TUI
- [ ] Logging + diagnóstico
- [ ] Documentación de uso

---

## 6. CRITERIOS DE ACEPTACIÓN (Por Funcionalidad)

### 6.1 Prompt Vivo y Mutante

| Criterio | Web | CLI | Estado |
|----------|-----|-----|--------|
| Editor en tiempo real | ✅ ContentEditable | ⏳ TextArea | Pendiente |
| Negociación de cambios | ✅ Dialog | ⏳ Dialog modal | Pendiente |
| Métricas de deriva (0-1) | ✅ DeltaMeter | ⏳ Gauge Ratatui | Parcial |
| Prevención desviaciones | ✅ Lógica backend | ✅ Mismo código | OK |

### 6.2 Interfaz Híbrida

| Criterio | Web | CLI | Estado |
|----------|-----|-----|--------|
| Botones de opción | ✅ Radio/Check | ⏳ OptionList | Pendiente |
| Comentario adicional | ✅ Input texto | ⏳ Input widget | Pendiente |
| Transiciones suaves | ✅ Framer Motion | ⏳ Animaciones Textual | Pendiente |
| Mínima escritura | ✅ Auto-complete | ⏳ Botones predefinidos | Pendiente |

### 6.3 Memoria Permanente

| Criterio | Web | CLI | Estado |
|----------|-----|-----|--------|
| Persistencia objetivos | ✅ localStorage | ⏳ SQLite | Pendiente |
| Inyección en prompt | ✅ Zustand | ✅ Mismo patrón | OK |
| Conducción inteligente | ✅ Lógica backend | ✅ Mismo código | OK |

---

## 7. PRÓXIMOS PASOS INMEDIATOS

### 7.1 Revisión del Plan (AHORA)

**Acciones del usuario:**
1. Leer este plan completo
2. Identificar discrepancias con visión original
3. Editar/corregir secciones necesarias
4. Aprobar plan para implementación

### 7.2 Implementación (Post-Aprobación)

**Orden de ejecución:**
```
1. Crear estructura de carpetas en AGENTES/sub-agentes/AgenteDeCambio/
2. Mover módulos core existentes (deepseek, delta, prompt, session)
3. Implementar App Textual mínima (Header, Footer, ChatArea, Input)
4. Integrar streaming DeepSeek
5. Añadir DeltaGauge Ratatui
6. Implementar flujos completos (chat, cuestionario, prompt editor)
7. Tests y documentación
```

---

## 8. NOTAS DE TRADUCCIÓN (Web → CLI)

### 8.1 Lo que se PIERDE (y NO importa)

| Elemento Web | ¿Por qué NO importa? |
|--------------|----------------------|
| Glassmorphism | Estético, no funcional |
| Animaciones 60fps | CLI no requiere fluidez visual |
| Burbujas con gradiente | Texto claro es suficiente |
| Microinteracciones hover | CLI se usa con teclado |
| Responsive design | Terminal tiene tamaño fijo |

### 8.2 Lo que se GANA

| Elemento CLI | Beneficio |
|--------------|-----------|
| Sin navegador | Menos RAM, más rápido |
| Nativo en terminal | Funciona en Note 8/Termux |
| Integración ARES | Mismo ecosistema, comandos unificados |
| Sin build process | Cambios inmediatos, sin compile |
| SSH-friendly | Remoto, servers, low-resource |

### 8.3 Lo que se MANTIENE (Esencial)

| Elemento | Implementación CLI |
|----------|-------------------|
| Prompt vivo | TextArea editable + gauge en tiempo real |
| Negociación delta | Mismo algoritmo, dialog modal |
| Memoria objetivos | SQLite + inyección en prompt |
| Streaming carácter | Mismo código, async generator |
| Doble instancia | Módulos separados (ejecutor/arquitecto) |

---

## 9. COMANDOS DE USO (Post-Implementación)

```bash
# Verificar estado
ares agente AgenteDeCambio status

# Instalar componentes Rust (si no están)
ares agente AgenteDeCambio install

# Probar componentes
ares agente AgenteDeCambio test

# Ejecutar interfaz TUI completa
ares agente AgenteDeCambio run

# Ayuda
ares agente AgenteDeCambio --help
```

---

## 10. DOCUMENTACIÓN INTELIGENTE (Conectada con TODO)

### 10.1 Documentación Original (Agente-De-Cambio-STABLE)

| Documento | Ruta Original | Síntesis (Meta + Intencionalidad) | Traducción CLI |
|-----------|---------------|-----------------------------------|----------------|
| **ListaRequerimientos.md** | `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/ListaRequerimientos.md` | **Meta:** 27 requerimientos con filosofía "Google Lens" (herramienta desaparece, resultado visible). **Intencionalidad:** Pragmatismo radical, "no sobra ni falta nada", adaptación perfecta a necesidad. Requiere métrica de deriva (0-1), negociación determinista, memoria permanente de objetivos, interfaz híbrida (botones + comentario). | CLI limpia, sin decoraciones. Gauge delta + dialog confirmación. SQLite para objetivos. OptionList + Input para interfaz híbrida. |
| **proyecto.md** | `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/proyecto.md` | **Meta:** Arquitectura completa (Next.js + Node.js + Socket.IO + DeepSeek). **Intencionalidad:** 5 etapas de implementación, sistema de diseño glassmorphism, streaming carácter por carácter, modo dual chat/cuestionario. Métricas de éxito: <2s respuesta, <100ms streaming, 60fps animaciones. | Textual (Python) en lugar de Next.js. Async generators en lugar de Socket.IO. TCSS en lugar de Tailwind. Mismas métricas adaptadas a CLI. |
| **Maestro.md** | `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/DISENO/Maestro.md` | **Meta:** Consolidar información táctica para IA externa. **Intencionalidad:** Sistema de coordenadas (Zonas A-D), filosofía de diseño NO NEGOCIABLE, estándares 2024-2026 (Capability-Based, MCP, Spring Physics). Convenciones de diálogo IA-usuario. | Zonas A-E en CLI. Filosofía "Google Lens" mantenida. Capability-Based → ≤3 funciones/módulo (ARES). Diálogo: `[ZONA]-[COMPONENTE]: [efecto]`. |
| **README.md** | `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/README.md` | **Meta:** Visión general del sistema. **Intencionalidad:** Prompt vivo y mutante, interfaz híbrida, glassmorphism premium, streaming tiempo real, arquitectura doble instancia (Ejecutor/Arquitecto). | Prompt vivo → TextArea editable. Interfaz híbrida → OptionList + Input. Streaming → async generator. Doble instancia → módulos separados. |

### 10.2 Documentación TRON (Traducción CLI)

| Documento | Ruta TRON | Síntesis (Meta + Intencionalidad) | Conexión con TODO |
|-----------|-----------|-----------------------------------|-------------------|
| **ARQUITECTURA-15-03-2026.md** | `docs/AgenteDeCambio/ARQUITECTURA-15-03-2026.md` | **Meta:** Traducir arquitectura web → CLI. **Intencionalidad:** Protocolo JSON para widgets, flujos de streaming, widgets modulares C→JSON. Checklist debug de problemas comunes. | TODO: Implementar protocolo JSON en `modules/comms/json_protocol.py` |
| **MODULOS-15-03-2026.md** | `docs/AgenteDeCambio/MODULOS-REUTILIZABLES-15-03-2026.md` | **Meta:** Traducir 4 módulos core (TypeScript → Python). **Intencionalidad:** deepseek_connector (2 funciones), delta_calculator (4 funciones), prompt_engine (4 funciones), session_manager (6 funciones). Código Python listo para usar. | TODO: Mover módulos a `modules/core/` y validar imports |
| **FLUJOS-15-03-2026.md** | `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md` | **Meta:** Documentar flujos chat/cuestionario/edición. **Intencionalidad:** Eventos Socket.IO originales → flujos CLI. Patrones extraídos (streaming, widget JSON, diálogo modal). Interfaces TUI por modo (ASCII diagrams). | TODO: Implementar flujos en `modules/ui/widgets/` |
| **PLAN-15-03-2026.md** | `docs/AgenteDeCambio/PLAN-IMPLEMENTACION-90-10-15-03-2026.md` | **Meta:** Estrategia híbrida 90% Textual + 10% Ratatui. **Intencionalidad:** Arquitectura de carpetas, flujo de comunicación Python↔Rust, TCSS completo. Hitos de implementación (3A, 3B, 3C). | TODO: Ejecutar hitos en orden (ver TODO-16-03-2026.md) |
| **RATATUI-15-03-2026.md** | `docs/Ratatui/RATATUI-REFERENCIA-TECNICA-15-03-2026.md` | **Meta:** Referencia técnica de Ratatui (Rust). **Intencionalidad:** Arquitectura modular (crates), widgets principales (Block, Paragraph, Gauge, Table, Tabs), patrón de renderizado (`terminal.draw`). | TODO: Compilar componentes Rust (ya completado) |
| **RATATUI-ALT-15-03-2026.md** | `docs/Ratatui/RATATUI-ALTERNATIVAS-PYTHON-TUI-15-03-2026.md` | **Meta:** Comparativa Textual vs Rich vs Urwid. **Intencionalidad:** Decisión recomendada: Textual (Python). Razones: integración nativa ARES, widgets interactivos, TCSS, async/await. | TODO: Usar Textual para 90% de la interfaz |
| **TEXTUAL-CUADERNO-15-03-2026.md** | `docs/Textual/TEXTUAL-CUADERNO-APUNTES-IA-15-03-2026.md` | **Meta:** Cuaderno completo de Textual (~2,500 líneas). **Intencionalidad:** 59 widgets builtin, patrones fundamentales (App mínima, Code Browser, Calculator, FiveByFive), arquitectura completa. | TODO: Seguir patrones del cuaderno para widgets |
| **TEXTUAL-PATRONES-15-03-2026.md** | `docs/Textual/TEXTUAL-PATRONES-AVANZADOS-15-03-2026.md` | **Meta:** Patrones avanzados de diseño. **Intencionalidad:** Chat Dashboard completo, worker asíncrono, reactivo avanzado, custom widget, screen con resultado, command palette custom, testing. | TODO: Implementar patrón Chat Dashboard |
| **TEXTUAL-EJEMPLOS-15-03-2026.md** | `docs/Textual/TEXTUAL-EJEMPLOS-REFERENCIA-15-03-2026.md` | **Meta:** Índice de 24 ejemplos + 59 widgets. **Intencionalidad:** Catálogo de widgets con ejemplos, TCSS reference, bindings, eventos, decoradores @on, utilidades. | TODO: Consultar ejemplos al implementar cada widget |

### 10.3 TODO Conectado (Táctica-Estrategia)

| TODO | Ruta | Conexión con Plan | Estado |
|------|------|-------------------|--------|
| **TODO-16-03-2026-07-45.md** | `docs/TODO/TODO-AGENTE-CAMBIO-RATATUI-CLI-16-03-2026-07-45.md` | **Meta:** Documentar edición-sección-acción en tiempo real. **Intencionalidad:** Trazabilidad completa de cambios, conexión bidireccional PLAN↔TODO. **16 items definidos** (4 etapas, 6% completado). | ⏳ EN PROGRESO (TODO-1.4 parcial) |

**Conexión Bidireccional:**
- **PLAN → TODO:** Cada etapa del PLAN tiene TODO items asociados (ver sección 11 del TODO)
- **TODO → PLAN:** Cada TODO item referencia sección del PLAN (ver "Conexión con PLAN")
- **Documentación → TODO:** Cada TODO item referencia documentación específica (ver "Conexión con Documentación")
- **TODO → Documentación:** TODO items usan documentación como referencia técnica

**Timeline de Ejecución:**
```
16-03-2026 07:45 → TODO creado
16-03-2026 08:00 → 16 items definidos
16-03-2026 08:15 → TODO-1.4 parcial (gauge ASCII funciona)
Próximo: TODO-1.1 (mover módulos core)
```

---

### 10.4 Código Existente

| Componente | Ruta | Estado | Conexión con TODO |
|------------|------|--------|-------------------|
| Módulos Core Python | `modules/ui/agente_de_cambio.py` | ✅ OK | TODO: Mover a `modules/core/` |
| Hybrid Renderer | `modules/ui/hybrid_renderer.py` | ✅ OK | TODO: Actualizar rutas absolutas |
| Ratatui Components | `AGENTES/sub-agentes/AgenteDeCambio/modules/ui/ratatui_components/` | ✅ COMPILADO | TODO: Probar en TUI real |
| Comandos ARES | `src/main.py` (agente AgenteDeCambio) | ✅ OK | TODO: Añadir ayuda enriquecida |

---

## 11. DIRECTRICES DE IMPLEMENTACIÓN

### 11.1 Filosofía "Google Lens" (NO NEGOCIABLE)

1. **Herramienta invisible:** Terminal limpia, sin decoraciones innecesarias
2. **Pragmatismo radical:** Si no cumple función crítica, se elimina
3. **Ratio utilidad/esfuerzo:** Máximo impacto con mínimo código
4. **Adaptación perfecta:** CLI que se siente como extensión del pensamiento
5. **Sin catedrales:** Navaja suiza bien afilada, no arquitectura compleja

### 11.2 Reglas de Oro ARES

1. **≤3 funciones por módulo:** Modularidad atómica
2. **JSON output para Agentes:** Estructura estándar
3. **Documentación granular:** Cada módulo con INDEX.md
4. **Git diff post-CRUD:** Validar cambios exactos
5. **dont-touch-my-eggs:** Reservar antes de trabajar

---

**FIN DEL PLAN - PENDIENTE DE REVISIÓN Y EDICIÓN**

*Fecha: 16-03-2026*  
*Próximo paso: Usuario lee, edita y aprueba plan*  
*Post-aprobación: Comenzar implementación Etapa 1*

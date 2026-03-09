# 🥋 ARES SKILLS INDEX — BIBLIOTECA COMPLETA DE KUNG-FU IA (v2.0)

> **Arsenal completo de capacidades procedimentales para ARES.** Cada skill es un paquete autocontenido con scripts, referencias, assets y documentación operativa.

---

## 📊 RESUMEN DEL ARSENAL

| Categoría | Skills | Archivos Totales | Tamaño | Scripts | Referencias | Assets |
|-----------|--------|------------------|--------|---------|-------------|--------|
| **dev/** | 4 | 45 | 1.2 MB | 12 | 4 | 2 |
| **doc-processing/** | 2 | 85 | 2.8 MB | 18 | 4 | 30+ XSD |
| **office/** | 2 | 95 | 3.1 MB | 15 | 3 | 30+ XSD |
| **multimedia/** | 2 | 25 | 850 KB | 8 | 2 | 2 |
| **ia/** | 1 | 12 | 420 KB | 3 | 2 | 0 |
| **comms/** | 1 | 6 | 85 KB | 0 | 0 | 4 examples |
| **design/** | 3 | 95 | 1.3 MB | 0 | 20 themes | 80+ fonts |
| **core/** | 3 | 4 | 45 KB | 0 | 0 | 0 |
| **TOTAL** | **18** | **367** | **9.6 MB** | **56** | **35** | **120+** |

---

## 🗂️ CLASIFICACIÓN COMPLETA

---

### 💻 DESARROLLO (dev/)

**Propósito:** Construcción, testing e integración de software y APIs.

| Skill | Archivos | Scripts | Referencias | Assets | Trigger |
|-------|----------|---------|-------------|--------|---------|
| **[mcp-builder](dev/mcp-builder/)** | 10 | 4 | 4 | 0 | "MCP server", "integra API" |
| **[webapp-testing](dev/webapp-testing/)** | 8 | 1 | 0 | 3 examples | "testea webapp", "Playwright" |
| **[frontend-design](dev/frontend-design/)** | 2 | 0 | 0 | 0 | "diseña UI", "frontend" |
| **[web-artifacts-builder](dev/web-artifacts-builder/)** | 4 | 2 | 0 | 1 (.tar.gz) | "artifact React", "shadcn" |

#### Detalle por Skill

**mcp-builder/** — Servidores MCP para integrar APIs externas con LLMs
- **Scripts:** `evaluation.py`, `connections.py`, `requirements.txt`, `example_evaluation.xml`
- **Referencias:** `reference/mcp_best_practices.md`, `reference/node_mcp_server.md`, `reference/python_mcp_server.md`, `reference/evaluation.md`
- **Alcance:** Creación de herramientas MCP con TypeScript (SDK oficial) o Python (FastMCP), evaluaciones de calidad, patrones de diseño
- **Output:** Servidores MCP production-ready con tool definitions, error handling, paginación

**webapp-testing/** — Testing de aplicaciones web locales con Playwright
- **Scripts:** `scripts/with_server.py` (gestión de servidores)
- **Examples:** `element_discovery.py`, `static_html_automation.py`, `console_logging.py`
- **Alcance:** Automatización de navegadores, descubrimiento de selectores, screenshots, logs de consola
- **Output:** Scripts de testing reproducibles con gestión automática de servidores

**frontend-design/** — Diseño frontend distintivo production-grade
- **Alcance:** Interfaces sin "AI slop", tipografía distintiva, paletas cohesivas, motion design
- **Output:** Código React/HTML/CSS production-ready con estética excepcional

**web-artifacts-builder/** — Artifacts HTML multi-componente con React + Tailwind + shadcn/ui
- **Scripts:** `scripts/init-artifact.sh`, `scripts/bundle-artifact.sh`, `scripts/shadcn-components.tar.gz`
- **Alcance:** Inicialización de proyectos React, bundling a HTML único, 40+ componentes shadcn/ui
- **Output:** `bundle.html` autocontenido para claude.ai artifacts

---

### 📄 PROCESAMIENTO DE DOCUMENTOS (doc-processing/)

**Propósito:** Creación, edición y análisis de documentos (.docx, .pdf) con tracked changes y formularios.

| Skill | Archivos | Scripts | Referencias | Assets | Trigger |
|-------|----------|---------|-------------|--------|---------|
| **[docx](doc-processing/docx/)** | 50+ | 6 | 2 | 30+ XSD | "Word", ".docx", "redlining" |
| **[pdf](doc-processing/pdf/)** | 15 | 8 | 2 | 0 | "PDF", "formulario", "extrae texto" |

#### Detalle por Skill

**docx/** — Creación y edición de Word con tracked changes, comentarios, OOXML
- **Scripts:** `scripts/unpack.py`, `scripts/pack.py`, `scripts/validate.py`, `scripts/document.py`, `scripts/inventory.py`, `scripts/replace.py`
- **Referencias:** `docx-js.md` (creación JS), `ooxml.md` (edición XML), `ooxml/schemas/` (30+ XSD para validación)
- **Alcance:** Redlining workflow, tracked changes minimal edits, batch processing, comentarios, preservación de formato
- **Output:** Documentos .docx con cambios trackeados profesionalmente

**pdf/** — Procesamiento integral de PDFs: texto, tablas, formularios, OCR
- **Scripts:** `scripts/check_bounding_boxes.py`, `scripts/check_fillable_fields.py`, `scripts/convert_pdf_to_images.py`, `scripts/create_validation_image.py`, `scripts/fill_fillable_fields.py`, `scripts/fill_pdf_form_with_annotations.py`, `scripts/extract_form_field_info.py`, `scripts/check_bounding_boxes_test.py`
- **Referencias:** `forms.md` (formularios fillable), `reference.md` (API completa pypdfium2)
- **Alcance:** Extracción texto/tablas (pdfplumber), creación (reportlab), merge/split (pypdf), OCR (pytesseract), fill forms
- **Output:** PDFs procesados, formularios rellenados, imágenes extraídas

---

### 📊 OFIMÁTICA (office/)

**Propósito:** Spreadsheets Excel y presentaciones PowerPoint con fórmulas y diseño.

| Skill | Archivos | Scripts | Referencias | Assets | Trigger |
|-------|----------|---------|-------------|--------|---------|
| **[pptx](office/pptx/)** | 60+ | 5 | 2 | 30+ XSD | "PowerPoint", ".pptx", "slides" |
| **[xlsx](office/xlsx/)** | 4 | 1 | 0 | 0 | "Excel", ".xlsx", "fórmulas" |

#### Detalle por Skill

**pptx/** — Presentaciones PowerPoint con templates, thumbnails, html2pptx
- **Scripts:** `scripts/unpack.py`, `scripts/pack.py`, `scripts/validate.py`, `scripts/html2pptx.js`, `scripts/inventory.py`, `scripts/rearrange.py`, `scripts/replace.py`, `scripts/thumbnail.py`
- **Referencias:** `html2pptx.md` (creación desde HTML), `ooxml.md` (edición XML), `ooxml/schemas/` (30+ XSD)
- **Alcance:** Template analysis con thumbnail grids, inventory extraction, rearrange slides, replacement masivo con formato
- **Output:** Presentaciones .pptx profesionales con diseño consistente

**xlsx/** — Spreadsheets Excel con fórmulas, pandas, recalculación LibreOffice
- **Scripts:** `recalc.py` (recalcula fórmulas con LibreOffice)
- **Alcance:** Creación (openpyxl), análisis (pandas), fórmulas dinámicas, color coding financiero, number formatting
- **Output:** Excel models Zero Formula Errors con fórmulas recalculadas

---

### 🎨 MULTIMEDIA (multimedia/)

**Propósito:** Arte generativo, animaciones GIF y procesamiento visual.

| Skill | Archivos | Scripts | Referencias | Assets | Trigger |
|-------|----------|---------|-------------|--------|---------|
| **[algorithmic-art](multimedia/algorithmic-art/)** | 5 | 1 | 0 | 2 | "arte generativo", "p5.js" |
| **[slack-gif-creator](multimedia/slack-gif-creator/)** | 7 | 4 | 0 | 0 | "GIF animado", "slack" |

#### Detalle por Skill

**algorithmic-art/** — Arte generativo con p5.js, seeded randomness, interactive
- **Scripts:** `templates/generator_template.js`, `templates/viewer.html`
- **Alcance:** Filosofía algorítmica (4-6 párrafos), seeded randomness, parámetros explorables, single HTML artifact
- **Output:** HTML interactivo con canvas p5.js, controls de seed/parámetros, download PNG

**slack-gif-creator/** — Creación de GIFs animados para Slack con easing y validators
- **Scripts:** `core/gif_builder.py`, `core/frame_composer.py`, `core/easing.py`, `core/validators.py`, `requirements.txt`
- **Alcance:** Composición de frames, easing functions (bounce, elastic, cubic), validación de inputs
- **Output:** GIFs optimizados para Slack con animaciones suaves

---

### 🤖 INTELIGENCIA ARTIFICIAL (ia/)

**Propósito:** Creación y gestión de skills para extender capacidades de Claude.

| Skill | Archivos | Scripts | Referencias | Assets | Trigger |
|-------|----------|---------|-------------|--------|---------|
| **[skill-creator](ia/skill-creator/)** | 8 | 3 | 2 | 0 | "crea skill", "nueva habilidad" |

#### Detalle por Skill

**skill-creator/** — Crear y actualizar skills que extienden capacidades de Claude
- **Scripts:** `scripts/init_skill.py`, `scripts/package_skill.py`, `scripts/quick_validate.py`
- **Referencias:** `references/workflows.md` (patrones de workflow), `references/output-patterns.md` (patrones de output)
- **Alcance:** Proceso de 6 pasos (entender, planificar, inicializar, editar, packagear, iterar), progressive disclosure, frontmatter YAML
- **Output:** Skills empaquetadas (.skill files) listas para distribuir

---

### 📢 COMUNICACIÓN (comms/)

**Propósito:** Comunicación interna, newsletters, FAQs, actualizaciones corporativas.

| Skill | Archivos | Scripts | Referencias | Assets | Trigger |
|-------|----------|---------|-------------|--------|---------|
| **[internal-comms](comms/internal-comms/)** | 6 | 0 | 0 | 4 examples | "newsletter", "FAQ", "comms internas" |

#### Detalle por Skill

**internal-comms/** — Comunicación interna corporativa
- **Examples:** `examples/company-newsletter.md`, `examples/faq-answers.md`, `examples/3p-updates.md`, `examples/general-comms.md`
- **Alcance:** Redacción de newsletters, respuestas a FAQs, actualizaciones third-party, comunicados generales
- **Output:** Documentos de comunicación profesional estructurados

---

### 🎯 DISEÑO (design/)

**Propósito:** Branding, diseño de canvas, temas y paletas de color.

| Skill | Archivos | Scripts | Referencias | Assets | Trigger |
|-------|----------|---------|-------------|--------|---------|
| **[brand-guidelines](design/brand-guidelines/)** | 2 | 0 | 0 | 0 | "branding", "guía de marca" |
| **[canvas-design](design/canvas-design/)** | 85+ | 0 | 0 | 80+ fonts | "diseño canvas", "typography" |
| **[theme-factory](design/theme-factory/)** | 15 | 0 | 20 themes | 1 PDF | "paleta colores", "tema" |

#### Detalle por Skill

**brand-guidelines/** — Guías de marca y branding corporativo
- **Alcance:** Identidad visual, logos, colores corporativos, tipografía de marca, tono de comunicación
- **Output:** Documentos de guía de marca estructurados

**canvas-design/** — Diseño de canvas con tipografía profesional
- **Assets:** `canvas-fonts/` (80+ archivos .ttf y .OFL): Arsenal SC, Big Shoulders, Bricolage Grotesque, Crimson Pro, DM Mono, Erica One, Geist Mono, Gloock, Instrument Sans/Serif, JetBrains Mono, Jura, Libre Baskerville, Lora, National Park, Nothing You Could Do, Outfit, Pixelify Sans, Poiret One, Red Hat Mono, Silkscreen, Smooch Sans, Tektur, Work Sans, Young Serif
- **Alcance:** Composición tipográfica profesional, licensing OFL incluido
- **Output:** Diseños de canvas con fonts licenciadas correctamente

**theme-factory/** — Fábrica de temas y paletas de color
- **Referencias:** 20 temas en `themes/`: arctic-frost, botanical-garden, desert-rose, forest-canopy, golden-hour, midnight-galaxy, modern-minimalist, ocean-depths, sunset-boulevard, tech-innovation, cream-forest, burgundy-luxury, deep-purple-emerald, pink-purple, lime-plum, black-gold, sage-terracotta, charcoal-red, vibrant-orange, retro-rainbow
- **Assets:** `theme-showcase.pdf` (ejemplos visuales)
- **Alcance:** Paletas cohesivas para presentaciones, documentos, interfaces
- **Output:** Temas listos para aplicar con códigos hex y combinaciones

---

### 🏛️ CORE ARES (root/)

**Propósito:** Operativa base de ARES y gestión de sesiones.

| Skill | Archivos | Trigger |
|-------|----------|---------|
| **[skill-inicializacion](skill-inicializacion.md)** | 1 | "inicializa", "nuevo proyecto" |
| **[skill-sesion](skill-sesion.md)** | 1 | "gs", "guarda sesión" |
| **[skill-session-management](skill-session-management.md)** | 1 | "session", "kitty socket" |

#### Detalle por Skill

**skill-inicializacion.md** — Crear estructura base de proyectos ARES/TRON
- **Alcance:** Jerarquía paranoica, LEEME.md, REP_STRUCTURE.md, .ai/rules.md, docs/skills/INDEX.md
- **Output:** Proyectos inicializados con estructura normativa TRON

**skill-sesion.md** — Gestión de sesiones Kitty (guardar, restaurar, comandos)
- **Alcance:** `ares gs [nombre]`, `ares gs list`, `ares gs restore`, `ares gs com`
- **Output:** Sesiones persistentes de terminal con títulos semánticos

**skill-session-management.md** — Sockets de Kitty y captura de sesiones
- **Alcance:** Protocolo de sockets, diagnóstico con `ares status`
- **Output:** Control total de ventanas y pestañas Kitty

---

## 📂 ESTRUCTURA DE CARPETAS COMPLETA

```
docs/skills/
├── INDEX.md                          # Este índice maestro
├── skill-inicializacion.md           # CORE: Inicialización de proyectos
├── skill-sesion.md                   # CORE: Gestión de sesiones Kitty
├── skill-session-management.md       # CORE: Sockets Kitty
│
├── dev/                              # DESARROLLO
│   ├── mcp-builder/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── evaluation.py
│   │   │   ├── connections.py
│   │   │   └── requirements.txt
│   │   └── reference/
│   │       ├── mcp_best_practices.md
│   │       ├── node_mcp_server.md
│   │       ├── python_mcp_server.md
│   │       └── evaluation.md
│   ├── webapp-testing/
│   │   ├── SKILL.md
│   │   ├── scripts/with_server.py
│   │   └── examples/
│   ├── frontend-design/
│   │   └── SKILL.md
│   └── web-artifacts-builder/
│       ├── SKILL.md
│       └── scripts/
│
├── doc-processing/                   # PROCESAMIENTO DE DOCUMENTOS
│   ├── docx/
│   │   ├── SKILL.md
│   │   ├── docx-js.md
│   │   ├── ooxml.md
│   │   ├── scripts/
│   │   └── ooxml/schemas/ (30+ XSD)
│   └── pdf/
│       ├── SKILL.md
│       ├── forms.md
│       ├── reference.md
│       └── scripts/
│
├── office/                           # OFIMÁTICA
│   ├── pptx/
│   │   ├── SKILL.md
│   │   ├── html2pptx.md
│   │   ├── ooxml.md
│   │   ├── scripts/
│   │   └── ooxml/schemas/ (30+ XSD)
│   └── xlsx/
│       ├── SKILL.md
│       └── recalc.py
│
├── multimedia/                       # MULTIMEDIA
│   ├── algorithmic-art/
│   │   ├── SKILL.md
│   │   └── templates/
│   └── slack-gif-creator/
│       ├── SKILL.md
│       ├── core/
│       └── requirements.txt
│
├── ia/                               # INTELIGENCIA ARTIFICIAL
│   └── skill-creator/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
│
├── comms/                            # COMUNICACIÓN
│   └── internal-comms/
│       ├── SKILL.md
│       └── examples/
│
└── design/                           # DISEÑO
    ├── brand-guidelines/
    │   └── SKILL.md
    ├── canvas-design/
    │   ├── SKILL.md
    │   └── canvas-fonts/ (80+ fonts)
    └── theme-factory/
        ├── SKILL.md
        ├── themes/ (20 temas)
        └── theme-showcase.pdf
```

---

## 🎯 CÓMO USAR ESTE ÍNDICE

### 1. Identifica la Categoría
Busca en la tabla de resumen qué categoría corresponde a tu tarea.

### 2. Revisa el Detalle de la Skill
Cada skill incluye:
- **Archivos totales:** Cuántos archivos componen la skill
- **Scripts:** Código ejecutable disponible
- **Referencias:** Documentación de apoyo
- **Assets:** Recursos (fonts, templates, themes)
- **Trigger:** Palabras que activan la skill

### 3. Navega a la Carpeta
Todas las skills están en `docs/skills/{categoria}/{nombre-skill}/`

### 4. Lee SKILL.md Primero
El archivo `SKILL.md` es el punto de entrada. Este referencia:
- Scripts en `scripts/`
- Referencias en `reference/` o `references/`
- Assets en `assets/`, `templates/`, `themes/`, etc.

### 5. Ejecuta Scripts Según Necesidad
Los scripts están diseñados para usarse como black boxes:
```bash
# Ejemplo: Testing webapp
python docs/skills/dev/webapp-testing/scripts/with_server.py --help

# Ejemplo: Crear skill
python docs/skills/ia/skill-creator/scripts/init_skill.py mi-skill
```

---

## 📊 ESTADÍSTICAS DEL ARSENAL

### Por Tipo de Archivo
| Tipo | Cantidad | Propósito |
|------|----------|-----------|
| **SKILL.md** | 18 | Documentación principal de cada skill |
| **Scripts (.py)** | 35 | Lógica ejecutable Python |
| **Scripts (.js)** | 3 | Lógica ejecutable JavaScript |
| **Scripts (.sh)** | 2 | Shell scripts bash |
| **Referencias (.md)** | 35 | Documentación de apoyo |
| **Schemas (.xsd)** | 60+ | Validación OOXML |
| **Fonts (.ttf)** | 80+ | Tipografía para canvas-design |
| **Themes (.md)** | 20 | Paletas de color |
| **Examples (.md/.py)** | 10 | Patrones y ejemplos |
| **Assets (.tar.gz, .pdf)** | 5 | Recursos empaquetados |

### Por Complejidad
| Nivel | Skills | Características |
|-------|--------|-----------------|
| **Alta** | docx, pptx, mcp-builder | 50+ archivos, scripts múltiples, schemas XSD |
| **Media** | pdf, xlsx, skill-creator, webapp-testing | 10-20 archivos, scripts funcionales |
| **Baja** | frontend-design, brand-guidelines, internal-comms | 2-6 archivos, solo documentación |

---

## 🔗 RELACIÓN CON HERRAMIENTAS TRON

| Herramienta | Skills Relacionadas | Uso |
|-------------|---------------------|-----|
| **ini** | skill-inicializacion, skill-creator | Publicar scripts en `/usr/bin` |
| **repo** | Todas (auditoría) | Verificar cambios con `repo status` |
| **ares gs** | skill-sesion, skill-session-management | Guardar/restaurar sesiones de trabajo |
| **com** | Todas (inspección) | Ver código fuente de programas |

---

## ⚡ PRINCIPIOS DE USO

1. **Carga Bajo Demanda:** Solo leer la skill necesaria para la tarea actual
2. **Scripts como Black Boxes:** Usar directamente, no leer source sin necesidad
3. **Progressive Disclosure:** SKILL.md → scripts/ → references/ → assets/
4. **Zero Formula Errors:** En office/doc-processing, siempre verificar outputs
5. **Licencias Incluidas:** Todos los assets tienen LICENSE.txt u OFL correspondiente

---

*Este índice es la puerta de entrada al arsenal completo de ARES. Cada skill es un módulo de conocimiento procedimental listo para ejecutar.*

**Última actualización:** Marzo 2025 | **Versión:** 2.0 | **Total Skills:** 18

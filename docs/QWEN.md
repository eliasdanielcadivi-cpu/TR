# 🧠 ARES - CONTEXTO PARA QWEN (v2.0)

## 🗺️ MAPA DE CARPETAS
- `/src`: Orquestador (`main.py`). NO tocar lógica de módulos aquí.
- `/modules`: Especialistas atómicos (Máx 3 funciones).
- `/config`: Soberanía de configuración (`config.yaml`).
- `/bin`: Binarios externos y scripts Bash.
- `/docs/skills/`: **Arsenal completo de Kung-Fu IA** — 18 skills, 367 archivos, 9.6 MB.

## ⚙️ INFRAESTRUCTURA (INI & REPO)
- `ini`: Gestiona entornos `uv` (`ini venv`) y publica en `/usr/bin` (`ini prod`).
- `repo`: Auditoría de cambios (`repo status`) y alcance (`repo audit <modulo>`).

## 🚨 PROTOCOLO DE EDICIÓN (CIRUJANO)
1. **Identificar:** Leer el módulo especialista.
2. **Editar:** Solo el archivo relevante.
3. **Auditar:** Ejecutar `repo status` para verificar que no hubo "salpicaduras".
4. **Respetar:** El directorio de trabajo (`PWD`) del usuario siempre es soberano.

## 📄 DOCUMENTACIÓN
- `LEEME.md`: Fuente de verdad de lo que está FUNCIONANDO.
- `INDEX.md`: Catálogo de módulos.
- `docs/skills/INDEX.md`: **Índice maestro exhaustivo** — 18 skills clasificadas con scripts, referencias y assets.

## 🚀 CÓMO APRENDER KUNG-FU (SKILLS)

### Índice Central
👉 **`docs/skills/INDEX.md`** — Punto de entrada único. Contiene:
- Tabla de resumen (8 categorías, 367 archivos, 9.6 MB)
- Clasificación completa por categoría
- Detalle de cada skill (scripts, referencias, assets, triggers)
- Estructura de carpetas completa (tree)
- Estadísticas del arsenal

### Categorías Disponibles
| Categoría | Ruta | Skills | Archivos | Scripts |
|-----------|------|--------|----------|---------|
| **ARES Core** | `docs/skills/` | inicializacion, sesion, session-management | 3 | 0 |
| **Desarrollo** | `docs/skills/dev/` | mcp-builder, webapp-testing, frontend-design, web-artifacts-builder | 45 | 12 |
| **Doc-Processing** | `docs/skills/doc-processing/` | docx, pdf | 85 | 18 |
| **Office** | `docs/skills/office/` | pptx, xlsx | 95 | 15 |
| **Multimedia** | `docs/skills/multimedia/` | algorithmic-art, slack-gif-creator | 25 | 8 |
| **IA** | `docs/skills/ia/` | skill-creator | 12 | 3 |
| **Comms** | `docs/skills/comms/` | internal-comms | 6 | 0 |
| **Design** | `docs/skills/design/` | brand-guidelines, canvas-design, theme-factory | 95 | 0 |

### Flujo de Uso
1. Leer `INDEX.md` completo para entender el arsenal disponible
2. Identificar categoría y skill específica
3. Leer `SKILL.md` de la skill (punto de entrada)
4. Usar scripts bajo demanda (`scripts/`, `reference/`, `assets/`)

### Principio de Carga Mínima
Solo cargar la skill necesaria para la tarea actual. Las skills están diseñadas para cargarse bajo demanda (progressive disclosure).

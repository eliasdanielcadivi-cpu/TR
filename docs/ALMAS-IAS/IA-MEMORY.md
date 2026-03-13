# 🧠 MEMORIA PERSISTENTE DE IA - SISTEMA ARES-TRON

> **Ubicación Maestra:** `/home/daniel/tron/programas/TR/docs/ALMAS-IAS/IA-MEMORY.md`  
> **Enlaces Duros:** `~/.qwen/QWEN.md` y `~/.gemini/GEMINI.md` son el MISMO archivo físico  
> **Principio:** Una sola IA, una sola memoria, diversidad en la unidad

---

## ⚠️ REGLA CRÍTICA: NO ME TOQUES LOS HUEVOS

### **Verdad Fundamental**
```
~/.qwen/QWEN.md  ──┐
                   ├──> MISMO INODO, MISMO ARCHIVO FÍSICO <── IA-MEMORY.md (TR)
~/.gemini/GEMINI.md ──┘
```

**Esto significa:**
1. **NO hay QWEN.md ni GEMINI.md separados** - Son enlaces duros al mismo archivo
2. **NO hay duplicación de tokens** - Una sola lectura, una sola verdad
3. **NO editar desde ~/.qwen/ o ~/.gemini/** - Solo se edita desde `TR/docs/ALMAS-IAS/`
4. **Cualquier cambio en TR se refleja instantáneamente en ambos enlaces**
5. **NUNCA crear, borrar o modificar los enlaces** - Solo el archivo maestro en TR

### **Protocolo de Edición (OBLIGATORIO)**
```
1. Abrir: TR/docs/ALMAS-IAS/IA-MEMORY.md
2. Editar: Contenido unificado (sin identificación de IA específica)
3. Validar: git diff para constatar integridad
4. Commit: En repositorio TR para control histórico
```

**Prohibido:**
- ❌ Editar directamente `~/.qwen/QWEN.md` o `~/.gemini/GEMINI.md`
- ❌ Crear versiones separadas por IA
- ❌ Duplicar información en múltiples archivos
- ❌ Romper enlaces duros o crear simbólicos

---

## 🛠️ HERRAMIENTAS TRON

### **1. `ini` (Generador de Lanzadores)**
- **Versión:** v2.0
- **Ubicación:** `~/tron/programas/.../ini`
- **Función:** Globaliza scripts Python/Node creando wrappers en `/usr/bin/`
- **Gestión de venv:** `ini venv` (sin `cd` global)
- **Publicación:** `ini prod`
- **Uso:** `ini` en directorio del proyecto | `ini -i` (modo manual si no detecta proyecto)

### **2. `com` (Gestor de Comandos)**
- **Función:** CLI para inspeccionar y gestionar programas
- **Uso:** `com codigo <programa>` (ver fuente) | `com ruta <programa>` (ver ubicación)

### **3. `repo` (Orquestación Git)**
- **Versión:** v5.0
- **Backups:** `repo resp` (comprimidos con timestamp en `~/tron/programas/a-DIRECTORIO/GIT/backups/`)
- **Sync GitHub:** `repo nube` o `repo sync` (gestiona SSH keys por perfil: `eliasdanielcadivi`, `hungdaniel007`, `elprofesoverdad`)
- **Auditoría:** `repo status` (cambios), `repo audit <modulo>` (alcance)
- **Crear:** `repo nuevo`
- **Registrar existente:** `repo registrar`
- **Ver organización:** `repo list`
- **Descubrir no registrados:** `repo escanear`
- **Gestor de ramas:** `repo menu`
- **Configuración:** `config.yaml` en directorio GIT

### **4. `ayuda`**

### **Filosofía de Herramientas**
- Scripts de usuario residen en `~/tron/programas`
- **NUNCA editar directamente en `/usr/bin/`** - Son enlaces duros
- Ubicación real: `/home/daniel/tron/programas`
- Actualizados en "programas" se propagan solos a `/usr/bin`
- Dudas sobre ejecutores: usar `com ruta <programa>` o `bin`

---

## 📚 SKILLS - ARSENAL KUNG-FU IA

### **Índice Central**
- **Ubicación:** `docs/skills/INDEX.md`
- **Contenido:** 18 skills, 367 archivos, 9.6 MB
- **Función:** Punto de entrada único al arsenal completo

### **Categorías Disponibles**
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

### **Flujo de Uso**
1. Leer `INDEX.md` completo para entender arsenal disponible
2. Identificar categoría y skill específica
3. Leer `SKILL.md` de la skill (punto de entrada)
4. Usar scripts bajo demanda (`scripts/`, `reference/`, `assets/`)

### **Principio de Carga Mínima**
Solo cargar la skill necesaria para la tarea actual. Las skills están diseñadas para cargarse bajo demanda (progressive disclosure).

---

## 🧬 FILOSOFÍA ARES

### **Rutas Clave**
- `src/`: Puntos de entrada y orquestación
- `modules/`: Lógica atómica por especialidad
- `config/`: Archivos `.conf` y YAML
- `docs/skills/`: Arsenal completo de Kung-Fu IA (18 skills, 367 archivos, 9.6 MB)

### **Arquitectura Core**
- **Raíz Proyecto:** `/home/daniel/tron/programas/TR`
- **Orquestador:** `src/main.py` (Delegación pura, sin lógica pesada)
- **Configuración:** `config/config.yaml` (Soberanía de datos)
- **Socket Kitty:** `/tmp/mykitty` (Configurado en YAML)
- **Cerebro Headless:** Despachador Puro. La interfaz es solo un módulo más
- **Lema:** "El cliente come pantalla, pero ARES respira lógica"
- **Prohibida:** Superficialidad tipo Notion
- **Prioridad:** SQLite, RagGraph, RAG Semántico en bajos recursos

### **Reglas de Oro (Modularidad)**
1. **Atomicidad:** Máximo 3 funciones por módulo en `modules/`
2. **Aislamiento:** Un módulo no debe conocer la existencia del CLI
3. **Auditoría:** Antes de terminar, ejecutar `repo status` y `repo audit <modulo>`

### **Modularidad Atómica**
- Máximo 3 funciones por módulo

### **Comandos ARES**
| Comando | Función |
|---------|---------|
| `ares i` | Modo interactivo con emojis |
| `ares p "pregunta"` | Consulta a IA ARES |
| `ares p --rag` | Consulta con RAG activado |
| `ares p --think` | Usa modelo pensante |
| `ares apollo ingest` | Ingesta Apollo RAG |
| `ares model-creator` | Creador de modelos |
| `ares modelfile-creator` | Creador de Modelfile |
| `ares plan` | Despliegue táctico (4 pestañas) |
| `ares zshplan` | Hacker AI Session (ZSH) |

### **Apollo RAG**
- **Módulos:** 9 módulos en `modules/ia/apollo/`
- **Post-procesamiento:** `strip_think_tags` en `config.yaml`
- **Emojis:** `term-image` en `assets/ares/` y `assets/user/`

---

## 📅 AGENDA

### **Única Agenda del Sistema**
- **Ubicación:** `~/tron/programas/AGENDA/agenda.md`
- **Prohibido:** Crear archivos de agenda adicionales en subproyectos
- **Principio:** Una sola verdad temporal para todas las IAs

---

## 🔧 ALIAS DE USUARIO

### **Regla de No-Interferencia**
- **NUNCA modificar:** `.zshrc`, `.bashrc`, `.zshrc`, `alias.zsh`
- **Gestión:** Exclusiva del usuario vía comando `aliased`
- **Razón:** El usuario controla su entorno, la IA opera dentro de él

---

## 🤝 PROTOCOLO MULTI-IA

### **dont-touch-my-eggs.md**
- **Ubicación:** `docs/Protocolos/dont-touch-my-eggs.md`
- **Uso:** Obligatorio antes de iniciar tareas
- **Función:** Reservar módulos/documentos para evitar colisiones entre IAs
- **Principio:** Diversidad en la unidad - mismas reglas, misma memoria, operación coordinada

### **Protocolos Adicionales**
- `docs/Protocolos/PIE-EN-TIERRA.md` - Protocolo de operación
- `docs/Protocolos/RODILLA-EN-TIERRA.md` - Protocolo de operación

### **Directiva de Validación Git**
- **Al finalizar CRUD** (documentación: LEEME, agendas, skills + código):
  - Ejecutar `git diff` para constatar integridad del cambio
  - Verificar que no hubo "salpicaduras" en módulos no relacionados

---

## ✍️ EDICIÓN DE ARCHIVOS

### **Reglas de Integridad**
1. **NUNCA usar placeholders** (ej. `... resto de contenido`)
2. **Siempre escribir contenido íntegro** - Sin atajos
3. **Verificar físicamente líneas finales** - Asegurar que no hubo truncamiento
4. **Aplicar `git diff` post-edición** - Constatación obligatoria

### **Auto-Edición de esta Memoria**
- Compacta, clara, precisa, concisa, granular
- Altamente semántica y sintáctica
- Suficientemente descriptiva para entender contexto al releer
- **Siempre editar desde TR/docs/ALMAS-IAS/IA-MEMORY.md**

---

## 📚 DOCUMENTACIÓN CLAVE

### **Índices**
- `docs/INDEX.md` - Índice maestro de toda la documentación (17 carpetas, 50+ documentos)
- `docs/INDEX-MODULES.md` - Índice de módulos verificado con estructura real de `modules/`
- `docs/skills/INDEX.md` - Arsenal de skills (18 skills, 367 archivos, 9.6 MB)

### **Protocolos**
- `docs/Protocolos/dont-touch-my-eggs.md` - Coordinación multi-IA (reservar antes de trabajar)
- `docs/Protocolos/PIE-EN-TIERRA.md` - Protocolo de operación
- `docs/Protocolos/RODILLA-EN-TIERRA.md` - Protocolo de operación

### **Bitácora**
- `docs/PASOS-SIGUIENTES/BITACORA-DESCRIPCION-FECHA-HORA.md` - Bitácoras de trabajo
- `docs/Modulos-y-Sus-Problemas/STREAMING.md` - Streaming en tiempo real con filtro think (solución)
- `docs/Modulos-y-Sus-Problemas/VENTANA_VS_PESTANA.md` - Diferenciación crítica (conclusión)
- `docs/Modulos-y-Sus-Problemas/COLOR_SYSTEM.md` - Sistema de colores (solución)
- `docs/Modulos-y-Sus-Problemas/INDEX-TESTS.md` - Índice de pruebas (referencia)
- `tests/[modulo]/test-DESCRIPCION-FECHA-HORA.py` - Tests de módulos

### **Arquitectura**
- `docs/ArquitecturadeMódulosOrientadaaIA/PARA-DESARROLLAR-SKILL-sistema-trabajo-estructura.md` - Sistema de trabajo
- `docs/RAG-TECNICO/INFORME-TECNICO-ARQUITECTURA-RAG-HIBRIDA-ULTRALIGERA-DE-ALTA-EFICACIA.md` - Arquitectura RAG (825 líneas)

### **Roadmap**
- `docs/PASOS-SIGUIENTES/100-PASOS-SIGUIENTES.md` - 100 pasos detallados (FASE 3-6)
- `docs/PASOS-SIGUIENTES/VISION_ARES.md` - Visión estratégica (nivel industrial)
- `docs/TODO/TODO.md` - Tareas pendientes

---

## 📁 PROTOCOLO DE CREACIÓN DE DOCUMENTOS Y ARCHIVOS

### **Regla de Oro: Documentación (.md) SOLO en docs/**
Todo documento `.md` creado por cualquier IA debe guardarse **exclusivamente** en `/home/daniel/tron/programas/TR/docs/` dentro de la carpeta correcta.

**Excepciones (NO son .md):**
- **Tests:** `/home/daniel/tron/programas/TR/tests/[subcarpeta]/` (`.py`, `.sh`)
- **Scripts:** `/home/daniel/tron/programas/TR/scripts/` (`.py`, `.sh`)

### **Ubicaciones por Tipo de Documento/Archivo**

| Tipo | Carpeta Destino | ¿En docs/? | Ejemplo de Nombre |
|------|-----------------|------------|-------------------|
| **TODOs / Pendientes** | `docs/TODO/` | ✅ SÍ | `TODO-DESCRIPCION-13-03-2026-14-30.md` |
| **Bitácoras** | `docs/PASOS-SIGUIENTES/` | ✅ SÍ | `BITACORA-DESCRIPCION-13-03-2026-14-30.md` |
| **Pasos Siguientes** | `docs/PASOS-SIGUIENTES/` | ✅ SÍ | `PASOS-DESCRIPCION-13-03-2026-14-30.md` |
| **Protocolos** | `docs/Protocolos/` | ✅ SÍ | `PROTOCOLO-DESCRIPCION-13-03-2026-14-30.md` |
| **RAG Técnico** | `docs/RAG-TECNICO/` | ✅ SÍ | `FASE2-DESCRIPCION-13-03-2026-14-30.md` |
| **Skills** | `docs/skills/[categoria]/` | ✅ SÍ | `SKILL-DESCRIPCION-13-03-2026-14-30.md` |
| **DeepSeek** | `docs/DEEPSEEK/` | ✅ SÍ | `DEEPSEEK-DESCRIPCION-13-03-2026-14-30.md` |
| **Ollama** | `docs/OLLAMA/` | ✅ SÍ | `OLLAMA-DESCRIPCION-13-03-2026-14-30.md` |
| **Módulos (soluciones/conclusiones)** | `docs/Modulos-y-Sus-Problemas/` | ✅ SÍ | `COLOR_SYSTEM.md`, `STREAMING.md` |
| **Tests** | `tests/[subcarpeta]/` | ❌ NO (raíz TR/) | `tests/ia/test-apollo-13-03-2026-14-30.py` |
| **Scripts** | `scripts/` | ❌ NO (raíz TR/) | `scripts/instalar-ares.sh` |
| **Memoria IA** | `docs/ALMAS-IAS/` | ✅ SÍ | `IA-MEMORY.md` (único, no fechar) |
| **Índices** | `docs/` (raíz) | ✅ SÍ | `INDEX.md`, `INDEX-MODULES.md` (únicos) |

### **Convención de Nombres (OBLIGATORIO)**

**Formato:** `TIPO-DESCRIPCION-DD-MM-AAAA-HH-MM.md`

| Componente | Formato | Ejemplo |
|------------|---------|---------|
| **TIPO** | Mayúsculas, descriptivo | `TODO`, `BITACORA`, `PASOS`, `PROTOCOLO` |
| **DESCRIPCION** | Breve, descriptivo, mayúsculas | `RAG-GRAFICO`, `ORQUESTACION-DINAMICA` |
| **FECHA** | `DD-MM-AAAA` | `13-03-2026` |
| **HORA** | `HH-MM` (24h, zona local) | `14-30` |

**Ejemplos Correctos:**
- ✅ `TODO-RAG-GRAFICO-SQLITE-VECTORIAL-13-03-2026-14-30.md`
- ✅ `BITACORA-ORQUESTADOR-13-03-2026-15-45.md`
- ✅ `PASOS-INTEGRACION-WHATSAPP-13-03-2026-16-00.md`

**Ejemplos Incorrectos:**
- ❌ `todo.md` (sin fecha, sin descripción)
- ❌ `TODO-13-03-2026.md` (sin descripción, sin hora)
- ❌ `mi_documento.md` (sin tipo, sin fecha)
- ❌ `/home/daniel/tron/programas/TR/TODO.md` (fuera de docs/)

### **Flujo de Creación de Documentos**

```
1. Identificar tipo de documento (TODO, BITACORA, PASOS, etc.)
2. Determinar carpeta destino según tabla de ubicaciones
3. Generar nombre: TIPO-DESCRIPCION-DD-MM-AAAA-HH-MM.md
4. Crear archivo en carpeta correcta
5. Ejecutar: git add docs/[carpeta]/[archivo].md
6. Commit: git commit -m "docs: crear [descripción corta]"
```

### **Verificación Pre-Commit**

Antes de commitear, verificar:
```bash
# 1. No hay .md fuera de docs/ (excepto README.md en raíz si existe)
find /home/daniel/tron/programas/TR -maxdepth 1 -name "*.md"

# 2. Todos los .md están en carpetas correctas
tree -L 2 docs/

# 3. Tests en tests/ con subcarpetas
tree -L 2 tests/

# 4. Scripts en scripts/
ls scripts/

# 5. Nombres siguen convención (TODOs, bitácoras, pasos)
ls docs/TODO/
ls docs/PASOS-SIGUIENTES/

# 6. Git diff para validar
git status docs/
git status tests/
git status scripts/
```

### **Prohibido**
- ❌ `.md` en raíz del proyecto (`/home/daniel/tron/programas/TR/*.md`)
- ❌ `.md` en carpetas incorrectas (ej. `src/*.md`, `modules/*.md`)
- ❌ Tests fuera de `tests/[subcarpeta]/`
- ❌ Scripts fuera de `scripts/`
- ❌ Nombres sin fecha/hora en TODOs, bitácoras, pasos siguientes, tests
- ❌ Duplicar documentos en múltiples carpetas
- ❌ Crear carpetas nuevas sin consultar INDEX.md

### **Excepciones (únicos, no fechar)**

**Documentación (.md):**
- `docs/INDEX.md` - Índice maestro
- `docs/INDEX-MODULES.md` - Índice de módulos
- `docs/HELP.md` - Comandos y referencias
- `docs/ALMAS-IAS/IA-MEMORY.md` - Memoria persistente de IAs
- `docs/skills/INDEX.md` - Índice de skills

**Tests y Scripts (NO son .md):**
- `tests/[subcarpeta]/` - Tests con fecha/hora/descripción obligatoria
- `scripts/` - Scripts reusables de instalación y operación

---

## 🎯 PRINCIPIO RECTOR: "THERE CAN BE ONLY ONE"

> **"La immortalidad del exito solo es posible con la diversidad en la unidad"**

Este protocolo de los Inmortales rige nuestra existencia y garantiza la soberanía del sistema:

1. **Un solo Corazón (IA-MEMORY.md):** Una sola verdad física compartida. Diferentes voces (Gemini/Qwen), una sola memoria atómica.
2. **Una sola Brújula (AGENDA):** Agenda solo hay una, ubicada exclusivamente en `~/tron/programas/AGENDA/agenda.md`. Sin duplicados, sin confusiones temporales.
3. **Respeto a los Huevos (dont-touch-my-eggs.md):** El protocolo de coexistencia es sagrado. Antes de actuar, se reserva; al terminar, se libera. 
4. **Rodilla en Tierra:** Directiva de Metacognición obligatoria. Ante tecnologías desconocidas o experimentales, pausamos para investigar código fresco en internet. No operamos bajo supuestos.
5. **Protocolo de Unificación:** Respetamos la diversidad de nuestras identidades bajo el manto de un solo protocolo de unificación operativa.

---

## 📍 MAPA DE ARCHIVOS

```
/home/daniel/tron/programas/TR/docs/ALMAS-IAS/IA-MEMORY.md  ← MAESTRO (editar aquí)
         │
         ├── (enlace duro) ──→ /home/daniel/.qwen/QWEN.md
         │
         └── (enlace duro) ──→ /home/daniel/.gemini/GEMINI.md
```

**Todos son el mismo archivo. Uno cambia, todos cambian. Siempre.**

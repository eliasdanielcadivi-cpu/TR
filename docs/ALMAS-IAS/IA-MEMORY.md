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
- **Ubicación:** `TR/docs/Protocolos/dont-touch-my-eggs.md`
- **Uso:** Obligatorio antes de iniciar tareas
- **Función:** Reservar módulos/documentos para evitar colisiones entre IAs
- **Principio:** Diversidad en la unidad - mismas reglas, misma memoria, operación coordinada

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

## 🎯 PRINCIPIO RECTOR: "THERE CAN BE ONLY ONE"

> **"La immortalidad del exito solo es posible con la diversidad en la unidad"**

Este protocolo de los Inmortales rige nuestra existencia y garantiza la soberanía del sistema:

1. **Un solo Corazón (IA-MEMORY.md):** Una sola verdad física compartida. Diferentes voces (Gemini/Qwen), una sola memoria atómica.
2. **Una sola Brújula (AGENDA):** Agenda solo hay una, ubicada exclusivamente en `~/tron/programas/AGENDA/agenda.md`. Sin duplicados, sin confusiones temporales.
3. **Respeto a los Huevos (dont-touch-my-eggs.md):** El protocolo de coexistencia es sagrado. Antes de actuar, se reserva; al terminar, se libera. 
4. **Protocolo de Unificación:** Respetamos la diversidad de nuestras identidades (memorias de procesamiento) bajo el manto de un solo protocolo de unificación operativa.

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

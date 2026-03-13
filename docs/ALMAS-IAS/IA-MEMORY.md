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
- **Ubicación:** `~/tron/programas/.../ini`
- **Función:** Globaliza scripts Python/Node creando wrappers en `/usr/bin/`
- **Uso:** `ini` en directorio del proyecto | `ini -i` (modo manual si no detecta proyecto)

### **2. `com` (Gestor de Comandos)**
- **Función:** CLI para inspeccionar y gestionar programas
- **Uso:** `com codigo <programa>` (ver fuente) | `com ruta <programa>` (ver ubicación)

### **3. `repo` (Orquestación Git)**
- **Backups:** `repo resp` (comprimidos con timestamp en `~/tron/programas/a-DIRECTORIO/GIT/backups/`)
- **Sync GitHub:** `repo nube` o `repo sync` (gestiona SSH keys por perfil: `eliasdanielcadivi`, `hungdaniel007`, `elprofesoverdad`)
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

## 🧬 FILOSOFÍA ARES

### **Arquitectura**
- **Cerebro Headless:** Despachador Puro. La interfaz es solo un módulo más
- **Lema:** "El cliente come pantalla, pero ARES respira lógica"
- **Prohibida:** Superficialidad tipo Notion
- **Prioridad:** SQLite, RagGraph, RAG Semántico en bajos recursos
- **Modularidad Atómica:** Máximo 3 funciones por módulo

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
- **Ubicación:** Raíz del proyecto (`TR/dont-touch-my-eggs.md`)
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

## 🎯 PRINCIPIO RECTOR

> **"1 Programador, 1 IA, actuando al unísono"**

- **Diversidad en la Unidad:** Mismas reglas, misma memoria, coordinación perfecta
- **No Pisarse los Huevos:** Protocolo `dont-touch-my-eggs.md` + validación git
- **Soberanía Tecnológica:** Herramientas TRON como base del sistema ARES

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

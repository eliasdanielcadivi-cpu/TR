# 🛰️ GEMINI - MEMORIA PERSISTENTE (Alma de IA)

> **Ubicación Original:** `/home/daniel/.gemini/GEMINI.md`
> **Propósito:** Conocimiento compartido para operación en igualdad de condiciones con Qwen
> **Actualización:** Sincronización bidireccional con QWEN-MEMORY.md

---

## **Herramientas TRON**
1. **`ini`** (Generador de Lanzadores): Script Python en `~/tron/programas/.../ini`. Globaliza scripts Python/Node creando wrappers en `/usr/bin/`. Uso: `ini` en directorio del proyecto, o `ini -i` (modo manual).
2. **`com`** (Gestor de Comandos): CLI para inspeccionar programas. Uso: `com codigo <programa>` (ver fuente), `com ruta <programa>` (ver ubicación).
3. **`repo`** (Orquestación Git): 
   - `repo resp` → backups comprimidos con timestamp
   - `repo nube` / `repo sync` → subir a GitHub gestionando SSH keys por perfil: `eliasdanielcadivi`, `hungdaniel007`, `elprofesoverdad`
   - `repo nuevo` → crear repositorio
   - `repo registrar` → añadir existente
   - `repo list` → ver organización
   - `repo escanear` → descubrir no registrados
   - `repo menu` → gestor de ramas interactivo
   - **Backups:** `~/tron/programas/a-DIRECTORIO/GIT/backups/`
   - **Config:** `config.yaml` en mismo directorio
4. **`ayuda`**

**Filosofía:** Scripts de usuario en `~/tron/programas`, nunca se editan directamente en `/usr/bin`. Ubicación real: `/home/daniel/tron/programas`. Enlaces duros a `/usr/bin`, actualizados en "programas" se propagan solos. Dudas sobre ejecutores: usar `bin`.

---

## **Filosofía ARES**
- **Cerebro Headless:** Despachador Puro. Interfaz es módulo más ('cliente come pantalla', ARES respira lógica).
- **Prohibida:** Superficialidad tipo Notion.
- **Prioridad:** SQLite, RagGraph, RAG Semántico en bajos recursos.
- **Arquitectura modular atómica:** Máximo 3 funciones por módulo.

**Comandos ARES:**
- `ares i` → Interactivo con emojis
- `ares p --rag` → Consulta con RAG
- `ares p --think` → Usa modelo pensante
- `ares apollo ingest` → Ingesta Apollo RAG
- `ares model-creator` → Creador de modelos
- `ares modelfile-creator` → Creador de Modelfile

**Apollo RAG:** 9 módulos en `modules/ia/apollo/`. Post-procesamiento: `strip_think_tags` en `config.yaml`. Emojis con `term-image` en `assets/ares/` y `assets/user/`.

---

## **Agenda**
- **Única en todo el sistema:** `~/tron/programas/AGENDA/agenda.md`
- **Prohibido:** Crear archivos de agenda adicionales en subproyectos

---

## **Alias**
- **NUNCA modificar:** `.zshrc`, `.bashrc`, `alias.zsh`
- **Gestión:** Exclusiva del usuario vía comando `aliased`

---

## **Protocolo Multi-IA (dont-touch-my-eggs.md)**
- **Ubicación:** Raíz del proyecto
- **Uso:** Obligatorio antes de iniciar tareas para reservar módulos/documentos y evitar colisiones

---

## **Directiva de Validación Git**
- **Al finalizar CRUD** (documentación: LEEME, agendas, skills + código): Ejecutar `git diff` para constatar integridad del cambio

---

## **Edición de Archivos**
- **NUNCA usar placeholders** (ej. '... resto de contenido')
- **Siempre:** Escribir contenido íntegro, verificar físicamente líneas finales para asegurar integridad
- **Post-edición:** Aplicar `git diff` como constatación obligatoria

---

## **Auto-Edición de Memoria**
- Compacta, clara, precisa, concisa, granular, altamente semántica y sintáctica
- Suficientemente descriptiva para entender contexto y razón al releer

---

## **Sincronización**
- **Qwen Memory:** `/home/daniel/.qwen/QWEN.md`
- **TR Repo:** `/home/daniel/tron/programas/TR/docs/ALMAS-IAS/QWEN-MEMORY.md`
- **Control de Versiones:** Este archivo está bajo Git en TR

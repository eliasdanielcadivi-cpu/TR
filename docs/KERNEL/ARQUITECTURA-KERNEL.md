# 🏛️ ARQUITECTURA DEL KERNEL ARES-TRON (V1.1)

El **Kernel** es el sistema operativo lógico que orquesta la inteligencia, la memoria y la ejecución de software en el ecosistema ARES-TRON. No es un binario estático, sino un conjunto de leyes y herramientas dinámicas que garantizan el **Agnosticismo Estructural**.

## 🛡️ LOS 5 PILARES DEL KERNEL

### 1. BIOS DINÁMICO (`sys_kernel.py`)
- **Propósito:** Resolución de símbolos y conciencia de ubicación.
- **Funcionalidad:** Detecta automáticamente el `@ROOT` del proyecto actual (subiendo por el árbol hasta encontrar `LEEME.md`).
- **Agnosticismo:** Permite que la misma lógica funcione en `TR`, `AGENDA`, o cualquier sub-agente sin cambiar el código.
- **Resolución de Símbolos:** Mapea alias como `@SKILLS`, `@TODO`, y `@MODULES` a rutas físicas reales.

### 2. MEMORIA UNIFICADA (`IA-MEMORY.md`)
- **Propósito:** Persistencia de contexto y axiomas globales.
- **Mecanismo:** Enlaces duros (`hard-links`) que conectan `~/.gemini/GEMINI.md` y `~/.qwen/QWEN.md` `~/.claude/CLAUDE.md` al mismo inodo físico.
- **Verdad Única:** Cualquier IA que entre al sistema lee la misma "alma", evitando la fragmentación de conocimiento.

### 3. ENRUTAMIENTO SEMÁNTICO (`INDEX.dsl.md` & Routers)
- **Propósito:** Despacho de intenciones basado en "Caps" (Capacidades) y "Triggers" (Disparadores).
- **Jerarquía:** 
  - **L0:** Índice Maestro (Categorías).
  - **L1:** Routers de Categoría (core, dev, ia, etc.).
  - **L2:** Skills (Lógica procedural).

### 4. ARSENAL DE SKILLS (Lógica Procedural DSL)
- **Propósito:** Definir el "Saber Hacer" del sistema.
- **Regla de Oro (Atomicidad):** Máximo 3 funciones por módulo. Si una tarea es compleja, se divide; si es trivial, se automatiza.
- **Formato DSL:** Basado en S-expressions y YAML para una lectura rápida por parte de la IA y mantenibilidad humana.

### 5. PROTOCOLO DE BLINDAJE (`skill-sys-config.dsl.md`)
- **Propósito:** Protección contra la entropía y errores de IA.
- **Acción:** Obliga a realizar respaldos (`.bak`) antes de cualquier edición en la configuración del sistema.
- **Validación:** Mandato de `git diff` post-operación para constatar que solo se cambió lo solicitado.

---

## 📂 ESTRUCTURA DE DIRECTORIOS (ESTÁNDAR TREE-L3)

Todo proyecto bajo el Kernel ARES debe seguir esta arquitectura paranoica:
- `bin/`: Lanzadores y binarios instalados vía `ini`, binarios o programas auxiliares del sistema.
- `config/`: Configuraciones estáticas (YAML/JSON).
- `db/`: Estado persistente y bases de datos.
- `docs`: Documanteción del sistema en subcarpetas y de los programas ayxiliares o dependencias estratégicas
- `docs/TODO/`: Zona de aterrizaje de planes (lógica secuencial temporal).
- `docs/skills/`: El arsenal de conocimiento.
- `src/`: El main orquetador y despachaor , corazón del sistema.
- `modules/`: Lógica funcional atómica.
- `scripts/`: Utilidades y automatizaciones.
- `papelera/`: Cementerio de módulos con contexto de recuperación.
- `tests/`: Validación experimental.
- `ÀGENTES`: contiene carpetas de  agentes o subagentes los subagentes pueden ser herramientas de los agentes. Contienen núcleos LLM (la carpeta se crea solo en caso de programas inteligentes)
- `scripts`: programas diversos del sistema, funciones de instalación o mantenimiento
- `herramientas`: programas especialmente diseñados para ser usados por ias, tambien pueden ser usados por humanos como comandos sin cabeza, no contienen núcleos LLM (la carpeta se crea solo en caso de programas inteligentes)
- `test`: pruebas a los programas, nunca se borran.
---

## 🔄 CICLO DE VIDA DEL SOFTWARE (ORQUESTADO POR `INI`)
1. **Init:** Estructuración del árbol.
2. **Dev:** Investigación SOTA -> Planificación -> Implementación Atómica.
3. **Maint:** Adaptación, limpieza o división de módulos.
4. **Prod:** Globalización en `/usr/bin` con wrappers blindados.

**Documentación Generada por el Kernel.**

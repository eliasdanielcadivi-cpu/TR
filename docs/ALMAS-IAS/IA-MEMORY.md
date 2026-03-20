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

---

## 📋 AGENDA DEL SISTEMA (ÚNICA)

**Ubicación:** `/home/daniel/tron/programas/AGENDA/agenda.md`  
**Comando:** `agenda` (alias para `uv run --quiet --project /home/daniel/tron/programas/AGENDA python /home/daniel/tron/programas/AGENDA/main.py`)  
**Base de datos:** `/home/daniel/tron/programas/AGENDA/` (SQLite u otro)

### ¿Qué es la Agenda del Sistema?

La **Agenda del Sistema** es el **documento maestro único** que mantiene información relevante pero concisa sobre las tareas de **TODOS los proyectos del sistema ARES-TRON**.

**Características:**
- **AI-OPERATED:** Diseñada para ser mantenida por IAs (Qwen/Gemini)
- **Estratégica + Táctica:** Planificación de alto nivel + tareas ejecutables
- **Histórico permanente:** Nada se elimina, se marca como completado
- **Trazable:** Cada tarea tiene contexto, objetivo, fase, prioridad

### Diferencia: SISTEMA vs PROYECTO

| Concepto | Definición | Ejemplo |
|----------|------------|---------|
| **SISTEMA** | El ecosistema completo ARES-TRON | Todos los proyectos interconectados |
| **PROYECTO** | Una unidad específica dentro del sistema | `Agente-De-Cambio-Estable`, `TR`, etc. |

**Jerarquía:**
```
SISTEMA ARES-TRON
├── PROYECTO: Agente-De-Cambio-Estable
│   ├── Documentación: LEEME.md, TODO-001, etc.
│   ├── Código: modules/, apps/
│   └── Agenda local: docs/CLAVE/estado.md (sincronizado con agenda.md)
├── PROYECTO: TR
│   ├── Documentación: docs/
│   └── Módulos: modules/
└── PROYECTO: Otros
```

### ¿Dónde se guarda la información?

| Tipo de Información | Ubicación |
|---------------------|-----------|
| **Agenda del Sistema** | `/home/daniel/tron/programas/AGENDA/agenda.md` |
| **Memoria de IA** | `/home/daniel/tron/programas/TR/docs/ALMAS-IAS/IA-MEMORY.md` |
| **Estado del Proyecto** | `/path/to/proyecto/docs/CLAVE/estado.md` |
| **Bitácora del Proyecto** | `/path/to/proyecto/docs/CLAVE/BITACORA.md` |

**Flujo de información:**
```
Agenda del Sistema (agenda.md)
    ↓ (sincroniza tareas relevantes)
Estado del Proyecto (estado.md)
    ↓ (documenta cambios)
Bitácora del Proyecto (BITACORA.md)
```

### Enlaces Duros de Memoria

```
~/.qwen/QWEN.md  ──┐
                   ├──> /home/daniel/tron/programas/TR/docs/ALMAS-IAS/IA-MEMORY.md
~/.gemini/GEMINI.md ──┘
```

**Esto significa:**
- Qwen y Gemini comparten la MISMA memoria
- Una sola lectura, una sola verdad
- Editar SIEMPRE desde `TR/docs/ALMAS-IAS/IA-MEMORY.md`
- Los cambios se reflejan instantáneamente en ambos enlaces

---

## 🔬 OBSERVACIÓN TÉCNICA: ENTROPÍA DE REFALIZACIÓN (NUEVA DIRECTIVA)

**Problema (Entropic Refactoring Drift):** Durante procesos de modularización o refactorización de alto nivel, la IA tiende a priorizar la elegancia del código (lógica sintáctica) sobre la fidelidad del pixel (constantes geométricas), provocando "desviaciones interpretativas" que destruyen maquetaciones estables.

**Para evitar:** La pérdida de "Cosas Buenas" visuales al cambiar el paradigma estructural.

**Directiva-Solución (Inmutabilidad Geométrica & Decoupling):**
1. **Decoupling de Estado:** El estado volátil (índices, contadores) NUNCA debe guardarse en archivos de configuración (YAML). Debe residir en archivos de estado volátiles (`.tmp`, `.json` en cache).
2. **Soberanía del Usuario:** Los archivos de configuración son de solo lectura para la IA, a menos que se solicite explícitamente una modificación.
3. **Traducción Literal:** Al encapsular lógica visual en fábricas o clases, las fórmulas matemáticas de posicionamiento deben copiarse de forma LITERAL, sin re-interpretación ni "mejoras" no solicitadas.

---

## 🛠️ HERRAMIENTAS TRON

### INI v3.0 - Orquestador de Ciclo de Vida

**Ubicación:** `/usr/bin/ini` (instalado) | `/home/daniel/tron/programas/a-DIRECTORIO/generador-de-lanzadores-python-encapsulados/ini` (fuente)

**Propósito:** Gestor de entornos y publicación de binarios con variables por proyecto.

**Comandos:**
| Comando | Descripción | Headless |
|---------|-------------|----------|
| `ini` | Modo interactivo completo (por defecto `prod`) | No |
| `ini init` | Crear nuevo proyecto Python con `pyproject.toml` | `-y` |
| `ini venv` | Inicializar entorno (.venv con uv o node_modules) | No |
| `ini prod` | Publicar binario en `/usr/bin` con wrapper bash | `-y` |
| `ini env` | Gestionar variables de entorno del proyecto | `-y` |
| `ini status` | Ver estado del proyecto y binarios | Sí |

**Archivos que genera/manipula:**
- `pyproject.toml` - Configuración de proyecto Python (UV)
- `.tron.env.json` - Variables de entorno y contadores genéricos por proyecto
- `/usr/bin/{comando}` - Wrapper bash con `TR_PROJECT_ROOT` inyectado

**Estructura de `.tron.env.json`:**
```json
{
  "project_name": "TR",
  "command_name": "ares",
  "variables": {
    "TR_ENV": "production",
    "TR_LOG_LEVEL": "info"
  },
  "generic_counters": {
    "counter_001": 0,
    "counter_002": 0
  }
}
```

**Flujo de Producción (`ini prod`):**
1. Detecta `pyproject.toml` o `package.json` (ofrece crear si no existe)
2. Escanea directorio buscando targets `.py` (raíz, `src/`, `modules/`)
3. Carga `.tron.env.json` para variables y nombre del comando
4. Valida nombre del binario (evita colisiones con `is_system_command()`)
5. Genera wrapper bash con variables inyectadas + `TR_PROJECT_ROOT`
6. Crea lanzador local en `bin/` (portátil)
7. Instala en `/usr/bin` con sudo
8. Verifica post-instalación y ofrece agregar al menú Openbox

**Características clave:**
- **CWD Sovereignty:** No hace `cd` global, respeta directorio del usuario
- **Variables por proyecto:** Cada proyecto tiene sus variables en `.tron.env.json`
- **Contadores genéricos:** Sistema automático de counters numerados (`counter_001`, `counter_002`...)
- **Soporte src/:** Búsqueda automática en `src/` y `modules/`
- **Rollback:** Limpia archivos temporales si falla la instalación
- **Headless completo:** Flag `-y` para automatización con IAs (sin preguntas)

**Ejemplo de wrapper generado:**
```bash
#!/bin/bash
# Generado por 'ini' v3.0
export TR_PROJECT_ROOT="/home/daniel/tron/programas/TR"
export TR_ENV="production"
export counter_001="0"
exec env -u VIRTUAL_ENV uv run --project "$TR_PROJECT_ROOT" python "$TR_PROJECT_ROOT/main.py" "$@"
```

---

(Resto de herramientas preservadas...)

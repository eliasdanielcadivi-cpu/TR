## NÚCLEO DE CREACIÓN DE SOFTWARE (KNOW-HOW ARES-TRON) - V2.1

### Reglas Absolutas de Desarrollo
- **Atomicidad Paranoica:** Máximo 3 funciones principales por archivo o módulo. La complejidad se resuelve mediante orquestación y división, jamás amontonando código.
- **Soberanía del Usuario y de Datos:** La IA tiene estrictamente prohibido decidir el paso a producción o ejecutar acciones destructivas sin la orden explícit (`confirmar=true`). Los parámetros de comportamiento (System Prompts, Modelos, Herramientas) deben ser inyectables y configurables, NUNCA hardcodeados.
- **Mandato No-Asunción (Fase Forense):** Queda prohibido programar parsers o lógica de integración para herramientas externas (CLIs, APIs) sin una captura física previa de su salida real (`stdout/stderr`) en archivos de prueba.
- **Preservación de Evidencias:** Jamás se borra código. Lo obsoleto se mueve a `papelera/` o `OLD/` con un archivo `NOTA.md` explicativo únicamente bajo orden humana.

### Metodología de Validación y Resiliencia
- **Protocolo de Snapshotting (No Borrado):** Versiones de scripts que alcancen hitos funcionales deben respaldarse físicamente (ej. `bridge-ok-v1.py`) como puntos de restauración inmediata.
- **Bucle de Autocorrección (Self-Repair Loop):** Los módulos que consuman salidas de IA deben implementar bucles de retroalimentación. Si una respuesta es inválida ("choreta"), el sistema debe interpelar al emisor con una "Nota de Arreglo" y exigir corrección antes de declarar fallo.
- **Protocolo de Resiliencia Industrial (7-Fails):** Todo motor crítico debe tener un contador de fallas. Al alcanzar el umbral (7), el sistema debe ejecutar auto-reparación autónoma (Update nativo o reinstalación nuclear vía curl).
- **Validación Post-CRUD:** Ejecución obligatoria de `git diff post_op` tras cualquier edición para garantizar integridad.

---

## CICLO DE VIDA DE DESARROLLO (FASES Y CASOS DETONADORES)

### Fase 1: Inicialización (INIT)
- **Caso Detonador:** El usuario ordena la creación de un nuevo proyecto o estructuración de directorio.
- **Know-How Operativo:** Despliegue de jerarquía Tree-L3. Creación obligatoria de `IA-CONTINUITY-REPORT.md` para transferencia de estado cognitivo entre sesiones de IA. Establecimiento de contratos iniciales (`LEEME.md`).

### Fase 2: Desarrollo (DEV)
- **Fase Forense Obligatoria:** Captura de datos reales antes de escribir lógica de negocio.
- **Planificación Temporal:** Antes de codificar, elaboración de TODO físico (`docs/TODO/TODO-$NAME.md`). Las tareas se agrupan en fases con temporalidad lógica inquebrantable.
- **Escritura Quirúrgica:** Construcción de módulos atómicos aplicando depuración máxima (verificación de sintaxis, resolución de imports).

### Fase 3: Mantenimiento (MAINT)
- **Adaptación y División:** Se interviene el código respetando la atomicidad. Si la lógica supera las 3 funciones, se divide en orquestador y submódulos.
- **Gestión de Papelera (Estricta):** El envío a `papelera/` incluye un archivo `NOTA.md` con el contexto del descarte.

### Fase 4: Producción y Despliegue (PROD)
- **Auditoría de Calidad:** Verificación de shebangs, permisos y ayuda interna funcional (`ares help`).
- **Globalización:** Uso de `ini prod` para publicación con soberanía de CWD.

---

## ANEXO ESPECIALIZADO: DESARROLLO DE IA Y AGENTES

### Soberanía de Identidad y Memoria
- **Mapeo Determinista:** Uso obligatorio de UUIDv5 para vincular nombres humanos (ej. "proyecto-x") a IDs de sesión de herramientas externas ("Cajas Negras").
- **Identidad Dinámica:** Los System Prompts deben cargarse desde archivos externos (.prompt) o parámetros posicionales, nunca grabados en el código.
- **Headless First:** La prioridad de salida en modo no-interactivo es el JSON puro y validado, compatible con `jq` y sistemas de automatización industrial.

---

## ESTRUCTURA PARANOICA DE DIRECTORIOS (TREE-L3)

Todo elemento tiene una ubicación lógica y explícita.

```text
{nombre_proyecto}/
├── config/                   # Configuración centralizada (prompts, layouts)
├── docs/
│   ├── skills/               # Capabilities ejecutables (.dsl.md)
│   ├── TODO/                 # Planes físicos por fases
│   └── RAG-V3/               # Informes de continuidad y contexto técnico
├── modules/                  # Módulos atómicos (max 3 funciones)
│   ├── core/                 # Lógica transversal
│   └── ia/                   # Adaptadores y Bridges de proveedores
├── AGENTES/                  # Sub-agentes LLM independientes
├── tests/                    # Capturas forenses y validaciones granulares
├── bin/                      # Bash Wrappers (uv run)
└── LEEME.md                  # Única fuente de verdad funcional
```

---

## SOBERANÍA DEL ENTORNO Y BASH WRAPPERS

Todo ejecutable en `bin/` local o `/usr/bin/` global debe ser un Bash Wrapper que utilice `uv run` para garantizar la soberanía del entorno y evitar errores de dependencias.

**Estándar de Wrapper:**
```bash
#!/bin/bash
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
exec uv run --project "$PROJECT_DIR" python "$PROJECT_DIR/src/main.py" "$@"
```

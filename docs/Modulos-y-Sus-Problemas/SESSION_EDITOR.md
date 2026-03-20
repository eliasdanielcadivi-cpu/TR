# Session Editor Module

## Propósito
Editor interactivo de sesiones guardadas en `db/*.json` para manipulación segura de configuraciones de sesiones Kitty.

## Ubicación
`/home/daniel/tron/programas/TR/modules/admon/session_editor.py`

## Funciones (Máximo 3 - Modularidad Atómica)

### 1. `load_session_file(ctx_obj, session_name)`
**Propósito:** Carga una sesión desde `db/{session_name}.json` con validación de existencia y parseo JSON.

**Args:**
- `ctx_obj`: Contexto ARES con `base_path`
- `session_name`: Nombre de la sesión (sin extensión)

**Returns:**
- `(data, error)`: Tupla con datos JSON o mensaje de error

**Errores posibles:**
- Sesión no encontrada
- JSON inválido
- Error de lectura

---

### 2. `save_session_file(ctx_obj, session_name, data)`
**Propósito:** Guarda una sesión con backup automático antes de escribir.

**Args:**
- `ctx_obj`: Contexto ARES con `base_path`
- `session_name`: Nombre de la sesión
- `data`: Datos JSON a guardar

**Returns:**
- `(success, message)`: Tupla de resultado

**Características:**
- Crea backup `.bak` antes de escribir
- Restaura backup automáticamente si falla la escritura
- Usa `json.dump` con indent=4 y ensure_ascii=False

---

### 3. `edit_session_interactive(ctx_obj, session_name)`
**Propósito:** Editor interactivo que abre el archivo JSON en el editor `micro`.

**Args:**
- `ctx_obj`: Contexto ARES
- `session_name`: Nombre de la sesión a editar

**Returns:**
- `(success, message)`: Tupla de resultado

**Flujo:**
1. Carga sesión actual
2. Muestra información (pestañas, ventanas)
3. Abre editor `micro`
4. Valida estructura JSON después de editar
5. Restaura backup si hay error de validación

**Estructura JSON esperada:**
```json
[
  {
    "is_focused": true,
    "tabs": [
      {"title": "TAB_TITLE", "cmd": "comando;a-ejecutar"},
      {"title": "ANOTHER_TAB", "cmd": ""}
    ]
  }
]
```

**Validaciones post-edición:**
- El archivo debe ser una lista
- Cada ventana debe ser un objeto con `tabs`
- Cada pestaña debe tener `title` (obligatorio) y `cmd` (opcional)

---

## Comandos CLI Asociados

### `ares gs edit <nombre>`
Edita cualquier sesión guardada en `db/`.

**Ejemplo:**
```bash
ares gs edit diaria
ares gs edit test_session
```

### `ares diario-edit`
Alias específico para editar la sesión `diaria`.

**Ejemplo:**
```bash
ares diario-edit
```

---

## Base de Datos

### Ubicación
`/home/daniel/tron/programas/TR/db/`

### Archivos
- `{session_name}.json` - Configuración de sesión
- `{session_name}.json.bak` - Backup automático

### Ejemplo: `diaria.json`
```json
[
  {
    "id": 1,
    "is_focused": true,
    "tabs": [
      {"title": "GEMINI", "cmd": ""},
      {"title": "QWEN", "cmd": ""},
      {"title": "COMANDO", "cmd": ""},
      {"title": "NOTAS", "cmd": "/usr/bin/micro /home/daniel/tron/Notas-Pendientes/notas.md"},
      {"title": "AGENDA", "cmd": "/home/daniel/.local/bin/uv run --quiet --project /home/daniel/tron/programas/AGENDA python /home/daniel/tron/programas/AGENDA/main.py"},
      {"title": "BR", "cmd": "/home/daniel/tron/programas/TR/bin/br"},
      {"title": "OLLAMA-SERVE", "cmd": "ollama serve"}
    ]
  }
]
```

---

## Directivas de Diseño Respetadas

### 1. Modularidad Atómica
- Máximo 3 funciones principales
- Cada función tiene una responsabilidad única
- Sin dependencias circulares

### 2. Soberanía del Usuario
- Archivos de configuración son de solo lectura hasta que se edita explícitamente
- Backup automático antes de modificaciones
- Validación previene corrupción de datos

### 3. Traducción Literal
- Las fórmulas de estructura JSON se mantienen literales
- No hay re-interpretación de campos existentes
- El usuario tiene control total sobre el contenido

### 4. Decoupling de Estado
- El estado volátil (edición) no se guarda hasta confirmación
- Los archivos JSON son configuración persistente
- El editor es una herramienta separada del orquestador

---

## Integración con Sistema Existente

### Window Registry
Las sesiones editadas se despliegan con registro automático en `window_registry` para control futuro.

### Socket Manager
Cada deploy genera sockets únicos automáticos basados en nombre de sesión + timestamp.

### Orchestrator
El módulo `session_editor` es complementario al `KittyOrchestrator`:
- `session_editor`: Edita configuración
- `orchestrator`: Despliega sesiones

---

## Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| "Sesión no encontrada" | Archivo no existe en `db/` | Usar `ares gs save` primero |
| "JSON inválido" | Error de sintaxis al editar | Backup se restaura automáticamente |
| "Editor micro no encontrado" | `micro` no instalado | `sudo apt install micro` |
| "Error al guardar" | Permisos insuficientes | Verificar permisos en `db/` |

---

## Próximas Evoluciones (Espacios para Automatización)

### 1. Multi-Socket Automático
Cada pestaña podría especificar socket preferences:
```json
{
  "tabs": [
    {"title": "GEMINI", "cmd": "", "socket": "unix:/tmp/gemini_socket"},
    {"title": "QWEN", "cmd": "", "socket": "unix:/tmp/qwen_socket"}
  ]
}
```

### 2. Plantillas de Sesiones
Crear sesiones desde plantillas predefinidas:
- `diaria` - Trabajo diario
- `dev` - Desarrollo
- `investigacion` - Búsqueda web
- `demo` - Demostraciones

### 3. Variables de Entorno por Sesión
Inyectar variables específicas por sesión:
```json
{
  "env": {
    "TR_ENV": "production",
    "OLLAMA_HOST": "localhost:11434"
  }
}
```

---

*Filosofía ARES: Orden Paranoico. Modularidad Atómica. Excelencia Técnica.*

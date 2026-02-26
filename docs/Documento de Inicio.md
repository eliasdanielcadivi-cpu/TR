# DOCUMENTO PRINCIPAL:

---

 He analizado profundamente toda la documentación proporcionada y los repositorios de referencia. Aquí está el análisis voraz y ultra granular de requerimientos del sistema TRON:

---

# TRON: ANÁLISIS VORAZ DE REQUERIMIENTOS DEL SISTEMA
## Terminal Remote Operations Nexus - Especificación Definitiva

---

## 1. REQUERIMIENTOS DE ARQUITECTURA BASE (1-15)

### 1.1 Estructura de Directorios Paranoicamente Ordenada
- **Ruta base**: `/home/daniel/tron/programas/TR/`
- **Estructura obligatoria**: Todo el código debe residir en carpetas jerárquicas estrictamente organizadas
- **Excepción única**: El archivo README puede estar en la raíz; todo lo demás en subcarpetas
- **Documentación**: Todo en `/docs` con conversión automática HTML→Markdown de referencias de Kitty

### 1.2 Gestión de Dependencias UV
- **Sistema de build**: UV (Python package manager) obligatorio
- **Configuración**: Archivos `pyproject.toml` en cada proyecto
- **Entornos virtuales**: Aislados pero accesibles desde `/usr/bin/`

### 1.3 Instalación Global Segura (Script `ini`)
El script `ini` proporcionado establece el patrón:
```python
launcher_content = f"""#!/bin/bash
# Generado por 'ini'
PROJECT_PATH="{current_dir}"
cd "$PROJECT_PATH"
exec uv run --project "$PROJECT_PATH" python "$PROJECT_PATH/{target}" "$@"
"""
```
- **Wrapper de shell**: Los ejecutables en `/usr/bin/` deben ser wrappers bash que redirijan a UV
- **Preservación de contexto**: No desconexión de entornos, configuraciones o bases de datos al mover a `/usr/bin/`

### 1.4 Compatibilidad Shell Maximizada
- **Cabeceras**: Todos los scripts Zsh deben usar shebang `#!/bin/bash` para máxima compatibilidad
- **Conversión automática**: La IA CLI debe convertir sources de scripts Zsh a Bash cuando sea necesario
- **Entorno**: Zsh + Oh My Zsh como shell interactivo, Bash para scripts de sistema

### 1.5 Configuración YAML Centralizada
- **Formato**: Todas las configuraciones en YAML (no JSON)
- **Ubicación**: `/home/daniel/tron/config/`
- **Jerarquía**: Configuración global → por proyecto → por sesión

### 1.6 Base de Datos Local (Opcional pero preparada)
- **Requisito**: El sistema debe soportar SQLite local sin romper al mover a `/usr/bin/`
- **Path resolución**: Usar rutas absolutas o variables de entorno `TRON_HOME`

### 1.7 Logging Estructurado
- **Formato**: JSON Lines para facilitar parsing por la IA
- **Rotación**: Automática por sesión con timestamps ISO 8601
- **Ubicación**: `/home/daniel/tron/logs/`

### 1.8 Sistema de Plugins/Extensiones
- **Arquitectura**: Cargar dinámicamente "gatitos" (kittens) de Kitty personalizados
- **Referencia**: Estudiar estructura de `gattino` (github.com/salvozappa/gattino)
- **Prioridad**: Los gatitos son tercer orden de importancia (después de control remoto y ventanas)

### 1.9 Seguridad por Contraseñas de Control Remoto
- **Implementación**: `remote_control_password` en kitty.conf con granularidad por acción
- **Autenticación**: Passwords diferentes para diferentes niveles de control (colores, ventanas, ejecución)
- **Encriptación**: Soporte para comunicación cifrada vía ECDH+X25519 para uso sobre SSH

### 1.10 Sistema de Sesiones Persistente
- **Formato**: Kitty sessions nativas
- **Funcionalidad**: Guardar y restaurar layouts completos de ventanas, tabs y aplicaciones
- **Identificación**: Cada ventana/tab debe tener metadatos de sesión para matching posterior

### 1.11 Gestión de Modelos LLM
Basado en la lista de modelos Ollama proporcionada:
- **Modelos soportados**:
  - `gemma3:4b` (3.3GB, template específico con `<start_of_turn>`)
  - `qwen2.5:3b` (1.9GB) y `qwen2.5:latest` (4.7GB)
  - `llama3.1:8b` (4.9GB)
  - `phi4-mini:latest` (2.5GB) y `phi4-mini-reasoning:3.8b` (3.2GB)
  - `llama3.2:3b` (2.0GB)
- **Template Gemma3**:
```
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if or (eq .Role "user") (eq .Role "system") }}<start_of_turn>user
{{ .Content }}<end_of_turn>
{{ if $last }}<start_of_turn>model
{{ end }}
{{- else if eq .Role "assistant" }}<start_of_turn>model
{{ .Content }}{{ if not $last }}<end_of_turn>
{{ end }}
{{- end }}
{{- end }}
```

### 1.12 Configuración de Modelos en YAML
- **Temperatura**: Ajustable por modelo (0.0 para reproducibilidad, 0.8 para creatividad)
- **Context window**: Configurable según modelo (128K para DeepSeek-V3.2)
- **Seed**: Opcional para reproducibilidad
- **Keep alive**: Control de tiempo en memoria (default 5m)

### 1.13 Múltiples Proveedores de IA
- **Ollama**: Endpoint local `http://localhost:11434`
- **DeepSeek**: API remota `https://api.deepseek.com` (compatible OpenAI)
- **Modelos locales**: Soporte para modelos quantizados vía llama.cpp
- **Fallback**: Si Ollama no responde, usar comando predefinido o pedir input manual

### 1.14 Caché de Contexto (DeepSeek)
- **Disco duro**: Caché automática de prefijos de solicitudes
- **Hit/Miss**: Tracking de `prompt_cache_hit_tokens` vs `prompt_cache_miss_tokens`
- **Optimización**: Reutilización de contexto en solicitudes consecutivas

### 1.15 Tool Calling (Funciones)
- **Ollama**: Soporte para `tools` en `/api/chat` con `tool_calls` y `tool_name`
- **DeepSeek**: Tool calling en modo pensante y no pensante
- **Strict mode**: Validación de esquemas JSON para parámetros de funciones

---

## 2. REQUERIMIENTOS DE TERMINAL KITTY (16-35)

### 2.1 Control Remoto Total vía Socket
- **Activación**: `allow_remote_control=yes` + `--listen-on unix:/tmp/tron-kitty`
- **Protocolo**: Uso extensivo de `kitten @` para todos los comandos
- **Matching sofisticado**: Por título, ID, cwd, cmdline, env vars, estado (active/focused)
- **Operaciones soportadas**: launch, focus-window, focus-tab, send-text, close-window, set-colors, etc.

### 2.2 Sistema de Ventanas Inteligente
- **Tipos soportados**: window, tab, os-window, overlay, overlay-main, background
- **Títulos configurables**: Cada ventana/tab debe tener nombre descriptivo seteable vía `kitten @ set-window-title` / `set-tab-title`
- **Colores dinámicos**: Cambio de esquemas de color vía `kitten @ set-colors` para efectos visuales
- **Opacidad**: Soporte para `dynamic_background_opacity` con ajuste en tiempo real

### 2.3 Layouts Avanzados
- **Layouts soportados**: tall, fat, grid, splits, horizontal, vertical, stack
- **Control**: Cambio dinámico vía `kitten @ goto-layout`
- **Bias de tamaño**: Ajuste proporcional de ventanas con `--bias` (0-100)
- **Posicionamiento**: Control preciso con `--location` (after, before, vsplit, hsplit)

### 2.4 Reproducción Multimedia Integrada
- **Video**: `mpv --profile=sw-fast --vo=kitty --vo-kitty-use-shm=yes --really-quiet`
- **Calidad**: Excelente resolución sin negociación (eficiencia máxima)
- **Formatos**: MKV, MP4, y streams soportados por mpv
- **Integración**: Lanzar videos en ventanas específicas con títulos descriptivos

### 2.5 Visualización de Imágenes y Documentos
- **Imágenes**: `kitten icat` para mostrar imágenes directamente en terminal
- **PDFs**: Integración con termpdf.py, tdf, fancy-cat, o meowpdf
- **Markdown**: presenterm o mdfried para slides con imágenes
- **Gráficos**: Soporte para matplotlib, gnuplot con backends Kitty

### 2.6 Integración Shell Sophisticada
- **Features requeridas**:
  - Navegación por prompts con Ctrl+Shift+Z/X
  - Click para posicionar cursor en comandos
  - Ctrl+Shift+Click derecho para ver output en pager
  - Clonado de shell con env vars y cwd copiados
  - Edición de archivos en nuevas ventanas incluso vía SSH
- **Marcadores**: Sistema de `marks` para resaltar texto (ERRORES, WARNINGS, etc.)

### 2.7 SSH y Transferencias
- **Kitten SSH**: Uso de `kitten ssh` para preservar funcionalidades avanzadas
- **Transferencia de archivos**: `kitten transfer` con confirmación automática desactivable
- **Remote file**: Edición de archivos remotos en ventanas locales

### 2.8 Hints y Navegación
- **URL hints**: `kitten hints` para abrir URLs, copiar al clipboard
- **Hyperlinked grep**: Integración con ripgrep para output clickeable
- **Selección de texto**: kitty-grab para selección keyboard-based en scrollback

### 2.9 Paneles de Escritorio (Opcional WOW)
- **Kitty panel**: Crear paneles de sistema con métricas en tiempo real
- **Posicionamiento**: Top, bottom, left, right vía `--os-panel`
- **Integración**: Con Openbox para paneles flotantes o docked

### 2.10 Configuración Programática
- **Reload**: `kitten @ load-config` para recargar configuración sin reiniciar
- **Overrides**: Soporte para `-o` flags en comandos de lanzamiento
- **Fuentes**: Cambio de tamaño dinámico con `kitten @ set-font-size`

### 2.11 Protocolo RC Específico
Basado en la documentación de Kitty RC:
```python
# Estructura base del protocolo
{
    "cmd": "command name",
    "version": [0, 14, 2],  # Versión Kitty
    "no_response": false,
    "kitty_window_id": "optional",
    "payload": {}  # Comando específico
}
```
- **Async**: Soporte para `async` y `cancel_async` en comandos que requieren input del usuario
- **Streaming**: Para envío de datos grandes (imágenes, archivos) con `stream: true` y `stream_id`

### 2.12 Encriptación de Comunicación
- **Protocolo**: ECDH con curva X25519
- **Nonce**: Time-based para prevenir replay attacks
- **AES-256-GCM**: Para encriptación de comandos con password
- **Synchronización**: Relojes deben estar sincronizados (±5 minutos)

### 2.13 Matching de Ventanas Sofisticado
Campos soportados para matching:
- `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session`, `recent`
- Estados: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`
- Operadores booleanos: `and`, `or`, `not`, paréntesis para agrupación

### 2.14 Comando Launch Extendido
Opciones críticas para TRON:
- `--type`: window, tab, os-window, overlay, overlay-main, background, os-panel
- `--location`: after, before, vsplit, hsplit, neighbor, first, last
- `--bias`: 0-100 para control de tamaño proporcional
- `--cwd`: current, last_reported, oldest, root
- `--env` y `--var`: Variables de entorno y user vars
- `--copy-colors`, `--copy-env`, `--copy-cmdline`: Herencia de ventana fuente
- `--allow-remote-control`: Habilitar control remoto en ventana específica
- `--remote-control-password`: Password granular por ventana

### 2.15 Watchers y Eventos
- **on_load**: Inicialización del watcher
- **on_resize**: Cambio de tamaño de ventana
- **on_focus_change`: Cambio de foco
- **on_close`: Cierre de ventana
- **on_cmd_startstop`: Inicio/fin de comando en shell
- **on_title_change`: Cambio de título
- **on_color_scheme_preference_change`: Cambio tema claro/oscuro

---

## 3. REQUERIMIENTOS DE ORQUESTACIÓN DE VENTANAS (36-50)

### 3.1 Puppet Master en Python
- **Tecnología**: Python 3.9+ con comunicación directa a Kitty vía sockets Unix
- **Alternativas evaluadas**: pyvda (Windows), wmctrl/xdotool (X11), pero preferir native Kitty RC
- **Función**: Recibir señales de la IA y traducir a comandos `kitten @`

### 3.2 Protocolo de Comandos IA→Orquestador
- **Formato**: JSON con campos estandarizados:
  ```json
  {
    "action": "focus|launch|move|resize|close",
    "target": "nombre_ventana_o_match",
    "position": "center|left|right|fullscreen",
    "command": "comando_a_ejecutar",
    "priority": "high|normal|low"
  }
  ```

### 3.3 Gestión de Foco Dinámica
- **Efecto "traer al frente"**: La IA debe poder enfocar cualquier ventana/tab específica
- **Historial de foco**: Mantener stack de ventanas recientes para "volver atrás"
- **Transiciones**: Instantáneas (Openbox es ligero) pero visibles

### 3.4 Posicionamiento Absoluto/Relativo
- **Coordenadas**: Soporte para posicionamiento por porcentaje de pantalla
- **Espacios de trabajo**: Integración con Openbox para mover entre desktops virtuales
- **Z-order**: Control de elevación de ventanas (raise/lower)

### 3.5 Lanzamiento de Aplicaciones con Contexto
- **Simples**: Comandos de una línea con `;` separadores
- **Compuestas**: Scripts multi-línea con heredocs
- **Entorno**: Preservación de variables de entorno entre ventanas
- **Identificación**: Cada app lanzada debe tener ID único trackeable

### 3.6 Control de Tabs Múltiples
- **Nomenclatura**: Tabs con nombres descriptivos (no numéricos)
- **Switching**: Cambio instantáneo entre tabs vía `kitten @ focus-tab --match title:xxx`
- **Colores**: Tabs con colores diferentes para diferenciación visual

### 3.7 Broadcasting y Sincronización
- **Broadcast**: Enviar mismo comando a múltiples ventanas simultáneamente
- **Sincronización**: Ejecutar comandos en secuencia específica entre ventanas
- **Esperas**: Sincronización con `wait-for-child-to-exit` cuando sea necesario

### 3.8 Overlay Windows Estratégicas
- **Uso**: Ventanas temporales para confirmaciones, inputs, o displays de estado
- **Tipos**: overlay (modal) vs overlay-main (persistente)
- **Integración**: No interferir con el flujo principal pero permitir interacción

### 3.9 Detección de Estado de Ventanas
- **Query**: `kitten @ ls` para obtener estado completo del árbol de ventanas
- **Parsing**: JSON parseable para tomar decisiones basadas en estado actual
- **Eventos**: Watchers para reaccionar a cambios (resize, focus, close)

### 3.10 Integración Openbox Específica
- **Comandos**: `openbox --action` para control de ventanas a nivel WM
- **Propiedades**: WM_CLASS, WM_NAME seteables para reglas de Openbox
- **Posicionamiento**: Uso de `wmctrl` como fallback si native RC no alcanza

### 3.11 Layouts Predefinidos para Demos
- **"code-review"**: 3 ventanas (código, tests, diff)
- **"monitoring"**: 4 ventanas (logs, métricas, alertas, terminal)
- **"multimedia"**: Video grande + controles + info
- **"presentation"**: Terminal principal + notas + timer

### 3.12 Transiciones Suaves
- **Cambio de layouts**: Animación instantánea pero perceptible
- **Cambio de colores**: Transición gradual de esquemas
- **Focus switching**: Highlight visual al cambiar foco

### 3.13 Multi-Monitor Support
- **Detección**: Identificar displays vía xrandr
- **Distribución**: Enviar ventanas a monitores específicos
- **Sincronización**: Comandos que afecten múltiples displays

### 3.14 Persistencia de Sesiones
- **Guardado**: `kitten @ ls --output-format session` para guardar estado
- **Restauración**: Lanzar desde archivo de sesión
- **Metadatos**: Preservar nombres, colores, comandos en ejecución

### 3.15 Control de Permisos Granular
- **Passwords múltiples**: Diferentes niveles (viewer, operator, admin)
- **Acciones permitidas**: Wildcards como `get-*`, `set-colors`
- **Autorización custom**: Script Python `is_cmd_allowed` para lógica propia

---

## 4. REQUERIMIENTOS DE INTERFAZ IA Y CLI (51-70)

### 4.1 Trigger de Invocación Simplificado
- **Formato**: `tr -p "hablar libre" opcionNombre opcionNombre` (doble guión medio)
- **Alternativas descartadas**: `?` simple puede ser confuso; `tr` es explícito y único
- **Contexto**: El usuario escribe `tr` seguido de descripción en español o inglés

### 4.2 Pipeline de Procesamiento IA
1. **Input**: `tr -p "borrar logs de más de 30 días"`
2. **Parseo**: Extraer opciones (`-p` = prompt, flags adicionales)
3. **Envío**: Prompt a Ollama (local) o DeepSeek (API)
4. **Generación**: Comando shell propuesto
5. **Confirmación**: Interfaz con Gum (Charm.sh) o similar para validación
6. **Ejecución**: Vía Orquestador Python a Kitty

### 4.3 Interfaz de Confirmación Elegante
- **Tecnología**: Gum (gum confirm, gum input, gum spin) de Charm.sh
- **Estilo**: Minimalista, colores consistentes con esquema de terminal
- **Opciones**:
  - Enter para confirmar
  - Esc para cancelar
  - 'e' para editar comando antes de ejecutar
  - 'x' para ejecutar con privilegios elevados (sudo)

### 4.4 Historial y Contexto Conversacional
- **Memoria**: Últimos N comandos y sus outputs para contexto
- **Referencias**: `!!` para repetir último comando, `!n` para el enésimo
- **Explicación**: Comando `explain` para que la IA explique qué hace un comando

### 4.5 Detección de Intenciones Avanzada
- **Análisis profundo**: No solo mapeo directo, sino inferencia de contexto
- **Ejemplos**:
  - "muestra el video" → detectar archivo video reciente o en cwd
  - "abre el proyecto" → detectar proyecto git en cwd o subdirectorios
  - "conecta al servidor" → usar SSH kitten con último host conocido

### 4.6 Manejo de Errores Inteligente
- **Captura**: Si un comando falla, capturar stderr automáticamente
- **Diagnóstico**: Enviar error a la IA para sugerir fix
- **Recuperación**: Opción de "arreglar y reintentar" o "deshacer"

### 4.7 Autocompletado Contextual
- **Fuentes**: Historial de comandos, archivos en cwd, hosts SSH conocidos
- **Integración**: Con shell nativo (zsh completions) y con interfaz Gum
- **Previsualización**: Mostrar efecto esperado antes de ejecutar

### 4.8 Modos de Ejecución
- **Seguro**: Solo muestra comando, no ejecuta (default para comandos destructivos)
- **Asistido**: Muestra y pide confirmación (default general)
- **Directo**: Ejecuta inmediatamente (para comandos whitelistados)
- **Batch**: Acumula comandos y ejecuta secuencia con una confirmación

### 4.9 Integración con Sistemas Externos
- **Ollama**: Endpoint local `http://localhost:11434`
- **DeepSeek**: API remota con streaming de respuestas
- **Modelos locales**: Soporte para modelos quantizados vía llama.cpp
- **Fallback**: Si Ollama no responde, usar comando predefinido o pedir input manual

### 4.10 Sistema de "Wut" Integrado
- **Función**: Explicar output de último comando automáticamente
- **Trigger**: `wut` o automático cuando se detecta error
- **Contexto**: Captura de scrollback vía `kitten @ get-text --extent last_cmd_output`
- **Presentación**: En ventana overlay o split

### 4.11 Snippets de Código Críticos - Ollama API

**Generación de Completion (Streaming)**:
```python
import requests
import json

def ollama_generate_stream(model, prompt, system=None, options=None):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": options or {}
    }
    if system:
        payload["system"] = system

    response = requests.post(url, json=payload, stream=True)
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            yield data
            if data.get("done"):
                break

# Uso
for chunk in ollama_generate_stream("gemma3:4b", "Why is the sky blue?"):
    print(chunk.get("response", ""), end="")
```

**Chat Completion con Tools**:
```python
def ollama_chat_with_tools(model, messages, tools=None):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "tools": tools or []
    }

    response = requests.post(url, json=payload)
    return response.json()

# Ejemplo de tool
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
}]
```

**Embeddings**:
```python
def ollama_embed(model, input_text):
    url = "http://localhost:11434/api/embed"
    payload = {
        "model": model,
        "input": input_text
    }
    response = requests.post(url, json=payload)
    return response.json()["embeddings"]
```

### 4.12 Snippets de Código Críticos - DeepSeek API

**Chat Completion (OpenAI-compatible)**:
```python
from openai import OpenAI

def deepseek_chat(messages, model="deepseek-chat", stream=False):
    client = OpenAI(
        api_key="sk-...",
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model=model,  # "deepseek-chat" o "deepseek-reasoner"
        messages=messages,
        stream=stream,
        temperature=0.7
    )

    if stream:
        for chunk in response:
            yield chunk.choices[0].delta.content
    else:
        return response.choices[0].message.content

# Uso con caché de contexto
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"}
]
```

**Tool Calling con Strict Mode**:
```python
def deepseek_tool_call(messages, tools):
    client = OpenAI(
        api_key="sk-...",
        base_url="https://api.deepseek.com/beta"  # Beta para strict mode
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        stream=False
    )

    # Verificar cache hit/miss
    usage = response.usage
    print(f"Cache hit: {usage.prompt_cache_hit_tokens}")
    print(f"Cache miss: {usage.prompt_cache_miss_tokens}")

    return response.choices[0].message.tool_calls
```

**JSON Mode**:
```python
def deepseek_json_output(prompt, schema=None):
    client = OpenAI(
        api_key="sk-...",
        base_url="https://api.deepseek.com"
    )

    messages = [
        {"role": "system", "content": "Respond in JSON format"},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={"type": "json_object"},
        stream=False
    )

    return json.loads(response.choices[0].message.content)
```

### 4.13 Snippets de Código Críticos - Kitty Remote Control

**Control básico**:
```python
import subprocess
import json

def kitty_rc(command, **kwargs):
    """Ejecutar comando kitty remote control"""
    cmd = ["kitten", "@", command]

    for key, value in kwargs.items():
        if isinstance(value, bool):
            if value:
                cmd.append(f"--{key.replace('_', '-')}")
        else:
            cmd.extend([f"--{key.replace('_', '-')}", str(value)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# Ejemplos
kitty_rc("launch", type="tab", tab_title="My Tab", keep_focus=True)
kitty_rc("focus-window", match="title:Output")
kitty_rc("send-text", match="cmdline:cat", data="Hello, World")
```

**Obtener estado**:
```python
def kitty_ls():
    """Obtener árbol de ventanas/tabs"""
    result = subprocess.run(
        ["kitten", "@", "ls", "--output-format", "json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

# Parsear para encontrar ventanas específicas
def find_window_by_title(title):
    tree = kitty_ls()
    for os_window in tree:
        for tab in os_window.get("tabs", []):
            for window in tab.get("windows", []):
                if title in window.get("title", ""):
                    return window
    return None
```

**Cambiar colores dinámicamente**:
```python
def kitty_set_colors(window_id, colors):
    """colors: dict como {'background': 'red', 'foreground': '#ffffff'}"""
    color_args = [f"{k}={v}" for k, v in colors.items()]
    kitty_rc("set-colors", match=f"id:{window_id}", *color_args)

# Efecto de alerta
kitty_set_colors(1, {"background": "#ff0000", "foreground": "#ffffff"})
```

**Enviar texto a ventana específica**:
```python
def kitty_send_to_window(match, text, stdin=False):
    if stdin:
        # Enviar vía stdin
        proc = subprocess.Popen(
            ["kitten", "@", "send-text", "--match", match, "--stdin"],
            stdin=subprocess.PIPE
        )
        proc.communicate(text.encode())
    else:
        kitty_rc("send-text", match=match, text=text)
```

### 4.14 Snippets de Código Críticos - Integración Gum

**Confirmación elegante**:
```bash
#!/bin/bash
# confirm.sh
gum confirm "¿Ejecutar comando?" --affirmative "Sí" --negative "No"
if [ $? -eq 0 ]; then
    echo "Ejecutando..."
fi
```

**Input con estilo**:
```bash
# input.sh
COMMAND=$(gum input --placeholder "Comando a ejecutar" --prompt "> ")
echo "Comando: $COMMAND"
```

**Spinner para operaciones largas**:
```bash
# spinner.sh
gum spin --spinner dot --title "Procesando con IA..." -- sleep 2
```

**Tabla de selección**:
```bash
# table.sh
echo -e "Comando\tDescripción" | gum table --widths 30,50
```

### 4.15 Snippets de Código Críticos - Openbox Integration

**Posicionar ventana**:
```bash
# Mover ventana a coordenadas específicas
wmctrl -r "Ventana" -e 0,100,100,800,600

# Maximizar
wmctrl -r "Ventana" -b add,maximized_vert,maximized_horz

# Cambiar a workspace específico
wmctrl -r "Ventana" -t 2

# Traer al frente
wmctrl -a "Ventana"
```

**Propiedades de ventana**:
```bash
# Listar ventanas con IDs
wmctrl -l

# Obtener ID de ventana activa
xdotool getactivewindow

# Mover ventana por ID
xdotool windowmove 12345678 100 100
```

---

## 5. REQUERIMIENTOS DE EXPERIENCIA VISUAL WOW (71-85)

### 5.1 Demostración de Salón/Conferencia
- **Escenario**: Usuario en reunión corporativa abre terminal y ejecuta `kv` (kitty visualizer)
- **Efecto**: Apertura instantánea de múltiples tabs preconfiguradas con nombres descriptivos
- **Contenido**: Cada tab muestra diferentes aspectos (logs, monitoreo, código, multimedia)

### 5.2 Apertura por Socket con Nombres
- **Comando**: `kv` o `tron start` abre Kitty con socket específico
- **Configuración**: Tabs predefinidas en YAML (nombre, comando, layout, colores)
- **Ejecución**: Comandos iniciales se ejecutan automáticamente en cada tab

### 5.3 Posicionamiento Cinematográfico
- **Grid de presentación**: Layouts predefinidos para diferentes tipos de demo
  - "code-review": 3 ventanas (código, tests, diff)
  - "monitoring": 4 ventanas (logs, métricas, alertas, terminal)
  - "multimedia": Video grande + controles + info
- **Transiciones**: Cambio de layouts suave pero perceptible

### 5.4 Visualización de Código con Estilo
- **Syntax highlighting**: En terminal vía `bat` o similar
- **Diffs**: Side-by-side con colores vía `delta`
- **Imágenes**: Mostrar diagramas de arquitectura vía `kitten icat`

### 5.5 Efectos de Color y Animación
- **Cambios de tema**: Transición de colores para indicar estados (verde=OK, rojo=error, azul=procesando)
- **Pulsos**: Cambio temporal de background color para alertas
- **Gradientes**: Opacidad variable para crear profundidad visual

### 5.6 Branding Personalizado
- **Logos**: `kitten @ set-window-logo` con logo del proyecto/corporación
- **Fondos**: Imágenes de fondo sutil con `kitten @ set-background-image`
- **Fuentes**: Tamaños variables para jerarquía visual (títulos grandes, código mediano, logs pequeños)

### 5.7 Interacción en Tiempo Real
- **Input simultáneo**: Escribir en una ventana y ver reflejo en otra (para comparaciones)
- **Broadcast typing**: Modo donde lo que se escribe va a todas las ventanas
- **Follow mode**: Una ventana sigue el foco de otra automáticamente

### 5.8 Captura y Replay de Sesiones
- **Grabación**: Guardar secuencia de comandos y sus outputs
- **Replay**: Reejecutar sesión paso a paso con pausas
- **Edición**: Modificar sesiones grabadas para crear demos perfectas

### 5.9 Integración con File Managers TUI
- **Ranger/nnn/Yazi**: Abrir en ventana dedicada con previews activados
- **Navegación**: Selección de archivo en FM → acción en otra ventana (editar, ver, ejecutar)
- **Sincronización**: CWD compartido entre FM y terminal de comandos

### 5.10 Dashboards de Sistema
- **Paneles**: Uso de `kitty-panel` o implementación propia
- **Métricas**: CPU, memoria, red, procesos en tiempo real
- **Visualización**: Gráficos ASCII o con `gnuplot`/`matplotlib` en terminal

### 5.11 Efecto "Hacker" Visual
- **Glitch effects**: Distorsiones temporales en texto
- **Matrix rain**: Código cayendo en background (opcional)
- **Typing sounds**: Audio feedback al escribir (opcional, configurable)

### 5.12 Transiciones de Foco
- **Spotlight**: Oscurecer ventanas no activas, resaltar activa
- **Zoom**: Aumentar tamaño de ventana enfocada temporalmente
- **Borders**: Colores dinámicos en bordes según estado

### 5.13 Sincronización de Scroll
- **Scroll compartido**: Múltiples ventanas scrollean juntas
- **Follow output**: Ventana secundaria sigue output de primaria
- **Diff scroll**: Comparación sincronizada de dos archivos

### 5.14 Atajos de Teclado Visuales
- **Cheatsheet overlay**: Mostrar atajos disponibles en ventana flotante
- **Hint mode**: Resaltar letras para acciones rápidas (como Vimium)
- **Macro recording**: Grabar y reproducir secuencias de comandos

### 5.15 Integración con el Entorno
- **Wallpaper dinámico**: Cambiar fondo de escritorio según modo
- **Cursor personalizado**: Diferentes cursores para diferentes modos
- **Notificaciones**: Esquinas de pantalla para alertas importantes

---

## 6. REQUERIMIENTOS DE REFERENCIA Y ESTUDIO (86-100)

### 6.1 Repositorios Obligatorios de Estudio
Debes descargar, leer y extraer ideas de código de:

1. **gattino** (github.com/salvozappa/gattino) - Integración Kitty+LLM
   - Estructura de kittens personalizados
   - Comunicación con APIs de IA
   - Manejo de prompts y respuestas

2. **ht** (github.com/catallo/ht) - Shell helper con AI, bajo uso de tokens
   - Optimización de prompts para reducir tokens
   - Caché de respuestas frecuentes
   - Integración con múltiples shells

3. **wut** (github.com/shobrook/wut) - Explicación de output de comandos
   - Captura de scrollback
   - Análisis de errores
   - Sugerencias contextuales

4. **zev** (github.com/dtnewman/zev) - Generación de comandos con confirmación
   - Interfaz de confirmación elegante
   - Manejo de flags y opciones
   - Historial de comandos generados

5. **terminal-command** (github.com/huss-mo/terminal-command) - CLI Python para comandos IA
   - Estructura de CLI con typer/click
   - Integración con Ollama
   - Manejo de configuración

6. **reTermAI** (github.com/pie0902/reTermAI) - Terminal AI assistant
   - Interfaz conversacional en terminal
   - Manejo de contexto multi-turn
   - Integración con shell nativo

### 6.2 Documentación Kitty a Convertir
Todas estas URLs deben descargarse y convertirse a Markdown en `/docs/`:

- Remote control: https://sw.kovidgoyal.net/kitty/remote-control/
- RC Protocol: https://sw.kovidgoyal.net/kitty/rc_protocol/
- Integrations: https://sw.kovidgoyal.net/kitty/integrations/
- Overview: https://sw.kovidgoyal.net/kitty/overview/
- Layouts: https://sw.kovidgoyal.net/kitty/layouts/
- Kittens intro: https://sw.kovidgoyal.net/kitty/kittens_intro/
- Hints kitten: https://sw.kovidgoyal.net/kitty/kittens/hints/
- SSH kitten: https://sw.kovidgoyal.net/kitty/kittens/ssh/
- Transfer kitten: https://sw.kovidgoyal.net/kitty/kittens/transfer/
- Hyperlinked grep: https://sw.kovidgoyal.net/kitty/kittens/hyperlinked_grep/
- Remote file: https://sw.kovidgoyal.net/kitty/kittens/remote_file/
- Open actions: https://sw.kovidgoyal.net/kitty/open_actions/
- Shell integration: https://sw.kovidgoyal.net/kitty/shell-integration/
- Marks: https://sw.kovidgoyal.net/kitty/marks/
- FAQ: https://sw.kovidgoyal.net/kitty/faq/

### 6.3 Herramientas de UI Recomendadas
- **Gum**: Para interfaces interactivas elegantes (confirmaciones, inputs, spinners)
- **FZF**: Para fuzzy finding de comandos, archivos, hosts
- **Zellij**: Alternativa a tmux/screen si se necesita multiplexación adicional
- **Starship**: Prompt personalizado con información de contexto

### 6.4 Eficiencia y Rendimiento
- **Consumo memoria**: Sistema completo debe funcionar en máquina con 8GB RAM (0.5GB base + 7.5GB disponibles)
- **Latencia**: Respuesta de IA < 2s para comandos simples
- **Paralelismo**: Múltiples ventanas no deben bloquearse mutuamente
- **Optimización**: Uso de `--profile=sw-fast` para mpv y flags similares para máxima eficiencia

### 6.5 Plantillas de Prompts
- **System prompt base**: "You are TRON, a terminal assistant specialized in shell commands..."
- **Few-shot examples**: Ejemplos de comandos naturales a shell commands
- **Context injection**: Variables de entorno, historial reciente, archivos en cwd
- **Output format**: Especificar formato de respuesta (JSON, markdown, plain)

### 6.6 Manejo de Errores y Edge Cases
- **Timeout de IA**: 10s para locales, 30s para remotas
- **Reintentos**: 3 intentos con backoff exponencial
- **Fallbacks**: Comando alternativo si IA no responde
- **Validación**: Sanitizar comandos antes de ejecutar (no permitir `rm -rf /`)

### 6.7 Logging y Debugging
- **Niveles**: DEBUG, INFO, WARN, ERROR
- **Formato**: JSON Lines con timestamp, nivel, componente, mensaje
- **Rotación**: Por día, mantener últimos 7 días
- **Análisis**: Script para analizar logs y sugerir mejoras

### 6.8 Testing Estratégico
- **Unit tests**: pytest con cobertura > 80%
- **Integration tests**: Scripts que abren Kitty real y verifican comportamiento
- **End-to-end**: Simular flujo completo de usuario
- **Performance**: Benchmarks de latencia y uso de recursos

### 6.9 Documentación de Usuario
- **README**: Instalación rápida, uso básico
- **Guía completa**: Todos los comandos y opciones
- **Ejemplos**: Scripts de ejemplo para escenarios comunes
- **Troubleshooting**: Solución de problemas frecuentes

### 6.10 Roadmap y Futuro
- **v1.0**: Core funcional (IA + Kitty + Orquestador)
- **v1.1**: Soporte multi-monitor, más layouts
- **v1.2**: Plugins de comunidad, marketplace
- **v2.0**: Integración IDE, soporte remoto mejorado

---
---
¡Excelente pregunta! Estás en el camino correcto. Para controlar Openbox programáticamente desde un "puppeteer" (como llamas a tu sistema de automatización), aquí tienes un enfoque completo:

## **Herramientas principales para el control programático:**

### **1. xdotool** (ya lo usas)
Perfecto para simular acciones del usuario:
```bash
# Abrir ventana
xdotool exec konsole

# Cerrar ventana activa
xdotool getactivewindow windowclose

# Mover/redimensionar
xdotool search --name "Konsole" windowmove 100 100 windowsize 800 600

# Enfocar ventana específica
xdotool search --class "konsole" windowactivate
```

### **2. wmctrl** (Complemento esencial)
Control más fino del gestor de ventanas:
```bash
# Listar ventanas
wmctrl -l

# Ir a escritorio específico
wmctrl -s 1

# Mover ventana a otro escritorio
wmctrl -r "Konsole" -t 2

# Maximizar/restaurar
wmctrl -r "Konsole" -b toggle,maximized_vert,maximized_horz
```

### **3. xprop/xwininfo** (Para obtener información)
```bash
# Obtener propiedades de ventana
xprop -id $(xdotool getactivewindow)

# Información detallada
xwininfo -id $(xdotool search --name "ollama")
```

## **Estructura recomendada para tu sistema:**

### **1. Script base de control (control_ventanas.sh)**
```bash
#!/bin/bash
# Controlador central de ventanas

WINDOW_CONTROL_DIR="/home/daniel/tron/control-ventanas"
mkdir -p "$WINDOW_CONTROL_DIR"

case "$1" in
    "abrir-terminal")
        konsole --new-tab -e "$2" &
        ;;
    "organizar")
        # Organizar ventanas en grid
        wmctrl -l | grep "$2" | while read id; do
            win_id=$(echo $id | cut -d' ' -f1)
            case "$3" in
                "izquierda")
                    wmctrl -ir "$win_id" -b remove,maximized_vert,maximized_horz
                    xdotool windowmove "$win_id" 0 0 windowsize "$win_id" 960 1080
                    ;;
                "derecha")
                    wmctrl -ir "$win_id" -b remove,maximized_vert,maximized_horz
                    xdotool windowmove "$win_id" 960 0 windowsize "$win_id" 960 1080
                    ;;
            esac
        done
        ;;
    "monitorear")
        # Monitorear nuevas ventanas
        xprop -spy -root _NET_ACTIVE_WINDOW | while read line; do
            win_id=$(echo $line | awk '{print $NF}')
            class=$(xprop -id $win_id WM_CLASS | cut -d'"' -f2)
            echo "Ventana activa: $class ($win_id)"
            # Aquí puedes enviar a tu sistema de IA
        done
        ;;
esac
```

### **2. Integración con Python (tu puppeteer principal)**
```python
#!/usr/bin/env python3
# control_ventanas.py

import subprocess
import json
import time
import re

class WindowController:
    def __init__(self):
        self.windows = {}
        self.update_window_list()

    def update_window_list(self):
        """Actualiza lista de ventanas usando wmctrl"""
        output = subprocess.check_output(['wmctrl', '-l']).decode()
        for line in output.split('\n'):
            if line:
                parts = line.split(maxsplit=3)
                if len(parts) >= 4:
                    win_id, desktop, pid, title = parts
                    self.windows[title] = {
                        'id': win_id,
                        'desktop': desktop,
                        'title': title
                    }

    def open_terminal(self, command=None, workspace=0):
        """Abre terminal con comando opcional"""
        if command:
            subprocess.Popen(['konsole', '--new-tab', '-e', command])
        else:
            subprocess.Popen(['konsole'])
        time.sleep(0.5)  # Esperar a que se abra
        self.move_to_workspace('konsole', workspace)

    def move_to_workspace(self, window_pattern, workspace):
        """Mueve ventana a workspace específico"""
        try:
            win_id = subprocess.check_output(
                ['xdotool', 'search', '--name', window_pattern]
            ).decode().strip()
            subprocess.run(['wmctrl', '-ir', win_id, '-t', str(workspace)])
        except:
            pass

    def split_screen(self, left_app=None, right_app=None):
        """Organiza dos aplicaciones en pantalla dividida"""
        if left_app:
            self.open_app(left_app)
            time.sleep(0.5)
            subprocess.run(['/home/daniel/tron/control-ventanas/control_ventanas.sh',
                          'organizar', left_app, 'izquierda'])

        if right_app:
            self.open_app(right_app)
            time.sleep(0.5)
            subprocess.run(['/home/daniel/tron/control-ventanas/control_ventanas.sh',
                          'organizar', right_app, 'derecha'])

    def open_app(self, app_name):
        """Abre aplicación basado en nombre"""
        apps = {
            'vscode': 'code',
            'chrome': 'google-chrome-stable',
            'terminal': 'konsole',
            'editor': 'kate',
            'ollama': 'konsole -e ollama run deepseek-coder'
        }
        if app_name in apps:
            subprocess.Popen(apps[app_name].split())

    def monitor_windows(self):
        """Monitorea cambios en ventanas para responder"""
        old_active = None
        while True:
            try:
                # Obtener ventana activa
                active_id = subprocess.check_output(
                    ['xdotool', 'getactivewindow']
                ).decode().strip()

                if active_id != old_active:
                    class_name = subprocess.check_output(
                        ['xprop', '-id', active_id, 'WM_CLASS']
                    ).decode()

                    # Extraer clase
                    match = re.search(r'"([^"]+)"', class_name)
                    if match:
                        window_class = match.group(1)
                        print(f"Cambio a: {window_class}")

                        # Aquí puedes tomar acciones automáticas
                        self.handle_window_change(window_class)

                    old_active = active_id

                time.sleep(0.5)
            except:
                time.sleep(1)

    def handle_window_change(self, window_class):
        """Responde a cambios de ventana"""
        # Ejemplo: Si abres terminal, preparar entorno
        if 'konsole' in window_class.lower():
            # Enviar comando automático
            subprocess.run(['xdotool', 'type', 'ollama run deepseek-coder'])
            subprocess.run(['xdotool', 'key', 'Return'])

        # Si abres Chrome, posicionarlo a la derecha
        elif 'chrome' in window_class.lower():
            time.sleep(1)
            subprocess.run(['/home/daniel/tron/control-ventanas/control_ventanas.sh',
                          'organizar', 'chrome', 'derecha'])

# Uso
if __name__ == "__main__":
    controller = WindowController()

    # Ejemplo: Abrir terminal con ollama y organizar pantalla
    controller.split_screen('vscode', 'terminal')

    # Iniciar monitor (en segundo plano)
    import threading
    monitor_thread = threading.Thread(target=controller.monitor_windows, daemon=True)
    monitor_thread.start()
```

### **3. Configuración avanzada en Openbox**
Añade a tu `~/.config/openbox/rc.xml`:

```xml
<!-- En la sección <applications> añade: -->
<applications>
    <!-- Aplicaciones específicas con comportamientos especiales -->
    <application class="Konsole" title=".*ollama.*">
        <desktop>2</desktop>
        <maximized>no</maximized>
        <position>
            <x>0</x>
            <y>0</y>
        </position>
        <size>
            <width>50%</width>
            <height>100%</height>
        </size>
    </application>

    <application class="Google-chrome" title=".*ChatGPT.*">
        <desktop>2</desktop>
        <position>
            <x>50%</x>
            <y>0</y>
        </position>
        <size>
            <width>50%</width>
            <height>100%</height>
        </size>
    </application>
</applications>

<!-- Atajos para control rápido -->
<keyboard>
    <keybind key="C-A-s">
        <action name="Execute">
            <command>/home/daniel/tron/control-ventanas/split_ollama_chrome.sh</command>
        </action>
    </keybind>

    <keybind key="C-A-f">
        <action name="Execute">
            <command>wmctrl -r :ACTIVE: -b toggle,fullscreen</command>
        </action>
    </keybind>
</keyboard>
```

### **4. Script de ejemplo: split_ollama_chrome.sh**
```bash
#!/bin/bash
# Organiza Ollama y Chrome para trabajo con IA

# Abrir terminal con ollama
konsole --new-tab -e "ollama run deepseek-coder" &
sleep 1

# Abrir Chrome
google-chrome-stable "https://chat.deepseek.com" &
sleep 2

# Organizar ventanas
WIN_TERMINAL=$(xdotool search --name "ollama" | tail -1)
WIN_CHROME=$(xdotool search --name "DeepSeek" | tail -1)

if [ -n "$WIN_TERMINAL" ] && [ -n "$WIN_CHROME" ]; then
    # Terminal a la izquierda
    xdotool windowmove "$WIN_TERMINAL" 0 0
    xdotool windowsize "$WIN_TERMINAL" 960 1080

    # Chrome a la derecha
    xdotool windowmove "$WIN_CHROME" 960 0
    xdotool windowsize "$WIN_CHROME" 960 1080

    # Enfocar terminal
    xdotool windowactivate "$WIN_TERMINAL"
fi
```

### **5. Sistema de eventos (opcional)**
Para una integración más profunda:

```python
# event_listener.py
import subprocess
import threading
import queue
import time

class WindowEventSystem:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.handlers = {}

    def start_monitoring(self):
        def monitor():
            process = subprocess.Popen(
                ['xprop', '-spy', '-root', '_NET_ACTIVE_WINDOW'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            for line in process.stdout:
                if '_NET_ACTIVE_WINDOW' in line:
                    self.event_queue.put(('window_change', line))

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    def register_handler(self, event_type, callback):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(callback)

    def process_events(self):
        while True:
            try:
                event = self.event_queue.get(timeout=1)
                event_type, data = event

                if event_type in self.handlers:
                    for handler in self.handlers[event_type]:
                        handler(data)

            except queue.Empty:
                time.sleep(0.1)

# Uso
events = WindowEventSystem()

def on_window_change(data):
    print(f"Ventana cambiada: {data}")
    # Aquí tu lógica con IA

events.register_handler('window_change', on_window_change)
events.start_monitoring()
events.process_events()
```

## **Recomendaciones finales:**

1. **Usa sockets/DBus** para comunicación entre procesos
2. **Crea un servicio systemd** para tu puppeteer
3. **Implementa logs** para debuggear
4. **Usa named pipes** para comunicación simple

¿Te gustaría que desarrolle alguna parte específica más a fondo?
---

## RESUMEN EJECUTIVO

**TRON** representa una **arquitectura de orquestación terminal de ultra alta densidad**, diseñada para maximizar el impacto visual y funcional en demostraciones técnicas profesionales. La clave está en la **integración sin fisuras** entre:

1. **Kitty** como canvas gráfico (vía Remote Control Protocol)
2. **IA Local/Remota** (Ollama/DeepSeek) como cerebro interpretativo
3. **Python** como orquestador de ventanas y lógica de negocio
4. **Openbox** como gestor de ventanas ligero y controlable
5. **Gum/FZF** como capa de interfaz usuario elegante

El comando `tr -p "hablar libre"` encapsula la filosofía: **eficiencia máxima con mínima fricción**, permitiendo al usuario expresar intenciones en lenguaje natural y verlas materializarse en una coreografía de ventanas, colores y comandos que generan el efecto "WOW" deseado en presentaciones corporativas.

La densidad de funcionalidad es comparable a un "buquetanque de petróleo" - máxima capacidad en mínimo espacio, sin sacrificar la eficiencia en la máquina objetivo (8GB RAM, entorno gráfico ligero).
---








# MATERIAL de ayuda y coontexto
---
Soy **Odiseo**. Entendido. La visión es clara: un entorno **Cyberpunk-Funcional (TRON Legacy)** donde la estética se encuentra con la eficiencia brutal. No es solo una terminal, es un **Centro de Comando Orquestado por IA** que manipula ventanas, renderiza multimedia nativa y se autogestiona con dependencias aisladas pero ejecución global.

Procedo a estructurar la respuesta en **5 Iteraciones Estratégicas** para que tu IA CLI construya esto paso a paso.

### Roles Definidos para esta Misión:
1.  **Arquitecto de Entornos de Alto Rendimiento (HPC UI):** Especialista en Kitty, protocolo gráfico, gestión de memoria (SHM) y Openbox.
2.  **Ingeniero de Backend Python/UV:** Encargado del encapsulamiento, gestión de dependencias (`uv`), y el sistema de auto-instalación en `/usr/bin`.
3.  **Integrador de IA Generativa (DeepSeek/Ollama):** Experto en APIs compatibles con OpenAI, *Prompt Caching*, salida JSON estricta y RAG local.

---

### ITERACIÓN 1: El Núcleo del Reactor (Estructura, Dependencias y Auto-Despliegue)

**Objetivo:** Establecer la base del proyecto en `/home/daniel/tron/programas/TR`, configurar el entorno virtual con `uv`, y crear el **Lanzador Maestro** que respeta tu código de auto-instalación, garantizando que el sistema sea portable y no rompa el sistema base.

**Instrucciones para la IA CLI:**

1.  **Inicialización del Proyecto:**
    *   Crear directorio raíz: `mkdir -p ~/tron/programas/TR`.
    *   Inicializar `uv`: `cd ~/tron/programas/TR && uv init`.
    *   Definir `pyproject.toml` con dependencias clave:
        *   `openai` (para DeepSeek/Ollama).
        *   `pyyaml` (configuración).
        *   `sh` o `subprocess` (ejecución de comandos).
        *   `rich` (para salidas visuales en el script Python antes de pasar a Gum).
        *   `ewmh` o `xcffib` (para control avanzado de ventanas Openbox desde Python, más rápido que `wmctrl`).

2.  **El Wrapper de Inmortalidad (Tu Script Mejorado):**
    *   La IA debe tomar tu script `#!/usr/bin/env python3...` y guardarlo como `installer.py`.
    *   **Mejora Táctica:** El script generado en `/usr/bin/` debe inyectar variables de entorno críticas para Kitty y DeepSeek antes de ejecutar el python del entorno virtual.
    *   *Código Concepto para la IA:*
        ```python
        # Fragmento a inyectar en el launcher_content de tu script
        launcher_content = f"""#!/bin/bash
        # TRON LAUNCHER - Generado por 'ini'
        export PROJECT_PATH="{current_dir}"
        export KITTY_LISTEN_ON="unix:/tmp/mykitty"
        export DEEPSEEK_API_KEY="tu_clave_aqui" # O cargar de un .env seguro
        cd "$PROJECT_PATH"
        # Ejecución crítica usando UV para aislamiento total
        exec uv run --project "$PROJECT_PATH" python "$PROJECT_PATH/{target}" "$@"
        """
        ```

3.  **Configuración YAML Centralizada:**
    *   Crear `config.yaml`. Aquí se definirán los "Roles" de la consola (ej: "Modo Presentación", "Modo Hacker", "Modo Debug").
    *   La IA debe leer este YAML para saber qué modelo usar (Ollama local o DeepSeek API) y qué parámetros de temperatura aplicar.

---

### ITERACIÓN 2: La Mente Sintética (Integración DeepSeek/Ollama + Context Caching)

**Objetivo:** Implementar el cerebro que traduce "borra los logs viejos" a `find . -name "*.log" ...`. Usaremos la documentación de DeepSeek que subiste para habilitar el **Context Caching** (ahorro de costes/tiempo) y la salida **JSON**.

**Instrucciones para la IA CLI:**

1.  **Cliente de IA Híbrido:**
    *   Crear módulo `brain.py`.
    *   Debe detectar si el endpoint es `localhost` (Ollama) o `api.deepseek.com`.
    *   **Implementación de DeepSeek Caching:** Según la documentación, el *System Prompt* debe ser idéntico en las primeras partes para que el caché funcione (hit).
    *   *Prompt del Sistema (Inmutable para Cache):*
        "Eres TRON, un asistente de terminal experto en Zsh y Bash para Ubuntu. Tu objetivo es generar comandos eficaces, eficientes y seguros. Respondes SIEMPRE en formato JSON estricto."

2.  **Estructura de Salida JSON:**
    *   Obligar a la IA a responder así para que Python pueda parsearlo sin errores:
        ```json
        {
          "thought": "El usuario quiere borrar logs. Es peligroso, usaré find con -delete pero pediré confirmación.",
          "command": "find . -name '*.log' -mtime +30 -delete",
          "risk_level": "high",
          "explanation": "Borrará recursivamente archivos .log de más de 30 días."
        }
        ```

3.  **Análisis de Repositorios (Inspiración):**
    *   *De `gattino`:* Extraer la lógica de cómo simplifica el prompt del usuario.
    *   *De `terminal-command`:* Ver cómo maneja los errores si la IA alucina un comando que no existe.

---

### ITERACIÓN 3: La Interfaz TRON (Gum + FZF + Zsh Integration)

**Objetivo:** Crear la experiencia de usuario. No basta con imprimir el comando. Debe verse elegante, confirmar con seguridad y permitir edición de último segundo.

**Instrucciones para la IA CLI:**

1.  **El Selector Visual (Gum):**
    *   Usar `subprocess` en Python para llamar a `gum`.
    *   Diseñar un "Confirmador" estilo TRON:
        *   Borde neón (Cyan).
        *   Si `risk_level` es "high" (del JSON de la IA), el borde cambia a Rojo y requiere escribir "CONFIRMAR".
    *   *Flujo:* Usuario input -> IA JSON -> Python parsea -> Gum muestra comando y explicación -> Enter -> Ejecución.

2.  **Integración con Zsh (El Truco del Buffer):**
    *   Para que el comando no se ejecute "a ciegas" sino que se escriba en tu prompt (opcionalmente), usaremos la técnica de `print -z` de Zsh o la inyección directa al historial de Kitty.
    *   *Comando Kitty:* `kitten @ send-text --match "id:..." "comando sugerido"` (sin el enter final, para que el usuario pulse Enter si lo desea, o con `\r` si confiamos ciegamente).

3.  **Feedback Loop:**
    *   Si el comando falla, capturar `stderr`, enviarlo de nuevo a la IA (Ollama/DeepSeek) y decir: "El comando falló con este error, arréglalo". (Auto-healing).

---

### ITERACIÓN 4: El Efecto WOW (Multimedia y Orquestación de Ventanas)

**Objetivo:** Aquí es donde la gente dice "WOW". Control remoto de Kitty, visualización de video/imágenes y movimiento de ventanas Openbox.

**Instrucciones para la IA CLI:**

1.  **Protocolo Remoto de Kitty (Socket):**
    *   Asegurar que `kitty.conf` tenga `allow_remote_control yes` y `listen_on unix:/tmp/mykitty`.
    *   Crear funciones Python en `orchestrator.py` que envuelvan comandos como:
        *   `kitten @ launch --type=tab --tab-title="VIDEO" --location=neighbor`
        *   `kitten @ set-window-layout tall`

2.  **Multimedia Nativa (MPV & ICAT):**
    *   **Video:** La IA debe saber que si el usuario pide "Pon el video de la intro", debe generar:
        `mpv --profile=sw-fast --vo=kitty --vo-kitty-use-shm=yes --really-quiet intro.mkv`
        *Nota:* El uso de SHM (Shared Memory) es vital para la eficiencia que pides.
    *   **Imágenes:** Usar `kitten icat --align=center imagen.png`.

3.  **El Titiritero (Openbox Control):**
    *   Usar `wmctrl` o `xdotool` (invocados desde Python) para mover la ventana de Kitty.
    *   *Escenario:* "IA, muéstrame el gráfico a la derecha".
        1.  Kitty abre nueva ventana OS (`--type=os-window`).
        2.  Python detecta el `window_id`.
        3.  Python ejecuta `wmctrl -ir <id> -e 0,1000,0,800,600` (Mueve la ventana a la derecha de tu pantalla).

---

### ITERACIÓN 5: Documentación Viva y RAG (La Sabiduría Concentrada)

**Objetivo:** Que la IA no solo ejecute, sino que sepa CÓMO usar Kitty y tus herramientas basándose en la documentación que proporcionaste.

**Instrucciones para la IA CLI:**

1.  **Ingesta de Conocimiento:**
    *   Descargar (usando `curl`/`wget` en tiempo de construcción) los README y docs de los repos sugeridos (`ht`, `zev`, `kitty docs`).
    *   Convertir HTML a Markdown (usando `pandoc` o librería python `markdownify`).
    *   Crear un índice vectorial simple (o búsqueda léxica jerárquica como sugeriste) en `~/tron/docs/index`.

2.  **Sistema de Ayuda Inteligente:**
    *   Cuando preguntes "¿Cómo hago un split en Kitty?", la IA no alucina. Consulta `~/tron/docs/layouts.md`, extrae el atajo `Ctrl+Shift+Enter` y te lo muestra.

3.  **Instrucciones Finales de Despliegue:**
    *   La IA generará un script `build_tron.sh` que:
        1.  Instala dependencias del sistema (`kitty`, `zsh`, `gum`, `mpv`, `ffmpeg`, `imagemagick`).
        2.  Clona tu estructura de carpetas.
        3.  Ejecuta tu `installer.py` para vincular todo a `/usr/bin/tr-ai`.

---

### Resumen de la "Bola de Nieve" (Estado Actualizado)

> **[Registro Semántico Comprimido - V2]:**
> Proyecto: **TRON-AI Console**.
> Base: **Ubuntu + Openbox + Kitty** (Socket Control habilitado).
> Núcleo: **Python + UV** (Aislamiento).
> Despliegue: **Autoinstalador en /usr/bin** (Wrapper seguro).
> IA: **Híbrida (Ollama Local / DeepSeek API)** con Context Caching.
> Interfaz: **Gum (TUI)** para confirmación de comandos peligrosos.
> Multimedia: **MPV (Kitty Backend)** y **ICAT** para visualización nativa.
> Orquestación: **Python controla Openbox** para mover ventanas físicamente según contexto.
> Documentación: **RAG Local** basado en repos de GitHub y docs oficiales de Kitty.

Soy **Odiseo**. Recibido. Ajustamos el rumbo: **Nada de RAG activo por ahora**. La prioridad es la **Ingesta Estructurada (Harvesting)**. La IA CLI debe descargar, clasificar y almacenar "paranoicamente" la documentación y los repositorios para que sirvan de *cantera de ideas* y código fuente para el desarrollo actual y futuro, manteniendo la arquitectura abierta para una futura indexación vectorial.

Procedo con las instrucciones detalladas divididas en iteraciones, integrando tu script de instalación y la lógica de "Efecto WOW".

### Roles Ajustados
1.  **Arquitecto de Sistemas & Despliegue (Python/UV):** Encargado de la estructura de carpetas, el entorno virtual y el script de auto-instalación en `/usr/bin`.
2.  **Curador de Conocimiento (Data Harvester):** Encargado de clonar repositorios y descargar documentación técnica en una estructura de directorios rígida ("orden paranoico") para análisis estático.
3.  **Ingeniero de Interfaz & Orquestación (Kitty/Openbox):** Encargado del control por socket, renderizado multimedia (MPV/ICAT) y la manipulación de ventanas.

---

### 1. La Bola de Nieve (Estado Actualizado)
> **[Registro Semántico Comprimido - V3]:**
> Objetivo: **Consola TRON-AI (Ubuntu/Openbox/Kitty)**.
> Núcleo: **Python + UV** (Gestión de dependencias moderna).
> Despliegue: **Script `ini.py`** (Auto-instalador en `/usr/bin` que respeta el entorno).
> Base de Conocimiento: **Estática/Estructurada** (Descarga de repos `ht`, `zev`, `wut` y docs de Kitty a `./Docs` para referencia de código, NO RAG activo aún).
> IA: **Híbrida (DeepSeek API / Ollama Local)** con salida JSON estricta.
> Interfaz: **Gum** (TUI elegante) + **Zsh** (Integración de buffer).
> Multimedia: **MPV** (Flags optimizados para Kitty/SHM) + **ICAT**.
> Control: **Socket Kitty + Openbox** (Orquestación de ventanas).

---

### 2. Plan de Acción: Instrucciones para la IA CLI

#### ITERACIÓN 1: El Cimiento (Estructura, UV y el Lanzador "Ini")

*Instrucción operativa:* Crear la estructura del proyecto y establecer el script de despliegue que garantiza la inmortalidad del comando en el sistema.

1.  **Estructura de Directorios (Orden Paranoico):**
    ```bash
    mkdir -p ~/tron/programas/TR/{src,config,docs/{repos,manuals},logs}
    cd ~/tron/programas/TR
    uv init
    ```

2.  **Dependencias (`pyproject.toml`):**
    Instruye a la IA para añadir estas librerías con `uv add`:
    *   `openai` (Cliente compatible para DeepSeek/Ollama).
    *   `typer` o `click` (Para CLI interna).
    *   `rich` (Salida visual antes de Gum).
    *   `pyyaml` (Configuración).
    *   `sh` (Ejecución de comandos de sistema simplificada).

3.  **El Lanzador Maestro (`ini.py`):**
    La IA debe generar el archivo `ini.py` en la raíz, conteniendo **exactamente** tu lógica, pero asegurando que el *wrapper* bash generado incluya las variables de entorno necesarias para Kitty y la IA.

    *Código a generar por la IA CLI (Basado en tu aporte):*
    ```python
    #!/usr/bin/env python3
    import os
    import sys
    import subprocess
    from pathlib import Path

    # ... [Tu código de detección y validación aquí] ...

    # MODIFICACIÓN CRÍTICA EN EL CONTENIDO DEL LANZADOR:
    # Se inyectan variables de entorno para que la IA sepa dónde está Kitty y las claves
    launcher_content = f"""#!/bin/bash
    # Generado por 'ini' - TRON AI SYSTEM
    export PROJECT_PATH="{current_dir}"
    export KITTY_LISTEN_ON="unix:/tmp/mykitty"
    export DEEPSEEK_API_KEY="${{DEEPSEEK_API_KEY:-tu_clave_por_defecto}}"

    cd "$PROJECT_PATH"
    # Ejecución vía UV para aislamiento total
    exec uv run --project "$PROJECT_PATH" python "$PROJECT_PATH/{target}" "$@"
    """
    # ... [Resto de tu código de instalación en /usr/bin] ...
    ```

#### ITERACIÓN 2: La Cosecha (Descarga de Conocimiento "Paranoica")

*Instrucción operativa:* La IA debe generar un script `harvest.py` (o bash) que descargue y organice los recursos externos. Esto NO es RAG, es "preparar la biblioteca" para que la IA lea código útil.

1.  **Repositorios de Referencia (GitHub):**
    Clonar en `~/tron/programas/TR/docs/repos/`:
    *   `gattino` (Referencia: Chat con LLM en Kitty).
    *   `ht` (Referencia: Wrapper de comandos).
    *   `wut` (Referencia: Explicación de comandos).
    *   `zev` (Referencia: Gestión de terminal).
    *   `terminal-command` (Referencia: Ejecución).
    *   `reTermAI` (Referencia: IA en terminal).
    *   `kitty-smart-tab` (Referencia: Control de pestañas).

2.  **Documentación Oficial (Manuales):**
    Descargar en `~/tron/programas/TR/docs/manuals/`:
    *   **Kitty Conf:** `curl -o kitty_conf.html https://sw.kovidgoyal.net/kitty/conf/`
    *   **Remote Control:** `curl -o remote_control.html https://sw.kovidgoyal.net/kitty/remote-control/`
    *   **Protocolo Gráfico:** `curl -o graphics.html https://sw.kovidgoyal.net/kitty/graphics-protocol/`
    *   **Integraciones:** `curl -o integrations.html https://sw.kovidgoyal.net/kitty/integrations/`

    *Nota:* La IA debe incluir una instrucción para convertir estos HTML a Markdown (usando `pandoc` si está disponible o `html2text`) para facilitar su lectura futura por el sistema.

#### ITERACIÓN 3: El Cerebro (DeepSeek/Ollama + JSON Estricto)

*Instrucción operativa:* Configurar el cliente de IA para que piense en JSON y use el caché de contexto de DeepSeek (según la documentación aportada).

1.  **Configuración del Cliente (`src/brain.py`):**
    *   **Base URL:** `https://api.deepseek.com` (o `localhost:11434` para Ollama).
    *   **Modelo:** `deepseek-chat` (No-thinking mode para rapidez) o `deepseek-reasoner` (Thinking mode para scripts complejos).
    *   **Prompt Caching:** El *System Prompt* debe ser estático y estar al principio para hacer "Cache Hit".

2.  **Prompt del Sistema (Inmutable):**
    ```text
    Eres TRON, un orquestador de terminal en Ubuntu.
    Tu salida debe ser SIEMPRE un objeto JSON válido.
    No incluyas markdown (```json) alrededor.
    Estructura requerida:
    {
      "thought": "Razonamiento breve",
      "command": "Comando exacto a ejecutar",
      "is_dangerous": true/false,
      "explanation": "Explicación corta para el humano",
      "media_type": "none" | "video" | "image"
    }
    ```

#### ITERACIÓN 4: El Efecto WOW (Multimedia y Control de Ventanas)

*Instrucción operativa:* Implementar los scripts que hacen la magia visual y el control remoto.

1.  **Reproductor Multimedia (`src/media.py`):**
    *   Debe construir el comando `mpv` con los flags exactos que solicitaste para rendimiento máximo en Kitty:
    ```python
    def play_video(file_path):
        cmd = [
            "mpv",
            "--profile=sw-fast",
            "--vo=kitty",
            "--vo-kitty-use-shm=yes", # CRÍTICO para eficiencia
            "--really-quiet",
            file_path
        ]
        subprocess.run(cmd)
    ```
    *   Para imágenes: `kitten icat --align=center archivo.jpg`.

2.  **Control Remoto de Kitty (`src/kitty_ctrl.py`):**
    *   Usar `socket` para enviar comandos JSON a Kitty (según la doc `rc_protocol`).
    *   **Funciones clave:**
        *   `new_tab(title, layout)`: Abre pestaña nueva.
        *   `send_text(window_id, text)`: Escribe en la terminal.
        *   `set_layout(layout_name)`: Cambia a 'tall', 'fat', etc.

3.  **Orquestador de Ventanas (Openbox/Python):**
    *   Script que usa `subprocess` para llamar a `wmctrl` o `xdotool`.
    *   *Ejemplo:* "Mueve la ventana actual a la derecha para mostrar el video a la izquierda".

#### ITERACIÓN 5: La Interfaz de Usuario (Gum + Zsh)

*Instrucción operativa:* Unir todo en el comando `tr-ai` (o como lo nombres en el instalador).

1.  **Flujo de Ejecución:**
    *   Usuario escribe: `tr-ai "muestra el video intro.mkv"`
    *   Python (`brain.py`) envía a DeepSeek.
    *   DeepSeek responde JSON: `{"command": "mpv ...", "media_type": "video"}`.
    *   Python detecta `media_type="video"`.
    *   Python usa `kitty_ctrl.py` para abrir una nueva pestaña llamada "CINE".
    *   Python ejecuta el comando `mpv` en esa pestaña.

2.  **Confirmación de Seguridad (Gum):**
    *   Si `is_dangerous` es `true` (ej: `rm -rf`), Python lanza:
        ```bash
        gum confirm "⚠️ PELIGRO: ¿Ejecutar borrado?" && ejecutar || echo "Cancelado"
        ```

### Resumen para tu IA CLI (Copy/Paste)

Copia esto para que tu IA genere el código:

```markdown
## DIRECTIVA DE CONSTRUCCIÓN: PROYECTO TRON-AI

**CONTEXTO:** Sistema de asistencia en terminal Ubuntu/Openbox/Kitty.
**UBICACIÓN:** `~/tron/programas/TR`
**GESTOR:** `uv`
**INSTALADOR:** Script `ini.py` personalizado (provisto por usuario).

**PASO 1: ESTRUCTURA PARANOICA**
Generar script bash para:
1. Crear `~/tron/programas/TR`.
2. Dentro crear: `src`, `config`, `docs/repos`, `docs/manuals`.
3. Ejecutar `uv init`.
4. Añadir dependencias: `openai`, `pyyaml`, `sh`, `rich`.

**PASO 2: EL INSTALADOR (ini.py)**
Generar `ini.py` usando el código exacto del usuario, pero modificando la variable `launcher_content` para exportar:
- `KITTY_LISTEN_ON="unix:/tmp/mykitty"`
- `DEEPSEEK_API_KEY`

**PASO 3: COSECHA DE CONOCIMIENTO (harvest.sh)**
Script para clonar en `docs/repos`:
- https://github.com/salvozappa/gattino
- https://github.com/catallo/ht
- https://github.com/shobrook/wut
- https://github.com/dtnewman/zev
- https://github.com/huss-mo/terminal-command
- https://github.com/pie0902/reTermAI
- https://github.com/yurikhan/kitty-smart-tab

Script para descargar Docs de Kitty en `docs/manuals` (convertir a MD si es posible).

**PASO 4: CEREBRO (src/brain.py)**
Implementar cliente OpenAI (para DeepSeek/Ollama).
- System Prompt: Estático (para Cache Hit), exige JSON estricto.
- Output Schema: `{"thought": str, "command": str, "risk": "low|high", "action_type": "shell|video|image"}`.

**PASO 5: MULTIMEDIA (src/media.py)**
Función para video: Ejecutar `mpv --profile=sw-fast --vo=kitty --vo-kitty-use-shm=yes --really-quiet`.

**PASO 6: INTERFAZ (src/main.py)**
Lógica principal:
1. Recibe input del usuario (sys.argv).
2. Consulta a `brain.py`.
3. Si es comando shell: Muestra con `gum`, si confirma -> ejecuta.
4. Si es video/imagen: Usa socket de Kitty para preparar entorno y ejecuta.
```

Soy **Odiseo**. Recibido y procesado. La incorporación de **Gemma 3 (4b)** altera la táctica de inferencia: su arquitectura multimodal y su plantilla específica (`<start_of_turn>`) requieren un manejo preciso en la capa de "Cerebro". Además, entiendo perfectamente que `ini` es tu herramienta soberana de despliegue (ya instalada en `/usr/bin/ini`); no la tocaremos, la **utilizaremos** para desplegar el nuevo sistema.

La configuración (temperatura, modelo, prompts del sistema) se desacopla del código y pasa estrictamente al `config.yaml`.

Aquí tienes las instrucciones refinadas para tu IA CLI, integrando los nuevos activos y respetando la directiva de URLs obligatorias.

### Roles Ajustados
1.  **Ingeniero de Prompting & Configuración (YAML Architect):** Define la "personalidad" del sistema en archivos estáticos, ajustando las plantillas de Gemma 3 y Qwen.
2.  **Bibliotecario de Código (Repo Harvester):** Ejecuta la descarga "paranoica" de referencias externas.
3.  **Operador de Despliegue (Ini Operator):** Prepara el proyecto para ser sellado y entregado al sistema mediante tu comando `ini`.

---

### 1. La Bola de Nieve (Estado Actualizado V4)
> **[Registro Semántico Comprimido]:**
> Proyecto: **TRON-AI Console**.
> Ubicación: `~/tron/programas/TR`.
> Motor IA: **Ollama Local** (Prioridad: `gemma3:4b`, `qwen2.5`, `phi4-mini`) o **DeepSeek API**.
> Configuración: Centralizada en `config.yaml` (Modelos, Templates, Temperatura).
> Despliegue: Uso del comando existente `/usr/bin/ini` (Python Wrapper).
> Base de Conocimiento: Descarga estática de repositorios y manuales a `./docs`.
> Interfaz: **Gum** + **Kitty Socket** + **Openbox**.
> Multimedia: MPV optimizado para Kitty.

---

### 2. Plan de Acción: Instrucciones para la IA CLI

#### ITERACIÓN 1: El Cerebro Configurable (YAML + Gemma 3)

*Instrucción operativa:* Crear el archivo de configuración que gobierna el comportamiento de la IA sin tocar el código Python. Aquí se define la plantilla de Gemma 3.

**Archivo:** `~/tron/programas/TR/config/settings.yaml`

```yaml
system:
  name: "TRON_AI"
  version: "1.0.0"
  debug: false

llm:
  # Opciones: ollama, deepseek
  provider: "ollama"
  # Modelos disponibles en tu sistema: gemma3:4b, qwen2.5:3b, phi4-mini:latest
  model: "gemma3:4b"
  base_url: "http://localhost:11434"
  temperature: 0.7
  # Context window para Gemma 3
  num_ctx: 8192

  # Configuración específica para JSON Mode (Ollama soporta format='json')
  format: "json"

prompts:
  # El System Prompt inmutable para caché y personalidad
  main_system: |
    Eres un asistente de terminal experto en Ubuntu, Zsh y Kitty.
    Tu objetivo es generar comandos JSON precisos.
    No expliques nada fuera del JSON.
    Estructura de respuesta: {"thought": "...", "command": "...", "risk": "low|high"}

templates:
  # Referencia de la plantilla oficial de Gemma 3 para uso en modo raw si fuera necesario
  gemma3: |
    <start_of_turn>user
    {prompt}<end_of_turn>
    <start_of_turn>model
```

#### ITERACIÓN 2: El Motor de Inferencia (`src/brain.py`)

*Instrucción operativa:* El script Python debe leer el YAML. Si usa Ollama, debe aprovechar el endpoint `/api/chat` que maneja las plantillas automáticamente, pero inyectando los parámetros del YAML.

*Lógica para la IA CLI:*
1.  Cargar `config/settings.yaml`.
2.  Inicializar cliente (usando librería `openai` compatible con Ollama o `requests` directo a la API documentada).
3.  **Manejo de Gemma 3:** Aunque Ollama aplica el template automáticamente en `/api/chat`, el script debe asegurar que el `system message` se pase correctamente según la documentación de la API de Ollama (algunos modelos pequeños requieren que el system prompt vaya en el primer mensaje del usuario si no soportan el rol 'system' nativamente, aunque Gemma 3 suele soportarlo).

*Snippet conceptual para `src/brain.py`:*
```python
import yaml
import os
from openai import OpenAI

# Cargar Configuración
with open("../config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

client = OpenAI(
    base_url=f"{config['llm']['base_url']}/v1",
    api_key="ollama", # Requerido pero no usado
)

def ask_tron(user_input):
    response = client.chat.completions.create(
        model=config['llm']['model'],
        messages=[
            {"role": "system", "content": config['prompts']['main_system']},
            {"role": "user", "content": user_input}
        ],
        temperature=config['llm']['temperature'],
        response_format={"type": "json_object"} # Forzar JSON
    )
    return response.choices[0].message.content
```

#### ITERACIÓN 3: La Cosecha Paranoica (Descarga de Recursos)

*Instrucción operativa:* Generar el script `harvest.sh` que descarga **obligatoriamente** las URLs proporcionadas para análisis estático. La IA debe saber que estos repositorios contienen la "sabiduría" de cómo manejar la terminal.

**Script:** `~/tron/programas/TR/harvest.sh`

```bash
#!/bin/bash
# TRON HARVESTER - Recolección de Inteligencia
# Este script descarga repositorios y documentación clave para el contexto de la IA.

DOCS_DIR="$HOME/tron/programas/TR/docs"
mkdir -p "$DOCS_DIR/repos" "$DOCS_DIR/manuals" "$DOCS_DIR/models"

echo "📥 Descargando Repositorios de Referencia (GitHub)..."

# Herramientas de IA en Terminal (Ideas de código)
git clone https://github.com/salvozappa/gattino "$DOCS_DIR/repos/gattino"
git clone https://github.com/catallo/ht "$DOCS_DIR/repos/ht"
git clone https://github.com/shobrook/wut "$DOCS_DIR/repos/wut"
git clone https://github.com/dtnewman/zev "$DOCS_DIR/repos/zev"
git clone https://github.com/huss-mo/terminal-command "$DOCS_DIR/repos/terminal-command"
git clone https://github.com/pie0902/reTermAI "$DOCS_DIR/repos/reTermAI"

# Control de Pestañas Kitty (Esencial para el orquestador)
git clone https://github.com/yurikhan/kitty-smart-tab "$DOCS_DIR/repos/kitty-smart-tab"

echo "📥 Descargando Documentación de Modelos (Contexto)..."
# Guardar referencias de los modelos que vamos a usar
echo "https://ollama.com/library/gemma3:4b" > "$DOCS_DIR/models/gemma3_ref.txt"
echo "https://ollama.com/library/gemma3:4b/blobs/e0a42594d802" >> "$DOCS_DIR/models/gemma3_ref.txt"

echo "📥 Descargando Manuales de Kitty (HTML -> MD)..."
# Aquí la IA debería implementar la conversión si tiene pandoc, sino descarga raw
curl -s https://sw.kovidgoyal.net/kitty/conf/ > "$DOCS_DIR/manuals/kitty_conf.html"
curl -s https://sw.kovidgoyal.net/kitty/remote-control/ > "$DOCS_DIR/manuals/remote_control.html"
curl -s https://sw.kovidgoyal.net/kitty/overview/#layouts > "$DOCS_DIR/manuals/layouts.html"
curl -s https://sw.kovidgoyal.net/kitty/kittens/hints/ > "$DOCS_DIR/manuals/hints.html"

echo "✅ Cosecha completada. Ejecuta el indexador (futuro RAG)."
```

#### ITERACIÓN 4: El Despliegue con `ini`

*Instrucción operativa:* Una vez que el código (`src/`), la configuración (`config/`) y la documentación (`docs/`) estén listos, se utiliza tu herramienta `ini`.

**Instrucciones para el Usuario (Simulación):**

1.  Asegúrate de estar en la carpeta del proyecto:
    `cd ~/tron/programas/TR`
2.  Verifica que `pyproject.toml` existe (creado por `uv init`).
3.  Ejecuta tu comando maestro:
    `ini`
4.  El script `ini` te preguntará:
    *   *Script original:* `src/main.py` (o el punto de entrada que definas).
    *   *Nombre global:* `tr-ai` (o `tron`).
5.  `ini` creará el wrapper en `/usr/bin/tr-ai` inyectando el entorno `uv` automáticamente.

---

### 3. Resumen de URLs Obligatorias (Contexto Documental)

La IA CLI debe incluir estas referencias en el archivo `README.md` generado dentro del proyecto `TR` bajo la sección "Fuentes de Conocimiento":

**Repositorios de Código (Inspiración):**
*   [Gattino (Chat en Kitty)](https://github.com/salvozappa/gattino)
*   [ht (Wrapper de comandos)](https://github.com/catallo/ht)
*   [wut (Explicación CLI)](https://github.com/shobrook/wut)
*   [zev (Gestión terminal)](https://github.com/dtnewman/zev)
*   [terminal-command](https://github.com/huss-mo/terminal-command)
*   [reTermAI](https://github.com/pie0902/reTermAI)
*   [Kitty Smart Tab](https://github.com/yurikhan/kitty-smart-tab)

**Documentación Técnica Kitty:**
*   [Configuración](https://sw.kovidgoyal.net/kitty/conf/)
*   [Control Remoto](https://sw.kovidgoyal.net/kitty/remote-control/)
*   [Protocolo RC](https://sw.kovidgoyal.net/kitty/rc_protocol/)
*   [Layouts](https://sw.kovidgoyal.net/kitty/layouts)
*   [Kittens Intro](https://sw.kovidgoyal.net/kitty/kittens_intro)
*   [Hints](https://sw.kovidgoyal.net/kitty/kittens/hints/)
*   [SSH Kitten](https://sw.kovidgoyal.net/kitty/kittens/ssh/)
*   [Integraciones](https://sw.kovidgoyal.net/kitty/integrations/)
*   [Marks](https://sw.kovidgoyal.net/kitty/marks/)

**Modelos LLM (Ollama Library):**
*   [Gemma 3 (4b)](https://ollama.com/library/gemma3:4b) - *Template Blob: e0a42594d802*
*   [Qwen 2.5](https://ollama.com/library/qwen2.5)
*   [Phi-4 Mini](https://ollama.com/library/phi4-mini)

---

### 4. Ejecución Final (Prompt para tu IA CLI)

Copia esto para generar los archivos finales:

```markdown
## DIRECTIVA DE CONSTRUCCIÓN FINAL: TRON-AI (GEMMA 3 EDITION)

**OBJETIVO:** Generar sistema de asistencia en terminal usando `uv`, `kitty` y `ollama`.
**DEPLOY:** Usar comando existente `ini`.

**TAREA 1: CONFIGURACIÓN (config/settings.yaml)**
Generar YAML con:
- Provider: ollama
- Model: gemma3:4b
- Temp: 0.7
- System Prompt: "Eres TRON. Responde JSON estricto: {thought, command, risk}."

**TAREA 2: COSECHADOR (harvest.sh)**
Script bash que hace `git clone` y `curl` de TODAS las URLs listadas en la sección "Resumen de URLs Obligatorias" del plan estratégico. Guardar en `~/tron/programas/TR/docs`.

**TAREA 3: CÓDIGO FUENTE (src/)**
- `brain.py`: Cliente OpenAI apuntando a localhost:11434/v1. Leer config del YAML.
- `media.py`: Wrapper para `mpv --vo=kitty --vo-kitty-use-shm=yes`.
- `main.py`: Lógica de Gum + Ejecución.

**TAREA 4: INSTRUCCIONES AL USUARIO**
"Ejecuta `uv sync` para instalar dependencias. Luego ejecuta `ini`, selecciona `src/main.py` y nombra el comando `tr-ai`."
```




# TRON: Análisis Voraz de Requerimientos del Sistema

## Contexto del Proyecto

**TRON** (Terminal Remote Operations Nexus) es un sistema de orquestación de terminales Kitty diseñado para crear demostraciones "WOW" en entornos corporativos. El sistema permite a una IA (Ollama/DeepSeek) controlar múltiples terminales, ventanas y aplicaciones mediante comandos naturales, generando una experiencia visual impactante de "entorno hacker" profesional.

---

## 1. REQUERIMIENTOS DE ARQUITECTURA BASE (1-10)

### 1.1 Estructura de Directorios Paranoicamente Ordenada
- **Ruta base**: `/home/daniel/tron/programas/TR/`
- **Estructura obligatoria**: Todo el código debe residir en carpetas jerárquicas estrictamente organizadas
- **Excepción única**: El archivo README puede estar en la raíz; todo lo demás en subcarpetas
- **Documentación**: Todo en `/docs` con conversión automática HTML→Markdown de referencias de Kitty

### 1.2 Gestión de Dependencias UV
- **Sistema de build**: UV (Python package manager) obligatorio
- **Configuración**: Archivos `pyproject.toml` en cada proyecto
- **Entornos virtuales**: Aislados pero accesibles desde `/usr/bin/`

### 1.3 Instalación Global Segura
- **Wrapper de shell**: Los ejecutables en `/usr/bin/` deben ser wrappers bash que redirijan a UV
- **Preservación de contexto**: No desconexión de entornos, configuraciones o bases de datos al mover a `/usr/bin/`
- **Script de referencia**: Usar lógica del script `ini` proporcionado (detección de proyecto UV, generación de lanzadores)

### 1.4 Compatibilidad Shell Maximizada
- **Cabeceras**: Todos los scripts Zsh deben usar shebang `#!/bin/bash` para máxima compatibilidad
- **Conversión automática**: La IA CLI debe convertir sources de scripts Zsh a Bash cuando sea necesario
- **Entorno**: Zsh + Oh My Zsh como shell interactivo, Bash para scripts de sistema

### 1.5 Configuración YAML Centralizada
- **Formato**: Todas las configuraciones en YAML (no JSON)
- **Ubicación**: `/home/daniel/tron/config/`
- **Jerarquía**: Configuración global → por proyecto → por sesión

### 1.6 Base de Datos Local (Opcional pero preparada)
- **Requisito**: El sistema debe soportar SQLite local sin romper al mover a `/usr/bin/`
- **Path resolución**: Usar rutas absolutas o variables de entorno `TRON_HOME`

### 1.7 Logging Estructurado
- **Formato**: JSON Lines para facilitar parsing por la IA
- **Rotación**: Automática por sesión con timestamps ISO 8601
- **Ubicación**: `/home/daniel/tron/logs/`

### 1.8 Sistema de Plugins/Extensiones
- **Arquitectura**: Cargar dinámicamente "gatitos" (kittens) de Kitty personalizados
- **Referencia**: Estudiar estructura de `gattino` (github.com/salvozappa/gattino)
- **Prioridad**: Los gatitos son tercer orden de importancia (después de control remoto y ventanas)

### 1.9 Seguridad por Contraseñas de Control Remoto
- **Implementación**: `remote_control_password` en kitty.conf con granularidad por acción
- **Autenticación**: Passwords diferentes para diferentes niveles de control (colores, ventanas, ejecución)
- **Encriptación**: Soporte para comunicación cifrada vía ECDH+X25519 para uso sobre SSH

### 1.10 Sistema de Sesiones Persistente
- **Formato**: Kitty sessions nativas
- **Funcionalidad**: Guardar y restaurar layouts completos de ventanas, tabs y aplicaciones
- **Identificación**: Cada ventana/tab debe tener metadatos de sesión para matching posterior

---

## 2. REQUERIMIENTOS DE TERMINAL KITTY (11-25)

### 2.1 Control Remoto Total vía Socket
- **Activación**: `allow_remote_control=yes` + `--listen-on unix:/tmp/tron-kitty`
- **Protocolo**: Uso extensivo de `kitten @` para todos los comandos
- **Matching sofisticado**: Por título, ID, cwd, cmdline, env vars, estado (active/focused)
- **Operaciones soportadas**: launch, focus-window, focus-tab, send-text, close-window, set-colors, etc.

### 2.2 Sistema de Ventanas Inteligente
- **Tipos soportados**: window, tab, os-window, overlay, overlay-main, background
- **Títulos configurables**: Cada ventana/tab debe tener nombre descriptivo seteable vía `kitten @ set-window-title` / `set-tab-title`
- **Colores dinámicos**: Cambio de esquemas de color vía `kitten @ set-colors` para efectos visuales
- **Opacidad**: Soporte para `dynamic_background_opacity` con ajuste en tiempo real

### 2.3 Layouts Avanzados
- **Layouts soportados**: tall, fat, grid, splits, horizontal, vertical, stack
- **Control**: Cambio dinámico vía `kitten @ goto-layout`
- **Bias de tamaño**: Ajuste proporcional de ventanas con `--bias` (0-100)
- **Posicionamiento**: Control preciso con `--location` (after, before, vsplit, hsplit)

### 2.4 Reproducción Multimedia Integrada
- **Video**: `mpv --profile=sw-fast --vo=kitty --vo-kitty-use-shm=yes --really-quiet`
- **Calidad**: Excelente resolución sin negociación (eficiencia máxima)
- **Formatos**: MKV, MP4, y streams soportados por mpv
- **Integración**: Lanzar videos en ventanas específicas con títulos descriptivos

### 2.5 Visualización de Imágenes y Documentos
- **Imágenes**: `kitten icat` para mostrar imágenes directamente en terminal
- **PDFs**: Integración con termpdf.py, tdf, fancy-cat, o meowpdf
- **Markdown**: presenterm o mdfried para slides con imágenes
- **Gráficos**: Soporte para matplotlib, gnuplot con backends Kitty

### 2.6 Integración Shell Sophisticada
- **Features requeridas**:
  - Navegación por prompts con Ctrl+Shift+Z/X
  - Click para posicionar cursor en comandos
  - Ctrl+Shift+Click derecho para ver output en pager
  - Clonado de shell con env vars y cwd copiados
  - Edición de archivos en nuevas ventanas incluso vía SSH
- **Marcadores**: Sistema de `marks` para resaltar texto (ERRORES, WARNINGS, etc.)

### 2.7 SSH y Transferencias
- **Kitten SSH**: Uso de `kitten ssh` para preservar funcionalidades avanzadas
- **Transferencia de archivos**: `kitten transfer` con confirmación automática desactivable
- **Remote file**: Edición de archivos remotos en ventanas locales

### 2.8 Hints y Navegación
- **URL hints**: `kitten hints` para abrir URLs, copiar al clipboard
- **Hyperlinked grep**: Integración con ripgrep para output clickeable
- **Selección de texto**: kitty-grab para selección keyboard-based en scrollback

### 2.9 Paneles de Escritorio (Opcional WOW)
- **Kitty panel**: Crear paneles de sistema con métricas en tiempo real
- **Posicionamiento**: Top, bottom, left, right vía `--os-panel`
- **Integración**: Con Openbox para paneles flotantes o docked

### 2.10 Configuración Programática
- **Reload**: `kitten @ load-config` para recargar configuración sin reiniciar
- **Overrides**: Soporte para `-o` flags en comandos de lanzamiento
- **Fuentes**: Cambio de tamaño dinámico con `kitten @ set-font-size`

---

## 3. REQUERIMIENTOS DE ORQUESTACIÓN DE VENTANAS (26-40)

### 3.1 Puppet Master en Python
- **Tecnología**: Python 3.9+ con comunicación directa a Kitty vía sockets Unix
- **Alternativas evaluadas**: pyvda (Windows), wmctrl/xdotool (X11), pero preferir native Kitty RC
- **Función**: Recibir señales de la IA y traducir a comandos `kitten @`

### 3.2 Protocolo de Comandos IA→Orquestador
- **Formato**: JSON con campos estandarizados:
  ```json
  {
    "action": "focus|launch|move|resize|close",
    "target": "nombre_ventana_o_match",
    "position": "center|left|right|fullscreen",
    "command": "comando_a_ejecutar",
    "priority": "high|normal|low"
  }
  ```

### 3.3 Gestión de Foco Dinámica
- **Efecto "traer al frente"**: La IA debe poder enfocar cualquier ventana/tab específica
- **Historial de foco**: Mantener stack de ventanas recientes para "volver atrás"
- **Transiciones**: Instantáneas (Openbox es ligero) pero visibles

### 3.4 Posicionamiento Absoluto/Relativo
- **Coordenadas**: Soporte para posicionamiento por porcentaje de pantalla
- **Espacios de trabajo**: Integración con Openbox para mover entre desktops virtuales
- **Z-order**: Control de elevación de ventanas (raise/lower)

### 3.5 Lanzamiento de Aplicaciones con Contexto
- **Simples**: Comandos de una línea con `;` separadores
- **Compuestas**: Scripts multi-línea con heredocs
- **Entorno**: Preservación de variables de entorno entre ventanas
- **Identificación**: Cada app lanzada debe tener ID único trackeable

### 3.6 Control de Tabs Múltiples
- **Nomenclatura**: Tabs con nombres descriptivos (no numéricos)
- **Switching**: Cambio instantáneo entre tabs vía `kitten @ focus-tab --match title:xxx`
- **Colores**: Tabs con colores diferentes para diferenciación visual

### 3.7 Broadcasting y Sincronización
- **Broadcast**: Enviar mismo comando a múltiples ventanas simultáneamente
- **Sincronización**: Ejecutar comandos en secuencia específica entre ventanas
- **Esperas**: Sincronización con `wait-for-child-to-exit` cuando sea necesario

### 3.8 Overlay Windows Estratégicas
- **Uso**: Ventanas temporales para confirmaciones, inputs, o displays de estado
- **Tipos**: overlay (modal) vs overlay-main (persistente)
- **Integración**: No interferir con el flujo principal pero permitir interacción

### 3.9 Detección de Estado de Ventanas
- **Query**: `kitten @ ls` para obtener estado completo del árbol de ventanas
- **Parsing**: JSON parseable para tomar decisiones basadas en estado actual
- **Eventos**: Watchers para reaccionar a cambios (resize, focus, close)

### 3.10 Integración Openbox Específica
- **Comandos**: `openbox --action` para control de ventanas a nivel WM
- **Propiedades**: WM_CLASS, WM_NAME seteables para reglas de Openbox
- **Posicionamiento**: Uso de `wmctrl` como fallback si native RC no alcanza

---

## 4. REQUERIMIENTOS DE INTERFAZ IA Y CLI (41-55)

### 4.1 Trigger de Invocación Simplificado
- **Formato**: `?? "comando en lenguaje natural"` (doble signo de interrogación)
- **Alternativas descartadas**: `?` simple puede ser confuso; `??` es explícito y único
- **Contexto**: El usuario escribe `??` seguido de descripción en español o inglés

### 4.2 Pipeline de Procesamiento IA
1. **Input**: `?? "borrar logs de más de 30 días"`
2. **Envío**: Prompt a Ollama (local) o DeepSeek (API)
3. **Generación**: Comando shell propuesto
4. **Confirmación**: Interfaz con Gum (Charm.sh) o similar para validación
5. **Ejecución**: Vía Orquestador Python a Kitty

### 4.3 Interfaz de Confirmación Elegante
- **Tecnología**: Gum (gum confirm, gum input, gum spin) de Charm.sh
- **Estilo**: Minimalista, colores consistentes con esquema de terminal
- **Opciones**:
  - Enter para confirmar
  - Esc para cancelar
  - 'e' para editar comando antes de ejecutar
  - 'x' para ejecutar con privilegios elevados (sudo)

### 4.4 Historial y Contexto Conversacional
- **Memoria**: Últimos N comandos y sus outputs para contexto
- **Referencias**: `!!` para repetir último comando, `!n` para el enésimo
- **Explicación**: Comando `explain` para que la IA explique qué hace un comando

### 4.5 Detección de Intenciones Avanzada
- **Análisis profundo**: No solo mapeo directo, sino inferencia de contexto
- **Ejemplos**:
  - "muestra el video" → detectar archivo video reciente o en cwd
  - "abre el proyecto" → detectar proyecto git en cwd o subdirectorios
  - "conecta al servidor" → usar SSH kitten con último host conocido

### 4.6 Manejo de Errores Inteligente
- **Captura**: Si un comando falla, capturar stderr automáticamente
- **Diagnóstico**: Enviar error a la IA para sugerir fix
- **Recuperación**: Opción de "arreglar y reintentar" o "deshacer"

### 4.7 Autocompletado Contextual
- **Fuentes**: Historial de comandos, archivos en cwd, hosts SSH conocidos
- **Integración**: Con shell nativo (zsh completions) y con interfaz Gum
- **Previsualización**: Mostrar efecto esperado antes de ejecutar

### 4.8 Modos de Ejecución
- **Seguro**: Solo muestra comando, no ejecuta (default para comandos destructivos)
- **Asistido**: Muestra y pide confirmación (default general)
- **Directo**: Ejecuta inmediatamente (para comandos whitelistados)
- **Batch**: Acumula comandos y ejecuta secuencia con una confirmación

### 4.9 Integración con Sistemas Externos
- **Ollama**: Endpoint local `http://localhost:11434`
- **DeepSeek**: API remota con streaming de respuestas
- **Modelos locales**: Soporte para modelos quantizados vía llama.cpp
- **Fallback**: Si Ollama no responde, usar comando predefinido o pedir input manual

### 4.10 Sistema de "Wut" Integrado
- **Función**: Explicar output de último comando automáticamente
- **Trigger**: `wut` o automático cuando se detecta error
- **Contexto**: Captura de scrollback vía `kitten @ get-text --extent last_cmd_output`
- **Presentación**: En ventana overlay o split

---

## 5. REQUERIMIENTOS DE EXPERIENCIA VISUAL WOW (56-70)

### 5.1 Demostración de Salón/Conferencia
- **Escenario**: Usuario en reunión corporativa abre terminal y ejecuta `kv` (kitty visualizer)
- **Efecto**: Apertura instantánea de múltiples tabs preconfiguradas con nombres descriptivos
- **Contenido**: Cada tab muestra diferentes aspectos (logs, monitoreo, código, multimedia)

### 5.2 Apertura por Socket con Nombres
- **Comando**: `kv` o `tron start` abre Kitty con socket específico
- **Configuración**: Tabs predefinidas en YAML (nombre, comando, layout, colores)
- **Ejecución**: Comandos iniciales se ejecutan automáticamente en cada tab

### 5.3 Posicionamiento Cinematográfico
- **Grid de presentación**: Layouts predefinidos para diferentes tipos de demo
  - "code-review": 3 ventanas (código, tests, diff)
  - "monitoring": 4 ventanas (logs, métricas, alertas, terminal)
  - "multimedia": Video grande + controles + info
- **Transiciones**: Cambio de layouts suave pero perceptible

### 5.4 Visualización de Código con Estilo
- **Syntax highlighting**: En terminal vía `bat` o similar
- **Diffs**: Side-by-side con colores vía `delta`
- **Imágenes**: Mostrar diagramas de arquitectura vía `kitten icat`

### 5.5 Efectos de Color y Animación
- **Cambios de tema**: Transición de colores para indicar estados (verde=OK, rojo=error, azul=procesando)
- **Pulsos**: Cambio temporal de background color para alertas
- **Gradientes**: Opacidad variable para crear profundidad visual

### 5.6 Branding Personalizado
- **Logos**: `kitten @ set-window-logo` con logo del proyecto/corporación
- **Fondos**: Imágenes de fondo sutil con `kitten @ set-background-image`
- **Fuentes**: Tamaños variables para jerarquía visual (títulos grandes, código mediano, logs pequeños)

### 5.7 Interacción en Tiempo Real
- **Input simultáneo**: Escribir en una ventana y ver reflejo en otra (para comparaciones)
- **Broadcast typing**: Modo donde lo que se escribe va a todas las ventanas
- **Follow mode**: Una ventana sigue el foco de otra automáticamente

### 5.8 Captura y Replay de Sesiones
- **Grabación**: Guardar secuencia de comandos y sus outputs
- **Replay**: Reejecutar sesión paso a paso con pausas
- **Edición**: Modificar sesiones grabadas para crear demos perfectas

### 5.9 Integración con File Managers TUI
- **Ranger/nnn/Yazi**: Abrir en ventana dedicada con previews activados
- **Navegación**: Selección de archivo en FM → acción en otra ventana (editar, ver, ejecutar)
- **Sincronización**: CWD compartido entre FM y terminal de comandos

### 5.10 Dashboards de Sistema
- **Paneles**: Uso de `kitty-panel` o implementación propia
- **Métricas**: CPU, memoria, red, procesos en tiempo real
- **Visualización**: Gráficos ASCII o con `gnuplot`/`matplotlib` en terminal

---

## 6. REQUERIMIENTOS DE REFERENCIA Y ESTUDIO (71-80)

### 6.1 Repositorios Obligatorios de Estudio
Debes descargar, leer y extraer ideas de código de:

1. **gattino** (github.com/salvozappa/gattino) - Integración Kitty+LLM
2. **ht** (github.com/catallo/ht) - Shell helper con AI, bajo uso de tokens
3. **wut** (github.com/shobrook/wut) - Explicación de output de comandos
4. **zev** (github.com/dtnewman/zev) - Generación de comandos con confirmación
5. **terminal-command** (github.com/huss-mo/terminal-command) - CLI Python para comandos IA
6. **reTermAI** (github.com/pie0902/reTermAI) - Terminal AI assistant

### 6.2 Documentación Kitty a Convertir
Todas estas URLs deben descargarse y convertirse a Markdown en `/docs/`:

- Remote control: https://sw.kovidgoyal.net/kitty/remote-control/
- RC Protocol: https://sw.kovidgoyal.net/kitty/rc_protocol/
- Integrations: https://sw.kovidgoyal.net/kitty/integrations/
- Overview: https://sw.kovidgoyal.net/kitty/overview/
- Layouts: https://sw.kovidgoyal.net/kitty/layouts/
- Kittens intro: https://sw.kovidgoyal.net/kitty/kittens_intro/
- Hints kitten: https://sw.kovidgoyal.net/kitty/kittens/hints/
- SSH kitten: https://sw.kovidgoyal.net/kitty/kittens/ssh/
- Transfer kitten: https://sw.kovidgoyal.net/kitty/kittens/transfer/
- Hyperlinked grep: https://sw.kovidgoyal.net/kitty/kittens/hyperlinked_grep/
- Remote file: https://sw.kovidgoyal.net/kitty/kittens/remote_file/
- Open actions: https://sw.kovidgoyal.net/kitty/open_actions/
- Shell integration: https://sw.kovidgoyal.net/kitty/shell-integration/
- Marks: https://sw.kovidgoyal.net/kitty/marks/
- FAQ: https://sw.kovidgoyal.net/kitty/faq/

### 6.3 Herramientas de UI Recomendadas
- **Gum**: Para interfaces interactivas elegantes (confirmaciones, inputs, spinners)
- **FZF**: Para fuzzy finding de comandos, archivos, hosts
- **Zellij**: Alternativa a tmux/screen si se necesita multiplexación adicional
- **Starship**: Prompt personalizado con información de contexto

### 6.4 Eficiencia y Rendimiento
- **Consumo memoria**: Sistema completo debe funcionar en máquina con 8GB RAM (0.5GB base + 7.5GB disponibles)
- **Latencia**: Respuesta de IA < 2s para comandos simples
- **Paralelismo**: Múltiples ventanas no deben bloquearse mutuamente
- **Optimización**: Uso de `--profile=sw-fast` para mpv y flags similares para máxima eficiencia

---

## 7. REQUERIMIENTOS DE IMPLEMENTACIÓN ESPECÍFICA (81-90)

### 7.1 Wrapper de Ejecución Segura
```bash
#!/bin/bash
# Ejemplo de wrapper generado por 'ini' para TRON
PROJECT_PATH="/home/daniel/tron/programas/TR"
cd "$PROJECT_PATH"
exec uv run --project "$PROJECT_PATH" python "$PROJECT_PATH/tron/main.py" "$@"
```

### 7.2 Sistema de Configuración por Defecto
- **kitty.conf base**: Con `allow_remote_control=yes`, `enabled_layouts=all`, `dynamic_background_opacity yes`
- **listen_on**: `unix:/tmp/tron-${USER}-$$` (socket único por sesión)
- **remote_control_password**: Al menos 3 niveles (viewer, operator, admin)

### 7.3 Módulos Python Requeridos
- `kitty-rc`: Cliente Python para protocolo RC (o uso directo de subprocess a `kitten @`)
- `ollama`: Cliente Python para API local
- `openai`: Cliente para DeepSeek u otros compatibles
- `pydantic`: Validación de configuraciones y protocolos
- `rich`: Formato de salida en terminal (tablas, colores, markdown)
- `typer`: CLI framework para comandos principales

### 7.4 Estructura de Proyecto Sugerida
```
/home/daniel/tron/
├── config/
│   ├── kitty/
│   ├── tron.yaml
│   └── sessions/
├── docs/
│   ├── kitty-remote-control.md
│   ├── kitty-integrations.md
│   └── ...
├── logs/
├── programas/
│   └── TR/
│       ├── pyproject.toml
│       ├── src/
│       │   ├── tron/
│       │   │   ├── __init__.py
│       │   │   ├── cli.py
│       │   │   ├── orchestrator.py
│       │   │   ├── ai_client.py
│       │   │   ├── kitty_controller.py
│       │   │   └── kittens/
│       │   └── kittens/
│       │       ├── __init__.py
│       │       ├── smart_tab.py
│       │       └── ...
│       └── tests/
└── wrappers/
    └── tron (script bash generado)
```

### 7.5 Sistema de Plantillas de Comandos
- **Formato**: Jinja2 para prompts a la IA
- **Variables**: `{cwd}`, `{history}`, `{selection}`, `{last_output}`
- **Contexto**: Inyección de contexto de ventanas cercanas en el prompt

### 7.6 Manejo de Errores de Conexión
- **Reintentos**: 3 intentos con backoff exponencial para llamadas a IA
- **Fallbacks**: Si Ollama cae, usar comando shell predefinido o mostrar ayuda estática
- **Timeouts**: 10s para comandos locales, 30s para generación IA

### 7.7 Sistema de Plugins/Extensions
- **Entry points**: Plugins registrados en `pyproject.toml` o directorio `plugins/`
- **API**: Clase base `TronPlugin` con métodos `on_launch`, `on_command`, `on_focus`
- **Ejemplos**: Plugin para Docker, Git, Kubernetes con comandos específicos

### 7.8 Testing y Calidad
- **Unit tests**: pytest con cobertura > 80%
- **Integration tests**: Scripts de prueba que abren Kitty real y verifican comportamiento
- **Linting**: ruff, mypy para type checking estricto
- **Pre-commit**: Hooks para formateo y validación de YAML

### 7.9 Documentación de Usuario
- **README**: En raíz, explicando instalación y uso básico
- **Guía de inicio rápido**: Comandos esenciales para primera demo
- **Referencia completa**: Todos los comandos y opciones en `/docs/`
- **Ejemplos**: Scripts de ejemplo para escenarios comunes (demo de logs, demo de código, etc.)

### 7.10 Licenciamiento y Atribución
- **Licencia**: MIT o GPL-3.0 (compatible con Kitty)
- **Atribuciones**: Reconocimiento a Kitty, Ollama, Gum, y proyectos referenciados
- **Contribuciones**: Guía clara para contribuir, código de conducta

---

## 8. REQUERIMIENTOS DE ESCALABILIDAD Y FUTURO (91-100)

### 8.1 Soporte para Múltiples Monitores
- **Detección**: Identificar displays disponibles vía xrandr o similar
- **Distribución**: Enviar ventanas a monitores específicos por nombre o posición
- **Sincronización**: Comandos que afecten múltiples displays simultáneamente

### 8.2 Integración con Editores
- **Neovim**: Plugin para comunicación bidireccional (como vim-slime pero nativo)
- **VSCode**: Extensión que se comunique con daemon TRON
- **Emacs**: Integración vía elisp para control de ventanas Kitty

### 8.3 Soporte para Wayland
- **Compatibilidad**: Asegurar que funciones bajo Wayland (no solo X11)
- **Limitaciones**: Documentar qué features no funcionan en Wayland (si las hay)
- **Optimización**: Usar protocolos específicos de Wayland cuando estén disponibles

### 8.4 Sistema de Macros
- **Grabación**: Grabar secuencias de comandos de usuario
- **Edición**: Modificar macros grabadas (quitar pasos, añadir delays)
- **Ejecución**: Reproducir macros con velocidad ajustable

### 8.5 Analytics y Mejora Continua
- **Telemetría opcional**: Estadísticas de uso (comandos más usados, errores comunes)
- **Mejora de prompts**: Ajustar prompts de IA basado en tasa de éxito de comandos
- **A/B testing**: Probar diferentes estrategias de generación de comandos

### 8.6 Comunidad y Ecosistema
- **Repositorio de "recetas"**: Comandos predefinidos para tareas comunes
- **Sharing**: Exportar/importar configuraciones y sesiones
- **Plugins de comunidad**: Sistema para compartir plugins de terceros

### 8.7 Seguridad Avanzada
- **Sandboxing**: Opción para ejecutar comandos generados en contenedores (Docker, bubblewrap)
- **Auditoría**: Log completo de todos los comandos ejecutados con contexto
- **Rollback**: Sistema para deshacer cambios de sistema (usando snapshots o backups)

### 8.8 Accesibilidad
- **Screen readers**: Compatibilidad con lectores de pantalla
- **Alto contraste**: Temas accesibles para usuarios con baja visión
- **Atajos de teclado**: Navegación completa sin mouse

### 8.9 Internacionalización
- **i18n**: Soporte para español (principal) e inglés
- **Localización**: Formatos de fecha, número, y colores culturales
- **RTL**: Soporte básico para idiomas de derecha a izquierda si es viable

### 8.10 Documentación de Arquitectura
- **Diagramas**: Arquitectura de componentes, flujo de datos, diagramas de secuencia
- **Decisiones**: Documento ADR (Architecture Decision Records) para decisiones clave
- **Roadmap**: Plan de desarrollo a 6 meses con milestones claros

---

## Resumen Ejecutivo

Este sistema TRON representa una **arquitectura de orquestación terminal de alta densidad**, diseñada para maximizar el impacto visual y funcional en demostraciones técnicas profesionales. La clave está en la **integración sin fisuras** entre:

1. **Kitty** como canvas gráfico (vía Remote Control Protocol)
2. **IA Local** (Ollama/DeepSeek) como cerebro interpretativo
3. **Python** como orquestador de ventanas y lógica de negocio
4. **Openbox** como gestor de ventanas ligero y controlable
5. **Gum/FZF** como capa de interfaz usuario elegante

La densidad de funcionalidad debe ser comparable a un "buquetanque de petróleo" - máxima capacidad en mínimo espacio, sin sacrificar la eficiencia en la máquina objetivo (8GB RAM, entorno gráfico ligero).

configuracion de openbox en ~/.config/openbox/lxubuntu-rc.xml



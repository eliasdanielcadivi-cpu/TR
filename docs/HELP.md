# 🛰 ARES - Ayuda Inteligente y Documentación

> Navega esta documentación con `broot` o léela directamente.

## 📚 Índice de Documentación

### Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `ares` | Sin argumentos: abre ARES Hub |
| `ares -h` | Muestra esta ayuda |
| `ares p "pregunta"` | Consulta IA rápida |
| `ares p "pregunta" --model gemma` | Usar modelo específico |
| `ares p "pregunta" --template code` | Usar plantilla YAML |
| `ares p "pregunta" --rag docs` | Consulta con contexto RAG |
| `ares p "razona" --think` | Usa modelo pensante (ares-think) |
| `ares i` | Modo interactivo REPL |
| `ares status` | Diagnóstico del sistema |
| `ares config` | Ver configuración global |
| `ares models` | Listar modelos disponibles |
| `ares templates` | Listar plantillas YAML |
| `ares tools` | Listar herramientas (function calling) |
| `ares apollo ingest archivo.pdf` | Ingerir documento a RAG |
| `ares model-creator list` | Gestionar modelos Ollama |
| `ares modelfile-creator list` | Gestionar Modelfiles YAML |
| `ares video <archivo>` | Reproduce video en kitty |
| `ares image <archivo>` | Muestra imagen en kitty |
| `ares plan` | Despliegue táctico (4 pestañas) |
| `ares zshplan` | Hacker AI Session (ZSH) |
| `ares mcat-demo` | Demo exhaustiva Mcat |
| `ares help` | Navegar docs/ con Broot |

### Gestión de Sesiones (gs)

| Comando | Descripción |
|---------|-------------|
| `ares gs save [nombre]` | Guarda sesión actual |
| `ares gs list` | Lista sesiones en db/ |
| `ares gs restore [nombre]` | Restaura en ventana actual |
| `ares gs deploy [nombre]` | Despliega en ventana NUEVA |
| `ares gs com "TITLE" "cmd"` | Envía comando a pestaña |
| `ares gs edit [nombre]` | Edita sesión JSON en micro |
| `ares diario` | Alias: deploy diaria |
| `ares diario-edit` | Alias: edit diaria |

### Inicialización (init)

| Opción | Descripción |
|--------|-------------|
| `ares init -l` | Enlaza config Kitty con ARES |
| `ares init -s` | Verifica estado (enlaces, dirs) |
| `ares init -r` | Recarga config en caliente |

### Socket y Ventanas

| Comando | Descripción |
|---------|-------------|
| `ares socket-check` | Verifica socket por defecto |
| `ares socket-check unix:/tmp/x` | Verifica socket específico |
| `ares socket-check --json` | Salida JSON para scripting |
| `ares windows` | Ver ventanas registradas |

### Aliases de Modelos

| Alias | Provider | Modelo |
|-------|----------|--------|
| `gemma` | Ollama | gemma3:4b |
| `gemma12b` | Ollama | gemma3:12b |
| `deepseek` | DeepSeek API | deepseek-chat |
| `openrouter` | OpenRouter | google/gemma-3-4b-it |

### Plantillas YAML

| Plantilla | Provider | Uso |
|-----------|----------|-----|
| `default` | gemma | Consultas generales |
| `chat` | gemma | Conversaciones multi-turno |
| `code` | gemma | Programación y código |
| `tools` | gemma | Function calling |
| `default` | deepseek | Consultas generales |

---

## 🎨 Módulo de Color (`ares color`)

### Uso Básico

```bash
# Aplicar color según archivo
ares color /home/daniel/Escritorio/QT5/elAsunto.md

# Listar reglas
ares color --list

# Auto-detectar
ares color --auto
```

### Estructura de Colores Hacker Neon

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `active_fg` | Texto cuando activa | `#FF00FF` |
| `inactive_fg` | Texto cuando inactiva | `#FF0080` |
| `active_bg` | Fondo cuando activa | `#1A001A` |
| `inactive_bg` | Fondo cuando inactiva | `#0D000D` |

### Paletas Disponibles

- **fuchsia**: `#FF00FF` (texto), `#1A001A` (fondo)
- **cyan**: `#00FFFF` (texto), `#001A1A` (fondo)
- **red**: `#FF0000` (texto), `#1A0000` (fondo)
- **green**: `#39FF14` (texto), `#0A1A0A` (fondo)
- **yellow**: `#FFFF00` (texto), `#1A1A00` (fondo)
- **orange**: `#FF6600` (texto), `#1A0D00` (fondo)

---

## 🎬 Módulo de Video (`ares video`)

### Uso Básico

```bash
# Reproducir video
ares video /ruta/al/video.mp4

# Con subtítulos
ares video --sub /ruta/al/sub.srt video.mp4

# Iniciar en timestamp
ares video --start 00:01:30 video.mp4

# Bucle infinito
ares video --loop video.mp4

# Velocidad ajustada
ares video --speed 1.5 video.mp4
```

### Opciones

| Opción | Descripción |
|--------|-------------|
| `--sub <archivo>` | Cargar subtítulos (.srt, .ass) |
| `--start <tiempo>` | Iniciar en timestamp (ej: `00:01:30`) |
| `--loop` | Bucle infinito |
| `--speed <valor>` | Velocidad (0.5-2.0) |
| `--volume <valor>` | Volumen (0-100) |
| `--audio-only` | Solo audio |
| `--screenshot` | Captura al finalizar |

### Atajos Durante Reproducción

| Tecla | Acción |
|-------|--------|
| `ESPACIO` | Pausar/Reproducir |
| `q` | Salir |
| `f` | Pantalla completa |
| `←/→` | Adelante/Atrás 5s |
| `↑/↓` | Adelante/Atrás 1min |
| `9/0` | Bajar/Subir volumen |
| `j` | Cambiar subtítulo |
| `v` | Cambiar pista de video |

### Configuración MPV

Editar: `/home/daniel/tron/programas/TR/config/mpv/mpv.conf`

---

## 🖼️ Módulo de Imagen (`ares image`)

### Uso Básico

```bash
# Mostrar imagen
ares image /ruta/a/imagen.jpg

# Cuadrícula de imágenes
ares image --grid img1.jpg img2.jpg img3.jpg

# Con ancho específico
ares image --width 80 imagen.png

# Limpiar imágenes
ares image --clear
```

### Opciones

| Opción | Descripción |
|--------|-------------|
| `--grid, -g` | Mostrar en cuadrícula |
| `--width, -w` | Ancho en columnas |
| `--height` | Alto en filas |
| `--align` | Alineación (left/center/right) |
| `--scale-up` | Escalar imágenes pequeñas |
| `--clear` | Limpiar imágenes mostradas |

### Formatos Soportados

- **Imágenes**: jpg, jpeg, png, gif, bmp, webp, tiff, ico, svg
- **Animados**: gif, apng, webp
- **Documentos**: pdf (primera página)

### Alternativas

```bash
# Usar icat directamente
kitten icat imagen.jpg

# Usar viu
viu imagen.jpg

# Usar term-image
term-image show imagen.jpg
```

---

## ⌨️ Atajos de Teclado en Kitty

### Navegación de Pestañas

| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+T` | Nueva pestaña |
| `Ctrl+Shift+W` | Cerrar pestaña |
| `Ctrl+←/→` | Pestaña anterior/siguiente |
| `Ctrl+Shift+P` | Renombrar pestaña |

### Navegación de Scroll

| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+PageUp` | Subir 100 líneas |
| `Ctrl+Shift+PageDown` | Bajar 100 líneas |

### Portapapeles

| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+C` | Copiar |
| `Ctrl+Shift+V` | Pegar |

### Ventanas/Paneles

| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+H/J/K/L` | Mover foco entre ventanas |
| `Ctrl+Alt+H/J/K/L` | Redimensionar ventanas |

---

## 📖 Referencias Externas

### Documentación Oficial de Kitty

- [Remote Control](https://sw.kovidgoyal.net/kitty/remote-control/)
- [Graphics Protocol](https://sw.kovidgoyal.net/kitty/graphics-protocol/)
- [Integrations](https://sw.kovidgoyal.net/kitty/integrations/)
- [Color Stack](https://sw.kovidgoyal.net/kitty/color-stack/)

### Herramientas Recomendadas

- **mpv**: Reproductor de video
- **kitten icat**: Visor de imágenes de kitty
- **viu**: Visor de imágenes alternativo
- **term-image**: Visor con más opciones

---

## 🔧 Configuración

### Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `TR/config/kitty.conf` | Configuración de kitty |
| `TR/config/mpv/mpv.conf` | Configuración de mpv |
| `TR/modules/color/config.yaml` | Reglas de coloreado |
| `TR/config/config.yaml` | Configuración general de TR |

### Recargar Configuración

```bash
# Recargar kitty.conf
Ctrl+Alt+R (desde kitty)

# O manualmente
kitten @ load-config
```

---

## 🤖 Uso de IA con ARES

### Ejemplos de Consultas

```bash
# Consulta simple (usa gemma3:4b por defecto)
ares p "¿Qué es Python?"

# Usar modelo específico
ares p "Explica la teoría de relatividad" --model gemma12b

# Usar plantilla de código
ares p "Escribe un hello world en Python" --template code

# Usar plantilla de chat
ares p "Tengo una duda sobre programación" --template chat

# Combinar modelo y plantilla
ares p "Optimiza esta función" --model gemma12b --template code

# Usar DeepSeek API (requiere DEEPSEEK_API_KEY)
ares p "Analiza este algoritmo" --model deepseek
```

### Herramientas Disponibles (Function Calling)

ARES soporta function calling con las siguientes herramientas:

| Herramienta | Descripción | Ejemplo de uso |
|-------------|-------------|----------------|
| `google_search` | Búsqueda en tiempo real | "¿Quién ganó el Mundial 2022?" |
| `translate_text` | Traducción de texto | "Traduce 'Hello' al español" |
| `get_weather` | Clima actual | "¿Qué temperatura hay en Madrid?" |
| `execute_shell` | Ejecutar comando | "Lista los archivos del directorio" |
| `read_file` | Leer archivo | "Lee el archivo config.yaml" |
| `write_file` | Escribir archivo | "Crea un archivo con este contenido" |

### Ver Recursos Disponibles

```bash
# Ver modelos disponibles
ares models

# Ver plantillas YAML
ares templates

# Ver herramientas
ares tools

# Ver configuración actual
ares config
```

---

## 🔧 Comandos Detallados (Menos Intuitivos)

### `ares init` - Gestión de Infraestructura

**¿Qué inicializa?** La infraestructura de Kitty y ARES: enlaces simbólicos, directorios, permisos.

```bash
# Enlazar configuración de Kitty con ARES (crea symlink kitty.conf)
ares init -l

# Verificar estado: enlaces, directorios, permisos
ares init -s

# Recargar configuración en Kitty caliente (sin reiniciar terminal)
ares init -r
```

**Cuándo usar:**
- `-l`: Primera instalación o cuando cambias kitty.conf
- `-s`: Diagnóstico, algo no funciona
- `-r`: Modificaste config y quieres aplicar sin cerrar Kitty

---

### `ares gs` - Gestión de Sesiones (Completo)

**Sesiones:** Configuraciones JSON en `db/` que definen ventanas, pestañas, títulos y comandos.

```bash
# Guardar sesión actual (ventanas, pestañas, colores)
ares gs save mi-sesion

# Listar sesiones guardadas
ares gs list

# Restaurar en ventana actual
ares gs restore mi-sesion

# Desplegar en ventana NUEVA (socket único automático)
ares gs deploy mi-sesion

# Enviar comando a pestaña específica por título
ares gs com "NOTAS" "micro /home/daniel/notas.md"

# Editar configuración JSON de sesión en editor micro
ares gs edit mi-sesion
```

**Estructura de sesión (`db/*.json`):**
```json
[
  {
    "is_focused": true,
    "tabs": [
      {"title": "GEMINI", "cmd": ""},
      {"title": "NOTAS", "cmd": "micro /path/to/notas.md"},
      {"title": "TERM", "cmd": "comando1;comando2;comando3"}
    ]
  }
]
```

**Comandos en pestañas:**
- Vacío `""`: Solo abre pestaña con título
- Simple `"micro archivo"`: Ejecuta comando
- Múltiple `"cmd1;cmd2;cmd3"`: Separa con `;`, la shell interpreta

---

### `ares diario` y `ares diario-edit` - Atajos Diarios

**`ares diario`**: Alias directo de `ares gs deploy diaria`. Lanza la sesión de trabajo diario.

**`ares diario-edit`**: Alias de `ares gs edit diaria`. Edita `db/diaria.json` en micro.

```bash
# Lanzar sesión diaria
ares diario

# Editar sesión diaria
ares diario-edit
```

**Backup automático:** Antes de editar, crea `diaria.json.bak`. Si hay error JSON, restaura automáticamente.

---

### `ares socket-check` - Diagnóstico de Sockets

**Socket Kitty:** Punto de comunicación UNIX para control remoto de ventanas/pestañas.

```bash
# Verificar socket por defecto (desde config.yaml)
ares socket-check

# Verificar socket específico
ares socket-check unix:/tmp/custom_socket

# Salida JSON (para scripting)
ares socket-check --json
```

**Qué verifica:**
- Existencia del archivo socket
- Permisos de lectura/escritura
- Proceso propietario
- Estado (activo/huérfano)

**Cuándo usar:**
- `ares gs deploy` falla con "socket ya existe"
- Kitty no responde a comandos remotos
- Debug de problemas de conexión

---

### `ares apollo ingest` - Sistema RAG

**RAG:** Retrieval-Augmented Generation. Ingiere documentos para búsqueda semántica con IA.

```bash
# Ingerir documento (PDF, MD, TXT, etc.)
ares apollo ingest documento.pdf

# Ingerir directorio completo
ares apollo ingest /path/to/docs/
```

**Qué hace:**
1. Extrae texto del documento
2. Divide en chunks semánticos
3. Genera embeddings (Ollama: mxbai-embed-large)
4. Guarda en SQLite + sqlite-vec
5. Indexa para búsqueda vectorial

**Luego usa:**
```bash
ares p "¿Qué dice el documento sobre X?" --rag docs
```

---

### `ares model-creator` y `modelfile-creator`

**model-creator:** Gestiona modelos Ollama (crear, actualizar, eliminar).

```bash
# Listar modelos Ollama disponibles
ares model-creator list

# Crear modelo desde padre
ares model-creator create mi-gemma --parent gemma:7b

# Actualizar parámetros (temp, top_p, etc.)
ares model-creator update mi-gemma --temperature 0.8

# Eliminar modelo
ares model-creator delete mi-gemma

# Mostrar Modelfile asociado
ares model-creator show mi-gemma
```

**modelfile-creator:** Gestiona plantillas YAML de comportamiento IA.

```bash
# Listar Modelfiles YAML
ares modelfile-creator list

# Crear nueva plantilla
ares modelfile-creator create code-reviewer --template code

# Actualizar plantilla existente
ares modelfile-creator update code-reviewer

# Eliminar plantilla
ares modelfile-creator delete code-reviewer

# Mostrar contenido
ares modelfile-creator show code-reviewer
```

**Diferencia:**
- `model-creator`: Modelos Ollama (binarios, pesos)
- `modelfile-creator`: Plantillas YAML (prompts, comportamiento)

---

### `ares help` vs `ares -h`

**`ares -h`:** Muestra ayuda rápida en terminal (este documento).

**`ares help`:** Abre navegador Broot en `docs/` para exploración jerárquica.

```bash
# Ayuda rápida (lo que estás leyendo)
ares -h

# Navegador documental completo
ares help
```

**Cuándo usar cada uno:**
- `-h`: Consulta rápida, no sabes el comando
- `help`: Exploración profunda, buscas documentación específica

---

*ARES: El orquestador definitivo por Daniel Hung.*

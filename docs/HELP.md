# 🛰 ARES - Ayuda Inteligente y Documentación

> Navega esta documentación con `broot` o léela directamente.

## 📚 Índice de Documentación

### Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `ares` | Sin argumentos: abre ARES Hub |
| `ares p "pregunta"` | Consulta a la IA ARES (Gemma/DeepSeek) |
| `ares p "pregunta" --model gemma` | Usar modelo específico |
| `ares p "pregunta" --template code` | Usar plantilla YAML |
| `ares status` | Diagnóstico del sistema |
| `ares config` | Ver configuración de IA |
| `ares models` | Listar modelos disponibles |
| `ares templates` | Listar plantillas YAML |
| `ares tools` | Listar herramientas (function calling) |
| `ares color <ruta>` | Aplica color Hacker Neon a pestaña |
| `ares video <archivo>` | Reproduce video en kitty |
| `ares image <archivo>` | Muestra imagen en kitty |
| `ares plan` | Despliegue táctico (4 pestañas) |
| `ares zshPlan` | Hacker AI Session (ZSH) |
| `ayuda zsh` | Ver hoja de trucos WOW y productividad Zsh |
| `sherlok --help` | Ojo Forense: Escanea e indexa tus programas propios |

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

### Documentación Adicional

- `docs/GEMMA_OLLAMA_GUIDE.md`: Guía completa de Gemma + Ollama
- `docs/DEEPSEEK_GUIDE.md`: Guía de DeepSeek API

---

*ARES: El orquestador definitivo por Daniel Hung.*

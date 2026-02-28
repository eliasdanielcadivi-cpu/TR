# 🛰 TR - Ayuda Inteligente y Documentación

> Navega esta documentación con `broot` o léela directamente.

## 📚 Índice de Documentación

### Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `tr` | Sin argumentos: abre esta ayuda |
| `tr p "pregunta"` | Consulta a la IA Tron |
| `tr status` | Diagnóstico del sistema |
| `tr color <ruta>` | Aplica color Hacker Neon a pestaña |
| `tr video <archivo>` | Reproduce video en kitty |
| `tr image <archivo>` | Muestra imagen en kitty |
| `tr plan` | Orquestación táctica |
| `tr model <alias>` | Cambia modelo de IA |

---

## 🎨 Módulo de Color (`tr color`)

### Uso Básico

```bash
# Aplicar color según archivo
tr color /home/daniel/Escritorio/QT5/elAsunto.md

# Listar reglas
tr color --list

# Auto-detectar
tr color --auto
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

## 🎬 Módulo de Video (`tr video`)

### Uso Básico

```bash
# Reproducir video
tr video /ruta/al/video.mp4

# Con subtítulos
tr video --sub /ruta/al/sub.srt video.mp4

# Iniciar en timestamp
tr video --start 00:01:30 video.mp4

# Bucle infinito
tr video --loop video.mp4

# Velocidad ajustada
tr video --speed 1.5 video.mp4
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

## 🖼️ Módulo de Imagen (`tr image`)

### Uso Básico

```bash
# Mostrar imagen
tr image /ruta/a/imagen.jpg

# Cuadrícula de imágenes
tr image --grid img1.jpg img2.jpg img3.jpg

# Con ancho específico
tr image --width 80 imagen.png

# Limpiar imágenes
tr image --clear
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

*Tron: YO Defiendo al Usuario.

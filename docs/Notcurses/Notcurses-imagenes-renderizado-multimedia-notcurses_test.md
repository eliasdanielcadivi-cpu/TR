# Notcurses - Guía de Imágenes y Renderizado Visual
## Módulo: `multimedia/notcurses_test.py`, `multimedia/notcurses_test_basico.py`

> **Estado:** Investigación completada - Wrapper básico identificado - Extensión creada  
> **Versión notcurses:** 3.0.7 (APT)  
> **Wrapper Python:** Compilado desde fuente (`/home/daniel/borrar/notcurses/cffi/`)  
> **Fecha:** 15-03-2026

---

## 📋 ÍNDICE

1. [Problema Detectado](#problema-detectado)
2. [Causa Raíz](#causa-raíz)
3. [API C Disponible (no expuesta en Python)](#api-c-disponible)
4. [Solución Implementada](#solución-implementada)
5. [Flujo de Trabajo con Imágenes](#flujo-de-trabajo-con-imágenes)
6. [Qué Deberías Ver en las Pruebas](#qué-deberías-ver-en-las-pruebas)
7. [Patrones Extraídos de Tutoriales](#patrones-extraídos)
8. [Widgets Modulares C → JSON](#widgets-modulares-c--json)

---

## 🔴 PROBLEMA DETECTADO

### Síntomas Observados

```
❌ "Veo elementos sí pero entremezclados con texto y desordenados"
❌ "No veo una pantalla" (layout estructurado)
❌ Imágenes no se renderizan
❌ Solo texto y colores básicos funcionan
```

### Diagnóstico Inicial

El wrapper Python básico (`notcurses.py`) **SOLO** expone:
- `Notcurses` - Inicialización
- `Ncplane` - Planos básicos (putEGCYX, getDimensions, setFgRGB, setBgRGB)
- `Cell` - Celdas individuales
- `Ncdirect` - Modo directo (sin planos)

**NO expone:**
- `ncvisual_*` - Carga y renderizado de imágenes
- `NCBLIT_*` - Constantes de blitter (tipos de renderizado)
- `NCSCALE_*` - Constantes de escalado
- `ncplane_create` - Creación de planos hijos
- Widgets (plots, menus, tables, etc.)

---

## 🎯 CAUSA RAÍZ

### Wrapper Python Incompleto

El archivo `/home/daniel/tron/programas/TR/.venv/lib/python3.13/site-packages/notcurses/notcurses.py` es **mínimo**:

```python
# Solo 150 líneas - Funciones básicas
class Notcurses:
    def __init__(self): ...
    def render(self): ...
    def stdplane(self): ...

class Ncplane:
    def putEGCYX(self, y, x, egc): ...
    def getDimensions(self): ...
    def setFgRGB(self, r, g, b): ...
    # NO HAY: create(), blit(), box(), gradient(), etc.
```

### Biblioteca C Subyacente SÍ Tiene Todo

El wrapper CFFI compilado (`_notcurses.cpython-*.so`) **SÍ tiene** las funciones:

```bash
$ python3 -c "from notcurses import _notcurses; print([x for x in dir(_notcurses.lib) if 'visual' in x.lower()][:30])"

['NCVISUAL_OPTION_ADDALPHA', 'NCVISUAL_OPTION_BLEND', 
 'ncvisual_at_yx', 'ncvisual_blit', 'ncvisual_decode',
 'ncvisual_destroy', 'ncvisual_from_file', 'ncvisual_from_rgba',
 'ncvisual_geom', 'ncvisual_resize', 'ncvisual_rotate',
 'ncvisual_stream', ...]
```

**Conclusión:** Las funciones están compiladas, pero el módulo Python no las expone.

---

## 📚 API C DISPONIBLE (No Expuesta en Python)

### Constantes de Blitter (Cómo Renderizar)

| Constante | Valor | Descripción | Uso |
|-----------|-------|-------------|-----|
| `NCBLIT_DEFAULT` | 0 | notcurses elige automáticamente | Recomendado |
| `NCBLIT_1x1` | 1 | Bloque ASCII completo (█) | Texto/arte ASCII |
| `NCBLIT_2x1` | 2 | Medios bloques (▄▀) | Imágenes 2:1 |
| `NCBLIT_2x2` | 3 | Quadrantes | Imágenes 4:1 |
| `NCBLIT_3x2` | 4 | Sextantes (Unicode 13) | Terminal moderno |
| `NCBLIT_4x2` | 5 | Octantes (Unicode 16) | Máxima resolución |
| `NCBLIT_BRAILLE` | 6 | Braille (2x4 puntos) | Arte Braille |
| `NCBLIT_PIXEL` | 7 | Píxeles nativos | Kitty, iTerm2, WezTerm |

### Constantes de Scaling (Cómo Escalar)

| Constante | Valor | Descripción |
|-----------|-------|-------------|
| `NCSCALE_NONE` | 0 | Sin escalado, tamaño original |
| `NCSCALE_SCALE` | 1 | Mantener aspect ratio |
| `NCSCALE_STRETCH` | 2 | Estirar para llenar |
| `NCSCALE_NONE_HIRES` | 3 | Sin escalado, alta resolución |
| `NCSCALE_SCALE_HIRES` | 4 | Escalado, alta resolución |

### Funciones ncvisual (Imágenes)

```c
// Cargar imagen desde archivo
struct ncvisual* ncvisual_from_file(const char* file);

// Cargar desde RGBA en memoria
struct ncvisual* ncvisual_from_rgba(const void* rgba, int rows, int stride, int cols);

// Renderizar imagen en plano
struct ncplane* ncvisual_blit(struct notcurses* nc, 
                               struct ncvisual* ncv,
                               struct ncvisual_options* vopts);

// Redimensionar imagen
int ncvisual_resize(struct ncvisual* ncv, int rows, int cols);

// Rotar imagen
int ncvisual_rotate(struct ncvisual* ncv, float radians);

// Obtener geometría
int ncvisual_geom(const struct notcurses* nc,
                  const struct ncvisual* ncv,
                  const struct ncplane* n,
                  struct ncvisual_geom* geom);

// Liberar recursos
void ncvisual_destroy(struct ncvisual* ncv);
```

### Estructura ncvisual_options

```c
struct ncvisual_options {
    struct ncplane* n;        // Plano destino
    int y, x;                 // Posición
    unsigned scaling;         // NCSCALE_*
    unsigned blitter;         // NCBLIT_*
    uint64_t flags;           // NCVISUAL_OPTION_*
    // ... más campos avanzados
};
```

### Funciones de Planos (Faltantes en Python)

```c
// Crear plano hijo
struct ncplane* ncplane_create(struct ncplane* parent,
                                const ncplane_options* opts);

// Mover plano
int ncplane_move_yx(struct ncplane* n, int y, int x);

// Box/Border
int ncplane_box_sized(struct ncplane* n,
                      const nccell* ul, const nccell* ur,
                      const nccell* ll, const nccell* lr,
                      const nccell* hl, const nccell* vl,
                      int yoff, int xoff, int leny, int lenx,
                      unsigned ctrl);

// Gradientes
int ncplane_gradient(struct ncplane* n,
                     const char* egc, unsigned stylebits,
                     uint64_t ul, uint64_t ur, uint64_t ll, uint64_t lr,
                     int yoff, int xoff, int leny, int lenx);
```

---

## ✅ SOLUCIÓN IMPLEMENTADA

### Archivo Creado: `visual.py`

Ubicación: `TR/.venv/lib/python3.13/site-packages/notcurses/visual.py`

```python
from . import _notcurses
lib = _notcurses.lib
ffi = _notcurses.ffi

# Constantes expuestas
NCBLIT_DEFAULT = lib.NCBLIT_DEFAULT
NCBLIT_PIXEL = lib.NCBLIT_PIXEL
NCSCALE_SCALE = lib.NCSCALE_SCALE
NCSCALE_STRETCH = lib.NCSCALE_STRETCH

class Visual:
    """Wrapper para ncvisual"""
    
    def __init__(self, path_or_rgba=None, ...):
        # Cargar desde archivo o RGBA
        self.ncv = lib.ncvisual_from_file(path.encode('utf-8'))
    
    def blit(self, plane, y=0, x=0, scaling=NCSCALE_SCALE, ...):
        # Renderizar imagen en plano
        vopts = ffi.new("struct ncvisual_options *")
        vopts.n = plane.getNcplane()
        vopts.y = y
        vopts.x = x
        vopts.scaling = scaling
        vopts.blitter = blitter
        return lib.ncvisual_blit(ffi.NULL, self.ncv, vopts)
    
    def resize(self, rows, cols, interpolative=True):
        lib.ncvisual_resize(self.ncv, rows, cols)
    
    def get_geometry(self, nc=None, plane=None):
        # Obtener dimensiones en píxeles y celdas
        geom = ffi.new("struct ncvisual_geom *")
        lib.ncvisual_geom(nc_ptr, self.ncv, plane_ptr, geom)
        return {'pixy': geom.pixy, 'pixx': geom.pixx, ...}
```

### Uso Básico

```python
from notcurses import Notcurses
from notcurses.visual import Visual, NCBLIT_PIXEL, NCSCALE_STRETCH

nc = Notcurses()
stdplane = nc.stdplane()

# Cargar imagen
v = Visual("/ruta/a/imagen.png")

# Renderizar en plano estándar
v.blit(stdplane, y=0, x=0, scaling=NCSCALE_STRETCH, blitter=NCBLIT_PIXEL)

nc.render()
```

---

## 🔄 FLUJO DE TRABAJO CON IMÁGENES

### 1. Verificar Soporte del Terminal

```python
from notcurses import Notcurses
from notcurses.visual import can_pixel, can_truecolor, can_utf8

nc = Notcurses()

print(f"✅ Pixel graphics: {can_pixel(nc)}")      # Kitty, iTerm2, WezTerm
print(f"✅ Truecolor: {can_truecolor(nc)}")       # 24-bit RGB
print(f"✅ UTF-8: {can_utf8(nc)}")                # Unicode
```

### 2. Cargar y Renderizar Imagen

```python
from notcurses import Notcurses
from notcurses.visual import Visual, NCBLIT_PIXEL, NCSCALE_STRETCH

nc = Notcurses()
stdplane = nc.stdplane()

# Obtener dimensiones del terminal
rows, cols = stdplane.getDimensions()

# Cargar imagen
v = Visual("/home/daniel/tron/programas/TR/assets/ares/term-image.png")

# Opción A: Renderizar directo en stdplane
v.blit(stdplane, y=0, x=0, scaling=NCSCALE_STRETCH, blitter=NCBLIT_PIXEL)

# Opción B: Crear plano hijo para la imagen
from notcurses.visual import plane_create
img_plane = plane_create(stdplane, {'rows': rows//2, 'cols': cols//2, 'yoff': 0, 'xoff': 0})
v.blit(img_plane, scaling=NCSCALE_SCALE, blitter=NCBLIT_PIXEL)

nc.render()
input("Presiona Enter...")
```

### 3. Layout Estructurado (Evitar "Desorden")

```python
from notcurses import Notcurses
from notcurses.visual import Visual, plane_create, NCBLIT_PIXEL, NCSCALE_STRETCH

nc = Notcurses()
stdplane = nc.stdplane()
rows, cols = stdplane.getDimensions()

# === LAYOUT TIPO DASHBOARD ===
# Header (fila 0-2)
header = plane_create(stdplane, {'rows': 3, 'cols': cols, 'yoff': 0, 'xoff': 0})
header.setFgRGB(255, 255, 255)
header.setBgRGB(0, 100, 200)
for i in range(3):
    header.putEGCYX(i, 0, " " * cols)  # Fondo de color
header.putEGCYX(1, cols//2 - 10, "🤖 ARES-TRON")

# Imagen principal (filas 3-15, izquierda)
img_height = rows // 2
img_width = cols // 2
img_plane = plane_create(stdplane, {
    'rows': img_height,
    'cols': img_width,
    'yoff': 3,
    'xoff': 0
})

v = Visual("/ruta/a/imagen.png")
v.blit(img_plane, scaling=NCSCALE_STRETCH, blitter=NCBLIT_PIXEL)

# Panel de texto (filas 3-15, derecha)
text_plane = plane_create(stdplane, {
    'rows': img_height,
    'cols': cols - img_width,
    'yoff': 3,
    'xoff': img_width
})
text_plane.setFgRGB(0, 255, 0)
text_plane.putEGCYX(0, 0, "Estado del Sistema:")
text_plane.putEGCYX(2, 0, "CPU: 45%")
text_plane.putEGCYX(3, 0, "RAM: 2.1GB / 8GB")

# Footer (últimas 2 filas)
footer = plane_create(stdplane, {
    'rows': 2,
    'cols': cols,
    'yoff': rows - 2,
    'xoff': 0
})
footer.setFgRGB(200, 200, 200)
footer.putEGCYX(0, 0, "═" * cols)
footer.putEGCYX(1, 0, "Presiona Q para salir")

nc.render()
```

### 4. Múltiples Imágenes con Planos

```python
# Grid de imágenes
imagenes = [
    "/ruta/img1.png",
    "/ruta/img2.png",
    "/ruta/img3.png",
    "/ruta/img4.png",
]

rows, cols = stdplane.getDimensions()
tile_rows = rows // 2
tile_cols = cols // 2

for i, path in enumerate(imagenes):
    y = (i // 2) * tile_rows
    x = (i % 2) * tile_cols
    
    plano = plane_create(stdplane, {
        'rows': tile_rows - 1,  # -1 para espaciado
        'cols': tile_cols - 1,
        'yoff': y,
        'xoff': x
    })
    
    v = Visual(path)
    v.blit(plano, scaling=NCSCALE_STRETCH, blitter=NCBLIT_PIXEL)

nc.render()
```

---

## 👁️ QUÉ DEBERÍAS VER EN LAS PRUEBAS

### Test 1: Colores RGB Básicos

**Archivo:** `modules/multimedia/notcurses_test_basico.py`

```python
# Código actual (solo texto con colores)
stdplane.setFgRGB(255, 0, 0)
stdplane.putEGCYX(1, 1, "ROJO")
```

**Deberías ver:**
```
┌────────────────────────────────────┐
│                                    │
│  ROJO    (texto en rojo puro)      │
│  VERDE   (texto en verde puro)     │
│  AZUL    (texto en azul puro)      │
│                                    │
└────────────────────────────────────┘
```

**Problema actual:** El texto aparece pero sin posición clara, todo mezclado.

**Causa:** No se está limpiando el plano antes de escribir, o no hay renderizado explícito.

---

### Test 2: Unicode y Caracteres Gráficos

```python
# Cajas y bordes Unicode
stdplane.putEGCYX(0, 0, "┌" + "─" * 38 + "┐")
stdplane.putEGCYX(1, 0, "│ Contenido       │")
stdplane.putEGCYX(2, 0, "└" + "─" * 38 + "┘")
```

**Deberías ver:**
```
┌──────────────────────────────────────┐
│ Contenido                            │
└──────────────────────────────────────┘
```

**Problema actual:** Caracteres Unicode se ven pero desalineados.

**Causa:** 
1. Terminal no está en modo UTF-8 correcto
2. Ancho de caracteres Unicode no calculado correctamente
3. Falta `nc.render()` después de dibujar

---

### Test 3: Gradientes

```python
# Gradiente manual (celda por celda)
for x in range(20):
    r = int(255 * x / 20)
    b = 255 - r
    cell = Cell(stdplane, "█")
    cell.setFgRGB(r, 0, b)
    stdplane.setBaseCell(cell)
    stdplane.putEGCYX(5, x, "█")
```

**Deberías ver:**
```
████████████████████
(Rojo → Púrpura → Azul, suave transición)
```

**Problema actual:** Gradiente se ve pero "a saltos" o mezclado.

**Causa:** 
1. Terminal no soporta truecolor (solo 256 colores)
2. No se usa `nc.render()` para actualizar
3. Celdas no se liberan correctamente (memory leak visual)

---

### Test 4: Imágenes (NUEVO - Con visual.py)

```python
from notcurses.visual import Visual, NCBLIT_PIXEL

v = Visual("/ruta/imagen.png")
v.blit(stdplane, y=0, x=0, scaling=NCSCALE_STRETCH, blitter=NCBLIT_PIXEL)
nc.render()
```

**Deberías ver:**
```
┌──────────────────────────────────────┐
│                                      │
│   [IMAGEN RENDERIZADA AQUÍ]          │
│   (ocupa toda la pantalla)           │
│                                      │
└──────────────────────────────────────┘
```

**Si usas layout estructurado:**
```
┌──────────────────────────────────────┐
│ 🤖 ARES-TRON          [Estado: OK]   │  ← Header
├──────────────────┬───────────────────┤
│                  │                   │
│   [IMAGEN]       │  CPU: 45%         │  ← Body
│                  │  RAM: 2.1GB       │
│                  │                   │
├──────────────────┴───────────────────┤
│ ═══════════════════════════════════  │  ← Footer
│ Presiona Q para salir                │
└──────────────────────────────────────┘
```

---

## 📖 PATRONES EXTRAÍDOS DE TUTORIALES

### Patrón 1: Render Loop con Input (de `intro.c`)

```c
// C original
while(!done){
    ncplane_erase(n);
    animate_frame(n, frame);
    notcurses_render(nc);
    ncinput in;
    notcurses_get_blocking(nc, &in);
    if(in.id == 'q') done = true;
}
```

**Python equivalente:**
```python
import sys

frame = 0
while True:
    stdplane.erase()  # Limpiar pantalla
    
    # Dibujar frame actual
    stdplane.putEGCYX(0, 0, f"Frame: {frame}")
    
    nc.render()
    
    # Input no bloqueante
    ch = sys.stdin.read(1)
    if ch == 'q':
        break
    
    frame += 1
```

---

### Patrón 2: Planos Hijos para Layout (de `view.c`)

```c
// C original - Crear plano para imagen
struct ncplane_options nopts = {
    .y = 1,
    .x = NCALIGN_RIGHT,
    .rows = 12,
    .cols = PIPCOLUMNS,
    .flags = NCPLANE_OPTION_HORALIGNED,
};
struct ncplane* pip = ncplane_create(stdplane, &nopts);

// Blit imagen en plano
struct ncvisual_options vopts = {.n = pip, .blitter = NCBLIT_PIXEL};
ncvisual_blit(nc, ncv, &vopts);
```

**Python equivalente:**
```python
from notcurses.visual import plane_create, NCALIGN_RIGHT

img_plane = plane_create(stdplane, {
    'yoff': 1,
    'xoff': 0,  # NCALIGN_RIGHT se maneja diferente
    'rows': 12,
    'cols': 40,
    'flags': 0  # NCPLANE_OPTION_HORALIGNED
})

v.blit(img_plane, scaling=NCSCALE_STRETCH, blitter=NCBLIT_PIXEL)
```

---

### Patrón 3: Transparencia y Canales (de `trans.c`)

```c
// C original - Fondo transparente
nccell c = NCCELL_TRIVIAL_INITIALIZER;
nccell_set_fg_alpha(&c, NCALPHA_BLEND);  // Mezclar con fondo
nccell_set_bg_alpha(&c, NCALPHA_TRANSPARENT);  // No tocar fondo
ncplane_set_base_cell(n, &c);
```

**Python equivalente:**
```python
# Requiere extender Cell con alpha
cell = Cell(stdplane, " ")
# cell.setFgAlpha(NCALPHA_BLEND)  # No disponible aún
# cell.setBgAlpha(NCALPHA_TRANSPARENT)
stdplane.setBaseCell(cell)
```

---

### Patrón 4: Animación con Timing (de `sliders.c`)

```c
// C original - Animación con delay
uint64_t startns = clock_getns(CLOCK_MONOTONIC);
uint64_t deadline = startns + delaymultiplier * 5000000000ULL;

while(clock_getns(CLOCK_MONOTONIC) < deadline){
    ncplane_move_yx(chunk, y, x);
    notcurses_render(nc);
    nanosleep(&iterdelay, NULL);
}
```

**Python equivalente:**
```python
import time

start = time.monotonic()
duration = 5.0  # segundos

while time.monotonic() - start < duration:
    y = int(time.monotonic() * 10) % rows
    x = int(time.monotonic() * 15) % cols
    img_plane.move(y, x)  # Requiere método move()
    nc.render()
    time.sleep(1/60)  # 60 FPS
```

---

### Patrón 5: Boxes y Bordes (de `box.c`)

```c
// C original - Box con gradientes
nccell ul, ur, ll, lr, hl, vl;
nccells_rounded_box(n, 0, &ul, &ur, &ll, &lr, &hl, &vl);
nccell_set_fg_rgb(&ul, 0xff0000);
nccell_set_fg_rgb(&ur, 0x00ff00);
// ...
ncplane_box_sized(n, &ul, &ur, &ll, &lr, &hl, &vl, rows, cols, 0);
```

**Python equivalente:**
```python
# Requiere extender Ncplane con box methods
def draw_box(plane, y, x, h, w, fg_rgb):
    # Top
    for i in range(w):
        plane.putEGCYX(y, x + i, "─")
    # Bottom
    for i in range(w):
        plane.putEGCYX(y + h - 1, x + i, "─")
    # Left
    for i in range(h):
        plane.putEGCYX(y + i, x, "│")
    # Right
    for i in range(h):
        plane.putEGCYX(y + i, x + w - 1, "│")
    # Corners
    plane.putEGCYX(y, x, "┌")
    plane.putEGCYX(y, x + w - 1, "┐")
    plane.putEGCYX(y + h - 1, x, "└")
    plane.putEGCYX(y + h - 1, x + w - 1, "┘")
```

---

## 🧩 WIDGETS MODULARES C → JSON

### Idea: Widgets como Módulos C Independientes

En lugar de crear wrappers Python complejos, crear **módulos C** que:
1. Reciben configuración JSON
2. Renderizan en plano específico
3. Devuelven estado JSON

### Ejemplo: Widget de Barra de Progreso

```c
// widget_progress.c
#include <notcurses/notcurses.h>
#include <cjson/cjson.h>

typedef struct {
    struct ncplane* plane;
    int width;
    int height;
    float progress;  // 0.0 - 1.0
    char* label;
} progress_widget_t;

// Inicializar widget desde JSON
progress_widget_t* progress_init(const char* json_config) {
    cJSON* cfg = cJSON_Parse(json_config);
    
    progress_widget_t* w = malloc(sizeof(progress_widget_t));
    w->width = cJSON_GetObjectItem(cfg, "width")->valueint;
    w->height = cJSON_GetObjectItem(cfg, "height")->valueint;
    w->progress = cJSON_GetObjectItem(cfg, "progress")->valuedouble;
    w->label = strdup(cJSON_GetObjectItem(cfg, "label")->valuestring);
    
    // Crear plano
    ncplane_options opts = {
        .rows = w->height,
        .cols = w->width,
        .yoff = cJSON_GetObjectItem(cfg, "y")->valueint,
        .xoff = cJSON_GetObjectItem(cfg, "x")->valueint,
    };
    w->plane = ncplane_create(stdplane, &opts);
    
    cJSON_Delete(cfg);
    return w;
}

// Renderizar widget
void progress_render(progress_widget_t* w) {
    ncplane_erase(w->plane);
    
    // Dibujar barra
    int filled = w->width * w->progress;
    for (int i = 0; i < w->width; i++) {
        if (i < filled) {
            ncplane_set_fg_rgb8(w->plane, 0, 255, 0);
            ncplane_putchar(w->plane, '█');
        } else {
            ncplane_set_fg_rgb8(w->plane, 50, 50, 50);
            ncplane_putchar(w->plane, '░');
        }
    }
    
    // Label
    ncplane_set_fg_rgb8(w->plane, 255, 255, 255);
    ncplane_printf(w->plane, " %s: %.0f%%", w->label, w->progress * 100);
}

// Obtener estado como JSON
char* progress_get_state(progress_widget_t* w) {
    cJSON* state = cJSON_CreateObject();
    cJSON_AddNumberToObject(state, "progress", w->progress);
    cJSON_AddStringToObject(state, "label", w->label);
    char* json = cJSON_PrintUnformatted(state);
    cJSON_Delete(state);
    return json;
}

// Liberar widget
void progress_destroy(progress_widget_t* w) {
    ncplane_destroy(w->plane);
    free(w->label);
    free(w);
}
```

### Uso desde Python

```python
import ctypes
import json

# Cargar biblioteca de widgets
widgets = ctypes.CDLL("/home/daniel/tron/programas/TR/modules/ui/widgets.so")

# Configurar widget
config = json.dumps({
    "x": 10,
    "y": 5,
    "width": 40,
    "height": 3,
    "progress": 0.75,
    "label": "CPU"
})

# Inicializar
widgets.progress_init.argtypes = [ctypes.c_char_p]
widgets.progress_init.restype = ctypes.c_void_p
widget_ptr = widgets.progress_init(config.encode())

# Render loop
while True:
    widgets.progress_render(widget_ptr)
    nc.render()
    
    # Obtener estado
    widgets.progress_get_state.restype = ctypes.c_char_p
    state_json = widgets.progress_get_state(widget_ptr)
    state = json.loads(state_json)
    print(f"Progreso: {state['progress']}")
    
    time.sleep(0.1)

# Limpiar
widgets.progress_destroy(widget_ptr)
```

### Flujo de Trabajo Modular

```
┌─────────────────────────────────────────────────────────┐
│                    PYTHON (Orquestador)                  │
│  - Inicializa notcurses                                  │
│  - Carga configuración JSON                              │
│  - Llama widgets C vía ctypes                            │
│  - Maneja input del usuario                              │
│  - Render loop                                           │
└─────────────────────────────────────────────────────────┘
                            │
                            │ ctypes / CFFI
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    C (Widgets)                           │
│  - widget_progress.c  → Barras, spinners                │
│  - widget_table.c     → Tablas de datos                 │
│  - widget_menu.c      → Menús navegables                 │
│  - widget_chart.c     → Gráficos (plots)                │
│  - widget_image.c     → Imágenes con ncvisual           │
│                                                            │
│  Cada widget:                                              │
│  ✓ Recibe JSON config                                      │
│  ✓ Renderiza en su plano                                   │
│  ✓ Devuelve estado JSON                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 CHECKLIST PARA DEBUGGAR "DESORDEN"

### 1. ¿Se está renderizando?

```python
# ❌ MAL - Sin render
stdplane.putEGCYX(0, 0, "Hola")
# Nunca se ve

# ✅ BIEN
stdplane.putEGCYX(0, 0, "Hola")
nc.render()  # ← Crucial
```

### 2. ¿Se limpia la pantalla antes?

```python
# ❌ MAL - Acumula frames
for i in range(100):
    stdplane.putEGCYX(0, 0, f"Frame {i}")
    nc.render()
# Se ve todo mezclado

# ✅ BIEN
for i in range(100):
    stdplane.erase()  # ← Limpiar antes
    stdplane.putEGCYX(0, 0, f"Frame {i}")
    nc.render()
```

### 3. ¿Los planos están en el orden correcto?

```python
# ❌ MAL - Imagen tapa texto
img_plane = plane_create(...)
text_plane = plane_create(...)
# text_plane queda debajo de img_plane

# ✅ BIEN
img_plane = plane_create(...)
text_plane = plane_create(...)
ncplane_move_above(text_plane, img_plane)  # ← Mover texto arriba
```

### 4. ¿Las coordenadas son correctas?

```python
# ❌ MAL - Coordenadas negativas o fuera de rango
stdplane.putEGCYX(-1, -1, "Texto")  # Comportamiento indefinido

# ✅ BIEN
rows, cols = stdplane.getDimensions()
stdplane.putEGCYX(0, 0, "Esquina superior izquierda")
stdplane.putEGCYX(rows-1, cols-1, "Esquina inferior derecha")
```

### 5. ¿El terminal soporta lo que intentas?

```python
from notcurses.visual import can_pixel, can_truecolor, can_utf8

print(f"Pixel: {can_pixel(nc)}")      # Si False, NCBLIT_PIXEL no funciona
print(f"Truecolor: {can_truecolor(nc)}")  # Si False, colores limitados
print(f"UTF-8: {can_utf8(nc)}")       # Si False, unicode se ve mal
```

---

## 🔗 REFERENCIAS

### Archivos Clave en Repositorio notcurses

| Archivo | Propósito | Líneas |
|---------|-----------|--------|
| `doc/examples/src/rendered.md` | Tutorial modo renderizado | ~200 |
| `doc/examples/src/planes.md` | Tutorial de planos | ~150 |
| `doc/examples/src/media.md` | Tutorial de imágenes | ~180 |
| `src/demo/demo.c` | Demo principal (orquestación) | 618 |
| `src/demo/intro.c` | Intro con gradientes/boxes | 248 |
| `src/demo/view.c` | Viewer de imágenes/video | 209 |
| `src/demo/trans.c` | Transparencias | 318 |
| `src/demo/sliders.c` | Widgets animados | 227 |
| `src/demo/box.c` | Boxes y bordes | 286 |
| `python/examples/002-hello-world.py` | Hello world Python | ~30 |
| `python/examples/007-plane_split.py` | Planos hijos Python | ~40 |

### Headers C para Consulta

- `/home/daniel/borrar/notcurses/include/notcurses/notcurses.h` - API completa (3500+ líneas)
- `/home/daniel/borrar/notcurses/include/notcurses/ncvisual.h` - ncvisual específico

---

## 📌 PRÓXIMOS PASOS

1. **Extender `notcurses.py`** con métodos faltantes:
   - `Ncplane.erase()`
   - `Ncplane.move(y, x)`
   - `Ncplane.box()`
   - `Ncplane.gradient()`

2. **Crear módulo de widgets C**:
   - `widgets.so` con funciones exportadas
   - JSON config/state para cada widget

3. **Test de imagen completo**:
   - Layout estructurado (header/body/footer)
   - Múltiples planos con imágenes
   - Input handling para navegación

4. **Documentar en agenda.md** el progreso

---

**Fin del documento** - 15-03-2026

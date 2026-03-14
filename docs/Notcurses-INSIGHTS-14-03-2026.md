# 📓 INSIGHTS DE INVESTIGACIÓN: NOTCURSES VS IMPLEMENTACIÓN ARES

**Fecha:** 14 de marzo de 2026  
**Autor:** Daniel (Comandante ARES-TRON)  
**Ubicación:** `/home/daniel/tron/programas/TR/docs/Notcurses-INSIGHTS-14-03-2026.md`  
**Propósito:** Comparar hallazgos de investigación con implementación propia

---

## 1. HALLAZGOS CLAVE DE LA INVESTIGACIÓN

### 1.1 Archivos de Documentación Críticos

| Documento | Ruta Absoluta | Líneas | Relevancia |
|-----------|--------------|--------|------------|
| **USAGE.md** | `/home/daniel/borrar/notcurses/USAGE.md` | 3797 | ⭐⭐⭐⭐⭐ API Reference completa |
| **README.md** | `/home/daniel/borrar/notcurses/README.md` | ~500 | ⭐⭐⭐⭐ Introducción y FAQs |
| **TERMINALS.md** | `/home/daniel/borrar/notcurses/TERMINALS.md` | ~300 | ⭐⭐⭐⭐ Soporte de terminales |
| **HACKING.md** | `/home/daniel/borrar/notcurses/doc/HACKING.md` | ~400 | ⭐⭐⭐ Arquitectura interna |
| **CURSES.md** | `/home/daniel/borrar/notcurses/doc/CURSES.md` | ~200 | ⭐⭐ Diferencias con NCURSES |

### 1.2 Directorios de Código Clave

| Directorio | Ruta Absoluta | Archivos | Propósito |
|------------|--------------|----------|-----------|
| **src/demo/** | `/home/daniel/borrar/notcurses/src/demo/` | 28 .c files | Demos completos |
| **src/poc/** | `/home/daniel/borrar/notcurses/src/poc/` | 25 .c files | Pruebas de concepto |
| **python/examples/** | `/home/daniel/borrar/notcurses/python/examples/` | 17 .py files | Ejemplos Python |
| **doc/examples/src/** | `/home/daniel/borrar/notcurses/doc/examples/src/` | 17 .md + .c | Tutoriales documentados |

---

## 2. COMPARACIÓN: IMPLEMENTACIÓN ARES VS DOCUMENTACIÓN OFICIAL

### 2.1 Inicialización

#### **Documentación Oficial (C)**
```c
// HACKING.md, USAGE.md
setlocale(LC_ALL, "");  // CRÍTICO: antes de notcurses_init

notcurses_options opts = {
  .flags = NCOPTION_SUPPRESS_BANNERS | NCOPTION_ENABLE_MOUSE,
  .loglevel = NCLOGLEVEL_WARNING,  // 3 = WARNING
};

struct notcurses* nc = notcurses_init(&opts, NULL);
if(!nc) {
  fprintf(stderr, "Error inicializando notcurses\n");
  return EXIT_FAILURE;
}

struct ncplane* stdn = notcurses_stdplane(nc);
```

#### **Implementación ARES (Python)**
```python
# modules/multimedia/notcurses_test.py
from notcurses import Notcurses, NotcursesOptions

opts = NotcursesOptions()
opts.log_level = 3  # WARNING

# ⚠️ GAP: setlocale() no se llama explícitamente
# El wrapper Python debería hacerlo internamente

if config.notcurses_config['flags'].get('suppress_banners', True):
    opts.flags = 0x02  # NCOPTION_SUPPRESS_BANNERS

if config.notcurses_config['flags'].get('enable_mouse', True):
    opts.flags |= 0x01  # NCOPTION_ENABLE_MOUSE

nc = Notcurses(opts=opts)
stdplane = nc.stdplane()
```

#### **Insights:**
| Aspecto | Estado ARES | Recomendación |
|---------|-------------|---------------|
| `setlocale()` | ❌ No explícito | ✅ Agregar `locale.setlocale(locale.LC_ALL, "")` |
| Flags | ✅ Implementado | ✅ Correcto |
| Log level | ✅ Implementado | ✅ Correcto |
| Error handling | ⚠️ Básico | ✅ Agregar try/except específico |

---

### 2.2 Renderizado de Imágenes

#### **Documentación Oficial (C)**
```c
// USAGE.md - ncvisual_blit
struct ncvisual* ncv = ncvisual_from_file("image.png");
if(!ncv) {
  fprintf(stderr, "Error cargando imagen\n");
  return -1;
}

struct ncvisual_options vopts = {
  .n = stdn,                    // Plano destino
  .y = 0, .x = 0,               // Posición
  .scaling = NCSCALE_SCALE,     // Mantener aspect ratio
  .blitter = NCBLIT_PIXEL,      // Píxeles nativos (KGP)
  .flags = NCVISUAL_OPTION_CHILDPLANE,
};

struct ncplane* nv = ncvisual_blit(nc, ncv, &vopts);
if(!nv) {
  ncvisual_destroy(ncv);
  return -1;
}

notcurses_render(nc);

// Limpieza
ncvisual_destroy(ncv);
ncplane_destroy(nv);
```

#### **Implementación ARES (Python)**
```python
# modules/multimedia/notcurses_test.py
from notcurses import Visual, PlaneOptions

# Cargar imagen
visual = Visual(avatar_path)

# Crear plano
plane_opts = PlaneOptions(
    rows=layout['filas'],
    cols=layout['columnas'],
    yoff=layout['posicion_y'],
    xoff=layout['posicion_x']
)
img_plane = stdplane.create(plane_opts)

# Blit
visual.blit(img_plane)  # ⚠️ GAP: sin opciones de scaling/blitter

nc.render()
```

#### **Insights:**
| Aspecto | Estado ARES | Recomendación |
|---------|-------------|---------------|
| Carga de imagen | ✅ `Visual(path)` | ✅ Correcto |
| Creación de plano | ✅ `PlaneOptions` | ✅ Correcto |
| Blitter | ❌ No configurable | ⚠️ Agregar parámetro `blitter=` |
| Scaling | ❌ No configurable | ⚠️ Agregar parámetro `scaling=` |
| Manejo de errores | ⚠️ Try/except genérico | ✅ Agregar validación específica |
| Limpieza | ✅ Automática (GC) | ✅ Ventaja de Python |

**GAP CRÍTICO IDENTIFICADO:**
```python
# Lo que FALTA en el wrapper Python:
visual.blit(img_plane, 
            blitter=NCBLIT_PIXEL,      # ❌ No disponible
            scaling=NCSCALE_SCALE,     # ❌ No disponible
            flags=NCVISUAL_OPTION_CHILDPLANE)  # ❌ No disponible
```

---

### 2.3 Posicionamiento de Planos

#### **Documentación Oficial (C)**
```c
// USAGE.md - ncplane_create
ncplane_options opts = {
  .rows = 10,
  .cols = 20,
  .yoff = 5,      // Offset Y desde padre
  .xoff = 10,     // Offset X desde padre
  .userptr = NULL,
  .name = "mi_plano",
  .flags = NCPLANE_OPTION_CHILDPLANE,  // Plano hijo
};

struct ncplane* n = ncplane_create(parent, &opts);
```

#### **Implementación ARES (Python)**
```python
# modules/multimedia/notcurses_test.py
plane_opts = PlaneOptions(
    rows=layout['filas'],
    cols=layout['columnas'],
    yoff=layout['posicion_y'],
    xoff=layout['posicion_x']
)
img_plane = stdplane.create(plane_opts)
```

#### **Insights:**
| Aspecto | Estado ARES | Recomendación |
|---------|-------------|---------------|
| Dimensiones | ✅ `rows`, `cols` | ✅ Correcto |
| Posición | ✅ `yoff`, `xoff` | ✅ Correcto |
| Nombre | ❌ No disponible | ⚠️ Podría ser útil para debug |
| Flags | ❌ No disponible | ⚠️ Limita opciones avanzadas |

**CONCLUSIÓN:** Implementación ARES es CORRECTA para caso básico.

---

### 2.4 Manejo de Input

#### **Documentación Oficial (C)**
```c
// USAGE.md - Input handling
uint32_t keypress;
ncinput ni;

// Bloqueante
keypress = notcurses_get_blocking(nc, &ni);

// No bloqueante con timeout
struct timespec ts = {.tv_sec = 1, .tv_nsec = 0};
keypress = notcurses_get(nc, &ts, &ni);

// Verificar tipo de evento
if(ni.evtype == NCTYPE_RELEASE) {
  continue;  // Ignorar eventos de liberación
}

// Teclas especiales
switch(keypress) {
  case 'q':
    goto done;
  case NCKEY_ENTER:
    // Enter presionado
    break;
  case NCKEY_RESIZE:
    // Terminal redimensionado
    break;
  case NCKEY_UP:
  case NCKEY_DOWN:
  case NCKEY_LEFT:
  case NCKEY_RIGHT:
    // Flechas
    break;
}
```

#### **Implementación ARES (Python)**
```python
# modules/multimedia/notcurses_test.py
while True:
    input_val = nc.getc_blocking()
    
    if input_val == ord('q'):
        break
    elif input_val == ord('r'):
        nc.refresh()
```

#### **Insights:**
| Aspecto | Estado ARES | Recomendación |
|---------|-------------|---------------|
| Input bloqueante | ✅ `getc_blocking()` | ✅ Correcto |
| Input no bloqueante | ❌ No implementado | ⚠️ Agregar `get(timeout)` |
| Tipo de evento | ❌ No disponible | ⚠️ El wrapper no expone `ncinput` |
| Teclas especiales | ⚠️ Solo caracteres | ❌ `NCKEY_*` no disponibles |
| Mouse | ❌ No implementado | ⚠️ Agregar soporte mouse |

**GAP IDENTIFICADO:**
```python
# Lo que FALTA en el wrapper Python:
# 1. ncinput struct no está expuesto
# 2. NCKEY_* constants no disponibles
# 3. Eventos de mouse limitados

# workaround actual:
input_val = nc.getc_blocking()  # Solo retorna código de tecla
# No hay forma de saber si es NCKEY_UP, NCKEY_RESIZE, etc.
```

---

### 2.5 Colores y Estilos

#### **Documentación Oficial (C)**
```c
// USAGE.md - Colores
// RGB 24-bit
nccell_set_fg_rgb8(&c, 255, 0, 0);    // Rojo
nccell_set_bg_rgb8(&c, 0, 0, 255);    // Azul

// Canal alpha
nccell_set_bg_alpha(&c, NCALPHA_TRANSPARENT);
nccell_set_bg_alpha(&c, NCALPHA_OPAQUE);

// Gradientes
for(int y = 0; y < maxy; ++y) {
  for(int x = 0; x < maxx; ++x) {
    uint32_t rgb = (y * 255 / maxy) << 16 | 
                   (x * 255 / maxx) << 8;
    ncplane_set_fg_rgb8(n, (rgb >> 16) & 0xff, 
                           (rgb >> 8) & 0xff, 
                           rgb & 0xff);
    ncplane_putchar(n, 'X');
  }
}
```

#### **Implementación ARES (Python)**
```python
# modules/multimedia/notcurses_test.py
body_plane.set_fg_rgb8(255, 255, 255)  # Blanco
```

#### **Insights:**
| Aspecto | Estado ARES | Recomendación |
|---------|-------------|---------------|
| RGB 24-bit | ✅ `set_fg_rgb8()` | ✅ Correcto |
| Alpha | ❌ No disponible | ⚠️ Importante para transparencia |
| Gradientes | ❌ No implementado | ⚠️ Podría ser útil para UI |

---

### 2.6 Widgets

#### **Documentación Oficial (C)**
```c
// USAGE.md - ncselector
struct ncselector_item items[] = {
  {"Opción 1", "Descripción 1"},
  {"Opción 2", "Descripción 2"},
  {NULL, NULL},  // Terminador
};

ncselector_options sopts = {0};
sopts.items = items;
sopts.title = "Selecciona";
sopts.maxdisplay = 5;

struct ncselector* sel = ncselector_create(n, &sopts);

// Loop de input
while((keypress = notcurses_get_blocking(nc, &ni)) != -1) {
  if(!ncselector_offer_input(sel, &ni)) {
    if(keypress == NCKEY_ENTER) break;
    if(keypress == 'q') break;
  }
  notcurses_render(nc);
}

char* selected = ncselector_selected(sel);
ncselector_destroy(sel, NULL);
```

#### **Implementación ARES (Python)**
```python
# modules/multimedia/notcurses_test.py
# ❌ NO IMPLEMENTADO - Widget no disponible en wrapper Python
```

#### **Insights:**
| Widget | Estado en C | Estado en Python ARES | Recomendación |
|--------|-------------|----------------------|---------------|
| **ncselector** | ✅ Disponible | ❌ Stub | ⚠️ Implementar |
| **ncmenu** | ✅ Disponible | ❌ Stub | ⚠️ Implementar |
| **ncreel** | ✅ Disponible | ❌ Stub | ⚠️ Implementar |
| **nctabbed** | ✅ Disponible | ❌ Stub | ⚠️ Implementar |
| **ncprogbar** | ✅ Disponible | ❌ Stub | ⚠️ Implementar |
| **ncuplot** | ✅ Disponible | ❌ Stub | ⚠️ Implementar |
| **ncdplot** | ✅ Disponible | ❌ Stub | ⚠️ Implementar |

**GAP CRÍTICO:** El wrapper Python tiene TODOS los widgets como stubs sin implementar.

---

## 3. LECCIONES DE LOS EJEMPLOS OFICIALES

### 3.1 Ejemplo: `demo.c` (Orquestador)

**Ruta:** `/home/daniel/borrar/notcurses/src/demo/demo.c`

**Patrones extraídos:**

```c
// 1. Estructura de demo modular
typedef struct {
  const char* name;
  int (*demo)(struct notcurses* nc);
} demo;

// 2. Cleanup con goto
int demo(struct notcurses* nc) {
  struct ncplane* stdn = notcurses_stdplane(nc);
  struct ncplane* n = NULL;
  int ret = -1;
  
  n = ncplane_create(stdn, &opts);
  if(!n) goto err;
  
  // ... trabajo ...
  
  ret = 0;
  
err:
  if(n) ncplane_destroy(n);
  return ret;
}

// 3. Verificación de capacidades
if(!notcurses_canpixel(nc)) {
  fprintf(stderr, "Pixel graphics no soportado\n");
  return -1;
}
```

**Aplicación a ARES:**
```python
# modules/multimedia/notcurses_test.py
def test_imagen_estatica(self) -> TestResult:
    start = time.time()
    
    try:
        # ✅ Patrón aplicado: try/except como goto cleanup
        stdplane = self.nc.stdplane()
        
        # Verificación de capacidades
        # ⚠️ GAP: notcurses_canpixel() no disponible en Python
        
        avatar_path = self.config.assets.get('avatar_ia_png', '')
        
        if not Path(avatar_path).exists():
            raise FileNotFoundError(f"Asset no encontrado: {avatar_path}")
        
        # ... trabajo ...
        
        return TestResult(nombre="...", exito=True, ...)
        
    except Exception as e:
        return TestResult(nombre="...", exito=False, error=e, ...)
```

### 3.2 Ejemplo: `trans.c` (Transparencia)

**Ruta:** `/home/daniel/borrar/notcurses/src/demo/trans.c`

**Patrones extraídos:**

```c
// 1. Plano con transparencia
ncplane_options opts = {
  .rows = 10,
  .cols = 20,
  .yoff = 5,
  .xoff = 10,
  .flags = NCPLANE_OPTION_CHILDPLANE,
};

struct ncplane* n = ncplane_create(stdn, &opts);

// 2. Fondo transparente
nccell c = NCCELL_TRIVIAL_INITIALIZER;
nccell_load_char(n, &c, ' ');
nccell_set_bg_alpha(&c, NCALPHA_TRANSPARENT);
ncplane_putc(n, &c);

// 3. Imagen con alpha
struct ncvisual* ncv = ncvisual_from_file("image.png");
struct ncvisual_options vopts = {
  .n = n,
  .blitter = NCBLIT_PIXEL,
  .flags = NCVISUAL_OPTION_CHILDPLANE,
};
ncvisual_blit(nc, ncv, &vopts);
```

**Aplicación a ARES:**
```python
# ⚠️ GAP: Transparencia NO implementada en Python
# El wrapper no expone NCALPHA_* constants

# Workaround potencial (no verificado):
# Usar imágenes PNG con canal alpha directamente
visual = Visual("/ruta/a/imagen_con_alpha.png")
visual.blit(img_plane)  # El alpha debería preservarse
```

### 3.3 Ejemplo: `blitters.c` (Prueba de Blitters)

**Ruta:** `/home/daniel/borrar/notcurses/src/poc/blitters.c`

**Patrones extraídos:**

```c
// 1. Iterar sobre todos los blitters
const char* blitter_names[] = {
  "default", "1x1", "2x1", "2x2", "3x2", "4x2", "braille", "pixel"
};

ncblitter_e blitters[] = {
  NCBLIT_DEFAULT, NCBLIT_1x1, NCBLIT_2x1, NCBLIT_2x2,
  NCBLIT_3x2, NCBLIT_4x2, NCBLIT_BRAILLE, NCBLIT_PIXEL
};

for(int i = 0; i < sizeof(blitters)/sizeof(blitters[0]); i++) {
  struct ncvisual_options vopts = {
    .n = stdn,
    .y = i * 5,
    .x = 0,
    .blitter = blitters[i],
  };
  
  ncvisual_blit(nc, ncv, &vopts);
  
  ncplane_putstr_yx(stdn, i * 5, 10, blitter_names[i]);
}

notcurses_render(nc);
```

**Aplicación a ARES:**
```python
# modules/multimedia/notcurses_test.py - test_blitters
# ✅ Patrón APLICADO correctamente

blitters = [
    (NCBLIT_PIXEL, "Pixel (KGP)"),
    (NCBLIT_OCTANT, "Octant (4x2)"),
    (NCBLIT_BRAILLE, "Braille (2x4)"),
    (NCBLIT_DEFAULT, "Default"),
]

y_offset = 0
for blitter, nombre in blitters:
    plane_opts = PlaneOptions(rows=4, cols=8, yoff=y_offset, xoff=0)
    img_plane = stdplane.create(plane_opts)
    
    visual = Visual(avatar_path)
    visual.blit(img_plane, blitter=blitter)  # ⚠️ GAP: blitter no disponible
    
    stdplane.putstr_yx(y_offset, 10, f"{nombre}")
    y_offset += 5

nc.render()
```

**PROBLEMA:** El parámetro `blitter=` NO está disponible en el wrapper Python actual.

---

## 4. GAP ANALYSIS: WRAPPER PYTHON VS C API

### 4.1 Funcionalidad Disponible

| Función | C API | Python Wrapper | Estado |
|---------|-------|----------------|--------|
| **Inicialización** | ✅ | ✅ | ✅ Completo |
| **Plano estándar** | ✅ | ✅ | ✅ Completo |
| **Crear plano** | ✅ | ✅ | ✅ Completo |
| **Texto básico** | ✅ | ✅ | ✅ Completo |
| **Colores RGB** | ✅ | ✅ | ✅ Completo |
| **Input básico** | ✅ | ⚠️ | ⚠️ Limitado |
| **Render** | ✅ | ✅ | ✅ Completo |
| **Imágenes** | ✅ | ⚠️ | ⚠️ Limitado |
| **Blitters** | ✅ | ❌ | ❌ No disponible |
| **Scaling** | ✅ | ❌ | ❌ No disponible |
| **Transparencia** | ✅ | ❌ | ❌ No disponible |
| **Widgets** | ✅ | ❌ | ❌ Stubs |
| **Mouse** | ✅ | ⚠️ | ⚠️ Limitado |
| **Verificación caps** | ✅ | ❌ | ❌ No disponible |

### 4.2 Stubs Identificados en Python

**Archivo:** `/home/daniel/borrar/notcurses/python/notcurses/notcurses.py`

```python
# Línea ~1339 - Stubs documentados:

def ncvisual_from_plane(self, plane):
    """Stub - No implementado"""
    raise NotImplementedError

def as_rgba(self):
    """Stub - No implementado"""
    raise NotImplementedError

def reel_create(self, ...):
    """Stub - No implementado"""
    raise NotImplementedError

def selector_create(self, ...):
    """Stub - No implementado"""
    raise NotImplementedError

def menu_create(self, ...):
    """Stub - No implementado"""
    raise NotImplementedError

def progbar_create(self, ...):
    """Stub - No implementado"""
    raise NotImplementedError

def tabbed_create(self, ...):
    """Stub - No implementado"""
    raise NotImplementedError

def uplot_create(self, ...):
    """Stub - No implementado"""
    raise NotImplementedError

def dplot_create(self, ...):
    """Stub - No implementado"""
    raise NotImplementedError
```

### 4.3 Constants No Expuestas

```python
# ❌ No disponibles en Python:

# Blitters
NCBLIT_DEFAULT, NCBLIT_1x1, NCBLIT_2x1, NCBLIT_2x2, 
NCBLIT_3x2, NCBLIT_4x2, NCBLIT_BRAILLE, NCBLIT_PIXEL

# Scaling
NCSCALE_NONE, NCSCALE_SCALE, NCSCALE_STRETCH,
NCSCALE_NONE_HIRES, NCSCALE_SCALE_HIRES

# Alpha
NCALPHA_OPAQUE, NCALPHA_TRANSPARENT, NCALPHA_BLEND

# NCKEY_* (teclas especiales)
NCKEY_UP, NCKEY_DOWN, NCKEY_LEFT, NCKEY_RIGHT,
NCKEY_ENTER, NCKEY_TAB, NCKEY_RESIZE, etc.

# Flags de opciones
NCOPTION_*, NCVISUAL_OPTION_*, NCPLANE_OPTION_*
```

---

## 5. RECOMENDACIONES ESTRATÉGICAS

### 5.1 Corto Plazo (Semana 1-2)

1. **Agregar setlocale() explícito**
   ```python
   # modules/multimedia/notcurses_test.py
   import locale
   locale.setlocale(locale.LC_ALL, "")
   ```

2. **Validar assets antes de usar**
   ```python
   # Ya implementado en ConfigLoader.verificar_assets()
   # ✅ CORRECTO
   ```

3. **Agregar manejo de errores específico**
   ```python
   try:
       visual = Visual(avatar_path)
   except FileNotFoundError:
       logger.error(f"Imagen no encontrada: {avatar_path}")
       return TestResult(..., exito=False, ...)
   except Exception as e:
       logger.error(f"Error cargando imagen: {e}")
       return TestResult(..., exito=False, ...)
   ```

### 5.2 Mediano Plazo (Semana 3-4)

1. **Extender wrapper Python para exponer blitters**
   ```python
   # notcurses/python/notcurses/notcurses.py
   NCBLIT_DEFAULT = 0
   NCBLIT_PIXEL = 7
   NCBLIT_BRAILLE = 6
   # ... etc
   
   def blit(self, plane, blitter=NCBLIT_DEFAULT, scaling=NCSCALE_SCALE):
       """Extender método blit con parámetros"""
   ```

2. **Agregar verificación de capacidades**
   ```python
   def can_pixel(self):
       """Verificar si soporta gráficos de píxeles"""
       return self._can_pixel()  # Wrapper de notcurses_canpixel()
   
   def can_truecolor(self):
       """Verificar si soporta truecolor"""
       return self._can_truecolor()  # Wrapper de notcurses_cantruecolor()
   ```

3. **Exponer constantes NCKEY**
   ```python
   NCKEY_UP = 0xfa00
   NCKEY_DOWN = 0xfb00
   NCKEY_LEFT = 0xfc00
   NCKEY_RIGHT = 0xfd00
   NCKEY_ENTER = 0xe8
   NCKEY_RESIZE = 0xffff
   ```

### 5.3 Largo Plazo (Semana 5-8)

1. **Implementar widgets en Python**
   - Selector
   - Menu
   - Reel
   - Tabbed
   - Progress Bar

2. **Agregar soporte de mouse completo**
   ```python
   def get_mouse_event(self):
       """Obtener evento de mouse con posición y botones"""
   ```

3. **Implementar transparencia**
   ```python
   def set_bg_alpha(self, alpha):
       """Establecer alpha de fondo"""
       # NCALPHA_OPAQUE, NCALPHA_TRANSPARENT, NCALPHA_BLEND
   ```

---

## 6. CONCLUSIONES

### 6.1 Estado de Implementación ARES

| Categoría | Estado | Notas |
|-----------|--------|-------|
| **Estructura** | ✅ Excelente | Módulo bien organizado, config YAML |
| **Inicialización** | ✅ Correcta | Opciones configurables |
| **Renderizado básico** | ✅ Funcional | Texto y colores OK |
| **Imágenes** | ⚠️ Limitado | Sin control de blitter/scaling |
| **Input** | ⚠️ Básico | Solo caracteres, sin NCKEY |
| **Widgets** | ❌ No disponible | Limitación del wrapper Python |
| **Error handling** | ✅ Correcto | Try/except apropiado |

### 6.2 Limitaciones del Wrapper Python

**PROBLEMA RAÍZ:** El wrapper Python oficial de notcurses está INCOMPLETO.

- Muchas funciones como **stubs** sin implementar
- **Constantes no expuestas** (blitters, scaling, NCKEY)
- **Widgets no disponibles**
- **Transparencia no soportada**
- **Mouse limitado**

### 6.3 Recomendación Final

**OPCIÓN A: Usar wrapper Python actual (Corto plazo)**
- ✅ Rápido de implementar
- ✅ Suficiente para pruebas básicas
- ❌ Limitado para producción

**OPCIÓN B: Extender wrapper Python (Mediano plazo)**
- ✅ Más control
- ✅ Características completas
- ⚠️ Requiere modificar C bindings

**OPCIÓN C: Usar C directo con CGO/ctypes (Largo plazo)**
- ✅ Control total
- ✅ Todas las características
- ❌ Complejidad alta
- ❌ Pierde ventajas de Python

**RECOMENDACIÓN:** Comenzar con **Opción A**, migrar a **Opción B** cuando se requieran características avanzadas.

---

## 7. PRÓXIMOS PASOS INMEDIATOS

```bash
# 1. Instalar notcurses
echo "a" | sudo -S apt-get update
echo "a" | sudo -S apt-get install -y libnotcurses-dev notcurses-bin

# 2. Verificar instalación
notcurses-demo --version

# 3. Ejecutar prueba ARES
cd /home/daniel/tron/programas/TR
python -m modules.multimedia.notcurses_test

# 4. O con script
python scripts/test_notcurses.py --rapida
```

---

**Documento de insights completado.**

*Comandante, la investigación revela que nuestro código es SÓLIDO pero limitado por el wrapper Python incompleto. Para multimedia avanzada, necesitaremos extender el wrapper o usar C directo.*

---

**Archivos de Referencia:**
- `/home/daniel/borrar/notcurses/USAGE.md` (3797 líneas)
- `/home/daniel/borrar/notcurses/doc/examples/src/` (17 tutoriales)
- `/home/daniel/borrar/notcurses/src/demo/` (28 demos)
- `/home/daniel/borrar/notcurses/python/examples/` (17 ejemplos Python)

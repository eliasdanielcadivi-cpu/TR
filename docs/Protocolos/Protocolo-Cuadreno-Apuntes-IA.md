# 📓 PROTOCOLO: CUADERNO DE APUNTES IA

### **Filosofía**
> **"Leer todo, extraer lo pertinente, crear guía progresiva y secuencial"**

Al investigar una tecnología nueva (ej. notcurses, ffmpeg, librerías C/C++):

1. **No copiar todo** - El repositorio/documentación original ya existe
2. **Extraer patrones clave** - Identificar lo aplicable a nuestro caso
3. **Crear "cuaderno de apuntes"** - Guía en `docs/[Tecnologia]/` con formato:
   - Nombre: `[Tecnologia]-[Parte/Funcionalidad]-[Módulo(s) TR].md`
   - Ejemplo: `Notcurses-imagenes-renderizado-multimedia-notcurses_test.md`

### **Estructura del Cuaderno de Apuntes**

```markdown
# [Tecnología] - [Parte/Funcionalidad]
## Módulo: [módulo(s) TR que trabajan con esto]

1. **Problema Detectado** - Síntomas observados
2. **Causa Raíz** - Por qué ocurre
3. **API Disponible** - Funciones/constants clave (C/C++/Python)
4. **Solución Implementada** - Código creado
5. **Flujo de Trabajo** - Cómo usarlo paso a paso
6. **Qué Deberías Ver** - Descripción visual de pruebas
7. **Patrones Extraídos** - Código de tutoriales/demos adaptado
8. **Widgets Modulares** - Integración C → JSON (si aplica)
9. **Checklist Debug** - Problemas comunes y soluciones
10. **Referencias** - Archivos clave en repositorio original
```

### **Ubicación de Guías**

| Tecnología | Carpeta | Ejemplo de Archivo |
|------------|---------|-------------------|
| Notcurses | `docs/Notcurses/` | `Notcurses-imagenes-renderizado-multimedia-notcurses_test.md` |
| FFmpeg | `docs/FFmpeg/` | `FFmpeg-decode-video-multimedia-ffmpeg_decode.md` |
| SQLite | `docs/SQLite/` | `SQLite-vector-search-rag-sqlite_vector.md` |

### **Flujo de Investigación**

```
1. Explorar repositorio/documentación original
   ├── Tutoriales (doc/examples/, docs/)
   ├── Demos (src/demo/, examples/)
   ├── Tests (tests/, test/)
   └── Headers (include/, *.h)

2. Identificar patrones aplicables
   ├── ¿Qué problemas resuelve?
   ├── ¿Cómo lo hace?
   └── ¿Qué puedo adaptar?

3. Crear/Actualizar cuaderno de apuntes
   ├── Copiar código C/C++ relevante (sin wrapper)
   ├── Traducir a Python si es necesario
   ├── Documentar qué se debería ver (expectativas)
   └── Checklist de problemas comunes

4. Implementar en TR
   ├── Crear módulo básico funcional
   ├── Extender si es necesario (visual.py)
   └── Testear con expectativas claras

5. Actualizar agenda.md con progreso
```

### **Principio de Mínima Envoltura**

**NO crear wrappers Python complejos** a menos que sea estrictamente necesario:

- ✅ **Sí:** Usar CFFI/ctypes para llamar funciones C directamente
- ✅ **Sí:** Crear widgets C que reciben JSON y devuelven JSON
- ❌ **No:** Re-implementar toda la API C en Python
- ❌ **No:** Traducir documentación completa

**Ejemplo: Widget C → JSON**

```c
// widget_progress.c - Recibe JSON, renderiza, devuelve estado
progress_widget_t* progress_init(const char* json_config);
void progress_render(progress_widget_t* w);
char* progress_get_state(progress_widget_t* w);  // JSON
void progress_destroy(progress_widget_t* w);
```

```python
# Python solo orquesta
import ctypes
widgets = ctypes.CDLL("widgets.so")
widget = widgets.progress_init(b'{"progress": 0.75, "label": "CPU"}')
widgets.progress_render(widget)
state = json.loads(widgets.progress_get_state(widget))
```

### **Actualización Progresiva**

- Las guías **NO son estáticas** - Se actualizan con cada descubrimiento
- Si otra IA encuentra un problema/solución → Actualizar guía
- Usar `git diff` para validar cambios en guías
- Commit en TR para control histórico

---

---

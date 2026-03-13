# TR Color Module - Documentación Técnica

## 📋 Descripción General

El módulo de color de TR proporciona coloreado automático de pestañas Kitty basado en rutas de archivos o patrones de directorios. Es un módulo **independiente** y **opcional** que no altera la funcionalidad existente de TR.

## 🎯 Objetivos

1. **Independencia**: Kitty debe ser independiente de la pigmentación del sistema (KDE, Openbox, LX, qt5ct)
2. **Automatización**: Coloreado automático según la ruta del archivo abierto
3. **Persistencia**: El color persiste mientras la pestaña esté abierta
4. **Modularidad**: Puede ser depurado sin afectar el resto de TR

## 🏗️ Arquitectura

```
modules/color/
├── __init__.py           # Exporta ColorEngine, ColorRule
├── color_engine.py       # Motor principal de matching y aplicación
├── config.yaml           # Reglas de coloreado (ruta → color/título)
└── README.md             # Documentación de uso

bin/
└── tr-color              # CLI independiente (headless)

src/
└── main.py               # Comando 'tr color' integrado
```

## 🔧 Componentes

### 1. ColorEngine (`color_engine.py`)

Clase principal que maneja:
- Carga de reglas desde YAML
- Matching de patrones (fnmatch)
- Aplicación de colores vía kitty remote control

```python
from modules.color import ColorEngine

engine = ColorEngine('modules/color/config.yaml')

# Obtener regla para una ruta
rule = engine.get_rule_for_path('/ruta/al/archivo')
print(rule['color'])  # #ff6600
print(rule['title'])  # "EL ASUNTO"

# Aplicar color a kitty
success = engine.apply('/ruta/al/archivo')
```

### 2. Configuración (`config.yaml`)

Formato de reglas:

```yaml
rules:
  - pattern: "/home/daniel/Escritorio/QT5/elAsunto.md"
    color: "#ff6600"
    title: "EL ASUNTO"
    priority: 10

  - pattern: "/home/daniel/Escritorio/QT5/*"
    color: "#39ff14"
    title: "QT5"
    priority: 5

defaults:
  color: "#39ff14"
  title: "KITTY"
```

**Campos:**
- `pattern`: Patrón fnmatch (ruta absoluta o con wildcards)
- `color`: Color hexadecimal (#RRGGBB)
- `title`: Título visible en la pestaña
- `priority`: Prioridad (mayor = más prioritario)

### 3. CLI (`bin/tr-color`)

Comando independiente para uso directo:

```bash
# Aplicar color por ruta
tr-color /home/daniel/Escritorio/QT5/elAsunto.md

# Auto-detectar archivo reciente
tr-color --auto

# Listar reglas
tr-color --list

# Testear sin aplicar
tr-color --test /ruta/al/archivo
```

### 4. Integración TR (`src/main.py`)

Comando integrado en TR:

```bash
tr color /ruta/al/archivo
tr color --auto
tr color --list
```

## 🎨 Reglas Configuradas

### Archivos Específicos QT5 (Prioridad: 10)

| Archivo | Color | Título |
|---------|-------|--------|
| elAsunto.md | #ff6600 (Naranja) | EL ASUNTO |
| PRUEBAS_MAPA.md | #00ccff (Cyan) | PRUEBAS MAPA |
| solucion-del-blanco-rebelde.md | #ff0066 (Rosa) | BLANCO REBELDE |
| SelectorHacker/index.html | #00ff00 (Verde) | SELECTOR HTML |
| SelectorHacker/server.js | #ffff00 (Amarillo) | SELECTOR SERVER |

### Directorios (Prioridad: 5)

| Directorio | Color | Título |
|------------|-------|--------|
| /home/daniel/Escritorio/QT5/* | #39ff14 (Verde Neón) | QT5 |
| /home/daniel/tron/* | #00ffff (Cyan) | TRON |
| /home/daniel/Escritorio/* | #ff9900 (Naranja) | ESCRITORIO |

### Extensiones (Prioridad: 2)

| Extensión | Color | Título |
|-----------|-------|--------|
| *.md | #66ccff | MARKDOWN |
| *.py | #ffcc00 | PYTHON |
| *.js | #ffff66 | JAVASCRIPT |
| *.html | #ff6666 | HTML |
| *.css | #66ffcc | CSS |
| *.sh | #ccff66 | BASH |

## 🔌 Integración con Kitty

### Remote Control

El módulo usa `kitten @` para:
1. Cambiar título de pestaña: `kitten @ set-tab-title "TÍTULO"`
2. Enviar secuencia de escape de color: `OSC 1 ; #COLOR BEL`

### Requisitos

- Kitty corriendo con `allow_remote_control yes`
- Socket disponible en `/tmp/mykitty` (configurado en TR)

### Limitaciones

- El color de pestaña via secuencia de escape puede no ser soportado por todos los temas
- El título siempre se aplica correctamente
- Requiere que kitty esté corriendo con el socket activo

## 📝 Uso con IA (LLM)

La IA de TR puede usar el módulo de color:

```bash
tr p "colorea esta pestaña según el archivo que estoy editando"
```

La IA puede:
1. Detectar el archivo actual del contexto
2. Llamar internamente a `tr color <ruta>`
3. Reportar el resultado al usuario

## 🔍 Depuración

### Testear regla sin aplicar

```bash
tr-color --test /ruta/al/archivo
```

Salida esperada:
```
RESULTADO DEL TEST:
============================================================
Ruta:    /home/daniel/Escritorio/QT5/elAsunto.md
Color:   #ff6600
Título:  EL ASUNTO
Patrón:  /home/daniel/Escritorio/QT5/elAsunto.md
Prioridad: 10
============================================================
```

### Verificar kitty remote control

```bash
kitten @ --to unix:/tmp/mykitty ls
```

Si funciona, devuelve JSON con el estado de ventanas/pestañas.

### Logs

El módulo no genera logs por defecto. Para depuración avanzada:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🛠️ Mantenimiento

### Agregar nueva regla

Editar `modules/color/config.yaml`:

```yaml
- pattern: "/nueva/ruta/*"
  color: "#RRGGBB"
  title: "NOMBRE"
  priority: 5
```

### Cambiar color existente

Modificar el valor `color` en la regla correspondiente.

### Eliminar regla

Comentar o remover la regla del YAML.

## 📚 Relación con SelectorHacker

**IMPORTANTE**: Este módulo es **INDEPENDIENTE** de SelectorHacker:

| Característica | tr-color (TR) | SelectorHacker |
|----------------|---------------|----------------|
| Objetivo | Colores de pestañas kitty | Colores del sistema (qt5ct) |
| Ámbito | Solo kitty | KDE, Openbox, LX, Qt apps |
| Persistencia | Mientras pestaña abierta | Permanente (archivo config) |
| Ubicación | modules/color/ | Escritorio/QT5/SelectorHacker/ |

No hay dependencia ni conflicto entre ambos.

## 🚀 Comandos Rápidos

```bash
# Uso directo
tr-color /ruta/al/archivo

# Desde TR
tr color /ruta/al/archivo

# Auto-detectar
tr-color --auto

# Listar reglas
tr-color --list

# Testear
tr-color --test /ruta/al/archivo

# Solo título
tr-color --title /ruta/al/archivo

# Solo color
tr-color --color /ruta/al/archivo
```

## ⚠️ Solución de Problemas

### "Socket /tmp/mykitty no existe"

Kitty no está corriendo con remote control habilitado. Reiniciar kitty:

```bash
kitty --listen-on unix:/tmp/mykitty
```

### "kitty no está en PATH"

Instalar kitty o verificar PATH:

```bash
which kitty
```

### "PyYAML no está instalado"

```bash
cd /home/daniel/tron/programas/TR
uv pip install pyyaml
```

### Los colores no se ven en la pestaña

Algunos temas de kitty no soportan secuencias de escape de color. El título sí debería verse siempre.

## 📖 Referencias

- [Kitty Remote Control](https://sw.kovidgoyal.net/kitty/remote-control/)
- [fnmatch pattern matching](https://docs.python.org/3/library/fnmatch.html)
- [OSC Escape Sequences](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)

---

**Versión**: 1.0.0  
**Autor**: TR Project  
**Licencia**: MIT

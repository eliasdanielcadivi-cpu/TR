# 🖼️ SISTEMA DE EMOJIS PNG PARA ARES — INVENTARIO COMPLETO

**Fecha:** 2026-03-10
**Propósito:** Documentación completa para que cualquier IA pueda manipular el sistema de emojis PNG en el chat de ARES.

---

## 📋 1. INVENTARIO DE ARCHIVOS

### 1.1 Archivos de Código Python

| Archivo | Ruta | Función | Líneas |
|---------|------|---------|--------|
| `emoji_manager.py` | `modules/ia/apollo/emoji_manager.py` | Gestión de emojis PNG | 95 |
| `main.py` | `src/main.py` | Integración en `ares i` | 565 |
| `generation.py` | `modules/ia/apollo/generation.py` | Post-procesamiento de respuestas | 271 |

### 1.2 Archivos de Assets (Imágenes PNG)

| Archivo | Ruta | Tamaño | Uso |
|---------|------|--------|-----|
| `ares-emoji.png` | `assets/ares/ares-emoji.png` | 278 KB | Emoji de ARES (tron-uprising) |
| `user-emoji.png` | `assets/user/user-emoji.png` | 396 KB | Emoji de usuario (luke-skywalker) |

### 1.3 Archivos de Configuración

| Archivo | Ruta | Sección Relevante |
|---------|------|-------------------|
| `config.yaml` | `config/config.yaml` | `ai.apollo`, `ai.aliases`, `ai.post_processing` |
| `ares_help.yaml` | `db/ares_help.yaml` | Comandos `i`, `p`, `apollo`, `model-creator` |

### 1.4 Documentación

| Archivo | Ruta | Propósito |
|---------|------|-----------|
| `FASE0-COMPLETADA-APOLLO-DB.md` | `docs/` | Documentación Fase 0 |
| `FASE1-COMPLETADA-APOLLO-INGESTA.md` | `docs/` | Documentación Fase 1 |
| `MODELOS-ARES.md` | `docs/` | Documentación de modelos y modelfiles |
| `AGENDA-PRUEBAS-FASE3.md` | `docs/` | Agenda de pruebas Fase 3 |
| `RESUMEN-TRABAJO-2026-03-09.md` | `docs/` | Resumen de trabajo |
| `TODO-RAG-GRAFICO-SQLITE-VECTORIAL.md` | `TR/` | TODO principal del proyecto |
| `agenda.md` | `AGENDA/` | Agenda MAESTRA del proyecto |

### 1.5 Scripts de Instalación y Agentes

| Archivo | Ruta | Propósito |
|---------|------|-----------|
| `install_mcat.sh` | `scripts/install_mcat.sh` | Instalación automática de mcat |
| `sherlok/` | `TR/AGENTES/sub-agentes/sherlok/` | Agente forense de indexación |
| `main.py` (sherlok) | `TR/AGENTES/sub-agentes/sherlok/main.py` | Punto de entrada de sherlok |
| `brain.py` | `TR/AGENTES/sub-agentes/sherlok/brain.py` | Análisis con LLM |
| `scanner.py` | `TR/AGENTES/sub-agentes/sherlok/scanner.py` | Escaneo de archivos |
| `persistence.py` | `TR/AGENTES/sub-agentes/sherlok/persistence.py` | SQLite para sherlok |
| `sherlok` (wrapper) | `/usr/bin/sherlok` | Wrapper bash generado por `ini` |

---

## 🎨 2. SISTEMA DE EMOJIS — EXPLICACIÓN TÉCNICA

### 2.1 ¿Qué es?

Sistema que reemplaza emojis Unicode (🤖 👤) por **imágenes PNG personalizadas** renderizadas directamente en la terminal Kitty usando el protocolo gráfico.

### 2.2 ¿Por qué?

| Ventaja | Descripción |
|---------|-------------|
| **Personalización** | Imágenes específicas de la marca ARES |
| **Escalabilidad** | Tamaño controlable (ancho/alto en celdas) |
| **Identidad visual** | Coherencia con branding TRON/ARES |
| **Protocolo nativo** | Kitty soporta imágenes sin dependencias externas |

### 2.3 ¿Cómo funciona?

```python
# Flujo de renderizado
1. emoji_manager.py carga PNG desde assets/
2. term-image convierte PNG a secuencias de escape ANSI
3. Kitty interpreta secuencias y muestra imagen
4. click.echo() imprime en terminal
```

### 2.4 Funciones Públicas

#### `show_emoji(emoji_type, width, height)`
```python
from modules.ia.apollo.emoji_manager import show_emoji

# Mostrar emoji de ARES (4 celdas ancho, 1 alto)
imagen = show_emoji('ares', width=4, height=1)

# Mostrar emoji de usuario (2 celdas ancho, 1 alto)
imagen = show_emoji('user', width=2, height=1)
```

**Parámetros:**
- `emoji_type`: "ares" o "user"
- `width`: Ancho en celdas de terminal (default: 4 para ares, 2 para user)
- `height`: Alto en celdas de terminal (default: 1)

**Retorna:** String con secuencias de escape ANSI o emoji Unicode si falla.

#### `format_output_with_emoji(text, emoji_type, prefix, width, height)`
```python
from modules.ia.apollo.emoji_manager import format_output_with_emoji

# Encabezado con emoji ARES al inicio
header = format_output_with_emoji(
    "MODO INTERACTIVO ARES",
    "ares",
    prefix=True,
    width=4,
    height=1
)

# Prompt con emoji USER al inicio
prompt = format_output_with_emoji(
    "Tú",
    "user",
    prefix=True,
    width=2,
    height=1
)
```

**Parámetros:**
- `text`: Texto a formatear
- `emoji_type`: "ares" o "user"
- `prefix`: True (emoji al inicio) o False (emoji al final)
- `width`, `height`: Dimensiones del emoji

**Retorna:** String formateado con emoji + texto.

#### `get_emoji_path(emoji_type)`
```python
from modules.ia.apollo.emoji_manager import get_emoji_path

# Obtener ruta del emoji de ARES
ruta = get_emoji_path('ares')
# Retorna: PosixPath('/home/daniel/tron/programas/TR/assets/ares/ares-emoji.png')
```

---

## 🔧 3. INTEGRACIÓN EN `ares i`

### 3.1 Flujo de Ejecución

```
ares i (comando)
  ↓
main.py → i_cmd()
  ↓
Importa emoji_manager.format_output_with_emoji()
  ↓
Crea encabezado con emoji ARES
  ↓
Muestra encabezado + opciones
  ↓
Loop interactivo:
  - Muestra prompt con emoji USER
  - Lee input del usuario
  - Procesa con/sin RAG
  - Genera respuesta con emoji ARES
  ↓
Muestra respuesta formateada
```

### 3.2 Código de Integración (main.py)

```python
from modules.ia.apollo.emoji_manager import format_output_with_emoji

# Encabezado
header = format_output_with_emoji(
    "MODO INTERACTIVO ARES",
    "ares",
    prefix=True,
    width=4,
    height=1
)
click.echo(header)

# Prompt de entrada
user_prompt = format_output_with_emoji(
    "Tú",
    "user",
    prefix=True,
    width=2,
    height=1
)
user_input = click.prompt(user_prompt, type=str)

# Respuesta
formatted = format_output_with_emoji(
    full_response,
    "ares",
    prefix=True,
    width=4,
    height=1
)
click.echo(f"\n{formatted}\n")
```

---

## ⚙️ 4. CONFIGURACIÓN DE TAMAÑO

### 4.1 Problema Actual

Las imágenes se ven **enormes** porque `term-image.draw()` renderiza a tamaño completo por defecto.

### 4.2 Solución Propuesta

**Opción A: Redimensionar imágenes PNG**
```bash
# Usar ImageMagick para redimensionar
convert assets/ares/ares-emoji.png -resize 100x25 assets/ares/ares-emoji.png
convert assets/user/user-emoji.png -resize 50x25 assets/user/user-emoji.png
```

**Opción B: Usar parámetros de draw()**
```python
# term-image tiene parámetros específicos por tipo de imagen
from term_image.image import from_file

image = from_file("assets/ares/ares-emoji.png")

# Para BlockImage (PNG sin transparencia)
render = image.draw(
    width=4,           # Ancho en celdas
    height=1,          # Alto en celdas
    preserve_aspect=True
)
```

**Opción C: Pre-renderizar a ASCII/Unicode pequeño**
```python
# Crear versión pequeña de la imagen
# Guardar como PNG de 4x1 celdas (32x8 píxeles aprox)
```

### 4.3 Recomendación

**Opción A (redimensionar PNG)** es la más simple y efectiva:
```bash
# Redimensionar a 4 celdas de ancho (32 píxeles, asumiendo 8x8 por celda)
convert assets/ares/ares-emoji.png -resize 32x8 assets/ares/ares-emoji.png
convert assets/user/user-emoji.png -resize 16x8 assets/user/user-emoji.png
```

---

## 🧪 5. PRUEBAS DE VALIDACIÓN

### 5.1 Prueba Unitaria (Python)

```python
#!/usr/bin/env python3
"""Test de emoji_manager.py"""

from modules.ia.apollo.emoji_manager import (
    show_emoji,
    format_output_with_emoji,
    get_emoji_path,
    ARES_EMOJI,
    USER_EMOJI
)

def test_rutas_existen():
    assert ARES_EMOJI.exists(), "ARES_EMOJI no existe"
    assert USER_EMOJI.exists(), "USER_EMOJI no existe"

def test_show_emoji():
    result = show_emoji('ares')
    assert len(result) > 0, "show_emoji retornó string vacío"
    # Verificar que contiene secuencias ANSI o emoji
    assert '🤖' in result or '\x1b[' in result, "No es imagen ni emoji"

def test_format_output():
    result = format_output_with_emoji("Hola", "ares", prefix=True)
    assert "Hola" in result, "Texto no está en output"

if __name__ == "__main__":
    test_rutas_existen()
    print("✅ Rutas OK")
    test_show_emoji()
    print("✅ show_emoji OK")
    test_format_output()
    print("✅ format_output OK")
    print("\n🎉 Todas las pruebas pasaron")
```

### 5.2 Prueba en Terminal Kitty

```bash
# Ejecutar directamente
cd /home/daniel/tron/programas/TR
source .venv/bin/activate

# Probar show_emoji
python3 -c "from modules.ia.apollo.emoji_manager import show_emoji; print(show_emoji('ares'))"

# Probar ares i
ares i
# Debería mostrar emojis PNG en encabezado y prompt
```

---

## 📝 6. GUÍA PARA IAs FUTURAS

### 6.1 Para Modificar Tamaños

1. **Editar `emoji_manager.py`:**
   - Cambiar parámetros `width` y `height` en `show_emoji()`
   - O redimensionar PNGs con ImageMagick

2. **Re-renderizar:**
   ```bash
   convert assets/ares/ares-emoji.png -resize 32x8 assets/ares/ares-emoji.png
   ```

3. **Probar:**
   ```bash
   python3 -c "from modules.ia.apollo.emoji_manager import show_emoji; print(show_emoji('ares'))"
   ```

### 6.2 Para Añadir Nuevos Emojis

1. **Añadir PNG en `assets/`:**
   ```bash
   cp nuevo-emoji.png assets/otros/nuevo-emoji.png
   ```

2. **Actualizar `emoji_manager.py`:**
   ```python
   OTRO_EMOJI = ASSETS_DIR / "otros" / "nuevo-emoji.png"
   ```

3. **Añadir función o parámetro:**
   ```python
   def show_emoji(emoji_type: str = "ares" | "user" | "otros"):
       ...
   ```

### 6.3 Para Cambiar Emojis Existentes

1. **Reemplazar PNG:**
   ```bash
   cp nuevo-diseno.png assets/ares/ares-emoji.png
   ```

2. **Validar tamaño:**
   ```bash
   identify assets/ares/ares-emoji.png
   # Debería mostrar: PNG 32x8 (o tamaño deseado)
   ```

---

## 🔗 7. DEPENDENCIAS

| Dependencia | Versión | Propósito |
|-------------|---------|-----------|
| `term-image` | 0.7.2 | Renderizado de imágenes PNG en terminal |
| `Pillow` | 10.4.0 | Procesamiento de imágenes (dependencia de term-image) |
| `Kitty` | >=0.25 | Terminal con protocolo gráfico |

### Verificación

```bash
# Verificar term-image instalado
python3 -c "import term_image; print(term_image.__version__)"

# Verificar Kitty soporta protocolo
echo -e '\x1b_Ga=d\x1b\\'
# Debería mostrar imagen de prueba o nada (no error)
```

---

## 📊 8. DIAGRAMA DE FLUJO

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO EJECUTA: ares i                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  main.py → i_cmd()                                          │
│  - Importa format_output_with_emoji()                       │
│  - Determina modelo (ares/ares-think)                       │
│  - Determina RAG dataset                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  MOSTRAR ENCABEZADO                                         │
│  format_output_with_emoji("MODO INTERACTIVO", "ares")       │
│  ↓                                                          │
│  emoji_manager.py:                                          │
│    1. Carga assets/ares/ares-emoji.png                      │
│    2. term_image.from_file()                                │
│    3. image.draw() → secuencias ANSI                        │
│    4. Retorna: "[ANSI] MODO INTERACTIVO"                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LOOP INTERACTIVO                                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. MOSTRAR PROMPT                                   │    │
│  │    format_output_with_emoji("Tú", "user")           │    │
│  │    ↓                                                │    │
│  │    assets/user/user-emoji.png → ANSI + "Tú: "       │    │
│  │                                                     │    │
│  │ 2. LEER INPUT                                       │    │
│  │    user_input = click.prompt()                      │    │
│  │                                                     │    │
│  │ 3. PROCESAR (RAG o directo)                         │    │
│  │    - Si RAG: retrieve() → compress() → generate()   │    │
│  │    - Si directo: ai_engine.ask()                    │    │
│  │                                                     │    │
│  │ 4. MOSTRAR RESPUESTA                                │    │
│  │    format_output_with_emoji(response, "ares")       │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ 9. CHECKLIST DE VALIDACIÓN

- [ ] `assets/ares/ares-emoji.png` existe y es PNG válido
- [ ] `assets/user/user-emoji.png` existe y es PNG válido
- [ ] `modules/ia/apollo/emoji_manager.py` tiene rutas correctas
- [ ] `term-image` está instalado (`uv add term-image`)
- [ ] Kitty soporta protocolo gráfico
- [ ] `ares i` muestra emojis en encabezado
- [ ] `ares i` muestra emoji en prompt "Tú"
- [ ] `ares i` muestra emoji en respuestas
- [ ] Tamaños son apropiados (no enormes)

---

*Documento creado para que cualquier IA pueda mantener y evolucionar el sistema de emojis PNG de ARES.*

# VENTANA vs PESTAÑA en Kitty — Diferenciación Crítica

## Propósito

Este documento existe para **evitar confusión entre título de VENTANA y título de PESTAÑA** en Kitty. Las IAs suelen confundirlos. Leer antes de modificar cualquier configuración de títulos.

---

## Definiciones Quirúrgicas

| Concepto | Qué es | Dónde se ve | Comando kitty |
|----------|--------|-------------|---------------|
| **VENTANA** | OS Window (ventana del sistema operativo) | Barra de título de la ventana (arriba, decoraciones del WM) | `--title` |
| **PESTAÑA** | Tab dentro de la ventana Kitty | Barra de pestañas (tab bar) dentro de Kitty | `--tab-title` |

---

## Jerarquía Visual

```
┌─────────────────────────────────────────────────────┐
│  VENTANA: "Ares por Daniel Hung" (--title)          │ ← Barra de título del WM
├─────────────────────────────────────────────────────┤
│ [PESTAÑA 1: "-"] [PESTAÑA 2: "CODE"] [+ ]          │ ← Tab bar de Kitty
├─────────────────────────────────────────────────────┤
│                                                     │
│   Contenido de la terminal aquí                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Dónde se Configura en ARES/TR

### Título de VENTANA (NO SE TOCA)

**Ubicación:** `config/config.yaml`

```yaml
identity:
  name: "ARES"
  full_name: "Terminal Remote Operations Nexus"
  window_title: "Ares por Daniel Hung"  # ← ESTO
```

**Se aplica en:** `modules/admon/boot_manager.py`

```python
title = ctx_obj.config.get('identity', {}).get('window_title', "ARES")
subprocess.run(["kitty", "--title", title, ...])
```

**Regla de oro:** Este valor **NO SE TOCA**. Es la identidad soberana de la ventana ARES.

---

### Título de PESTAÑA (Inicial mínimo)

**Ubicación inicial:** `modules/admon/boot_manager.py`

```python
# Después de lanzar kitty, setear nombre de primera pestaña
time.sleep(0.3)
subprocess.run([
    "kitty", "@", "--to", socket,
    "set-tab-title", "-"  # ← Nombre mínimo por defecto
])
```

**Nueva pestaña (atajo):** `config/kitty.conf`

```conf
# Antes (MAL):
map ctrl+shift+t  new_tab

# Ahora (BIEN):
map ctrl+shift+t  launch --type=tab --tab-title=-
```

---

## El Buen Camino vs El Mal Camino

### ✅ BUEN CAMINO — Para título de VENTANA

```python
# 1. Leer de config.yaml
title = ctx_obj.config['identity']['window_title']

# 2. Pasar a kitty al lanzar
subprocess.run(["kitty", "--title", title, ...])

# 3. NO tocar después (deja que el WM lo gestione)
```

### ❌ MAL CAMINO — Para título de VENTANA

```python
# ERROR: Usar hardcodeado
subprocess.run(["kitty", "--title", "Mi Ventana", ...])

# ERROR: Cambiar después con set-window-title (confunde al WM)
kitty.run(["set-window-title", "Otro Título"])
```

---

### ✅ BUEN CAMINO — Para título de PESTAÑA

```python
# 1. Al crear pestaña, especificar --tab-title
kitty.run(["launch", "--type=tab", "--tab-title=-", cmd])

# 2. O cambiar existente con set-tab-title
kitty.run(["set-tab-title", "NUEVO_NOMBRE"])

# 3. O desde kitty.conf con atajo
# map ctrl+shift+t  launch --type=tab --tab-title=-
```

### ❌ MAL CAMINO — Para título de PESTAÑA

```python
# ERROR: Usar new_tab sin --tab-title (zsh lo cambia)
map ctrl+shift+t  new_tab

# ERROR: No especificar título y dejar que powerlevel10k lo setee
# (termina mostrando rutas largas como "~/tron/programas/TR/...")
```

---

## Comandos kitty — Referencia Rápida

| Comando | Afecta | Uso |
|---------|--------|-----|
| `--title` | VENTANA | Al lanzar kitty |
| `--tab-title` | PESTAÑA | Al lanzar con `launch --type=tab` |
| `set-window-title` | VENTANA | Remote control (evitar) |
| `set-tab-title` | PESTAÑA | Remote control (correcto) |

---

## Flujo de Arranque ARES

```
ares (sin args)
    ↓
boot_manager.py:launch_ares()
    ↓
1. kitty --title "Ares por Daniel Hung"  ← VENTANA
    ↓
2. kitty @ set-tab-title "-"            ← PESTAÑA 1
    ↓
Ventana lista con pestaña "-"
```

---

## Flujo de Nueva Pestaña

```
Usuario: Ctrl+Shift+T
    ↓
kitty.conf: map ctrl+shift+t launch --type=tab --tab-title=-
    ↓
Nueva pestaña con nombre "-"
```

---

## Por Qué Esta Confusión Ocurre

1. **kitty usa `--title` para VENTANA**, no para pestaña (contraintuitivo)
2. **zsh/powerlevel10k cambia título de pestaña** automáticamente vía escape sequences
3. **IA lee "title" y asume que es pestaña** (error común)
4. **Documentación de kitty dice "window title"** pero window = OS window, no tab

---

## Reglas de Oro para IA

1. **VENTANA = `--title` = config.yaml = NO SE TOCA**
2. **PESTAÑA = `--tab-title` = boot_manager.py / kitty.conf = MÍNIMO POR DEFECTO**
3. **Si ves "title" en código, pregunta: ¿es ventana o pestaña?**
4. **Nunca usar `new_tab` solo, siempre `launch --type=tab --tab-title=X`**
5. **zsh puede cambiar pestaña después, pero el inicial debe ser corto**

---

## Archivos Clave en TR

| Archivo | Qué controla |
|---------|--------------|
| `config/config.yaml` | `identity.window_title` (VENTANA) |
| `modules/admon/boot_manager.py` | Lanza ventana + setea primera pestaña |
| `config/kitty.conf` | Atajo Ctrl+Shift+T para nuevas pestañas |
| `modules/tactico/plan_manager.py` | Pestañas con nombres específicos (plan) |
| `modules/tactico/zsh_plan_manager.py` | Pestañas con nombres específicos (zshPlan) |

---

*Documento creado para evitar que IAs confundan VENTANA con PESTAÑA. Leer antes de modificar títulos.*

# Kitty Initialization - TRON

## 📋 Descripción General

El sistema de inicialización de Kitty de TRON permite que la terminal se ejecute con una configuración centralizada **hacker neon** desde cualquier lugar del sistema, sin modificar la configuración original de Kitty.

## 🎯 Objetivos

1. **Centralización**: La configuración vive en `TR/config/kitty.conf` y se gestiona desde TR
2. **Transparencia**: Kitty usa la configuración TRON automáticamente al ejecutarse
3. **No destructivo**: No modifica la configuración original de Kitty del usuario
4. **Gestión simple**: Comandos `tr init` para gestionar la configuración

## 🏗️ Arquitectura

```
~/.config/kitty/kitty.conf  →  /home/daniel/tron/programas/TR/config/kitty.conf
     (enlace simbólico)              (configuración central TRON)
```

## 🚀 Comandos Rápidos

### Ver Estado de Configuración

```bash
tr init
# o
tr init --status
```

Salida esperada:
```
╭──────────────────────────────────────╮
│ TRON KITTY - Estado de Configuración │
╰──────────────────────────────────────╯

✓ Configuración TRON:
  /home/daniel/tron/programas/TR/config/kitty.conf

✓ Enlace simbólico:
  ~/.config/kitty/kitty.conf → /home/daniel/tron/programas/TR/config/kitty.conf

⚠ Kitty (con socket TRON):
  No está corriendo con remote control
```

### Crear Enlace Simbólico (Configuración Global)

```bash
tr init --link
```

Esto crea un enlace simbólico en `~/.config/kitty/kitty.conf` que apunta a la configuración TRON.

**Efecto**: Kitty usará automáticamente la configuración TRON cada vez que se ejecute, sin importar desde dónde se lance.

### Eliminar Enlace Simbólico

```bash
tr init --unlink
```

Restaura el comportamiento por defecto de Kitty.

### Recargar Configuración en Kitty en Ejecución

```bash
tr init --reload
```

Aplica los cambios de configuración sin necesidad de reiniciar Kitty.

## 🎨 Configuración Hacker Neon Incluida

La configuración TRON incluye:

### Colores de Alto Contraste
- **Fondo**: Hiperoscuro `#030305`
- **Texto**: Cyan neón `#00FFFF`
- **Cursor**: Fuchsia neón `#FF00FF`
- **Pestaña activa**: Fuchsia sobre negro
- **Pestaña inactiva**: Cyan oscuro sobre negro casi puro

### Fuente
- **Familia**: JetBrainsMono Nerd Font
- **Tamaño**: 16pt
- **Ligaduras**: Habilitadas

### Atajos de Teclado
| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+T` | Nueva pestaña |
| `Ctrl+Shift+W` | Cerrar pestaña |
| `Ctrl+Shift+PgUp/PgDn` | Navegar pestañas |
| `Ctrl+Shift+C/V` | Copiar/Pegar |
| `Ctrl+Alt+R` | Recargar configuración |

### Control Remoto
- Habilitado para módulos TR (`tr-color`, `tr-plan`)
- Socket en `/tmp/mykitty`

## 📁 Scripts Disponibles

### tr-kitty-init

Script avanzado de inicialización:

```bash
# Iniciar Kitty con configuración TRON
tr-kitty-init

# Forzar nueva instancia
tr-kitty-init --new

# Recargar configuración
tr-kitty-init --reload

# Ver estado
tr-kitty-init --status

# Crear enlace simbólico
tr-kitty-init --link

# Eliminar enlace simbólico
tr-kitty-init --unlink
```

Ubicación: `/home/daniel/tron/programas/TR/bin/tr-kitty-init`

## 🔧 Flujo de Trabajo Recomendado

### 1. Primera Instalación

```bash
# Crear enlace simbólico global
tr init --link

# Verificar estado
tr init --status

# Iniciar Kitty
kitty
```

### 2. Cambios de Configuración

```bash
# Editar configuración en TR
nvim ~/tron/programas/TR/config/kitty.conf

# Recargar en Kitty existente
tr init --reload
# o
kitty @ load-config ~/tron/programas/TR/config/kitty.conf
```

### 3. Uso Diario

Simplemente ejecuta `kitty` desde cualquier lugar. La configuración TRON se aplicará automáticamente.

## 🎯 Integración con Módulos TR

### tr-color

El módulo de coloreado de pestañas funciona automáticamente:

```bash
# Colorear pestaña según archivo
tr color /ruta/al/archivo.py

# La pestaña tomará el color según las reglas en modules/color/config.yaml
```

### tr-plan

El orquestador táctico lanza Kitty con la configuración TRON:

```bash
tr plan
```

## ⚠️ Solución de Problemas

### "Kitty no usa la configuración TRON"

Verifica el enlace simbólico:

```bash
ls -la ~/.config/kitty/kitty.conf
```

Debe mostrar:
```
kitty.conf -> /home/daniel/tron/programas/TR/config/kitty.conf
```

Si no, recrea el enlace:

```bash
tr init --link
```

### "Socket /tmp/mykitty no existe"

Kitty no se inició con remote control. Reinicia Kitty:

```bash
# Cierra todas las instancias de Kitty
# Luego inicia una nueva
kitty
```

### "Los colores no se ven como esperado"

Algunos temas del sistema pueden interferir. Verifica:

```bash
# Ver configuración actual
kitty @ get-colors

# Recargar configuración
tr init --reload
```

### "Quiero volver a la configuración original de Kitty"

```bash
# Eliminar enlace simbólico
tr init --unlink

# Kitty usará su configuración por defecto (~/.config/kitty/kitty.conf original)
```

## 📚 Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `TR/config/kitty.conf` | Configuración central TRON (editar aquí) |
| `~/.config/kitty/kitty.conf` | Enlace simbólico → configuración TRON |
| `TR/bin/tr-kitty-init` | Script de inicialización avanzado |
| `TR/docs/KITTY_INIT.md` | Esta documentación |

## 🎨 Personalización

### Cambiar Colores

Edita `TR/config/kitty.conf`:

```conf
# Colores base
foreground    #00FFFF    # Color de texto
background    #030305    # Color de fondo
cursor        #FF00FF    # Color de cursor

# Pestaña activa
active_tab_foreground   #030305
active_tab_background   #FF00FF
```

### Cambiar Tamaño de Fuente

```conf
font_size    18.0    # Aumentar tamaño
```

### Cambiar Atajos

```conf
map ctrl+shift+x    new_tab    # Nuevo atajo para nueva pestaña
```

## 🔐 Seguridad

El sistema usa enlaces simbólicos, lo que significa:

- ✅ No se duplica configuración
- ✅ Los cambios en TR se propagan automáticamente
- ✅ Fácil de revertir (`tr init --unlink`)
- ✅ No requiere permisos de root

## 📖 Referencias

- [Kitty Configuration](https://sw.kovidgoyal.net/kitty/conf/)
- [Kitty Remote Control](https://sw.kovidgoyal.net/kitty/remote-control/)
- [LEEME.md](../LEEME.md) - Documentación principal de TRON

---

**Versión**: 1.0.0
**Autor**: TR Project
**Actualizado**: 2026-02-27

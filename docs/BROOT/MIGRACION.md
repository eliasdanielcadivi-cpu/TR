# 📁 BROOT - Migración a TRON

**Fecha:** 5 de marzo de 2026  
**Versión:** 2.0 (Limpia)

---

## 🎯 Objetivo

Migrar **broot** desde linuxbrew hacia el ecosistema encapsulado de TRON, sin alterar PATH, usando enlaces del sistema.

---

## 📊 Estado Final

| Componente | Ubicación |
|------------|-----------|
| Binario puro | `TR/bin/broot-core/broot-bin` (12MB) |
| Wrapper | `TR/bin/broot` |
| Función shell `br` | `TR/bin/br` |
| Configuración | `TR/config/broot/` |
| Enlace sistema | `/usr/bin/broot` → `TR/bin/broot` |
| Backup config | `~/.qwen/backups/broot-system-backup/` |

---

## 🔧 Proceso de Migración

### 1. Backup de Configuración Original

```bash
mkdir -p ~/.qwen/backups/broot-system-backup
cp -r ~/.config/broot/* ~/.qwen/backups/broot-system-backup/
```

---

### 2. Limpieza de Instalación Existente

```bash
# Eliminar symlinks de linuxbrew
rm /home/linuxbrew/.linuxbrew/bin/broot
rm /home/linuxbrew/.linuxbrew/bin/br

# Eliminar symlinks de /usr/local/bin
sudo rm /usr/local/bin/broot
sudo rm /usr/local/bin/br

# Eliminar plugins
rm -rf ~/tron/plugins/broot
```

---

### 3. Crear Wrapper en TR/bin

**Archivo:** `TR/bin/broot`

```bash
#!/bin/bash
TRON_BASE="/home/daniel/tron/programas/TR"
exec "$TRON_BASE/bin/broot-core/broot-bin" \
    --conf "$TRON_BASE/config/broot/conf.hjson" \
    "$@"
```

---

### 4. Crear Enlace en /usr/bin

```bash
chmod +x TR/bin/broot
echo "a" | sudo -S ln -sf TR/bin/broot /usr/bin/broot
```

---

### 5. Crear Función Shell `br`

**Archivo:** `TR/bin/br`

```bash
_TRON_BROOT_BIN=".../broot-core/broot-bin"
_TRON_BROOT_CONF=".../config/broot/conf.hjson"

function br {
    local cmd cmd_file code
    cmd_file=$(mktemp)
    if "$_TRON_BROOT_BIN" --conf "$_TRON_BROOT_CONF" --outcmd "$cmd_file" "$@"; then
        cmd=$(<"$cmd_file")
        command rm -f "$cmd_file"
        eval "$cmd"
    else
        code=$?
        command rm -f "$cmd_file"
        return "$code"
    fi
}
```

---

### 6. Actualizar .bashrc

```bash
# Broot TRON: Función shell br
if [ -f /home/daniel/tron/programas/TR/bin/br ]; then
    source /home/daniel/tron/programas/TR/bin/br
fi
```

---

## 🧪 Verificación

```bash
# En shell interactivo
which broot
# Salida: /usr/bin/broot

broot --version
# Salida: broot 1.55.0

type br
# Salida: br is a function
```

---

## 📁 Estructura

```
tron/programas/TR/
├── bin/
│   ├── broot              # Wrapper (970 bytes)
│   ├── br                 # Función shell (1.4KB)
│   └── broot-core/
│       └── broot-bin      # Binario (12MB)
├── config/
│   └── broot/
│       ├── conf.hjson
│       ├── verbs.hjson
│       └── *.hjson        # 6 skins
└── docs/BROOT/MIGRACION.md

Sistema:
/usr/bin/broot -> TR/bin/broot
```

---

## 🗑️ Pendiente de Orden

Configuración original en `~/.config/broot/` **NO eliminada**.

Espera string: `"borra config broot"`

---

## 📖 Referencias

- [broot install br](https://dystroy.org/broot/install-br/)
- [Documentación oficial](https://dystroy.org/broot/)

---

*Migración limpia, sin alterar PATH, encapsulamiento total.*

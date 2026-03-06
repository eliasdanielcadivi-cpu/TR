# 📁 BROOT - Migración a TRON (v3.0 - Oficial)

**Fecha:** 5 de marzo de 2026  
**Versión:** 3.0 (Binario oficial GitHub)

---

## 🎯 Objetivo

Instalar **broot** desde la fuente oficial (GitHub releases) en el ecosistema TRON, con configuración encapsulada y soporte para variables de entorno (kitty graphics).

---

## 📊 Estado Final

| Componente | Ubicación |
|------------|-----------|
| Binario oficial | `TR/bin/broot-core/broot-bin` (13MB, v1.55.0) |
| Wrapper | `TR/bin/broot` |
| Función shell `br` | `TR/bin/br` |
| Configuración | `TR/config/broot/` |
| Enlace sistema | `/usr/bin/broot` → `TR/bin/broot` |
| Backup config | `~/.qwen/backups/broot-system-backup/` |
| Config antigua | ❌ ELIMINADA (`~/.config/broot`) |

---

## 🔧 Proceso de Migración

### 1. Backup y Limpieza

```bash
# Backup (ya realizado)
mkdir -p ~/.qwen/backups/broot-system-backup
cp -r ~/.config/broot/* ~/.qwen/backups/broot-system-backup/

# Eliminar configuración antigua
rm -rf ~/.config/broot
```

---

### 2. Descargar Binario Oficial

```bash
curl -L https://github.com/Canop/broot/releases/download/v1.55.0/broot_1.55.0.zip -o /tmp/broot.zip
unzip /tmp/broot.zip -d /tmp/broot-extract
```

**Binario Linux x86_64:** `x86_64-unknown-linux-gnu/broot`

---

### 3. Instalar en TRON

```bash
# Copiar binario oficial
sudo cp /tmp/broot-extract/x86_64-unknown-linux-gnu/broot TR/bin/broot-core/broot-bin
sudo chmod +x TR/bin/broot-core/broot-bin
```

---

### 4. Crear Wrapper con Variables de Entorno

**Archivo:** `TR/bin/broot`

```bash
#!/bin/bash
TRON_BASE="/home/daniel/tron/programas/TR"
BROOT_BIN="$TRON_BASE/bin/broot-core/broot-bin"
BROOT_CONF="$TRON_BASE/config/broot/conf.hjson"

# Preservar TERM para kitty graphics
export TERM="${TERM:-xterm-256color}"

exec "$BROOT_BIN" --conf "$BROOT_CONF" "$@"
```

---

### 5. Crear Enlace en /usr/bin

```bash
chmod +x TR/bin/broot
sudo ln -sf TR/bin/broot /usr/bin/broot
```

---

### 6. Función Shell `br`

**Archivo:** `TR/bin/br`

```bash
_TRON_BROOT_BIN=".../broot-core/broot-bin"
_TRON_BROOT_CONF=".../config/broot/conf.hjson"

function br {
    local cmd cmd_file code
    cmd_file=$(mktemp)
    export TERM="${TERM:-xterm-256color}"
    
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

### 7. Actualizar .bashrc

```bash
# Broot TRON: Función shell br
if [ -f /home/daniel/tron/programas/TR/bin/br ]; then
    source /home/daniel/tron/programas/TR/bin/br
fi
```

---

## 🧪 Verificación

```bash
# Función br
source ~/.bashrc
type br
# Salida: br is a function

br --version
# Salida: broot 1.55.0

# Binario
which broot
# Salida: /usr/bin/broot

broot --version
# Salida: broot 1.55.0
```

---

## 📁 Estructura

```
tron/programas/TR/
├── bin/
│   ├── broot              # Wrapper con variables de entorno
│   ├── br                 # Función shell (source)
│   └── broot-core/
│       └── broot-bin      # Binario oficial (13MB)
├── config/
│   └── broot/
│       ├── conf.hjson     # Config principal
│       ├── verbs.hjson    # Verbos personalizados
│       └── *.hjson        # 6 skins
└── docs/BROOT/MIGRACION.md

Sistema:
/usr/bin/broot -> TR/bin/broot
```

---

## 🗑️ Limpieza Realizada

- ✅ `~/.config/broot/` ELIMINADA
- ✅ linuxbrew symlinks eliminados
- ✅ /usr/local/bin symlinks eliminados
- ✅ ~/tron/plugins/broot eliminado

---

## 🔌 Variables de Entorno

### Específicas de Broot

| Variable | Propósito |
|----------|-----------|
| `BR_*` | Configuración en línea de comandos |
| `BROOT_*` | Configuración general |

### Sistema

| Variable | Propósito |
|----------|-----------|
| `TERM` | Si contiene "kitty" → protocolo gráfico kitty |
| `TERMINAL` | Alternativa a TERM |

---

## 📖 Referencias

- [GitHub Releases](https://github.com/Canop/broot/releases)
- [Install br](https://dystroy.org/broot/install-br/)
- [Variables de entorno](https://dystroy.org/broot/config-file/)
- [Kitty graphics protocol](https://dystroy.org/broot/images/)

---

*Migración completa: binario oficial, configuración TRON, variables preservadas.*

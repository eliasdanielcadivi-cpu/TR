# 🛡️ ARES como Terminal Predeterminada del Sistema

**Fecha:** 5 de marzo de 2026  
**Autor:** Daniel Hung  
**Versión:** 1.0

---

## 📋 Resumen Ejecutivo

Este documento detalla la configuración forense aplicada para establecer **ARES** (`/usr/bin/ares`) como la terminal predeterminada en todo el entorno gráfico Openbox/LXQt de Lubuntu.

### Objetivo
Reemplazar **Konsole** y cualquier otra terminal por **ARES** en todos los puntos de lanzamiento del sistema.

---

## 🔍 Análisis Forense Previo

### Estado Original del Sistema

| Componente | Terminal Original |
|------------|-------------------|
| `x-terminal-emulator` | `/usr/bin/konsole` |
| Menú Openbox | `x-terminal-emulator` |
| Atajo `Ctrl+Alt+T` | `konsole` |
| Dolphin (F4) | `konsole` |
| LXSession | `lxterminal` |
| LXPanel | `lxterminal` |
| Tint2 Launcher | `x-terminal-emulator.desktop` |

---

## 🛠️ Cambios Aplicados

### 1. **Alternativas del Sistema** (`update-alternatives`)

**Archivo:** `/etc/alternatives/x-terminal-emulator`

**Comando ejecutado:**
```bash
echo "a" | sudo -S update-alternatives --install /usr/bin/x-terminal-emulator x-terminal-emulator /usr/bin/ares 45
```

**Resultado:**
```
x-terminal-emulator → /usr/bin/ares (prioridad 45)
```

**Impacto:** Todas las aplicaciones que usan `x-terminal-emulator` ahora lanzan ARES.

---

### 2. **Openbox - Menú Contextual**

**Archivo:** `~/.config/openbox/menu.xml`

**Cambio:**
```xml
<!-- ANTES -->
<item label="Terminal emulator">
  <action name="Execute">
    <execute>x-terminal-emulator</execute>
  </action>
</item>

<!-- DESPUÉS -->
<item label="Terminal ARES">
  <action name="Execute">
    <execute>/usr/bin/ares</execute>
  </action>
</item>
```

---

### 3. **Openbox - Atajos de Teclado**

**Archivo:** `~/.config/openbox/rc.xml`

**Cambio:**
```xml
<!-- ANTES -->
<keybind key="C-A-t">
  <action name="Execute">
    <command>konsole</command>
  </action>
</keybind>

<!-- DESPUÉS -->
<keybind key="C-A-t">
  <action name="Execute">
    <command>/usr/bin/ares</command>
  </action>
</keybind>
```

**Recarga aplicada:**
```bash
openbox --reconfigure
```

---

### 4. **Openbox - Menú Dinámico de Aplicaciones**

**Archivo:** `~/.config/openbox/clean-menu.py`

**Cambio:**
```python
# ANTES
terminal_string = "x-terminal-emulator -e"

# DESPUÉS
terminal_string = "/usr/bin/ares"
```

**Impacto:** Las aplicaciones que requieren terminal en el menú dinámico usan ARES.

---

### 5. **LXSession - Gestor de Sesiones**

**Archivo:** `~/.config/lxsession/LXDE/desktop.conf`

**Cambio:**
```ini
# ANTES
terminal_manager/command=lxterminal

# DESPUÉS
terminal_manager/command=/usr/bin/ares
```

---

### 6. **LXPanel - Barra de Tareas**

**Archivo:** `~/.config/lxpanel/launchtaskbar.cfg`

**Cambio:**
```ini
# ANTES
x-terminal-emulator=lxterminal

# DESPUÉS
x-terminal-emulator=/usr/bin/ares
```

---

### 7. **Tint2 - Launcher del Panel**

**Archivo:** `~/.config/tint2/vertical-neutral-icons.tint2rc`

**Cambio:**
```ini
# ANTES
launcher_item_app = x-terminal-emulator.desktop

# DESPUÉS
launcher_item_app = ares.desktop
```

---

### 8. **Archivo .desktop de ARES**

**Archivo creado:** `~/.local/share/applications/ares.desktop`

**Contenido:**
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=ARES Terminal
Comment=Terminal ARES - Orquestador Táctico TRON
Exec=/usr/bin/ares
Icon=utilities-terminal
Categories=System;TerminalEmulator;
StartupNotify=true
Actions=NewWindow;

[Desktop Action NewWindow]
Name=Nueva Ventana ARES
Exec=/usr/bin/ares
```

**Comando aplicado:**
```bash
update-desktop-database ~/.local/share/applications/
```

---

### 9. **GSettings - Terminal Predeterminada GNOME**

**Comando ejecutado:**
```bash
gsettings set org.gnome.desktop.default-applications.terminal exec '/usr/bin/ares'
```

**Verificación:**
```bash
gsettings get org.gnome.desktop.default-applications.terminal exec
# Resultado: '/usr/bin/ares'
```

---

## 📊 Matriz de Impacto

| Punto de Lanzamiento | Método | Terminal Actual |
|---------------------|--------|-----------------|
| **Menú Openbox (clic derecho)** | `menu.xml` | ✅ ARES |
| **Ctrl+Alt+T** | `rc.xml` | ✅ ARES |
| **Dolphin F4** | `x-terminal-emulator` | ✅ ARES |
| **Aplicaciones con terminal** | `clean-menu.py` | ✅ ARES |
| **LXSession** | `desktop.conf` | ✅ ARES |
| **LXPanel** | `launchtaskbar.cfg` | ✅ ARES |
| **Tint2 Launcher** | `.tint2rc` | ✅ ARES |
| **gsettings** | GNOME config | ✅ ARES |

---

## 🔧 Comandos de Verificación

```bash
# Verificar alternativa del sistema
update-alternatives --display x-terminal-emulator

# Verificar gsettings
gsettings get org.gnome.desktop.default-applications.terminal exec

# Verificar cuál es ares
which ares
# Resultado: /usr/bin/ares
```

---

## 🧩 Arquitectura de la Solución

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO                                  │
│         (Menús, Atajos, Launchers, Dolphin)                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              CAPA DE CONFIGURACIÓN                          │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │  menu.xml   │   rc.xml    │ clean-menu  │  dolphinrc  │ │
│  │  lxsession  │   lxpanel   │   tint2rc   │  gsettings  │ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           CAPA DE ALTERNATIVAS DEL SISTEMA                  │
│     /etc/alternatives/x-terminal-emulator → /usr/bin/ares   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ARES (/usr/bin/ares)                     │
│           Orquestador Táctico TRON - Kitty Backend          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Archivos Modificados

| Ruta | Tipo | Backup |
|------|------|--------|
| `~/.config/openbox/menu.xml` | XML | No |
| `~/.config/openbox/rc.xml` | XML | No |
| `~/.config/openbox/clean-menu.py` | Python | No |
| `~/.config/lxsession/LXDE/desktop.conf` | INI | No |
| `~/.config/lxpanel/launchtaskbar.cfg` | INI | No |
| `~/.config/tint2/vertical-neutral-icons.tint2rc` | INI | No |
| `/etc/alternatives/x-terminal-emulator` | Symlink | Automático |

**Archivos Creados:**
- `~/.local/share/applications/ares.desktop`

---

## 🚀 Flujo de Lanzamiento - Dolphin F4

```
Usuario presiona F4 en Dolphin
         │
         ▼
Dolphin consulta x-terminal-emulator
         │
         ▼
Sistema resuelve /etc/alternatives/x-terminal-emulator
         │
         ▼
Apunta a /usr/bin/ares
         │
         ▼
ARES lanza Kitty con configuración TRON
         │
         ▼
Terminal Hacker Neon lista para uso
```

---

## ⚠️ Notas Importantes

1. **Permisos sudo:** Se requirió `echo "a" | sudo -S` para comandos de alternativas.

2. **Prioridad en alternatives:** ARES tiene prioridad 45, superior a Konsole (40).

3. **No se modificaron archivos de sesión de Konsole:** Los archivos en `~/.config/session/konsole_*` son caché y se regeneran automáticamente.

4. **Recarga necesaria:** `openbox --reconfigure` aplica cambios inmediatamente.

---

## 🔐 Seguridad y Soberanía

- ✅ Todos los cambios son locales (`~/.config/`)
- ✅ No hay dependencias de nube
- ✅ El binario `/usr/bin/ares` es gestionado por `ini` (TRON)
- ✅ Configuración auditable y versionable

---

## 📖 Referencias

- [LEEME.md](../../LEEME.md) - Documentación principal de ARES
- [kitty.conf](../../config/kitty.conf) - Configuración de Kitty
- [Openbox RC](https://openbox.org/wiki/Help:Actions) - Acciones de Openbox

---

*Documento generado como parte de la configuración forense del sistema TRON.*

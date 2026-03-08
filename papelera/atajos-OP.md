# Atajos de Teclado de Openbox - Guía Completa

## 🖱️ Atajos que Controlan el Ratón (Mouse) - CRÍTICOS

### Movimiento del Cursor
| Atajo | Acción |
|-------|--------|
| `Win + Ctrl + ↑` | Mover cursor arriba 10px |
| `Win + Ctrl + ↓` | Mover cursor abajo 10px |
| `Win + Ctrl + ←` | Mover cursor izquierda 10px |
| `Win + Ctrl + →` | Mover cursor derecha 10px |
| `Ctrl + Win + Alt + ↑` | Mover cursor arriba 15px (más rápido) |
| `Ctrl + Win + Alt + ↓` | Mover cursor abajo 15px |
| `Ctrl + Win + Alt + ←` | Mover cursor izquierda 15px |
| `Ctrl + Win + Alt + →` | Mover cursor derecha 15px |

### Clics del Ratón
| Atajo | Acción |
|-------|--------|
| `Win + Ctrl + Enter` | Clic izquierdo (click 1) |
| `Win + Ctrl + Shift + Enter` | Clic derecho (click 3, con retardo 0.5s) |

### Script de Ratón (raton.sh)
| Atajo | Acción |
|-------|--------|
| `Ctrl + Win + Break` | Ejecutar raton.sh - **Alternar clic izquierdo** (mousedown/mouseup) |

#### Detalle de `raton.sh` (`/home/daniel/tron/programas/Admon/QT5-Openbox/raton.sh`):
```bash
#!/bin/bash
STATE_FILE="/tmp/mouse_link_state"
if [ ! -f $STATE_FILE ]; then 
    xdotool mousedown 1   # Presionar botón izquierdo
    touch $STATE_FILE
else 
    xdotool mouseup 1     # Soltar botón izquierdo
    rm $STATE_FILE
fi
```
**Función:** Mantener presionado el botón izquierdo hasta pulsar nuevamente el atajo. Útil para arrastrar elementos.

---

## 🚀 Lanzamiento de Aplicaciones

| Atajo | Aplicación |
|-------|------------|
| `Ctrl + Alt + T` | ARES (`/usr/bin/ares`) |
| `Ctrl + Alt + K` | Kate (editor de texto) |
| `Ctrl + Alt + E` | Dolphin (gestor de archivos) |
| `Ctrl + Alt + I` | Google Chrome |
| `Ctrl + Alt + A` | Antigravity |
| `Ctrl + Alt + C` | Visual Studio Code |
| `Ctrl + Alt + M` | Mousepad (editor de texto) |
| `Ctrl + Alt + N` | Kate - abrir notas.md |
| `Ctrl + Alt + V` | Pavucontrol (control de audio) |
| `Ctrl + Alt + R` | Network Manager (`nm-connection-editor`) |
| `Win + E` | Dolphin |

---

## 🖥️ Navegación entre Escritorios

### Con Teclas de Dirección
| Atajo | Acción |
|-------|--------|
| `Ctrl + Alt + ←` | Ir al escritorio izquierdo |
| `Ctrl + Alt + →` | Ir al escritorio derecho |
| `Ctrl + Alt + ↑` | Ir al escritorio superior |
| `Ctrl + Alt + ↓` | Ir al escritorio inferior |

### Con Teclas de Función
| Atajo | Acción |
|-------|--------|
| `Win + F1` | Ir al escritorio 1 |
| `Win + F2` | Ir al escritorio 2 |
| `Win + F3` | Ir al escritorio 3 |
| `Win + F4` | Ir al escritorio 4 |

### Mostrar Escritorio
| Atajo | Acción |
|-------|--------|
| `Win + D` | Mostrar/ocultar escritorio (ToggleShowDesktop) |

### Mover Ventanas entre Escritorios
| Atajo | Acción |
|-------|--------|
| `Shift + Alt + ←` | Enviar ventana al escritorio izquierdo |
| `Shift + Alt + →` | Enviar ventana al escritorio derecho |
| `Shift + Alt + ↑` | Enviar ventana al escritorio superior |
| `Shift + Alt + ↓` | Enviar ventana al escritorio inferior |

---

## 🪟 Gestión de Ventanas

### Cerrar y Minimizar
| Atajo | Acción |
|-------|--------|
| `Alt + F4` | Cerrar ventana |
| `Alt + Escape` | Bajar ventana, quitar foco |
| `Win + ↓` | Iconificar ventana (minimizar) |

### Cambiar entre Ventanas
| Atajo | Acción |
|-------|--------|
| `Alt + Tab` | Siguiente ventana |
| `Alt + Shift + Tab` | Ventana anterior |
| `Ctrl + Alt + Tab` | Siguiente ventana (incluye paneles y escritorios) |

### Navegación Direccional de Ventanas
| Atajo | Acción |
|-------|--------|
| `Win + Shift + →` | Ciclar ventana a la derecha |
| `Win + Shift + ←` | Ciclar ventana a la izquierda |
| `Win + Shift + ↑` | Ciclar ventana arriba |
| `Win + Shift + ↓` | Ciclar ventana abajo |

### Menú de Ventana
| Atajo | Acción |
|-------|--------|
| `Alt + Espacio` | Mostrar menú del cliente |

### Ajuste de Ventanas (Snapping con bl-aerosnap)
| Atajo | Acción |
|-------|--------|
| `Win + ←` | Ajustar ventana a la izquierda |
| `Win + →` | Ajustar ventana a la derecha |
| `Win + ↑` | Maximizar ventana |

---

## 📸 Capturas de Pantalla

| Atajo | Acción |
|-------|--------|
| `Print` | Flameshot GUI |
| `Shift + Print` | Scrot - área seleccionada → `~/Capturas/` |
| `Alt + Print` | Scrot - ventana actual (`scrot -s`) |

---

## 🔧 Sistema y Configuración

| Atajo | Acción |
|-------|--------|
| `Ctrl + Alt + Delete` | Reiniciar sistema (`reboot`) |
| `Ctrl + Alt + Backspace` | Apagar sistema (`systemctl poweroff`) |

---

## 📋 Menús

| Atajo | Acción |
|-------|--------|
| `Tecla Menú` | Mostrar menú raíz de Openbox |

---

## 🖱️ Atajos de Ratón (Mouse Bindings)

### En el Marco de la Ventana (Frame)
| Acción | Efecto |
|--------|--------|
| `Alt + Clic Izq` (Press) | Enfocar y elevar ventana |
| `Alt + Clic Izq` (Click) | Desenrollar ventana |
| `Alt + Clic Izq` (Drag) | Mover ventana |
| `Alt + Clic Der` (Press) | Enfocar, elevar y desenrollar |
| `Alt + Clic Der` (Drag) | Redimensionar ventana |
| `Alt + Clic Central` (Press) | Bajar ventana, quitar foco |
| `Alt + Rueda Arriba` | Ir al escritorio anterior |
| `Alt + Rueda Abajo` | Ir al siguiente escritorio |
| `Ctrl + Alt + Rueda Arriba` | Ir al escritorio anterior |
| `Ctrl + Alt + Rueda Abajo` | Ir al siguiente escritorio |
| `Shift + Alt + Rueda Arriba` | Enviar ventana al escritorio anterior |
| `Shift + Alt + Rueda Abajo` | Enviar ventana al siguiente escritorio |

### En la Barra de Título (Titlebar)
| Acción | Efecto |
|--------|--------|
| `Clic Izq` (Drag) | Mover ventana |
| `Clic Izq` (Doble Click) | Maximizar/restaurar ventana |
| `Rueda Arriba` | Enrollar ventana (shade) |
| `Rueda Abajo` | Desenrollar ventana (unshade) |

### En las Esquinas y Bordes
| Acción | Efecto |
|--------|--------|
| `Clic Izq` (Press) | Enfocar, elevar, desenrollar |
| `Clic Central` (Press) | Bajar ventana, quitar foco |
| `Clic Der` (Press) | Enfocar, elevar, mostrar menú cliente |
| `Clic Izq` (Drag) en bordes | Redimensionar desde ese borde |

### En el Escritorio (Desktop/Root)
| Acción | Efecto |
|--------|--------|
| `Rueda Arriba` | Ir al escritorio anterior |
| `Rueda Abajo` | Ir al siguiente escritorio |
| `Alt + Rueda Arriba` | Ir al escritorio anterior |
| `Alt + Rueda Abajo` | Ir al siguiente escritorio |
| `Clic Central` | Mostrar menú de lista de ventanas |
| `Clic Der` | Mostrar menú raíz |

---

**Nota:** `Win` = Tecla Super/Windows, `Ctrl` = Control, `Alt` = Alt, `Shift` = Mayús

**Fuente:** `~/.config/openbox/rc.xml`

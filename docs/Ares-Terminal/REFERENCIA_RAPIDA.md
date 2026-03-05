# ⚡ Referencia Rápida - ARES Terminal Predeterminada

## Comandos de Verificación

```bash
# ¿Qué terminal usa el sistema?
update-alternatives --display x-terminal-emulator | head -5

# ¿Dónde apunta x-terminal-emulator?
ls -la /etc/alternatives/x-terminal-emulator

# ¿Existe ares?
which ares

# ¿gsettings está configurado?
gsettings get org.gnome.desktop.default-applications.terminal exec
```

---

## Atajos de Teclado Activos

| Atajo | Acción |
|-------|--------|
| `Ctrl + Alt + T` | Abre ARES |
| `Win + E` | Abre Dolphin |
| `F4` (en Dolphin) | Abre ARES en ruta actual |

---

## Menú Contextual Openbox

**Clic derecho en escritorio → Terminal ARES** → Lanza ARES

---

## Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `~/.config/openbox/rc.xml` | Atajos de teclado |
| `~/.config/openbox/menu.xml` | Menú contextual |
| `~/.config/lxsession/LXDE/desktop.conf` | Terminal de sesión |
| `/etc/alternatives/x-terminal-emulator` | Alternativa del sistema |

---

## Restaurar Konsole (si es necesario)

```bash
echo "a" | sudo -S update-alternatives --set x-terminal-emulator /usr/bin/konsole
```

---

## Estructura de Documentación

```
/home/daniel/tron/programas/TR/docs/Ares-Terminal/
├── CONFIGURACION_TERMINAL_PREDETERMINADA.md  (este documento completo)
└── REFERENCIA_RAPIDA.md                       (archivo actual)
```

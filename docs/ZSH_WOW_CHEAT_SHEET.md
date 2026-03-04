# ⚡ ARES ZSH WOW - HOJA DE TRUCOS (Hacker Edition)

Bienvenido al entorno de shell definitivo. Esta guía resume todas las capacidades tácticas que hemos integrado en tu Zsh.

---

## 🎨 INTERFAZ VISUAL (Powerlevel10k)

### 1. El Prompt Inteligente
- **Izquierda**:  (OS) → Directorio (Truncado) → Rama Git (Estado) → Nueva línea para input.
- **Derecha**: Código Error (✘) | Tiempo Ejecución (⏱️) | Procesos BG (⚙️) | Python Venv (🐍) | Hora (AM/PM).

### 2. Directorio Camaleón
- Si la ruta es larga, se encoge: `~/t/p/T/m/ia` en lugar de `~/tron/programas/TR/modules/ia`.
- Las carpetas importantes ("anclas") siempre permanecen legibles.

---

## 🛠️ PLUGINS Y PRODUCTIVIDAD

### 🚀 Autocompletado y Sugerencias
- **Zsh-Autosuggestions**: Mientras escribes, verás una sugerencia en gris basada en tu historial.
- **Acción**: Presiona `Flecha Derecha` o `End` para aceptar la sugerencia completa.
- **Zsh-Syntax-Highlighting**: Los comandos válidos se ven en **Verde**, los inexistentes en **Rojo**.

### 🔍 Búsqueda Difusa (FZF)
- **CTRL+R**: Busca en tu historial de comandos con interfaz visual neón.
- **CTRL+T**: Busca archivos en el directorio actual para insertarlos en el comando.
- **ALT+C**: Navega a subdirectorios rápidamente usando búsqueda difusa.

### ⚡ Atajos de Teclado
- **CTRL+U**: Borra toda la línea actual.
- **CTRL+A / CTRL+E**: Salta al inicio / fin de la línea.
- **ALT+B / ALT+F**: Salta una palabra atrás / adelante.
- **Flecha Arriba / Abajo**: Busca en el historial solo comandos que empiecen como lo que ya escribiste.

---

## 🛰️ COMANDOS TÁCTICOS ARES

| Comando | Descripción |
|---------|-------------|
| `ares` | Abre ARES Hub (Nueva ventana Kitty con título fijo). |
| `ares -p "..."` | Consulta rápida a la IA Ares (Gemma 3). |
| `ares status` | Diagnóstico de socket Kitty y salud del sistema. |
| `ares plan` | Despliegue original (4 pestañas Neon). |
| `ares zshplan` | **WOW**: Lanza sesión IA (TRAIN, DATA, MODELS, LOGS) en Zsh Puro. |
| `ares init -r` | Recarga la configuración de Kitty en caliente. |

---

## 🐚 OPCIONES DE "MAGIA" ZSH
- **AUTO_CD**: Escribe solo el nombre de una carpeta y presiona `Enter` para entrar. No necesitas escribir `cd`.
- **CORRECT**: Si escribes mal un comando (ej: `sl`), Zsh te preguntará: *¿Quisiste decir ls?*
- **SUDO**: Presiona `ESC` dos veces (o `CTRL+S`) para añadir `sudo` al comando que acabas de escribir.

---
*ARES: Sencillez Eficaz. Máxima Potencia.*

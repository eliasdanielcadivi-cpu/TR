# 🛰 TR - Terminal Remote Operations Nexus (TRON)

**Tron** es un orquestador táctico diseñado para transformar la terminal Kitty en una estación de trabajo de alta productividad aumentada por IA. Actúa como el cerebro para el control de ventanas, sesiones inteligentes y flujos de trabajo de programación de alto rendimiento.

## 🚀 ACCESO RÁPIDO (LAUNCHER)
El proyecto está encapsulado y disponible globalmente mediante el comando `tr`.
- **Producción:** `/usr/bin/tr` (Lanzador gestionado por `ini`).
- **Ayuda Inteligente:** Ejecuta `tr` solo para abrir el navegador de ayuda **Broot**.

## 🧠 COMANDOS MAESTROS
- `tr p "pregunta"`: Consulta a la IA Tron (Gemma 3 / DeepSeek).
- `tr plan`: Despliegue táctico de pestañas, diagnósticos y multimedia.
- `tr model <alias>`: Cambia el cerebro de IA (gemma, deepseek).
- `tr status`: Diagnóstico del socket Kitty y estado del sistema.
- `tr view <ruta>`: Visualización multimedia HQ (icat/mpv).
- `tr color <ruta>`: Aplica color Hacker Neon a pestaña según archivo (módulo color).

## 🏗 ARQUITECTURA MODULAR (Anti-Entropía)
Siguiendo la regla de **máximo 3 funcionalidades por módulo** para facilitar el *vibe coding*:

- `src/main.py`: Punto de entrada CLI y despachador de comandos.
- `src/config.py`: Gestión de contexto, rutas y persistencia YAML.
- `src/kitty.py`: Socket Remote Control, diagnóstico y lanzamiento.
- `src/engine.py`: Motores de IA (Ollama/DeepSeek) y plantillas de prompt.
- `src/plan.py`: Orquestador de flujos de trabajo y verificación de Handshake.
- `modules/color/`: Módulo de coloreado de pestañas con set-tab-color (Hacker Neon).
- `bin/tr-video`: Herramienta independiente de video HQ para Kitty.
- `bin/tr-color`: CLI independiente para coloreado de pestañas.

## 📂 ORGANIZACIÓN DEL DIRECTORIO
```bash
TR/
├── bin/          # Herramientas auxiliares (tr-video, tr-color)
├── config/       # Configuración (kitty.conf, config.yaml, zsh/)
├── data/         # Persistencia de sesiones y handshakes
├── docs/         # DOCUMENTACIÓN NAVEGABLE (Broot help)
├── modules/      # Módulos independientes (color/)
├── src/          # Código fuente modularizado
├── tests/        # Pruebas automatizadas
└── venv/         # Entorno virtual Python (Visible/UV)
```

## 📄 DOCUMENTACIÓN TÉCNICA (docs/)
Accede a estos documentos mediante `tr help` o `broot docs/`:
1.  **INDEX.md**: Mapa de componentes del proyecto.
2.  **MANUAL.md**: Guía de usuario y comandos extendidos.
3.  **Shortcuts.md**: Tabla de compatibilidad de atajos (Kitty + Zsh).
4.  **Requerimientos.md**: Bitácora de 150+ tareas de desarrollo.
5.  **ZSH/Trucos.md**: Optimización del shell y plugins.
6.  **modulo-colores-y-diseno.md**: Documentación del módulo de color (set-tab-color, Hacker Neon).
7.  **COLOR_MODULE.md**: Documentación técnica del módulo tr-color.

## ⌨️ ATAJOS CLAVE (WOW FACTOR)
- `Ctrl+Shift+T`: Nueva Pestaña.
- `Ctrl+Shift+W`: Cerrar Pestaña.
- `Ctrl+Shift+PgUp/PgDn`: Navegar pestañas.
- `Ctrl+Shift+C/V`: Copiar y Pegar.
- **Mouse:** Soporte completo de ratón habilitado en Kitty.

---
*Tron: Smart Always. Boba Nunca.*

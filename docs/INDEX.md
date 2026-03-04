# 🛰️ ARES - ÍNDICE DE MÓDULOS Y COMPONENTES (v2.0)

**⚠️ REGLA DE ORO:** Consultar este índice ANTES de crear cualquier módulo nuevo.  
**📋 MÁXIMO 3 FUNCIONES** por módulo (filosofía ARES de modularidad atómica).

---

## 🏛️ NÚCLEO (root / config)

### main.py - Despachador Puro
**Propósito:** Punto de entrada único. No contiene lógica de negocio, solo orquestación de comandos.
**Relaciones:** Importa dinámicamente de `modules/`.

### config/ - Gestión de Entorno
- `config.yaml`: Única fuente de verdad para identidad (Ares), rutas y sockets.
- `kitty_remote.py`: Motor de bajo nivel para control de la terminal. (Funciones: `is_running`, `launch_hub`, `run`).

---

## 🧩 JERARQUÍA DE MÓDULOS (modules/)

### admon/ - Gestión de Sistema
**Propósito:** Mantenimiento y diagnóstico de la salud de ARES.
- `diag_manager.py`: Diagnóstico visual de sockets y pestañas.
- `init_manager.py`: Gestión de enlaces simbólicos y recarga de configuración.

### ia/ - Cerebro Agéntico
**Propósito:** Conectividad con modelos de lenguaje y lógica de prompts.
- `ai_engine.py`: Conector para Ollama y DeepSeek.
- `investigador/`: Módulo especializado en exploración web e inteligencia.

### ui/ - Interfaz y Estética
**Propósito:** Control visual y documentación interactiva.
- `help_manager.py`: Visualización de manuales neón y orquestación de IA en terminal.
- `color/`: Motor de identidad visual dinámica para pestañas.

### multimedia/ - Puppeteering de Medios
**Propósito:** Integración de video, imagen y audio en la terminal.
- `media_manager.py`: Control de `mpv` (IPC) y `icat` para renderizado de alta fidelidad.

### tactico/ - Orquestación de Flujos
**Propósito:** Despliegue de entornos de trabajo predefinidos.
- `plan_manager.py`: Ejecución de `arn plan` y verificación de handshake.
- `zsh_plan_manager.py`: Ejecución de `ares zshPlan` para sesiones de IA en Zsh.

### whatsapp/ - Comunicaciones Externas
**Propósito:** Puente entre ARES y la red de mensajería para distribución de datos.

---

## 🔧 BINARIOS GLOBALES (bin/)
- `ares`: Lanzador maestro (Abre ARES Hub).
- `arn`: Comando táctico corto (Despacho rápido).
- `tr-investigador`: Herramienta de inteligencia independiente.

---
*Filosofía ARES: Orden Paranoico. Modularidad Atómica. Excelencia Técnica.*

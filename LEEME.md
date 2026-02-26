# TR - Terminal Remote Operations Nexus (INTELIGENTE)

**TR** es un orquestador inteligente diseñado para transformar la terminal Kitty en una estación de trabajo de alta productividad aumentada por IA (Ollama/DeepSeek). Actúa como el cerebro táctico para el control de ventanas, sesiones, multimedia y flujos de trabajo de programación.

## 1. INFRAESTRUCTURA (Higiene Organizacional)

*   `src/`: Lógica de ejecución (Python 3.12+).
*   `config/`: Archivos YAML de configuración (LLMs, Kitty, Openbox).
*   `docs/`: Documentación técnica y bitácoras de requerimientos.
*   `data/`: Almacenamiento de sesiones (JSON).
*   `logs/`: Registro de operaciones (`logs/session.jsonl`).
*   `db/`: Persistencia (SQLite para historial y búsqueda vectorial ligera).
*   `bin/`: Binarios y scripts auxiliares.
*   `venv/`: Entorno virtual gestionado por **UV** (SIN PUNTO).

## 2. PILARES TECNOLÓGICOS

1.  **Terminal:** [Kitty](https://sw.kovidgoyal.net/kitty/) con Remote Control (RC) vía Unix Socket.
2.  **Entorno:** [Openbox](http://openbox.org/) para posicionamiento de ventanas.
3.  **IA:** 
    *   **Ollama:** Modelos locales (Gemma 3, Qwen 2.5, Llama 3.2).
    *   **DeepSeek:** API de alto rendimiento con Context Caching.
4.  **Utilidades:** `gum`, `fzf`, `icat`, `mpv`.

## 3. LANZADOR GLOBAL

El proyecto utiliza el comando `ini` para desplegar un wrapper en `/usr/bin/tr` que apunta a este entorno encapsulado.

```bash
# Para actualizar o crear el lanzador:
cd ~/tron/programas/TR
ini
```

## 4. DOCUMENTACIÓN CLAVE

*   [Requerimientos Extensivos](docs/Requerimientos.md)
*   [API DeepSeek](docs/Apideepseek.md)
*   [Manual Kitty RC](docs/Controlar%20a%20Kitty%20desde%20scripts%20(1).md)

---
*Ultima actualización: Jueves, 26 de Febrero de 2026*

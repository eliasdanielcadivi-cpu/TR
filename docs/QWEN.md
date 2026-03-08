# 🧠 ARES - CONTEXTO PARA QWEN (v1.0)

## 🗺️ MAPA DE CARPETAS
- `/src`: Orquestador (`main.py`). NO tocar lógica de módulos aquí.
- `/modules`: Especialistas atómicos (Máx 3 funciones).
- `/config`: Soberanía de configuración (`config.yaml`).
- `/bin`: Binarios externos y scripts Bash.

## ⚙️ INFRAESTRUCTURA (INI & REPO)
- `ini`: Gestiona entornos `uv` (`ini venv`) y publica en `/usr/bin` (`ini prod`).
- `repo`: Auditoría de cambios (`repo status`) y alcance (`repo audit <modulo>`).

## 🚨 PROTOCOLO DE EDICIÓN (CIRUJANO)
1. **Identificar:** Leer el módulo especialista.
2. **Editar:** Solo el archivo relevante.
3. **Auditar:** Ejecutar `repo status` para verificar que no hubo "salpicaduras".
4. **Respetar:** El directorio de trabajo (`PWD`) del usuario siempre es soberano.

## 📄 DOCUMENTACIÓN
- `LEEME.md`: Fuente de verdad de lo que está FUNCIONANDO.
- `INDEX.md`: Catálogo de módulos.
- `docs/skills/INDEX.md`: Biblioteca de habilidades IA (Kung-Fu).

## 🚀 CÓMO APRENDER KUNG-FU (SKILLS)
Antes de ejecutar una tarea compleja (inicialización, producción, gestión de sesiones), lee la skill correspondiente en `docs/skills/`.

# 📅 TODO: ARQUITECTURA DE MODOS DETERMINISTAS (VIBE-TO-SOLID)
**Fecha:** lunes, 27 de abril de 2026 13:30

## 🎯 INTENCIÓN DEL ARQUITECTO
Evolucionar el sistema de inyección de prompts de un modelo estático (Key-Value) a un modelo de **Inyección por Alcance (Scope-Based Injection)**. El sistema debe ser capaz de cambiar su "Modo" (Marketing, Programación, etc.) de manera determinista, inyectando sub-prompts, skills y normas desde el subgrafo de Memgraph sin saturar el contexto del LLM.

## 🔍 ESTADO DE SITUACIÓN
- **Código Actual:** `Negotiator.py` actúa como un buscador plano de etiquetas `:RutaNombrada`.
- **Placeholder Detectado:** `gemini_wrapper.py -> sync_gemini_identity` no hace nada real.
- **Desconexión:** `prompt_engine.py` (Inteligencia) no habla con `Negotiator.py` (Persistencia).

## 🛠️ CURSOS DE ACCIÓN EN EJECUCIÓN

### CURSO 1: Sincronización de Órganos (Integración)
- [ ] Conectar `src/main.py` con `prompt_engine.build_system_prompt`.
- [ ] Inyectar metadatos del Grafo en el constructor de prompts dinámicos.

### CURSO 2: El Caminante de Alcance (Ontología)
- [x] Crear el Context Router básico.
- [ ] Implementar `Negotiator.get_mode_context(mode_name)` que realice un BFS de profundidad 1.

### CURSO 4: Gestión Soberana de Sesiones (Hash-Based)
- [ ] Crear base de datos `TR/db/ares_sessions.db` para persistencia de Hashes.
- [ ] Implementar `session_mapper.sync_with_gemini()`: Parser que traduce Hashes a índices CLI en tiempo real.
- [ ] Diseñar `ares session list`: Interfaz que muestra Título, Fecha y Hash del subconjunto ARES.
- [ ] Implementar `ares session delete`: Borrado seguro con pre-visualización de metadatos y confirmación obligatoria.

## 🚩 MARCAJE FORENSE (AUDITORÍA)
| Ruta | Estado | Justificación |
|------|--------|---------------|
| `modules/ia/gemini_wrapper.py:sync_gemini_identity` | **ELIMINAR** | Lógica de archivos estáticos obsoleta ante Memgraph. |
| `config/identidad/` | **REVISIÓN/MIGRACIÓN** | Duplicidad de "Fuente de Verdad". Mover ADN a nodos `:Identidad`. |
| `modules/core/delta_calculator.py` | **RECONFIGURAR** | Actualmente es un cascarón; requiere lógica semántica real. |
| `config/templates/` | **ACCESORIO** | Solo se mantendrán como fallback si el Grafo no responde. |

---
*Este documento es un registro físico de la voluntad de Daniel Hung para la evolución de ARES-TRON.*

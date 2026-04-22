# 🛰️ ARES - ÍNDICE DE MÓDULOS Y COMPONENTES

> **Verificado con estructura real:** `/home/daniel/tron/programas/TR/modules/`
> **Última actualización:** 2026-04-18 (Post-Ingeniería Memgraph)
> **Filosofía:** Máximo 3 funciones por módulo (modularidad atómica)

---

## 🏛️ NÚCLEO

### `src/main.py` - Despachador Puro
**Propósito:** Punto de entrada único. Orquestación de comandos.

**Nuevos Comandos ARES-TRON:**
- `ares p --mengraph`: Consulta RAG con Grafo en RAM.
- `ares i --mengraph`: Modo interactivo con respaldo de grafos.
- `ares gemini --mengraph`: Inicia Gemini con la ruta CARGA_SISTEMA (Identidad Soberana).
- `ares gemini --ruta <nombre>`: Invoca una Ruta Nombrada (Wisdom) específica.
- `ares mem [start|stop|status]`: Orquestación de contenedores Docker.

---

## 🧩 MÓDULOS (`modules/`)

### `core/` - Motor Transversal y Recursos
| Sub-módulo | Propósito |
|------------|-----------|
| `limit_manager.py` | Gestión de hardware adaptativo (Límites 8GB RAM). |
| `session_manager.py` | Persistencia de sesiones Kitty. |

### `ia/` - Inteligencia y Negociación
| Sub-módulo | Propósito |
|------------|-----------|
| `negotiator.py` | Intercepción de rechazos y navegación de Rutas Nombradas. |
| `gemini_wrapper.py` | Integración determinista con gemini-cli. |
| `ai_engine.py` | Orquestador multi-provider (Ollama, DeepSeek, Cloud). |

### `rag_mengraph/` - Sistema Cognitivo de Grafos (Memgraph)
**Estado:** ✅ ACTIVO (Nuevo Estándar ARES)
**Propósito:** Motor RAG de alta fidelidad con extracción determinista y tejido lógico.

| Sub-módulo | Propósito |
|------------|-----------|
| `core/orchestrator.py` | Orquestador del ciclo STORM (Ingesta completa). |
| `core/retriever.py` | Motor de búsqueda híbrida (Vectorial + Grafo). |
| `validators/relation_guard.py` | Seguridad C1-C4 y filtrado de criticidad. |
| `validators/quarantine_manager.py`| Almacén HJSON para aprobación humana de Serendipia. |
| `storage/ingestor.py` | Inyector inmutable con Hashes de Evidencia SHA-256. |

---

### `investigador/` - Exploración Web
...

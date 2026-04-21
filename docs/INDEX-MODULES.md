# 🛰️ ARES - ÍNDICE DE MÓDULOS Y COMPONENTES

> **Verificado con estructura real:** `/home/daniel/tron/programas/TR/modules/`
> **Última actualización:** 2026-04-18 (Post-Ingeniería Memgraph)
> **Filosofía:** Máximo 3 funciones por módulo (modularidad atómica)

---

## 🏛️ NÚCLEO

### `src/main.py` - Despachador Puro
**Propósito:** Punto de entrada único. Orquestación de comandos.

**Nuevos Comandos Memgraph:**
- `ares p --mengraph`: Consulta RAG con Grafo en RAM.
- `ares i --mengraph`: Modo interactivo con respaldo de grafos.
- `ares mem [start|stop|status]`: Orquestación de contenedores Docker.

---

## 🧩 MÓDULOS (`modules/`)

... (módulos anteriores omitidos para brevedad) ...

### `rag_mengraph/` - Sistema Cognitivo de Grafos (Memgraph)
**Estado:** ✅ ACTIVO (Nuevo Estándar ARES)
**Propósito:** Motor RAG de alta fidelidad con extracción determinista y tejido lógico.

| Sub-módulo | Propósito |
|------------|-----------|
| `core/orchestrator.py` | Orquestador del ciclo STORM (Ingesta completa). |
| `core/retriever.py` | Motor de búsqueda híbrida (Vectorial + Grafo). |
| `core/schema_weaver.py` | Micro-RAG de esquema para guiar al LLM. |
| `core/serendipia_engine.py` | Inferencia de Verbos y descubrimiento de relaciones. |
| `ingestion/spacy_engine.py` | Pipeline NLP Anti-Bloat con EntityRuler. |
| `storage/memgraph_db.py` | Driver Bolt y gestión ontológica. |
| `storage/ingestor.py` | Inyector inmutable con Hashes de Evidencia. |
| `validators/relation_guard.py` | Seguridad C1-C4 y filtrado de criticidad. |
| `validators/quarantine_manager.py`| Almacén HJSON para aprobación humana. |

---

### `investigador/` - Exploración Web
...

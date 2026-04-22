# 🛰️ ARES - ÍNDICE DEFINITIVO DE MÓDULOS Y COMPONENTES

> **Única Fuente de Verdad:** Verificado con estructura real en `/home/daniel/tron/programas/TR/modules/`
> **Última actualización:** 2026-04-22 (Fase Soberanía Cognitiva)
> **Filosofía:** Máximo 3 funciones principales por módulo (Atomicidad Paranoica).

---

## 🏛️ NÚCLEO (`src/`)

### `main.py` - Orquestador y Despachador
Punto de entrada único del sistema. Gestiona la CLI y delega la ejecución a los módulos correspondientes.
**Comandos Destacados:**
- `ares p`: Consulta IA multi-provider.
- `ares gemini`: Wrapper determinista con soporte para Grafos.
- `ares mem`: Gestión de infraestructura Memgraph (Docker).
- `ares gs`: Gestión de sesiones Kitty.

---

## 🧩 MÓDULOS (`modules/`)

### `admon/` - Administración del Sistema
| Módulo | Propósito |
|--------|-----------|
| `boot_manager.py` | Lanzamiento inicial del ARES Hub. |
| `diag_manager.py` | Diagnóstico integral de sockets y conectividad. |
| `init_manager.py` | Gestión de infraestructura y enlaces simbólicos. |
| `memgraph_manager.py` | Control de contenedores Docker Memgraph. |
| `session_manager.py` | Captura y restauración de estados de Kitty. |

### `core/` - Motor Transversal y Recursos
| Módulo | Propósito |
|--------|-----------|
| `limit_manager.py` | Gestión de hardware adaptativo (8GB RAM / GPU). |
| `socket_manager.py` | Control de sockets UNIX para Kitty. |
| `window_registry.py` | Registro y limpieza de ventanas activas. |
| `prompt_engine.py` | Motor de plantillas y construcción de contextos. |

### `ia/` - Inteligencia y Negociación
| Módulo | Propósito |
|--------|-----------|
| `ai_engine.py` | Dispatcher multi-provider (Ollama, DeepSeek, Cloud). |
| `negotiator.py` | Intercepción de rechazos y navegación de Rutas Nombradas. |
| `gemini_wrapper.py` | Integración determinista con gemini-cli. |
| `apollo/` | Sub-sistema RAG documental (Kùzu + SQLite-vec). |
| `providers/` | Adaptadores para diferentes motores de inferencia. |

### `rag_mengraph/` - Sistema Cognitivo de Grafos (Memgraph)
| Sub-módulo | Propósito |
|------------|-----------|
| `core/orchestrator.py` | Orquestador del ciclo STORM (Ingesta completa). |
| `core/retriever.py` | Motor de búsqueda híbrida (Vectorial + Grafo). |
| `core/tool.py` | Interfaz Universal JSON para agentes externos. |
| `validators/relation_guard.py` | Seguridad C1-C4 y filtrado de criticidad. |
| `validators/quarantine_manager.py`| Almacén HJSON para aprobación humana. |
| `storage/ingestor.py` | Inyector inmutable con Hashes de Evidencia SHA-256. |

### `multimedia/` - Puppeteering Terminal
| Módulo | Propósito |
|--------|-----------|
| `media_manager.py` | Orquestador de video (MPV) e imagen (ICAT). |
| `asset_optimizer.py` | Optimización de recursos visuales para terminal. |

### `ui/` - Interfaz y Estética
| Módulo | Propósito |
|--------|-----------|
| `industrial_engine.py` | Renderizado de cintillos y avatares industriales. |
| `chat_production.py` | Loop REPL interactivo con estética Neón. |
| `agente_de_cambio.py` | Interfaz TUI híbrida (Textual/Ratatui). |
| `help_manager.py` | Gestor del sistema de ayuda soberana. |

### `aviso/` - Recordatorios Naturales
| Módulo | Propósito |
|--------|-----------|
| `aviso_engine.py` | Procesamiento de recordatorios en lenguaje natural. |
| `aviso_daemon.py` | Servicio en segundo plano para notificaciones. |

---

## 🛠️ SCRIPTS ESTRATÉGICOS (`scripts/`)
- `seed_named_routes.py`: Inicialización de Rutas Nombradas (Carga del Sistema) en Memgraph.
- `ares_sync_identity.py`: Sincronización de identidad Maestra en todos los modelos.

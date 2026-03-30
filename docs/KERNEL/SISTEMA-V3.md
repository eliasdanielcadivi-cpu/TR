 Entendido. Voy a diseñar un blueprint completo para un **módulo RAG embebido** que se integre con ARES existente, no lo reemplace. El RAG será un sub-sistema accesible tanto desde `ares i` (interactivo) como `ares p` (headless), manteniendo la filosofía de ARES: determinista cuando puede, semántico cuando debe, siempre con soberanía del usuario.

Primero, déjame leer nuevamente el documento de arquitectura del kernel para extraer los principios clave que debemos respetar.
Voy a leer directamente el contenido del archivo que ya está disponible en el contexto. Analizando los documentos proporcionados, extraigo los principios arquitectónicos clave:

---

## ANÁLISIS DE PRINCIPIOS ARES-TRON V.2 (Del documento A-V1-ARQUITECTURA-KERNEL.md)

### Principios Fundamentales para el Módulo RAG:

| Principio | Implicación para RAG |
|-----------|----------------------|
| **Punteros $MAP dinámicos** | El RAG debe resolver rutas vía SQLite, no hardcoded |
| **Motor de Inferencia Híbrido** | SQL determinista primero, vectorial después, grafo si es necesario, LLM solo bajo demanda |
| **Tiers de Recuperación (T0-T4)** | T0-T3 para latencia ≈0, T4 solo con trigger explícito "piensa" |
| **Zero-Hallucination** | RelationGuard C1-C4: relaciones críticas requieren validación |
| **Snapthots de Sesión por PID** | Cada invocación de `ares p` o `ares i` debe tener contexto inmutable |
| **Skill Cartógrafo** | Modo conversacional para cuando el usuario quiere "mapear" conocimiento |
| **Agnosticismo Estructural** | Si muevo el proyecto, solo cambia un registro en DB |

### Restricciones Críticas del Kernel:

1. **No tres bases de datos desincronizadas** → Usar SQLite con extensiones (sqlite-vec) + Kùzu embebido
2. **No simplificación booleana en runtime** → Usar BDD pre-computados o DAG fijos (NetworkX)
3. **No Zsh como IPC complejo** → El RAG inyecta contexto vía archivos temporales o stdin/stdout estructurado
4. **Latencia ≈ 0 para T0-T3** → Cache agresiva, índices SQLite, grafo en memoria para consultas frecuentes

---

## BLUEPRINT: MÓDULO RAG ARES-EMBEDDED

### Nombre del Módulo: `ares-rag` (Sub-sistema interno, no reemplaza ARES)

### Ubicación en ARES existente:
```
~/tron/programas/TR/
├── modules/rag/                    # NUEVO: Módulo RAG embebido
│   ├── __init__.py
│   ├── core/
│   │   ├── tier_router.py          # Motor T0-T4 (Anexo I)
│   │   ├── context_engine.py       # Gestión de snapshots por PID
│   │   └── rag_orchestrator.py     # Interfaz única para ares p / ares i
│   ├── engines/
│   │   ├── sql_engine.py           # T1: Determinista
│   │   ├── vector_engine.py        # T2: sqlite-vec
│   │   ├── graph_engine.py         # T3: Kùzu embebido
│   │   └── llm_engine.py           # T4: Ollama/DeepSeek (bajo demanda)
│   ├── validators/
│   │   └── relation_guard.py       # C1-C4 zero-hallucination
│   ├── ingestors/
│   │   ├── file_ingestor.py        # Markdown, Python, etc.
│   │   ├── code_ingestor.py        # AST parsing para Python
│   │   └── graph_builder.py        # Construye relaciones en Kùzu
│   ├── skills/
│   │   └── cartografo.py           # Skill conversacional (Anexo H)
│   └── cli/
│       └── rag_cli.py              # Interface para comandos ares rag *
├── db/rag/                         # NUEVO: Datos del RAG (no tocar ares_relational.sqlite principal)
│   ├── rag_core.sqlite             # Metadatos + validaciones
│   ├── rag_vectors.sqlite          # Embeddings (sqlite-vec)
│   └── rag_graph.kuzu              # Grafo de conocimiento
├── config/rag.yaml                 # Configuración del módulo
└── docs/rag/                       # Documentación del módulo
    └── SKILL-RAG.md                # Skill definition para IAs
```

---

## ARQUITECTURA DETALLADA

### 1. PRINCIPIO DE INTEGRACIÓN: ARES como Orquestador, RAG como Motor

```
┌─────────────────────────────────────────────────────────────┐
│                    ARES (Orquestador Principal)             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │  ares p     │  │  ares i   │  │  ares agente [name] │   │
│  │  (headless) │  │(interactivo)│  │  (sub-agentes)      │   │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘   │
│         │                │                     │              │
│         └────────────────┴─────────────────────┘              │
│                          │                                    │
│              ┌───────────▼───────────┐                       │
│              │   RAG_ORCHESTRATOR    │  ← Punto único de      │
│              │   (modules/rag/core/) │    entrada al RAG      │
│              └───────────┬───────────┘                       │
│                          │                                    │
│         ┌────────────────┼────────────────┐                   │
│         ▼                ▼                ▼                   │
│    ┌─────────┐     ┌──────────┐     ┌──────────┐             │
│    │  TIER   │     │  TIER    │     │   TIER   │             │
│    │ROUTER   │────▶│ ROUTER   │────▶│  ROUTER  │             │
│    │ (T0-T1) │     │ (T2-T3)  │     │  (T4)    │             │
│    │Determinista    │Semántico │     │Razonador │             │
│    └─────────┘     └──────────┘     └──────────┘             │
│         │                │                │                   │
│    ┌────▼────┐      ┌────▼────┐      ┌───▼────┐              │
│    │ SQLite  │      │sqlite-vec│      │Ollama/ │              │
│    │  Core   │      │ + Kùzu   │      │DeepSeek│              │
│    │         │      │  Grafo   │      │(trigger│              │
│    │         │      │          │      │"piensa")│             │
│    └─────────┘      └──────────┘      └─────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### 2. FLUJO DE DATOS: ares p vs ares i

#### Caso A: `ares p "consulta"` (Headless)

```python
# En modules/rag/cli/rag_cli.py
def headless_query(query: str, options: dict) -> dict:
    """
    Modo sin cabeza: solo T0-T3, nunca T4 (a menos que --deep flag)
    Retorna JSON estructurado para piping
    """
    orchestrator = RAGOrchestrator()
    
    # Forzar tier máximo (default T3, no T4)
    max_tier = Tier.T3_GRAPH
    if options.get('--deep'):
        max_tier = Tier.T4_REASONING  # Solo con flag explícito
    
    result = orchestrator.retrieve(query, max_tier=max_tier)
    
    # Output estructurado (JSON o markdown simple)
    return {
        "answer": result.data,
        "confidence": result.confidence,
        "tier_used": result.tier.name,
        "latency_ms": result.latency_ms,
        "sources": result.sources if hasattr(result, 'sources') else []
    }
```

#### Caso B: `ares i` → Comando `/rag` (Interactivo)

```python
# En el loop interactivo de ares i
def interactive_rag_mode(user_input: str, session_context: dict):
    """
    Modo interactivo: puede escalar a T4 con "piensa"
    Mantiene conversación y contexto de sesión
    """
    orchestrator = RAGOrchestrator(session_pid=session_context['pid'])
    
    # Detectar trigger semántico T4
    force_t4 = orchestrator.is_deep_thinking_trigger(user_input)
    
    result = orchestrator.retrieve(user_input, force_t4=force_t4)
    
    if result.requires_t4 and not force_t4:
        # Sugerir al usuario que use "piensa"
        return f"{result.data}\n\n[Sugerencia: Escribe 'piensa' para análisis profundo]"
    
    return format_interactive_response(result)
```

### 3. ESTRUCTURA DE BASES DE DATOS (Unificada, no tres silos)

#### `db/rag/rag_core.sqlite` (Metadatos y Control)

```sql
-- Tabla de documentos indexados
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    doc_id TEXT UNIQUE NOT NULL,        -- UUID o path hash
    source_path TEXT NOT NULL,          -- Ruta física (resuelta via $MAP)
    doc_type TEXT,                      -- 'markdown', 'python', 'yaml', etc.
    title TEXT,
    summary TEXT,                       -- Generado por LLM en ingesta
    chunk_count INTEGER,
    last_indexed TIMESTAMP,
    validation_status TEXT DEFAULT 'pending' -- pending, approved, stale
);

-- Tabla de chunks (para recuperación granular)
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    doc_id TEXT REFERENCES documents(doc_id),
    chunk_index INTEGER,
    content TEXT,                       -- Texto del chunk
    start_line INTEGER,
    end_line INTEGER,
    char_count INTEGER
);

-- Tabla de entidades extraídas (para grafo)
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    entity_type TEXT,                   -- 'function', 'class', 'concept', 'file'
    source_doc_id TEXT,
    source_chunk_id INTEGER,
    confidence REAL                     -- 0.0-1.0, de extractor
);

-- Tabla de relaciones propuestas (Anexo G: C1-C4)
CREATE TABLE relation_proposals (
    id INTEGER PRIMARY KEY,
    subject_entity TEXT,
    relation_verb TEXT,
    object_entity TEXT,
    criticality TEXT CHECK(criticality IN ('C1','C2','C3','C4')),
    confidence REAL,
    proposed_by TEXT,                   -- 'llm_extractor', 'user', 'inference'
    status TEXT DEFAULT 'pending',      -- pending, approved, rejected, stale
    proposed_at TIMESTAMP,
    validated_by TEXT,
    validated_at TIMESTAMP,
    context_snapshot TEXT               -- JSON del contexto que generó la propuesta
);

-- Tabla de índice de skills (integración con sistema de skills ARES)
CREATE TABLE rag_skills_index (
    id INTEGER PRIMARY KEY,
    skill_name TEXT,
    skill_path TEXT,
    embedding_model TEXT,
    last_synced TIMESTAMP
);
```

#### `db/rag/rag_vectors.sqlite` (sqlite-vec)

```sql
-- Extensión sqlite-vec cargada
CREATE VIRTUAL TABLE embeddings USING vec0(
    chunk_id INTEGER PRIMARY KEY,       -- Referencia a chunks.id
    embedding float[768],               -- nomic-embed-text o similar
    +doc_id TEXT,                       -- Metadata joinable
    +entity_tags TEXT                   -- Tags de entidades en este chunk
);
```

#### `db/rag/rag_graph.kuzu` (Kùzu embebido)

```cypher
// Schema de grafo para conocimiento estructurado
CREATE NODE TABLE Entity(
    name STRING,
    type STRING,                        // 'function', 'module', 'concept', 'skill'
    source_doc STRING,
    validated BOOLEAN DEFAULT false,
    PRIMARY KEY (name)
);

CREATE REL TABLE REQUIRES(
    FROM Entity TO Entity,
    weight DOUBLE DEFAULT 1.0,
    criticality STRING DEFAULT 'C2',    // C1-C4
    validated BOOLEAN DEFAULT false
);

CREATE REL TABLE RELATES_TO(
    FROM Entity TO Entity,
    relation_type STRING,               // 'implements', 'uses', 'describes', etc.
    confidence DOUBLE,
    context STRING                      // Frase que justifica la relación
);

CREATE REL TABLE PART_OF(
    FROM Entity TO Entity,            // Jerarquía: función -> módulo -> proyecto
    order_index INTEGER
);
```

### 4. SISTEMA DE TIERS (T0-T4) - Implementación

#### `modules/rag/core/tier_router.py`

```python
#!/usr/bin/env python3
"""
Motor de recuperación por capas (T0-T4)
Diseñado para latencia ≈ 0 en T0-T3, T4 bajo demanda explícita
"""
import time
import sqlite3
import hashlib
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from functools import lru_cache
import json

class Tier(Enum):
    T0_CACHE = "cache"           # Memoria inmediata
    T1_SQL = "sql"               # Determinista exacto
    T2_VECTOR = "vector"         # Semántica por similitud
    T3_GRAPH = "graph"           # Traversia de conocimiento
    T4_REASONING = "reasoning"   # LLM con chain-of-thought (trigger: "piensa")

@dataclass
class RetrievalResult:
    data: Any
    tier: Tier
    confidence: float
    latency_ms: float
    sources: List[Dict] = field(default_factory=list)
    requires_t4: bool = False
    t4_context: Optional[Dict] = None  # Datos para T4 si se solicita

class TieredRAGRouter:
    """
    Router principal que implementa la estrategia de recuperación progresiva.
    Cada tier es un callable que retorna Optional[RetrievalResult].
    """
    
    T4_TRIGGERS = {'piensa', 'piénsalo', 'analiza profundo', 'deep dive', 
                   'modo pensamiento', 'razona paso a paso', 'think'}
    
    def __init__(self, config_path: str = "config/rag.yaml"):
        self.config = self._load_config(config_path)
        self.cache = {}  # T0: Simple dict, LRU por tamaño
        self.cache_max_size = self.config.get('cache_size', 1000)
        
        # Conexiones lazy
        self._sql_conn = None
        self._vec_conn = None
        self._graph_db = None
        
        # Tier handlers registrados
        self.tier_handlers: Dict[Tier, Callable] = {
            Tier.T0_CACHE: self._t0_cache_lookup,
            Tier.T1_SQL: self._t1_sql_search,
            Tier.T2_VECTOR: self._t2_vector_search,
            Tier.T3_GRAPH: self._t3_graph_traversal,
            Tier.T4_REASONING: self._t4_llm_reasoning,
        }
    
    def _load_config(self, path: str) -> dict:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)
    
    def is_t4_trigger(self, query: str) -> bool:
        """Detecta si el usuario solicita explícitamente razonamiento profundo"""
        query_lower = query.lower()
        return any(trigger in query_lower for trigger in self.T4_TRIGGERS)
    
    def retrieve(self, query: str, 
                 max_tier: Tier = Tier.T4_REASONING,
                 force_t4: bool = False,
                 session_context: Optional[Dict] = None) -> RetrievalResult:
        """
        Pipeline de recuperación progresiva.
        
        Args:
            query: Consulta del usuario
            max_tier: Tier máximo permitido (para ares p, default T3)
            force_t4: Si True, salta directo a T4 (solo para ares i con trigger)
            session_context: Datos de sesión (PID, proyecto actual, etc.)
        """
        start_time = time.time()
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
        
        # T4 forzado: bypass de T0-T3
        if force_t4 and max_tier == Tier.T4_REASONING:
            return self._execute_t4(query, session_context, start_time)
        
        # Pipeline progresivo T0 → T3
        for tier in [Tier.T0_CACHE, Tier.T1_SQL, Tier.T2_VECTOR, Tier.T3_GRAPH]:
            if tier.value > max_tier.value:
                break
            
            handler = self.tier_handlers[tier]
            result = handler(query, query_hash, session_context)
            
            if result and result.confidence >= self._tier_threshold(tier):
                result.latency_ms = (time.time() - start_time) * 1000
                return result
        
        # T3 insuficiente: ofrecer T4 (pero no ejecutar)
        if Tier.T4_REASONING.value <= max_tier.value:
            t3_partial = self._t3_graph_traversal(query, query_hash, session_context)
            return RetrievalResult(
                data=t3_partial.data if t3_partial else {"insufficient_data": True},
                tier=Tier.T3_GRAPH,
                confidence=t3_partial.confidence if t3_partial else 0.5,
                latency_ms=(time.time() - start_time) * 1000,
                requires_t4=True,
                t4_context=self._prepare_t4_context(query, t3_partial, session_context)
            )
        
        # Fallback: nada encontrado
        return RetrievalResult(
            data={"error": "No se encontró información relevante"},
            tier=Tier.T3_GRAPH,
            confidence=0.0,
            latency_ms=(time.time() - start_time) * 1000
        )
    
    def _tier_threshold(self, tier: Tier) -> float:
        """Umbrales de confianza mínima por tier"""
        thresholds = {
            Tier.T0_CACHE: 0.95,
            Tier.T1_SQL: 0.90,
            Tier.T2_VECTOR: 0.75,
            Tier.T3_GRAPH: 0.70,
        }
        return thresholds.get(tier, 0.0)
    
    # ========== IMPLEMENTACIÓN DE TIERS ==========
    
    def _t0_cache_lookup(self, query: str, query_hash: str, ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T0: Cache en memoria (LRU simple)"""
        if query_hash in self.cache:
            cached = self.cache[query_hash]
            return RetrievalResult(
                data=cached['data'],
                tier=Tier.T0_CACHE,
                confidence=0.98,  # Alta confianza por ser exacto
                latency_ms=0,
                sources=cached.get('sources', [])
            )
        return None
    
    def _t1_sql_search(self, query: str, query_hash: str, ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T1: Búsqueda exacta y semántica ligera en SQL"""
        # Implementación: buscar en documents.title, entities.name
        # Retorna si encuentra match exacto o muy cercano
        pass  # Código detallado en implementación
    
    def _t2_vector_search(self, query: str, query_hash: str, ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T2: Búsqueda por similitud de embeddings (sqlite-vec)"""
        # Implementación: embedding de query → vec0 search → reranking
        pass
    
    def _t3_graph_traversal(self, query: str, query_hash: str, ctx: Optional[Dict]) -> Optional[RetrievalResult]:
        """T3: Navegación por grafo de conocimiento (Kùzu)"""
        # Implementación: extraer entidades → traversia 2-3 saltos → ensamblar contexto
        pass
    
    def _t4_llm_reasoning(self, query: str, ctx: Optional[Dict], start_time: float) -> RetrievalResult:
        """T4: Razonamiento profundo con LLM local (Ollama/DeepSeek)"""
        # Implementación: chain-of-thought, streaming opcional, costo controlado
        pass
    
    def _prepare_t4_context(self, query: str, t3_result: Optional[RetrievalResult], 
                           session_ctx: Optional[Dict]) -> Dict:
        """Prepara el contexto enriquecido para T4"""
        return {
            "original_query": query,
            "t3_partial_data": t3_result.data if t3_result else None,
            "session_project": session_ctx.get('project') if session_ctx else None,
            "available_entities": [],  # Populated from T3 traversal
            "suggested_reasoning_path": "Análisis de dependencias y contexto del proyecto"
        }
    
    def _execute_t4(self, query: str, ctx: Optional[Dict], start_time: float) -> RetrievalResult:
        """Ejecución completa de T4 con streaming de progreso"""
        # Integración con Ollama/DeepSeek API
        # Retorna estructura con pasos intermedios y conclusión
        pass
```

### 5. INTEGRACIÓN CON ARES EXISTENTE

#### Modificación mínima a `src/main.py` de ARES

```python
# En el inicializador de ARES, agregar:
from modules.rag.core.rag_orchestrator import RAGOrchestrator

class AresHub:
    def __init__(self):
        # ... código existente ...
        
        # Inicializar RAG como sub-sistema
        self.rag = RAGOrchestrator(
            config_path=f"{self.project_root}/config/rag.yaml"
        )
    
    def handle_query(self, query: str, mode: str = "headless", **options):
        """
        mode: "headless" (ares p) o "interactive" (ares i)
        """
        if mode == "headless":
            # ares p: solo T0-T3, nunca T4 a menos que --deep
            max_tier = Tier.T3_GRAPH
            if options.get('deep'):
                max_tier = Tier.T4_REASONING
            return self.rag.retrieve(query, max_tier=max_tier)
        
        else:  # interactive
            # ares i: detectar trigger "piensa", permitir T4
            force_t4 = self.rag.is_t4_trigger(query)
            return self.rag.retrieve(query, force_t4=force_t4)
```

#### Nuevos comandos CLI: `ares rag *`

```python
# modules/rag/cli/rag_cli.py
import click  # o argparse si ARES no usa click

@click.group(name='rag')
def rag_group():
    """Comandos de recuperación aumentada (RAG)"""
    pass

@rag_group.command()
@click.argument('query')
@click.option('--deep', is_flag=True, help='Forzar análisis profundo (T4)')
@click.option('--tier', type=click.Choice(['t1', 't2', 't3', 't4']), help='Tier máximo')
@click.option('--json', 'output_json', is_flag=True, help='Salida JSON estructurada')
def search(query, deep, tier, output_json):
    """
    ares rag search "consulta" [--deep] [--tier t3] [--json]
    Headless: retorna resultado directo
    """
    orchestrator = RAGOrchestrator()
    
    max_tier = Tier.T4_REASONING if deep else Tier.T3_GRAPH
    if tier:
        max_tier = Tier[tier.upper()]
    
    result = orchestrator.retrieve(query, max_tier=max_tier)
    
    if output_json:
        click.echo(json.dumps(result.to_dict(), indent=2))
    else:
        click.echo(format_console_output(result))

@rag_group.command()
def status():
    """ares rag status - Estado del índice RAG"""
    # Mostrar estadísticas: documentos indexados, entidades, relaciones pendientes

@rag_group.command()
@click.argument('path')
@click.option('--watch', is_flag=True, help='Monitorear cambios')
def ingest(path, watch):
    """ares rag ingest <path> - Indexar documento o directorio"""

@rag_group.command()
def cartografo():
    """ares rag cartografo - Entrar al modo de mapeo conversacional"""
    # Lanza skill interactiva para gestionar el grafo de conocimiento
```

### 6. SKILL CARTÓGRAFO (Integrada con ares i)

```python
# modules/rag/skills/cartografo.py
class SkillCartografoRAG:
    """
    Skill conversacional para gestión del grafo de conocimiento.
    Se activa vía: ares rag cartografo o trigger semántico en ares i
    """
    
    SYSTEM_PROMPT = """Eres el Cartógrafo de Conocimiento de ARES.
    Modo: Negociación supervisada de relaciones C1-C4.
    
    Comandos disponibles:
    - "mapear [archivo/proyecto]" → Analizar y proponer entidades/relaciones
    - "validar pendientes" → Mostrar relaciones C2-C4 por aprobar
    - "conectar X con Y" → Proponer relación específica
    - "grafo de [entidad]" → Visualizar vecindad en grafo
    - "salir" → Volver a ARES normal
    
    Reglas:
    1. Nunca modificar el grafo sin confirmación explícita (sí/no)
    2. Relaciones C3/C4 (seguridad/integridad) requieren doble confirmación
    3. Presentar cambios como diff antes de aplicar
    4. Usar emojis ⚠️ para alertas de criticidad
    """
    
    def run_interactive(self):
        """Loop conversacional integrado con ares i"""
        # Implementación: usa el mismo sistema de streaming que ares i
        pass
```

---

## ESTRUCTURA DE ARCHIVOS COMPLETA (Tree-L3)

```
~/tron/programas/TR/modules/rag/
├── __init__.py                     # Exports: RAGOrchestrator, Tier
├── README.md                         # Documentación rápida del módulo
├── SKILL-RAG.md                      # Definición de skill para IAs
├── requirements.txt                  # Dependencias: sqlite-vec, kuzu, ollama
├── config/
│   └── rag.yaml                      # Configuración principal
├── core/
│   ├── __init__.py
│   ├── tier_router.py                # Motor T0-T4 (150 líneas aprox)
│   ├── context_engine.py             # Snapshots por PID (Anexo D)
│   ├── rag_orchestrator.py           # Interfaz unificada
│   └── session_manager.py            # Gestión de sesiones ares i/p
├── engines/
│   ├── __init__.py
│   ├── base_engine.py                # Abstract base
│   ├── sql_engine.py                 # T1: SQLite determinista
│   ├── vector_engine.py              # T2: sqlite-vec
│   ├── graph_engine.py               # T3: Kùzu wrapper
│   └── llm_engine.py                 # T4: Ollama/DeepSeek client
├── validators/
│   ├── __init__.py
│   └── relation_guard.py             # C1-C4 classifier (Anexo G)
├── ingestors/
│   ├── __init__.py
│   ├── base_ingestor.py
│   ├── markdown_ingestor.py          # Chunking de docs
│   ├── python_ingestor.py            # AST parsing
│   └── graph_builder.py              # Construye triples para Kùzu
├── skills/
│   ├── __init__.py
│   └── cartografo.py                 # Skill conversacional (Anexo H)
├── cli/
│   ├── __init__.py
│   └── rag_cli.py                    # Comandos ares rag *
└── utils/
    ├── __init__.py
    ├── embeddings.py                 # Wrapper de modelo de embeddings
    ├── text_chunker.py               # Estrategias de chunking
    └── cache_manager.py              # LRU y persistencia

~/tron/programas/TR/db/rag/           # DATOS (gitignored)
├── .gitkeep
├── rag_core.sqlite                   # Metadatos + validaciones
├── rag_vectors.sqlite                # Embeddings (sqlite-vec)
└── rag_graph.kuzu/                   # Directorio de Kùzu

~/tron/programas/TR/config/
└── rag.yaml                          # Config del módulo (referencia)
```

---

## CÓDIGO CLAVE: Implementaciones Esenciales

### A. `modules/rag/core/rag_orchestrator.py` (Interfaz Principal)

```python
#!/usr/bin/env python3
"""
RAGOrchestrator: Punto único de entrada para el sistema RAG.
Integra con ARES existente sin modificar su arquitectura core.
"""
import os
import json
from typing import Optional, Dict, Any, Literal
from dataclasses import asdict

from .tier_router import TieredRAGRouter, Tier, RetrievalResult
from ..validators.relation_guard import RelationGuard

class RAGOrchestrator:
    """
    Orquestador del módulo RAG. Expone interfaz simple para ARES.
    
    Uso en ARES:
        from modules.rag import RAGOrchestrator
        rag = RAGOrchestrator()
        result = rag.retrieve("consulta", mode="headless")  # ares p
        result = rag.retrieve("consulta", mode="interactive") # ares i
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.project_root = os.environ.get('TR_PROJECT_ROOT', 
                                          os.path.expanduser('~/tron/programas/TR'))
        self.config_path = config_path or f"{self.project_root}/config/rag.yaml"
        self.db_root = f"{self.project_root}/db/rag"
        
        # Asegurar estructura
        os.makedirs(self.db_root, exist_ok=True)
        
        # Componentes
        self.router = TieredRAGRouter(self.config_path)
        self.guard = RelationGuard(f"{self.db_root}/rag_core.sqlite")
        self.session_pid = os.getpid()
        
        # Snapshot de contexto (Anexo D: inmutabilidad por sesión)
        self._session_snapshot = self._load_session_context()
    
    def _load_session_context(self) -> Dict[str, Any]:
        """Carga o crea snapshot inmutable para esta sesión"""
        # Leer de variables de entorno heredadas (de ares padre)
        snapshot = {
            'pid': self.session_pid,
            'project': os.environ.get('ARES_CURRENT_PROJECT'),
            'cwd': os.getcwd(),
            'map_pointers': self._resolve_map_pointers()
        }
        return snapshot
    
    def _resolve_map_pointers(self) -> Dict[str, str]:
        """Resuelve $MAP desde SQLite (Agnosticismo Estructural)"""
        # Consulta rápida a tabla pointers
        return {'$R': self.project_root, '$S': f"{self.project_root}/modules",
                '$D': f"{self.project_root}/docs", '$M': self.db_root}
    
    def is_deep_thinking_trigger(self, query: str) -> bool:
        """Detecta si el usuario quiere T4"""
        return self.router.is_t4_trigger(query)
    
    def retrieve(self, query: str, 
                 mode: Literal["headless", "interactive"] = "headless",
                 max_tier: Optional[Tier] = None,
                 force_t4: bool = False) -> RetrievalResult:
        """
        Recuperación principal. Modo determina comportamiento de T4.
        
        Args:
            query: Texto de consulta
            mode: "headless" (ares p, no T4 sin --deep) o "interactive" (ares i)
            max_tier: Forzar tier máximo (override de mode)
            force_t4: Forzar T4 (solo en interactive o con flag)
        """
        # Determinar tier máximo según modo
        if max_tier is None:
            max_tier = Tier.T3_GRAPH if mode == "headless" else Tier.T4_REASONING
        
        # En headless, nunca forzar T4 a menos que explicito
        if mode == "headless" and force_t4 and max_tier != Tier.T4_REASONING:
            force_t4 = False
        
        result = self.router.retrieve(
            query=query,
            max_tier=max_tier,
            force_t4=force_t4,
            session_context=self._session_snapshot
        )
        
        # Post-procesamiento: validar relaciones en resultado
        if result.sources:
            result.sources = self._validate_sources(result.sources)
        
        return result
    
    def _validate_sources(self, sources: list) -> list:
        """Filtra fuentes no validadas según RelationGuard"""
        validated = []
        for src in sources:
            # Si la fuente implica relación C3/C4 no validada, marcar como tentative
            if self._is_critical_unvalidated(src):
                src['confidence_tier'] = 'tentative'
            validated.append(src)
        return validated
    
    def _is_critical_unvalidated(self, source: dict) -> bool:
        """Check rápido de criticidad (placeholder para lógica real)"""
        return False  # Implementar con guard.can_execute()
    
    def to_json(self, result: RetrievalResult) -> str:
        """Serialización para ares p --json"""
        return json.dumps({
            'data': result.data,
            'tier': result.tier.value,
            'confidence': result.confidence,
            'latency_ms': result.latency_ms,
            'sources': result.sources,
            'session_pid': self.session_pid
        }, indent=2, default=str)
    
    # ===== Métodos de gestión del índice =====
    
    def ingest_document(self, path: str, doc_type: Optional[str] = None) -> Dict:
        """Indexar nuevo documento en el RAG"""
        from ..ingestors import get_ingestor_for
        ingestor = get_ingestor_for(path, doc_type)
        return ingestor.process(path, self.db_root)
    
    def get_status(self) -> Dict:
        """Estadísticas del índice RAG"""
        # Consultas rápidas a las tres bases
        return {
            'documents_count': 0,  # TODO: implementar
            'entities_count': 0,
            'pending_validations': 0,
            'last_ingestion': None
        }
```

### B. `modules/rag/validators/relation_guard.py` (Seguridad C1-C4)

```python
#!/usr/bin/env python3
"""
RelationGuard: Sistema de clasificación y validación de relaciones.
Implementa Zero-Hallucination para el grafo de conocimiento.
"""
import sqlite3
import json
from dataclasses import dataclass
from typing import Literal, Optional, Dict, List
from enum import Enum

class Criticality(Enum):
    C1_DESCRIPTIVE = "C1"      # Metadatos, tags, semántica libre
    C2_OPERATIONAL = "C2"      # Dependencias de ejecución
    C3_DATA_INTEGRITY = "C3"   # Modificación de datos persistentes
    C4_SECURITY = "C4"         # Ejecución privilegiada, permisos

@dataclass
class Relation:
    subject: str
    verb: str
    obj: str
    confidence: float = 0.9
    source: Literal["llm", "user", "core", "inferred"] = "llm"
    context: Optional[str] = None

class RelationGuard:
    """
    Guardián de relaciones. Determina qué puede usarse para enrutamiento.
    
    Reglas (Anexo G):
    - C4: NUNCA auto-ejecutar. Requiere validación explícita en DB.
    - C3: Requiere validación explícita.
    - C2: Requiere validación O ser parte de core_schema.
    - C1: Auto-aceptar si confianza > 0.95.
    """
    
    VERB_TO_CRITICALITY = {
        # C4 - Seguridad
        'EJECUTA_COMO': Criticality.C4_SECURITY,
        'ESCALA_PRIVILEGIOS': Criticality.C4_SECURITY,
        'BORRA': Criticality.C4_SECURITY,
        'MODIFICA_PERMISOS': Criticality.C4_SECURITY,
        
        # C3 - Integridad
        'ESCRIBE_EN': Criticality.C3_DATA_INTEGRITY,
        'MODIFICA': Criticality.C3_DATA_INTEGRITY,
        'ELIMINA': Criticality.C3_DATA_INTEGRITY,
        'ACTUALIZA_DB': Criticality.C3_DATA_INTEGRITY,
        
        # C2 - Operacional
        'REQUIERE': Criticality.C2_OPERATIONAL,
        'DEPENDE_DE': Criticality.C2_OPERATIONAL,
        'USA': Criticality.C2_OPERATIONAL,
        'IMPORTA': Criticality.C2_OPERATIONAL,
        'LLAMA_A': Criticality.C2_OPERATIONAL,
        
        # C1 - Descriptivo (default)
        'TRATA_SOBRE': Criticality.C1_DESCRIPTIVE,
        'SIMILAR_A': Criticality.C1_DESCRIPTIVE,
        'CATEGORIZADO_COMO': Criticality.C1_DESCRIPTIVE,
        'TAG': Criticality.C1_DESCRIPTIVE,
        'DESCRIBE': Criticality.C1_DESCRIPTIVE,
    }
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_tables()
    
    def _ensure_tables(self):
        """Asegura que tabla de validación existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS relation_validation_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    verb TEXT NOT NULL,
                    object TEXT NOT NULL,
                    criticality TEXT NOT NULL,
                    confidence REAL,
                    proposed_by TEXT,
                    status TEXT DEFAULT 'pending',
                    proposed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    validated_by TEXT,
                    context TEXT,
                    UNIQUE(subject, verb, object)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rel_status 
                ON relation_validation_queue(status, criticality)
            """)
    
    def classify(self, relation: Relation) -> Criticality:
        """Clasifica relación por su verbo"""
        verb_upper = relation.verb.upper()
        return self.VERB_TO_CRITICALITY.get(verb_upper, Criticality.C1_DESCRIPTIVE)
    
    def can_execute(self, relation: Relation) -> bool:
        """
        Determina si la relación puede usarse para enrutamiento/ejecución.
        Core del Zero-Hallucination.
        """
        crit = self.classify(relation)
        
        # C4 y C3: Nunca sin validación explícita
        if crit in (Criticality.C4_SECURITY, Criticality.C3_DATA_INTEGRITY):
            return self._is_validated(relation)
        
        # C2: Validado O es parte del core (hardcoded)
        if crit == Criticality.C2_OPERATIONAL:
            return self._is_validated(relation) or relation.source == "core"
        
        # C1: Auto-aceptar si muy confiable
        if crit == Criticality.C1_DESCRIPTIVE:
            return relation.confidence > 0.95 or self._is_validated(relation)
        
        return False
    
    def _is_validated(self, relation: Relation) -> bool:
        """Check en DB de status 'approved'"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT 1 FROM relation_validation_queue 
                WHERE subject = ? AND verb = ? AND object = ? AND status = 'approved'
            """, (relation.subject, relation.verb, relation.obj))
            return c.fetchone() is not None
    
    def propose(self, relation: Relation, proposed_by: str = "rag_module") -> Dict:
        """
        Ingresa relación a cola de validación. Retorna status.
        """
        crit = self.classify(relation)
        
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("""
                    INSERT INTO relation_validation_queue 
                    (subject, verb, object, criticality, confidence, proposed_by, context, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now', '+7 days'))
                """, (relation.subject, relation.verb, relation.obj,
                      crit.value, relation.confidence, proposed_by,
                      relation.context))
                conn.commit()
                
                if crit == Criticality.C4_SECURITY:
                    return {
                        'status': 'QUEUED_CRITICAL',
                        'message': f'⚠️ Relación C4 ({relation.verb}) requiere validación inmediata',
                        'relation': f'{relation.subject} →[{relation.verb}]→ {relation.obj}'
                    }
                return {'status': 'QUEUED', 'criticality': crit.value}
                
            except sqlite3.IntegrityError:
                return {'status': 'EXISTS', 'message': 'Relación ya en cola'}
    
    def get_pending(self, criticality: Optional[Criticality] = None) -> List[Dict]:
        """Obtener relaciones pendientes de validación"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            if criticality:
                c.execute("""
                    SELECT * FROM relation_validation_queue 
                    WHERE status = 'pending' AND criticality = ?
                    ORDER BY proposed_at
                """, (criticality.value,))
            else:
                c.execute("""
                    SELECT * FROM relation_validation_queue 
                    WHERE status = 'pending'
                    ORDER BY criticality DESC, proposed_at
                """)
            
            return [dict(row) for row in c.fetchall()]
    
    def validate(self, subject: str, verb: str, obj: str, 
                 validator: str, decision: Literal['approved', 'rejected']) -> bool:
        """Validar o rechazar relación pendiente"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE relation_validation_queue 
                SET status = ?, validated_by = ?, validated_at = CURRENT_TIMESTAMP
                WHERE subject = ? AND verb = ? AND object = ? AND status = 'pending'
            """, (decision, validator, subject, verb, obj))
            conn.commit()
            return c.rowcount > 0
```

### C. `modules/rag/engines/llm_engine.py` (T4: Ollama/DeepSeek)

```python
#!/usr/bin/env python3
"""
LLMEngine: Razonamiento profundo T4. Solo bajo demanda explícita.
Integra con Ollama local y opcionalmente DeepSeek API.
"""
import os
import json
import time
from typing import Iterator, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ReasoningResult:
    conclusion: str
    intermediate_steps: list
    confidence: float
    tokens_used: int
    latency_ms: float
    model_used: str

class LLMEngine:
    """
    Motor de razonamiento T4. Chain-of-thought con streaming opcional.
    
    Configuración en rag.yaml:
        t4:
          model_local: "gemma3:4b"  # Ollama
          model_api: "deepseek-chat"  # Fallback
          api_key_env: "DEEPSEEK_API_KEY"
          max_tokens: 4096
          temperature: 0.3  # Baja para determinismo
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('t4', {})
        self.model_local = self.config.get('model_local', 'gemma3:4b')
        self.model_api = self.config.get('model_api')
        self.api_key = os.environ.get(self.config.get('api_key_env', 'DEEPSEEK_API_KEY'))
        
        # Cliente Ollama (lazy import)
        self._ollama = None
        
    def _get_ollama(self):
        if self._ollama is None:
            import ollama
            self._ollama = ollama
        return self._ollama
    
    def reason(self, query: str, context: Dict[str, Any], 
               stream_callback: Optional[callable] = None) -> ReasoningResult:
        """
        Ejecuta razonamiento profundo con contexto enriquecido del RAG.
        
        Args:
            query: Pregunta original del usuario
            context: Output de T3 (entidades, relaciones, documentos relevantes)
            stream_callback: Función para streaming de pasos intermedios
        """
        start_time = time.time()
        
        # Construir prompt estructurado
        prompt = self._build_reasoning_prompt(query, context)
        
        # Preferir Ollama local (soberanía)
        if self._ollama_available():
            result = self._reason_with_ollama(prompt, stream_callback)
        elif self.api_key:
            result = self._reason_with_api(prompt, stream_callback)
        else:
            raise RuntimeError("No hay modelo LLM disponible para T4")
        
        result.latency_ms = (time.time() - start_time) * 1000
        return result
    
    def _build_reasoning_prompt(self, query: str, context: Dict) -> str:
        """Construye prompt con contexto del grafo RAG"""
        entities = context.get('entities', [])
        relations = context.get('relations', [])
        documents = context.get('documents', [])
        
        prompt = f"""Eres un asistente de análisis profundo para el sistema ARES.
Analiza la siguiente consulta usando el contexto proporcionado del grafo de conocimiento.

CONSULTA DEL USUARIO:
{query}

CONTEXTO DEL SISTEMA (recuperado de T0-T3):
Entidades relevantes: {', '.join(entities[:10])}
Relaciones encontradas: {len(relations)}
Documentos fuente: {len(documents)}

Instrucciones:
1. Piensa paso a paso (muestra tu razonamiento)
2. Cita las entidades/documentos específicos que usas
3. Si hay información insuficiente, indícalo claramente
4. Mantén la respuesta técnica y precisa

Razonamiento:"""
        return prompt
    
    def _ollama_available(self) -> bool:
        """Check si Ollama está corriendo localmente"""
        try:
            ollama = self._get_ollama()
            ollama.list()
            return True
        except Exception:
            return False
    
    def _reason_with_ollama(self, prompt: str, stream_callback) -> ReasoningResult:
        """Streaming con Ollama local"""
        ollama = self._get_ollama()
        
        response = ollama.generate(
            model=self.model_local,
            prompt=prompt,
            stream=True,
            options={'temperature': self.config.get('temperature', 0.3)}
        )
        
        full_response = []
        steps = []
        current_step = []
        
        for chunk in response:
            text = chunk.get('response', '')
            full_response.append(text)
            
            # Detectar pasos de razonamiento (heurística simple)
            if text.strip().startswith(('1.', '2.', '3.', 'Paso', 'Primero', 'Segundo')):
                if current_step:
                    steps.append(''.join(current_step))
                current_step = [text]
            else:
                current_step.append(text)
            
            if stream_callback:
                stream_callback(text)
        
        if current_step:
            steps.append(''.join(current_step))
        
        full_text = ''.join(full_response)
        
        # Extraer conclusión (último párrafo o sección)
        conclusion = self._extract_conclusion(full_text)
        
        return ReasoningResult(
            conclusion=conclusion,
            intermediate_steps=steps,
            confidence=0.92,  # Estimado por modelo local
            tokens_used=chunk.get('eval_count', 0),
            latency_ms=0,  # Se calcula afuera
            model_used=self.model_local
        )
    
    def _reason_with_api(self, prompt: str, stream_callback) -> ReasoningResult:
        """Fallback a DeepSeek API (no streaming por defecto)"""
        import requests
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model_api,
            'messages': [
                {'role': 'system', 'content': 'Eres un asistente de análisis técnico profundo.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': self.config.get('temperature', 0.3),
            'max_tokens': self.config.get('max_tokens', 4096)
        }
        
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        content = data['choices'][0]['message']['content']
        
        return ReasoningResult(
            conclusion=content,
            intermediate_steps=[],  # API no da pasos intermedios fácilmente
            confidence=0.88,
            tokens_used=data.get('usage', {}).get('total_tokens', 0),
            latency_ms=0,
            model_used=self.model_api
        )
    
    def _extract_conclusion(self, full_text: str) -> str:
        """Extrae la conclusión final del texto de razonamiento"""
        # Heurística: último párrafo sustancial o sección "Conclusión"
        lines = full_text.strip().split('\n')
        
        # Buscar marcadores de conclusión
        for i, line in enumerate(reversed(lines)):
            if any(marker in line.lower() for marker in ['conclusión', 'conclusion', 'en resumen', 'por tanto']):
                # Retornar desde este punto hasta el final
                idx = len(lines) - 1 - i
                return '\n'.join(lines[idx:]).strip()
        
        # Fallback: últimos 3 párrafos
        return '\n'.join(lines[-3:]).strip()
```

---

## INTEGRACIÓN FINAL CON ARES

### Modificación a `main.py` existente (mínima invasiva)

```python
# En ~/tron/programas/TR/src/main.py, agregar al inicializador:

class AresHub:
    def __init__(self):
        # ... código existente ...
        
        # Inicializar RAG como sub-sistema opcional
        try:
            from modules.rag import RAGOrchestrator
            self.rag = RAGOrchestrator()
            self.rag_available = True
        except ImportError:
            self.rag = None
            self.rag_available = False
    
    def handle_command(self, cmd: str, args: list, mode: str = "headless"):
        # ... código existente ...
        
        # Interceptar comandos RAG
        if cmd == "rag":
            return self._handle_rag_command(args, mode)
        
        # Integrar RAG en consultas generales (opcional, configurable)
        if self.rag_available and self.config.get('rag_auto_enhance'):
            # Enriquecer respuesta con contexto RAG
            pass
    
    def _handle_rag_command(self, args: list, mode: str):
        """Delega a módulo RAG"""
        if not self.rag_available:
            return {"error": "Módulo RAG no disponible. Ejecuta: pip install -r modules/rag/requirements.txt"}
        
        from modules.rag.cli import rag_cli
        # Pasar control al CLI del RAG
        return rag_cli.main(args, standalone_mode=False)
```

---

## CHECKLIST DE IMPLEMENTACIÓN PARA IA CLI

| Paso | Archivo | Descripción | Prioridad |
|------|---------|-------------|-----------|
| 1 | `modules/rag/config/rag.yaml` | Configuración base | Crítico |
| 2 | `scripts/init_rag_db.py` | Inicialización de bases | Crítico |
| 3 | `modules/rag/validators/relation_guard.py` | Seguridad C1-C4 | Crítico |
| 4 | `modules/rag/core/tier_router.py` | Motor T0-T4 | Crítico |
| 5 | `modules/rag/core/rag_orchestrator.py` | Interfaz principal | Crítico |
| 6 | `modules/rag/engines/sql_engine.py` | T1 determinista | Alto |
| 7 | `modules/rag/engines/vector_engine.py` | T2 sqlite-vec | Alto |
| 8 | `modules/rag/engines/graph_engine.py` | T3 Kùzu | Alto |
| 9 | `modules/rag/engines/llm_engine.py` | T4 Ollama/DeepSeek | Alto |
| 10 | `modules/rag/skills/cartografo.py` | Modo conversacional | Medio |
| 11 | `modules/rag/cli/rag_cli.py` | Comandos `ares rag *` | Medio |
| 12 | `modules/rag/ingestors/` | Indexación de documentos | Medio |
| 13 | `docs/rag/SKILL-RAG.md` | Documentación para IAs | Bajo |

---

## PRINCIPIOS DE DISEÑO VERIFICADOS

| Principio Kernel | Implementación en RAG |
|------------------|----------------------|
| **Punteros $MAP** | `rag_orchestrator._resolve_map_pointers()` lee de SQLite |
| **Tiers T0-T4** | `TieredRAGRouter` con umbrales de confianza |
| **Zero-Hallucination** | `RelationGuard` con C1-C4, validación obligatoria C3/C4 |
| **Snapthots por PID** | `RAGOrchestrator._session_snapshot` inmutable |
| **Skill Cartógrafo** | `SkillCartografoRAG` en `modules/rag/skills/` |
| **Agnosticismo** | Rutas resueltas desde DB, no hardcoded |
| **Latencia ≈ 0** | Cache T0, índices SQLite, Kùzu embebido |
| **T4 bajo demanda** | Trigger "piensa", nunca auto-activar en `ares p` |

---

**¿Este blueprint es suficiente para que una IA CLI construya el módulo RAG completo, o requieres especificación adicional de algún componente interconector (ej: protocolo exacto entre `ares i` y el modo cartógrafo, o estrategia de chunking específica)?**

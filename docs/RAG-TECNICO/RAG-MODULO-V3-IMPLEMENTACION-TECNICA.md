# 🧠 RAG MÓDULO V3 - IMPLEMENTACIÓN TÉCNICA

**Fecha:** 2026-03-30
**Contexto:** Implementación del sistema RAG según blueprint SISTEMA-V3.md
**Objetivo:** Documentación técnica completa orientada a pruebas y depuración del nuevo módulo RAG

## 📋 RESUMEN DE ARQUITECTURA

El módulo RAG V3 implementa una arquitectura híbrida de 5 niveles (T0-T4) con zero-hallucination y validación C1-C4:

```
T0: CACHE          → Respuestas en caché (instantáneo)
T1: SQL            → Búsqueda relacional por keywords y entidades
T2: VECTOR         → Similitud semántica con embeddings
T3: GRAPH          → Traversía de grafo de conocimiento
T4: REASONING      → Razonamiento profundo Chain-of-Thought
```

### Características Clave:
- **Zero-Hallucination**: Sistema de validación RelationGuard (C1-C4)
- **Agnosticismo Estructural**: $MAP pointers dinámicos para rutas
- **Inmutabilidad por Sesión**: Snapshots por PID del proceso
- **Lazy Loading**: Conexiones a DB solo cuando son necesarias
- **Multi-proveedor LLM**: Ollama local + DeepSeek API fallback
- **AST Analysis**: Análisis estructural de código Python

## 🏗️ ESTRUCTURA DE DIRECTORIOS

```
modules/rag/
├── __init__.py                    # Exportación de módulo
├── init_rag_db.py                 # Script de inicialización de bases de datos
├── config/
│   └── rag.yaml                   # Configuración completa
├── core/
│   ├── __init__.py
│   ├── tier_router.py            # Router principal T0-T4 (1,181 líneas)
│   └── rag_orchestrator.py       # Orquestador para ARES (162 líneas)
├── engines/
│   ├── __init__.py
│   ├── sql_engine.py             # T1: SQL search (155 líneas)
│   ├── vector_engine.py          # T2: Vector search (222 líneas)
│   ├── graph_engine.py           # T3: Graph traversal (174 líneas)
│   └── llm_engine.py             # T4: LLM reasoning (511 líneas)
├── ingestors/
│   ├── __init__.py
│   ├── file_ingestor.py          # Ingestor genérico (368 líneas)
│   └── code_ingestor.py          # Ingestor de código con AST (447 líneas)
├── validators/
│   ├── __init__.py
│   └── relation_guard.py         # Validación C1-C4 (116 líneas)
├── skills/
│   ├── __init__.py
│   └── cartografo.py             # Skill Cartógrafo (445 líneas)
├── cli/                          # Comandos CLI (vacío actualmente)
├── utils/                        # Utilidades (vacío actualmente)
└── requirements.txt              # Dependencias del módulo
```

## 🔧 COMPONENTES TÉCNICOS

### 1. TieredRAGRouter (`core/tier_router.py`)
**Propósito:** Coordinación de los 5 niveles de recuperación

**Propiedades principales:**
```python
# Lazy loading de motores
@property
def sql_engine(self) -> SQLSearchEngine
@property
def vector_engine(self -> VectorSearchEngine
@property
def graph_engine(self) -> GraphEngine
@property
def llm_engine(self) -> LLMEngine
```

**Flujo de trabajo:**
1. **T0 Cache**: Verifica caché por query hash
2. **T1 SQL**: Búsqueda keyword + entidades en SQLite
3. **T2 Vector**: Similitud semántica con sqlite-vec
4. **T3 Graph**: Traversía de relaciones en Kùzu
5. **T4 Reasoning**: Chain-of-Thought con LLM

**Métodos clave:**
- `retrieve()`: Punto de entrada principal
- `_t0_cache_lookup()`: Búsqueda en caché LRU
- `_t1_sql_search()`: SQL con FTS y entidades
- `_t2_vector_search()`: Embeddings + similitud coseno
- `_t3_graph_traversal()`: Grafo de conocimiento
- `_t4_llm_reasoning()`: Razonamiento profundo
- `_suggest_reasoning_path()`: Sugiere camino para T4

### 2. RAGOrchestrator (`core/rag_orchestrator.py`)
**Propósito:** Interfaz unificada para ARES

**Integración con ARES:**
```python
from modules.rag import RAGOrchestrator
rag = RAGOrchestrator()
result = rag.retrieve("consulta", mode="headless")  # ares p
result = rag.retrieve("consulta", mode="interactive") # ares i
```

**Métodos principales:**
- `retrieve()`: Recuperación principal con modos headless/interactive
- `is_deep_thinking_trigger()`: Detección de triggers para T4
- `ingest_document()`: Indexar nuevo documento
- `get_status()`: Estadísticas del índice
- `get_cartografo()`: Obtener skill Cartógrafo
- `run_cartografo()`: Ejecutar modo interactivo Cartógrafo

### 3. Motores de Búsqueda

#### 3.1 SQLSearchEngine (`engines/sql_engine.py`)
**Tecnología:** SQLite3 + FTS5
**Índices:** `documents`, `entities`, `keywords`
**Métodos:** `keyword_search()`, `entity_search()`, `hybrid_search()`

#### 3.2 VectorSearchEngine (`engines/vector_engine.py`)
**Tecnología:** sqlite-vec + Ollama embeddings
**Modelo:** `gemma3:4b` (embeddinggemma)
**Dimensiones:** 384 (all-MiniLM-L6-v2 compatible)
**Métodos:** `embed_text()`, `similarity_search()`, `hybrid_rerank()`

#### 3.3 GraphEngine (`engines/graph_engine.py`)
**Tecnología:** Kùzu embedded graph database
**Esquema:** Nodos (Entity, Document, Concept) + Relaciones
**Métodos:** `traverse()`, `find_relationships()`, `expand_neighborhood()`

#### 3.4 LLMEngine (`engines/llm_engine.py`)
**Proveedores:** Ollama local (prioritario) → DeepSeek API (fallback)
**Modelos:** `gemma3:4b` (local), `deepseek-chat` (API)
**Chain-of-Thought:** 6 pasos estructurados
**Métodos:** `reason()`, `reason_async()`, `get_status()`

### 4. Ingestores

#### 4.1 FileIngestor (`ingestors/file_ingestor.py`)
**Formatos soportados:** `.txt`, `.md`, `.py`, `.json`, `.yaml`, `.yml`
**Chunking inteligente:** Basado en estructura del documento
**Metadata extraction:** Tipo, tamaño, líneas, encoding

#### 4.2 CodeIngestor (`ingestors/code_ingestor.py`)
**Análisis AST:** Python (funciones, clases, métodos, imports)
**Entidades extraídas:** `CodeEntity`, `CodeRelationship`
**Chunking estructural:** Por entidades (funciones/clases) con contexto

### 5. RelationGuard (`validators/relation_guard.py`)
**Sistema de validación C1-C4:**
- **C1 (Descriptivo)**: Hechos verificables (auto-aprobado)
- **C2 (Operacional)**: Acciones del sistema (aprobación simple)
- **C3 (Integridad)**: Datos sensibles (doble confirmación)
- **C4 (Seguridad)**: Operaciones críticas (triple validación)

**Base de datos:** SQLite con tablas `validations`, `validation_logs`

### 6. Skill Cartógrafo (`skills/cartografo.py`)
**Propósito:** Gestión conversacional del grafo de conocimiento
**Comandos:** `mapear`, `validar`, `conectar`, `grafo`, `salir`
**Integración:** Se activa via `ares rag cartografo` o trigger semántico

## 🛠️ PRUEBAS Y DEPURACIÓN

### 1. Pruebas de Componentes Individuales

#### 1.1 Probando TieredRAGRouter
```python
# test_tier_router.py
from modules.rag.core.tier_router import TieredRAGRouter

router = TieredRAGRouter("config/rag.yaml")

# Test T1 (SQL)
result = router._t1_sql_search("función login", max_results=5)
print(f"T1 Results: {len(result.data)} items, confidence: {result.confidence}")

# Test T2 (Vector)
result = router._t2_vector_search("autenticación de usuarios", max_results=5)
print(f"T2 Results: {len(result.data)} items, confidence: {result.confidence}")

# Test completo
result = router.retrieve("¿Cómo funciona el sistema de login?", max_tier=Tier.T2_EMBEDDING)
print(f"Full retrieval: tier={result.tier}, confidence={result.confidence}")
```

#### 1.2 Probando motores individuales
```python
# test_engines.py
from modules.rag.engines.vector_engine import VectorSearchEngine

# Test embeddings
engine = VectorSearchEngine({"embeddings": {"model": "gemma3:4b"}})
vector = engine.embed_text("Hello world")
print(f"Vector shape: {len(vector)}, first 5: {vector[:5]}")

# Test similitud
results = engine.similarity_search("authentication system", k=3)
for i, (doc_id, score) in enumerate(results):
    print(f"{i+1}. {doc_id} (score: {score:.3f})")
```

### 2. Depuración del Flujo de Recuperación

#### 2.1 Modo verbose
```bash
# Establecer nivel de log
export RAG_LOG_LEVEL=DEBUG

# Ejecutar con debug
python -c "
from modules.rag.core.rag_orchestrator import RAGOrchestrator
rag = RAGOrchestrator()
result = rag.retrieve('test query', mode='headless')
print(f'Tier: {result.tier}, Confidence: {result.confidence}')
"
```

#### 2.2 Monitoreo de bases de datos
```bash
# SQLite documents
sqlite3 db/rag/rag_sqlite.db "SELECT count(*) as total_docs FROM documents;"

# sqlite-vec embeddings
sqlite3 db/rag/rag_vector.db "SELECT count(*) as total_vectors FROM embeddings;"

# Kùzu graph
python -c "
from kuzu import Database
db = Database('db/rag/rag_graph.kuzu')
result = db.execute('MATCH (n) RETURN count(n) as nodes')
print(f'Graph nodes: {result.get_next()[0]}')
"
```

### 3. Pruebas de Ingestión

#### 3.1 Ingestión de documento simple
```python
# test_ingestion.py
from modules.rag.core.rag_orchestrator import RAGOrchestrator

rag = RAGOrchestrator()
result = rag.ingest_document("/path/to/document.md")
print(f"Ingested: {result['document_id']}, chunks: {result['chunks_count']}")
```

#### 3.2 Ingestión de código con AST
```python
# test_code_ingestion.py
from modules.rag.ingestors.code_ingestor import CodeIngestor

ingestor = CodeIngestor()
doc = ingestor.process("/path/to/module.py")
print(f"Entities extracted: {len(doc.entities)}")
for entity in doc.entities[:5]:
    print(f"  - {entity['name']} ({entity['entity_type']})")
```

### 4. Pruebas de Validación C1-C4

```python
# test_validation.py
from modules.rag.validators.relation_guard import RelationGuard

guard = RelationGuard("db/rag/rag_core.sqlite")

# Test C1 (auto-aprobado)
result = guard.validate("descriptive", "El sistema usa Python 3.11", {})
print(f"C1 validation: {result['status']}, confidence: {result['confidence']}")

# Test C2 (requiere aprobación)
result = guard.validate("operational", "Eliminar tabla de usuarios", {"user": "admin"})
print(f"C2 validation: {result['status']}, requires_approval: {result['requires_approval']}")
```

## 🐛 DIAGNÓSTICO DE ERRORES COMUNES

### 1. "No se pudo cargar sqlite-vec"
**Síntoma:** `sqlite3.OperationalError: no such module: vec0`
**Causa:** Extensión sqlite-vec no instalada
**Solución:**
```bash
# Instalar sqlite-vec
pip install sqlite-vec

# Verificar instalación
python -c "import sqlite_vec; print('sqlite-vec version:', sqlite_vec.__version__)"
```

### 2. "Ollama no disponible"
**Síntoma:** `ConnectionError: HTTPConnectionPool`
**Causa:** Ollama no está corriendo
**Solución:**
```bash
# Iniciar Ollama
ollama serve &

# Verificar modelos
ollama list

# Probar embeddings
curl http://localhost:11434/api/embeddings -d '{"model": "gemma3:4b", "prompt": "test"}'
```

### 3. "Kùzu database error"
**Síntoma:** `RuntimeError: Failed to create database directory`
**Causa:** Permisos o espacio en disco
**Solución:**
```bash
# Verificar permisos
ls -la db/rag/

# Crear directorio si no existe
mkdir -p db/rag/

# Verificar espacio
df -h .
```

### 4. "Baja confianza en resultados"
**Síntoma:** `confidence < 0.6` consistentemente
**Causas:**
- Índice vacío o con pocos documentos
- Embeddings de baja calidad
- Consultas demasiado genéricas
**Solución:**
```bash
# Verificar estado del índice
ares rag status

# Ingerir más documentos
ares rag ingest /path/to/docs/

# Probar con consultas específicas
ares p "buscar función 'def authenticate_user' en módulo auth"
```

## 📊 MÉTRICAS Y MONITOREO

### 1. Métricas de rendimiento
```python
# Métricas por tier
metrics = {
    't0_cache_hit_rate': cache_hits / total_queries,
    't1_sql_latency_avg': sum(sql_times) / len(sql_times),
    't2_vector_recall@5': relevant_found / total_relevant,
    't3_graph_traversal_depth': avg_traversal_depth,
    't4_reasoning_confidence': avg_reasoning_confidence
}
```

### 2. Logs estructurados
```python
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('rag')

# Log estructurado
logger.info(json.dumps({
    'event': 'retrieval_complete',
    'query': query,
    'tier': result.tier.name,
    'confidence': result.confidence,
    'latency_ms': result.latency_ms,
    'sources_count': len(result.sources)
}))
```

### 3. Health checks
```bash
# Script de health check
python modules/rag/health_check.py

# Salida esperada:
# {
#   "status": "healthy",
#   "components": {
#     "sql": {"status": "ok", "documents": 142},
#     "vector": {"status": "ok", "embeddings": 1250},
#     "graph": {"status": "ok", "nodes": 89, "edges": 210},
#     "llm": {"status": "ok", "providers": ["ollama"]}
#   }
# }
```

## 🔄 FLUJOS DE TRABAJO

### 1. Inicialización del sistema
```bash
# 1. Instalar dependencias
pip install -r modules/rag/requirements.txt

# 2. Inicializar bases de datos
python modules/rag/init_rag_db.py

# 3. Ingerir documentos iniciales
ares rag ingest ~/tron/programas/TR/docs/

# 4. Verificar estado
ares rag status
```

### 2. Desarrollo y testing
```bash
# 1. Ejecutar tests unitarios
cd ~/tron/programas/TR
python -m pytest modules/rag/tests/ -v

# 2. Ejecutar pruebas de integración
python modules/rag/tests/integration_test.py

# 3. Depurar con pdb
python -m pdb -c "from modules.rag.core.tier_router import TieredRAGRouter; r=TieredRAGRouter(); r.retrieve('test')"
```

### 3. Monitoreo en producción
```bash
# 1. Verificar logs
tail -f ~/.cache/ares/rag.log

# 2. Monitorear métricas
watch -n 5 'ares rag status --json | jq .'

# 3. Health check periódico
crontab -e
# */5 * * * * cd ~/tron/programas/TR && python modules/rag/health_check.py >> /tmp/rag_health.log
```

## 📝 COMANDOS CLI DISPONIBLES

### Comandos ARES integrados:
```bash
# RAG general
ares rag status                    # Estado del sistema RAG
ares rag ingest <archivo>          # Ingerir documento
ares rag cartografo                # Modo Cartógrafo interactivo

# Uso en consultas
ares p "consulta" --rag            # Usar RAG en modo headless
ares i --rag                       # Modo interactivo con RAG
ares i --rag --think               # Interactivo con RAG + pensamiento profundo
```

### Comandos internos de depuración:
```bash
# Directamente desde Python
python -m modules.rag.init_rag_db --reset      # Reiniciar bases
python -m modules.rag.validators.relation_guard --stats  # Estadísticas validación
python -m modules.rag.skills.cartografo --test # Test skill Cartógrafo
```

## 🚨 PROCEDIMIENTOS DE EMERGENCIA

### 1. Índice corrupto
```bash
# 1. Detener ARES
pkill -f "ares i"

# 2. Respaldar índice corrupto
mv db/rag db/rag_corrupt_$(date +%Y%m%d_%H%M%S)

# 3. Reconstruir
python modules/rag/init_rag_db.py
ares rag ingest /ruta/a/documentos/importantes

# 4. Reiniciar
ares i --rag
```

### 2. Memory leak
```bash
# 1. Identificar proceso
ps aux | grep -i rag | grep -v grep

# 2. Verificar memoria
top -p $(pgrep -f "python.*rag")

# 3. Reiniciar con límites
ulimit -v 1000000  # 1GB límite
python -c "from modules.rag.core.rag_orchestrator import RAGOrchestrator; rag=RAGOrchestrator()"
```

### 3. LLM no responde
```bash
# 1. Verificar Ollama
curl -s http://localhost:11434/api/tags | jq .

# 2. Probar con modelo alternativo
export RAG_LLM_MODEL="deepseek-chat"
export DEEPSEEK_API_KEY="tu_key"

# 3. Forzar fallback
python -c "
import os
os.environ['RAG_LLM_FORCE_API'] = '1'
from modules.rag.core.rag_orchestrator import RAGOrchestrator
rag = RAGOrchestrator()
"
```

## 📈 OPTIMIZACIONES RECOMENDADAS

### 1. Para desarrollo:
```yaml
# config/rag.yaml (development)
cache:
  size: 100  # Cache reducido
embeddings:
  batch_size: 4  # Lotes pequeños
graph:
  memory_limit_mb: 256  # Límite bajo
```

### 2. Para producción:
```yaml
# config/rag.yaml (production)
cache:
  size: 1000  # Cache amplio
embeddings:
  batch_size: 32  # Lotes grandes
graph:
  memory_limit_mb: 1024  # Más memoria
llm:
  timeout_seconds: 30  # Timeout generoso
```

### 3. Para testing:
```yaml
# config/rag.yaml (testing)
cache:
  enabled: false  # Sin cache
embeddings:
  mock: true  # Embeddings mock
graph:
  in_memory: true  # Grafo en memoria
llm:
  mock_reasoning: true  # Razonamiento simulado
```

---

## 🎯 CONCLUSIÓN

El módulo RAG V3 implementa una arquitectura híbrida completa con:

✅ **5 niveles de recuperación** (Cache → SQL → Vector → Graph → Reasoning)
✅ **Sistema de validación C1-C4** para zero-hallucination
✅ **Agnosticismo estructural** con $MAP pointers dinámicos
✅ **Multi-proveedor LLM** con fallback automático
✅ **Análisis AST** para código Python
✅ **Skill Cartógrafo** para gestión conversacional
✅ **Integración completa** con ARES CLI

**Próximos pasos recomendados:**
1. Implementar suite completa de tests unitarios
2. Añadir métricas de telemetría detalladas
3. Desarrollar dashboard de monitoreo
4. Optimizar embeddings para dominio específico
5. Implementar sistema de feedback y mejora continua

**Referencias:**
- Blueprint original: `docs/KERNEL/SISTEMA-V3.md`
- Configuración: `modules/rag/config/rag.yaml`
- Inicialización: `modules/rag/init_rag_db.py`
- Integración ARES: `src/main.py` (comandos `ares rag *`)
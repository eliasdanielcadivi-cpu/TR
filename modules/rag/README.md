# Módulo RAG Embebido - Sistema V3

Módulo de Recuperación Aumentada por Grados (T0-T4) para ARES.
Implementa la arquitectura descrita en `docs/KERNEL/SISTEMA-V3.md`.

## Características Principales

- **Arquitectura híbrida T0-T4**: Cache → SQL → Vector → Graph → Reasoning
- **Zero-Hallucination**: Sistema de validación RelationGuard C1-C4
- **Soberanía de datos**: Ollama local para embeddings y razonamiento
- **Agnosticismo estructural**: Rutas resueltas dinámicamente vía $MAP
- **Latencia ≈0**: Cache agresiva e índices optimizados

## Estructura del Módulo

```
modules/rag/
├── core/           # Componentes core
│   ├── rag_orchestrator.py    # Punto único de entrada
│   ├── tier_router.py         # Motor T0-T4
│   └── context_engine.py      # Snapshots por PID
├── engines/        # Motores de búsqueda
│   ├── sql_engine.py          # T1: Determinista
│   ├── vector_engine.py       # T2: sqlite-vec
│   ├── graph_engine.py        # T3: Kùzu
│   └── llm_engine.py          # T4: Ollama/DeepSeek
├── validators/     # Validación
│   └── relation_guard.py      # C1-C4 Zero-Hallucination
├── ingestors/      # Ingestión
│   ├── file_ingestor.py       # Markdown, Python, etc.
│   ├── code_ingestor.py       # AST parsing
│   └── graph_builder.py       # Construye relaciones en Kùzu
├── skills/         # Skills conversacionales
│   └── cartografo.py          # Skill Cartógrafo
├── cli/            # Interfaz CLI
│   └── rag_cli.py             # Comandos `ares rag *`
├── utils/          # Utilidades
├── config/         # Configuración
└── db/             # Bases de datos (en proyecto TR/db/rag/)
```

## Instalación

1. Instalar dependencias:
   ```bash
   pip install -r modules/rag/requirements.txt
   ```

2. Inicializar bases de datos:
   ```bash
   python modules/rag/init_rag_db.py
   ```

3. Configurar en `config/rag.yaml` (opcional).

## Uso

### Comandos CLI
```bash
# Buscar con RAG
ares rag search "consulta" [--deep] [--tier t3] [--json]

# Estado del índice
ares rag status

# Indexar documento
ares rag ingest <path> [--watch]

# Modo Cartógrafo (gestión de grafo)
ares rag cartografo
```

### Integración con ARES
```bash
# Headless (solo T0-T3)
ares p "consulta"

# Headless con análisis profundo (T4)
ares p "consulta" --deep

# Interactivo (puede escalar a T4 con "piensa")
ares i
```

### Desde Python
```python
from modules.rag import RAGOrchestrator

rag = RAGOrchestrator()
result = rag.retrieve("consulta", mode="headless")
print(result.data)
```

## Tiers de Recuperación

| Tier | Tipo | Tecnología | Latencia | Uso |
|------|------|------------|----------|-----|
| T0 | Cache | Memoria | ≈0ms | Cache LRU de consultas exactas |
| T1 | Determinista | SQLite | <10ms | Búsqueda exacta en metadatos |
| T2 | Semántica | sqlite-vec | <50ms | Similitud de embeddings |
| T3 | Conocimiento | Kùzu | <100ms | Traversia de grafo |
| T4 | Razonamiento | Ollama/DeepSeek | 1-10s | Chain-of-thought profundo |

## RelationGuard C1-C4

Sistema de validación para prevenir alucinaciones:

- **C1_DESCRIPTIVE**: Metadatos y tags (auto-aprobado si confianza > 0.95)
- **C2_OPERATIONAL**: Dependencias de ejecución (validación o core schema)
- **C3_DATA_INTEGRITY**: Modificación de datos persistentes (validación explícita)
- **C4_SECURITY**: Ejecución privilegiada (validación explícita obligatoria)

## Configuración

Ver `modules/rag/config/rag.yaml` para opciones completas.

## Notas de Diseño

1. **Filosofía atómica**: Cada módulo tiene máximo 3 funciones públicas principales.
2. **Agnosticismo**: Rutas resueltas desde SQLite, no hardcoded.
3. **Soberanía**: Ollama local por defecto, API como fallback.
4. **Compatibilidad**: Coexiste con sistema Apollo RAG existente.

## Próximos Pasos

1. Implementar ingestión de documentos reales
2. Optimizar traversia de grafo para T3
3. Añadir más skills conversacionales
4. Integración profunda con UI de ARES
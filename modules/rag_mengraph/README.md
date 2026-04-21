# 🕸️ Módulo RAG Mengraph (OpenCore)

Sistema de Recuperación Aumentada por Grafo basado en Memgraph (Grafo en RAM).

## 🛠️ Interfaz Universal (Toolification)
Este módulo está diseñado para ser invocado como una herramienta pura por LLMs externos.

### Funciones Públicas (core/tool.py):
1. `query_json(text)`: Retorna hallazgos estructurados del grafo.
2. `get_schema_summary()`: Retorna el esquema MAGE del grafo.
3. `quick_stats()`: Retorna métricas de nodos y relaciones.

## 🚀 Uso vía CLI
```bash
ares rag query "término" --json
```

## 🏗️ Arquitectura
- **core/**: Lógica de recuperación y tool interface.
- **storage/**: Driver de conexión con Memgraph (Bolt).
- **extraction/**: NLP (spaCy) para convertir texto en nodos/relaciones.

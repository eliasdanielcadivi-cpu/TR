# Apollo Data — Persistencia RAG + CRM

**Fecha:** 2026-03-09
**Estado:** Fase 0 — Schema inicializado

---

## Archivos de Base de Datos

| Archivo | Propósito | Tamaño |
|---------|-----------|--------|
| `knowledge.db` | RAG: documentos, chunks, embeddings (sqlite-vec), entidades, relaciones | ~0 MB (vacío) |
| `users.db` | CRM: usuarios, clientes, interacciones, follow-ups | ~0 MB (vacío) |

---

## Schema RAG (knowledge.db)

### Tablas

```sql
-- Documentos fuente
documents (id, title, source, ingested_at, metadata)

-- Chunks de texto
chunks (id, document_id, chunk_index, text, tokens, parent_chunk_id)

-- Embeddings vectoriales (sqlite-vec)
embeddings (chunk_id, vector[1024], document_id, chunk_index)

-- Entidades extraídas
entities (id, name, type, description, embedding[1024])

-- Relaciones entre entidades
relations (id, subject_id, predicate, object_id, chunk_id, confidence)
```

### Modelo de Embeddings

- **Modelo:** `mxbai-embed-large:335m` (Ollama)
- **Dimensiones:** 1024
- **Métrica:** Coseno

---

## Schema CRM (users.db)

### Tablas

```sql
-- Usuarios del sistema ARES
users (id, name, email, created_at, last_active, preferences)

-- Clientes (decantados de múltiples fuentes)
clients (id, name, type, source, status, metadata, created_at, updated_at)

-- Interacciones con clientes
interactions (id, client_id, user_id, type, channel, summary, full_content, sentiment, action_items, created_at)

-- Relaciones cliente-documento
client_documents (client_id, document_id, relevance_score)
```

### Fuentes Soportadas

- WhatsApp (exportación TXT)
- Email (IMAP/POP3)
- Web (formularios)
- Importación manual (CSV/JSON)

---

## Uso desde Python

```python
from modules.ia.apollo import apollo_db

# Conectar a RAG
rag_conn = apollo_db.get_connection(db_type="knowledge")

# Conectar a CRM
crm_conn = apollo_db.get_connection(db_type="users")

# Cerrar conexiones
apollo_db.close_db()
```

---

## Notas de Implementación

- **sqlite-vec:** Extensión cargada dinámicamente para búsqueda vectorial
- **ChromaDB:** Alternativa si sqlite-vec presenta issues
- **Embeddings:** Generados vía Ollama API (`mxbai-embed-large:335m`)
- **LLM:** `alibayram/smollm3:latest` o DeepSeek API (configurable)

---

*Documento vivo. Actualizar con cada cambio de schema.*

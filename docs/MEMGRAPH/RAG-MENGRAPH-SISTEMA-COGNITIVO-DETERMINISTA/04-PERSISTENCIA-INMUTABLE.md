# INFORME 04: PERSISTENCIA INMUTABLE Y EVIDENCIA
**Sistema:** RAG Mengraph V1.0
**Módulo:** `modules/rag_mengraph/storage/`

## 🗃️ EL CONCEPTO: EL ANCLA DETERMINISTA
En un sistema cognitivo, los datos deben ser inmutables. El motor de persistencia utiliza la técnica **Merge-and-Hash** para asegurar que el conocimiento nunca se degrade ni se duplique.

### Componentes Clave:
1.  **Inyector Cypher ACID (`ingestor.py`):** Realiza operaciones de `MERGE` en Memgraph. Si el nodo existe, actualiza el timestamp; si no, lo crea con su vector semántico.
2.  **Adverbios de Evidencia (Hash SHA-256):** Cada relación (arista) en el grafo lleva una propiedad `evidence_hash`.
    -   Este hash apunta al fragmento exacto de texto que originó la conexión.
    -   Permite una trazabilidad forense total: *"¿Por qué ARES cree que A se conecta con B? Porque aquí está el hash que lo prueba"*.

## ⚙️ FUNCIONAMIENTO TÉCNICO
El sistema genera embeddings semánticos (1024 dimensiones) vía Ollama antes de la inyección. Esto permite:
-   Búsqueda semántica instantánea.
-   Actualización de vectores en caliente (población de índices HNSW).

### Índices HNSW:
Se automatizó la creación de índices vectoriales para cada Sustantivo:
`CREATE VECTOR INDEX index_ai_skill_vector ON :AI_SKILL(embedding)`

## 🥤 SACANDO EL JUGO
Gracias a los Hashes de Evidencia, este RAG es **auditable**. Puedes usar Memgraph Lab para buscar una relación sospechosa y pedirle al sistema que te muestre el manual o bitácora original basándose en el hash.

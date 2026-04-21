# INFORME 05: RECUPERACIÓN HÍBRIDA Y PODA
**Sistema:** RAG Mengraph V1.0
**Módulo:** `modules/rag_mengraph/core/`

## 🔍 EL CONCEPTO: EL DIAGRAMA DE VENN
El motor de recuperación de ARES-TRON no busca textos; busca **dimensiones de la realidad**. Fusiona la búsqueda vectorial (semántica) con el traversal de grafos (lógica física).

### Componentes Clave:
1.  **Búsqueda de Anclas:** Localiza los nodos semánticamente similares a la consulta del usuario mediante el índice HNSW en RAM.
2.  **Expansión de Contexto (Traversal):** Desde el nodo ancla, el sistema explora automáticamente sus conexiones vecinas.
    -   Esto asegura que si preguntas por un Gurú, ARES también te hable de sus Herramientas y Metodologías, aunque no las hayas mencionado en la pregunta.
3.  **Poda Determinista:** Se descartan relaciones cuya confianza sea menor al umbral (default: 0.8) o cuyo Verbo sea prohibido.

## ⚙️ FUNCIONAMIENTO TÉCNICO
Se implementó una consulta Cypher Single-Store:
```cypher
CALL vector_search.search($index, $k, $embed) YIELD node, similarity
WITH node, similarity WHERE similarity >= $threshold
MATCH (node)-[r]-(neighbor)
RETURN node, r, neighbor
```
Esto reduce la latencia a microsegundos al realizar toda la computación dentro de Memgraph.

## 🥤 SACANDO EL JUGO
Para obtener la respuesta más precisa del RAG:
-   Usa el comando `ares p "¿pregunta?" --mengraph --verbose`.
-   El modo `verbose` te mostrará los triplets exactos recuperados, permitiéndote ver el razonamiento físico del grafo detrás de la respuesta de la IA.

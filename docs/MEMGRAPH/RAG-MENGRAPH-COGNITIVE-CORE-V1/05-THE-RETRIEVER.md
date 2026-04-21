# INFORME 05: THE RETRIEVER - RECUPERACIÓN HÍBRIDA
**Sistema:** RAG Mengraph V1.0 - Nucleo Cognitivo

## 🔍 EL DIAGRAMA DE VENN COGNITIVO
Este motor no busca palabras clave. Busca la intersección entre la **Semántica** y la **Estructura Física**.

### 1. Match Vectorial (Semántica)
Usa el índice HNSW para encontrar las "Anclas" (nodos con embeddings similares a la consulta).
- **Modelo:** `mxbai-embed-large` (1024 dims).
- **Métrica:** `cos` (Coseno).

### 2. Traversal BFS (Estructura)
Una vez encontrada el ancla, el sistema ejecuta un `*bfs 0..2` (Breadth-First Search).
- **Expansión:** No solo trae el nodo, sino sus conexiones `:NEXT` y `:PERMITTED_RELATION`.
- **Cero Alucinación:** El LLM solo ve fragmentos que están físicamente conectados en la RAM.

## 🚀 JUGO TÁCTICO
Al preguntar *"¿Qué diseña el Agente?"*:
1. El vector encuentra `Agente Publicador`.
2. El BFS se mueve a `Script de Epifanía`.
3. El LLM recibe: *"El Agente diseña el Script de Epifanía (Verificado físicamente en Grafo)"*.

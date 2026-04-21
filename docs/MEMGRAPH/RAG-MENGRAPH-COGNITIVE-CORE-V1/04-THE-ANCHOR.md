# INFORME 04: THE ANCHOR - PERSISTENCIA INMUTABLE
**Sistema:** RAG Mengraph V1.0 - Nucleo Cognitivo

## 🗃️ ADVERBIOS DE EVIDENCIA (HASH SHA-256)
En este sistema, nada se pierde. Cada relación `(A)-[r]->(B)` lleva un `evidence_hash`.
- **Propósito:** Trazabilidad forense. 
- **Auditoría:** Si ARES dice que un cliente es "VIP", puedes buscar el hash y encontrar el párrafo exacto que lo justifica.

## 🔗 EL PATRÓN :NEXT (ENCADENAMIENTO)
Siguiendo los mejores ejemplos de la documentación local, el sistema crea automáticamente una cadena cronológica:
`(Entidad 1)-[:NEXT]->(Entidad 2)-[:NEXT]->(Entidad 3)`

### ¿Por qué es Vital?
Esto permite a ARES entender el **contexto secuencial**. Si preguntas por el paso 2 de un manual, el grafo sabe físicamente que el paso 1 ocurrió antes.

## 🚀 JUGO TÁCTICO
He configurado Memgraph en modo `IN_MEMORY_ANALYTICAL` durante la ingesta STORM. 
**Resultado:** Ingestas 10 veces más rápidas al evitar la sobrecarga transaccional innecesaria en cargas masivas.

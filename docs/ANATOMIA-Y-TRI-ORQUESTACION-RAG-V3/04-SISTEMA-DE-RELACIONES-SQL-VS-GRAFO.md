# 🕸️ Manual 04: El Sistema de Relaciones (SQL vs Grafo)

En este manual entiendes cómo Ares conecta los puntos. No solo lee, **Relaciona**.

## 🚀 Perspectiva del Operador: ¿A qué afecta esto?
Cuando preguntas "¿Cómo influye X en Y?", Ares no solo busca X e Y, busca el **Camino** entre ellos.

### 🧩 Anatomía del Vínculo Técnico:

#### 1. Relación en SQL (Relacional/Tablas)
- **Atómico:** Tablas vinculadas por `id`. 
- **Ejemplo:** Un Chunk pertenece a un Documento (`chunks.document_id = documents.id`). 
- **Uso:** Ideal para saber de dónde viene un fragmento de texto.
- **Tripas:** `SELECT d.source FROM chunks c JOIN documents d ON c.document_id = d.id WHERE c.id = ?`.

#### 2. Relación en Grafo (Kùzu/Semántico-Lógico)
- **Atómico:** Nodos vinculados por Edges (Relaciones). 
- **Ejemplo:** `Modulo A` -> `IMPORTA` -> `Modulo B`. 
- **Uso:** Ideal para navegar por la arquitectura del código o jerarquías complejas.
- **Tripas (Cypher):** `MATCH (a:Entity)-[r:DEPENDS_ON]->(b:Entity) RETURN a, r, b`.

### 💡 Lección de Productividad:
Para que Ares sea un experto en tu código, debes usar el **Cartógrafo**.
`ares p "Usa el cartógrafo para vincular ai_engine.py con providers.py"`
Ares creará un registro en el grafo. En la próxima búsqueda con `-v`, verás esa relación activada.

---
*💡 Diferencia Clave: SQL es para "dónde está el dato", el Grafo es para "qué significa el dato en conjunto".*

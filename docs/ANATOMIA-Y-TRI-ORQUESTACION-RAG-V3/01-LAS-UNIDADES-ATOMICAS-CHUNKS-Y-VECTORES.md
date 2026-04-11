# 🧬 Manual 01: El ADN del Conocimiento (Chunks, Vectores y Entidades)

Este manual define la unidad mínima de información en ARES RAG V3 desde dos frentes: cómo la ves tú (Texto) y cómo la procesa el motor (Cálculo).

## 🚀 Caso de Uso: El archivo "perdido" `SKILL.md`
**Problema:** Preguntas por `SKILL.md` y Ares dice "No lo sé".
**Diagnóstico:** El archivo existe en el disco, pero no en el **Índice Semántico**. 

### 1. La Unidad Atómica: El CHUNK
Para Ares, un archivo no es una unidad; es una **secuencia de Chunks**.
- **Perspectiva Usuario (Operador):** Es un párrafo con sentido completo que Ares puede citar.
- **Perspectiva Técnica (Arquitecto):** Es un objeto JSON con `id`, `text`, y `metadata`.
- **Anatomía en `knowledge.db`:** 
  ```sql
  -- Consulta las tripas con: sqlite3 knowledge.db "SELECT text FROM chunks LIMIT 1;"
  { "id": "chunk_001", "text": "Las skills son módulos de...", "source": "docs/skills/maestro.md" }
  ```

### 2. La Identidad Matemática: El EMBEDDING
- **Perspectiva Usuario:** Es el "concepto" o "intención" detrás de las palabras.
- **Perspectiva Técnica:** Un vector de 1024 dimensiones (float32) generado por `mxbai-embed-large`.
- **Flujo de Trabajo:**
  1. `file_reader.py` lee el archivo físico.
  2. `chunker.py` lo fragmenta (ej: cada 512 tokens).
  3. `embeddings.py` lo convierte en vector.
  4. `sqlite-vec` lo guarda en la tabla `embeddings`.

### 💡 Lección de Afinación:
Si Ares no encuentra un archivo, la solución es la **Re-Ingesta**:
`ares ingest --path docs/skills/ --dataset default`
Esto fuerza al sistema a crear nuevos átomos (Chunks) y sus identidades (Vectores).

---
*Próximo paso: Aprende a modificar estas piezas en el Manual 02.*

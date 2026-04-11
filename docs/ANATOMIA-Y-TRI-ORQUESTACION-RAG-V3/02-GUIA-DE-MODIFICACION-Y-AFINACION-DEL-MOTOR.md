# 🛠️ Manual 02: Guía de Modificación y Afinación del Motor

En este manual aprendes a mover las perillas del cerebro de Ares. No es solo usar, es **Afinar**.

## 🚀 Matriz de Problemas y Soluciones Técnicas

| Si el Operador percibe... | El Problema Técnico es... | La Pieza (Archivo) a modificar es... |
| :--- | :--- | :--- |
| Ares no encuentra términos exactos. | Poco peso a la búsqueda SQL/FTS5. | `modules/ia/apollo/retrieval.py` (ajustar RRF). |
| Ares da respuestas incompletas. | Chunks demasiado pequeños. | `modules/rag/ingestion/chunker.py` (ajustar CHUNK_SIZE). |
| Ares "alucina" con datos viejos. | Contexto sucio o ruidoso. | `modules/ia/apollo/compression.py` (bajar tokens). |

### 🧩 Guía de Modificación Directa:

#### 1. Modificar la "Agudeza" de la Ingesta
Si programas mucho, Ares necesita entender bloques de código completos.
- **Toca:** `modules/rag/ingestion/chunker.py`.
- **Qué hacer:** Aumenta el `CHUNK_OVERLAP` para que el inicio de una función se vea en el chunk anterior.

#### 2. Modificar el "Filtro de Pensamientos"
Si el modelo `deepseek` muestra sus etiquetas `<think>` y te estorba.
- **Toca:** `config/config.yaml`.
- **Qué hacer:** Añade el nombre exacto del modelo a la lista `thinking`. Ares activará el filtro dinámico automáticamente.

#### 3. Personalizar la "Orquestación"
Ares decide qué nivel de búsqueda usar (Tiered RAG).
- **Toca:** `modules/rag/core/tier_router.py`.
- **Táctica:** Puedes forzar a Ares a usar siempre el Nivel 2 (Grafo) modificando los umbrales de decisión.

---
*💡 Flujo Productivo: "Modifica → Re-Ingesta → Prueba con -v".*

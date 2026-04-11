# 🧪 Manual 03: Los Rayos X (Depuración Verbose -v)

Este manual te enseña a leer la **Dato Bruto** que Ares te muestra cuando usas `-v`. No te fíes de la respuesta final, fíjate en el origen.

## 🚀 Caso de Uso: ¿Cómo saber si Ares está "adivinando"?
**Comando:** `ares p "¿Quién es Daniel Hung?" --rag default -v`

### 📊 Cómo leer las tablas de Depuración:

#### 1. Tabla de Búsqueda Semántica (🧠)
- **Score 0.6+:** Ares está muy seguro de que el fragmento es relevante.
- **Score < 0.4:** El fragmento es ruidoso o poco útil.
- **Dato Arquitectónico:** Si el score es bajo para un archivo clave, Ares está perdiendo **Agudeza**. Solución: Re-ingesta con un Chunker más pequeño.

#### 2. Tabla de Grafo (🕸️)
- **Entidad & Relaciones:** Muestra qué conexiones conceptuales ha hecho Ares.
- **Qué observar:** Si ves `Modulo X -> DEPENDS_ON -> Modulo Y`, Ares responderá como un experto en arquitectura. Si está vacía, Ares responderá como un lector de texto plano.
- **Dato Bruto:** Si las relaciones están mal, borra y regenera el grafo con `graph_builder.py`.

#### 3. Tabla Relacional (📁)
- **FTS/LIKE:** Es la búsqueda clásica por palabras. 
- **Cuándo usar:** Cuando buscas una clase o función exacta (ej: `AIEngine`). Si no aparece aquí, el archivo no ha sido indexado en la base de datos SQL.

### 🧬 Batería de Pruebas Rápidas:
- **Prueba 1:** `ares p "clase AIEngine" -v` (Verifica búsqueda técnica exacta).
- **Prueba 2:** `ares p "¿Cómo se integra el RAG?" -v` (Verifica búsqueda semántica).
- **Prueba 3:** `ares p "¿Cuál es el núcleo del sistema?" -v` (Verifica fusión RRF).

---
*💡 Flujo Productivo: Si Ares falla, activa `-v` y busca en qué tabla falta la información.*

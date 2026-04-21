# INFORME 01: ARQUITECTURA DE INGESTA "THE TROJAN"
**Sistema:** RAG Mengraph V1.0
**Módulo:** `modules/rag_mengraph/ingestion/`

## 🧩 EL CONCEPTO: EL CABALLO DE TROYA
A diferencia de los RAGs tradicionales que confían ciegamente en el NER (Named Entity Recognition) estadístico, el motor **"The Trojan"** inyecta metadatos estratégicos directamente en el pipeline de spaCy.

### Componentes Clave:
1.  **Pipeline Anti-Bloat:** Se configuró un modelo `es_core_news_sm` desactivando componentes pesados (`parser`, `ner`, `lemmatizer`). Esto permite procesar miles de tokens en milisegundos con un consumo de RAM mínimo (crítico para sistemas de 7.3GB).
2.  **Extracción Determinista (EntityRuler):** Se utiliza una técnica de coincidencia de patrones exacta basada en la **Ontología Maestra**.
3.  **El ID Compuesto:** Cada entidad extraída lleva un `id` invisible con el formato `DOMINIO|SUB_ID` (ej: `ARES|GURU_HORMOZI`). 
    -   Esto asegura que, sin importar cómo aparezca el texto (sinónimos), el sistema siempre sepa a qué "Eje Transversal" pertenece.

## ⚙️ FUNCIONAMIENTO TÉCNICO
El archivo `pattern_compiler.py` lee el `ontology_master.json` y genera reglas para spaCy. Cuando `spacy_engine.py` procesa un texto, no solo encuentra la palabra, sino que recupera el ancla lógica del sistema.

### Ejemplo de Salida:
Texto: *"Usa el Cierre de Doble Lazo hoy"*
-   **Ancla:** `Cierre de Doble Lazo`
-   **Sustantivo (Label):** `PROMPT_TEMPLATE`
-   **Trojan ID:** `ARES_COGNITIVE_SYSTEM|GURU_HORMOZI`

## 🥤 SACANDO EL JUGO
Para añadir un nuevo Gurú o Filosofía al sistema:
1.  Edita `config/rag_mengraph/ontology_master.json`.
2.  Añade el patrón en la sección `sustantivos`.
3.  Reinicia la ingesta. **ARES ahora reconoce instantáneamente esa nueva realidad.**

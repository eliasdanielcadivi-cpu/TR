# ANEXO TÉCNICO: INGENIERÍA DE MÓDULOS ARES-TRON (RAG-V3)

Este anexo detalla la implementación física y lógica de los módulos que componen el sistema **RAG de Grafos en RAM**, basándose en la auditoría directa del código fuente en `modules/rag_mengraph/`.

---

## 1. EL CICLO STORM (ORQUESTACIÓN INTEGRAL)
Ubicación: `modules/rag_mengraph/core/orchestrator.py`

El sistema no realiza una ingesta simple; ejecuta un ciclo de seis fases denominado **STORM** (Streaming-Text-Ontology-Relation-Mapping):
1.  **Extracción Determinista**: spaCy identifica "Anclas" (Sustantivos) usando el `EntityRuler`.
2.  **Inyección de Sustantivos**: Los nodos se crean en Memgraph con etiquetas raíz `ARES_ENTITY`.
3.  **Tejido Lógico (Inferencia)**: El `SerendipiaEngine` utiliza un LLM para descubrir "Verbos" entre los sustantivos detectados.
4.  **RelationGuard**: Clasificación de seguridad C1-C4.
5.  **Inyección Directa**: Relaciones seguras (C1/C2) entran al grafo.
6.  **Cuarentena**: Relaciones críticas o nuevas (Serendipia) se desvían a `QuarantineManager`.

---

## 2. SEGURIDAD Y CLASIFICACIÓN (RELATIONGUARD)
Ubicación: `modules/rag_mengraph/validators/relation_guard.py`

ARES-TRON aplica un cortafuegos ontológico:
- **C1/C2 (Rutinario)**: Relaciones pre-autorizadas en `ontology_master.json`.
- **C3/C4 (Crítico)**: Relaciones que afectan la lógica de negocio o seguridad.
- **NEW_VERB (Serendipia)**: Cuando la IA descubre una relación no mapeada, el sistema la marca para revisión humana, evitando la contaminación del grafo.

---

## 3. TRAZABILIDAD Y EVIDENCIA (ADVERBIOS DE EVIDENCIA)
Ubicación: `modules/rag_mengraph/storage/ingestor.py`

Para garantizar que la IA no "alucine" conocimiento, cada nodo y relación incluye:
- **SHA-256 Hash**: Un "Adverbio de Evidencia" generado a partir del texto original.
- **Encadenamiento :NEXT**: Los nodos se conectan secuencialmente según aparecieron en el documento original, permitiendo reconstruir el contexto narrativo mediante algoritmos de grafos.
- **Trojan IDs**: Identificadores inmutables (ej. `GURU_01`) incrustados en los nodos que anclan el lenguaje natural del LLM a la estructura rígida de la base de datos.

---

## 4. MOTOR DE SERENDIPIA Y TEJIDO DE ESQUEMAS
Ubicación: `modules/rag_mengraph/core/serendipia_engine.py` y `schema_weaver.py`

- **Micro-RAG de Esquema**: Antes de que la IA infiera relaciones, el `SchemaWeaver` consulta a Memgraph: *"¿Qué relaciones están permitidas entre estas dos etiquetas?"*. El LLM solo recibe el fragmento de la ontología necesario, optimizando el contexto.
- **Inferencia de Verbos**: El LLM actúa como un "Navegador Semántico", proponiendo conexiones basadas en la realidad del texto pero limitadas por la ontología autorizada.

---

## 5. INTERFAZ UNIVERSAL (MENGRAPHTOOL)
Ubicación: `modules/rag_mengraph/core/tool.py`

Diseñado para la interoperabilidad industrial:
- **Salida JSON Pura**: Compatible con `jq` y otros agentes autónomos.
- **Schema Summary**: Utiliza la capacidad `MAGE llm_util.schema` para que el LLM externo entienda la estructura del grafo en milisegundos.
- **Relevancia Vectorial**: Combina la búsqueda por grafos con distancias de coseno para priorizar los resultados más cercanos a la intención del usuario.

---
*Fin del Anexo Técnico - Documento Generado mediante Auditoría Forense de Código.*

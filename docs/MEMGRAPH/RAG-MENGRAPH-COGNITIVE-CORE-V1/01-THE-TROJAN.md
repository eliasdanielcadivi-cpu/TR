# INFORME 01: ARQUITECTURA "THE TROJAN"
**Sistema:** RAG Mengraph V1.0 - Nucleo Cognitivo

## 🔬 EL PROBLEMA DEL NER ESTADÍSTICO
En un sistema industrial como ARES, no podemos permitir que la IA "adivine" qué es una entidad. Un error del 5% en la detección puede corromper el 100% de la lógica comercial del CRM o de los manuales de Gurús.

## 🛡️ LA SOLUCIÓN: EXTRACCIÓN DETERMINISTA
He implementado un pipeline de **spaCy** configurado en modo **Anti-Bloat**. 

### 1. El Caballo de Troya (Trojan ID)
Utilizamos el campo `id` de `EntityRuler`. Cada vez que el sistema detecta una palabra como "Cierre de Doble Lazo", le ancla un ID inmutable: `ARES_COGNITIVE_SYSTEM|GURU_HORMOZI`.
-   **Veracidad:** Sin importar cómo se escriba, el sistema sabe que es de Hormozi.
-   **Eficacia:** No requiere inferencia del LLM para el anclaje inicial.

### 2. Optimización Térmica y de RAM
El motor desactiva el `parser`, `ner` estadístico y `lemmatizer`. Esto permite que spaCy consuma menos de 100MB de RAM durante el procesamiento, dejando el resto para Memgraph.

## 🚀 JUGO TÁCTICO
Al procesar el manual `test_granular.txt`, el sistema extrajo:
- `Agente Publicador` -> ID: `CORE`
- `Script de Epifanía` -> ID: `GURU_BRUNSON`
- `Lead VIP` -> ID: `CORE`

**Resultado:** ARES ahora tiene anclas físicas irrefutables.

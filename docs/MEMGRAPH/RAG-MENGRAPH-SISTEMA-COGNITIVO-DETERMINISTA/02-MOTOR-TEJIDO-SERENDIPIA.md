# INFORME 02: MOTOR DE TEJIDO Y SERENDIPIA
**Sistema:** RAG Mengraph V1.0
**Módulo:** `modules/rag_mengraph/core/`

## 🕸️ EL CONCEPTO: EL TEJEDOR LÓGICO
Una vez que spaCy identifica los "Sustantivos", el sistema entra en la fase de **Tejido**. El objetivo es descubrir cómo se relacionan físicamente esas entidades dentro del texto, transformándolas en "Verbos".

### Componentes Clave:
1.  **Micro-RAG de Esquema (`schema_weaver.py`):** Antes de llamar al LLM, el sistema consulta a Memgraph: *"¿Qué relaciones están permitidas legalmente entre estos Sustantivos?"*.
    -   Esto reduce el prompt en un 80% y elimina alucinaciones estructurales.
2.  **Motor de Serendipia (`serendipia_engine.py`):** Es la inteligencia que lee el texto original y busca el Verbo.
    -   Si detecta una relación brillante que no está en el mapa, la propone como "Serendipia", permitiendo que el grafo "aprenda" nuevas dinámicas.

## ⚙️ FUNCIONAMIENTO TÉCNICO
El LLM recibe un prompt estructurado con:
-   Entidades detectadas.
-   Leyes ontológicas (esquema permitido).
-   Misión: Generar un JSON de relaciones.

### Ejemplo de Serendipia:
Entidades: `Lead VIP`, `Cierre de Doble Lazo`.
Relación Inferida: `CUALIFICA_A` (Confianza: 0.98).
Razonamiento: *"El texto indica que el cierre se usa específicamente para este tipo de lead"*.

## 🥤 SACANDO EL JUGO
Este motor es el que permite el **Agnosticismo Estructural**. No necesitas programar cada relación; solo define los Sustantivos en la Ontología y el Tejedor hará el resto del trabajo sucio, conectando los puntos por ti.

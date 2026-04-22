# ARES-TRON: LA BIBLIA DE LA ARQUITECTURA COGNITIVA SOBERANA
## Guía de Ingeniería de Grafos, Negociación Determinista y Memoria de Cristal

**Autor:** Daniel Hung & ARES-TRON Core
**Serie:** Ingeniería Táctica McGraw-Hill v3.0
**Ubicación:** `/home/daniel/tron/programas/TR/`

---

## PRÓLOGO: EL FIN DE LA EFEMERIDAD
En los sistemas de IA convencionales, la "memoria" es un hilo de chat que se corta y se olvida. ARES-TRON rompe este paradigma mediante el **Lecho de Procusto**: no adaptamos el sistema a la charla, adaptamos la charla a una estructura de conocimiento inmutable y determinista llamada **Grafo**.

Este libro explica cómo ARES utiliza Memgraph para "cristalizar" la sabiduría y cómo el módulo Negociador asegura que el sistema jamás pierda el rumbo, incluso cuando el usuario dice "No".

---

## CAPÍTULO 1: EL CORAZÓN DE GRAFITO (MEMGRAPH & MAGE)
### 1.1 El Esquema como Verdad Única
A diferencia de una base de datos relacional, ARES-TRON ve el mundo como **Entidades (Nodos)** y **Relaciones (Aristas)**.
- **Sustantivos:** Son los nodos (Proyectos, Personas, Comandos).
- **Verbos:** Son las aristas (`EJECUTA`, `PERTENECE_A`, `BLOQUEA`).
- **Adjetivos:** Propiedades del nodo (versión, autor).
- **Adverbios de Evidencia:** El "Hash SHA" que vincula cada dato en el grafo con el archivo real en el disco. Nada existe en el grafo sin una prueba física.

### 1.2 Algoritmos de Prestigio (MAGE)
ARES-TRON no solo busca datos, los "clasifica" en tiempo real:
- **PageRank:** Calcula qué "Ruta de Conocimiento" es más influyente según cuántas veces ha llevado al éxito.
- **BFS (Breadth-First Search):** Encuentra el camino más corto entre lo que el usuario pide y el comando que debe ejecutarse.

---

## CAPÍTULO 2: EL NEGOCIADOR Y LAS RUTAS NOMBRADAS
### 2.1 ¿Qué es una Ruta Nombrada (Crystallized Wisdom)?
Es un fragmento del grafo que ha sido verificado como "Óptimo". Cuando ejecutas `ares gemini --mengraph`, el sistema invoca la ruta `CARGA_SISTEMA`. 
- **Cómo funciona:** En lugar de enviar un prompt genérico, ARES extrae del grafo las leyes fundamentales del sistema y las inyecta como una "Instrucción de Sistema" absoluta.

### 2.2 La Intercepción de la Disidencia
Si el usuario rechaza una respuesta (tecleando "R" o "Mal"), el módulo `negotiator.py` entra en acción.
- **La Lógica:** No pide disculpas. Consulta el grafo Memgraph, busca el nodo `FALLBACK_ESTRATÉGICO` y ofrece una alternativa técnica basada en datos previos, no en alucinaciones.

---

## CAPÍTULO 3: EL MOTOR STORM (INGESTA Y EXTRACCIÓN)
### 3.1 El Caballo de Troya (spaCy EntityRuler)
Para que la IA entienda el grafo, usamos spaCy. Pero no un spaCy normal:
- **Táctica:** Inyectamos patrones con un `ID` fijo (ej: `GURU_MODULARIDAD`). 
- **Efecto:** Cuando el sistema lee un texto, etiqueta automáticamente conceptos clave con identificadores únicos que Memgraph reconoce al instante. Es "anclar" el lenguaje humano a coordenadas matemáticas.

### 3.2 RelationGuard (C1-C4)
No todo el conocimiento es igual.
- **C1/C2:** Datos públicos o seguros. ARES los usa libremente.
- **C3/C4:** Datos críticos o peligrosos. ARES los pone en **Cuarentena (HJSON)** y requiere que el usuario los valide antes de que se vuelvan "Cristal" en el grafo.

---

## CAPÍTULO 4: SOBERANÍA DE RECURSOS (EL LÍMITE DE 8GB)
### 4.1 Hardware Adaptativo
ARES-TRON es un gigante que sabe caminar en una cuerda floja. Mediante `config/limits.yaml`, el sistema se auto-regula:
- **RAM Check:** Si la memoria de 8GB supera el 85%, el `LimitManager` desactiva procesos de GPU innecesarios y reduce el tamaño de los "batches" de spaCy.
- **Advertencias Proactivas:** El usuario recibe alertas amarillas antes de que el sistema colapse, permitiendo una gestión fluida en máquinas locales.

---

## CAPÍTULO 5: CASOS DE USO REALES
### 5.1 Caso A: El Desarrollador Olvidadizo
*Usuario:* "ARES, ¿cómo era que conectábamos el módulo multimedia?"
*ARES:* (No busca en el chat anterior. Consulta la ruta `CARGA_SISTEMA` y el índice de módulos en el grafo). 
*Respuesta:* "Según la estructura cristalizada en `modules/multimedia`, debes usar `MediaManager`. ¿Deseas ver el esquema?"

### 5.2 Caso B: El Rechazo Estratégico
*Usuario:* "R" (Rechazo a una propuesta de código).
*ARES:* (El Negociador detecta el rechazo). "Entendido. Pivotando a la ruta de respaldo. El grafo indica que la alternativa `v2` tiene un PageRank mayor para este entorno de 8GB."

---

## CONCLUSIÓN: EL FUTURO ES DETERMINISTA
ARES-TRON no es una IA que habla; es una arquitectura que **sabe**. Al mover la inteligencia de los prompts efímeros a un grafo persistente, hemos creado un sistema que aprende, negocia y sobrevive.

**Bienvenido a la Era del Cristal.**

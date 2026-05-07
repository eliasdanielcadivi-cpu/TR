# 🛰️ MANUAL TÉCNICO SOBERANO: ARES-TRON (RAG-V3 + MENGRAPH)

Este documento define la física operativa del sistema ARES-TRON. No es una guía de usuario; es el manual del Arquitecto para la gestión, edición y expansión del Córtex Cognitivo basado en Grafos.

---

## 1. ANATOMÍA DE LA INYECCIÓN JIT (JUST-IN-TIME)

La inyección de información en ARES no es estática (archivos `.md`). Ocurre en el **Tiempo T-10ms** antes de la invocación del modelo. 

### 1.1 El Proceso de Ensamblado
Cuando ejecutas `ares gemini` o `ares run`, el sistema activa el `modules/ia/context_router.py`. Este módulo realiza las siguientes acciones:
1.  **Detección de Alcance**: Identifica el `target_id` (ej. `INIT` o `ares`).
2.  **Activación Estructural**: No busca palabras parecidas; lanza una consulta Cypher `MATCH (n {id: $target})-[:*1..2]->(m)`. Esto recupera el nodo central y todo lo que esté a 2 saltos de distancia.
3.  **Serialización Cognitiva**: Convierte esos nodos y relaciones en un bloque de texto estructurado bajo el encabezado `INSTRUCCIÓN DE SISTEMA`.
4.  **Fusión de Mente y Cuerpo**: Pega este bloque al inicio de tu prompt y lo envía a `gemini-cli`.

### 1.2 Grafo vs. Vectorización
*   **RAG Gráfico (Activo)**: Se usa para leyes, normas, identidades y flujos. Es determinista. Si el grafo dice que `INIT` requiere `Fase Forense`, la IA recibirá esa instrucción sin falta.
*   **RAG Vectorial (Latente)**: Reside en `modules/ia/apollo`. Se activa cuando pides "buscar en documentos". Aquí entra la vectorización (vía `es_core_news_sm` y embeddings). A diferencia del grafo, aquí la recuperación es probabilística (Top-K resultados más parecidos).

---

## 2. EL ESTADO ACTUAL DE LA MEMORIA (CONTENIDO REAL)

Tras la siembra ontológica, tu base de datos Memgraph contiene el **Subgrafo Raíz**:

*   **Nodo Identidad (`ares`)**: Contiene el "Alma" del sistema. Es el nodo que define que ARES es el "Arquitecto" y no un simple "Asistente".
*   **Nodos Modo (`INIT`, `DEV`)**: Definen las fases de trabajo. 
    *   `INIT` está conectado a `Fase Forense Obligatoria`.
    *   `DEV` está conectado a `Atomicidad Paranoica`.
*   **Nodo Documento (`doc_nucleo`)**: Puntero físico al archivo `NUCLEO DE CREACION...`. Permite que la IA "sepa" que su sabiduría proviene de una fuente de verdad verificable.

**¿Por qué estas relaciones?**
Usamos `:SE_RIGE_POR` para principios y `:OPERA_EN` para dominios. Esto permite que la IA sepa que si está en `INIT`, el principio de `Fase Forense` es una ley de la física que no puede ignorar.

---

## 3. MAPA DE CONFIGURACIÓN Y EDICIÓN

Para modificar el comportamiento de ARES, debes saber dónde tocar:

| Elemento | Ubicación de Edición | Método de Aplicación |
| :--- | :--- | :--- |
| **Identidad Base** | `config/identidad/ares.yaml` | `ares gemini` (Fallback) |
| **Flujos de Trabajo** | `scripts/seed_know_how_flow.py` | Ejecutar script para actualizar grafo |
| **Leyes y Principios** | Memgraph Lab (UI) | `MATCH (p:Principio {id: '...'}) SET p.nombre = '...'` |
| **Sesiones de IA** | `db/ares_sessions.db` (SQLite) | `ares sessions` (Listado RAW) |
| **Módulos Tácticos** | `modules/tactico/` | Edición directa en Python (Atomicidad 3-func) |

---

## 4. ARSENAL DE COMANDOS: 10 CASOS REALES (MÉTODO ALCANCE)

Aquí tienes cómo usar el sistema ahora mismo, qué hace el grafo "atrás" y para qué sirve.

### Caso 1: Inicialización de Emprendimiento (Modo INIT)
**Escenario**: Vas a crear un nuevo sistema de gestión de ventas.
**Comando**: `ares run INIT`
*   **Interno**: Busca el nodo `INIT`. Recupera las relaciones `:REQUIERE -> Fase Forense`. 
*   **Recuperación**: Extrae el texto: "No programes sin capturar stdout/stderr".
*   **Por qué**: Fuerza a Gemini a pedirte los logs antes de escribir el código de ventas.

### Caso 2: Auditoría de Código Existente (Modo DEV)
**Escenario**: Quieres saber si un script de Python es "Soberano".
**Comando**: `ares gemini "Revisa mi script ventas.py" --ruta DEV`
*   **Interno**: Salta al nodo `DEV` y sigue la flecha `:SE_RIGE_POR -> Atomicidad Paranoica`.
*   **Recuperación**: Inyecta la regla de "Máximo 3 funciones por archivo".
*   **Por qué**: La IA criticará tu código si es denso, basándose en la ley del grafo.

### Caso 3: Identidad Corporativa en el Prompt
**Escenario**: Necesitas que la IA hable con la voz de tu empresa.
**Comando**: `ares gemini "Redacta un correo" --mengraph`
*   **Interno**: `MATCH (a:Identidad {id: 'ares'})-[:TIENE_ALMA]->(s)`.
*   **Recuperación**: Trae el valor `Alma: Soberanía`.
*   **Por qué**: El correo tendrá un tono directo, autoritario y profesional, no servil.

### Caso 4: Recuperación de Continuidad de Sesión
**Escenario**: Ayer trabajaste en el RAG y hoy quieres seguir.
**Comando**: `ares sessions` (luego copias el Hash) -> `ares gemini "Seguimos con el paso 2" -c [INDICE]`
*   **Interno**: `session_mapper` traduce el Hash inmutable al índice de hoy.
*   **Recuperación**: Reconecta con la charla #25 o #28 de Gemini.
*   **Por qué**: Evitas perder el hilo semántico de lo que la IA ya "aprendió" ayer.

### Caso 5: Despliegue de Entorno de Datos (Diaria)
**Escenario**: Empiezas tu jornada de programación.
**Comando**: `ares gs deploy diaria`
*   **Interno**: Llama a `modules/tactico/plan_manager.py`.
*   **Acción**: Ejecuta `kitty @ set-tab-title CONTROL`, `MATRIX`, etc.
*   **Por qué**: Prepara tu cuerpo físico (terminal) para que coincida con tu layout mental.

### Caso 6: Ingesta de Nueva Sabiduría (STORM)
**Escenario**: Tienes un PDF con un manual de ventas y quieres que ARES lo "sepa".
**Comando**: `ares mengraph ingest "Contenido del manual..." --label VentaSota`
*   **Interno**: `MengraphProcessor` usa spaCy para detectar Sustantivos y Verbos.
*   **Acción**: Crea nodos conectados en Memgraph.
*   **Por qué**: La próxima vez que uses `--mengraph`, ese conocimiento estará disponible por "alcance".

### Caso 7: Diagnóstico de Salud del Sistema
**Escenario**: Sientes que el sistema está lento o falla.
**Comando**: `ares init --status`
*   **Interno**: `diag_manager.py` revisa sockets, Docker y conectividad Bolt.
*   **Acción**: Reporte visual de qué "órgano" está fallando.
*   **Por qué**: Soberanía del Entorno: tú controlas la infraestructura, no al revés.

### Caso 8: Consulta de Verdad en el Grafo (Headless)
**Escenario**: Necesitas que un script externo sepa cuál es el objetivo de INIT.
**Comando**: `ares gemini "objetivo" --ruta INIT --json`
*   **Interno**: Recupera el campo `objective` del nodo `INIT`.
*   **Recuperación**: Devuelve `{"response": "Estructuración y Contratos"}`.
*   **Por qué**: Permite automatizar otros programas usando a ARES como base de datos de intenciones.

### Caso 9: Control Multimedia Táctico
**Escenario**: Estás programando y quieres música ambiental sin salir de la terminal.
**Comando**: `ares media play`
*   **Interno**: `MediaManager` envía señal IPC al socket de MPV.
*   **Por qué**: Mantiene tu atención en el flujo de trabajo (Flow State).

### Caso 10: Sincronización de Identidad Nuclear
**Escenario**: Cambiaste el nombre del proyecto en el grafo y quieres que Ollama lo sepa.
**Comando**: `ares identidad-inyectar`
*   **Interno**: Lee el nodo `Identidad` y re-crea los Modelfiles locales.
*   **Por qué**: Asegura consistencia total: lo que ves en el Lab es lo mismo que la IA cree que es.

---

## 5. REGLA DE ORO DE LA EDICIÓN
**No programes lógica en `src/main.py`.** Si el sistema necesita una nueva cualidad:
1. Crea un módulo en `modules/`.
2. Define máximo 3 funciones.
3. Añade el nodo correspondiente en Memgraph.
4. Conecta el comando en `main.py` solo como un dispatcher.

*Este es el camino a la Soberanía Cognitiva.*

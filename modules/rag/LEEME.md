# 📖 LEEME - Módulo RAG V3 (Refactorización Atómica)

## 🎯 Paradigma y Reflexión
Este sistema ha sido replanteado en sus "primitivas" lógicas. La meta es aislar las tecnologías para que cada parte sea una función pequeña, independiente y físicamente encapsulada en su propia tecnología. El secreto del éxito reside en poner **toda la atención fija en el paso particular y la difusa en el sistema** (la conectividad de lo atómico-primitivo). 

Diseñamos partes atómicas como módulos llamables, configurables y reutilizables, diseñando de manera que sean accesibles desde otros sin romper la reutilización en orquestadores.

## 🛠️ Proceso Estándar de Trabajo (Protocolo Daniel Hung)
Para garantizar la excelencia técnica y evitar el auto-engaño, seguimos este protocolo estrictamente:

1.  **Respaldo Git Obligatorio:** Cada vez que vayamos a trabajar hacemos un respaldo git antes y después de modificar.
2.  **Comprobación de Diferencias:** Comprobamos con `git diff` si ciertamente modificamos solo lo que deberíamos. 
3.  **Atomicidad Indivisible:** Reconfigurar el RAG en funciones pequeñas agrupadas en módulos en subcarpetas de **no más de 3 funciones pequeñas**. Una función debe hacer una sola cosa y bien.
4.  **Predicción de Fallos:** Pensar en los puntos de fallo de cada función y de cada elemento, prediciendo qué pudiera fallar antes de que ocurra.
5.  **Veracidad de Datos Brutos:** Las comprobaciones se basan en **datos brutos** y no en interpretaciones. Es mejor leer la salida bruta de programas y funciones que diseñar una prueba y decir "ok si corre al final ponemos todo bien". No nos auto-engañamos.
6.  **Conexión Inequívoca:** Si se requiere interpretar, debe ser en base a una conexión inequívoca entre un dato bruto y una salida (quizás filtrada), pero conectada directamente con el dato bruto y no manipulada o sustituida.
7.  **Humildad y Consulta Real:** No confiar al 100% en el entrenamiento previo. Buscar **CÓDIGO REAL Y PALPABLE DE EJEMPLO** de documentación oficial, manuales y tutoriales reales. Si ya estamos en la conexión de lo atómico, buscamos **CÓDIGO REAL DE INTERCONEXIÓN**.
8.  **Límite de Soberbia:** Si dedico tres o cuatro iteraciones y no se resuelve, pedimos auxilio al usuario con un informe en mano y documentos clave en rutas absolutas para buscar en una IA externa.
9.  **Viveza Técnica:** Aprovechar SDKs y tecnologías intermedias (como LangChain con Kùzu) que hagan más fácil y rápido el trabajo sin agregar RAM indiscriminada.

## 🤖 Política de Configuración de Modelos (Ollama & DeepSeek)
Para evitar el "hardcodeo" y mantener la flexibilidad, seguimos esta política:

1.  **Configuración vía Modelfile:** Los parámetros de comportamiento (temperatura, system prompts, stops) residen en `/config/ia/ollama/*.Modelfile`. 
    - `ares.Modelfile`: Optimizado para respuesta directa.
    - `ares-think.Modelfile`: Incluye la regla crítica de razonamiento forzado dentro de etiquetas `<think>`.
2.  **Gestión de Pensamientos (Think Tags):**
    - La visibilidad de los pensamientos depende del flag `--think` (CLI) o `/think` (Interactive).
    - **Modelos Pensantes:** Aquellos configurados con capacidad de razonamiento (ej: `ares-think`, `deepseek-r1`). Si el flag está activo, se muestran las etiquetas. Si está inactivo, el sistema las filtra en tiempo real manteniendo el streaming.
    - **Modelos No Pensantes:** Si generan etiquetas vacías o espurias, el sistema las filtra por defecto para mantener la limpieza visual.
3.  **Agnosticismo de Código:** El motor de IA no busca nombres de modelos específicos ("ares", "deepseek") de forma estática. Consulta un mapeo dinámico en la configuración para determinar las capacidades del modelo.

## ⚠️ Bitácora de Errores y Erratas
- **Parser Kùzu:** Rechaza sintaxis compleja. Solución: Atomicidad en queries de Cypher.
- **SyntaxError en main.py:** Causado por exceso de confianza y dejar bloques `try` incompletos.
- **Streaming de Etiquetas:** Corregido implementando un filtro con buffer que maneja fragmentación de chunks.
- **CLI Arg Error:** `--rag` requiere un argumento explícito por diseño de Click.

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

## ⚠️ Bitácora de Errores y Erratas
- **Parser Kùzu:** Rechaza sintaxis compleja. Solución: Atomicidad en queries de Cypher.
- **SyntaxError en main.py:** Causado por exceso de confianza y dejar bloques `try` incompletos.
- **CLI Arg Error:** `--rag` requiere un argumento explícito por diseño de Click.
- **Borrachera de Contexto:** Tratar de resolver todo a la vez sin planificar las partes pequeñas.

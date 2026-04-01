# 📖 LEEME - Módulo RAG V3 (Refactorización Atómica)

## Propósito
Este documento define la estructura y el proceso de trabajo para el sistema RAG. Hemos replanteado el sistema en sus "primitivas" lógicas para asegurar que cada parte funcione bien por sí sola antes de unirlas.

## 🛠️ Proceso Estándar de Trabajo (Protocolo ARES-TRON)
Para garantizar la integridad del sistema, seguimos este protocolo estrictamente:

1.  **Respaldo Pre-Modificación:** `git add . && git commit -m "Backup: [Tarea]"` antes de tocar cualquier código.
2.  **Modificación Atómica:** Solo se modifican o crean funciones pequeñas (máximo 3 por archivo). Deben ser diseñadas como módulos llamables, configurables y reutilizables.
3.  **Verificación Basada en Datos Brutos:** Las comprobaciones NO se basan en interpretaciones subjetivas ("parece que funciona"). Se basan en leer la salida bruta de programas y funciones. Debe existir una conexión inequívoca entre el dato bruto y la salida filtrada.
4.  **Límite de Resolución:** Si tras tres o cuatro iteraciones no se resuelve un error, se detiene la ejecución, se redacta un informe con rutas absolutas y se pide auxilio al usuario.
5.  **Búsqueda de Código Real:** No confiar al 100% en el entrenamiento previo. Buscar ejemplos de documentación oficial, manuales y tutoriales reales. Si se usa tecnología intermedia (SDKs como LangChain para Kùzu), aprovechar su documentación oficial.
6.  **Comprobación de Diferencias:** `git diff` para asegurar que solo modificamos lo que debíamos.
7.  **Respaldo Post-Modificación:** Commit final con la descripción de la mejora.

## 🎯 Paradigma
**Atomicidad Relacionable:** Cada función hace una sola cosa y la hace bien, pero está diseñada para ser interconectada. Foco fijo en el paso particular y foco difuso en la conectividad del sistema total.

## ⚠️ Errores Encontrados (Historial)
- **Kùzu Parser Error:** El parser rechaza sintaxis complejas. Se requiere usar sintaxis oficial verificada para RECURSIVE_REL.
- **CLI Arg Error:** `--rag` requiere un argumento explícito (dataset). El sistema falla en la interfaz de usuario.
- **Auto-engaño del Agente:** No validar contra la salida real del comando final.

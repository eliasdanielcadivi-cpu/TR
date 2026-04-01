# 📖 LEEME - Módulo RAG V3 (Refactorización Atómica)

## Propósito
Este documento define la estructura y el proceso de trabajo para el sistema RAG. Hemos replanteado el sistema en sus "primitivas" lógicas para asegurar que cada parte funcione bien por sí sola antes de unirlas.

## 🛠️ Proceso Estándar de Trabajo
Para garantizar la integridad del sistema ARES-TRON, seguimos este protocolo estrictamente:
1.  **Respaldo Pre-Modificación:** `git add . && git commit -m "Backup: [Tarea]"` antes de tocar cualquier código.
2.  **Modificación Atómica:** Solo se modifican o crean funciones pequeñas (máximo 3 por archivo).
3.  **Verificación Post-Modificación:** Ejecutar la prueba específica del módulo.
4.  **Comprobación de Diferencias:** `git diff` para asegurar que solo modificamos lo que debíamos.
5.  **Respaldo Post-Modificación:** Commit final con la descripción de la mejora.

## ⚠️ Errores Encontrados (Historial)
- **Kùzu Parser Error:** La sintaxis `[*1..3]` fallaba por complejidad excesiva en una sola función. Se requiere división en saltos simples y recursivos.
- **CLI Arg Error:** `--rag` requiere un argumento explícito del dataset (default, skills, etc.).
- **Ollama 500:** Fallos de infraestructura que deben ser manejados por un fallback de embedding robusto y aislado.

## 🎯 Paradigma
**Atomicidad Granular:** Cada función hace una sola cosa y la hace bien. Los módulos son independientes y conceptualmente encapsulados.

# 🤖 PROTOCOLO OPERATIVO DEL KERNEL (V1.1)

El Protocolo Operativo es la ley que rige la interacción entre la **IA Operadora** y el **Ecosistema ARES-TRON**. Ninguna acción puede realizarse sin seguir estas fases.

## ⚖️ AXIOMAS FUNDAMENTALES

1. LEEME.md es la Verdad Única
Si una funcionalidad o módulo no está documentado en el LEEME.md, no existe para el sistema. Este archivo es el reflejo fiel del estado actual del programa.
2. Sincronización mediante el Kernel
No se debe modificar el código y alterar el LEEME.md de forma arbitraria. El proceso debe ser sistemático a través del Kernel:
3. Gestión de TODOs: Toda modificación o nueva funcionalidad debe originarse en un TODO.
4. Estructura por Fases: Cada TODO se desglosa en fases, las cuales representan puntos de prueba de una funcionalidad terminada o una parte razonablemente funcional y verificable.
5. Composición de Fases: Cada fase está integrada por un conjunto de tareas específicas.
6. Actualización de la Verdad: La actualización del LEEME.md no es constante ni aleatoria; ocurre exclusivamente al finalizar una fase. Una vez que la funcionalidad supera sus puntos de prueba, el progreso se vuelca al documento principal, asegurando que la "Verdad" se actualice solo con software validado.
7. **Atomicidad Paranoica:** Máximo 3 funciones por archivo. La complejidad se resuelve mediante orquestación, no mediante archivos gigantes.
8. **Precedencia de Contexto:** Las instrucciones en `GEMINI.md` / `IA-MEMORY.md` invalidan cualquier preferencia general de la IA.

---

## 🛤️ EL CAMINO DE LA IA (FASE DE GUERRA)

### 1. FASE DE INVESTIGACIÓN (RESEARCH)
- **Análisis de Intención:** Ampliar la petición del usuario para entender el "por qué" y el "para qué".
- **SOTA (State of the Art):** Buscar soluciones modernas y eficientes antes de escribir código.
- **Auditoría Local:** Buscar patrones similares en `modules/` o `scripts/` para mantener la coherencia.

### 2. FASE DE PLANIFICACIÓN (STRATEGY)
- **TODO Lógico:** Crear un archivo en `docs/TODO/TODO-$NAME-$Date.md`.
- **Secuencia Temporal:** El plan debe ser descriptivo y seguir un orden lógico (qué va primero, qué va después).
- **Aprobación:** Mostrar el plan al usuario antes de proceder si la tarea es de alta complejidad.
- Existen dos tipos de TODO el de la herramienta de la ia (interno) y el físico que la ia crea un .md el TODO interno se va actualizando conforma avanza la ia en sus tareas pero el TODO .md por fases al igual que el léeme.

### 3. FASE DE EJECUCIÓN (ACT)
- **Implementación Atómica:** Crear módulos en `modules/` siguiendo la plantilla estándar.
- **Blindaje de Configuración:** Si se edita el sistema, activar la skill `sys-config` para crear respaldos.
- **Comentarios Relevantes:** El código debe comentar los problemas difíciles, no lo evidente.

### 4. FASE DE VALIDACIÓN (VALIDATE)
- **Git Diff:** Obligatorio después de cada cambio CRUD.
- **Doble Perspectiva:** Validar técnicamente (logs/compilación) y estructuralmente (integridad del árbol).
- **Consistencia:** Actualizar `LEEME.md` y la `agenda.md` del sistema.

---

## 🚫 PROHIBICIONES CRÍTICAS
- **No duplicar lógica:** Si ya existe un módulo que hace algo, úsalo o extiéndelo.
- **No borrar rutas duras:** El Kernel depende de la estabilidad de `@SKILLS` y `@MEMORY`.
- **No actuar sin plan:** Una IA que escribe código sin un `TODO` en `docs/TODO/` está violando el Kernel.

**Protocolo Generado por el Kernel.**

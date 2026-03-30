# skill-dev.dsl.md (Kernel V1.1)
# Purpose: Desarrollo de módulos atómicos y orquestación por fases
# Goal: Sincronización de la Verdad (LEEME.md) mediante software validado.

skill: "dev"
trigger: ["desarrolla", "nuevo módulo", "crea"]

logic:
  pre:
    ;; 1. INVESTIGACIÓN (RESEARCH)
    - (analizar_intencion "Para qué sirve este módulo?")
    - (auditar_local "Existen módulos similares en modules/ o herramientas/?")
    - (investigar_sota "Mejor enfoque técnico actual")

  proc:
    ;; 2. PLANIFICACIÓN (STRATEGY)
    - (todo_interno "Lista rápida de pasos técnicos para la IA")
    - (crear_todo_fisico "docs/TODO/TODO-$NAME-$DATE.md" 
        (desglose_por_fases "Fases funcionales con puntos de prueba"))

    ;; 3. EJECUCIÓN (ACT)
    - (implementacion_atomica 
        (limit "3 funciones por archivo")
        (location "modules/ o src/")
        (rules "S-expressions, YAML o Python según proyecto"))

    ;; 4. VALIDACIÓN (VALIDATE)
    - (git_diff "Validación técnica de cambios CRUD")
    - (test_fase "Verificar puntos de prueba de la fase actual")

  post:
    ;; 5. SINCRONIZACIÓN DE LA VERDAD
    - (if (fase_completada)
        (seq 
          (actualizar_leeme "Reflejar progreso solo de software validado")
          (sincronizar_agenda "Vincular con agenda.md y gantt-cli")
          (msg "Fase cerrada: Verdad Única actualizada en LEEME.md"))
        (msg "Tarea completada: Pendiente cierre de fase para actualizar LEEME.md"))

outputs:
  phase_status: "in_progress | completed"
  truth_sync: "boolean"
  artifact: "modules/$name.py"

# Garantía del Kernel
guarantee: "Software validado antes de ser verdad documental."

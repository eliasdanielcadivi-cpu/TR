# skill-ciclo-vida.dsl.md
# Purpose: Meta-Skill de Orquestación del Ciclo de Vida del Proyecto (init → dev → prod → maint)
# Goal: Control unificado de tareas mediante agenda como elemento ordinario de seguimiento

skill: "ciclo-vida"
trigger: ["ciclo de vida", "proyecto", "fases", "seguimiento proyecto", "estado proyecto", "timeline proyecto"]
inputs:
  proyecto: { type: string, req: true, desc: "Nombre del proyecto (TR, AGENDA, Agente-De-Cambio-Estable, etc.)" }
  accion: { type: enum, options: [iniciar, desarrollar, producir, mantener, estado, sincronizar], req: false }

logic:
  pre:
    - (assert (exists? "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"))
    - (assert (exists? "/home/daniel/tron/programas/TR/LEEME.md"))

  proc:
    - (context
        (local-purpose "Orquestación del ciclo de vida del proyecto con agenda como control ordinario")
        (inherit-from "@MEMORY")
        (flow "init → dev → prod → maint (agenda sincroniza tareas en gantt-cli)"))

    - (load_subskill "agenda") ;; Carga skill-agenda.dsl.md para gestión de tareas

    - (switch $accion
        (case "iniciar"
            (load_subskill "init")
            (agenda_add_tarea $proyecto "FASE 1: Inicialización" "Estructura Tree-L3")
            (gantt_update_progress $proyecto "FASE 1 — ENTORNO" 100))

        (case "desarrollar"
            (load_subskill "dev")
            (agenda_add_tarea $proyecto "FASE 2: Desarrollo" "Creación de módulos atómicos")
            (gantt_update_progress $proyecto "FASE 2 — PERCEPCIÓN" 50))

        (case "producir"
            (load_subskill "prod")
            (agenda_add_tarea $proyecto "FASE 3: Producción" "Globalización a /usr/bin")
            (gantt_update_progress $proyecto "FASE 3 — COGNICIÓN" 100))

        (case "mantener"
            (load_subskill "maint")
            (agenda_add_tarea $proyecto "FASE 4: Mantenimiento" "Adaptación, papelera, recuperación")
            (gantt_update_progress $proyecto "FASE 4 — EJECUCIÓN" 0))

        (case "estado"
            (cmd "agenda --gantt $proyecto")
            (gantt_get_status $proyecto))

        (case "sincronizar"
            (cmd "agenda --actualizar-desde-gantt")
            (msg "Agenda sincronizada con gantt-cli"))

        (case null
            (mostrar_ciclo_completo $proyecto))
      )

  post:
    - (require (git_diff post_op))
    - (log_state "Ciclo de vida $accion ejecutado en $proyecto")

outputs:
  ciclo:
    fases:
      - nombre: "FASE 1: Inicialización"
        skill: "init"
        agenda_marker: "FASE 1 — ENTORNO"
        gantt_progress: 100
        tareas: ["Estructura Tree-L3", "LEEME.md", "Protocolos"]

      - nombre: "FASE 2: Desarrollo"
        skill: "dev"
        agenda_marker: "FASE 2 — PERCEPCIÓN"
        gantt_progress: 50
        tareas: ["Módulos atómicos (max 3 funcs)", "docs/TODO", "Git diff"]

      - nombre: "FASE 3: Producción"
        skill: "prod"
        agenda_marker: "FASE 3 — COGNICIÓN"
        gantt_progress: 100
        tareas: ["Globalización /usr/bin", "LEEME.md [PROD]", "Verificación"]

      - nombre: "FASE 4: Mantenimiento"
        skill: "maint"
        agenda_marker: "FASE 4 — EJECUCIÓN"
        gantt_progress: 0
        tareas: ["Adaptar", "Papelera", "Recuperar", "Documentar"]

proyectos_activos:
  TR:
    ruta: "/home/daniel/tron/programas/TR"
    fase_actual: "FASE 3 — COGNICIÓN (Apollo RAG)"
    agenda_sync: true
    gantt_config: "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"

  AGENDA:
    ruta: "/home/daniel/tron/programas/AGENDA"
    fase_actual: "FASE 4 — EJECUCIÓN (50%)"
    agenda_sync: true
    gantt_config: "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"

  Agente-De-Cambio-Estable:
    ruta: "/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable"
    fase_actual: "FASE 3 — COGNICIÓN (HITO 2 COMPLETADO)"
    agenda_sync: true
    gantt_config: "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"

protocol:
  sincronizacion:
    - (on-init-complete
        (agenda_add_fase "FASE 1 — ENTORNO" 100)
        (gantt_set_progress "FASE 1" 100))
    - (on-dev-start
        (agenda_add_fase "FASE 2 — PERCEPCIÓN" 0)
        (gantt_set_progress "FASE 2" 0))
    - (on-dev-module-complete
        (agenda_add_tarea "Módulo $name completado")
        (gantt_update_task $name 100))
    - (on-prod-complete
        (agenda_add_fase "FASE 3 — COGNICIÓN" 100)
        (gantt_set_progress "FASE 3" 100))
    - (on-maint-action
        (agenda_log_maint $action)
        (gantt_log_maint $action))

  reconciliacion:
    - (daily-sync
        (cmd "agenda --actualizar-desde-gantt")
        (llm_compare "agenda.md vs version_discreta")
        (llm_reconcile "cambios del usuario"))

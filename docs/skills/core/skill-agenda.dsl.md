# skill-agenda.dsl.md
# Purpose: Sistema de agenda con flujo bidireccional gantt-cli (Verified Tree-L3)
# Goal: Gestión de proyectos con timeline, reconciliación LLM ↔ gantt-cli

skill: "agenda"
trigger: ["agenda", "gantt", "proyectos", "tareas", "timeline"]
inputs:
  action: { type: enum, options: [actualizar, reconciliar, gantt-cli, extraer, help], req: false }
  proyecto: { type: string, desc: "Nombre del proyecto (TR, AGENDA, Agente-De-Cambio-Estable)" }

logic:
  pre:
    - (assert (exists? "/home/daniel/tron/programas/AGENDA/main.py"))
    - (assert (exists? "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"))

  proc:
    - (context
        (local-purpose "Sistema de agenda con flujo bidireccional gantt-cli ↔ agenda.md")
        (inherit-from "@MEMORY")
        (flow "gantt-cli JSON → agenda --actualizar-desde-gantt → agenda.md → LLM lee → actualiza JSON"))

    - (switch $action
        (case "actualizar"
            (cmd "agenda --actualizar-desde-gantt")
            (msg "agenda.md actualizada desde gantt-cli"))

        (case "reconciliar"
            (cmd "agenda --reconciliar")
            (msg "Diff generado para reconciliación LLM"))

        (case "gantt-cli"
            (cmd "agenda --gantt-cli")
            (msg "TUI de gantt-cli lanzada"))

        (case "extraer"
            (cmd "agenda --extraer-tareas")
            (msg "Tareas pendientes extraídas"))

        (case "help"
            (cmd "agenda --help")
            (msg "Ayuda de agenda mostrada"))

        (case null
            (cmd "agenda")
            (msg "Agenda visualizada"))
      )

  post:
    - (require (git_diff post_op))
    - (log_state "Agenda action $action executed")

outputs:
  agenda_state:
    proyectos: ["TR", "Agente-De-Cambio-Estable", "AGENDA"]
    flujo: "bidireccional: gantt-cli ↔ agenda.md (LLM reconcilia)"
    comandos:
      - "agenda --actualizar-desde-gantt"
      - "agenda --reconciliar"
      - "agenda --gantt-cli"
      - "agenda --extraer-tareas"
      - "agenda --help"

proyectos:
  TR:
    ruta: "/home/daniel/tron/programas/TR"
    fases_completadas: ["FASE 0 — APOLLO DB", "FASE 1 — APOLLO INGESTA"]
    en_progreso: ["FASE 2 — APOLLO RETRIEVAL (50%)"]
    proximas: ["Pruebas Apollo", "MODEL CREATOR", "CRM BÁSICO", "NEWS ENGINE", "COMERCIALIZACIÓN"]
    gantt_config: "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"

  Agente-De-Cambio-Estable:
    ruta: "/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable"
    fases_completadas: ["FASE 1 — ENTORNO TUI", "FASE 2 — PERCEPCIÓN", "FASE 3 — COGNICIÓN"]
    en_progreso: []
    proximas: ["FASE 4 — EJECUCIÓN", "Integrar Socket.IO", "FASE 5 — CONECTIVIDAD", "PRODUCCIÓN"]
    gantt_config: "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"

  AGENDA:
    ruta: "/home/daniel/tron/programas/AGENDA"
    fases_completadas: ["FASE 1 — ENTORNO", "FASE 2 — PERCEPCIÓN", "FASE 3 — COGNICIÓN"]
    en_progreso: ["FASE 4 — EJECUCIÓN (50%)"]
    proximas: ["FASE 5 — CONECTIVIDAD", "FASE 6 — PRODUCCIÓN"]
    gantt_config: "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"

protocol:
  reconciliacion:
    - (on-agenda-edit
        (llm_read "agenda.md")
        (llm_read ".version_discreta/agenda_generada.md")
        (llm_compare "inferencial")
        (llm_update_gantt "progress: 0→100"))
  actualizacion:
    - (on-gantt-change
        (cmd "agenda --actualizar-desde-gantt")
        (insert_between_markers)
        (save_version_discreta))

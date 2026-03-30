# skill-agenda.dsl.md
# Purpose: Sistema de agenda con flujo bidireccional (ARES-OS Standard)
# Logic: gantt-cli JSON ↔ agenda.md ↔ IA-Reconciler

skill: "agenda"
trigger: ["agenda", "gantt", "proyectos", "tareas", "timeline", "reconciliar"]
inputs:
  action: { type: enum, options: [actualizar, reconciliar, gantt-cli, extraer, sync], default: actualizar }
  proyecto: { type: string, desc: "Proyecto destino (TR, AGENDA, Agente-De-Cambio-Estable, etc.)" }

logic:
  pre:
    - (assert (exists? "/home/daniel/tron/programas/AGENDA/main.py"))
    - (assert (exists? "/home/daniel/tron/programas/AGENDA/gantt-cli/config/projects.json"))
    - (backup "agenda.md")

  proc:
    - (context
        (local-purpose "Orquestación bidireccional del estado del sistema")
        (inherit-from "@MEMORY")
        (protocol "ARES-AGENDA-V1"))

    - (switch $action
        (case "actualizar"
            ;; Flujo: JSON -> MD
            (cmd "agenda --actualizar-desde-gantt")
            (read "agenda.md")
            (msg "Agenda sincronizada desde el estado de los proyectos."))

        (case "reconciliar"
            ;; Flujo: MD -> IA -> JSON
            (read "agenda.md")
            (llm_inference "Detect changes in status, dates, or phases")
            (cmd "agenda --reconciliar")
            (msg "Iniciando proceso de reconciliación inferencial."))

        (case "sync"
            ;; Ciclo Completo
            (cmd "agenda --actualizar-desde-gantt")
            (read "agenda.md")
            (llm_reflect "Is the agenda aligned with the user intent?")
            (if (not aligned)
                (exec (prompt_user "Detecto discrepancias. ¿Deseas reconciliar el JSON con tus notas?")))
            (cmd "git diff agenda.md"))

        (case "gantt-cli"
            (cmd "agenda --gantt-cli")
            (msg "Lanzando TUI de gestión de proyectos."))

        (case "extraer"
            (cmd "agenda --extraer-tareas")
            (msg "Generando lista de tareas pendientes para el contexto actual."))
      )

  post:
    - (require (git_diff post_op))
    - (log_state "ARES Agenda synchronized: $action")

outputs:
  json: { status: "success", flow: "bidirectional", last_op: $action }

# Proyectos Registrados (Dinámico vía Kernel)
proyectos:
  TR: "/home/daniel/tron/programas/TR"
  Agente-De-Cambio-Estable: "/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable"
  AGENDA: "/home/daniel/tron/programas/AGENDA"

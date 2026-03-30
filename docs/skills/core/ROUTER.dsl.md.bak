# ROUTER.dsl.md (Category: core)
# Purpose: Orchestrate System-Level Skills (Meta-Knowledge)
# Goal: Kernel, Init, Session, Agenda, and Project Lifecycle Management

(context
  (local-purpose "System Meta-Knowledge, Initialization, Lifecycle, Project Management, and Agenda")
  (inherit-from "@MEMORY"))

sub-skills:
  kernel:
    ref: "skill-system-kernel.dsl.md"
    caps: ["sys-audit", "sys-resolve", "sys-recover"]
    trig: ["sys", "kernel", "audit", "resolve"]

  init:
    ref: "skill-init.dsl.md"
    caps: ["project-init", "ares-structure", "leeme-gen"]
    trig: ["init", "start", "proyecto"]

  dev:
    ref: "skill-dev.dsl.md"
    caps: ["module-dev", "todo-logic", "git-diff"]
    trig: ["desarrolla", "nuevo módulo", "crea"]

  prod:
    ref: "skill-prod.dsl.md"
    caps: ["globalize-bin", "ini-deploy", "usr-bin"]
    trig: ["prod", "deploy", "globalizar"]

  maint:
    ref: "skill-maint.dsl.md"
    caps: ["module-maint", "trash-bin", "module-split"]
    trig: ["maint", "fix", "mantenimiento"]

  session:
    ref: "skill-session.dsl.md"
    caps: ["kitty-session", "save-tabs", "restore-state"]
    trig: ["gs", "session", "sesion"]

  agenda:
    ref: "skill-agenda.dsl.md"
    caps: ["gantt-management", "project-timeline", "task-reconciliation"]
    trig: ["agenda", "gantt", "proyectos", "tareas", "timeline"]

  ciclo-vida:
    ref: "skill-ciclo-vida.dsl.md"
    caps: ["lifecycle-orchestration", "init-dev-prod-maint", "agenda-sync"]
    trig: ["ciclo de vida", "proyecto", "fases", "seguimiento proyecto", "estado proyecto"]

logic:
  (match-intent $query
    (case (in_trig? "kernel") (load $kernel))
    (case (in_trig? "init") (load $init))
    (case (in_trig? "dev") (load $dev))
    (case (in_trig? "prod") (load $prod))
    (case (in_trig? "maint") (load $maint))
    (case (in_trig? "session") (load $session))
    (case (in_trig? "agenda") (load $agenda))
    (case (in_trig? "ciclo") (load $ciclo-vida))
  )

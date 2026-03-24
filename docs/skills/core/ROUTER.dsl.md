# ROUTER.dsl.md (Category: core)
# Purpose: Orchestrate System-Level Skills (Meta-Knowledge)
# Goal: Kernel, Init, Session, and Agenda Management

(context
  (local-purpose "System Meta-Knowledge, Initialization, Lifecycle, and Project Management")
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

  maint:
    ref: "skill-maint.dsl.md"
    caps: ["module-maint", "trash-bin", "module-split"]
    trig: ["maint", "fix", "mantenimiento"]

  prod:
    ref: "skill-prod.dsl.md"
    caps: ["globalize-bin", "ini-deploy", "usr-bin"]
    trig: ["prod", "deploy", "globalizar"]

  session:
    ref: "skill-session.dsl.md"
    caps: ["kitty-session", "save-tabs", "restore-state"]
    trig: ["gs", "session", "sesion"]

  agenda:
    ref: "skill-agenda.dsl.md"
    caps: ["gantt-management", "project-timeline", "task-reconciliation"]
    trig: ["agenda", "gantt", "proyectos", "tareas", "timeline"]

logic:
  (match-intent $query
    (case (in_trig? "kernel") (load $kernel))
    (case (in_trig? "init") (load $init))
    (case (in_trig? "maint") (load $maint))
    (case (in_trig? "prod") (load $prod))
    (case (in_trig? "session") (load $session))
    (case (in_trig? "agenda") (load $agenda))
  )

# INDEX.dsl.md
# Purpose: Master Router of the Skills Library (Arsenal)
# Goal: Prevent "Sub-Router Blindness" via Semantic Signatures

(context
  (local-purpose "Procedural Knowledge Arsenal Index")
  (inherit-from "@MEMORY"))

arsenal:
  dev:
    router: "@SKILLS/dev/ROUTER.dsl.md"
    caps: ["mcp-server", "webapp-testing", "frontend-design", "web-artifacts"]
    trig: ["desarrollo", "api", "ui", "react"]

  doc-proc:
    router: "@SKILLS/doc-processing/ROUTER.dsl.md"
    caps: ["docx-redlining", "pdf-forms", "ooxml-unpack"]
    trig: ["word", "pdf", "ooxml", "documentos"]

  office:
    router: "@SKILLS/office/ROUTER.dsl.md"
    caps: ["pptx-slides", "xlsx-formulas", "pptx-thumbnails"]
    trig: ["excel", "powerpoint", "slides", "ofimatica"]

  multimedia:
    router: "@SKILLS/multimedia/ROUTER.dsl.md"
    caps: ["algorithmic-art", "gif-creation", "p5js"]
    trig: ["video", "arte", "gif", "animacion"]

  ia:
    router: "@SKILLS/ia/ROUTER.dsl.md"
    caps: ["skill-creator", "skill-packager"]
    trig: ["meta", "crear skill", "ia"]

  design:
    router: "@SKILLS/design/ROUTER.dsl.md"
    caps: ["branding", "typography", "color-themes"]
    trig: ["diseño", "fuentes", "marca"]

  comms:
    router: "@SKILLS/comms/ROUTER.dsl.md"
    caps: ["newsletter-creation", "faq-management", "corporate-comms"]
    trig: ["newsletter", "faq", "comunicacion"]

  core:
    router: "@SKILLS/core/ROUTER.dsl.md"
    caps: ["system-kernel", "initialization", "session-mgmt", "agenda-gantt", "ciclo-vida"]
    trig: ["kernel", "sys", "init", "sesion", "agenda", "gantt", "ciclo de vida", "proyecto"]

logic:
  (on-intent $query
    (match (or (in_trig? $query) (in_caps? $query))
      (then (load-router $router))
      (else (fail "No skill category found. Try 'kernel audit'"))))

protocol:
  expansion:
    - (on-new-skill
        (register-in-subrouter $parent_router)
        (update-signatures-in-master @SKILLS/INDEX.dsl.md))
  maintenance:
    - (on-modify
        (exec "python3 core/sys_kernel.py pulse")
        (notify-parent $new_hash))
  consistency:
    - (daily-audit (exec "python3 core/sys_kernel.py audit"))

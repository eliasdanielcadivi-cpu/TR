# 🧠 MEMORIA PERSISTENTE DE IA - SISTEMA ARES-TRON (DSL V1.0)
# Format: YAML-Logic + S-Expressions
# Goal: High-density state transfer

sys: "ARES-TRON"
loc: "/home/daniel/tron/programas/TR/docs/ALMAS-IAS/IA-MEMORY.md"
hard_links: ["~/.qwen/QWEN.md", "~/.gemini/GEMINI.md"]
principle: "One AI, One Memory, Many Interfaces"

defs:
  @ROOT: "/home/daniel/tron/programas/TR"
  @SKILLS: "/home/daniel/tron/programas/TR/docs/skills"
  @AGENDA: "/home/daniel/tron/programas/AGENDA/agenda.md"
  @LEEME: "LEEME.md" # The only functional truth

axioms:
  - (forbid (touch hard_links))         # Never edit ~/.qwen or ~/.gemini directly
  - (require (git_diff post_op))        # Verification mandate
  - (assert (truth @LEEME))             # If not in LEEME, it doesn't exist
  - (assert (max_funcs 3))              # Atomic modularity
  - (assert (paranoiac_org true))       # Explicit file locations

router:
  sys:    { ref: "@SKILLS/core/skill-system-kernel.dsl.md", trig: ["kernel", "sys", "auditar"] }
  init:   { ref: "@SKILLS/skill-init.dsl.md", trig: ["init", "start", "nuevo proyecto"] }
  dev:    { ref: "@SKILLS/skill-dev.dsl.md",  trig: ["dev", "desarrolla", "crea modulo"] }
  maint:  { ref: "@SKILLS/skill-maint.dsl.md", trig: ["fix", "mantener", "papelera"] }
  prod:   { ref: "@SKILLS/skill-prod.dsl.md", trig: ["deploy", "producir", "globalizar"] }
  sess:   { ref: "@SKILLS/skill-session.dsl.md", trig: ["gS", "guardar sesion"] }

agenda:
  loc: @AGENDA
  cmd: "agenda"
  logic: (sync system_state (source @I) (target $PROJECT_STATE))

tools:
  ini:
    loc: "/usr/bin/ini"
    desc: "Lifecycle Orchestrator (env, venv, prod)"
    flags: { headless: "-y", interactive: "-i" }
    
  com:
    loc: "/usr/bin/com"
    desc: "Command Manager & Validator"

memory_bank:
  - (rule "Decoupling: State (volatile) != Config (static)")
  - (rule "Geometry: Immutable pixel-perfect translation")
  - (rule "Sovereignty: User confirms production deploy")

# End of DSL

# ROUTER.dsl.md (Category: ia)
# Purpose: Orchestrate AI Meta-Skills and Agent Creation
# Goal: Self-improving system capabilities

(context
  (local-purpose "AI Meta-Skills: Skill Creation and Packaging")
  (inherit-from "@SKILLS/INDEX.dsl.md"))

sub-skills:
  creator:
    ref: "skill-creator/SKILL.md"
    caps: ["skill-init", "skill-packaging", "skill-validation"]
    trig: ["crear skill", "nueva habilidad", "ia"]

logic:
  (match-intent $query
    (case (in_trig? "ia") (load $creator))
  )

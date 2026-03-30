# ROUTER.dsl.md (Category: comms)
# Purpose: Orchestrate Internal and External Communications
# Goal: Clear, professional corporate messaging

(context
  (local-purpose "Communication Systems: Newsletters, FAQs, Announcements")
  (inherit-from "@SKILLS/INDEX.dsl.md"))

sub-skills:
  internal:
    ref: "internal-comms/SKILL.md"
    caps: ["newsletter-creation", "faq-management", "corporate-comms"]
    trig: ["newsletter", "faq", "comunicacion"]

logic:
  (match-intent $query
    (case (in_trig? "newsletter") (load $internal))
  )

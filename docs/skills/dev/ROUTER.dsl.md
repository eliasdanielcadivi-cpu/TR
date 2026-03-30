# ROUTER.dsl.md (Category: dev)
# Purpose: Orchestrate Software Development Skills
# Goal: Low-redundancy access to coding/testing modules

(context
  (local-purpose "Software Engineering, APIs, and Frontend Orchestration")
  (inherit-from "@SKILLS/INDEX.dsl.md"))

sub-skills:
  mcp:
    ref: "mcp-builder/SKILL.md"
    caps: ["mcp-server-creation", "api-integration", "fastmcp"]
    trig: ["mcp", "server", "sdk"]
    
  test:
    ref: "webapp-testing/SKILL.md"
    caps: ["playwright-automation", "browser-testing", "e2e"]
    trig: ["test", "playwright", "automation"]
    
  ui:
    ref: "frontend-design/SKILL.md"
    caps: ["ui-aesthetic", "no-ai-slop", "react-design"]
    trig: ["ui", "frontend", "design"]
    
  artifact:
    ref: "web-artifacts-builder/SKILL.md"
    caps: ["react-artifacts", "shadcn-bundle", "single-html"]
    trig: ["artifact", "bundle", "shadcn"]

logic:
  (match-intent $query
    (case (in_trig? "mcp") (load $mcp))
    (case (in_trig? "test") (load $test))
    (case (in_trig? "ui") (load $ui))
    (case (in_trig? "artifact") (load $artifact))
  )

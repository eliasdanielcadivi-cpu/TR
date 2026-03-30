# ROUTER.dsl.md (Category: multimedia)
# Purpose: Orchestrate Creative and Multimedia Generation
# Goal: Generative Art, Animation, and Visualization

(context
  (local-purpose "Creative Assets: p5.js and GIF generation")
  (inherit-from "@SKILLS/INDEX.dsl.md"))

sub-skills:
  art:
    ref: "algorithmic-art/SKILL.md"
    caps: ["p5js-generation", "seeded-randomness", "interactive-html"]
    trig: ["art", "p5js", "generative"]
    
  gif:
    ref: "slack-gif-creator/SKILL.md"
    caps: ["gif-easing", "slack-animation", "frame-composition"]
    trig: ["gif", "animation", "slack"]

logic:
  (match-intent $query
    (case (in_trig? ["art", "p5js"]) (load $art))
    (case (in_trig? ["gif", "slack"]) (load $gif))
  )

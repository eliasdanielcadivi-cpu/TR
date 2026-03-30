# ROUTER.dsl.md (Category: design)
# Purpose: Orchestrate Visual Identity and Branding
# Goal: Consistent aesthetics and typography

(context
  (local-purpose "Design Systems: Typography, Themes, Branding")
  (inherit-from "@SKILLS/INDEX.dsl.md"))

sub-skills:
  brand:
    ref: "brand-guidelines/SKILL.md"
    caps: ["branding", "identity", "logos"]
    trig: ["marca", "brand", "identity"]
    
  canvas:
    ref: "canvas-design/SKILL.md"
    caps: ["typography", "fonts", "layout"]
    trig: ["canvas", "font", "fuente"]
    
  themes:
    ref: "theme-factory/SKILL.md"
    caps: ["color-palettes", "themes", "skins"]
    trig: ["tema", "color", "paleta"]

logic:
  (match-intent $query
    (case (in_trig? "branding") (load $brand))
    (case (in_trig? "canvas") (load $canvas))
    (case (in_trig? "tema") (load $themes))
  )

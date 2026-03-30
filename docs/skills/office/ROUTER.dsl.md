# ROUTER.dsl.md (Category: office)
# Purpose: Orchestrate Productivity and Document Automation
# Goal: Error-free Office document manipulation

(context
  (local-purpose "Document Automation: Spreadsheets and Presentations")
  (inherit-from "@SKILLS/INDEX.dsl.md"))

sub-skills:
  excel:
    ref: "xlsx/SKILL.md"
    caps: ["xlsx-formulas", "recalc-libreoffice", "pandas-data"]
    trig: ["excel", "xlsx", "formulas", "datos"]
    
  powerpoint:
    ref: "pptx/SKILL.md"
    caps: ["pptx-slides", "html2pptx", "slide-thumbnails", "ooxml-unpack"]
    trig: ["powerpoint", "pptx", "slides", "presentacion"]

logic:
  (match-intent $query
    (case (in_trig? ["excel", "xlsx"]) (load $excel))
    (case (in_trig? ["powerpoint", "pptx"]) (load $powerpoint))
  )

# ROUTER.dsl.md (Category: doc-proc)
# Purpose: Orchestrate Advanced Document Processing
# Goal: OOXML redlining, PDF manipulation, and extraction

(context
  (local-purpose "Document Engineering: Word (.docx) and PDF")
  (inherit-from "@SKILLS/INDEX.dsl.md"))

sub-skills:
  docx:
    ref: "docx/SKILL.md"
    caps: ["docx-redlining", "ooxml-unpack", "document-inventory"]
    trig: ["word", "docx", "redline", "ooxml"]
    
  pdf:
    ref: "pdf/SKILL.md"
    caps: ["pdf-forms", "text-extraction", "pdf-merging"]
    trig: ["pdf", "form", "ocr", "extraer"]

logic:
  (match-intent $query
    (case (in_trig? ["word", "docx"]) (load $docx))
    (case (in_trig? ["pdf"]) (load $pdf))
  )

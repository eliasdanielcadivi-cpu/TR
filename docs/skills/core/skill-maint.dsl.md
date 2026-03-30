# skill-maint.dsl.md
# Purpose: Maintain existing code (Adapt, Trash, Recover, Split)
# Philosophy: Evolution, not just repair.

skill: "maint"
trigger: ["mantener", "adaptar", "a papelera", "recuperar", "dividir"]
inputs:
  name: { type: string, req: true }
  action: { type: enum, options: [adapt, trash, recover, doc, split] }
  context: { type: string, desc: "Reason for maintenance" }

logic:
  pre:
    - (or (exists? "src/modules/$name") 
          (exists? "Agentes/$name")
          (exists? "papelera/$name*"))

  proc:
    - (switch $action
        (case "adapt"
            (modify "src/modules/$name" $context)
            (validate_3_funcs "src/modules/$name")
            (update "LEEME.md" "[ADAPTED] $name: $context"))
            
        (case "trash"
            (move "src/modules/$name" "papelera/$name_$DATE")
            (write "papelera/$name_$DATE/NOTA.md" $context)
            (update "LEEME.md" "[TRASH] $name: $context"))
            
        (case "recover"
            (read "papelera/$name/NOTA.md")
            (if (allowed? recovery)
                (move "papelera/$name" "src/modules/$name")
                (fail "Recovery forbidden by NOTA.md"))
            (update "LEEME.md" "[RECOVERED] $name"))
            
        (case "doc"
            (write "docs/$name.md" (analyze_complexity $name))
            (append_comment "src/modules/$name" "See docs/$name.md")
            (update "LEEME.md" "[DOC] $name updated"))
            
        (case "split"
            (identify_subfunctions $name)
            (create_modules ["$name_sub1", "$name_sub2"])
            (convert_to_orchestrator "$name")
            (update "LEEME.md" "[SPLIT] $name -> submodules"))
      )

  post:
    - (assert (valid_state "LEEME.md"))
    - (msg_user "Action $action on $name completed.")

outputs:
  json: { state: "ok", action: $action, module: $name }

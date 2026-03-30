# skill-system-kernel.dsl.md
# Purpose: System Meta-Knowledge & BIOS
# Format: YAML-Logic + S-Expressions

skill: "system-kernel"
trigger: ["kernel", "sys", "reparar", "auditar", "donde estoy"]
inputs:
  action: { type: enum, options: [resolve, introspect, audit, recover], req: true }
  target: { type: string, desc: "Symbol or Path" }

logic:
  pre:
    - (assert (exists? "/home/daniel/tron/programas/TR/docs/skills/core/sys_kernel.py"))
  
  proc:
    - (context
        (local-purpose "System integrity and logical routing")
        (inherit-from "IA-MEMORY.md"))

    - (switch $action
        (case "resolve"
            (cmd "python3 core/sys_kernel.py resolve $target"))
            
        (case "introspect"
            (cmd "python3 core/sys_kernel.py introspect $target"))
            
        (case "audit"
            (cmd "python3 core/sys_kernel.py audit"))
            
        (case "recover"
            (msg_user (cmd "python3 core/sys_kernel.py recover $CURRENT_TASK")))
      )

  post:
    - (log_state "Kernel operation $action executed on $target")

outputs:
  json: { status: "ok", result: "$CMD_OUTPUT" }

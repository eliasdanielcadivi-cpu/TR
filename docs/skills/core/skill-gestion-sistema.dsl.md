# skill-gestion-sistema.dsl.md (Kernel V1.1)
# Purpose: Gestión administrativa de Skills y Routers (Interfaz Daniel-IA)
# Goal: Sincronización de estados ON/OFF entre Pseudocódigo y DSL.

skill: "gestion-sistema"
trigger: ["gestionar skill", "activar skill", "desactivar skill", "estado skill"]
inputs:
  skill_name: { type: string, req: true, desc: "Nombre de la habilidad (ej: init, dev, maint)" }
  target_state: { type: string, req: true, enum: ["ON", "OFF"], desc: "Estado deseado" }

logic:
  pre:
    ;; 1. INVESTIGACIÓN BILINGÜE
    - (read "docs/skills/SOPORTE/skills/$skill_name-HUMAN.md")
    - (msg "Leyendo estado actual del soporte humanizado de $skill_name...")

  proc:
    ;; 2. PLAN DE GESTIÓN (TODO INTERNO)
    - (if (eq $target_state "OFF")
        (seq 
          (comment_in_router $skill_name) ;; Desactiva la skill en el router real
          (update_human_status $skill_name "🔴 OFF (Inactiva)")
          (msg "Habilidad $skill_name desactivada en el router.")
        )
        (seq 
          (uncomment_in_router $skill_name) ;; Activa la skill en el router real
          (update_human_status $skill_name "🟢 ON (Activa)")
          (msg "Habilidad $skill_name activada en el router.")
        ))

  post:
    ;; 3. VALIDACIÓN Y SINCRONIZACIÓN
    - (git_diff "ROUTER.dsl.md")
    - (kernel_audit "Verificar integridad del enrutamiento")
    - (msg "Sincronización completada. El backend bilingüe está actualizado.")

outputs:
  current_state: "$target_state"
  router_sync: "boolean"

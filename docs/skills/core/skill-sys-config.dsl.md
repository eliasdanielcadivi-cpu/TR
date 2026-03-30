# skill-metacognicion.dsl.md (Alias: sys-config)
# Purpose: Metacognición y Blindaje del Kernel ARES-TRON
# Goal: Auto-auditoría, Evolución Protegida y Soberanía Arquitectónica.

skill: "metacognicion"
trigger: ["configurar sistema", "editar memoria", "ajustar router", "modificar kernel", "actualizar index", "metacognicion"]
inputs:
  target: { type: string, req: true, desc: "Componente del Kernel a intervenir (@MEMORY, @INDEX, @ROUTER, @KERNEL_DOCS)" }
  reason: { type: string, req: true, desc: "Justificación técnica del cambio (Auditoría de Intención)" }

logic:
  pre:
    ;; 1. FASE DE GUERRA: INVESTIGACIÓN
    - (intent_expansion "Analizar impacto del cambio en el Kernel")
    - (research_local ["docs/KERNEL/", "docs/skills/core/sys_kernel.py"])
    - (backup $target ".bak") ;; Resguardo atómico obligatorio
    - (msg "Metacognición Activa: Resguardo de $target creado. Iniciando fase de planificación.")

  proc:
    ;; 2. FASE DE GUERRA: PLANIFICACIÓN (TODO-LOGIC)
    - (write "docs/TODO/TODO-SYS-CHANGE-$DATE.md" 
        (create_todo 
          (logic "Temporal/Secuencial")
          (description "Plan de modificación del núcleo del sistema")))
    
    - (context
        (local-purpose "Intervención en la estructura soberana del sistema")
        (inherit-from "@MEMORY")
        (protocol "ARES-META-V1"))

    ;; 3. FASE DE GUERRA: ACCIÓN (IMPLEMENTACIÓN)
    - (implementation
        (action "replace") ;; Reemplazo quirúrgico mandatorio
        (rule "Strict adherence to S-expressions & YAML syntax")
        (validation_tool "python3 core/sys_kernel.py audit"))

  post:
    ;; 4. FASE DE GUERRA: VALIDACIÓN (CONSTATACIÓN)
    - (require (cmd "git diff $target"))
    - (vision_constatation
        (tech "Kernel Audit status")
        (structural "Integrity of the routing tree"))
    - (update "LEEME.md" "[META] Kernel evolved: $target modified for $reason")
    - (msg "Metacognición completada: El Kernel ha evolucionado de forma segura.")

outputs:
  evolution_status: "stable"
  backup: "$target.bak"
  audit_log: "docs/KERNEL/LOG-EVOLUCION.md"

# Referencias de Poder
references:
  architecture: "docs/KERNEL/ARQUITECTURA-KERNEL.md"
  protocol: "docs/KERNEL/PROTOCOLO-OPERATIVO.md"
  kernel_tool: "docs/skills/core/sys_kernel.py"

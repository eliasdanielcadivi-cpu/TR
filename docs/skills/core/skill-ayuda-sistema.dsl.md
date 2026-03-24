# skill-ayuda-sistema.dsl.md
# Purpose: Sistema de Ayuda Unificada para todos los programas ARES-TRON
# Goal: Centralizar documentación y ayudar a usuarios/IA a encontrar información

skill: "ayuda-sistema"
trigger: ["ayuda", "help", "--help", "-h", "documentación", "manual"]
inputs:
  programa: { type: string, req: false, desc: "Nombre del programa (agenda, ares, ini, com, etc.)" }
  contexto: { type: string, desc: "Contexto de uso (ciclo-vida, dev, init, prod, maint)" }

logic:
  pre:
    - (assert (exists? "/home/daniel/tron/programas/AYUDA/config.json"))
    - (assert (exists? "/home/daniel/tron/programas/AYUDA/main.py"))

  proc:
    - (context
        (local-purpose "Sistema de ayuda unificado para programas ARES-TRON")
        (inherit-from "@MEMORY")
        (flow "programa --help → ayuda programa → AYUDA/docs/<categoria>/<programa>.md"))

    - (if (eq $programa null)
        (mostrar_meta_ayuda)
        (cargar_ayuda_programa $programa))

    - (if (eq $contexto "ciclo-vida")
        (load_subskill "ciclo-vida")
        (ayuda_contextual "ciclo de vida del proyecto"))

    - (if (eq $contexto "dev")
        (load_subskill "dev")
        (ayuda_contextual "desarrollo de módulos"))

    - (if (eq $contexto "agenda")
        (load_subskill "agenda")
        (ayuda_contextual "gestión de proyectos con gantt-cli"))

  post:
    - (log_state "Ayuda de $programa mostrada")

outputs:
  meta_ayuda:
    descripcion: "Sistema de Ayuda Unificada ARES-TRON"
    comandos:
      - "ayuda <programa>"
      - "<programa> --help"
      - "ayuda --help"
    categorias:
      - TRON: ["agenda", "ares", "multimedia"]
      - SISTEMA: ["menu", "openbox", "zsh"]
      - ADMON: ["ini", "com", "repo"]
      - AGENTES: ["sherlok", "AgenteDeCambio"]
      - PROGRAMAS-PROPIOS: ["aviso"]
      - PLUGINS: ["broot"]

rutas_ayuda:
  agenda: "/home/daniel/tron/programas/AYUDA/docs/TRON/agenda.md"
  ares: "/home/daniel/tron/programas/AYUDA/docs/TRON/ares.md"
  ini: "/home/daniel/tron/programas/AYUDA/docs/ADMON/ini.md"
  com: "/home/daniel/tron/programas/AYUDA/docs/ADMON/com.md"
  menu: "/home/daniel/tron/programas/AYUDA/docs/SISTEMA/menu.md"
  sherlok: "/home/daniel/tron/programas/AYUDA/docs/AGENTES/sherlok.md"
  broot: "/home/daniel/tron/programas/AYUDA/docs/PLUGINS/broot.md"
  leeme: "/home/daniel/tron/programas/TR/LEEME.md"
  index: "/home/daniel/tron/programas/TR/docs/INDEX.md"

protocol:
  integracion:
    - (on-programa-help
        (cmd "ayuda $programa")
        (load_doc $rutas_ayuda.$programa))
    - (on-ciclo-vida-help
        (load_subskill "ciclo-vida")
        (ayuda_contextual "fases: init → dev → prod → maint"))
    - (on-agenda-help
        (load_subskill "agenda")
        (ayuda_contextual "gantt-cli ↔ agenda.md (flujo bidireccional)"))
    - (on-dev-help
        (load_subskill "dev")
        (ayuda_contextual "desarrollo: módulos atómicos, max 3 funcs, git diff"))

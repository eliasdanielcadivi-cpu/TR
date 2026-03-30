# skill-init.dsl.md (Kernel V1.1)
# Purpose: Inicialización de proyectos bajo el estándar ARES-TRON
# Goal: Estructura Tree-L3 Agnóstica y Paranoica.

skill: "init"
trigger: ["inicializa", "nuevo proyecto", "start"]

logic:
  pre:
    - (auditar "Verificar que el directorio actual esté vacío o sea un nuevo @ROOT")
    - (mkdir "docs/TODO")
    - (mkdir "docs/skills")

  proc:
    ;; Estructura Nuclear (Obligatoria)
    - (mkdir "src")       ;; El Orquestador
    - (mkdir "modules")   ;; Lógica Atómica
    - (mkdir "bin")       ;; Lanzadores
    - (mkdir "config")    ;; Configuración estática
    - (mkdir "db")        ;; Persistencia
    - (mkdir "scripts")   ;; Automatizaciones
    - (mkdir "tests")     ;; Validación persistente
    - (mkdir "papelera")  ;; Cementerio con contexto

    ;; Estructura de Inteligencia (Condicional)
    - (if (is_intelligent_project) 
        (seq 
          (mkdir "AGENTES")      ;; Sub-agentes con núcleos LLM
          (mkdir "herramientas") ;; Utilidades para IA sin núcleos propios
        ))

    ;; Inicialización de Verdad Única
    - (write "LEEME.md" 
        (template "Standard LEEME.md: Titulo, Descripción, Fases, Módulos"))

  post:
    - (msg "Proyecto inicializado bajo Kernel V1.1. Estructura Tree-L3 desplegada.")
    - (msg "Siguiente paso: Crear el primer TODO físico en docs/TODO/")

outputs:
  structure: "Tree-L3 (V1.1)"
  status: "Ready for Dev"

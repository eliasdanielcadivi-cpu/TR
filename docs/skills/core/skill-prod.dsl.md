# skill-prod.dsl.md
# Purpose: Globalize functional scripts via TRON `ini`
# Philosophy: User sovereignty, confirmation required.

skill: "prod"
trigger: ["producir", "globalizar", "a /usr/bin", "lanzar"]
inputs:
  name: { type: string, req: true }
  method: { type: enum, options: [auto, manual], default: auto }
  confirm: { type: bool, default: false }

logic:
  pre:
    - (assert (eq $confirm true))
    - (assert (in_LEEME? $name [DEV, ADAPTED]))
    - (not (in_LEEME? $name [TRASH]))
    - (validate_shebang "src/modules/$name/funciones.py")
    - (validate_chmod "src/modules/$name/funciones.py")
    - (validate_help "src/modules/$name/funciones.py")

  proc:
    - (if (eq $method "auto")
        (cmd "ini")
        (cmd "ini -i"))
        
    - (verify [
        (cmd "com ruta $name" -> "/usr/bin/$name"),
        (cmd "$name --help")
      ])
      
    - (update "LEEME.md" "[PROD] $name: Globalized via $method")

  post:
    - (msg_user "Module $name globalized. Execute with '$name'.")

outputs:
  json: { state: "ok", action: "prod", wrapper: "/usr/bin/$name" }

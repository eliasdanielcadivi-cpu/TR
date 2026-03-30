# skill-session.dsl.md
# Purpose: Persist/Restore Kitty Terminal sessions
# Format: JSON Schema for state

skill: "session"
trigger: ["gS", "guardar sesión", "restaurar sesión"]
inputs:
  action: { type: enum, options: [save, restore], default: save }
  name: { type: string, default: "session_$DATE" }

logic:
  pre:
    - (exists? "/tmp/mykitty") ;; Socket check

  proc:
    - (if (eq $action "save")
        (then
          (read_socket "/tmp/mykitty")
          (extract_tree [os_window -> tabs -> title])
          (write "db/$name.json" $state)
        )
        (else ;; restore
          (read "db/$name.json" $state)
          (foreach $window $state
            (create_os_window)
            (foreach $tab $window
              (create_tab $tab.title $tab.cwd)
            )
          )
        )
      )

  post:
    - (msg_user "Session $name $action completed.")

outputs:
  json: { state: "ok", file: "db/$name.json" }

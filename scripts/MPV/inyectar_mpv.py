import os
from pathlib import Path

# Rutas de destino globales para todos los usuarios
MPV_DIR = Path("/etc/mpv")
SCRIPTS_DIR = MPV_DIR / "scripts"

# Contenido del script Lua (fix_subdelay.lua)
LUA_SCRIPT = """--[[
        Guion sencillo para arreglar el retraso de los subtítulos desplazados.

        Primero, avanza cuadro a cuadro hasta donde el subtítulo deseado (letrero) DEBERÍA comenzar, presiona ALT+Z.
        Luego, avanza cuadro a cuadro hasta donde el subtítulo deseado (letrero) REALMENTE comienza, presiona ALT+Z.
        ¡Listo!

        Puedes presionar ALT+Z  Es el Alt izquierdo  dos veces seguidas para poner el retraso de los subtítulos a cero.
]]--
local start_time = nil

function on_script_action()
  local playback_time = mp.get_property_native("playback-time")

  if start_time == playback_time then
        mp.osd_message("Identical frames, clearing sub-delay")
        mp.set_property_native("sub-delay", 0)
        start_time = nil
   
  elseif start_time ~= nil then
        -- Take current sub-delay into account
        local sub_delay = mp.get_property_native("sub-delay")
        local delta = start_time - playback_time + sub_delay
        mp.set_property_native("sub-delay", delta)
        mp.osd_message("Set sub-delay to " .. tostring(delta), 2)
        start_time = nil

  else
        start_time = playback_time
        mp.osd_message("Picked expected frame, now pick the actual frame", 2)
  end
end

mp.add_key_binding("alt+z", "fix_subdelay_action", on_script_action)
"""

# Contenido de los atajos de teclado (input.conf) estilo VLC
INPUT_CONF = """# Controles de Volumen (VLC style)
UP    add volume 5
DOWN  add volume -5

# Controles de Navegación
RIGHT seek 10
LEFT  seek -10

# Velocidad de reproducción
- multiply speed 0.9091
+ multiply speed 1.1

# Pistas multimedia
a cycle audio
s cycle sub

# Navegación cuadro a cuadro
, frame-back-step
. frame-step

# Ciclos Loop (A-B)
[ set ab-loop-a ${=time-pos}
] set ab-loop-b ${=time-pos}
\\ clear-ab-loop

# Captura de pantalla
Ctrl+PRINT screenshot
"""

def inyectar_configuracion():
    print(f"[*] Verificando directorios en {MPV_DIR}...")
    try:
        # Crear directorios si no existen
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Inyectar input.conf
        input_conf_path = MPV_DIR / "input.conf"
        with open(input_conf_path, "w", encoding="utf-8") as f:
            f.write(INPUT_CONF)
        print(f"[+] Archivo inyectado: {input_conf_path}")
        
        # Inyectar script lua
        lua_path = SCRIPTS_DIR / "fix_subdelay.lua"
        if not lua_path.exists():
            with open(lua_path, "w", encoding="utf-8") as f:
                f.write(LUA_SCRIPT)
            print(f"[+] Archivo inyectado: {lua_path}")
        else:
            print(f"[*] El script {lua_path} ya existe. Omitiendo para evitar sobrescritura.")
            
        print("[*] ¡Inyección completada con éxito!")

    except PermissionError:
        print("[!] Error de permisos: Este script debe ejecutarse con 'sudo' para escribir en /etc/mpv/")
    except Exception as e:
        print(f"[!] Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    inyectar_configuracion()

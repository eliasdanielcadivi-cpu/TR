import os
import time
import subprocess

SOCKET = "unix:/tmp/mykitty"
DEBUG_FILE = "/home/daniel/tron/programas/TR/test/zdotdir_debug.txt"

def run_command(cmd_args):
    base_cmd = ["kitty", "@", "--to", SOCKET]
    full_cmd = base_cmd + cmd_args
    subprocess.run(full_cmd, capture_output=True, text=True)

if os.path.exists(DEBUG_FILE): os.remove(DEBUG_FILE)

# Lanzar ares
subprocess.run(["/usr/bin/ares"], check=True)

# Esperar a que el socket esté listo y Kitty cargue el shell
time.sleep(5) 

# Enviar comandos con doble expansión para asegurar que el Shell de Kitty responda
commands = [
    f'echo "SISTEMA: $(uname -a)" > {DEBUG_FILE}',
    f'echo "USUARIO: $(whoami)" >> {DEBUG_FILE}',
    f'echo "ZDOTDIR_REAL: $ZDOTDIR" >> {DEBUG_FILE}',
    f'alias actz >> {DEBUG_FILE} 2>&1',
    f'which actz >> {DEBUG_FILE} 2>&1'
]

for cmd in commands:
    run_command(["send-text", f"{cmd}\n"])
    time.sleep(0.5)

time.sleep(2)

if os.path.exists(DEBUG_FILE):
    with open(DEBUG_FILE, 'r') as f:
        print(f.read())
else:
    print("❌ Error: No se pudo capturar el diagnóstico.")

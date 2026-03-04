import os
import subprocess
from pathlib import Path

def launch_ares(ctx_obj):
    """Lógica de arranque del sistema ARES."""
    title = ctx_obj.config.get('identity', {}).get('window_title', "ARES")
    socket_path = ctx_obj.socket_path
    kitty_conf = ctx_obj.kitty_conf
    socket = ctx_obj.socket

    # Limpieza de socket previo
    if os.path.exists(socket_path):
        os.remove(socket_path)

    # Asegurar inicio en HOME
    os.chdir(os.path.expanduser("~"))
    
    subprocess.run([
        "kitty",
        "--title", title,
        "-c", kitty_conf,
        "--listen-on", socket,
        "--detach"
    ])

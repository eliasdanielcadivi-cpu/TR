import os
import subprocess
import time
import json
from rich.console import Console

console = Console()

class KittyRemote:
    """Funcionalidades 1-3: Diagnóstico, Lanzamiento y Ejecución de Comandos."""
    def __init__(self, ctx):
        self.ctx = ctx

    def is_running(self):
        return os.path.exists(self.ctx.socket_path)

    def launch_hub(self):
        if os.path.exists(self.ctx.socket_path): os.remove(self.ctx.socket_path)
        subprocess.run(["kitty", "-c", self.ctx.kitty_conf, "--listen-on", self.ctx.socket, "--detach"], check=True)
        for _ in range(15):
            if self.is_running():
                time.sleep(2)
                return True
            time.sleep(0.5)
        return False

    def run(self, cmd_args):
        if not self.is_running(): return None
        base_cmd = ["kitty", "@", "--to", self.ctx.socket]
        full_cmd = base_cmd + cmd_args
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None

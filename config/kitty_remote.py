import os
import subprocess
import time
import json
from rich.console import Console

console = Console()

class KittyRemote:
    """Control remoto de Kitty (Diagnóstico, Lanzamiento, Ejecución)."""
    def __init__(self, ctx):
        self.ctx = ctx

    def is_running(self):
        return os.path.exists(self.ctx.socket_path)

    def launch_hub(self):
        """
        Lanza kitty con título fijo de ventana 'Ares por Daniel Hung'.
        """
        if os.path.exists(self.ctx.socket_path):
            os.remove(self.ctx.socket_path)
        
        # Leer título desde config si es posible, sino default
        title = self.ctx.config.get('identity', {}).get('window_title', "Ares por Daniel Hung")

        # Inyectar ZDOTDIR para soberanía de Zsh (Configuración encapsulada en TR)
        env = os.environ.copy()
        env["ZDOTDIR"] = os.path.join(self.ctx.base_path, "config/zsh")

        subprocess.run([
            "kitty",
            "-c", self.ctx.kitty_conf,
            "--listen-on", self.ctx.socket,
            "--detach",
            "--title", title
        ], env=env, check=True)
        
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

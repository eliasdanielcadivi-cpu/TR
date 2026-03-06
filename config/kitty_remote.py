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
        """Verifica si el socket existe y responde."""
        if not os.path.exists(self.ctx.socket_path):
            return False
        # Prueba de conexión rápida
        res = subprocess.run(
            ["kitty", "@", "--to", self.ctx.socket, "ls"],
            capture_output=True, text=True, timeout=1
        )
        return res.returncode == 0

    def launch_hub(self):
        """
        Lanza kitty con título fijo y configuración TRON.
        """
        # Limpieza agresiva de socket huérfano
        if os.path.exists(self.ctx.socket_path):
            try:
                os.remove(self.ctx.socket_path)
            except OSError:
                pass
        
        title = self.ctx.config.get('identity', {}).get('window_title', "Ares por Daniel Hung")
        env = os.environ.copy()
        env["ZDOTDIR"] = os.path.join(self.ctx.base_path, "config/zsh")

        # Lanzar proceso desacoplado
        subprocess.Popen([
            "kitty",
            "-c", self.ctx.kitty_conf,
            "--listen-on", self.ctx.socket,
            "--title", title
        ], env=env, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Esperar a que el socket se cree y responda
        for _ in range(10):
            if self.is_running():
                return True
            time.sleep(0.5)
        return False

    def run(self, cmd_args):
        if not self.is_running(): return None
        base_cmd = ["kitty", "@", "--to", self.ctx.socket]
        full_cmd = base_cmd + cmd_args
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None

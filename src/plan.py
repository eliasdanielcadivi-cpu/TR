import os
import time
from rich.console import Console

console = Console()

class TacticalOrchestrator:
    """Funcionalidades 1-3: Handshake, Lanzamiento de Pestañas Inteligentes y Multimedia (Video/Imagen)."""
    def __init__(self, kitty, ctx):
        self.kitty = kitty
        self.ctx = ctx

    def launch_smart(self, title, color, cmd):
        """Lanza y configura una pestaña."""
        win_id = self.kitty.run(["launch", "--type=tab", "--tab-title", title])
        if not win_id: return
        time.sleep(0.8)
        self.kitty.run(["set-tab-color", "--match", f"id:{win_id}", f"background={color}"])
        time.sleep(0.8)
        # Usamos doble escape para el retorno de carro en f-strings
        self.kitty.run(["send-text", "--match", f"id:{win_id}", f"{cmd}\r"])

    def deploy_plan(self):
        """Ejecuta el plan maestro."""
        if os.path.exists(self.ctx.handshake_file): os.remove(self.ctx.handshake_file)
        console.print("[bold green]🛰  Desplegando Plan Tron Modular...")

        self.launch_smart("TRON-HUB", "#39ff14", f"echo 'ALIVE' > {self.ctx.handshake_file}; echo '--- Tron Hub Online ---';")
        self.launch_smart("DIAG", "#00d7ff", "echo 'RECURSOS:'; ls -F; df -h; free -m;")
        
        v_path = "/home/daniel/Descargas/The Pendragon Cycle Rise Of The Merlin S01E03 E3 A Fatherless Child 1080p DLWP WEB-DL AAC2 0 H 264-DJT[EZTVx.to].mkv"
        self.launch_smart("VIDEO", "#ff0000", f"~/tron/programas/TR/bin/tr-video \"{v_path}\"")
        
        i_path = f"{self.ctx.base_path}/assets/2026-02-26_12-48.png"
        self.launch_smart("IMAGEN", "#ff00ff", f"kitty +kitten icat \"{i_path}\"")

        time.sleep(1.5)
        return os.path.exists(self.ctx.handshake_file)

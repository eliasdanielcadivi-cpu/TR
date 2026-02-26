#!/usr/bin/env python3
import click
import subprocess
import os
import time
from rich.console import Console

console = Console()

class TRContext:
    def __init__(self):
        self.base_path = os.path.expanduser("~/tron/programas/TR")
        self.socket = "unix:/tmp/mykitty"
        self.socket_path = "/tmp/mykitty"
        self.handshake_file = "/tmp/tron_handshake.txt"
        self.kitty_conf = f"{self.base_path}/config/kitty.conf"

class KittyRemote:
    def __init__(self, ctx):
        self.ctx = ctx

    def is_running(self):
        return os.path.exists(self.ctx.socket_path)

    def run(self, cmd_args):
        if not self.is_running(): return None
        base_cmd = ["kitty", "@", "--to", self.ctx.socket]
        full_cmd = base_cmd + cmd_args
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout.strip()

@click.group()
def cli(): pass

@cli.command()
def plan():
    ctx = TRContext()
    kitty = KittyRemote(ctx)
    
    if os.path.exists(ctx.handshake_file): os.remove(ctx.handshake_file)
    
    console.print("[bold green]🛰  Desplegando Plan Tron con Estética Reforzada...")

    def launch_smart(title, color, cmd):
        # Lanzamos pestaña
        res = kitty.run(["launch", "--type=tab", "--tab-title", title])
        if not res: return
        time.sleep(0.7)
        # Pintamos con color HEX brillante
        kitty.run(["set-tab-color", "--match", f"title:{title}", f"background={color}"])
        time.sleep(0.7)
        # Inyectamos comando
        kitty.run(["send-text", "--match", f"title:{title}", f"{cmd}\r"])

    # 1. TRON-HUB (VERDE NEÓN)
    launch_smart("TRON-HUB", "#39ff14", f"echo 'HANDSHAKE OK' > {ctx.handshake_file}; echo '--- Tron Hub Online ---';")

    # 2. SISTEMA (AZUL ELÉCTRICO)
    launch_smart("DIAG", "#00d7ff", "echo 'RECURSOS DEL SISTEMA:'; df -h; free -m;")

    # 3. VIDEO-HQ (ROJO SANGRE)
    v_path = "/home/daniel/Descargas/The Pendragon Cycle Rise Of The Merlin S01E03 E3 A Fatherless Child 1080p DLWP WEB-DL AAC2 0 H 264-DJT[EZTVx.to].mkv"
    launch_smart("VIDEO", "#ff0000", f"~/tron/programas/TR/bin/tr-video \"{v_path}\"")

    # 4. IMAGEN (MAGENTA NEÓN)
    i_path = f"{ctx.base_path}/assets/2026-02-26_12-48.png"
    launch_smart("IMAGEN", "#ff00ff", f"kitty +kitten icat \"{i_path}\"")

    time.sleep(1.5)
    if os.path.exists(ctx.handshake_file):
        console.print("[bold green]✔ Plan completado. Fuente 14px y Atajos Konsole activos.")
    else:
        console.print("[bold red]⚠ Falló el handshake. Revisa el socket.")

if __name__ == "__main__":
    cli()

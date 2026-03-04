#!/usr/bin/env python3
import click
import yaml
import subprocess
import os
import sys
import time
from rich.console import Console
from rich.panel import Panel

# TRON: SMART ORCHESTRATOR V3 (NEW INODE)
console = Console()

class TRContext:
    def __init__(self):
        self.base_path = os.path.expanduser("~/tron/programas/TR")
        self.socket = "unix:/tmp/mykitty"
        self.socket_path = "/tmp/mykitty"
        self.kitty_conf = f"{self.base_path}/config/kitty.conf"
        self.handshake_file = f"{self.base_path}/data/handshake.txt"

class KittyRemote:
    def __init__(self, ctx):
        self.ctx = ctx

    def is_running(self):
        return os.path.exists(self.ctx.socket_path)

    def launch_kitty(self):
        console.print("[bold yellow]⚡ Lanzando Hub de Tron (Cyber-Glow)...")
        if os.path.exists(self.ctx.socket_path):
            os.remove(self.ctx.socket_path)
        # Lanzamos kitty con la config WOW
        subprocess.run(["kitty", "-c", self.ctx.kitty_conf, "--listen-on", self.ctx.socket, "--detach"], check=True)
        for _ in range(15):
            if os.path.exists(self.ctx.socket_path):
                time.sleep(2)
                return True
            time.sleep(0.5)
        return False

    def run(self, cmd_args):
        if not self.is_running(): return None
        base_cmd = ["kitty", "@", "--to", self.ctx.socket]
        full_cmd = base_cmd + cmd_args
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout.strip()

@click.group()
def cli():
    pass

@cli.command()
def plan():
    ctx = TRContext()
    kitty = KittyRemote(ctx)
    
    if not kitty.is_running():
        if not kitty.launch_kitty():
            console.print("[bold red]✘ Error crítico: Kitty no respondió.")
            return

    console.print("[bold green]🛰  Iniciando Orquestación Inteligente...")

    def launch_smart(title, color, cmd):
        # 1. Lanzar Pestaña
        kitty.run(["launch", "--type=tab", "--tab-title", title])
        time.sleep(0.7)
        # 2. Pintar Pestaña (set-tab-color)
        kitty.run(["set-tab-color", "--match", f"title:{title}", f"background={color}"])
        time.sleep(0.7)
        # 3. Inyectar Texto
        kitty.run(["send-text", "--match", f"title:{title}", f"{cmd}\r"])

    # Limpiar handshake previo
    if os.path.exists(ctx.handshake_file): os.remove(ctx.handshake_file)

    # EJECUCIÓN TÁCTICA
    launch_smart("TRON-HUB", "green", f"echo 'HANDSHAKE OK' > '{ctx.handshake_file}'; echo '--- Tron Online. Bienvenido Daniel. ---'; ls -F;")
    launch_smart("SISTEMA", "blue", "echo 'Analizando Recursos:'; df -h; free -m; uname -a;")
    
    video_path = "/home/daniel/Descargas/The Pendragon Cycle Rise Of The Merlin S01E03 E3 A Fatherless Child 1080p DLWP WEB-DL AAC2 0 H 264-DJT[EZTVx.to].mkv"
    launch_smart("VIDEO-HQ", "red", f"~/tron/programas/TR/bin/tr-video \"{video_path}\"")
    
    img_path = "/home/daniel/tron/programas/TR/assets/2026-02-26_12-48.png"
    launch_smart("IMAGE-VIEW", "magenta", f"kitty +kitten icat \"{img_path}\"")

    # Validación Inteligente
    time.sleep(1.5)
    if os.path.exists(ctx.handshake_file):
        with open(ctx.handshake_file, 'r') as f:
            console.print(f"[bold green]✔ Handshake Confirmado:[/bold green] {f.read().strip()}")
    else:
        console.print("[bold red]⚠ No se detectó handshake. La orquestación puede haber sido parcial.")

if __name__ == "__main__":
    cli()

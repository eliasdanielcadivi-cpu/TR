#!/usr/bin/env python3
import click
import yaml
import subprocess
import os
import sys
import time
from rich.console import Console

# TRON: CYBER-TACTICAL PLAN (EJECUCIÓN REAL)
console = Console()

class TRContext:
    def __init__(self):
        self.base_path = os.path.expanduser("~/tron/programas/TR")
        self.config_path = f"{self.base_path}/config/config.yaml"
        self.socket = "unix:/tmp/mykitty"
        self.socket_path = "/tmp/mykitty"
        self.kitty_conf = f"{self.base_path}/config/kitty.conf"

class KittyRemote:
    def __init__(self, ctx):
        self.ctx = ctx

    def is_running(self):
        return os.path.exists(self.ctx.socket_path)

    def launch_kitty(self):
        console.print("[bold cyan]⚡ Lanzando Hub de Tron (Cyber-Tactical)...")
        # Forzamos la configuración WOW
        subprocess.run(["kitty", "-c", self.ctx.kitty_conf, "--listen-on", self.ctx.socket, "--detach"], check=True)
        for _ in range(15):
            if os.path.exists(self.ctx.socket_path):
                time.sleep(1.5)
                return True
            time.sleep(0.5)
        return False

    def run(self, cmd_args):
        if not self.is_running(): return None
        base_cmd = ["kitty", "@", "--to", self.ctx.socket]
        full_cmd = base_cmd + cmd_args
        # console.print(f"[dim]DEBUG: {' '.join(full_cmd)}[/dim]")
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[bold red]KITTY ERROR:[/bold red] {result.stderr}")
        return result.stdout.strip()

@click.group()
def cli():
    pass

@cli.command()
def plan():
    ctx = TRContext()
    kitty = KittyRemote(ctx)
    
    # Si Kitty no está abierto con nuestro socket, lo abrimos
    if not kitty.is_running():
        if not kitty.launch_kitty():
            console.print("[red]Error: Kitty no arrancó con WOW Factor.")
            return

    console.print("[bold green]🚀 Desplegando Orquestación Profunda...")

    # 1. TRON-INICIO (Pestaña Verde) - Saludo y Diagnóstico
    kitty.run(["launch", "--type=tab", "--tab-title", "TRON-INICIO", "--tab-bg", "#00ff00", "--tab-fg", "#000000"])
    time.sleep(0.5)
    kitty.run(["send-text", "--match", "title:TRON-INICIO", "echo 'Tron Hub Online. Bienvenido Daniel.'; ls -F; uname -a;\r"])

    # 2. SISTEMA (Pestaña Azul) - Cadena de comandos real
    kitty.run(["launch", "--type=tab", "--tab-title", "DIAG-SISTEMA", "--tab-bg", "#0000ff"])
    time.sleep(0.5)
    # Comando;comando;comando;comando real
    cmd_chain = "echo 'Analizando recursos...'; df -h; free -m; ps aux | head -n 5; echo 'Listo.';"
    kitty.run(["send-text", "--match", "title:DIAG-SISTEMA", f"{cmd_chain}\r"])

    # 3. VIDEO-HQ (Pestaña Roja) - mpv con Merlín
    video_path = "/home/daniel/Descargas/The Pendragon Cycle Rise Of The Merlin S01E03 E3 A Fatherless Child 1080p DLWP WEB-DL AAC2 0 H 264-DJT[EZTVx.to].mkv"
    if os.path.exists(video_path):
        video_cmd = f"~/tron/programas/TR/bin/tr-video \"{video_path}\""
        kitty.run(["launch", "--type=tab", "--tab-title", "MULTIMEDIA-HQ", "--tab-bg", "#ff0000"])
        time.sleep(0.5)
        kitty.run(["send-text", "--match", "title:MULTIMEDIA-HQ", f"{video_cmd}\r"])
    else:
        console.print(f"[yellow]⚠ Video no encontrado en: {video_path}[/yellow]")

    # 4. IMAGEN-VIEW (Pestaña Magenta) - icat
    img_path = "/home/daniel/tron/programas/TR/assets/2026-02-26_12-48.png"
    if os.path.exists(img_path):
        kitty.run(["launch", "--type=tab", "--tab-title", "IMAGEN", "--tab-bg", "#ff00ff"])
        time.sleep(0.5)
        kitty.run(["send-text", "--match", "title:IMAGEN", f"kitty +kitten icat \"{img_path}\"\r"])
    else:
        console.print(f"[yellow]⚠ Imagen no encontrada en: {img_path}[/yellow]")

    console.print("[bold green]✔ Orquestación completada con WOW Factor.")

if __name__ == "__main__":
    cli()

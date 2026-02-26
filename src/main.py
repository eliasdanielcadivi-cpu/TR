#!/usr/bin/env python3
import click
import yaml
import subprocess
import os
import sys
import time
import json
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class TRContext:
    def __init__(self):
        self.base_path = os.path.expanduser("~/tron/programas/TR")
        self.config_path = f"{self.base_path}/config/config.yaml"
        self.socket = "unix:/tmp/mykitty"
        self.socket_path = "/tmp/mykitty"
        self.handshake_file = "/tmp/tron_handshake.txt"
        self.kitty_conf = f"{self.base_path}/config/kitty.conf"
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return {'ai': {'enabled': True, 'ollama': {'model': 'gemma3:4b'}, 'aliases': {'gemma': {'provider': 'ollama', 'model': 'gemma3:4b'}, 'deepseek': {'provider': 'deepseek', 'model': 'deepseek-chat'}}}}
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

class KittyRemote:
    def __init__(self, ctx):
        self.ctx = ctx

    def is_running(self):
        return os.path.exists(self.ctx.socket_path)

    def launch_hub(self):
        console.print("[bold yellow]⚡ Iniciando Kitty Hub con WOW Factor (14px)...")
        if os.path.exists(self.ctx.socket_path): os.remove(self.ctx.socket_path)
        subprocess.run(["kitty", "-c", self.ctx.kitty_conf, "--listen-on", self.ctx.socket, "--detach"], check=True)
        for _ in range(20):
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

class AIEngine:
    def __init__(self, config):
        self.config = config

    def ask(self, prompt, model_alias=None):
        model = self.config['ollama']['model']
        if model_alias and 'aliases' in self.config and model_alias in self.config['aliases']:
            model = self.config['aliases'][model_alias]['model']
        
        url = f"{self.config['ollama']['base_url']}/api/generate"
        if "gemma" in model.lower():
            prompt = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
            
        payload = {"model": model, "prompt": prompt, "stream": False}
        try:
            response = requests.post(url, json=payload, timeout=30)
            return response.json().get('response', "Error: Sin respuesta.")
        except Exception as e:
            return f"Error IA: {e}"

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = TRContext()

@cli.command()
@click.pass_obj
def status(obj):
    """Diagnóstico de Tron y Kitty."""
    kitty = KittyRemote(obj)
    table = Table(title="Tron System Status")
    table.add_column("Componente", style="cyan")
    table.add_column("Estado", style="magenta")
    table.add_row("Socket Kitty", "ACTIVO" if kitty.is_running() else "DESCONECTADO")
    state_res = kitty.run(["ls"])
    state = json.loads(state_res) if state_res else None
    table.add_row("Pestañas Abiertas", str(len(state[0]['tabs'])) if state else "0")
    console.print(table)
    if state:
        console.print(Panel(json.dumps(state, indent=2), title="Kitty State JSON", border_style="dim"))

@cli.command()
@click.argument("alias")
@click.pass_obj
def model(obj, alias):
    """Cambia el modelo (gemma, deepseek)."""
    if alias in obj.config['ai']['aliases']:
        obj.config['ai']['ollama']['model'] = obj.config['ai']['aliases'][alias]['model']
        with open(obj.config_path, 'w') as f:
            yaml.dump(obj.config, f)
        console.print(f"[bold green]✔ Modelo Tron cambiado a: {alias}")
    else:
        console.print(f"[bold red]✘ Alias '{alias}' no encontrado.")

@cli.command()
@click.argument("task", required=False)
@click.pass_obj
def plan(obj, task):
    """Orquestación táctica WOW."""
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        if not kitty.launch_hub(): return

    if os.path.exists(obj.handshake_file): os.remove(obj.handshake_file)
    console.print("[bold green]🛰  Desplegando Plan Tron...")

    def launch_smart(title, color, cmd):
        win_id = kitty.run(["launch", "--type=tab", "--tab-title", title])
        if not win_id: return
        time.sleep(0.8)
        kitty.run(["set-tab-color", "--match", f"id:{win_id}", f"background={color}"])
        time.sleep(0.8)
        kitty.run(["send-text", "--match", f"id:{win_id}", f"{cmd}\r"])

    launch_smart("TRON-HUB", "#39ff14", f"echo 'ALIVE' > {obj.handshake_file}; echo '--- Tron Hub Online ---';")
    launch_smart("DIAG", "#00d7ff", "echo 'RECURSOS:'; df -h; free -m;")
    v_path = "/home/daniel/Descargas/The Pendragon Cycle Rise Of The Merlin S01E03 E3 A Fatherless Child 1080p DLWP WEB-DL AAC2 0 H 264-DJT[EZTVx.to].mkv"
    launch_smart("VIDEO", "#ff0000", f"~/tron/programas/TR/bin/tr-video \"{v_path}\"")
    i_path = f"{obj.base_path}/assets/2026-02-26_12-48.png"
    launch_smart("IMAGEN", "#ff00ff", f"kitty +kitten icat \"{i_path}\"")

    time.sleep(2)
    if os.path.exists(obj.handshake_file):
        console.print("[bold green]✔ Plan completado. Fuente 14px y Atajos Konsole activos.")
    else:
        console.print("[bold red]⚠ No se detectó handshake.")

@cli.command(name="p")
@click.argument("prompt")
@click.option("--model", "-m", help="Alias del modelo")
@click.pass_obj
def p(obj, prompt, model):
    ai = AIEngine(obj.config['ai'])
    with console.status("[bold blue]Tron pensando..."):
        response = ai.ask(prompt, model_alias=model)
    console.print(Panel(response, title="Tron", border_style="green"))

if __name__ == "__main__":
    cli()

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
            return {'ai': {'enabled': True, 'ollama': {'model': 'gemma3:4b'}, 'aliases': {'gemma': {'provider': 'ollama', 'model': 'gemma3:4b'}}}}
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

class KittyRemote:
    def __init__(self, ctx):
        self.ctx = ctx

    def is_running(self):
        return os.path.exists(self.ctx.socket_path)

    def get_state(self):
        """Plan A: Obtener estado vía Socket."""
        res = self.run(["ls"])
        return json.loads(res) if res else None

    def launch_hub(self):
        """Lanza Kitty si no está activo."""
        console.print("[bold yellow]⚡ Iniciando Kitty Hub con WOW Factor...")
        if os.path.exists(self.ctx.socket_path):
            os.remove(self.ctx.socket_path)
        
        subprocess.run(["kitty", "-c", self.ctx.kitty_conf, "--listen-on", self.ctx.socket, "--detach"], check=True)
        
        # Espera síncrona inteligente
        for _ in range(20):
            if self.is_running():
                time.sleep(1.5) # Tiempo para que el primer shell esté listo
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
        # Mapeo de alias inteligente
        model = self.config['ollama']['model']
        if model_alias and 'aliases' in self.config and model_alias in self.config['aliases']:
            model = self.config['aliases'][model_alias]['model']
        
        url = f"{self.config['ollama']['base_url']}/api/generate"
        # Plantilla Gemma
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
    """Diagnóstico total de Tron y Kitty."""
    kitty = KittyRemote(obj)
    table = Table(title="Tron System Status")
    table.add_column("Componente", style="cyan")
    table.add_column("Estado", style="magenta")
    
    table.add_row("Socket Kitty", "ACTIVO" if kitty.is_running() else "DESCONECTADO")
    
    state = kitty.get_state()
    table.add_row("Pestañas Abiertas", str(len(state[0]['tabs'])) if state else "0")
    
    console.print(table)
    if state:
        console.print(Panel(json.dumps(state, indent=2), title="Kitty State JSON", border_style="dim"))

@cli.command()
@click.argument("task", required=False)
@click.pass_obj
def plan(obj, task):
    """Orquestación táctica con verificación de Handshake."""
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        if not kitty.launch_hub():
            console.print("[bold red]❌ Error: Kitty no respondió al arranque.")
            return

    if os.path.exists(obj.handshake_file): os.remove(obj.handshake_file)
    console.print("[bold green]🛰  Desplegando Plan Tron...")

    def launch_tab_smart(title, color, cmd):
        # 1. Lanzar y capturar ID
        # launch devuelve el ID de la ventana creada
        win_id = kitty.run(["launch", "--type=tab", "--tab-title", title])
        if not win_id: return None
        
        time.sleep(0.8) # Sincronización
        # 2. Pintar
        kitty.run(["set-tab-color", "--match", f"id:{win_id}", f"background={color}"])
        # 3. Ejecutar
        kitty.run(["send-text", "--match", f"id:{win_id}", f"{cmd}\r"])
        return win_id

    # Pestaña 1: Handshake
    launch_tab_smart("TRON-HUB", "green", f"echo 'ALIVE' > {obj.handshake_file}; echo '--- HUB ONLINE ---';")
    
    # Pestaña 2: Sistema
    launch_tab_smart("DIAG", "blue", "echo 'RECURSOS:'; df -h; free -m;")
    
    # Pestaña 3: Video HQ
    v_path = "/home/daniel/Descargas/The Pendragon Cycle Rise Of The Merlin S01E03 E3 A Fatherless Child 1080p DLWP WEB-DL AAC2 0 H 264-DJT[EZTVx.to].mkv"
    launch_tab_smart("VIDEO", "red", f"~/tron/programas/TR/bin/tr-video \"{v_path}\"")

    # Verificación final de Handshake
    time.sleep(2)
    if os.path.exists(obj.handshake_file):
        console.print("[bold green]✔ Handshake Verificado. Orquestación exitosa.")
    else:
        console.print("[bold red]⚠ Alerta: No se detectó handshake. Posible fallo de inyección.")

@cli.command(name="p")
@click.argument("prompt")
@click.option("--model", "-m", help="Alias del modelo (gemma, deepseek)")
@click.pass_obj
def p(obj, prompt, model):
    """Consulta a Tron."""
    ai = AIEngine(obj.config['ai'])
    with console.status("[bold blue]Tron pensando..."):
        response = ai.ask(prompt, model_alias=model)
    console.print(Panel(response, title="Tron", border_style="green"))

if __name__ == "__main__":
    cli()

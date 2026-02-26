#!/usr/bin/env python3
import click
import json
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Importes modulares
from config import TRContext
from kitty import KittyRemote
from engine import AIEngine
from plan import TacticalOrchestrator

console = Console()

@click.group()
@click.pass_context
def cli(ctx):
    """Tron: Terminal Remote Operations Nexus (Modular)"""
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

@cli.command()
@click.argument("alias")
@click.pass_obj
def model(obj, alias):
    """Cambia el modelo (gemma, deepseek)."""
    if alias in obj.config['ai']['aliases']:
        obj.config['ai']['ollama']['model'] = obj.config['ai']['aliases'][alias]['model']
        obj.save_config()
        console.print(f"[bold green]✔ Modelo Tron cambiado a: {alias}")
    else:
        console.print(f"[bold red]✘ Alias '{alias}' no encontrado.")

@cli.command()
@click.pass_obj
def plan(obj):
    """Orquestación táctica WOW."""
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        if not kitty.launch_hub(): return

    orchestrator = TacticalOrchestrator(kitty, obj)
    if orchestrator.deploy_plan():
        console.print("[bold green]✔ Plan completado con éxito.")
    else:
        console.print("[bold red]⚠ No se detectó handshake.")

@cli.command(name="p")
@click.argument("prompt")
@click.option("--model", "-m", help="Alias del modelo")
@click.pass_obj
def p(obj, prompt, model):
    """Consulta a Tron."""
    ai = AIEngine(obj.config['ai'])
    if not sys.stdout.isatty():
        print(ai.ask(prompt, model_alias=model))
        return
    with console.status("[bold blue]Tron pensando..."):
        response = ai.ask(prompt, model_alias=model)
    console.print(Panel(response, title="Tron", border_style="green"))

if __name__ == "__main__":
    cli()

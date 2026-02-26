#!/usr/bin/env python3
import click
import json
import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Importes modulares
from config import TRContext
from kitty import KittyRemote
from engine import AIEngine
from plan import TacticalOrchestrator

# Módulo de color (opcional - se importa bajo demanda)
# from modules.color import ColorEngine

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Tron: Terminal Remote Operations Nexus (Modular)"""
    ctx.obj = TRContext()
    if ctx.invoked_subcommand is None:
        ctx.invoke(help)

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
@click.pass_obj
def help(obj):
    """Lanza la ayuda inteligente navegable con Broot."""
    docs_path = os.path.join(obj.base_path, "docs")
    console.print(f"[bold cyan]🛰  Lanzando Ayuda Inteligente en {docs_path}...")
    # Lanzamos broot sobre la carpeta de documentación
    subprocess.run(["broot", docs_path])

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

@cli.command()
@click.argument("path", required=False)
@click.option("--list", "-l", "list_rules", is_flag=True, help="Lista reglas configuradas")
@click.option("--auto", "-a", is_flag=True, help="Auto-detectar archivo en PWD")
@click.pass_obj
def color(obj, path, list_rules, auto):
    """
    Coloreado automático de pestañas Kitty.
    
    Aplica colores y títulos a pestañas kitty según la ruta del archivo.
    Las reglas están definidas en modules/color/config.yaml
    
    Ejemplos:
        tr color /home/daniel/Escritorio/QT5/elAsunto.md
        tr color --auto
        tr color --list
    """
    # Agregar base_path al sys.path para importar módulos externos
    import sys
    if obj.base_path not in sys.path:
        sys.path.insert(0, obj.base_path)
    
    # Importar bajo demanda para no romper si el módulo no existe
    try:
        from modules.color import ColorEngine
    except ImportError as e:
        console.print(f"[bold red]✗ Error: Módulo de color no disponible: {e}")
        console.print("  Ejecuta: pip install pyyaml")
        return
    except Exception as e:
        console.print(f"[bold red]✗ Error inesperado: {type(e).__name__}: {e}")
        return
    
    engine = ColorEngine(os.path.join(obj.base_path, 'modules/color/config.yaml'))
    
    if list_rules:
        # Listar reglas
        rules = engine.list_rules()
        table = Table(title="Reglas de Coloreado")
        table.add_column("#", style="cyan")
        table.add_column("Patrón", style="green")
        table.add_column("Color", style="yellow")
        table.add_column("Título", style="magenta")
        table.add_column("Prioridad", style="blue")
        
        for i, rule in enumerate(rules, 1):
            table.add_row(
                str(i),
                rule['pattern'],
                rule['color'],
                rule['title'],
                str(rule['priority'])
            )
        console.print(table)
        return
    
    if auto:
        # Auto-detectar archivo reciente en PWD
        try:
            files = os.listdir('.')
            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            if files:
                path = os.path.abspath(files[0])
            else:
                console.print("[bold red]✗ No hay archivos en el directorio actual")
                return
        except Exception as e:
            console.print(f"[bold red]✗ Error: {e}")
            return
    
    if not path:
        console.print("[bold yellow]⚠ Se requiere una ruta o --auto/--list")
        console.print("  Usa 'tr color --help' para más información")
        return
    
    # Aplicar color
    rule = engine.get_rule_for_path(path)
    console.print(f"[bold cyan]📁 Archivo:[/bold cyan] {path}")
    console.print(f"[bold magenta]🎨 Color:[/bold magenta] {rule['color']}")
    console.print(f"[bold green]📝 Título:[/bold green] {rule['title']}")
    
    # Intentar aplicar vía kitty remote control
    success = engine.apply(path, obj.socket_path)
    
    if success:
        console.print("[bold green]✓ Color aplicado exitosamente")
    else:
        console.print("[bold yellow]⚠ No se pudo aplicar el color en kitty")
        console.print("  Posibles causas:")
        console.print("  - Kitty no está corriendo")
        console.print("  - Socket /tmp/mykitty no existe")
        console.print("  - Permiso denegado")
        console.print("")
        console.print("  El color se mostrará arriba pero no se aplicó a la pestaña.")

if __name__ == "__main__":
    cli()

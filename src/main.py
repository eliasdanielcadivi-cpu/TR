#!/usr/bin/env python3
"""
TR - Terminal Remote Operations Nexus (Main CLI)
================================================

Punto de entrada único para el CLI de TRON.
Sigue la regla de modularidad: solo despacho de comandos, sin lógica de negocio.

Funciones:
1. cli() - Grupo de comandos Click
2. dispatch() - Despacha a módulos según comando
3. show_help() - Muestra ayuda navegable con Broot
"""

import click
import json
import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Importes modulares del núcleo
from config import TRContext
from kitty import KittyRemote
from engine import AIEngine
from plan import deploy_plan, verify_handshake

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
    """
    Lanza la ayuda inteligente navegable con Broot.
    Muestra documentación completa de todos los comandos TR.
    """
    docs_path = os.path.join(obj.base_path, "docs")
    help_file = os.path.join(docs_path, "HELP.md")
    
    console.print(f"[bold cyan]🛰  Ayuda Inteligente de TR[/bold cyan]")
    console.print(f"[dim]Ubicación: {docs_path}[/dim]")
    console.print("")
    
    # Verificar si broot está disponible
    if subprocess.run(["which", "broot"], capture_output=True).returncode == 0:
        # Usar broot para navegación
        console.print("[bold green]✓ Abriendo con Broot (navegable)[/bold green]")
        subprocess.run(["broot", docs_path])
    else:
        # Fallback: mostrar HELP.md con less
        if os.path.exists(help_file):
            console.print("[yellow]⚠ Broot no disponible, mostrando HELP.md[/yellow]")
            subprocess.run(["less", "-R", help_file])
        else:
            console.print("[red]✗ No se encontró HELP.md[/red]")
            # Mostrar ayuda básica
            console.print("")
            console.print("[bold cyan]Comandos Principales:[/bold cyan]")
            console.print("  tr p \"pregunta\"     - Consulta a la IA")
            console.print("  tr status            - Diagnóstico del sistema")
            console.print("  tr color <ruta>      - Aplica color a pestaña")
            console.print("  tr video <archivo>   - Reproduce video")
            console.print("  tr image <archivo>   - Muestra imagen")
            console.print("  tr plan              - Orquestación táctica")
            console.print("  tr model <alias>     - Cambia modelo de IA")
            console.print("")
            console.print("[dim]Para documentación completa, instala broot:[/dim]")


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
        if not kitty.launch_hub():
            return

    # Usar módulo plan (modularidad)
    if deploy_plan(kitty, obj):
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
    """
    # Agregar base_path al sys.path para importar módulos externos
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

    rule = engine.get_rule_for_path(path)
    console.print(f"[bold cyan]📁 Archivo:[/bold cyan] {path}")
    console.print(f"[bold magenta]🎨 Color:[/bold magenta] {rule['color']}")
    console.print(f"[bold green]📝 Título:[/bold green] {rule['title']}")

    success = engine.apply(path, obj.socket_path)

    if success:
        console.print("[bold green]✓ Color aplicado exitosamente")
    else:
        console.print("[bold yellow]⚠ No se pudo aplicar el color en kitty")
        console.print("  Posibles causas:")
        console.print("  - Kitty no está corriendo")
        console.print("  - Socket /tmp/mykitty no existe")
        console.print("  - Permiso denegado")


@cli.command()
@click.option("--link", "-l", "create_link", is_flag=True, help="Crea enlace simbólico")
@click.option("--unlink", "-u", is_flag=True, help="Elimina enlace simbólico")
@click.option("--status", "-s", is_flag=True, help="Muestra estado de configuración")
@click.option("--reload", "-r", is_flag=True, help="Recarga configuración en kitty")
@click.pass_obj
def init(obj, create_link, unlink, status, reload):
    """
    Gestiona configuración centralizada de Kitty.

    Delega al módulo init.py (máx 3 funciones).
    """
    # Importar módulo init (modularidad)
    from init import create_symlink, reload_config, get_status, unlink_config

    tr_kitty_conf = os.path.join(obj.base_path, 'config/kitty.conf')
    kitty_link = os.path.expanduser('~/.config/kitty/kitty.conf')

    # Crear enlace
    if create_link:
        console.print("[bold cyan]📁 Creando enlace simbólico...[/bold cyan]")
        result = create_symlink(tr_kitty_conf, kitty_link)
        if result['success']:
            console.print(f"[bold green]✓ {result['message']}[/bold green]")
            console.print(f"  [cyan]{kitty_link} → {result['target']}[/cyan]")
        else:
            console.print(f"[bold red]✗ {result['message']}[/bold red]")
        return

    # Eliminar enlace
    if unlink:
        console.print("[bold cyan]📁 Eliminando enlace simbólico...[/bold cyan]")
        result = unlink_config(kitty_link)
        if result['success']:
            console.print(f"[bold green]✓ {result['message']}[/bold green]")
        else:
            console.print(f"[bold red]✗ {result['message']}[/bold red]")
        return

    # Recargar configuración
    if reload:
        console.print("[bold cyan]🔄 Recargando configuración...[/bold cyan]")
        result = reload_config(obj.socket, tr_kitty_conf)
        if result['success']:
            console.print(f"[bold green]✓ {result['message']}[/bold green]")
        else:
            console.print(f"[bold red]✗ {result['message']}[/bold red]")
        return

    # Mostrar estado (default)
    console.print(Panel.fit(
        "[bold magenta]TRON KITTY - Estado de Configuración[/bold magenta]",
        border_style="magenta"
    ))
    console.print("")

    result = get_status(tr_kitty_conf, kitty_link, obj.socket)

    # Estado de configuración TRON
    if result['tr_config']['exists']:
        console.print(f"[bold green]✓ Configuración TRON:[/bold green]")
        console.print(f"  [cyan]{result['tr_config']['path']}[/cyan]")
    else:
        console.print(f"[bold red]✗ Configuración TRON:[/bold red]")
        console.print(f"  [red]{result['tr_config']['path']} (NO ENCONTRADA)[/red]")
    console.print("")

    # Estado de enlace simbólico
    if result['symlink']['exists'] and result['symlink']['valid']:
        console.print(f"[bold green]✓ Enlace simbólico:[/bold green]")
        console.print(f"  [cyan]~/.config/kitty/kitty.conf → {result['symlink']['target']}[/cyan]")
    elif result['symlink']['exists']:
        console.print(f"[bold yellow]⚠ Enlace simbólico (apunta a otro lado):[/bold yellow]")
        console.print(f"  [cyan]~/.config/kitty/kitty.conf → {result['symlink']['target']}[/cyan]")
    else:
        console.print(f"[bold yellow]⚠ Enlace simbólico:[/bold yellow]")
        console.print(f"  [cyan]~/.config/kitty/kitty.conf (NO EXISTE)[/cyan]")
    console.print("")

    # Estado de kitty
    if result['kitty']['running']:
        console.print(f"[bold green]✓ Kitty (con socket TRON):[/bold green]")
        console.print(f"  [cyan]Activo en {result['kitty']['socket']}[/cyan]")
        console.print(f"  [cyan]Pestañas abiertas: {result['kitty']['tabs']}[/cyan]")
    else:
        console.print(f"[bold yellow]⚠ Kitty (con socket TRON):[/bold yellow]")
        console.print(f"  [cyan]No está corriendo con remote control[/cyan]")
    console.print("")

    # Instrucciones
    console.print("[bold magenta]╭─ Comandos rápidos ─────────────────────────────╮[/bold magenta]")
    console.print("[bold magenta]│[/bold magenta] [cyan]tr init --link    [/cyan] Crea enlace simbólico global    [bold magenta]│[/bold magenta]")
    console.print("[bold magenta]│[/bold magenta] [cyan]tr init --reload  [/cyan] Recarga configuración en kitty  [bold magenta]│[/bold magenta]")
    console.print("[bold magenta]│[/bold magenta] [cyan]tr init --unlink  [/cyan] Elimina enlace simbólico        [bold magenta]│[/bold magenta]")
    console.print("[bold magenta]╰──────────────────────────────────────────────────╯[/bold magenta]")
    console.print("")

    if not result['symlink']['valid']:
        console.print("[yellow]💡 Sugerencia: Ejecuta [bold]tr init --link[/bold] para configurar kitty globalmente[/yellow]")


@cli.command()
@click.argument("archivo", required=True)
@click.option("--sub", help="Archivo de subtítulos (.srt, .ass)")
@click.option("--start", help="Timestamp de inicio (ej: 00:01:30)")
@click.option("--loop", is_flag=True, help="Reproducir en bucle")
@click.option("--speed", type=float, default=1.0, help="Velocidad de reproducción")
@click.option("--volume", type=int, default=80, help="Volumen (0-100)")
@click.option("--audio-only", is_flag=True, help="Solo audio")
@click.pass_obj
def video(obj, archivo, sub, start, loop, speed, volume, audio_only):
    """
    Reproduce video en kitty usando mpv.
    
    Usa el protocolo de gráficos de kitty para renderizado.
    Configuración: TR/config/mpv/mpv.conf
    """
    import subprocess
    
    tr_base = obj.base_path
    mpv_conf = os.path.join(tr_base, "config/mpv/mpv.conf")
    
    # Construir comando
    cmd = [
        "mpv",
        f"--config={mpv_conf}",
        "--profile=sw-fast",
        "--vo=kitty",
        "--vo-kitty-use-shm=yes",
        "--really-quiet",
    ]
    
    if sub:
        cmd.append(f"--sub-file={sub}")
    if start:
        cmd.append(f"--start={start}")
    if loop:
        cmd.append("--loop-file=inf")
    if speed != 1.0:
        cmd.append(f"--speed={speed}")
    cmd.append(f"--volume={volume}")
    if audio_only:
        cmd.append("--vid=no")
    
    cmd.append(archivo)
    
    console.print(f"[bold cyan]🎬 Reproduciendo:[/bold cyan] {archivo}")
    subprocess.run(cmd)


@cli.command()
@click.argument("archivos", nargs=-1, required=True)
@click.option("--grid", "-g", is_flag=True, help="Mostrar en cuadrícula")
@click.option("--width", "-w", help="Ancho en columnas")
@click.option("--align", default="left", help="Alineación (left/center/right)")
@click.option("--scale-up", is_flag=True, help="Escalar imágenes pequeñas")
@click.option("--clear", is_flag=True, help="Limpiar imágenes")
@click.pass_obj
def image(obj, archivos, grid, width, align, scale_up, clear):
    """
    Muestra imágenes en kitty usando icat.
    
    Usa el protocolo de gráficos de kitty.
    Solo funciona en kitty terminal.
    """
    import subprocess
    
    if clear:
        # Limpiar imágenes
        print("\033[3J", end="")
        console.print("[bold green]✓ Imágenes limpiadas[/bold green]")
        return
    
    if not archivos:
        console.print("[red]✗ Error: Se requiere al menos un archivo[/red]")
        return
    
    # Construir comando icat
    cmd = ["kitten", "icat"]
    
    if grid:
        cmd.append("--grid")
    if width:
        cmd.append(f"--width={width}")
    if align:
        cmd.append(f"--align={align}")
    if scale_up:
        cmd.append("--scale-up")
    
    cmd.extend(archivos)
    
    console.print(f"[bold cyan]🖼️  Mostrando {len(archivos)} imagen(es)[/bold cyan]")
    subprocess.run(cmd)


if __name__ == "__main__":
    cli()

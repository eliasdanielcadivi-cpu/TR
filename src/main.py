#!/usr/bin/env python3
"""ARES: Terminal Remote Operations Nexus.

Orquestador táctico para Kitty terminal con IA multi-provider.
"""

import click
import sys
import os
from pathlib import Path

# --- FIX DE RUTA ---
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from config import TRContext, KittyRemote
from modules.admon.boot_manager import launch_ares
from modules.admon.init_manager import manage_config
from modules.admon.diag_manager import show_status
from modules.tactico.plan_manager import deploy_plan
from modules.tactico.zsh_plan_manager import deploy_zsh_plan
from modules.ui.help_manager import HelpManager
from modules.multimedia.media_manager import MediaManager


@click.group(invoke_without_command=True)
@click.option("-p", "--prompt", help="Consulta IA rápida")
@click.pass_context
def cli(ctx, prompt):
    """ARES: Terminal Remote Operations Nexus.
    
    Sin argumentos: abre ARES Hub.
    Con -p: consulta rápida a la IA.
    """
    ctx.obj = TRContext()
    if prompt:
        HelpManager(ctx.obj).query_ai(prompt)
        ctx.exit()
    if ctx.invoked_subcommand is None:
        launch_ares(ctx.obj)


@cli.command(name="p")
@click.argument("prompt")
@click.option("--model", "-m", help="Alias de modelo (gemma, gemma12b, deepseek)")
@click.option("--template", "-t", help="Plantilla YAML (default, chat, code, tools)")
@click.option("--temperature", type=float, default=0.7, help="Temperatura (0-1)")
@click.pass_obj
def p_cmd(obj, prompt, model, template, temperature):
    """Consulta a la IA ARES con opciones avanzadas.
    
    Ejemplos:
        tr p "¿Qué es Python?"
        tr p "Escribe un hello world" --model gemma12b
        tr p "Explica este código" --template code
        tr p "Traduce hello al español" --model gemma --template chat
    """
    HelpManager(obj).query_ai(
        prompt,
        model_alias=model,
        template=template,
        temperature=temperature
    )


@cli.command()
@click.pass_obj
def status(obj):
    """Diagnóstico del socket Kitty y estado del sistema."""
    show_status(obj)


@cli.command()
@click.pass_obj
def help(obj):
    """Abre documentación navegable con Broot."""
    HelpManager(obj).show_help()


@cli.command(name="models")
@click.pass_obj
def models_cmd(obj):
    """Lista modelos disponibles por provider."""
    HelpManager(obj).list_models()


@cli.command(name="templates")
@click.option("--provider", "-p", help="Filtrar por provider (gemma, deepseek)")
@click.pass_obj
def templates_cmd(obj, provider):
    """Lista plantillas YAML disponibles."""
    HelpManager(obj).list_templates(provider)


@cli.command(name="tools")
@click.pass_obj
def tools_cmd(obj):
    """Lista herramientas disponibles para function calling."""
    HelpManager(obj).list_tools()


@cli.command(name="config")
@click.pass_obj
def config_cmd(obj):
    """Muestra configuración actual de IA."""
    HelpManager(obj).show_config()


@cli.command()
@click.pass_obj
def plan(obj):
    """Despliegue táctico original: 4 pestañas coloreadas Hacker Neon."""
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        kitty.launch_hub()
    deploy_plan(kitty, obj)


@cli.command()
@click.pass_obj
def zshPlan(obj):
    """Despliegue táctico ZSH (Hacker AI Session)."""
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        kitty.launch_hub()
    deploy_zsh_plan(kitty, obj)


@cli.command()
@click.option("--link", "-l", is_flag=True, help="Enlazar configuración")
@click.option("--status", "-s", is_flag=True, help="Ver estado")
@click.option("--reload", "-r", is_flag=True, help="Recargar configuración")
@click.pass_obj
def init(obj, **kwargs):
    """Gestión de configuración de ARES."""
    manage_config(obj, **kwargs)


@cli.command()
@click.argument("archivo", type=click.Path(exists=True))
@click.option("--sub", help="Ruta al archivo de subtítulos")
@click.option("--start", help="Tiempo de inicio (ej. 10, 01:15:00)")
@click.option("--loop", is_flag=True, help="Reproducir en bucle infinito")
@click.option("--speed", type=float, default=1.0, help="Velocidad de reproducción")
@click.option("--volume", type=int, default=80, help="Volumen (0-100)")
@click.option("--audio-only", is_flag=True, help="Reproducir solo audio (sin video)")
@click.pass_obj
def video(obj, archivo, **kwargs):
    """Reproduce un video en Kitty usando mpv."""
    MediaManager(obj).play_video(archivo, **kwargs)


@cli.command()
@click.argument("archivos", nargs=-1, type=click.Path(exists=True))
@click.option("--clear", is_flag=True, help="Limpiar imágenes en terminal")
@click.option("--grid", is_flag=True, help="Mostrar en cuadrícula")
@click.option("--width", help="Ancho de la imagen")
@click.option("--align", help="Alineación (left, center, right)")
@click.option("--scale-up", is_flag=True, help="Escalar imagen si es pequeña")
@click.pass_obj
def image(obj, archivos, **kwargs):
    """Muestra imágenes en Kitty terminal."""
    MediaManager(obj).show_image(archivos, **kwargs)


if __name__ == "__main__":
    cli()

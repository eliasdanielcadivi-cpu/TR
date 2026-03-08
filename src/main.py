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
from modules.admon import session_manager
from modules.tactico.plan_manager import deploy_plan
from modules.tactico.zsh_plan_manager import deploy_zsh_plan
from modules.ui.help_manager import HelpManager
from modules.multimedia.media_manager import MediaManager


@click.group(invoke_without_command=True)
@click.option("-p", "--prompt", help="Consulta IA rápida (modo directo)")
@click.pass_context
def cli(ctx, prompt):
    """🚀 ARES: Terminal Remote Operations Nexus.
    
    Sin argumentos: Lanza el ARES Hub (Dashboard táctico).
    Con -p: Realiza una consulta directa a la IA configurada.
    """
    ctx.obj = TRContext()
    if prompt:
        HelpManager(ctx.obj).query_ai(prompt)
        ctx.exit()
    if ctx.invoked_subcommand is None:
        launch_ares(ctx.obj)


@cli.command(name="p")
@click.argument("prompt")
@click.option("--model", "-m", help="Alias del modelo a usar (ej: gemma, gemma12b, deepseek, openrouter)")
@click.option("--template", "-t", help="Plantilla YAML del sistema (default, chat, code, tools)")
@click.option("--temperature", "-T", type=float, default=0.7, help="Creatividad de la respuesta (0.0-1.0). Default: 0.7")
@click.pass_obj
def p_cmd(obj, prompt, model, template, temperature):
    """🤖 Consulta Inteligente (Modo Experto).
    
    Permite interactuar con la IA especificando el modelo, la plantilla de comportamiento
    y la temperatura de respuesta.
    """
    HelpManager(obj).query_ai(
        prompt,
        model_alias=model,
        template=template,
        temperature=temperature
    )


@cli.command(name="model")
@click.argument("provider", required=False)
@click.pass_obj
def model_cmd(obj, provider):
    """⚙️  Configura el Provider de IA por defecto.
    
    Cambia entre 'gemma' (Ollama local) y 'deepseek' (API remota).
    Si no se especifica PROVIDER, muestra la configuración actual.
    """
    if not provider:
        HelpManager(obj).show_config()
        return

    valid_providers = ["gemma", "deepseek", "openrouter"]
    if provider.lower() not in valid_providers:
        click.echo(f"❌ Provider '{provider}' no reconocido. Válidos: {', '.join(valid_providers)}")
        return

    obj.config['ai']['default_provider'] = provider.lower()
    obj.save_config()
    click.echo(f"✅ Provider por defecto actualizado a: [bold cyan]{provider.lower()}[/bold cyan]")


@cli.command()
@click.pass_obj
def status(obj):
    """🔍 Diagnóstico Integral del Sistema.
    
    Verifica el socket de Kitty, handshakes de IA, conectividad de modelos
    y estado de los enlaces simbólicos de configuración.
    """
    show_status(obj)


@cli.command(name="gs")
@click.argument("name", required=False)
@click.pass_obj
def gs_cmd(obj, name):
    """💾 Guarda el estado actual de la sesión de Kitty.
    
    Captura todas las ventanas y pestañas abiertas en el socket ARES
    y las persiste en un archivo JSON para su restauración posterior.
    """
    from config import KittyRemote
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        click.echo(f"❌ El socket {obj.socket_path} no existe. Kitty no parece estar corriendo con ARES.")
        return

    if not name:
        name = click.prompt("📝 Nombre para esta sesión", type=str, default="last_session")

    success, result = session_manager.capture_and_save(obj, kitty, name)
    if success:
        click.echo(f"✅ Sesión guardada en: {result}")
    else:
        click.echo(f"❌ Error: {result}")


@cli.command()
@click.pass_obj
def help(obj):
    """📚 Manual de Operaciones y Documentación.
    
    Abre el explorador de documentación técnica interactivo (Broot).
    Contiene guías de arquitectura, módulos y protocolos ARES.
    """
    HelpManager(obj).show_help()


@cli.command(name="models")
@click.pass_obj
def models_cmd(obj):
    """📦 Lista Modelos Disponibles.
    
    Muestra los modelos configurados en Ollama y los disponibles vía API externa.
    """
    HelpManager(obj).list_models()


@cli.command(name="templates")
@click.option("--provider", "-p", help="Filtrar por provider (gemma, deepseek)")
@click.pass_obj
def templates_cmd(obj, provider):
    """📄 Catálogo de Plantillas YAML.
    
    Lista las plantillas de comportamiento (prompts del sistema) disponibles
    para orquestar la IA según la tarea (Chat, Código, Herramientas).
    """
    HelpManager(obj).list_templates(provider)


@cli.command(name="tools")
@click.pass_obj
def tools_cmd(obj):
    """🛠️  Inventario de Herramientas (Function Calling).
    
    Muestra las capacidades extendidas que la IA puede ejecutar (Shell, Archivos, Busqueda).
    """
    HelpManager(obj).list_tools()


@cli.command(name="config")
@click.pass_obj
def config_cmd(obj):
    """⚙️  Inspección de Configuración.
    
    Muestra el estado actual de 'config.yaml', incluyendo identidades,
    sockets y rutas críticas del ecosistema.
    """
    HelpManager(obj).show_config()


@cli.command()
@click.pass_obj
def plan(obj):
    """🚩 Despliegue Táctico Original.
    
    Lanza el entorno de trabajo estándar: 4 pestañas pre-configuradas
    con identidad visual Hacker Neon y colores dinámicos.
    """
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        kitty.launch_hub()
    deploy_plan(kitty, obj)


@cli.command(name="zshplan")
@click.pass_obj
def zsh_plan_cmd(obj):
    """⚔️  Despliegue Táctico ZSH (AI Session).
    
    Inicia una sesión de terminal optimizada para investigación con IA,
    integrando zsh-autosuggestions y el entorno de herramientas ARES.
    """
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        kitty.launch_hub()
    deploy_zsh_plan(kitty, obj)


@cli.command()
@click.option("--link", "-l", is_flag=True, help="Enlazar configuración de Kitty con ARES")
@click.option("--status", "-s", is_flag=True, help="Ver estado de la inicialización")
@click.option("--reload", "-r", is_flag=True, help="Recargar configuración en Kitty caliente")
@click.pass_obj
def init(obj, **kwargs):
    """🛠️  Gestión de Infraestructura.
    
    Configura enlaces simbólicos, recarga archivos .conf y asegura que
    el entorno local esté sincronizado con el núcleo de ARES.
    """
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
    """🎬 Multimedia: Reproductor de Video.
    
    Inyecta video en la terminal Kitty usando MPV con comunicación IPC
    y control de alta fidelidad desde la CLI.
    """
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
    """🖼️  Multimedia: Visualizador de Imágenes.
    
    Renderiza imágenes directamente en las celdas de Kitty usando el protocolo
    icat. Soporta cuadrículas, escalado y alineación dinámica.
    """
    MediaManager(obj).show_image(archivos, **kwargs)


if __name__ == "__main__":
    cli()

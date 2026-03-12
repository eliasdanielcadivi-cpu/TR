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
from modules.tactico.mcat_demo import deploy_mcat_demo


from modules.ui.help_manager import HelpManager
from modules.multimedia.media_manager import MediaManager


@click.group(invoke_without_command=True, add_help_option=False)
@click.option("-p", "--prompt", help="Consulta IA rápida (modo directo)")
@click.option("-h", "--help", is_flag=True, is_eager=True, help="Mostrar ayuda enriquecida")
@click.pass_context
def cli(ctx, prompt, help):
    """🚀 ARES: Terminal Remote Operations Nexus.
    
    Sin argumentos: Lanza el ARES Hub (Dashboard táctico).
    Con -p: Realiza una consulta directa a la IA configurada.
    """
    obj = ctx.ensure_object(TRContext)
    ctx.obj = obj

    # --- MANEJO DE AYUDA ENRIQUECIDA ---
    if help:
        HelpManager(obj).show_enhanced_help()
        ctx.exit()
    # ----------------------------------

    if prompt:
        HelpManager(ctx.obj).query_ai(prompt)
        ctx.exit()
    if ctx.invoked_subcommand is None:
        launch_ares(ctx.obj)


@cli.command(name="mcat-demo")
@click.pass_obj
def mcat_demo_cmd(obj):
    """🛠️  Mcat Demo: Despliegue de capacidades completas.
    
    Lanza 4 pestañas demostrando el parseo de documentos, conversión de archivos,
    visualización multimedia en terminal y modo interactivo.
    """
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        kitty.launch_hub()
    deploy_mcat_demo(kitty, obj)


@cli.command(name="p")
@click.argument("prompt")
@click.option("--model", "-m", help="Alias del modelo a usar (ej: gemma, gemma12b, deepseek, openrouter, ares, ares-think)")
@click.option("--template", "-t", help="Plantilla YAML del sistema (default, chat, code, tools)")
@click.option("--temperature", "-T", type=float, default=0.7, help="Creatividad de la respuesta (0.0-1.0). Default: 0.7")
@click.option("--rag", help="Etiqueta de dataset RAG (default, docs, skills, codigo, config)")
@click.option("--think", is_flag=True, help="Usar modelo pensante (ares-think:latest)")
@click.pass_obj
def p_cmd(obj, prompt, model, template, temperature, rag, think):
    """🤖 Consulta Inteligente (Modo Experto).

    Permite interactuar con la IA especificando el modelo, la plantilla de comportamiento
    y la temperatura de respuesta.

    Con --rag: Usa RAG para recuperar contexto del dataset especificado.
    Con --think: Usa ares-think:latest (mantiene etiquetas <think></think>)
    """
    # Determinar modelo final
    final_model = model
    if think:
        final_model = "ares-think:latest"
    
    # Si se usa --rag, inyectar contexto RAG
    if rag:
        from modules.ia.apollo import retrieve, compress_context, generate_answer

        # Recuperar contexto del dataset
        results = retrieve(query=prompt, k=5, mode="fused", dataset=rag)

        # Obtener textos de chunks
        chunks = results.get("semantic", [])[:5]

        if chunks:
            # Comprimir contexto
            context = compress_context(chunks, query=prompt, max_tokens=1500)

            # Generar respuesta con contexto RAG
            llm_model = final_model if final_model else "ares:latest"
            response = generate_answer(
                query=prompt,
                context=context,
                model=llm_model,
                temperature=temperature,
                apply_post_processing=True
            )

            # Añadir fuentes
            from modules.ia.apollo import generate_citations
            full_response = generate_citations(response, chunks)

            click.echo(full_response)
            ctx.exit()
        else:
            click.echo("⚠️  No se encontró contexto relevante en el dataset '{}'.".format(rag))
            # Continuar con consulta normal sin RAG

    # Consulta normal sin RAG
    HelpManager(obj).query_ai(
        prompt,
        model_alias=final_model,
        template=template,
        temperature=temperature
    )


@cli.command(name="i")
@click.option("--rag", help="Dataset RAG por defecto (default, docs, skills, codigo, config)")
@click.option("--model", "-m", default="ares:latest", help="Modelo LLM")
@click.option("--think", is_flag=True, help="Activar modo pensante (usa ares-think)")
@click.pass_obj
def i_cmd(obj, rag, model, think):
    """💬 Modo Interactivo ARES (Loop REPL).
    
    Delega la gestión visual y el loop interactivo al módulo especializado.
    """
    from modules.ui.chat_interface import start_interactive_chat
    start_interactive_chat(obj, rag=rag, model=model, think=think)


@cli.command(name="model")
@click.argument("model_name", required=False, default=None)
@click.option("--list", "-l", "list_models", is_flag=True, help="List all available Ollama models")
@click.option("--set-default", "-s", is_flag=True, help="Set model as default (requires model_name)")
@click.pass_obj
def model_cmd(obj, model_name, list_models, set_default):
    """⚙️  Gestiona Modelos de IA por defecto.

    Sin argumentos: Muestra el modelo/provider actual.
    Con MODEL_NAME: Cambia el modelo predeterminado a cualquier modelo Ollama.
    Con --list: Lista todos los modelos disponibles en Ollama.
    Con --set-default: Establece el modelo como predeterminado.

    Soporta todos los modelos Ollama (mistral, qwen, deepseek-r1, etc.)
    y futuros modelos automáticamente.
    """
    from modules.ia.ai_engine import AIEngine
    
    ai_engine = AIEngine(obj.config['ai'], str(obj.base_path))
    
    # Prioridad 1: --list flag (siempre que esté presente, listar)
    if list_models:
        _list_all_models(ai_engine, obj)
        return
    
    # Prioridad 2: Sin argumentos (mostrar config actual)
    if model_name is None:
        _show_current_model(obj)
        return
    
    # Prioridad 3: Establecer nuevo modelo por defecto
    _set_default_model(obj, model_name, set_default)


def _list_all_models(ai_engine, obj) -> None:
    """Listar todos los modelos disponibles (Ollama + Cloud)."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    console = Console()
    
    # Modelos locales (Ollama)
    console.print(Panel("[bold cyan]📦 Modelos Locales (Ollama)[/bold cyan]", border_style="cyan"))
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            table = Table(show_header=True, header_style="bold green")
            table.add_column("Nombre", style="green", width=40)
            table.add_column("Size", style="yellow", width=12)
            table.add_column("Modified", style="blue", width=20)
            
            for model in models:
                name = model.get("name", "unknown")
                size = model.get("size", "N/A")
                size_str = f"{size / 1e9:.1f} GB" if isinstance(size, (int, float)) else size
                modified = model.get("modified_at", "N/A")[:10] if isinstance(model.get("modified_at"), str) else "N/A"
                table.add_row(name, size_str, modified)
            
            console.print(table)
        else:
            console.print("[red]❌ No se pudo conectar con Ollama[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
    
    # Modelos Cloud
    console.print("\n[bold magenta]📡 Modelos Cloud (API)[/bold magenta]")
    cloud_table = Table(show_header=True, header_style="bold magenta")
    cloud_table.add_column("Provider", style="cyan")
    cloud_table.add_column("Modelos", style="green")
    
    # DeepSeek
    cloud_table.add_row("DeepSeek", "deepseek-chat, deepseek-coder")
    # OpenRouter (placeholder)
    cloud_table.add_row("OpenRouter", "Múltiples modelos (configurable)")
    
    console.print(cloud_table)
    console.print("\n[dim]💡 Usa 'ares model <nombre> --set-default' para cambiar el modelo predeterminado[/dim]")


def _show_current_model(obj) -> None:
    """Mostrar modelo/provider actual."""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    ai_config = obj.config.get("ai", {})
    gemma_config = ai_config.get("gemma", {})
    default_model = gemma_config.get("model", "gemma3:4b")
    default_provider = ai_config.get("default_provider", "gemma")
    
    panel = Panel(
        f"[bold green]Provider Activo:[/bold green] {default_provider}\n"
        f"[bold cyan]Modelo Predeterminado:[/bold cyan] {default_model}\n\n"
        f"[dim]💡 Usa 'ares model --list' para ver todos los modelos[/dim]\n"
        f"[dim]💡 Usa 'ares model <modelo> --set-default' para cambiar[/dim]",
        title="⚙️ Configuración Actual",
        border_style="cyan"
    )
    console.print(panel)


def _set_default_model(obj, model_name: str, set_default: bool) -> None:
    """Establecer modelo como predeterminado."""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    # Verificar si el modelo existe en Ollama
    model_exists = False
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = [m.get("name", "") for m in data.get("models", [])]
            if model_name in models or model_name.lower() in [m.lower() for m in models]:
                model_exists = True
    except:
        pass
    
    # Si no existe en Ollama, verificar si es un modelo cloud válido
    cloud_models = ["deepseek-chat", "deepseek-coder"]
    if not model_exists and model_name not in cloud_models:
        # Advertencia pero permitir continuar (puede ser un modelo nuevo)
        console.print(f"[yellow]⚠️  El modelo '{model_name}' no se encontró en Ollama.[/yellow]")
        console.print("[dim]Si es un modelo cloud o nuevo, puedes continuar.[/dim]\n")
    
    # Actualizar configuración
    ai_config = obj.config.get("ai", {})
    if "gemma" not in ai_config:
        ai_config["gemma"] = {}
    
    ai_config["gemma"]["model"] = model_name
    obj.config["ai"] = ai_config
    obj.save_config()
    
    console.print(Panel(
        f"[bold green]✅ Modelo predeterminado actualizado[/bold green]\n\n"
        f"Modelo: [bold cyan]{model_name}[/bold cyan]\n\n"
        f"[dim]Las próximas consultas usarán este modelo por defecto.[/dim]",
        border_style="green"
    ))


@cli.command()
@click.pass_obj
def status(obj):
    """🔍 Diagnóstico Integral del Sistema.
    
    Verifica el socket de Kitty, handshakes de IA, conectividad de modelos
    y estado de los enlaces simbólicos de configuración.
    """
    show_status(obj)


@cli.group(name="gs", invoke_without_command=True)
@click.pass_context
def gs_cmd(ctx):
    """💾 Gestión de Sesiones de Kitty.
    
    Sin subcomando: Lanza el proceso de guardado rápido.
    Subcomandos: list, restore, com, save.
    """
    if ctx.invoked_subcommand is None:
        # Lógica de guardado por defecto (ares gs)
        ctx.invoke(gs_save)


@gs_cmd.command(name="save")
@click.argument("name", required=False)
@click.pass_obj
def gs_save(obj, name):
    """💾 Guarda la sesión actual."""
    from config import KittyRemote
    from modules.admon import session_manager
    kitty = KittyRemote(obj)
    
    if not kitty.is_running():
        click.echo(f"❌ El socket {obj.socket_path} no existe. Kitty no está corriendo.")
        return

    if not name:
        name = click.prompt("📝 Nombre para esta sesión", type=str, default="last_session")

    success, result = session_manager.capture_and_save(obj, kitty, name)
    if success:
        click.echo(f"✅ Sesión guardada en: {result}")
    else:
        click.echo(f"❌ Error: {result}")


@gs_cmd.command(name="list")
@click.pass_obj
def gs_list(obj):
    """📋 Lista sesiones guardadas."""
    from modules.admon import session_manager
    sessions = session_manager.list_sessions(obj)
    if not sessions:
        click.echo("📭 No hay sesiones guardadas en 'db/'.")
        return
    
    click.echo("📂 [bold cyan]Sesiones Disponibles:[/bold cyan]")
    for s in sessions:
        click.echo(f"  • {s}")


@gs_cmd.command(name="restore")
@click.argument("name")
@click.pass_obj
def gs_restore(obj, name):
    """🔄 Restaura una sesión por nombre."""
    from config import KittyRemote
    from modules.admon import session_manager
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        click.echo("❌ Kitty no está corriendo.")
        return

    success, msg = session_manager.restore_session(obj, kitty, name)
    if success:
        click.echo(f"✅ {msg}")
    else:
        click.echo(f"❌ {msg}")


@gs_cmd.command(name="deploy")
@click.argument("name")
@click.option("--socket", help="Socket UNIX personalizado (ej. /tmp/custom)")
@click.pass_obj
def gs_deploy(obj, name, socket):
    """🚀 Despliega una sesión en una ventana/socket NUEVO."""
    from modules.tactico.orchestrator import KittyOrchestrator
    orch = KittyOrchestrator(obj)
    
    # Si no se da socket, generamos uno temporal basado en el nombre de la sesión
    target_socket = socket or f"/tmp/ares_session_{name}"
    
    click.echo(f"🛰️  Desplegando sesión '{name}' en socket '{target_socket}'...")
    success, msg = orch.deploy_session_from_db(name, socket=target_socket, new_window=True)
    
    if success:
        click.echo(f"✅ {msg}")
    else:
        click.echo(f"❌ {msg}")


@gs_cmd.command(name="com")
@click.argument("tab_title")
@click.argument("command")
@click.pass_obj
def gs_com(obj, tab_title, command):
    """⚔️  Envía un comando a una pestaña específica."""
    from config import KittyRemote
    from modules.admon import session_manager
    kitty = KittyRemote(obj)
    if not kitty.is_running():
        click.echo("❌ Kitty no está corriendo.")
        return

    success, msg = session_manager.send_command_to_tab(kitty, tab_title, command)
    if success:
        click.echo(f"✅ {msg}")
    else:
        click.echo(f"❌ {msg}")


@cli.command()
@click.pass_obj
def help(obj):
    """📚 Manual de Operaciones Extendido (Broot).
    
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

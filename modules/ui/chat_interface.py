"""Chat Interface: Orquestación de Estados Wow y Historial.

Implementa el ciclo de vida de los mensajes:
1. Turno de ARES genera Efecto Wow (Vivo).
2. El Historial permanece liviano (Light).

Comandos interactivos:
- /model, /m - Listar/cambiar modelo
- /think - Activar/desactivar modo pensante
- /rag - Activar/desactivar RAG
- /clear, /c - Limpiar pantalla
- /help, /h - Mostrar ayuda
- /quit, /exit - Salir
"""

import click
import sys
from modules.ia.apollo.emoji_manager import get_asset_render, get_layout_config
from modules.ia.ai_engine import AIEngine


def render_thinking_state():
    """Muestra el spinner Wow (Video/GIF pesado) durante la espera."""
    spinner = get_asset_render("spinner", mode="live")
    click.echo(f"\r{spinner}", nl=False)


def _list_models_and_switch(obj, current_model):
    """Listar modelos y permitir cambio."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    console = Console()
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            console.print(Panel("[bold cyan]📦 Modelos Locales (Ollama)[/bold cyan]", border_style="cyan"))
            
            table = Table(show_header=True, header_style="bold green")
            table.add_column("#", style="dim", width=4)
            table.add_column("Nombre", style="green")
            table.add_column("Size", style="yellow", width=10)
            table.add_column("Modified", style="blue", width=12)
            
            model_names = []
            for idx, model in enumerate(models, 1):
                name = model.get("name", "unknown")
                model_names.append(name)
                size = model.get("size", "N/A")
                size_str = f"{size / 1e9:.1f} GB" if isinstance(size, (int, float)) else "N/A"
                modified = model.get("modified_at", "N/A")[:10] if isinstance(model.get("modified_at"), str) else "N/A"
                table.add_row(f"{idx}.", name, size_str, modified)
            
            console.print(table)
            click.echo("\n[dim]Escribe el número o nombre del modelo, o 'cancel' para volver[/dim]")
            choice = click.prompt("  Modelo", type=str, prompt_suffix="> ")
            
            if choice.lower() == "cancel":
                return current_model
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(model_names):
                    click.echo(f"[green]✓ Cambiando a: {model_names[idx]}[/green]")
                    return model_names[idx]
            except ValueError:
                pass
            
            if choice in model_names:
                click.echo(f"[green]✓ Cambiando a: {choice}[/green]")
                return choice
            elif choice.lower() in [m.lower() for m in model_names]:
                matched = next(m for m in model_names if m.lower() == choice.lower())
                click.echo(f"[green]✓ Cambiando a: {matched}[/green]")
                return matched
            
            click.echo(f"[yellow]⚠️  Modelo '{choice}' no encontrado[/yellow]")
            return current_model
            
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        return current_model
    
    console.print("\n[bold magenta]📡 Modelos Cloud[/bold magenta]")
    console.print("  • deepseek-chat (DeepSeek API)")
    console.print("  • deepseek-coder (DeepSeek API)")
    
    choice = click.prompt("  Modelo", type=str, prompt_suffix="> ")
    if choice.lower() in ["deepseek-chat", "deepseek-coder", "deepseek"]:
        click.echo(f"[green]✓ Cambiando a: {choice}[/green]")
        return choice
    
    return current_model


def _show_help():
    """Mostrar ayuda de comandos."""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    help_text = """[bold]Comandos Disponibles:[/bold]
  [cyan]/model[/cyan], [cyan]/m[/cyan]       Listar y cambiar modelo
  [cyan]/think[/cyan]            Activar/desactivar modo pensante
  [cyan]/rag[/cyan]              Activar/desactivar RAG
  [cyan]/clear[/cyan], [cyan]/c[/cyan]       Limpiar pantalla
  [cyan]/help[/cyan], [cyan]/h[/cyan]        Mostrar esta ayuda
  [cyan]/quit[/cyan], [cyan]/exit[/cyan]     Salir del modo interactivo"""
    
    console.print(Panel(help_text, title="📚 Ayuda", border_style="cyan"))


def start_interactive_chat(obj, rag=None, model="ares:latest", think=False):
    """Ejecuta el chat con transición automática entre Wow e Historial."""

    cfg = get_layout_config()
    ares_color = cfg.get('colors', {}).get('ares_text', 'cyan')
    sep_char = cfg.get('separator_char', '┃')

    click.clear()
    click.echo(get_asset_render("header_ares", mode="history"))
    click.secho(f"   SISTEMA ARES ACTIVO | Modelo: {model}", fg=ares_color, bold=True)
    if think:
        click.secho("   [MODO PENSANTE ACTIVO]", fg="magenta", bold=True)
    if rag:
        click.secho(f"   [RAG: {rag}]", fg="yellow", bold=True)
    click.echo("")

    while True:
        try:
            click.echo(get_asset_render("separator", mode="history"))

            user_icon = get_asset_render("user", mode="history")
            user_header = get_asset_render("header_user", mode="history")
            user_input = click.prompt(f"{user_icon} {user_header} {sep_char}", type=str, prompt_suffix=" ")

            if user_input.strip().startswith("/"):
                cmd = user_input.strip().lower()
                
                if cmd in ("/quit", "/exit"):
                    break
                elif cmd in ("/clear", "/c"):
                    click.clear()
                    click.echo(get_asset_render("header_ares", mode="history"))
                    click.secho(f"   SISTEMA ARES ACTIVO | Modelo: {model}", fg=ares_color, bold=True)
                    continue
                elif cmd in ("/help", "/h"):
                    _show_help()
                    continue
                elif cmd.startswith("/model") or cmd.startswith("/m "):
                    model = _list_models_and_switch(obj, model)
                    continue
                elif cmd.startswith("/think"):
                    think = not think
                    status = "ACTIVO" if think else "INACTIVO"
                    click.echo(f"[magenta]✓ Modo pensante: {status}[/magenta]")
                    continue
                elif cmd.startswith("/rag"):
                    if rag:
                        rag = None
                        click.echo("[yellow]✓ RAG desactivado[/yellow]")
                    else:
                        rag = click.prompt("Dataset RAG", type=str, default="default")
                        click.echo(f"[yellow]✓ RAG activado: {rag}[/yellow]")
                    continue
                elif not user_input.strip():
                    continue

            if not user_input.strip():
                continue

            render_thinking_state()

            engine = AIEngine(obj.config['ai'], str(obj.base_path))
            current_model = "ares-think:latest" if think else model
            response = engine.ask(user_input, model_alias=current_model)

            click.echo("\r" + " " * 60 + "\r", nl=False)

            click.echo(get_asset_render("separator", mode="live"))

            ares_avatar = get_asset_render("ares", mode="live")
            ares_header = get_asset_render("header_ares", mode="live")
            click.echo(f"{ares_avatar} {ares_header} {sep_char} ", nl=False)

            click.secho(response, fg=ares_color)

            click.echo("\n" + " " * 10 + get_asset_render("separator", mode="history") + "\n")

        except (KeyboardInterrupt, EOFError):
            break

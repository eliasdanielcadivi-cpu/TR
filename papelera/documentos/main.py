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
    """💬 Modo Interactivo (REPL con IA).

    Inicia una sesión interactiva tipo REPL para conversar con la IA.
    Comandos especiales:
      /quit, /exit - Salir
      /model <nombre> - Cambiar modelo
      /rag <dataset> - Cambiar dataset RAG
      /think on|off - Activar/desactivar modo pensante
      /clear - Limpiar pantalla
      /help - Ayuda
    """
    import readline  # Historial de comandos
    from modules.ia.apollo.emoji_manager import format_output_with_emoji, get_emoji_render, get_ui_config
    
    # --- 1. Cargar Configuración UI ---
    ui_cfg = get_ui_config()
    ares_color = ui_cfg.get('colors', {}).get('ares_text', 'cyan')
    user_color = ui_cfg.get('colors', {}).get('user_text', 'white')
    sep = ui_cfg.get('separator', '┃')
    
    # --- 2. Determinar Modelo Inicial ---
    if think:
        current_model = "ares-think:latest"
    else:
        current_model = model
    
    current_rag = rag
    think_mode = think  # Track think mode separately
    
    # --- 3. Encabezado Limpio (Minimalista-Cyberpunk) ---
    click.clear()
    header = format_output_with_emoji("SISTEMA ARES ACTIVO", "ares", width=4, height=2)
    click.echo(header)
    click.echo(f"   Modelo: [bold {ares_color}]{current_model}[/bold {ares_color}]")
    click.echo(f"   RAG Dataset: [bold {user_color}]{current_rag or 'desactivado'}[/bold {user_color}]")
    click.echo(f"   Think Mode: [yellow]{'ON' if think_mode else 'OFF'}[/yellow]")
    click.secho(f"   {'─' * 45}", fg=ares_color)
    click.echo("   Comandos: /quit, /model, /rag, /think, /clear, /help")
    click.echo("") # Espacio para respirar
    
    while True:
        try:
            # --- 4. Turno Usuario: Avatar + Separador + Prompt ---
            user_icon = get_emoji_render("user", width=2, height=1)
            user_input = click.prompt(f"{user_icon} {sep}", type=str, prompt_suffix=" ")
            
            # Comandos especiales
            if user_input.strip().startswith("/"):
                parts = user_input.strip().split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command in ("/quit", "/exit"):
                    click.echo("👋 ¡Hasta luego!")
                    break
                
                elif command == "/model":
                    if args:
                        current_model = args
                        click.echo(f"✅ Modelo: {current_model}")
                    else:
                        click.echo(f"Modelo actual: {current_model}")
                
                elif command == "/rag":
                    if args:
                        valid_datasets = ["default", "docs", "skills", "codigo", "config"]
                        if args in valid_datasets:
                            current_rag = args
                            click.echo(f"✅ RAG Dataset: {current_rag}")
                        else:
                            click.echo(f"❌ Datasets válidos: {', '.join(valid_datasets)}")
                    else:
                        click.echo(f"RAG actual: {current_rag or 'desactivado'}")
                
                elif command == "/think":
                    if args.lower() in ("on", "1", "true"):
                        think_mode = True
                        current_model = "ares-think:latest"
                        click.echo("✅ Think Mode: ON (usa ares-think)")
                    elif args.lower() in ("off", "0", "false"):
                        think_mode = False
                        current_model = "ares:latest"
                        click.echo("✅ Think Mode: OFF (usa ares)")
                    else:
                        click.echo(f"Think Mode: {'ON' if think_mode else 'OFF'}")
                
                elif command == "/clear":
                    click.clear()
                    click.echo(header)
                
                elif command == "/help":
                    click.echo("""
📚 Comandos disponibles:
  /quit, /exit  - Salir del modo interactivo
  /model <nombre> - Cambiar modelo LLM
  /rag <dataset>  - Cambiar dataset RAG (default, docs, skills, codigo, config)
  /think on|off   - Activar/desactivar modo pensante (usa ares-think)
  /clear          - Limpiar pantalla
  /help           - Mostrar esta ayuda
""")
                
                else:
                    click.echo(f"❌ Comando desconocido: {command}. Usa /help")
                continue
            
            # Consulta normal
            if not user_input.strip():
                continue
            
            # --- 5. Turno ARES: Avatar + Separador + Respuesta (Sin bordes ASCII) ---
            if current_rag:
                from modules.ia.apollo import retrieve, compress_context, generate_answer, generate_citations
                
                click.secho(f"   🔍 Buscando contexto en '{current_rag}'...", fg="yellow", err=True)
                results = retrieve(query=user_input, k=5, mode="fused", dataset=current_rag)
                
                chunks = results.get("semantic", [])[:5]
                context = compress_context(chunks, query=user_input, max_tokens=1500) if chunks else ""
                
                click.secho(f"   🤖 Generando con {current_model}...", fg=ares_color, err=True)
                response = generate_answer(
                    query=user_input,
                    context=context,
                    model=current_model,
                    temperature=0.1,
                    apply_post_processing=True
                )
                
                # Citas
                full_response = generate_citations(response, chunks) if chunks else response
            else:
                from modules.ia.ai_engine import AIEngine
                engine = AIEngine(obj.config['ai'], str(obj.base_path))
                full_response = engine.ask(user_input, model_alias=current_model)
            
            # Renderizado final (Estética "Wow" sin ruido)
            ares_icon = get_emoji_render("ares", width=4, height=2)
            click.echo(f"\n{ares_icon} {sep} ", nl=False)
            click.secho(full_response, fg=ares_color)
            click.echo("") # Espacio para respirar visualmente
                
        except KeyboardInterrupt:
            click.echo("\n👋 Interrumpido. Usa /quit para salir.")
        except EOFError:
            break


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

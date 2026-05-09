#!/usr/bin/env python3
"""ARES: Terminal Remote Operations Nexus.

Orquestador táctico para Kitty terminal con IA multi-provider.
"""

import click
import sys
import os
import subprocess
from pathlib import Path

# --- FIX DE RUTA ---
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

# --- CARGA DE ENTORNO ---
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, "config", ".env"))
# ------------------------

from config import TRContext, KittyRemote
from modules.admon.boot_manager import launch_ares
from modules.admon.init_manager import manage_config
from modules.admon.diag_manager import show_status
from modules.admon import session_manager
from modules.admon.grafo_manager import (
    start_grafo_server,
    stop_grafo_server,
    check_grafo_status,
)
from modules.admon.memgraph_manager import (
    start_memgraph,
    stop_memgraph,
    memgraph_status,
)
from modules.tactico.plan_manager import deploy_plan
from modules.tactico.zsh_plan_manager import deploy_zsh_plan
from modules.tactico.mcat_demo import deploy_mcat_demo

# Inicializar bases de datos
from modules.core.session_manager import init_db as init_session_db
from modules.core.window_registry import init_db as init_window_db
init_session_db()
init_window_db()

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

    # --- MANEJO DE AYUDA ENRIQUECIDA (SISTEMA SOBERANO) ---
    if help:
        HelpManager(obj).show_enhanced_help()
        ctx.exit()
    # -----------------------------------------------------

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
@click.option("--provider", "-P", help="Proveedor de IA (ollama, gemini, deepseek, openrouter)")
@click.option("--template", "-t", default="default", help="Plantilla YAML del sistema (default, chat, code, tools)")
@click.option("--temperature", "-T", type=float, default=0.7, help="Creatividad de la respuesta (0.0-1.0). Default: 0.7")
@click.option("--rag", is_flag=False, flag_value="default", default=None, help="Etiqueta de dataset RAG (default, docs, skills, codigo, config)")
@click.option("--mengraph", is_flag=True, help="Usar motor RAG Memgraph (vía Grafo en RAM)")
@click.option("--think", is_flag=True, help="Usar modelo pensante (ares-think:latest)")
@click.option("-v", "--verbose", is_flag=True, help="Mostrar depuración RAG detallada")
@click.pass_obj
def p_cmd(obj, prompt, model, provider, template, temperature, rag, mengraph, think, verbose):
    """🤖 Consulta Inteligente (Modo Experto)."""
    # Determinar modelo final
    final_model = model
    if think:
        final_model = "ares-think:latest"
    
    # Orquestar con AIEngine
    from modules.ia.ai_engine import AIEngine
    ai = AIEngine(obj.config['ai'], str(obj.base_path))

    # Prioridad: RAG Mengraph (Si se solicita explícitamente)
    if mengraph:
        from modules.utils import messenger
        from modules.rag_mengraph.core.tool import MengraphTool
        from modules.ia.ai_engine import AIEngine
        import json
        import sys

        try:
            ONTOLOGY = f"{obj.base_path}/config/rag_mengraph/ontology_master.json"
            tool = MengraphTool(ONTOLOGY)
            
            # Recuperar contexto del grafo vía Interfaz Universal (JSON)
            result_json = tool.query_json(prompt)
            data = json.loads(result_json)

            if data['status'] == 'success' and data['data']:
                context_str = "\n".join([f"Ancla: {item['ancla']} -> Relacionado: {item['relacionado']}" for item in data['data']])
                
                # Orquestar con AIEngine
                ai = AIEngine(obj.config['ai'], str(obj.base_path))
                system_instr = f"Eres ARES. Responde basándote en este contexto estructurado de GRAFOS (Memgraph):\n\n{context_str}\n\nSi el contexto no es suficiente, indícalo."
                
                click.secho("🧠 ARES consultando Grafo (Interfaz Universal)...", fg="magenta", bold=True)
                
                # Usar el alias del provider como modelo si se pasa explícitamente y no hay modelo
                effective_alias = provider if provider and not final_model else final_model

                for chunk in ai.ask_stream(prompt, model_alias=effective_alias, template=template, temperature=temperature):
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                sys.stdout.write("\n")
                
                if verbose:
                    click.secho("\n🔍 Evidencia JSON:", fg="yellow", dim=True)
                    click.echo(result_json)
                return
            else:
                messenger.warn("No se encontró información relevante en el Grafo Memgraph.")
        except Exception as e:
            messenger.error(f"Error en RAG Memgraph: {e}")
            return

    # Si se usa --rag tradicional (Apollo/Kuzu), inyectar contexto RAG
    if rag:
        from modules.utils import messenger
        try:
            from modules.ia.apollo import retrieve, compress_context, generate_answer
            
            # Recuperar contexto del dataset
            results = retrieve(query=prompt, k=5, mode="fused", dataset=rag)
            
            # --- MODO VERBOSE (DEPURACIÓN RAG) ---
            if verbose:
                from rich.console import Console
                from rich.panel import Panel
                from rich.table import Table
                console = Console()
                
                console.print(Panel(f"[bold yellow]🔍 DEPURACIÓN RAG (Dataset: {rag})[/bold yellow]", border_style="yellow"))
                
                # 1. Bloques Semánticos
                sem_table = Table(title="🧠 Búsqueda Semántica (Vectorial)", box=None)
                sem_table.add_column("Score", style="green")
                sem_table.add_column("Fuente", style="cyan")
                sem_table.add_column("Preview", style="white", ratio=2)
                for r in results.get("semantic", []):
                    preview = (r.get("text", "")[:100] + "...") if len(r.get("text", "")) > 100 else r.get("text", "")
                    sem_table.add_row(f"{r.get('score', 0):.4f}", r.get("source", "N/A"), preview)
                console.print(sem_table)
                
                # 2. Grafo de Entidades
                graph_table = Table(title="🕸️ Búsqueda en Grafo (Entidades)", box=None)
                graph_table.add_column("Entidad", style="magenta")
                graph_table.add_column("Tipo", style="blue")
                graph_table.add_column("Relaciones", style="white")
                for e in results.get("graph", []):
                    rels = ", ".join([f"{r['predicate']} -> {r['object_name']}" for r in e.get("relations", [])])
                    graph_table.add_row(e.get("name", "N/A"), e.get("type", "N/A"), rels)
                console.print(graph_table)
                
                # 3. Búsqueda Relacional (FTS/LIKE)
                rel_table = Table(title="📁 Búsqueda Relacional (FTS/LIKE)", box=None)
                rel_table.add_column("Fuente", style="cyan")
                rel_table.add_column("Match", style="white")
                for r in results.get("relational", []):
                    rel_table.add_row(r.get("source", "N/A"), r.get("text", "")[:80] + "...")
                console.print(rel_table)
                
                # 4. Resultados Fusionados (RRF)
                fused_table = Table(title="🧬 Ranking Fusionado (RRF)", box=None)
                fused_table.add_column("Score RRF", style="yellow")
                fused_table.add_column("Chunk ID", style="cyan")
                for r in results.get("fused", []):
                    fused_table.add_row(f"{r.get('rrf_score', 0):.6f}", str(r.get("chunk_id", "N/A")))
                console.print(fused_table)
                
                # 5. Parámetros LLM
                params_info = f"[bold]Modelo:[/bold] {final_model or 'ares:latest'} | [bold]Temp:[/bold] {temperature} | [bold]Think Mode:[/bold] {think}"
                console.print(Panel(params_info, title="🤖 Parámetros de Generación", border_style="blue"))
            # -------------------------------------
            
            # Obtener textos de chunks
            chunks = results.get("semantic", [])[:5]

            if chunks:
                # Comprimir contexto
                context = compress_context(chunks, query=prompt, max_tokens=1500)

                # Generar respuesta con contexto RAG (Streaming + Filtro)
                from modules.ia.apollo.generation import generate_answer_stream
                import sys
                
                llm_model = final_model if final_model else "ares:latest"
                full_response = ""
                
                # Determinar si filtrar think basado en las capacidades del modelo
                from modules.ia.ai_engine import AIEngine
                ai_tmp = AIEngine(obj.config['ai'], str(obj.base_path))
                _, real_model_name = ai_tmp._resolve_provider_and_model(final_model, None)
                
                caps = ai_tmp.get_model_capabilities(real_model_name)
                # Filtrar si no se pide explícitamente pensar, o si el modelo genera tags vacíos (no-thinking)
                should_filter = not think or not caps["thinking"]

                # Ares pensando...
                click.secho("🤖 ARES recuperando y razonando...", fg="cyan", dim=True)
                
                for chunk in generate_answer_stream(
                    query=prompt,
                    context=context,
                    model=llm_model,
                    temperature=temperature,
                    filter_think=should_filter
                ):
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    full_response += chunk
                
                sys.stdout.write("\n")

                # Añadir fuentes si existen
                if results.get("sources"):
                    click.secho("\n📚 Fuentes RAG:", fg="yellow", bold=True)
                    for src in results["sources"][:3]:
                        click.echo(f"- {src.get('path', 'Documento')}")
                
                return
            else:
                messenger.warn(f"No se encontró información relevante en el dataset '{rag}'.")
                
        except Exception as e:
            if "connection" in str(e).lower() or "ollama" in str(e).lower():
                messenger.error("Ollama no está corriendo. No se puede realizar búsqueda semántica.")
            else:
                messenger.error(f"Error en RAG: {e}")
            return

    # Consulta normal sin RAG
    HelpManager(obj).query_ai(
        prompt,
        model_alias=final_model,
        template=template,
        temperature=temperature,
        think=think,
        provider=provider
    )


@cli.command(name="i")
@click.option("--rag", help="Dataset RAG por defecto (default, docs, skills, codigo, config)")
@click.option("--mengraph", is_flag=True, help="Activar motor RAG Memgraph para toda la sesión")
@click.option("--model", "-m", default="ares:latest", help="Modelo LLM")
@click.option("--think", is_flag=True, help="Activar modo pensante (usa ares-think)")
@click.pass_obj
def i_cmd(obj, rag, mengraph, model, think):
    """💬 Modo Interactivo ARES (Loop REPL).
    
    Delega la gestión visual y el loop interactivo al motor de producción industrial.
    """
    from modules.ui.chat_production import start_production_chat
    start_production_chat(obj, rag=rag, model=model, think=think, mengraph=mengraph)


@cli.command(name="maq")
@click.pass_obj
def maq_cmd(obj):
    """🎨 Modo Prueba de Maquetación Industrial V18.
    
    Permite probar el posicionamiento de avatares y cintillos
    usando el motor de inyección binaria directa.
    """
    from modules.ui.industrial_engine import render_industrial_maq
    render_industrial_maq()


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
@click.option("--force", "-f", is_flag=True, help="Forzar limpieza de socket existente")
@click.option("--no-register", is_flag=True, help="No registrar en window_registry (temporal)")
@click.pass_obj
def gs_deploy(obj, name, socket, force, no_register):
    """🚀 Despliega una sesión en una ventana/socket NUEVO.
    
    Por defecto genera un socket ÚNICO automático para cada deploy.
    Esto permite múltiples ventanas de Kitty con sesiones del mismo nombre.
    
    Con --socket: Usa socket personalizado (fijo, no único).
    Con --force: Elimina socket existente incluso si está en uso.
    Con --no-register: No registra en window_registry.
    """
    from modules.tactico.orchestrator import KittyOrchestrator
    from modules.core.socket_manager import cleanup_orphan_socket, generate_unique_socket
    import os

    orch = KittyOrchestrator(obj)

    # 🔧 NUEVO: Generar socket único automático si no se proporciona socket personalizado
    if socket:
        # Socket personalizado - usar tal cual
        target_socket = socket
        click.echo(f"📌 Usando socket personalizado: {target_socket}")
    else:
        # Socket único automático basado en nombre de sesión + timestamp
        target_socket = generate_unique_socket(f"ares_session_{name}")
        click.echo(f"🆔 Socket único generado: {target_socket}")

    # Validación solo si es socket personalizado (los únicos no necesitan cleanup)
    if socket:
        clean_path = target_socket.replace('unix:', '')
        if os.path.exists(clean_path):
            if not force:
                click.echo(f"⚠️  Socket ya existe: {clean_path}")
                click.echo("   Usa --force para limpiar o quita --socket para socket único")
                click.echo("   Usa 'ares socket-check' para diagnosticar")
                return

            click.echo(f"🧹 Limpiando socket existente...")
            success, msg = cleanup_orphan_socket(target_socket, force=True)
            if not success:
                click.echo(f"❌ Error al limpiar: {msg}")
                return

    click.echo(f"🛰️  Desplegando sesión '{name}'...")
    success, msg, used_socket = orch.deploy_session_from_db(
        name, 
        socket=target_socket if socket else None,  # None = usar generado
        new_window=True,
        register=not no_register
    )

    if success:
        click.echo(f"✅ {msg}")
        click.echo(f"🔌 Socket: {used_socket}")
        if not no_register:
            click.echo(f"📋 Registrada en window_registry (usa 'ares windows' para ver)")
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


@gs_cmd.command(name="edit")
@click.argument("name")
@click.pass_obj
def gs_edit(obj, name):
    """✏️  Edita una sesión guardada (títulos y comandos).
    
    Abre el archivo JSON de la sesión en el editor micro para modificar:
      • Títulos de pestañas
      • Comandos de inicialización (usa ';' para separar múltiples)
      • Estructura de ventanas
    
    El sistema valida automáticamente la estructura después de guardar.
    """
    from modules.admon.session_editor import edit_session_interactive
    from rich.console import Console
    
    console = Console()
    
    success, msg = edit_session_interactive(obj, name)
    
    if success:
        console.print(f"\n✅ [green]{msg}[/green]")
        console.print(f"[dim]💡 Usa 'ares gs deploy {name}' para lanzar la sesión editada[/dim]")
    else:
        console.print(f"\n❌ [red]{msg}[/red]")


@cli.command(name="diario")
@click.pass_obj
def diario_cmd(obj):
    """📅 Despliega sesión diaria (alias de 'ares gs deploy diaria').
    
    Atajo para lanzar rápidamente la sesión de trabajo diario configurada en db/diaria.json.
    Equivalente a: ares gs deploy diaria
    
    La sesión 'diaria' puede editarse con: ares diario-edit
    """
    from modules.tactico.orchestrator import KittyOrchestrator
    from modules.core.socket_manager import generate_unique_socket
    from rich.console import Console
    
    console = Console()
    orch = KittyOrchestrator(obj)
    
    # Generar socket único automático
    target_socket = generate_unique_socket("ares_session_diaria")
    console.print(f"🆔 Socket único generado: {target_socket}")
    console.print(f"📅 Desplegando sesión 'diaria'...")
    
    success, msg, used_socket = orch.deploy_session_from_db(
        "diaria",
        socket=None,  # None = usar generado automáticamente
        new_window=True,
        register=True
    )
    
    if success:
        console.print(f"✅ {msg}")
        console.print(f"🔌 Socket: {used_socket}")
        console.print(f"📋 Registrada en window_registry (usa 'ares windows' para ver)")
    else:
        console.print(f"❌ {msg}")


@cli.command(name="diario-edit")
@click.pass_obj
def diario_edit_cmd(obj):
    """✏️  Edita la sesión diaria (alias de 'ares gs edit diaria').
    
    Atajo para editar rápidamente la configuración de la sesión diaria.
    Equivalente a: ares gs edit diaria
    
    Abre db/diaria.json en el editor micro para modificar:
      • Títulos de pestañas
      • Comandos de inicialización
    """
    from modules.admon.session_editor import edit_session_interactive
    from rich.console import Console
    
    console = Console()
    
    success, msg = edit_session_interactive(obj, "diaria")
    
    if success:
        console.print(f"\n✅ [green]{msg}[/green]")
        console.print(f"[dim]💡 Usa 'ares diario' para lanzar la sesión editada[/dim]")
    else:
        console.print(f"\n❌ [red]{msg}[/red]")


@cli.command(name="identidad-inyectar")
@click.pass_obj
def identidad_inyectar_cmd(obj):
    """🧠 Inyecta la Identidad Maestra de ARES en todo el sistema.
    
    Proceso quirúrgico que:
      1. Actualiza la definición en LEEME.md y ares.md (vía TRON).
      2. Inyecta la identidad en los Modelfiles de Ollama.
      3. Recrea los modelos 'ares' y 'ares-think' en Ollama.
    """
    import subprocess
    from pathlib import Path
    
    script_path = Path(obj.base_path) / "scripts/ares_sync_identity.py"
    
    if not script_path.exists():
        click.echo(f"❌ Error: No se encontró el script de sincronización en {script_path}")
        return

    click.echo("🛰️  Iniciando proceso de Inyección de Identidad ARES...")
    # Usar el intérprete de python del venv actual
    python_bin = sys.executable
    subprocess.run([python_bin, str(script_path)])


@cli.command(name="identidad-editar")
@click.pass_obj
def identidad_editar_cmd(obj):
    """✏️  Edita la Identidad Maestra de ARES (ares.yaml).
    
    Abre la configuración de identidad en el editor micro.
    Permite modificar la definición y las rutas de inyección.
    
    IMPORTANTE: Tras editar, ejecuta 'ares identidad-inyectar' para aplicar.
    """
    import subprocess
    from pathlib import Path
    
    yaml_path = Path(obj.base_path) / "config/identidad/ares.yaml"
    
    if not yaml_path.exists():
        click.echo(f"❌ Error: No se encontró el archivo de identidad en {yaml_path}")
        return

    subprocess.run(["micro", str(yaml_path)])
    click.echo("\n✅ [green]Edición finalizada.[/green]")
    click.echo("[dim]💡 Ejecuta 'ares identidad-inyectar' para propagar los cambios.[/dim]")


@cli.command(name="socket-check")
@click.argument("socket-path", required=False)
@click.option("--json", "as_json", is_flag=True, help="Salida en formato JSON")
@click.pass_obj
def socket_check(obj, socket_path, as_json):
    """🔍 Verifica estado de sockets activos.
    
    Sin argumentos: Usa el socket por defecto de config.yaml.
    Con --json: Formato JSON para scripting.
    
    Ejemplos:
      ares socket-check
      ares socket-check unix:/tmp/mykitty
      ares socket-check --json
    """
    from modules.core.socket_manager import get_socket_info, _normalize_socket_path
    import json as json_module
    
    # Usar socket por defecto si no se proporciona
    if not socket_path:
        socket_path = obj.config.get('kitty', {}).get('socket', 'unix:/tmp/mykitty')
    
    # Normalizar para visualización
    normalized = _normalize_socket_path(socket_path)
    
    # Obtener información detallada
    info = get_socket_info(socket_path)
    
    if as_json:
        click.echo(json_module.dumps(info, indent=2))
        return
    
    # Salida formateada con Rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    
    console = Console()
    
    # Panel principal
    status_icon = "✅" if info["is_responsive"] else "❌" if info["exists"] else "⚠️"
    status_text = "Activo" if info["is_responsive"] else "Huérfano" if info["is_orphan"] and info["exists"] else "Inexistente"
    
    panel = Panel(
        f"[bold cyan]Socket:[/bold cyan] {socket_path}\n"
        f"[bold green]Estado:[/bold green] {status_icon} {status_text}",
        title="🔌 Socket Check",
        border_style="cyan" if info["is_responsive"] else "yellow" if info["exists"] else "red"
    )
    console.print(panel)
    
    # Tabla de detalles
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Propiedad", style="cyan")
    table.add_column("Valor", style="green")
    
    table.add_row("Existe:", "✓ Sí" if info["exists"] else "✗ No")
    table.add_row("Es socket UNIX:", "✓ Sí" if info["is_socket"] else "✗ No")
    table.add_row("Responsivo:", "✓ Sí" if info["is_responsive"] else "✗ No")
    table.add_row("Huérfano:", "✓ Sí" if info["is_orphan"] else "✗ No")
    
    if info["permissions"]:
        table.add_row("Permisos:", info["permissions"])
    if info["owner_uid"] is not None:
        table.add_row("Owner UID:", str(info["owner_uid"]))
    if info["error"]:
        table.add_row("Error:", f"[red]{info['error']}[/red]")
    
    console.print(table)

    # Recomendaciones
    if not info["exists"]:
        console.print("\n[yellow]💡 El socket no existe. Kitty no está corriendo con este socket.[/yellow]")
    elif not info["is_responsive"]:
        console.print("\n[yellow]💡 Socket huérfano detectado. Usa 'ares gs deploy --force' para limpiar.[/yellow]")
    elif info["is_responsive"]:
        console.print("\n[green]✓ Socket operativo. Listo para usar.[/green]")


@cli.command(name="windows")
@click.option("--json", "as_json", is_flag=True, help="Salida en formato JSON")
@click.option("--cleanup", "-c", is_flag=True, help="Limpiar ventanas huérfanas")
@click.pass_obj
def windows_cmd(obj, as_json, cleanup):
    """🪟 Lista ventanas Kitty gestionadas por ARES.
    
    Muestra el registro de ventanas con sus sockets asociados.
    Permite identificar qué ventana corresponde a qué sesión.
    
    Con --cleanup: Elimina registros de ventanas cuyos sockets ya no existen.
    Con --json: Formato JSON para scripting.
    
    Ejemplos:
      ares windows
      ares windows --cleanup
      ares windows --json
    """
    from modules.core.window_registry import (
        list_active_windows,
        cleanup_stale_windows,
        get_registry_stats
    )
    import json as json_module
    
    # Limpieza si se solicita
    if cleanup:
        removed = cleanup_stale_windows()
        if removed:
            click.echo(f"🧹 {len(removed)} ventana(s) huérfana(s) eliminada(s):")
            for name in removed:
                click.echo(f"   - {name}")
        else:
            click.echo("✅ No hay ventanas huérfanas")
        if not as_json:
            click.echo()
    
    # Obtener estadísticas
    stats = get_registry_stats()
    
    if as_json:
        windows = list_active_windows()
        click.echo(json_module.dumps({
            "stats": stats,
            "windows": windows
        }, indent=2))
        return
    
    # Salida formateada con Rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    
    console = Console()
    
    # Panel de estadísticas
    panel = Panel(
        f"[bold green]Total registradas:[/bold green] {stats['count']}\n"
        f"[bold cyan]Activas (socket existe):[/bold cyan] {stats['sockets_existentes']}\n"
        f"[bold yellow]Huérfanas (socket no existe):[/bold yellow] {stats['sockets_huerfanos']}",
        title="🪟 Window Registry",
        border_style="cyan"
    )
    console.print(panel)
    
    # Listar ventanas
    windows = list_active_windows()
    
    if not windows:
        console.print("\n[yellow]⚠️  No hay ventanas registradas.[/yellow]")
        console.print("[dim]Usa 'ares gs deploy <nombre>' para crear una.[/dim]")
        return
    
    # Tabla de ventanas
    table = Table(title="Ventanas Activas", show_header=True, header_style="bold magenta")
    table.add_column("Sesión", style="green", width=20)
    table.add_column("Socket", style="cyan", width=50)
    table.add_column("Window ID", style="yellow", width=12)
    table.add_column("Creada", style="white", width=20)
    
    for w in windows:
        # Estado del socket
        import os
        clean_path = w["socket_path"].replace('unix:', '')
        socket_exists = os.path.exists(clean_path)
        status_icon = "✅" if socket_exists else "❌"
        
        session_name = f"{status_icon} {w['session_name']}"
        socket_path = w["socket_path"][:47] + "..." if len(w["socket_path"]) > 50 else w["socket_path"]
        window_id = str(w["window_id"]) if w["window_id"] else "[dim]N/A[/dim]"
        created = w["created_at"][:16].replace('T', ' ')
        
        table.add_row(session_name, socket_path, window_id, created)
    
    console.print(table)
    console.print(f"\n[dim]💡 Usa 'ares gs deploy <nombre>' para crear nueva ventana[/dim]")
    console.print(f"[dim]💡 Usa 'ares gs deploy <nombre> --socket <ruta>' para socket fijo[/dim]")


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


@cli.command(name="gemini")
@click.argument("prompt", nargs=-1, required=False)
@click.option("--chat", "-c", default=None, type=int, help="ID de la sesión")
@click.option("--new", "-n", is_flag=True, help="Forzar nueva sesión")
@click.option("--mengraph", is_flag=True, help="Inyectar CARGA_SISTEMA")
@click.option("--ruta", help="Ruta de Sabiduría Cristalizada")
@click.pass_obj
def gemini_wrapper_cmd(obj, prompt, chat, new, mengraph, ruta):
    """🤖 Gemini Wrapper v3: Sesiones Soberanas y Grafos."""
    from modules.ia.session_mapper import resolve_session_id, get_latest_session_info
    from modules.core.session_db import init_db, register_session
    from modules.ia.gemini_wrapper import invoke_chat
    
    init_db()
    chat_id = resolve_session_id(chat, new)
    original_prompt = " ".join(prompt) if prompt else "Sesión Interactiva"
    
    full_prompt = original_prompt
    if mengraph or ruta:
        from modules.ia.context_router import route_and_assemble
        full_prompt = route_and_assemble(ruta or "CARGA_SISTEMA", full_prompt)

    click.secho(f"🛰️  Invocando Gemini (Session: {chat_id or 'NEW'})...", fg="cyan", dim=True)
    result = invoke_chat(full_prompt, chat_id)
    
    latest = get_latest_session_info()
    if latest:
        register_session(latest["hash"], original_prompt)
    click.echo(result)


@cli.command(name="run")
@click.argument("phase_id")
@click.pass_obj
def run_phase_cmd(obj, phase_id):
    """🚀 Ejecutar Fase de Grafo (INIT/DEV/PROD)."""
    from modules.core.orchestrator import run_lifecycle_phase
    res, meta = run_lifecycle_phase(phase_id)
    if res:
        click.secho(f"🛰️  Fase: {phase_id}", fg="magenta", bold=True)
        click.echo(res.get("ejecucion_soberana"))
    else:
        click.secho(meta, fg="red")


@cli.command(name="sessions")
def sessions_list_cmd():
    """📋 Listado RAW de Sesiones Gemini (Hash-Based)."""
    from modules.core.session_db import get_ares_sessions
    from modules.ia.session_mapper import sync_with_gemini
    ares_db = get_ares_sessions()
    cli_s = {s["hash"]: s["index"] for s in sync_with_gemini()}
    for s in ares_db:
        click.echo(f"{cli_s.get(s['hash'], 'N/A')} | {s['fecha_registro']} | {s['hash']} | {s['titulo']}")


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


# ============================================================================
# GRAFO - Servidor arrows.app (Despachador puro → modules/admon/grafo_manager.py)
# ============================================================================

@cli.command(name="grafo")
@click.option("--port", "-p", default=4200, help="Puerto del servidor (default: 4200)")
@click.option("--no-browser", is_flag=True, help="No abrir navegador")
@click.option("--stop", is_flag=True, help="Detener servidor activo")
@click.option("--status", is_flag=True, help="Ver estado del servidor")
@click.pass_obj
def grafo_cmd(obj, port, no_browser, stop, status):
    """🔷 Servidor arrows.app — Dibujante de Grafos Neo4j.

    Lanza arrows.app en pestaña Kitty + abre navegador (xdg-open).

    Cierre (3 métodos):
      1) Cerrar pestaña Kitty → SIGTERM
      2) Ctrl+C en pestaña → SIGINT
      3) ares grafo --stop → kill PID + pgrep

    Ejemplos:
      ares grafo            # Puerto 4200, abre navegador
      ares grafo -p 8080    # Puerto personalizado
      ares grafo --stop     # Detener servidor
      ares grafo --status   # Ver estado
    """
    if stop:
        result = stop_grafo_server()
    elif status:
        result = check_grafo_status()
    else:
        result = start_grafo_server(obj, port=port, no_browser=no_browser)

    click.echo(result.get("msg", ""))


# ============================================================================
# MEM - Gestión de Memgraph (Docker + Graph Database)
# ============================================================================

@cli.group(name="mem", invoke_without_command=True)
@click.pass_context
def mem_cmd(ctx):
    """🗃️  Memgraph: Graph Database + Memgraph Lab (UI).

    Subcomandos:
      start  - Iniciar Docker daemon + contenedores Memgraph
      stop   - Detener contenedores Memgraph
      status - Ver estado de Docker y contenedores

    Servicios:
      memgraph-mage  - Base de datos graph (bolt://localhost:7687)
      memgraph-lab   - UI web (http://localhost:3000)

    Ejemplos:
      ares mem start    # Iniciar todo
      ares mem stop     # Detener contenedores
      ares mem status   # Ver estado
      ares mem          # Equivale a: ares mem status
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(mem_status_cmd)


@mem_cmd.command(name="start")
def mem_start_cmd():
    """🚀 Iniciar Docker daemon + Memgraph (Mage + Lab)."""
    result = start_memgraph()
    click.echo(result.get("msg", ""))


@mem_cmd.command(name="stop")
def mem_stop_cmd():
    """🛑 Detener contenedores Memgraph."""
    result = stop_memgraph()
    click.echo(result.get("msg", ""))


@mem_cmd.command(name="status")
def mem_status_cmd():
    """📊 Ver estado de Docker y contenedores Memgraph."""
    result = memgraph_status()
    click.echo(result.get("msg", ""))


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


# ============================================================================
# AGENTES - Despachador de Sub-Agentes Standalone
# ============================================================================

@cli.group(name="agente")
@click.pass_obj
def agente(obj):
    """🤖 Despachador de Sub-Agentes Standalone.
    
    Ejecuta sub-agentes especializados de forma independiente.
    Cada sub-agente es una aplicación autónoma con su propia UI/CLI.
    
    Usa: ares agente [nombre_agente]
    
    Sub-Agentes Disponibles:
      AgenteDeCambio  - Interfaz TUI híbrida (90% Textual + 10% Ratatui)
      sherlok         - Auditor de código con ADN Técnico Industrial
      tron            - Orquestador de modelos Cloud (DeepSeek/OpenRouter)
    
    Ejemplos:
      ares agente AgenteDeCambio run      - Ejecutar AgenteDeCambio TUI
      ares agente tron --router           - Menú interactivo de OpenRouter
      ares agente sherlok                 - Ejecutar auditoría Sherlok
    """
    pass


# ============================================================================
# TRON - Orquestador de IA Multi-provider
# ============================================================================

@agente.command(name="tron", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
def agente_tron(ctx):
    """🤖 TRON: Orquestador de IA Multi-provider (DeepSeek/OpenRouter).
    
    Permite interactuar con modelos de nube de forma transparente.
    Equivalente al comando 'tron' o 'tronAres'.
    
    Uso: ares agente tron [opciones] [perfil] [modelo] [comando]
    
    Ejemplos:
      ares agente tron --router           - Menú interactivo
      ares agente tron openrouter claude  - Iniciar chat con Claude
    """
    from modules.admon.init_manager import get_binary_path
    
    # Ruta al script real de tron
    # Usando la ruta detectada en la investigación inicial
    tron_script = "/home/daniel/tron/programas/TR/AGENTES/sub-agentes/TRON/bin/tron.py"
    
    if not os.path.exists(tron_script):
        # Intentar ruta alternativa
        tron_script = "/home/daniel/tron/programas/ProyectoPizza/TRON/bin/tron.py"
        
    if not os.path.exists(tron_script):
        click.echo("❌ Error: No se encontró el script de TRON.")
        return

    # Ejecutar tron con los argumentos pasados
    cmd = ["uv", "run", "--project", os.path.dirname(tron_script), "python", tron_script] + ctx.args
    subprocess.run(cmd)


# ============================================================================
# SHERLOK - Auditor de código
# ============================================================================

@agente.command(name="sherlok", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
def agente_sherlok(ctx):
    """🔍 SHERLOK: Auditor de código con ADN Técnico Industrial.
    
    Analiza la base de código para detectar fallos, sugerir mejoras
    y auditar la modularidad industrial.
    
    Uso: ares agente sherlok [opciones]
    
    Ejemplos:
      ares agente sherlok run             - Iniciar auditoría completa
      ares agente sherlok status          - Ver estado de auditorías previas
    """
    # Ruta al script real de sherlok
    sherlok_script = "/home/daniel/tron/programas/TR/AGENTES/sub-agentes/sherlok/main.py"
    
    if not os.path.exists(sherlok_script):
        click.echo("❌ Error: No se encontró el script de SHERLOK.")
        return

    # Ejecutar sherlok con los argumentos pasados
    cmd = ["uv", "run", "--project", os.path.dirname(sherlok_script), "python", sherlok_script] + ctx.args
    subprocess.run(cmd)


# ============================================================================
# AGENTE DE CAMBIO - Sub-agente TUI Híbrido (90% Textual + 10% Ratatui)
# ============================================================================

@agente.command(name="AgenteDeCambio")
@click.argument("accion", default="run", type=click.Choice(["run", "test", "install", "status"]))
@click.pass_obj
def agente_agente_de_cambio(obj, accion):
    """🤖 AgenteDeCambio: Interfaz TUI híbrida para extracción cognitiva.
    
    Interfaz 90% Textual + 10% Ratatui con prompts vivos, métricas de deriva
    y modo dual chat/cuestionario.
    
    ACCION:
      run     - Ejecutar interfaz TUI completa (default)
      test    - Test de componentes Rust/Textual
      install - Instalar componentes Rust (Ratatui)
      status  - Verificar estado de instalación
    
    Ejemplo:
      ares agente AgenteDeCambio run      - Ejecutar TUI
      ares agente AgenteDeCambio test     - Test componentes
      ares agente AgenteDeCambio install  - Instalar Rust
      ares agente AgenteDeCambio status   - Verificar estado
    """
    if accion == "run":
        from modules.ui.agente_de_cambio import run_demo
        run_demo()
    elif accion == "test":
        from modules.ui.agente_de_cambio import run_tests
        run_tests()
    elif accion == "install":
        from modules.ui.agente_de_cambio import install_rust_components
        install_rust_components()
    elif accion == "status":
        from modules.ui.agente_de_cambio import show_status
        show_status()


# ============================================================================
# APOLLO - Sistema RAG T0-T4 (Kùzu / SQLite-vec)
# ============================================================================

@cli.group(name="apollo")
def apollo_cmd():
    """🧠 Sistema RAG Apollo: Recuperación de contexto documental.
    
    Usa motor Kùzu + SQLite-vec para búsqueda semántica y relacional.
    """
    pass

@apollo_cmd.command(name="cartografo")
@click.pass_obj
def apollo_cartografo_cmd(obj):
    """🗺️  Modo Cartógrafo: Gestión conversacional del conocimiento."""
    try:
        rag = RAGOrchestrator()
        rag.run_cartografo()
    except Exception as e:
        click.echo(f"❌ Error iniciando Cartógrafo: {e}")

@apollo_cmd.command(name="ingest")
@click.argument("path")
@click.option("--doc-type", "-t", help="Tipo de documento")
@click.pass_obj
def apollo_ingest_cmd(obj, path, doc_type):
    """📥 Indexar documento en el sistema RAG Apollo."""
    try:
        rag = RAGOrchestrator()
        result = rag.ingest_document(path, doc_type)
        click.echo(f"✅ Documento indexado: {result}")
    except Exception as e:
        click.echo(f"❌ Error indexando: {e}")

# ============================================================================
# MENGRAPH - Sistema RAG de Grafos en RAM (Memgraph)
# ============================================================================

@cli.group(name="mengraph")
def mengraph_cmd():
    """🕸️  Sistema RAG Mengraph: Consultas estructuradas al Grafo en RAM."""
    pass

@mengraph_cmd.command(name="ingest")
@click.argument("text")
@click.option("--label", "-l", help="Etiqueta opcional para el nodo principal")
@click.pass_obj
def mengraph_ingest_cmd(obj, text, label):
    """📥 Ingestar conocimiento en el Grafo (Memgraph)."""
    try:
        from modules.rag_mengraph.extraction.processor import MengraphProcessor
        ontology = f"{obj.base_path}/config/rag_mengraph/ontology_master.json"
        processor = MengraphProcessor(ontology)
        
        click.echo(f"🧠 Procesando: \"{text[:50]}...\"")
        result = processor.process_and_store(text, manual_label=label)
        
        if result['status'] == 'success':
            click.secho(f"✅ Éxito: Se crearon/actualizaron {result['nodes']} nodos y {result['edges']} relaciones.", fg="green")
        else:
            click.echo(f"❌ Error en procesamiento: {result['message']}")
    except Exception as e:
        click.echo(f"❌ Error fatal en ingesta: {e}")

@mengraph_cmd.command(name="query")
@click.argument("text")
@click.option("--top-k", default=5, help="Número de resultados")
@click.option("--mode", type=click.Choice(['deterministic', 'hybrid']), default='hybrid', help="Switche Cognitivo: determinista (léxico) o híbrido (semántico)")
@click.option("--json", "as_json", is_flag=True, help="Salida en formato JSON puro")
@click.pass_obj
def mengraph_query_cmd(obj, text, top_k, mode, as_json):
    """🔍 Consultar el Grafo V9 (Switche Determinista-Híbrido)."""
    from modules.rag_mengraph.core.tool import MengraphTool
    tool = MengraphTool()
    
    result_json = tool.query_json(text, top_k=top_k, mode=mode)
    
    if as_json:
        click.echo(result_json)
    else:
        import json
        data = json.loads(result_json)
        if data['status'] == 'success':
            click.secho(f"🧠 Modo: {data['mode'].upper()}", fg="magenta", bold=True)
            for item in data['data']:
                click.secho(f"📍 Concepto: {item['concept']}", fg="cyan")
                click.echo(f"   Ref: {item['file']} (Líneas {item['lines']})")
        else:
            click.echo(f"❌ Error: {data['message']}")

@mengraph_cmd.command(name="schema")
@click.pass_obj
def mengraph_schema_cmd(obj):
    """📜 Mostrar el esquema MAGE del grafo."""
    from modules.rag_mengraph.core.tool import MengraphTool
    tool = MengraphTool()
    click.echo(tool.get_schema_summary())

@mengraph_cmd.command(name="stats")
@click.pass_obj
def mengraph_stats_cmd(obj):
    """📊 Estadísticas rápidas de la taxonomía V9."""
    from modules.rag_mengraph.core.tool import MengraphTool
    tool = MengraphTool()
    click.echo(tool.quick_stats())



# ============================================================================

if __name__ == "__main__":
    cli()

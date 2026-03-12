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

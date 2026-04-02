"""Chat Interface: Orquestación Blindada con Streaming y Mcat.

Gestiona el flujo de IA con streaming en tiempo real y usa
mcat como contenedor para la maquetación final.
"""

import click
import sys
import time
from modules.ia.apollo.emoji_manager import get_asset_render, get_layout_config, get_asset_path
from modules.ui.mcat_render import render_block_with_mcat
from modules.ia.ai_engine import AIEngine

def start_interactive_chat(obj, rag=None, model="ares:latest", think=False):
    """Loop interactivo blindado."""
    cfg = get_layout_config()
    ares_color = cfg.get('colors', {}).get('ares_text', 'cyan')
    
    click.clear()
    click.secho("🛰️ NÚCLEO ARES ACTIVO | CONTENEDOR MCAT", fg=ares_color, bold=True)

    while True:
        try:
            # --- TURNO USUARIO ---
            user_icon = get_asset_render("user", mode="history")
            user_input = click.prompt(f"{user_icon} ❯", type=str, prompt_suffix=" ")

            if user_input.strip() in ("/quit", "/exit"): break
            if not user_input.strip(): continue

            # --- GENERAR RESPUESTA (Visión IA con Streaming) ---
            engine = AIEngine(obj.config['ai'], str(obj.base_path))
            
            # Determinar capacidades dinámicas del modelo
            provider, real_model = engine._resolve_provider_and_model(model, None)
            caps = engine.get_model_capabilities(real_model)
            
            # Filtrar si no se pide pensar o el modelo no es pensante
            filter_think = not think or not caps["thinking"]
            
            if filter_think:
                engine.reset_think_filter()

            click.secho(f"🤖 [ARES con {real_model or model}]...", fg="yellow", dim=True, nl=False)
            
            full_response = ""
            for chunk in engine.ask_stream(user_input, model_alias=model, filter_think=filter_think):
                if chunk:
                    # Imprimir primer token borrando el "Pensando..."
                    if not full_response:
                        sys.stdout.write("\r" + " " * 40 + "\r") # Limpiar línea
                        
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    full_response += chunk
            
            sys.stdout.write("\n")
            
            # --- RENDERIZADO FINAL CON MCAT (Contenedor Robusto) ---
            # Obtenemos el path físico desde el gestor de emojis
            ares_wow_path = get_asset_path("ares", mode="live")
            
            # Delegación al contenedor robusto mcat para el bloque final
            render_block_with_mcat(full_response, image_path=ares_wow_path, title="ARES-IA")

        except (KeyboardInterrupt, EOFError):
            break

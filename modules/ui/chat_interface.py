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

            # --- GENERAR RESPUESTA (Visión IA) ---
            engine = AIEngine(obj.config['ai'], str(obj.base_path))
            
            click.secho(f"🤖 [Pensando con {model}]...", fg="yellow", dim=True)
            
            response = engine.ask(user_input, model_alias=model)
            
            # --- RENDERIZADO FINAL CON MCAT ---
            # Obtenemos el path físico desde el gestor de emojis
            ares_wow_path = get_asset_path("ares", mode="live")
            
            # Delegación al contenedor robusto mcat
            render_block_with_mcat(response, image_path=ares_wow_path, title="ARES-IA")

        except (KeyboardInterrupt, EOFError):
            break

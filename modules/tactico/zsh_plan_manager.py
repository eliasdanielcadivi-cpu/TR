import os
import subprocess
from rich.console import Console

console = Console()

def deploy_zsh_plan(kitty, ctx):
    """
    Despliegue táctico ZSH Plan: Sesión de IA con Oh My Zsh.
    """
    console.print("[bold green]🚀 Iniciando Protocolo ZSH Plan (ARES AI Session)...[/bold green]")
    
    # 1. Definir pestañas y comandos
    tabs = [
        {"title": "TRAIN", "color": "#39FF14", "bg": "#0A1A0A", "path": "~/proyectos/ia"},
        {"title": "DATA", "color": "#00FFFF", "bg": "#001A1A", "path": "~/datasets"},
        {"title": "MODELS", "color": "#FF00FF", "bg": "#1A001A", "path": "~/models"},
        {"title": "LOGS", "color": "#FF0000", "bg": "#1A0000", "path": "~/logs"},
    ]

    # Asegurar que los directorios existen (o al menos no romper si no)
    for tab in tabs:
        full_path = os.path.expanduser(tab['path'])
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)

    # 2. Lanzar pestañas
    for tab in tabs:
        # Lanzar pestaña con zsh soberano (encapsulado en TR/config/zsh)
        zdotdir = os.path.join(ctx.base_path, "config/zsh")
        kitty.run([
            "launch", 
            "--type=tab", 
            f"--tab-title={tab['title']}", 
            f"--cwd={tab['path']}",
            f"env", f"ZDOTDIR={zdotdir}", "zsh"
        ])
        
        # Aplicar color a la pestaña recién creada
        # Nota: kitty @ set-tab-color aplica a la pestaña activa
        kitty.run([
            "set-tab-color",
            f"active_fg={tab['color']}",
            f"active_bg={tab['bg']}",
            f"inactive_fg={tab['color']}",
            f"inactive_bg={tab['bg']}"
        ])

    # 3. Cerrar la pestaña inicial si es solo una terminal vacía (opcional)
    # console.print("[dim]Pestañas configuradas con éxito.[/dim]")
    return True

import os
import sys
from rich.console import Console
from .diag_manager import show_status # Reutilizar lógica de diagnóstico

console = Console()

def manage_config(obj, **kwargs):
    """Despachador central de inicialización y configuración."""
    from .init_manager_logic import create_symlink, reload_config, get_status, unlink_config
    
    tr_conf = os.path.join(obj.base_path, 'config/kitty.conf')
    user_conf = os.path.expanduser('~/.config/kitty/kitty.conf')
    
    if kwargs.get('link'):
        res = create_symlink(tr_conf, user_conf)
        console.print(f"[bold green]Link:[/bold green] {res['message']}")
    elif kwargs.get('unlink'):
        res = unlink_config(user_conf)
        console.print(f"[bold red]Unlink:[/bold green] {res['message']}")
    elif kwargs.get('reload'):
        res = reload_config(obj.socket, tr_conf)
        console.print(f"[bold cyan]Reload:[/bold cyan] {res['message']}")
    else:
        # Por defecto muestra estado detallado
        res = get_status(tr_conf, user_conf, obj.socket)
        console.print("[bold magenta]Estado de ARES verificado.[/bold magenta]")

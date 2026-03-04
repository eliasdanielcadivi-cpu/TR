import json
from rich.console import Console
from rich.table import Table
from config import KittyRemote

console = Console()

def show_status(context):
    """Muestra el diagnóstico del sistema ARES."""
    kitty = KittyRemote(context)
    table = Table(title="ARES System Status")
    table.add_column("Componente", style="cyan")
    table.add_column("Estado", style="magenta")
    
    # Estado del Socket
    running = kitty.is_running()
    table.add_row("Socket Kitty", "ACTIVO" if running else "DESCONECTADO")
    
    # Estado de Pestañas
    if running:
        state_res = kitty.run(["ls"])
        state = json.loads(state_res) if state_res else None
        tabs_count = sum(len(w.get('tabs', [])) for w in state) if state else 0
        table.add_row("Pestañas Abiertas", str(tabs_count))
    else:
        table.add_row("Pestañas Abiertas", "-")
        
    console.print(table)

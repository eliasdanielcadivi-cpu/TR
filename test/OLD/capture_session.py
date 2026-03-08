#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

# --- CONFIGURACIÓN DE RUTA PARA IMPORTAR MÓDULOS ---
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

try:
    from config import TRContext, KittyRemote
    from rich.console import Console
    from rich.table import Table
except ImportError:
    print("Error: No se pudieron importar los módulos de ARES. Asegúrate de estar en el entorno correcto.")
    sys.exit(1)

console = Console()

def capture_session():
    """Lee el socket de Kitty y captura la estructura de ventanas y pestañas."""
    ctx = TRContext()
    kitty = KittyRemote(ctx)
    
    if not kitty.is_running():
        console.print(f"[bold red]Error:[/bold red] El socket {ctx.socket_path} no existe. Kitty no parece estar corriendo con ARES.")
        return

    # Obtener el estado actual de Kitty en formato JSON
    # 'ls' devuelve toda la jerarquía: Ventanas OS -> Pestañas -> Ventanas
    raw_ls = kitty.run(["ls"])
    if not raw_ls:
        console.print("[bold red]Error:[/bold red] No se pudo obtener información del socket.")
        return

    try:
        session_data = json.loads(raw_ls)
    except json.JSONDecodeError:
        console.print("[bold red]Error:[/bold red] Error al decodificar la respuesta JSON de Kitty.")
        return

    # Estructura para guardar en DB (según deseo del usuario)
    summary = []

    table = Table(title="Captura de Sesión ARES (Kitty)")
    table.add_column("OS Window ID", justify="center", style="cyan")
    table.add_column("Tab ID", justify="center", style="magenta")
    table.add_column("Tab Title", style="green")
    table.add_column("Active", justify="center")

    for os_window in session_data:
        os_id = os_window.get('id')
        os_focused = os_window.get('is_focused', False)
        
        tabs_info = []
        for tab in os_window.get('tabs', []):
            tab_id = tab.get('id')
            tab_title = tab.get('title')
            is_active = tab.get('is_active', False)
            
            table.add_row(
                str(os_id) if os_focused else f"{os_id} (bg)",
                str(tab_id),
                tab_title,
                "✓" if is_active else ""
            )
            
            tabs_info.append({
                "tab_id": tab_id,
                "title": tab_title,
                "is_active": is_active
            })
            
        summary.append({
            "os_window_id": os_id,
            "is_focused": os_focused,
            "tabs": tabs_info
        })

    console.print(table)
    
    # Simulación de guardado en DB (JSON)
    db_path = os.path.join(ctx.base_path, "db/last_session.json")
    with open(db_path, "w") as f:
        json.dump(summary, f, indent=4)
    
    console.print(f"\n[bold green]Éxito:[/bold green] Sesión capturada y guardada en [blue]{db_path}[/blue]")
    console.print(f"Total ventanas OS: {len(session_data)}")
    console.print(f"Total pestañas detectadas: {sum(len(w['tabs']) for w in session_data)}")

if __name__ == "__main__":
    capture_session()

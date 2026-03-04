import os
import time
from rich.console import Console

try:
    from modules.color import ColorEngine
except ImportError:
    ColorEngine = None

console = Console()

def launch_tab(kitty, title, colors, cmd=None):
    """Lanza una pestaña y le aplica colores tácticos."""
    # 1. Lanzar pestaña
    args = ["launch", "--type=tab", f"--tab-title={title}"]
    if cmd:
        args.append(cmd)
    
    kitty.run(args)
    
    # 2. Aplicar colores (Si el motor de color está disponible)
    # Nota: set-tab-color necesita un target, por defecto es la activa
    if colors:
        color_cmd = [
            "set-tab-color",
            f"active_fg={colors['active_fg']}",
            f"inactive_fg={colors['inactive_fg']}",
            f"active_bg={colors['active_bg']}",
            f"inactive_bg={colors['inactive_bg']}"
        ]
        kitty.run(color_cmd)

def deploy_plan(kitty, ctx):
    """
    Ejecuta el plan maestro: 4 pestañas de alto rendimiento.
    """
    console.print("[bold cyan]🚀 Iniciando Protocolo ARES...[/bold cyan]")
    
    # Definición de Colores (Hacker Neon)
    # Estos valores deberían venir de COLOR_SYSTEM.md, los hardcodeo por seguridad
    PALETTE = {
        'CYBERPUNK': {'active_fg': '#00FFFF', 'inactive_fg': '#00AAAA', 'active_bg': '#001A1A', 'inactive_bg': '#000D0D'},
        'NEON_GODDESS': {'active_fg': '#FF00FF', 'inactive_fg': '#AA00AA', 'active_bg': '#1A001A', 'inactive_bg': '#0D000D'},
        'MATRIX': {'active_fg': '#39FF14', 'inactive_fg': '#22AA00', 'active_bg': '#0A1A0A', 'inactive_bg': '#050D05'},
        'BLADE_RUNNER': {'active_fg': '#FF6600', 'inactive_fg': '#AA4400', 'active_bg': '#1A0D00', 'inactive_bg': '#0D0600'}
    }

    # 1. CYBERPUNK (Control) - Ya existe (la ventana inicial), solo colorear
    # Renombrar primera pestaña
    kitty.run(["set-tab-title", "CONTROL"])
    kitty.run([
        "set-tab-color",
        f"active_fg={PALETTE['CYBERPUNK']['active_fg']}",
        f"active_bg={PALETTE['CYBERPUNK']['active_bg']}"
    ])

    # 2. NEON GODDESS (Visualización/IA)
    launch_tab(kitty, "VISUAL", PALETTE['NEON_GODDESS'])

    # 3. MATRIX (Código/Logs)
    launch_tab(kitty, "MATRIX", PALETTE['MATRIX'])

    # 4. BLADE RUNNER (Multimedia/Comms)
    launch_tab(kitty, "COMMS", PALETTE['BLADE_RUNNER'])

    # Handshake
    handshake_path = os.path.join(ctx.base_path, "data/handshake")
    with open(handshake_path, "w") as f:
        f.write(str(time.time()))
    
    return True

def verify_handshake(handshake_file):
    return os.path.exists(handshake_file)

"""
Plan Module - Orquestador Táctico de Pestañas
==============================================

Módulo independiente para desplegar flujos de trabajo con pestañas coloreadas.
Sigue la regla de modularidad TRON: máximo 3 funciones públicas.

Funciones:
1. launch_tab(title, colors, command) - Lanza pestaña con colores Hacker Neon
2. deploy_plan(kitty_remote, ctx) - Ejecuta plan maestro con 4 pestañas
3. verify_handshake(handshake_file) - Verifica que todo esté online

Colores Hacker Neon (TESTEADOS):
- active_fg: Texto neón brillante (cuando activa)
- inactive_fg: Texto neón (cuando inactiva)  
- active_bg: Fondo oscuro del color (cuando activa)
- inactive_bg: Fondo más oscuro (cuando inactiva)
"""

import os
import time
from rich.console import Console

console = Console()


def launch_tab(kitty_remote, title, colors, command=""):
    """
    Lanza pestaña con colores Hacker Neon espectaculares.

    Args:
        kitty_remote: Instancia KittyRemote
        title: Título de la pestaña
        colors: Dict con active_fg, inactive_fg, active_bg, inactive_bg
        command: Comando a ejecutar (opcional)
    """
    # Lanzar pestaña
    win_id = kitty_remote.run(["launch", "--type=tab", "--tab-title", title])
    if not win_id:
        return

    time.sleep(0.5)

    # Aplicar colores con set-tab-color (4 componentes)
    color_args = [
        "set-tab-color",
        "--match", f"id:{win_id}",
        f"active_fg={colors['active_fg']}",
        f"inactive_fg={colors['inactive_fg']}",
        f"active_bg={colors['active_bg']}",
        f"inactive_bg={colors['inactive_bg']}"
    ]
    kitty_remote.run(color_args)

    time.sleep(0.3)

    # Ejecutar comando si hay
    if command:
        kitty_remote.run(["send-text", "--match", f"id:{win_id}", f"{command}\n"])


def deploy_plan(kitty_remote, ctx):
    """
    Ejecuta el plan maestro con las 4 pestañas más bonitas del mundo hacker.

    Paleta de colores:
    - CYBERPUNK: Cyan eléctrico sobre fondo espacio profundo
    - NEON GODDESS: Fuchsia vibrante sobre noche oscura
    - MATRIX GREEN: Verde código sobre negro absoluto
    - BLADE RUNNER: Ámbar anaranjado sobre sombra

    Args:
        kitty_remote: Instancia KittyRemote
        ctx: Contexto TRON

    Returns:
        True si handshake exitoso
    """
    if os.path.exists(ctx.handshake_file):
        os.remove(ctx.handshake_file)

    console.print("[bold cyan]🛰  Desplegando Plan Tron - Edición Hacker Neon...")
    console.print("")

    # ═══════════════════════════════════════════════════════════════════════════
    # PESTAÑA 1: CYBERPUNK HUB - Centro de comando principal
    # ═══════════════════════════════════════════════════════════════════════════
    # Cyan eléctrico (#00FFFF) sobre fondo espacio profundo (#001A1A)
    colors_cyberpunk = {
        'active_fg': '#00FFFF',      # Cyan eléctrico brillante
        'inactive_fg': '#00AAAA',    # Cyan oscuro
        'active_bg': '#001A1A',      # Fondo cyan muy oscuro
        'inactive_bg': '#000D0D'     # Fondo casi negro
    }
    console.print("[bold magenta]▶  Lanzando CYBERPUNK HUB...[/bold magenta]")
    launch_tab(
        kitty_remote,
        "CYBERPUNK",
        colors_cyberpunk,
        f"echo '╔════════════════════════════════════════╗'; "
        f"echo '║  🛰  CYBERPUNK COMMAND CENTER  ║'; "
        f"echo '╚════════════════════════════════════════╝'; "
        f"echo ''; "
        f"echo '💾 Sistema: ONLINE'; "
        f"echo '🌐 Red: Conectada'; "
        f"echo '🔒 Seguridad: Activa'; "
        f"echo ''; "
        f"echo '--- Tron Hub Online ---'; "
        f"echo 'ALIVE' > {ctx.handshake_file}"
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # PESTAÑA 2: NEON GODDESS - Diagnóstico y recursos
    # ═══════════════════════════════════════════════════════════════════════════
    # Fuchsia vibrante (#FF00FF) sobre noche oscura (#1A001A)
    colors_neon = {
        'active_fg': '#FF00FF',      # Fuchsia eléctrico
        'inactive_fg': '#AA00AA',    # Fuchsia oscuro
        'active_bg': '#1A001A',      # Fondo fuchsia muy oscuro
        'inactive_bg': '#0D000D'     # Fondo casi negro
    }
    console.print("[bold yellow]▶  Lanzando NEON GODDESS...[/bold yellow]")
    launch_tab(
        kitty_remote,
        "NEON GODDESS",
        colors_neon,
        "echo '╔════════════════════════════════════════╗'; "
        "echo '║  💎  NEON GODDESS DIAGNOSTICS  ║'; "
        "echo '╚════════════════════════════════════════╝'; "
        "echo ''; "
        "echo '📊 RECURSOS DEL SISTEMA:'; "
        "echo ''; "
        "ls -F; "
        "echo ''; "
        "df -h | head -5; "
        "echo ''; "
        "free -m | head -3"
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # PESTAÑA 3: MATRIX GREEN - Terminal de código
    # ═══════════════════════════════════════════════════════════════════════════
    # Verde código (#39FF14) sobre negro absoluto (#0A1A0A)
    colors_matrix = {
        'active_fg': '#39FF14',      # Verde matrix brillante
        'inactive_fg': '#22AA00',    # Verde oscuro
        'active_bg': '#0A1A0A',      # Fondo verde muy oscuro
        'inactive_bg': '#050D05'     # Fondo casi negro
    }
    console.print("[bold green]▶  Lanzando MATRIX GREEN...[/bold green]")
    launch_tab(
        kitty_remote,
        "MATRIX",
        colors_matrix,
        "echo '╔════════════════════════════════════════╗'; "
        "echo '║  🌿  MATRIX CODE TERMINAL  ║'; "
        "echo '╚════════════════════════════════════════╝'; "
        "echo ''; "
        "echo '👾 Welcome to the Matrix...'; "
        "echo ''; "
        "echo 'Sigue al conejo blanco 🐇'; "
        "echo ''; "
        "neofetch --stdout 2>/dev/null || echo '📦 Instala neofetch para info del sistema'"
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # PESTAÑA 4: BLADE RUNNER - Multimedia y logs
    # ═══════════════════════════════════════════════════════════════════════════
    # Ámbar anaranjado (#FF6600) sobre sombra (#1A0D00)
    colors_blade = {
        'active_fg': '#FF6600',      # Ámbar neón
        'inactive_fg': '#AA4400',    # Ámbar oscuro
        'active_bg': '#1A0D00',      # Fondo ámbar muy oscuro
        'inactive_bg': '#0D0600'     # Fondo casi negro
    }
    console.print("[bold red]▶  Lanzando BLADE RUNNER...[/bold red]")

    # Ruta de video de prueba
    video_path = "/home/daniel/Descargas/The Pendragon Cycle Rise Of The Merlin S01E03 E3 A Fatherless Child 1080p DLWP WEB-DL AAC2 0 H 264-DJT[EZTVx.to].mkv"
    image_path = f"{ctx.base_path}/assets/2026-02-26_12-48.png"

    launch_tab(
        kitty_remote,
        "BLADE RUNNER",
        colors_blade,
        f"echo '╔════════════════════════════════════════╗'; "
        f"echo '║  🎬  BLADE RUNNER MULTIMEDIA ║'; "
        f"echo '╚════════════════════════════════════════╝'; "
        f"echo ''; "
        f"echo '🎥 Multimedia Ready'; "
        f"echo '📺 Video: {video_path}'; "
        f"echo '🖼️  Imagen: {image_path}'; "
        f"echo ''; "
        f"echo 'Usa: tr-video <ruta> para reproducir'; "
        f"echo 'Usa: kitty +kitten icat <ruta> para imágenes'"
    )

    # Esperar que todo esté listo
    time.sleep(1.5)

    # Verificar handshake
    handshake_ok = os.path.exists(ctx.handshake_file)

    console.print("")
    if handshake_ok:
        console.print("[bold green]✔ Plan completado con éxito - 4 pestañas hacker neón activas[/bold green]")
    else:
        console.print("[bold yellow]⚠ Handshake no detectado - Verifica CYBERPUNK tab[/bold yellow]")

    return handshake_ok


def verify_handshake(handshake_file):
    """
    Verifica que el handshake file exista.

    Args:
        handshake_file: Ruta al archivo de handshake

    Returns:
        True si existe, False si no
    """
    return os.path.exists(handshake_file)

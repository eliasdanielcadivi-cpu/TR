import os
from rich.console import Console

console = Console()

def launch_mcat_tab(kitty, title, colors, cmd=None):
    """Lanza una pestaña mcat con identidad visual neon y comando shell."""
    args = ["launch", "--type=tab", f"--tab-title={title}"]
    if cmd:
        # Usar zsh para ejecutar y mantener el prompt interactivo
        args.append("zsh")
        args.append("-c")
        args.append(f"{cmd}; exec zsh")

    kitty.run(args)
    if colors:
        color_cmd = [
            "set-tab-color",
            f"active_fg={colors['active_fg']}",
            f"active_bg={colors['active_bg']}"
        ]
        kitty.run(color_cmd)

def deploy_mcat_demo(kitty, ctx):
    """🚩 MEGA-DEMO Mcat: Despliegue Exhaustivo en 7 Fases.
    
    Lanza una suite completa de pestañas didácticas en español para 
    dominar Mcat desde ARES.
    """
    console.print("[bold cyan]🚀 Iniciando Mega-Protocolo MCAT (Despliegue Maestro)...[/bold cyan]")
    
    PALETTE = {
        'GUIA': {'active_fg': '#FFFFFF', 'active_bg': '#333333'}, # Gris/Blanco (Manual)
        'DOCS': {'active_fg': '#00FFFF', 'active_bg': '#001A1A'}, # Cian (Cerebro)
        'CODE': {'active_fg': '#39FF14', 'active_bg': '#0A1A0A'}, # Verde (Matrix)
        'MEDIA': {'active_fg': '#FF00FF', 'active_bg': '#1A001A'}, # Fuchsia (Neon)
        'CONVERT': {'active_fg': '#FFFF00', 'active_bg': '#1A1A00'}, # Amarillo (Energía)
        'INTERACTIVE': {'active_fg': '#FF6600', 'active_bg': '#1A0D00'}, # Naranja (Táctico)
        'LS': {'active_fg': '#00AAAA', 'active_bg': '#000D0D'} # Azul oscuro (Sistema)
    }
    
    assets = os.path.join(ctx.base_path, "assets/mcat-demo")
    
    # --- 1. GUÍA DE OPERACIONES (El Manual) ---
    cmd1 = f"clear && mcat {assets}/mcat-guia.md"
    launch_mcat_tab(kitty, "📖 GUÍA-OPERACIONES", PALETTE['GUIA'], cmd1)
    
    # --- 2. DOCUMENTOS OFIMÁTICA (PDF/Office) ---
    cmd2 = (
        f"clear && echo '--- VISUALIZACIÓN DE PDF ---' && mcat {assets}/demo-documento.pdf && "
        f"echo '\n--- CONVERSIÓN DE OFFICE (DOCX) ---' && mcat {assets}/archivo-demo.docx"
    )
    launch_mcat_tab(kitty, "📄 DOCS-OFIMÁTICA", PALETTE['DOCS'], cmd2)
    
    # --- 3. BATERÍA DE CÓDIGO (Resaltado de Sintaxis) ---
    cmd3 = (
        f"clear && echo '--- BASH TACTICAL (Highlighter) ---' && mcat {assets}/sh-codigo.sh -t monokai && "
        f"echo '\n--- PYTHON ASYNC (Modern Syntax) ---' && mcat {assets}/py-codigo.py && "
        f"echo '\n--- RUST SERVER (Error Handling) ---' && mcat {assets}/rs-codigo.rs"
    )
    launch_mcat_tab(kitty, "💻 CÓDIGO-FUENTE", PALETTE['CODE'], cmd3)
    
    # --- 4. VISUALIZACIÓN DE IMÁGENES (Kitty Graphics) ---
    cmd4 = f"clear && echo '--- RENDERIZADO DE ALTA FIDELIDAD ---' && mcat {assets}/demo-imagen.png"
    launch_mcat_tab(kitty, "🖼️ IMAGEN-KITTY", PALETTE['MEDIA'], cmd4)
    
    # --- 5. REPRODUCCIÓN DE VIDEO (In-Terminal) ---
    cmd5 = f"clear && echo '--- REPRODUCTOR DE VIDEO INTEGRADO ---' && mcat {assets}/demo-video.mp4"
    launch_mcat_tab(kitty, "🎬 VIDEO-STREAM", PALETTE['MEDIA'], cmd5)
    
    # --- 6. MOTOR DE CONVERSIÓN (Pipeline Táctico) ---
    # Convertimos ZIP a MD y previsualizamos
    cmd6 = (
        f"clear && echo '--- INSPECCIÓN DE ARCHIVOS COMPRIMIDOS (ZIP -> MD) ---' && "
        f"mcat {assets}/archivo-demo.zip && "
        f"echo '\n--- PREVISUALIZACIÓN DE PRESENTACIONES (PPTX) ---' && mcat {assets}/pptx-presentacion.pptx"
    )
    launch_mcat_tab(kitty, "🔄 CONVERSIÓN-ARCHIVOS", PALETTE['CONVERT'], cmd6)
    
    # --- 7. MODO INTERACTIVO (Zoom & Pan) ---
    cmd7 = (
        f"clear && echo '--- LANZANDO VISOR INTERACTIVO (Usa WASD y +/-) ---' && "
        f"mcat {assets}/demo-documento.pdf -o interactive"
    )
    launch_mcat_tab(kitty, "🎮 INTERACTIVO-ZOOM", PALETTE['INTERACTIVE'], cmd7)

    # --- 8. LISTADO VISUAL (Thumbnails) ---
    cmd8 = f"clear && echo '--- LISTADO TÁCTICO CON MINIATURAS ---' && mcat ls {assets}"
    launch_mcat_tab(kitty, "📂 EXPLORADOR-VISUAL", PALETTE['LS'], cmd8)

    return True

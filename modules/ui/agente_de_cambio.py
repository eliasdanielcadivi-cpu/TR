"""
AgenteDeCambio - Módulo de interfaz TUI híbrida para ARES

Interfaz 90% Textual + 10% Ratatui para extracción cognitiva
con prompts vivos, métricas de deriva y modo dual chat/cuestionario.

Módulo atómico (≤3 funciones principales) - Filosofía ARES
"""

import sys
from pathlib import Path

# Ruta a componentes
TR_ROOT = Path(__file__).parent.parent.parent
AGENTE_ROOT = TR_ROOT / "AGENTES" / "sub-agentes" / "AgenteDeCambio"


def run_demo():
    """
    Ejecutar demo de interfaz TUI
    
    Función 1: Inicia la app de demostración Textual
    con componentes híbridos (Textual + Ratatui)
    """
    print("🚀 Iniciando AgenteDeCambio CLI...")
    print()
    
    # Intentar cargar renderer Rust
    try:
        from .hybrid_renderer import RatatuiRenderer
        renderer = RatatuiRenderer()
        rust_ok = True
        print("✅ Rust components: OK")
    except Exception as e:
        rust_ok = False
        renderer = None
        print(f"⚠️  Rust components: NO DISPONIBLES ({e})")
        print(f"   Ejecuta: ares agente AgenteDeCambio install")
    
    print()
    print("═" * 60)
    print("DEMO: Componentes Híbridos (Textual + Ratatui)")
    print("═" * 60)
    print()
    print("Presiona Ctrl+Q para salir")
    print()
    
    # Importar y ejecutar app real
    from .app import run_app
    run_app()


def run_tests():
    """
    Ejecutar tests de componentes
    
    Función 2: Testea componentes Rust y Textual
    Muestra resultados y retorna código de exito
    """
    print("🧪 Testing componentes...")
    print()
    
    try:
        sys.path.insert(0, str(AGENTE_ROOT / "modules" / "ui"))
        from hybrid_renderer import RatatuiRenderer
        renderer = RatatuiRenderer()
        print("✅ RatatuiRenderer: OK")
        
        # Test gauges
        print("\n1. Delta BAJO (0.15 < 0.3) - OK:")
        print(renderer.render_gauge(0.15, 0.3))
        
        print("\n2. Delta MEDIO (0.45 > 0.3) - REVIEW:")
        print(renderer.render_gauge(0.45, 0.3))
        
        print("\n3. Delta ALTO (0.85 > 0.3) - REJECT:")
        print(renderer.render_gauge(0.85, 0.3))
        
        # Test sparkline
        print("\n4. Historial de Delta (Sparkline):")
        history = [0.1, 0.15, 0.2, 0.25, 0.3, 0.45, 0.5, 0.4, 0.35, 0.3]
        print(renderer.render_sparkline(history, width=40, height=3))
        
        print("\n✅ Todos los tests pasaron")
        return 0
        
    except FileNotFoundError as e:
        print(f"⚠️  Rust components no disponibles")
        print(f"   Ejecuta: ares agente-de-cambio install")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def install_rust_components():
    """
    Instalar componentes Rust (Ratatui)
    
    Función 3: Compila biblioteca Rust con cargo build --release
    """
    print("📦 Instalando componentes Rust (Ratatui)...")
    print()
    
    rust_path = AGENTE_ROOT / "modules" / "ui" / "ratatui_components"
    
    if not rust_path.exists():
        print(f"❌ Ruta no encontrada: {rust_path}")
        print(f"   Verifica que AgenteDeCambio esté correctamente estructurado")
        return 1
    
    print(f"📁 Directorio: {rust_path}")
    print()
    print("Ejecutando cargo build --release...")
    print()
    
    import subprocess
    result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=rust_path,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Build completado exitosamente")
        print()
        print("📦 Biblioteca generada:")
        lib_path = rust_path / "target" / "release" / "libratui_components.so"
        print(f"   {lib_path}")
        
        if lib_path.exists():
            print("✅ Componentes Rust listos para usar")
            print()
            print("Ahora ejecuta: ares agente AgenteDeCambio run")
        else:
            print("⚠️  Biblioteca .so no encontrada")
            return 1
    else:
        print("❌ Error en build:")
        print(result.stderr)
        print()
        print("💡 Tips:")
        print("   1. Verifica que Rust esté instalado: rustc --version")
        print("   2. Si no está: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
        print("   3. Luego: source ~/.cargo/env (ya está en .zshrc de ARES)")
        return 1
    
    return 0


def show_status():
    """Mostrar estado de instalación"""
    print("📊 Estado de AgenteDeCambio CLI")
    print("═" * 60)
    print()
    
    # Verificar Python deps
    print("1. Dependencias Python:")
    try:
        import textual
        print(f"   ✅ textual: v{textual.__version__}")
    except ImportError:
        print(f"   ❌ textual: NO INSTALADO")
    
    try:
        import httpx
        print(f"   ✅ httpx: v{httpx.__version__}")
    except ImportError:
        print(f"   ❌ httpx: NO INSTALADO")
    
    # Verificar Rust components - usar ruta absoluta
    print()
    print("2. Componentes Rust (Ratatui):")
    lib_path = Path("/home/daniel/tron/programas/TR/AGENTES/sub-agentes/AgenteDeCambio/modules/ui/ratatui_components/target/release/libratui_components.so")
    
    if lib_path.exists():
        print(f"   ✅ Biblioteca: {lib_path.name}")
        print(f"   ✅ Estado: COMPILADO ({lib_path.stat().st_size // 1024}KB)")
    else:
        print(f"   ⚠️  Biblioteca: NO COMPILADA")
        print(f"   💡 Ejecuta: ares agente AgenteDeCambio install")
    
    # Verificar estructura
    print()
    print("3. Estructura de carpetas:")
    print(f"   ✅ TR_ROOT: {TR_ROOT}")
    print(f"   ✅ Agentes: {TR_ROOT / 'AGENTES'}")
    print(f"   ✅ Docs: {TR_ROOT / 'docs'}")
    
    print()
    print("═" * 60)
    print("Comandos disponibles:")
    print("   ares agente AgenteDeCambio run      - Ejecutar demo TUI")
    print("   ares agente AgenteDeCambio test     - Test componentes")
    print("   ares agente AgenteDeCambio install  - Instalar Rust")
    print("   ares agente AgenteDeCambio status   - Este mensaje")
    print("═" * 60)

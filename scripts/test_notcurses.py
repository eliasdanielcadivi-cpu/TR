#!/usr/bin/env python3
# =============================================================================
# SCRIPT DE PRUEBA NOTCURSES - ARES-TRON
# =============================================================================
# Propósito: Ejecutar pruebas de imágenes con notcurses de forma standalone
# Uso: ./scripts/test_notcurses.py
#      o: python scripts/test_notcurses.py
# =============================================================================

import sys
import os
from pathlib import Path

# =============================================================================
# SETUP DE RUTAS
# =============================================================================

# Obtener directorio del script
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent

# Agregar al path
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# IMPORTS
# =============================================================================

# Verificar notcurses primero (antes de cualquier otra cosa)
print("\n" + "=" * 60)
print("VERIFICANDO DEPENDENCIAS")
print("=" * 60 + "\n")

try:
    from notcurses import Notcurses
    print("✅ notcurses: OK")
except ImportError as e:
    print("❌ notcurses: NO INSTALADO")
    print(f"\n   Error: {e}")
    print("\n" + "=" * 60)
    print("INSTALACIÓN DE NOTCURSES")
    print("=" * 60)
    print("\nOpción 1: Desde repositorios (recomendado)")
    print("   sudo apt-get update")
    print("   sudo apt-get install libnotcurses-dev notcurses-bin python3-notcurses")
    print("\nOpción 2: Build from source")
    print("   git clone https://github.com/dankamongmen/notcurses.git")
    print("   cd notcurses && mkdir build && cd build")
    print("   cmake .. -DUSE_MULTIMEDIA=ffmpeg -DUSE_CXX=on")
    print("   make -j$(nproc) && sudo make install && sudo ldconfig")
    print("\nOpción 3: Pip (puede no funcionar)")
    print("   pip install notcurses")
    print("\n" + "=" * 60)
    sys.exit(1)

try:
    import yaml
    print("✅ pyyaml: OK")
except ImportError:
    print("⚠️  pyyaml: NO INSTALADO (usando configuración por defecto)")

try:
    import logging
    print("✅ logging: OK (stdlib)")
except ImportError:
    print("❌ logging: FALLO (esto es raro)")

print("\n" + "=" * 60)
print("INICIANDO PRUEBAS NOTCURSES")
print("=" * 60 + "\n")

# =============================================================================
# PRUEBA RÁPIDA
# =============================================================================

def prueba_rapida():
    """Prueba rápida de notcurses sin configuración YAML"""
    
    print("🧪 Prueba Rápida de Notcurses\n")
    
    try:
        # Inicializar notcurses
        print("  1. Inicializando notcurses...")
        nc = Notcurses()
        print("     ✅ Notcurses inicializado")
        print(f"     Terminal: {nc.termname}")
        print(f"     Dimensiones: {nc.stdplane.cols}x{nc.stdplane.rows}")
        
        stdplane = nc.stdplane()
        
        # Mensaje de bienvenida
        print("\n  2. Renderizando mensaje...")
        stdplane.set_fg_rgb8(0, 255, 255)  # Cyan
        stdplane.putstr_yx(0, 0, "╔════════════════════════════════════╗")
        stdplane.putstr_yx(1, 0, "║     ARES-TRON Notcurses Test       ║")
        stdplane.putstr_yx(2, 0, "║           ¡Funciona! 🎉            ║")
        stdplane.putstr_yx(3, 0, "╚════════════════════════════════════╝")
        nc.render()
        print("     ✅ Mensaje renderizado")
        
        # Probar imagen si existe
        avatar_path = PROJECT_ROOT / 'assets' / 'ares' / 'ares-neon.png'
        
        if avatar_path.exists():
            print(f"\n  3. Cargando imagen: {avatar_path}")
            
            try:
                from notcurses import PlaneOptions, Visual
                
                # Crear plano para imagen
                plane_opts = PlaneOptions(rows=8, cols=16, yoff=5, xoff=0)
                img_plane = stdplane.create(plane_opts)
                
                # Cargar y blitear imagen
                visual = Visual(str(avatar_path))
                visual.blit(img_plane)
                nc.render()
                
                print("     ✅ Imagen renderizada correctamente")
                
            except Exception as e:
                print(f"     ⚠️  Error renderizando imagen: {e}")
        else:
            print(f"\n  3. ⚠️  Imagen no encontrada: {avatar_path}")
        
        # Instrucciones
        print("\n" + "=" * 60)
        print("Presiona 'q' para salir")
        print("=" * 60)
        
        # Loop de input
        while True:
            input_val = nc.getc_blocking()
            if input_val == ord('q'):
                print("\n  Saliendo...")
                break
        
        nc.stop()
        print("  ✅ Notcurses detenido correctamente")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en prueba rápida: {e}")
        import traceback
        traceback.print_exc()
        return False


# =============================================================================
# PRUEBA COMPLETA CON CONFIGURACIÓN
# =============================================================================

def prueba_completa():
    """Prueba completa usando configuración YAML"""
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETA CON CONFIGURACIÓN")
    print("=" * 60 + "\n")
    
    # Importar módulo de prueba
    try:
        from modules.multimedia import notcurses_test
        print("✅ Módulo notcurses_test cargado")
    except ImportError as e:
        print(f"❌ Error cargando módulo: {e}")
        return False
    
    # Ejecutar main del módulo
    return notcurses_test.main() == 0


# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================

def mostrar_menu():
    """Mostrar menú de opciones"""
    print("\n" + "=" * 60)
    print("MENÚ DE PRUEBAS NOTCURSES")
    print("=" * 60)
    print("\n  1. Prueba rápida (sin YAML)")
    print("  2. Prueba completa (con configuración)")
    print("  3. Salir")
    print("\n" + "=" * 60)
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    if opcion == '1':
        return prueba_rapida()
    elif opcion == '2':
        return prueba_completa()
    elif opcion == '3':
        print("\n👋 ¡Hasta luego!")
        return True
    else:
        print("\n❌ Opción inválida")
        return False


# =============================================================================
# MODO AUTOMÁTICO VS INTERACTIVO
# =============================================================================

if __name__ == "__main__":
    # Verificar modo de ejecución
    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()
        
        if modo == '--rapida' or modo == '-r':
            # Prueba rápida directa
            exito = prueba_rapida()
            sys.exit(0 if exito else 1)
            
        elif modo == '--completa' or modo == '-c':
            # Prueba completa directa
            exito = prueba_completa()
            sys.exit(0 if exito else 1)
            
        elif modo == '--help' or modo == '-h':
            print("\nUso: python scripts/test_notcurses.py [opción]")
            print("\nOpciones:")
            print("  -r, --rapida    Ejecutar prueba rápida")
            print("  -c, --completa  Ejecutar prueba completa con YAML")
            print("  -h, --help      Mostrar esta ayuda")
            print("\nSin opciones: Modo interactivo con menú")
            sys.exit(0)
        
        else:
            print(f"\n❌ Opción desconocida: {modo}")
            print("Usa -h para ayuda")
            sys.exit(1)
    
    else:
        # Modo interactivo con menú
        exito = mostrar_menu()
        sys.exit(0 if exito else 1)

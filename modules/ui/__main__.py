#!/usr/bin/env python3
"""
AgenteDeCambio CLI - Wrapper de ejecución

Ejecuta la aplicación AgenteDeCambio desde la línea de comandos.

Uso:
    python -m modules.ui.agente_de_cambio run
    python -m modules.ui.agente_de_cambio demo
"""

import sys
from pathlib import Path

# Agregar TR al PATH
TR_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TR_ROOT))

from modules.ui.agente_de_cambio import run_demo, run_tests, show_status


def main():
    """Punto de entrada principal"""
    if len(sys.argv) < 2:
        print("Uso: python -m modules.ui.agente_de_cambio [run|demo|test|status]")
        print()
        print("Comandos:")
        print("  run    - Ejecutar interfaz TUI completa")
        print("  demo   - Ejecutar demo de componentes")
        print("  test   - Test de componentes")
        print("  status - Verificar estado")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "run":
        run_demo()
    elif command == "demo":
        from modules.ui.app import demo_app
        demo_app()
    elif command == "test":
        run_tests()
    elif command == "status":
        show_status()
    else:
        print(f"Comando desconocido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

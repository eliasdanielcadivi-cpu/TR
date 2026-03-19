#!/usr/bin/env python3
"""
AgenteDeCambio CLI - Script de lanzamiento

Este script muestra información y luego lanza la app Textual.
"""

import os
import sys
from pathlib import Path

# Colores para terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def main():
    """Punto de entrada principal"""
    # Agregar TR al path
    TR_ROOT = Path(__file__).parent.parent.resolve()
    sys.path.insert(0, str(TR_ROOT))
    
    print(f"\n{BOLD}{GREEN}🚀 AgenteDeCambio CLI{RESET}\n")
    print(f"{BOLD}Iniciando interfaz TUI...{RESET}\n")
    
    # Verificar API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print(f"{YELLOW}⚠️  ADVERTENCIA: DEEPSEEK_API_KEY no configurada{RESET}")
        print(f"   Para usar el chat, configura la variable de entorno:")
        print(f"   {GREEN}export DEEPSEEK_API_KEY='sk-tu-api-key'{RESET}\n")
        print(f"   Obtén tu API key en: https://platform.deepseek.com/api_keys\n")
    else:
        print(f"{GREEN}✅ DeepSeek API Key: Configurada{RESET}\n")
    
    print(f"{BOLD}Controles:{RESET}")
    print(f"  {GREEN}Enter{RESET}  - Enviar mensaje")
    print(f"  {GREEN}Ctrl+Q{RESET} - Salir")
    print(f"  {GREEN}Ctrl+S{RESET} - Guardar sesión")
    print(f"  {GREEN}F1{RESET}    - Mostrar ayuda")
    print()
    print(f"{BOLD}Iniciando app TUI en 3 segundos...{RESET}\n")
    
    import time
    time.sleep(1)
    
    # Importar y ejecutar app
    from modules.ui.app import run_app
    run_app()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}App cerrada por usuario{RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}❌ Error:{RESET} {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

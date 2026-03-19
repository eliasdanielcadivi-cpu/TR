#!/usr/bin/env python3
"""
Diagnóstico de AgenteDeCambio CLI

Verifica que todos los componentes estén listos antes de ejecutar.
"""

import sys
import os
from pathlib import Path

# Colores
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def check(msg, ok=True):
    """Mostrar chequeo"""
    status = f"{GREEN}✅{RESET}" if ok else f"{RED}❌{RESET}"
    print(f"{status} {msg}")
    return ok

print(f"\n{BOLD}🔍 Diagnóstico de AgenteDeCambio CLI{RESET}\n")

all_ok = True

# 1. Verificar Python path
print(f"{BOLD}1. Python Path:{RESET}")
tr_root = Path("/home/daniel/tron/programas/TR")
sys.path.insert(0, str(tr_root))
check(f"TR_ROOT agregado: {tr_root}")

# 2. Verificar imports
print(f"\n{BOLD}2. Imports:{RESET}")
try:
    from modules.ui.app import AgenteDeCambioApp, run_app
    check("modules.ui.app import OK")
except Exception as e:
    check(f"modules.ui.app import: {e}", ok=False)
    all_ok = False

try:
    from modules.core import create_session, create_completion_stream
    check("modules.core import OK")
except Exception as e:
    check(f"modules.core import: {e}", ok=False)
    all_ok = False

# 3. Verificar API Key
print(f"\n{BOLD}3. Configuración:{RESET}")
api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key:
    check(f"DEEPSEEK_API_KEY: configurada ({api_key[:10]}...)")
else:
    check("DEEPSEEK_API_KEY: NO configurada", ok=False)
    print(f"\n   {YELLOW}Para configurar:{RESET}")
    print(f"   export DEEPSEEK_API_KEY='sk-tu-api-key'")

# 4. Verificar terminal
print(f"\n{BOLD}4. Terminal:{RESET}")
if sys.stdin.isatty():
    check("Terminal interactiva: OK")
else:
    check("Terminal: NO interactiva (probable causa de fallo)", ok=False)
    print(f"\n   {YELLOW}La app necesita una terminal interactiva (TTY){RESET}")

# 5. Verificar dependencias
print(f"\n{BOLD}5. Dependencias:{RESET}")
try:
    import textual
    check(f"textual: v{textual.__version__}")
except ImportError:
    check("textual: NO instalado", ok=False)
    all_ok = False

try:
    import httpx
    check(f"httpx: v{httpx.__version__}")
except ImportError:
    check("httpx: NO instalado", ok=False)
    all_ok = False

# Resumen
print(f"\n{'='*60}")
if all_ok:
    print(f"{GREEN}✅ Todo está listo para ejecutar{RESET}")
    print(f"\n{BOLD}Comando para ejecutar:{RESET}")
    print(f"   python -m modules.ui.agente_de_cambio run")
else:
    print(f"{RED}❌ Hay errores que corregir{RESET}")

print(f"{'='*60}\n")

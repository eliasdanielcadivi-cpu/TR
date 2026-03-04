import os
import sys
import json
import time
from pathlib import Path

# Configurar entorno para importar módulos de ARES
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from config import TRContext
from modules.ia.ai_engine import AIEngine
from modules.admon.init_manager_logic import get_status

def test_config_loading():
    print("🧪 Probando carga de configuración...")
    ctx = TRContext()
    assert ctx.config is not None
    assert "identity" in ctx.config
    print("✅ Configuración cargada: " + ctx.config['identity']['window_title'])

def test_ia_exportable():
    print("🧪 Probando motor de IA (Mock/Headless)...")
    ctx = TRContext()
    ai = AIEngine(ctx.config['ai'])
    # Verificamos que el objeto sea instanciable y tenga el método ask
    assert hasattr(ai, 'ask')
    print("✅ Motor IA listo para exportación.")

def test_status_logic():
    print("🧪 Probando lógica de diagnóstico...")
    ctx = TRContext()
    status = get_status(ctx.kitty_conf, "~/.config/kitty/kitty.conf", ctx.socket)
    assert 'socket' in status
    print(f"✅ Diagnóstico verificado en socket: {status['socket']}")

if __name__ == "__main__":
    print("=== ARES HEADLESS VALIDATION SUITE ===")
    try:
        test_config_loading()
        test_ia_exportable()
        test_status_logic()
        print("
🚀 RESULTADO: Todos los módulos están bien enlazados.")
    except Exception as e:
        print(f"
❌ FALLO DE INTEGRACIÓN: {str(e)}")
        sys.exit(1)

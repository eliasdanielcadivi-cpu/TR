import os
import subprocess
import time
from pathlib import Path

from config import KittyRemote

def launch_ares(ctx_obj):
    """Lógica de arranque del sistema ARES."""
    kitty = KittyRemote(ctx_obj)
    
    # 1. Lanzar ventana kitty a través de KittyRemote (Centralizado)
    if not kitty.launch_hub():
        return False

    # 2. Nombre de la PRIMERA PESTAÑA: mínimo ("-" por defecto)
    # Esperar que kitty inicie antes de enviar comando remoto
    time.sleep(0.3)
    kitty.run(["set-tab-title", "-"])
    return True

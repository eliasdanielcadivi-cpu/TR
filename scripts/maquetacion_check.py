#!/usr/bin/env python3
"""Maquetación Industrial Check: Verificación de Layout Complejo.

Valida:
1. Renderizado de Cintillos (Rectangulares).
2. Renderizado de Separadores (Barras).
3. Componentes de Animación (Spinner).
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from modules.ia.apollo.emoji_manager import get_asset_render, get_layout_config

def industrial_vision_check():
    print("🛰️ [CONSTATACIÓN INDUSTRIAL] Verificando maquetación de bloques...\n")
    
    # Lista de componentes críticos para el nuevo diseño
    components = ["separator", "header_ares", "header_user", "thinking_spinner", "thinking_label"]
    
    all_ok = True
    for comp in components:
        ansi = get_asset_render(comp)
        is_kitty = "\x1b_G" in ansi
        size = len(ansi)
        
        print(f"Componente: {comp:18} | Kitty: {'✅' if is_kitty else '❌'} | Buffer: {size} bytes")
        
        if not is_kitty or size < 50:
            all_ok = False

    print("\n" + "="*40)
    if all_ok:
        print("✅ [EXITO] Todos los componentes de maquetación inyectan Kitty Protocol.")
        print("💡 Los cambios en el YAML se reflejarán en las dimensiones de los cintillos.")
    else:
        print("⚠️ [AVISO] Algunos componentes usan fallback. Verificar existencia de archivos en assets/ui/")

if __name__ == "__main__":
    industrial_vision_check()

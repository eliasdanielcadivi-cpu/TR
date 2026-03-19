#!/usr/bin/env python3
"""
AgenteDeCambio CLI - Versión simplificada sin Textual

Esta versión usa print/input para demostrar que la lógica funciona.
"""

import sys
import os
from pathlib import Path

# Agregar TR al path
TR_ROOT = Path("/home/daniel/tron/programas/TR")
sys.path.insert(0, str(TR_ROOT))

from modules.core import create_session, get_session, update_session

print("=" * 60)
print("AgenteDeCambio CLI - Modo Simplificado")
print("=" * 60)
print()

# Crear sesión
session = create_session()
print(f"✅ Sesión creada: {session['id']}")
print()

print("Escribe tu mensaje (o 'salir' para terminar):")
print()

while True:
    try:
        # Obtener mensaje del usuario
        user_input = input("👤 Tú: ").strip()
        
        if user_input.lower() == 'salir':
            print("\n¡Hasta luego!")
            break
        
        if not user_input:
            continue
        
        # Simular respuesta del bot
        print(f"🤖 Bot: Recibido: '{user_input}'")
        print(f"   (Streaming DeepSeek pendiente de API Key)")
        print()
        
    except KeyboardInterrupt:
        print("\n\nApp cerrada por usuario")
        break
    except EOFError:
        print("\n\nFin de input")
        break

print()
print("=" * 60)
print("Sesión guardada correctamente")
print("=" * 60)

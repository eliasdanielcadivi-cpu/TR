#!/usr/bin/env python3
"""
Prueba Temprana 2: set-tab-color básico
========================================
Prueba el comando set-tab-color de kitty para cambiar
el color de fondo de una pestaña.
"""

import socket
import json
import sys
import os

SOCKET_PATH = '/tmp/mykitty'

def enviar_set_tab_color(color_hex: str, match: str = 'self') -> bool:
    """
    Envía comando set-tab-color a kitty
    
    Args:
        color_hex: Color en formato #RRGGBB
        match: Expresión de match (default: 'self')
    
    Returns:
        True si exitoso, False en caso contrario
    """
    # Convertir hex a RGB entero
    color_hex = color_hex.lstrip('#')
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:6], 16)
    
    # Color como entero 24-bit
    color_int = (r << 16) | (g << 8) | b
    
    print(f"\nEnviando set-tab-color:")
    print(f"  Color: {color_hex} (RGB: {r},{g},{b})")
    print(f"  Match: {match}")
    
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect(SOCKET_PATH)
        
        # Construir comando según documentación oficial
        # https://sw.kovidgoyal.net/kitty/remote-control/#at-set-tab-color
        command = {
            'cmd': 'set-tab-color',
            'version': [0, 35, 0],
            'payload': {
                'match': [match],
                'colors': {
                    'background': color_int
                }
            }
        }
        
        message = json.dumps(command).encode('utf-8')
        
        # Enviar longitud + mensaje
        client.sendall(len(message).to_bytes(4, 'big'))
        client.sendall(message)
        
        # Recibir respuesta
        response_len_bytes = client.recv(4)
        if len(response_len_bytes) == 4:
            response_len = int.from_bytes(response_len_bytes, 'big')
            response = client.recv(response_len)
            data = json.loads(response.decode('utf-8'))
            
            client.close()
            
            # Verificar respuesta
            if data.get('code', '') == 'OK':
                print(f"  ✓ Respuesta: OK")
                return True
            else:
                print(f"  ✗ Respuesta: {data}")
                return False
        else:
            print(f"  ✗ No se recibió respuesta válida")
            client.close()
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def probar_colores():
    """Prueba varios colores en la pestaña actual"""
    print("=" * 60)
    print("PRUEBA TEMPRANA 2: set-tab-color Básico")
    print("=" * 60)
    
    # Verificar socket primero
    if not os.path.exists(SOCKET_PATH):
        print(f"\n✗ ERROR: Socket {SOCKET_PATH} no existe")
        print("Ejecuta primero test_1_socket.py")
        return False
    
    # Colores de prueba
    colores = [
        ('#ff0000', 'ROJO'),
        ('#00ff00', 'VERDE'),
        ('#0000ff', 'AZUL'),
        ('#ffff00', 'AMARILLO'),
        ('#ff00ff', 'MAGENTA'),
        ('#00ffff', 'CYAN'),
    ]
    
    print("\nPrueba de colores (5 segundos cada uno):")
    print("-" * 60)
    
    for color, nombre in colores:
        print(f"\n[{nombre}] Color: {color}")
        exito = enviar_set_tab_color(color, 'self')
        
        if exito:
            print(f"  → Color {nombre} aplicado, espera 3 segundos...")
            import time
            time.sleep(3)
        else:
            print(f"  → Falló aplicar color {nombre}")
            return False
    
    # Restaurar color original (negro)
    print(f"\n[RESTAURAR] Volviendo al color original")
    enviar_set_tab_color('#000000', 'self')
    
    return True


if __name__ == '__main__':
    print("\nNOTA: Esta prueba cambia visiblemente el color de fondo")
    print("      de la pestaña activa. Deberías ver los colores")
    print("      ROJO, VERDE, AZUL, AMARILLO, MAGENTA, CYAN")
    print("      en secuencia.\n")
    
    input("Presiona ENTER cuando estés listo para comenzar la prueba...")
    
    exito = probar_colores()
    
    print("\n" + "=" * 60)
    if exito:
        print("RESULTADO: ✓ set-tab-color FUNCIONA correctamente")
    else:
        print("RESULTADO: ✗ set-tab-color FALLÓ")
        print("\nPosibles causas:")
        print("1. Kitty no tiene remote control habilitado")
        print("2. El comando set-tab-color no está disponible en esta versión")
        print("3. Error de protocolo en el mensaje JSON")
    print("=" * 60)
    sys.exit(0 if exito else 1)

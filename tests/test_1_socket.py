#!/usr/bin/env python3
"""
Prueba Temprana 1: Verificar socket kitty y remote control
===========================================================
Verifica si kitty está corriendo con remote control habilitado
y si el socket está disponible.
"""

import os
import socket
import json
import sys

SOCKET_PATH = '/tmp/mykitty'

def verificar_socket():
    """Verifica si el socket de kitty existe y está accesible"""
    print("=" * 60)
    print("PRUEBA TEMPRANA 1: Verificar Socket Kitty")
    print("=" * 60)
    
    # 1. Verificar si el archivo socket existe
    print(f"\n1. Verificando existencia del socket: {SOCKET_PATH}")
    if not os.path.exists(SOCKET_PATH):
        print(f"   ✗ ERROR: El socket {SOCKET_PATH} NO existe")
        print("\n   Posibles causas:")
        print("   - Kitty no está corriendo")
        print("   - Kitty no se inició con --listen-on")
        print("   - El socket está en otra ruta")
        print("\n   Para iniciar kitty con socket:")
        print("   kitty -o allow_remote_control=yes --listen-on unix:/tmp/mykitty")
        return False
    
    print(f"   ✓ Socket existe")
    
    # 2. Verificar si es un socket UNIX
    print(f"\n2. Verificando tipo de archivo")
    try:
        mode = os.stat(SOCKET_PATH).st_mode
        import stat
        if stat.S_ISSOCK(mode):
            print(f"   ✓ Es un socket UNIX")
        else:
            print(f"   ✗ No es un socket UNIX (es {oct(mode)})")
            return False
    except Exception as e:
        print(f"   ✗ Error verificando tipo: {e}")
        return False
    
    # 3. Intentar conectar
    print(f"\n3. Intentando conectar al socket")
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect(SOCKET_PATH)
        print(f"   ✓ Conexión exitosa")
        client.close()
    except socket.error as e:
        print(f"   ✗ Error conectando: {e}")
        return False
    
    # 4. Enviar comando 'ls' para verificar remote control
    print(f"\n4. Enviando comando 'ls' para verificar remote control")
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect(SOCKET_PATH)
        
        # Construir mensaje JSON según protocolo kitty RC
        command = {
            'cmd': 'ls',
            'version': [0, 35, 0]
        }
        message = json.dumps(command).encode('utf-8')
        
        # Enviar longitud (4 bytes big-endian) + mensaje
        client.sendall(len(message).to_bytes(4, 'big'))
        client.sendall(message)
        
        # Recibir respuesta
        response_len_bytes = client.recv(4)
        if len(response_len_bytes) == 4:
            response_len = int.from_bytes(response_len_bytes, 'big')
            response = client.recv(response_len)
            data = json.loads(response.decode('utf-8'))
            
            if 'data' in data:
                tabs = data['data'][0].get('tabs', [])
                print(f"   ✓ Remote control funcional")
                print(f"   ✓ Pestañas abiertas: {len(tabs)}")
                client.close()
                return True
            else:
                print(f"   ✗ Respuesta inválida: {data}")
                client.close()
                return False
        else:
            print(f"   ✗ No se recibió longitud de respuesta")
            client.close()
            return False
            
    except Exception as e:
        print(f"   ✗ Error en remote control: {e}")
        return False

if __name__ == '__main__':
    exito = verificar_socket()
    print("\n" + "=" * 60)
    if exito:
        print("RESULTADO: ✓ Socket kitty VERIFICADO correctamente")
    else:
        print("RESULTADO: ✗ Socket kitty NO VERIFICADO")
        print("\nACCIÓN REQUERIDA:")
        print("1. Inicia kitty con remote control:")
        print("   kitty -o allow_remote_control=yes --listen-on unix:/tmp/mykitty")
        print("\n2. O verifica si kitty ya está corriendo:")
        print("   pgrep -a kitty")
    print("=" * 60)
    sys.exit(0 if exito else 1)

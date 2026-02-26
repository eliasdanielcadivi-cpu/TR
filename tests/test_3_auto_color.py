#!/usr/bin/env python3
"""
Prueba Automática: Verificación de Cambio de Color en Kitty
============================================================
Abre kitty, aplica color, lee con get-colors, verifica y cierra.
Todo automático sin intervención humana.
"""

import os
import sys
import socket
import json
import subprocess
import time
import signal

SOCKET_PATH = '/tmp/mykitty'
KITTY_PID_FILE = '/tmp/test_kitty.pid'

def limpiar_socket():
    """Limpia socket si existe"""
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)
        print(f"  ✓ Socket {SOCKET_PATH} eliminado")

def iniciar_kitty():
    """Inicia kitty en background con remote control"""
    print("\n1. Iniciando kitty con remote control...")
    
    limpiar_socket()
    
    # Comando para iniciar kitty
    cmd = [
        'kitty',
        '-o', 'allow_remote_control=yes',
        '--listen-on', f'unix:{SOCKET_PATH}',
        '--detach',
        '--title', 'TEST-KITTY-COLOR'
    ]
    
    print(f"   Comando: {' '.join(cmd)}")
    
    # Iniciar en background
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    # Guardar PID
    with open(KITTY_PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    print(f"   PID kitty: {proc.pid}")
    
    # Esperar a que kitty inicie y el socket esté disponible
    print("   Esperando kitty... ", end='', flush=True)
    for i in range(30):  # Máximo 3 segundos
        time.sleep(0.1)
        if os.path.exists(SOCKET_PATH):
            print(f"✓ listo ({i*0.1:.1f}s)")
            return proc.pid
    
    print("✗ TIMEOUT")
    return None

def cerrar_kitty(pid):
    """Cierra kitty limpiamente"""
    print(f"\n5. Cerrando kitty (PID: {pid})...")
    
    try:
        # Enviar SIGTERM
        os.kill(pid, signal.SIGTERM)
        print("   ✓ SIGTERM enviado")
        
        # Esperar un momento
        time.sleep(0.5)
        
        # Verificar si aún existe
        try:
            os.kill(pid, 0)
            # Aún existe, enviar SIGKILL
            os.kill(pid, signal.SIGKILL)
            print("   ✓ SIGKILL enviado (no cerró con SIGTERM)")
        except ProcessLookupError:
            print("   ✓ Kitty cerrado correctamente")
            
    except ProcessLookupError:
        print("   ✓ Kitty ya no existe")
    except Exception as e:
        print(f"   ✗ Error cerrando: {e}")
    
    # Limpiar PID file
    if os.path.exists(KITTY_PID_FILE):
        os.unlink(KITTY_PID_FILE)
    
    # Limpiar socket
    limpiar_socket()

def enviar_comando(cmd_name, payload=None):
    """Envía comando RC a kitty vía socket"""
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect(SOCKET_PATH)
        
        command = {'cmd': cmd_name, 'version': [0, 35, 0]}
        if payload:
            command['payload'] = payload
        
        message = json.dumps(command).encode('utf-8')
        client.sendall(len(message).to_bytes(4, 'big'))
        client.sendall(message)
        
        response_len_bytes = client.recv(4)
        if len(response_len_bytes) == 4:
            response_len = int.from_bytes(response_len_bytes, 'big')
            response = client.recv(response_len)
            data = json.loads(response.decode('utf-8'))
            client.close()
            return data
        else:
            client.close()
            return None
    except Exception as e:
        print(f"   ✗ Error enviando comando: {e}")
        return None

def get_colors():
    """Obtiene colores actuales usando get-colors"""
    result = subprocess.run(
        ['kitten', '@', '--to', f'unix:{SOCKET_PATH}', 'get-colors'],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        colors = {}
        for line in result.stdout.strip().split('\n'):
            if ' ' in line:
                key, value = line.split(None, 1)
                colors[key] = value
        return colors
    else:
        print(f"   ✗ Error get-colors: {result.stderr}")
        return None

def aplicar_color(color_hex):
    """Aplica color de fondo usando set-colors"""
    result = subprocess.run(
        ['kitten', '@', '--to', f'unix:{SOCKET_PATH}', 'set-colors', f'background={color_hex}'],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.returncode == 0

def test_cambio_color():
    """Ejecuta prueba completa de cambio de color"""
    print("=" * 70)
    print("PRUEBA AUTOMÁTICA: Verificación de Cambio de Color en Kitty")
    print("=" * 70)
    
    pid = None
    try:
        # 1. Iniciar kitty
        pid = iniciar_kitty()
        if not pid:
            print("\n✗ FALLÓ: No se pudo iniciar kitty")
            return False
        
        # 2. Obtener colores iniciales
        print("\n2. Obteniendo colores iniciales...")
        colores_iniciales = get_colors()
        if not colores_iniciales:
            print("   ✗ No se pudo obtener colores iniciales")
            return False
        
        background_inicial = colores_iniciales.get('background', 'desconocido')
        print(f"   Background inicial: {background_inicial}")
        
        # 3. Aplicar nuevo color
        color_test = '#ff6600'  # Naranja
        print(f"\n3. Aplicando color de prueba: {color_test}")
        exito_aplicar = aplicar_color(color_test)
        if not exito_aplicar:
            print("   ✗ No se pudo aplicar el color")
            return False
        print("   ✓ Color aplicado")
        
        # Pequeña pausa para que kitty procese el cambio
        time.sleep(0.3)
        
        # 4. Leer colores después del cambio
        print("\n4. Leyendo colores después del cambio...")
        colores_finales = get_colors()
        if not colores_finales:
            print("   ✗ No se pudo obtener colores finales")
            return False
        
        background_final = colores_finales.get('background', 'desconocido')
        print(f"   Background final: {background_final}")
        
        # 5. Verificar cambio
        print("\n5. Verificando cambio...")
        print(f"   Inicial: {background_inicial}")
        print(f"   Final:   {background_final}")
        print(f"   Esperado: {color_test}")
        
        # Comparar (normalizar formato)
        background_final_norm = background_final.lower().lstrip('#')
        color_test_norm = color_test.lower().lstrip('#')
        
        if background_final_norm == color_test_norm:
            print("\n   ✓✓✓ COLOR CAMBIÓ CORRECTAMENTE ✓✓✓")
            return True
        else:
            print(f"\n   ✗ COLOR NO CAMBIÓ (esperado {color_test}, obtenido {background_final})")
            return False
        
    except Exception as e:
        print(f"\n✗ ERROR en prueba: {e}")
        return False
    finally:
        # Siempre cerrar kitty
        if pid:
            cerrar_kitty(pid)
        
        print("\n" + "=" * 70)
        print("PRUEBA COMPLETADA")
        print("=" * 70)

if __name__ == '__main__':
    # Verificar prerequisitos
    print("Verificando prerequisitos...")
    
    if not subprocess.run(['which', 'kitty'], capture_output=True).returncode == 0:
        print("✗ kitty no está instalado")
        sys.exit(1)
    
    if not subprocess.run(['which', 'kitten'], capture_output=True).returncode == 0:
        print("✗ kitten no está instalado")
        sys.exit(1)
    
    print("✓ kitty y kitten disponibles")
    
    # Ejecutar prueba
    exito = test_cambio_color()
    
    sys.exit(0 if exito else 1)

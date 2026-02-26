#!/usr/bin/env python3
"""
Prueba de Integración: tr-color con kitty real
===============================================
Abre kitty, usa tr-color para aplicar color según ruta de archivo,
verifica con get-colors y cierra.
"""

import os
import sys
import subprocess
import time
import signal

SOCKET_PATH = '/tmp/mykitty'
KITTY_PID_FILE = '/tmp/test_kitty.pid'
TR_BASE = '/home/daniel/tron/programas/TR'

def limpiar():
    """Limpia socket y PID file"""
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)
    if os.path.exists(KITTY_PID_FILE):
        os.unlink(KITTY_PID_FILE)

def iniciar_kitty():
    """Inicia kitty en background"""
    print("\n1. Iniciando kitty...")
    limpiar()
    
    cmd = [
        'kitty',
        '-o', 'allow_remote_control=yes',
        '--listen-on', f'unix:{SOCKET_PATH}',
        '--detach',
        '--title', 'TEST-TR-COLOR'
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with open(KITTY_PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    print(f"   PID: {proc.pid}")
    print("   Esperando... ", end='', flush=True)
    
    for i in range(30):
        time.sleep(0.1)
        if os.path.exists(SOCKET_PATH):
            print(f"✓ ({i*0.1:.1f}s)")
            return proc.pid
    
    print("✗ TIMEOUT")
    return None

def cerrar_kitty(pid):
    """Cierra kitty"""
    print(f"\n4. Cerrando kitty (PID: {pid})...")
    
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.5)
        try:
            os.kill(pid, 0)
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        print("   ✓ Cerrado")
    except:
        pass
    
    limpiar()

def get_colors():
    """Obtiene colores actuales"""
    result = subprocess.run(
        ['kitten', '@', '--to', f'unix:{SOCKET_PATH}', 'get-colors'],
        capture_output=True, text=True, timeout=5
    )
    
    if result.returncode == 0:
        colors = {}
        for line in result.stdout.strip().split('\n'):
            if ' ' in line:
                key, value = line.split(None, 1)
                colors[key] = value
        return colors
    return None

def ejecutar_tr_color(ruta_archivo):
    """Ejecuta tr-color con una ruta"""
    print(f"\n2. Ejecutando tr-color con: {ruta_archivo}")
    
    # Usar el binario tr-color directamente
    cmd = [
        os.path.join(TR_BASE, 'bin/tr-color'),
        ruta_archivo
    ]
    
    # Establecer ambiente para que use el socket correcto
    env = os.environ.copy()
    env['KITTY_LISTEN_ON'] = f'unix:{SOCKET_PATH}'
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=TR_BASE,
        env=env
    )
    
    print(f"   stdout: {result.stdout.strip()}")
    if result.stderr:
        print(f"   stderr: {result.stderr.strip()}")
    
    return result.returncode == 0

def test_tr_color():
    """Prueba tr-color con archivos reales"""
    print("=" * 70)
    print("PRUEBA DE INTEGRACIÓN: tr-color con kitty real")
    print("=" * 70)
    
    # Archivos de prueba con sus colores esperados
    tests = [
        ('/home/daniel/Escritorio/QT5/elAsunto.md', '#ff6600', 'EL ASUNTO'),
        ('/home/daniel/Escritorio/QT5/PRUEBAS_MAPA.md', '#00ccff', 'PRUEBAS MAPA'),
        ('/home/daniel/Escritorio/QT5/SelectorHacker/server.js', '#ffff00', 'SELECTOR SERVER'),
    ]
    
    pid = None
    resultados = []
    
    try:
        for ruta, color_esperado, titulo_esperado in tests:
            print(f"\n{'='*70}")
            print(f"TEST: {os.path.basename(ruta)}")
            print(f"{'='*70}")
            
            # Iniciar kitty
            pid = iniciar_kitty()
            if not pid:
                print("✗ FALLÓ: No se pudo iniciar kitty")
                return False
            
            # Obtener colores iniciales
            print("\n   Colores iniciales:")
            colores = get_colors()
            if colores:
                print(f"   background: {colores.get('background', 'N/A')}")
            
            # Ejecutar tr-color
            exito = ejecutar_tr_color(ruta)
            
            # Esperar un momento
            time.sleep(0.3)
            
            # Obtener colores finales
            print("\n   Colores después de tr-color:")
            colores_finales = get_colors()
            if colores_finales:
                background_final = colores_finales.get('background', 'N/A')
                print(f"   background: {background_final}")
                
                # Verificar
                background_norm = background_final.lower().lstrip('#')
                color_esperado_norm = color_esperado.lower().lstrip('#')
                
                if background_norm == color_esperado_norm:
                    print(f"\n   ✓✓✓ COLOR CORRECTO: {color_esperado} ✓✓✓")
                    resultados.append((ruta, True, color_esperado, background_final))
                else:
                    print(f"\n   ✗ COLOR INCORRECTO: esperado {color_esperado}, obtenido {background_final}")
                    resultados.append((ruta, False, color_esperado, background_final))
            else:
                print("   ✗ No se pudo leer colores")
                resultados.append((ruta, False, color_esperado, 'N/A'))
            
            # Cerrar kitty
            cerrar_kitty(pid)
            pid = None
            
            # Pequeña pausa entre tests
            time.sleep(0.5)
        
        # Resumen final
        print("\n" + "=" * 70)
        print("RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        for ruta, exito, esperado, obtenido in resultados:
            estado = "✓" if exito else "✗"
            print(f"{estado} {os.path.basename(ruta)}: esperado={esperado}, obtenido={obtenido}")
        
        exitosos = sum(1 for _, e, _, _ in resultados if e)
        total = len(resultados)
        
        print(f"\nTotal: {exitosos}/{total} tests exitosos")
        
        return exitosos == total
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        if pid:
            cerrar_kitty(pid)
        return False

if __name__ == '__main__':
    print("Verificando prerequisitos...")
    
    if not subprocess.run(['which', 'kitty'], capture_output=True).returncode == 0:
        print("✗ kitty no está instalado")
        sys.exit(1)
    
    if not subprocess.run(['which', 'kitten'], capture_output=True).returncode == 0:
        print("✗ kitten no está instalado")
        sys.exit(1)
    
    tr_color_path = os.path.join(TR_BASE, 'bin/tr-color')
    if not os.path.exists(tr_color_path):
        print(f"✗ tr-color no existe: {tr_color_path}")
        sys.exit(1)
    
    print("✓ Prerequisitos OK")
    
    exito = test_tr_color()
    sys.exit(0 if exito else 1)

#!/usr/bin/env python3
import os
import time
import subprocess
from pathlib import Path

def test_kitty_command():
    test_file = Path("/home/daniel/tron/programas/TR/papelera/test_live_kitty.txt")
    if test_file.exists():
        test_file.unlink()
    
    print("🚀 Lanzando ventana de prueba...")
    # Lanzar kitty con un comando que escribe en papelera y se cierra
    cmd = f"echo 'KITTY_WORKS' > {test_file} && exit"
    subprocess.run(["kitty", "@", "launch", "--type=os-window", "--title=TEST_EXPERIMENTAL", "sh", "-c", cmd])
    
    print("⏳ Esperando ejecución...")
    time.sleep(3)
    
    if test_file.exists():
        with open(test_file, 'r') as f:
            content = f.read().strip()
            if content == "KITTY_WORKS":
                print("✅ PRUEBA EXITOSA: Kitty ejecutó el comando y escribió en papelera.")
                return True
    
    print("❌ PRUEBA FALLIDA: El archivo no se creó o el contenido es incorrecto.")
    return False

if __name__ == "__main__":
    test_kitty_command()

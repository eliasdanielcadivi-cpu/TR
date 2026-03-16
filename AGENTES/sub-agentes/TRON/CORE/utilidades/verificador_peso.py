#!/usr/bin/env python3
import subprocess
import os
import sys

def verificar_archivos_grandes(limite_mb=95):
    """
    Encuentra archivos en el repositorio que excedan un límite de tamaño.
    Devuelve una lista de tuplas (ruta, tamaño_mb) si los encuentra, o False si no.
    """
    archivos_grandes = []
    try:
        raiz_repo = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], 
            check=True, capture_output=True, text=True
        ).stdout.strip()
        
        archivos_git = subprocess.run(
            ["git", "ls-files", "-z"], 
            check=True, capture_output=True, text=True
        ).stdout.split('\0')
        
        limite_bytes = limite_mb * 1024 * 1024
        
        for archivo_rel in archivos_git:
            if not archivo_rel:
                continue
            
            ruta_abs = os.path.join(raiz_repo, archivo_rel)
            
            if os.path.exists(ruta_abs) and not os.path.islink(ruta_abs):
                tamano_bytes = os.path.getsize(ruta_abs)
                if tamano_bytes > limite_bytes:
                    tamano_mb = round(tamano_bytes / (1024 * 1024), 2)
                    archivos_grandes.append((ruta_abs, tamano_mb))

    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
        
    return archivos_grandes

if __name__ == '__main__':
    limite = 99
    if len(sys.argv) > 1:
        try:
            limite = int(sys.argv[1])
        except ValueError:
            print(f"Límite inválido. Usando {limite}MB.")

    lista_grandes = verificar_archivos_grandes(limite)
    if lista_grandes:
        print(f"Archivos grandes detectados (> {limite}MB):")
        for ruta, tamano in lista_grandes:
            print(f"- {ruta} ({tamano} MB)")
        sys.exit(1) # Salida con error para que los hooks puedan detener el proceso
    else:
        print(f"No se encontraron archivos que superen los {limite}MB.")
        sys.exit(0)

#!/usr/bin/env python3
import argparse
import sys
import json
import os
from pathlib import Path

# Añadir ruta de clases al path de python dinámicamente
# Base: TRON/CORE/herramientas/ -> TRON/CORE/
CORE_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(CORE_PATH))

from clases.git_core import GitCore

def main():
    parser = argparse.ArgumentParser(description="Gestor Git TRON JSON Interface")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomandos
    p_guardar = subparsers.add_parser("guardar")
    p_guardar.add_argument("-m", "--mensaje", default="Checkpoint TRON")

    p_volver = subparsers.add_parser("volver")
    p_volver.add_argument("-p", "--pasos", type=int, default=1)

    p_nube = subparsers.add_parser("nube")

    # Parsear
    args = parser.parse_args()
    
    # Ejecutar lógica
    core = GitCore()
    resultado = {}

    if args.comando == "guardar":
        resultado = core.guardar_cambios(args.mensaje)
    elif args.comando == "volver":
        resultado = core.retroceder_seguro(args.pasos)
    elif args.comando == "nube":
        resultado = core.sincronizar_nube()

    # SALIDA JSON DETERMINISTA
    print(json.dumps(resultado, ensure_ascii=False))

if __name__ == "__main__":
    main()

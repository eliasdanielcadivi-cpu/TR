#!/usr/bin/env python3
import sys
import os
import json
import argparse

# Asegurar que el directorio raíz de TR esté en el path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.ia.mcp.bridge import execute_bridge

def main():
    parser = argparse.ArgumentParser(description="Puente MCP ARES-TRON para Cajas Negras LLM")
    parser.add_argument("json_payload", help="El objeto JSON-RPC 2.0 emitido por el LLM")
    parser.add_argument("--path", default="/home/daniel", help="Ruta permitida para el servidor de archivos")
    parser.add_argument("--debug", action="store_true", help="Activa el logging detallado")
    
    args = parser.parse_args()
    
    # Ejecución del puente
    resultado = execute_bridge(args.json_payload, allowed_path=args.path, debug=args.debug)
    
    # Salida Headless (JSON Puro para captura)
    print(json.dumps(resultado))

if __name__ == "__main__":
    main()

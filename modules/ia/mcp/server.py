import subprocess
import json
import time

def start_mcp_process(command):
    """Inicia el subproceso del servidor MCP con tuberías configuradas."""
    return subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

def perform_mcp_handshake(process):
    """Ejecuta el protocolo de inicialización MCP (Handshake)."""
    init_req = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "Ares-MCP-Bridge", "version": "1.0"}
        }
    }
    process.stdin.write(json.dumps(init_req) + "\n")
    process.stdin.flush()
    
    # Leer respuesta de inicialización
    response = process.stdout.readline()
    
    # Notificación de inicialización completada (requerida por el estándar)
    initialized_notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    process.stdin.write(json.dumps(initialized_notif) + "\n")
    process.stdin.flush()
    
    return json.loads(response) if response else None

def send_and_receive(process, payload):
    """Envía un comando JSON-RPC y captura la respuesta del servidor."""
    process.stdin.write(json.dumps(payload) + "\n")
    process.stdin.flush()
    line = process.stdout.readline()
    return json.loads(line) if line else None

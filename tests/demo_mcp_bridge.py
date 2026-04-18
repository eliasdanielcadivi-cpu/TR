import subprocess
import json
import os

def run_bridge(payload, path="/home/daniel/tron/programas/TR/tests/mcp_lab"):
    cmd = ["/home/daniel/tron/programas/TR/bin/ares-mcp", "--path", path, json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return {"error": "Failed to parse JSON", "raw": result.stdout}

if __name__ == "__main__":
    lab_path = "/home/daniel/tron/programas/TR/tests/mcp_lab"
    
    print("--- 1. Listando Directorio ---")
    res1 = run_bridge({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "list_directory", "arguments": {"path": lab_path}}
    })
    print(json.dumps(res1, indent=2))
    
    print("\n--- 2. Escribiendo Archivo de Prueba ---")
    test_file = os.path.join(lab_path, "resultado_demo.txt")
    res2 = run_bridge({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "write_file", "arguments": {"path": test_file, "content": "Prueba exitosa del Puente MCP Ares-Tron\nFase 1 completada."}}
    })
    print(json.dumps(res2, indent=2))
    
    print("\n--- 3. Ejecutando Comando Bash (cat) ---")
    res3 = run_bridge({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "run_command", "arguments": {"command": f"cat {test_file}"}}
    })
    print(json.dumps(res3, indent=2))

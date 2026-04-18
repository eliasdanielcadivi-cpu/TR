import sys
import json
import subprocess
import time

def probe_server(name, command):
    print(f"Probing {name}...")
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "Probe", "version": "1.0"}
        }
    }
    
    process.stdin.write(json.dumps(init_req) + "\n")
    process.stdin.flush()
    
    # Wait a bit for response
    time.sleep(1)
    
    response = process.stdout.readline()
    print(f"Response from {name}: {response}")
    
    process.terminate()
    return response

if __name__ == "__main__":
    probe_server("bash", ["npx", "-y", "@modelcontextprotocol/server-bash"])
    probe_server("fs", ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/home/daniel/tron/programas/TR/tests/mcp_lab"])

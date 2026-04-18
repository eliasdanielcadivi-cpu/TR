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
    
    # Wait longer for response
    time.sleep(2)
    
    # Check if process is still alive
    if process.poll() is not None:
        print(f"{name} process exited with code {process.returncode}")
        print(f"Stderr: {process.stderr.read()}")
        return
    
    # Try to read all available output
    import fcntl
    import os
    fd = process.stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    
    try:
        response = process.stdout.read()
        print(f"Response from {name}: {response}")
    except Exception as e:
        print(f"Error reading from {name}: {e}")

    err = process.stderr.read()
    if err:
        print(f"Stderr from {name}: {err}")
    
    process.terminate()

if __name__ == "__main__":
    probe_server("bash", ["npx", "-y", "@modelcontextprotocol/server-bash"])

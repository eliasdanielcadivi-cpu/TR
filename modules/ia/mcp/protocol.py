import json

def validate_rpc_call(payload):
    """Valida que la entrada sea un JSON-RPC 2.0 válido."""
    if not isinstance(payload, dict):
        return False, "Payload debe ser un objeto JSON"
    if payload.get("jsonrpc") != "2.0":
        return False, "Versión JSON-RPC debe ser 2.0"
    if payload.get("method") not in ["tools/call", "tools/list"]:
        return False, "Método debe ser 'tools/call' o 'tools/list'"
    if payload.get("method") == "tools/call" and ("params" not in payload or "name" not in payload["params"]):
        return False, "Faltan parámetros obligatorios (params.name)"
    return True, None

def route_tool_to_command(tool_name, allowed_path="/home/daniel"):
    """Mapea el nombre de la herramienta al comando del servidor MCP correspondiente."""
    # bash-mcp utiliza 'run', 'run_background', 'kill_background', 'list_background'
    BASH_TOOLS = ["run", "run_background", "kill_background", "list_background", "run_command"]
    FS_TOOLS = ["read_file", "write_file", "list_directory", "move_file", "create_directory"]
    
    if tool_name in BASH_TOOLS:
        return ["npx", "-y", "bash-mcp"]
    elif tool_name in FS_TOOLS:
        return ["npx", "-y", "@modelcontextprotocol/server-filesystem", allowed_path]
    return None

def format_error_response(error_id, message):
    """Genera una respuesta de error JSON-RPC 2.0 estándar."""
    return {
        "jsonrpc": "2.0",
        "id": error_id,
        "error": {
            "code": -32601,
            "message": message
        }
    }

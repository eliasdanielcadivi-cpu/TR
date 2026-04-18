import sys
import json
import logging
from . import server
from . import protocol

def setup_bridge_logging(debug=False):
    """Configura el sistema de logging para el puente."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | [MCP_BRIDGE] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("MCP_Bridge")

def execute_bridge(llm_json_input, allowed_path="/home/daniel", debug=False):
    """Orquestador principal del puente MCP."""
    logger = setup_bridge_logging(debug)
    
    # 1. Parsear y Validar
    try:
        payload = json.loads(llm_json_input)
    except json.JSONDecodeError:
        return protocol.format_error_response(None, "JSON inválido")
    
    is_valid, error_msg = protocol.validate_rpc_call(payload)
    if not is_valid:
        return protocol.format_error_response(payload.get("id"), error_msg)
    
    # 2. Enrutar
    method = payload.get("method")
    if method == "tools/list":
        tool_name = "LIST_TOOLS"
        # Para listar herramientas, usamos el servidor de bash por defecto para inspección
        command = ["npx", "-y", "bash-mcp"]
    else:
        tool_name = payload["params"]["name"]
        # Remapeo automático para compatibilidad con el prompt sugerido
        if tool_name == "run_command":
            tool_name = "run"
            payload["params"]["name"] = "run"
            
        command = protocol.route_tool_to_command(tool_name, allowed_path)
    
    if not command:
        return protocol.format_error_response(payload.get("id"), f"Operación no soportada")
    
    # 3. Ejecutar ciclo de vida del servidor
    process = None
    try:
        logger.debug(f"Iniciando servidor para {tool_name}: {command}")
        process = server.start_mcp_process(command)
        
        # Handshake
        handshake_res = server.perform_mcp_handshake(process)
        logger.debug(f"Handshake completado: {handshake_res}")
        
        # Ejecución de herramienta
        result = server.send_and_receive(process, payload)
        return result
        
    except Exception as e:
        logger.error(f"Error en ejecución MCP: {str(e)}")
        return protocol.format_error_response(payload.get("id"), f"Excepción interna: {str(e)}")
    finally:
        if process:
            process.terminate()

if __name__ == "__main__":
    # Para pruebas directas desde CLI si fuera necesario
    if len(sys.argv) > 1:
        res = execute_bridge(sys.argv[1], debug=True)
        print(json.dumps(res, indent=2))

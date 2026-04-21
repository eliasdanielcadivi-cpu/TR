PRUEBA 1 CREAR ARCHIVO
./bin/ares-mcp --path /home/daniel/tron/programas/TR/tests/mcp_lab '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "write_file", "arguments": {"path": "/home/daniel/tron/programas/TR/tests/mcp_lab/test_script.py", "content": "print(\"Hola Mundo\")"}}}'
PRUEBA 2 LISTAR DIRECTORIO
./bin/ares-mcp --path /home/daniel/tron/programas/TR/tests/mcp_lab '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "list_directory", "arguments": {"path": "/home/daniel/tron/programas/TR/tests/mcp_lab"}}}'
PRUEBA 3 LEER ARCHIVO
./bin/ares-mcp --path /home/daniel/tron/programas/TR/tests/mcp_lab '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "read_file", "arguments": {"path": "/home/daniel/tron/programas/TR/tests/mcp_lab/test_script.py"}}}'
PRUEBA 4 EJECUTAR SCRIPT
./bin/ares-mcp '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "run_command", "arguments": {"command": "python3 /home/daniel/tron/programas/TR/tests/mcp_lab/test_script.py"}}}'
PRUEBA 5 RENOMBRAR ARCHIVO
./bin/ares-mcp '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "run_command", "arguments": {"command": "mv /home/daniel/tron/programas/TR/tests/mcp_lab/test_script.py /home/daniel/tron/programas/TR/tests/mcp_lab/final_script.py"}}}'
PRUEBA 6 MOVER A PAPELERA
./bin/ares-mcp '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "run_command", "arguments": {"command": "mv /home/daniel/tron/programas/TR/tests/mcp_lab/final_script.py /home/daniel/tron/programas/TR/tests/mcp_lab/papelera/"}}}'
PRUEBA 7 PRUEBA DE RED
./bin/ares-mcp '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "run_command", "arguments": {"command": "curl -I https://google.com"}}}'
PRUEBA 8 LISTAR HERRAMIENTAS MCP
./bin/ares-mcp '{"jsonrpc": "2.0", "id": 8, "method": "tools/list", "params": {}}'

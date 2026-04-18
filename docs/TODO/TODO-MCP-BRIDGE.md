# TODO: Implementación Puente MCP ARES-TRON

## FASE 1: INFRAESTRUCTURA Y PRUEBAS FORENSES (Actual)
- [ ] Crear estructura de directorios en `modules/ia/mcp/`.
- [ ] Guardar System Prompt en `config/prompts/mcp_system.prompt`.
- [ ] Captura Forense: Ejecutar pruebas manuales del JSON-RPC esperado y capturar salida de servidores MCP (`bash`, `filesystem`).
- [ ] Implementar Módulos Atómicos (Máx 3 funciones):
    - [ ] `modules/ia/mcp/server.py`: Gestión de procesos y handshake.
    - [ ] `modules/ia/mcp/protocol.py`: Enrutamiento y validación JSON-RPC.
    - [ ] `modules/ia/mcp/bridge.py`: Orquestador principal.
- [ ] Crear Bash Wrapper en `bin/ares-mcp`.
- [ ] Configurar entorno `test/mcp_lab/` con archivos de prueba.

## FASE 2: VALIDACIÓN Y REFINAMIENTO (PRUEBAS DE ESTRÉS)
- [ ] Pruebas de edición de texto en `test/mcp_lab/`.
- [ ] Pruebas de gestión de archivos (creación, borrado controlado a papelera).
- [ ] Implementar Bucle de Autocorrección (Self-Repair Loop) si el JSON es inválido.
- [ ] Validación Post-CRUD con `repo status`.

## FASE 3: INTEGRACIÓN AVANZADA (MEMORIA Y CONTEXTO)
- [ ] Integración con Memoria DSL V1.0.
- [ ] Inyección de documentos clave según contexto.
- [ ] Estado de documentos y trazabilidad de cambios.

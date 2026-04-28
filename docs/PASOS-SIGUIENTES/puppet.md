### 🟤 PRIORIDAD 7: FASE 4 - Ejecución (Pasos 85-94)

#### Ares Puppet (Pasos 85-89)

85. **Crear `modules/ia/puppet/`** - Directorio para módulo de control de terminal
86. **Crear `puppet_controller.py`** - Funciones: `launch_session()`, `run_command()`, `capture_output()`, `close_session()`
87. **Implementar `launch_session()`** - Lanzar sesión Kitty en socket específico con layout definido
88. **Implementar `run_command()`** - Enviar comando a sesión específica y esperar output
89. **Implementar sandbox de seguridad** - Lista blanca de comandos permitidos, bloqueo de comandos peligrosos (rm -rf, etc.)

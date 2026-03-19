#!/usr/bin/env python3
"""
Orchestrator: Inteligencia de despliegue dinámico con Trazabilidad Permanente.
Filosofía ARES: Genérico, rítmico y resiliente.
"""
import subprocess
import time
import json
import os
from pathlib import Path
from typing import Optional

class KittyOrchestrator:
    def __init__(self, ctx_obj):
        self.ctx = ctx_obj
        self.base_dir = Path(ctx_obj.base_path)
        self.trace_log = self.base_dir / "logs/orchestrator_trace.log"
        self.papelera = self.base_dir / "papelera"

        # Asegurar directorios
        self.trace_log.parent.mkdir(exist_ok=True)
        self.papelera.mkdir(exist_ok=True)

        # Ciclo Maestro de 12 Colores Hacker Neon
        self.color_cycle = [
            {'afg': '#00FFFF', 'ifg': '#00AAAA', 'abg': '#001A1A', 'ibg': '#000D0D'}, # 1. Cyan
            {'afg': '#FF00FF', 'ifg': '#AA00AA', 'abg': '#1A001A', 'ibg': '#0D000D'}, # 2. Magenta
            {'afg': '#39FF14', 'ifg': '#22AA00', 'abg': '#0A1A0A', 'ibg': '#050D05'}, # 3. Matrix Green
            {'afg': '#FF6600', 'ifg': '#AA4400', 'abg': '#1A0D00', 'ibg': '#0D0600'}, # 4. Orange
            {'afg': '#FF0000', 'ifg': '#AA0000', 'abg': '#1A0000', 'ibg': '#0D0000'}, # 5. Red
            {'afg': '#0000FF', 'ifg': '#0000AA', 'abg': '#00001A', 'ibg': '#00000D'}, # 6. Blue
            {'afg': '#FFFF00', 'ifg': '#AAAA00', 'abg': '#1A1A00', 'ibg': '#0D0D00'}, # 7. Yellow
            {'afg': '#00FFCC', 'ifg': '#00AA88', 'abg': '#001A14', 'ibg': '#000D0A'}, # 8. Teal
            {'afg': '#CC00FF', 'ifg': '#8800AA', 'abg': '#14001A', 'ibg': '#0A000D'}, # 9. Purple
            {'afg': '#FF0066', 'ifg': '#AA0044', 'abg': '#1A000A', 'ibg': '#0D0005'}, # 10. Hot Pink
            {'afg': '#66FF00', 'ifg': '#44AA00', 'abg': '#0A1A00', 'ibg': '#050D00'}, # 11. Electric Lime
            {'afg': '#0066FF', 'ifg': '#0044AA', 'abg': '#000A1A', 'ibg': '#00050D'}  # 12. Sky Blue
        ]

    def deploy_session_from_db(self, session_name, socket=None, new_window=True, register=True):
        """
        [FUNCIÓN PÚBLICA 1]
        Despliega una sesión con recuperación de errores y trazabilidad.

        Usa Socket Lifecycle Manager para:
        - Validar ruta y permisos del socket
        - Limpiar sockets huérfanos automáticamente
        - Esperar con timeout y validación activa
        
        Si register=True, registra la ventana en Window Registry para control futuro.

        Args:
            session_name: Nombre de la sesión
            socket: Socket personalizado (si None, genera uno único automático)
            new_window: Si True, crea nueva ventana Kitty
            register: Si True, registra en window_registry
        
        Returns:
            (success, message, socket_path): Tupla de resultado con socket usado

        Example:
            # Desplegar con socket único automático
            success, msg, socket = orch.deploy_session_from_db("diaria")
            print(f"Socket creado: {socket}")
            
            # Desplegar con socket personalizado
            success, msg, socket = orch.deploy_session_from_db("diaria", socket="/tmp/custom")
        """
        from modules.admon import session_manager
        from modules.core.socket_manager import (
            validate_socket_path,
            cleanup_orphan_socket,
            wait_for_socket_ready,
            generate_unique_socket
        )
        from modules.core.window_registry import (
            register_window,
            update_window_id
        )

        data = session_manager.load_session_data(self.ctx, session_name)
        if not data:
            return False, f"Sesión '{session_name}' no encontrada.", None

        # 🔧 NUEVO: Generar socket único si no se proporciona uno explícito
        target_socket = socket or generate_unique_socket(f"ares_session_{session_name}")

        # 1. Preparar Ventana
        if new_window:
            # 🔧 NUEVO: Validar socket antes de lanzar
            valid, error = validate_socket_path(target_socket)
            if not valid:
                self._log_error("VALIDATION", target_socket, "", f"Socket inválido: {error}")
                return False, f"Socket inválido: {error}", target_socket

            # 🔧 NUEVO: Limpiar socket huérfano
            cleaned, error = cleanup_orphan_socket(target_socket)
            if not cleaned:
                self._log_error("CLEANUP", target_socket, "", f"No se pudo limpiar: {error}")
                return False, f"No se pudo limpiar socket: {error}", target_socket

            window_title = self.ctx.config.get('identity', {}).get('window_title', "Ares por Daniel Hung")

            # 🔧 NUEVO: Configurar entorno ZSH como launch_hub
            env = os.environ.copy()
            env["ZDOTDIR"] = os.path.join(self.ctx.base_path, "config/zsh")

            # 🔧 NUEVO: Pasar configuración explícita de Kitty
            kitty_conf = getattr(self.ctx, 'kitty_conf', None)
            cmd_args = [
                "kitty",
                "--title", window_title,
                "--listen-on", f"unix:{target_socket}",
                "-o", "allow_remote_control=yes",
                "--detach"
            ]

            # Agregar config explícita si existe
            if kitty_conf and os.path.exists(kitty_conf):
                cmd_args.insert(1, "-c")
                cmd_args.insert(2, kitty_conf)

            proc = subprocess.Popen(cmd_args, env=env, start_new_session=True)

            # 🔧 NUEVO: Espera con validación activa y timeout
            success, error = wait_for_socket_ready(target_socket, timeout=15)
            if not success:
                self._log_error("SOCKET_WAIT", target_socket, "", error)
                return False, f"Socket no respondió: {error}", target_socket

            # 🔧 NUEVO: Registrar ventana en window_registry
            if register:
                register_window(
                    session_name=session_name,
                    socket_path=target_socket,
                    window_id=None,  # Se actualiza después
                    metadata={"pid": proc.pid, "session_name": session_name}
                )

        # 2. Orquestar Pestañas
        tab_count = 0
        all_tabs = []
        for os_window in data:
            all_tabs.extend(os_window.get('tabs', []))

        for tab in all_tabs:
            title = tab.get('title', f"TAB_{tab_count}")
            cmd = tab.get('cmd')
            color_config = self.color_cycle[tab_count % 12]
            
            if tab_count == 0 and new_window:
                # Mutar primera pestaña
                self._run_remote(target_socket, ["set-tab-title", "--match", "recent:0", title])
                if cmd and cmd.strip():
                    self._run_remote(target_socket, ["send-text", "--match", "recent:0", f"{cmd}\n"])
            else:
                # Lanzar nueva pestaña
                print(f"  ↳ Lanzando: {title}")
                args = ["launch", "--type=tab", "--tab-title", title]
                if cmd and cmd.strip():
                    # SISTEMA DE RESILIENCIA: Ejecuta el comando y luego lanza una shell 
                    # para que la pestaña NO se cierre sola. 
                    # Se elimina la redirección 2> porque algunas TUIs (Broot) la usan para la interfaz.
                    persist_cmd = f"{cmd}; echo '\n--- PROCESO FINALIZADO (Presiona Ctrl+C para salir o usa la shell) ---'; exec zsh -i"
                    args.extend(["sh", "-c", persist_cmd])
                
                self._run_remote(target_socket, launch_args=args)
            
            # Aplicar Pigmentación
            time.sleep(0.5) # Más tiempo para que Kitty registre el proceso
            self._apply_pigmentation(target_socket, title, color_config)

            tab_count += 1
            time.sleep(0.6) # Mayor estabilidad rítmica entre lanzamientos

        # 🔧 NUEVO: Obtener window_id y actualizar registro
        if new_window and register:
            try:
                window_id = self._get_window_id_for_socket(target_socket)
                if window_id:
                    from modules.core.window_registry import update_window_id
                    update_window_id(session_name, window_id)
            except Exception as e:
                self._log_error("WINDOW_ID", target_socket, "", f"No se pudo obtener window_id: {e}")

        return True, f"Desplegadas {tab_count} pestañas de '{session_name}'", target_socket

    def _get_window_id_for_socket(self, socket: str) -> Optional[int]:
        """
        Obtiene el window_id de Kitty para un socket dado.
        
        Args:
            socket: Ruta del socket
            
        Returns:
            window_id o None si no se pudo obtener
        """
        try:
            result = self._run_remote(socket, args=["ls"])
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                if data and len(data) > 0:
                    # Retornar el ID de la primera ventana
                    return data[0].get('id')
        except:
            pass
        return None

    def _apply_pigmentation(self, socket, title, c):
        self._run_remote(socket, [
            "set-tab-color", "--match", f"title:^{title}$",
            f"active_fg={c['afg']}", f"inactive_fg={c['ifg']}",
            f"active_bg={c['abg']}", f"inactive_bg={c['ibg']}"
        ])

    def _run_remote(self, socket, args=None, launch_args=None):
        """Ejecuta y registra trazas de error."""
        cmd = ["kitten", "@", "--to", f"unix:{socket}"]
        if args: cmd.extend(args)
        if launch_args: cmd.extend(launch_args)

        res = subprocess.run(cmd, capture_output=True, text=True)

        # Registrar traza si hay error
        if res.returncode != 0:
            self._log_error("REMOTE_CMD", socket, cmd, res.stderr)
        return res

    def _log_error(self, context: str, socket: str, cmd: list, error_msg: str):
        """
        Registra errores con información detallada para debugging.
        
        Args:
            context: Contexto del error (VALIDATION, CLEANUP, SOCKET_WAIT, REMOTE_CMD)
            socket: Ruta del socket involucrado
            cmd: Comando que falló (lista o string vacío)
            error_msg: Mensaje de error
        """
        with open(self.trace_log, "a", encoding="utf-8") as f:
            f.write(f"[{time.ctime()}] ERROR [{context}]\n")
            f.write(f"  SOCKET: {socket}\n")
            if cmd:
                f.write(f"  CMD: {' '.join(cmd) if isinstance(cmd, list) else cmd}\n")
            f.write(f"  ERROR: {error_msg}\n")
            
            # 🔧 NUEVO: Información adicional de diagnóstico
            normalized = socket.replace('unix:', '')
            f.write(f"  SOCKET_EXISTS: {os.path.exists(normalized)}\n")
            if os.path.exists(normalized):
                try:
                    import stat
                    file_stat = os.stat(normalized)
                    f.write(f"  SOCKET_MODE: {stat.filemode(file_stat.st_mode).strip()}\n")
                except:
                    pass
            
            f.write("-" * 60 + "\n")

    def _wait_for_socket(self, socket):
        """
        Espera pasiva a que el socket responda (legacy, usar wait_for_socket_ready).
        
        @deprecated Usar modules.core.socket_manager.wait_for_socket_ready
        """
        from modules.core.socket_manager import wait_for_socket_ready
        success, _ = wait_for_socket_ready(socket, timeout=10)
        return success

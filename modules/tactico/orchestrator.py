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

    def deploy_session_from_db(self, session_name, socket=None, new_window=True):
        """
        [FUNCIÓN PÚBLICA 1]
        Despliega una sesión con recuperación de errores y trazabilidad.
        """
        from modules.admon import session_manager
        data = session_manager.load_session_data(self.ctx, session_name)
        if not data:
            return False, f"Sesión '{session_name}' no encontrada."

        target_socket = socket or self.ctx.socket_path
        
        # 1. Preparar Ventana
        if new_window:
            window_title = self.ctx.config.get('identity', {}).get('window_title', "Ares por Daniel Hung")
            subprocess.Popen([
                "kitty", "--title", window_title, "--listen-on", f"unix:{target_socket}",
                "-o", "allow_remote_control=yes", "--detach"
            ])
            self._wait_for_socket(target_socket)

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
        
        return True, f"Desplegadas {tab_count} pestañas de '{session_name}'."

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
            with open(self.trace_log, "a") as f:
                f.write(f"[{time.ctime()}] CMD: {' '.join(cmd)}\n")
                f.write(f"STDOUT: {res.stdout}\n")
                f.write(f"STDERR: {res.stderr}\n")
                f.write("-" * 40 + "\n")
        return res

    def _wait_for_socket(self, socket):
        for _ in range(20):
            if self._run_remote(socket, args=["ls"]).returncode == 0: break
            time.sleep(0.5)

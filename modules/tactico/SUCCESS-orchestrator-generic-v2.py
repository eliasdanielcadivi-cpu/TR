#!/usr/bin/env python3
"""
Orchestrator: Inteligencia de despliegue dinámico impulsada por ciclos cromáticos.
Filosofía ARES: Genérico, modular y rítmico.
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
        
        # Ciclo Maestro de 12 Colores Hacker Neon (afg, ifg, abg, ibg)
        self.color_cycle = [
            {'afg': '#00FFFF', 'ifg': '#00AAAA', 'abg': '#001A1A', 'ibg': '#000D0D'}, # 1. Cyan (Cyberpunk)
            {'afg': '#FF00FF', 'ifg': '#AA00AA', 'abg': '#1A001A', 'ibg': '#0D000D'}, # 2. Magenta (Neon Goddess)
            {'afg': '#39FF14', 'ifg': '#22AA00', 'abg': '#0A1A0A', 'ibg': '#050D05'}, # 3. Matrix Green
            {'afg': '#FF6600', 'ifg': '#AA4400', 'abg': '#1A0D00', 'ibg': '#0D0600'}, # 4. Orange (Blade Runner)
            {'afg': '#FF0000', 'ifg': '#AA0000', 'abg': '#1A0000', 'ibg': '#0D0000'}, # 5. Red (Red Alert)
            {'afg': '#0000FF', 'ifg': '#0000AA', 'abg': '#00001A', 'ibg': '#00000D'}, # 6. Blue (Deep Blue)
            {'afg': '#FFFF00', 'ifg': '#AAAA00', 'abg': '#1A1A00', 'ibg': '#0D0D00'}, # 7. Yellow Neon
            {'afg': '#00FFCC', 'ifg': '#00AA88', 'abg': '#001A14', 'ibg': '#000D0A'}, # 8. Teal/Seafoam
            {'afg': '#CC00FF', 'ifg': '#8800AA', 'abg': '#14001A', 'ibg': '#0A000D'}, # 9. Purple
            {'afg': '#FF0066', 'ifg': '#AA0044', 'abg': '#1A000A', 'ibg': '#0D0005'}, # 10. Hot Pink
            {'afg': '#66FF00', 'ifg': '#44AA00', 'abg': '#0A1A00', 'ibg': '#050D00'}, # 11. Electric Lime
            {'afg': '#0066FF', 'ifg': '#0044AA', 'abg': '#000A1A', 'ibg': '#00050D'}  # 12. Sky Blue
        ]

    def deploy_session_from_db(self, session_name, socket=None, new_window=True):
        """
        [FUNCIÓN PÚBLICA 1]
        Carga una sesión desde db/ y la despliega con ciclo de colores.
        Lógica extraída de la prueba exitosa ares_final_master.py.
        """
        from modules.admon import session_manager
        data = session_manager.load_session_data(self.ctx, session_name)
        if not data:
            return False, f"Sesión '{session_name}' no encontrada en DB."

        target_socket = socket or self.ctx.socket_path
        
        # 1. Preparar Ventana Soberana (No se toca el título después de lanzar)
        if new_window:
            window_title = self.ctx.config.get('identity', {}).get('window_title', "ARES")
            subprocess.Popen([
                "kitty", "--title", window_title, "--listen-on", f"unix:{target_socket}",
                "-o", "allow_remote_control=yes", "--detach"
            ])
            self._wait_for_socket(target_socket)

        # 2. Orquestar Pestañas
        tab_count = 0
        for os_window in data:
            for tab in os_window.get('tabs', []):
                title = tab.get('title', f"TAB_{tab_count}")
                cmd = tab.get('cmd')
                
                # Obtener configuración de color para esta pestaña
                color_config = self.color_cycle[tab_count % 12]
                
                if tab_count == 0 and new_window:
                    # Mutar la primera pestaña creada automáticamente por Kitty
                    self._run_remote(target_socket, ["set-tab-title", "--match", "recent:0", title])
                    # Si la pestaña inicial tiene comando, inyectarlo (aunque GEMINI suele ser vacío)
                    if cmd and cmd.strip():
                        self._run_remote(target_socket, ["send-text", "--match", "recent:0", f"{cmd}\n"])
                else:
                    # Lanzar nueva pestaña
                    args = ["launch", "--type=tab", "--tab-title", title]
                    if cmd and cmd.strip():
                        # Inyección determinista vía sh -c exec
                        args.extend(["sh", "-c", f"exec {cmd}"])
                    self._run_remote(target_socket, launch_args=args)
                
                # Aplicar color (Match por título de la pestaña que acabamos de nombrar/crear)
                self._apply_pigmentation(target_socket, title, color_config)
                
                tab_count += 1
                time.sleep(0.5) # Estabilidad rítmica
        
        return True, f"Desplegadas {tab_count} pestañas de '{session_name}' con ciclo cromático."

    def apply_theme_by_index(self, tab_title, index, socket=None):
        """[FUNCIÓN PÚBLICA 2] Aplica color basado en índice."""
        target_socket = socket or self.ctx.socket_path
        color_config = self.color_cycle[index % 12]
        self._apply_pigmentation(target_socket, tab_title, color_config)

    def list_cycle_colors(self):
        """[FUNCIÓN PÚBLICA 3] Lista colores activos."""
        return [c['afg'] for c in self.color_cycle]

    # --- SOPORTE INTERNO ---
    def _apply_pigmentation(self, socket, title, c):
        self._run_remote(socket, [
            "set-tab-color", "--match", f"title:^{title}$",
            f"active_fg={c['afg']}", f"inactive_fg={c['ifg']}",
            f"active_bg={c['abg']}", f"inactive_bg={c['ibg']}"
        ])

    def _run_remote(self, socket, args=None, launch_args=None):
        cmd = ["kitten", "@", "--to", f"unix:{socket}"]
        if args: cmd.extend(args)
        if launch_args: cmd.extend(launch_args)
        return subprocess.run(cmd, capture_output=True, text=True)

    def _wait_for_socket(self, socket):
        for _ in range(20):
            if self._run_remote(socket, args=["ls"]).returncode == 0: break
            time.sleep(0.5)

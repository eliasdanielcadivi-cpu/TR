"""
Grafo Manager — Servidor arrows.app (Dibujante de Grafos Neo4j).

Lanza/detiene el servidor de arrows.app en una pestaña de Kitty
y abre el navegador con el sistema por defecto (xdg-open).

Métodos de cierre (3):
  1) Cerrar la pestaña Kitty → SIGTERM → cleanup trap
  2) Ctrl+C en la pestaña → SIGINT → cleanup trap
  3) ares grafo --stop → kill por PID + pgrep respaldo
"""

import os
import signal
import subprocess
import json
import time
import urllib.request
from pathlib import Path

from config import KittyRemote

# ── Constantes ──
PID_FILE = Path("/tmp/ares-grafoserver.pid")
ARROWS_DIR = Path("/home/daniel/tron/programas/arrows.app")


def start_grafo_server(ctx_obj, port=4200, no_browser=False):
    """
    Lanza arrows.app en pestaña Kitty + abre navegador.

    Args:
        ctx_obj: Contexto TR (para KittyRemote).
        port: Puerto del servidor (default 4200).
        no_browser: Si True, no abre navegador.

    Returns:
        dict: {"ok": bool, "pid": int|None, "port": int, "msg": str}
    """
    if not ARROWS_DIR.exists():
        return {"ok": False, "pid": None, "port": port,
                "msg": "Directorio arrows.app no encontrado"}

    # Verificar si ya hay uno corriendo
    if PID_FILE.exists():
        try:
            data = json.loads(PID_FILE.read_text())
            old_pid = data.get("pid")
            os.kill(old_pid, 0)
            return {"ok": False, "pid": old_pid, "port": port,
                    "msg": f"Ya hay servidor activo en PID {old_pid}. "
                           f"Detener con: ares grafo --stop"}
        except (ProcessLookupError, json.JSONDecodeError, OSError):
            PID_FILE.unlink(missing_ok=True)

    # Asegurar Kitty
    kitty = KittyRemote(ctx_obj)
    if not kitty.is_running():
        if not kitty.launch_hub():
            return {"ok": False, "pid": None, "port": port,
                    "msg": "No se pudo iniciar Kitty"}

    # Crear wrapper bash con signal traps
    wrapper_script = Path("/tmp/ares-grafoserver.sh")
    wrapper_content = f"""#!/bin/bash
set -e
PID_FILE="{PID_FILE}"
ARROWS_DIR="{ARROWS_DIR}"

cleanup() {{
    echo "🛑 Cerrando servidor arrows.app..."
    pkill -P $$ 2>/dev/null || true
    rm -f "$PID_FILE"
    exit 0
}}

trap cleanup SIGTERM SIGINT SIGHUP EXIT

cd "$ARROWS_DIR"
npx nx serve arrows-ts --host 0.0.0.0 --port {port} &
SERVER_PID=$!

echo '{{"pid": '$SERVER_PID', "port": {port}}}' > "$PID_FILE"
echo "🔷 arrows.app en http://localhost:{port} (PID: $SERVER_PID)"

wait $SERVER_PID
"""
    wrapper_script.write_text(wrapper_content)
    os.chmod(wrapper_script, 0o755)

    # Lanzar en pestaña Kitty
    tab_title = f"grafo :{port}"
    kitty.run([
        "launch", "--type=tab", f"--tab-title={tab_title}",
        "bash", str(wrapper_script)
    ])

    # Esperar a que el servidor arranque
    ready = False
    for _ in range(15):
        time.sleep(1)
        try:
            urllib.request.urlopen(f"http://localhost:{port}", timeout=1)
            ready = True
            break
        except Exception:
            continue

    # Abrir navegador
    browser_msg = ""
    if not no_browser:
        subprocess.Popen(
            ["xdg-open", f"http://localhost:{port}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        browser_msg = f" — Navegador abierto"

    # Leer PID del archivo
    pid = None
    if PID_FILE.exists():
        try:
            pid = json.loads(PID_FILE.read_text()).get("pid")
        except (json.JSONDecodeError, OSError):
            pass

    status = "listo" if ready else "arrancando (puede tardar)"
    return {
        "ok": True,
        "pid": pid,
        "port": port,
        "msg": f"Pestaña '{tab_title}' creada — {status}{browser_msg}"
    }


def stop_grafo_server():
    """
    Detiene el servidor arrows.app activo (3 métodos de respaldo).

    Returns:
        dict: {"ok": bool, "msg": str}
    """
    # Método 1: PID file
    if PID_FILE.exists():
        try:
            data = json.loads(PID_FILE.read_text())
            pid = data.get("pid")
            if pid:
                os.kill(pid, signal.SIGTERM)
                PID_FILE.unlink(missing_ok=True)
                # Respaldo: matar árbol de procesos
                subprocess.run(
                    ["pkill", "-f", "nx serve arrows-ts"],
                    capture_output=True
                )
                return {"ok": True, "msg": f"Servidor detenido (PID {pid})"}
        except (ProcessLookupError, json.JSONDecodeError):
            PID_FILE.unlink(missing_ok=True)

    # Método 2: pgrep por nombre de proceso
    result = subprocess.run(
        ["pgrep", "-f", "nx serve arrows-ts"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        pids = result.stdout.strip().split("\n")
        for p in pids:
            try:
                os.kill(int(p), signal.SIGTERM)
            except (ProcessLookupError, ValueError):
                pass
        return {"ok": True, "msg": "Servidor detenido por proceso"}

    return {"ok": False, "msg": "No hay servidor arrows.app activo"}


def check_grafo_status():
    """
    Verifica el estado del servidor arrows.app.

    Returns:
        dict: {"running": bool, "pid": int|None, "port": int|None, "msg": str}
    """
    if not PID_FILE.exists():
        return {"running": False, "pid": None, "port": None,
                "msg": "No hay servidor registrado"}

    try:
        data = json.loads(PID_FILE.read_text())
        pid = data.get("pid")
        port = data.get("port")
        os.kill(pid, 0)  # check alive
        return {"running": True, "pid": pid, "port": port,
                "msg": f"Corriendo en http://localhost:{port} (PID {pid})"}
    except (ProcessLookupError, json.JSONDecodeError, OSError):
        PID_FILE.unlink(missing_ok=True)
        return {"running": False, "pid": None, "port": None,
                "msg": "PID huérfano limpiado — servidor no activo"}

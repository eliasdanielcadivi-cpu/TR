"""
Memgraph Manager — Gestión de Docker + Memgraph (Mage + Lab).

Inicia/detiene el daemon Docker y los contenedores de Memgraph
desde TR/db/memgraph-platform/docker-compose.yml.

Servicios:
  - memgraph-mage: Base de datos graph (puertos 7687, 7444)
  - memgraph-lab:  UI web (puerto 3000)

Métodos de cierre (2):
  1) ares mem stop → docker compose down
  2) Cierre manual de contenedores (docker stop)
"""

import subprocess
import time
from pathlib import Path

# ── Constantes ──
MEMGRAPH_DIR = Path("/home/daniel/tron/programas/TR/db/memgraph-platform")
COMPOSE_FILE = MEMGRAPH_DIR / "docker-compose.yml"


def _sudo(cmd: str) -> subprocess.CompletedProcess:
    """Ejecuta comando con sudo usando pipe de contraseña."""
    return subprocess.run(
        f'echo "a" | sudo -S bash -c "{cmd}"',
        shell=True, capture_output=True, text=True
    )


def _docker_running() -> bool:
    """Verifica si el daemon Docker está corriendo."""
    try:
        r = subprocess.run(
            ["docker", "info"], capture_output=True, text=True, timeout=5
        )
        return r.returncode == 0
    except Exception:
        return False


def _compose(cmd: str) -> subprocess.CompletedProcess:
    """Ejecuta docker compose desde el directorio de Memgraph."""
    return subprocess.run(
        f'docker compose -f {COMPOSE_FILE} {cmd}',
        shell=True, capture_output=True, text=True, timeout=120
    )


def start_memgraph():
    """
    Inicia Docker daemon + contenedores Memgraph (Mage + Lab).

    Returns:
        dict: {"ok": bool, "services": list, "msg": str}
    """
    if not MEMGRAPH_DIR.exists():
        return {"ok": False, "services": [],
                "msg": f"Directorio no encontrado: {MEMGRAPH_DIR}"}

    if not COMPOSE_FILE.exists():
        return {"ok": False, "services": [],
                "msg": f"docker-compose.yml no encontrado en {MEMGRAPH_DIR}"}

    # 1) Asegurar Docker daemon
    if not _docker_running():
        r = _sudo("systemctl start docker")
        if r.returncode != 0:
            err = r.stderr.strip()
            return {"ok": False, "services": [],
                    "msg": f"No se pudo iniciar Docker daemon: {err}"}
        # Esperar a que Docker esté listo
        for _ in range(10):
            time.sleep(1)
            if _docker_running():
                break
        else:
            return {"ok": False, "services": [],
                    "msg": "Docker daemon no respondió tras 10s"}

    # 2) Verificar si ya están corriendo
    r = subprocess.run(
        ["docker", "ps", "--filter", "name=memgraph", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    running = [n.strip() for n in r.stdout.strip().split("\n") if n.strip()]
    if "memgraph-mage" in running and "memgraph-lab" in running:
        return {
            "ok": True,
            "services": running,
            "msg": "Memgraph ya está corriendo — memgraph-mage, memgraph-lab"
        }

    # 3) docker compose up -d
    r = _compose("up -d")
    if r.returncode != 0:
        err = (r.stderr or r.stdout).strip()
        return {"ok": False, "services": [],
                "msg": f"Error al iniciar contenedores: {err}"}

    # 4) Esperar a que los servicios estén listos
    time.sleep(3)
    r = subprocess.run(
        ["docker", "ps", "--filter", "name=memgraph",
         "--format", "{{.Names}}\t{{.Status}}"],
        capture_output=True, text=True
    )
    services = []
    for line in r.stdout.strip().split("\n"):
        if line.strip():
            name = line.split("\t")[0].strip()
            services.append(name)

    if "memgraph-mage" in services and "memgraph-lab" in services:
        return {
            "ok": True,
            "services": services,
            "msg": (
                "✅ Memgraph iniciado\n"
                "  🔷 memgraph-mage (DB):  bolt://localhost:7687  |  http://localhost:7444\n"
                "  🖥  memgraph-lab (UI):   http://localhost:3000"
            )
        }

    # Parcialmente iniciado
    return {
        "ok": True,
        "services": services,
        "msg": f"⚠️  Servicios iniciados: {services} (algunos pueden estar arrancando)"
    }


def stop_memgraph():
    """
    Detiene contenedores Memgraph via docker compose down.

    Returns:
        dict: {"ok": bool, "msg": str}
    """
    if not COMPOSE_FILE.exists():
        return {"ok": False, "msg": f"docker-compose.yml no encontrado"}

    # Verificar si hay algo que detener
    r = subprocess.run(
        ["docker", "ps", "--filter", "name=memgraph", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    running = [n.strip() for n in r.stdout.strip().split("\n") if n.strip()]
    if not running:
        return {"ok": True, "msg": "No hay contenedores Memgraph activos"}

    # docker compose down
    r = _compose("down")
    if r.returncode != 0:
        err = (r.stderr or r.stdout).strip()
        return {"ok": False, "msg": f"Error al detener contenedores: {err}"}

    return {
        "ok": True,
        "msg": "🛑 Memgraph detenido — memgraph-mage, memgraph-lab (Docker daemon sigue activo)"
    }


def memgraph_status():
    """
    Verifica el estado de Docker daemon y contenedores Memgraph.

    Returns:
        dict: {"docker": bool, "containers": list, "msg": str}
    """
    docker_up = _docker_running()
    status_parts = []

    # Docker daemon
    if docker_up:
        status_parts.append("🐳 Docker daemon: activo")
    else:
        status_parts.append("🐳 Docker daemon: inactivo")

    # Contenedores
    r = subprocess.run(
        ["docker", "ps", "-a", "--filter", "name=memgraph",
         "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"],
        capture_output=True, text=True
    )

    containers = []
    for line in r.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        name = parts[0].strip() if len(parts) > 0 else "?"
        status = parts[1].strip() if len(parts) > 1 else ""
        ports = parts[2].strip() if len(parts) > 2 else ""
        running = "Up" in status
        containers.append({
            "name": name, "status": status,
            "ports": ports, "running": running
        })
        icon = "🟢" if running else "🔴"
        port_summary = ports.replace("0.0.0.0:", "").replace("->", "←").replace("[::]:", "")
        status_parts.append(f"  {icon} {name}: {status} ({port_summary})")

    if not containers:
        status_parts.append("  ℹ️  Sin contenedores Memgraph registrados")

    # URLs útiles si están corriendo
    running_containers = [c["name"] for c in containers if c["running"]]
    if "memgraph-lab" in running_containers:
        status_parts.append("\n  🌐 UI: http://localhost:3000")
    if "memgraph-mage" in running_containers:
        status_parts.append("  🔌 Bolt: localhost:7687  |  HTTP: localhost:7444")

    return {
        "docker": docker_up,
        "containers": containers,
        "msg": "\n".join(status_parts)
    }

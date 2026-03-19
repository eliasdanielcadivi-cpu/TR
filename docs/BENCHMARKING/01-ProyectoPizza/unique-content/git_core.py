#!/usr/bin/env python3
import subprocess
import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# --- CONFIGURACIÓN DINÁMICA DE RUTAS ---
# Base: TRON/CORE/clases/ -> TRON/CORE/
CORE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = CORE_DIR.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "git_ops.log"
VERIFICADOR_PESO = CORE_DIR / "utilidades" / "verificador_peso.py"

# Configuración de Logging (Solo para humanos/auditoría, NO para el LLM)
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GitCore:
    def __init__(self):
        self.root = self._get_git_root()

    def _get_git_root(self):
        try:
            # Busca la raíz del repo git actual
            return subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], 
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except:
            return os.getcwd()

    def _run_cmd(self, cmd_list, cwd=None):
        """Ejecuta comandos silenciando el output para el usuario, pero guardándolo en logs."""
        try:
            logging.info(f"EJECUTANDO: {' '.join(cmd_list)}")
            result = subprocess.run(
                cmd_list,
                cwd=cwd or self.root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logging.info(f"EXITO: {result.stdout}")
                return {"success": True, "stdout": result.stdout.strip(), "stderr": ""}
            else:
                logging.error(f"FALLO: {result.stderr}")
                return {"success": False, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
        except Exception as e:
            logging.critical(f"EXCEPCION: {str(e)}")
            return {"success": False, "error": str(e)}

    def guardar_cambios(self, mensaje: str):
        """
        1. Verifica peso.
        2. Añade archivos.
        3. Hace commit si hay cambios.
        """
        # 1. Verificar peso (Hook interno)
        if VERIFICADOR_PESO.exists():
            # Usamos sys.executable para usar el mismo python del venv
            peso_check = self._run_cmd([sys.executable, str(VERIFICADOR_PESO)])
            if not peso_check["success"]:
                 return {
                    "estado": "error",
                    "razon": "Archivos grandes detectados",
                    "detalle": "Revisa el log o la salida del verificador.",
                    "accion": "Elimina archivos grandes o usa git lfs."
                }
        else:
            logging.warning("Verificador de peso no encontrado, saltando validación.")

        # 2. Git Add
        self._run_cmd(["git", "add", "-A"])
        
        # 3. Verificar cambios
        diff = self._run_cmd(["git", "diff", "--cached", "--quiet"])
        if diff["success"]: # Exit code 0 = No hay diferencias
            return {"estado": "neutro", "mensaje": "No hay cambios nuevos para guardar."}

        # 4. Commit
        commit = self._run_cmd(["git", "commit", "-m", mensaje])
        
        if commit["success"]:
            return {"estado": "exito", "mensaje": f"Checkpoint guardado: '{mensaje}'"}
        else:
            return {"estado": "error", "mensaje": "Fallo al crear commit", "debug": str(LOG_FILE)}

    def retroceder_seguro(self, pasos: int):
        """Usa git revert para deshacer cambios sin borrar historia."""
        try:
            pasos = int(pasos)
            if pasos < 1: raise ValueError
        except ValueError:
            return {"estado": "error", "mensaje": "Pasos debe ser un entero positivo."}

        rango = f"HEAD~{pasos}..HEAD"
        # --no-edit evita que git abra un editor de texto
        res = self._run_cmd(["git", "revert", "--no-edit", rango])
        
        if res["success"]:
            return {"estado": "exito", "mensaje": f"Se revirtieron los últimos {pasos} cambios de forma segura."}
        else:
            return {"estado": "error", "mensaje": "Conflicto al revertir. Revisa los archivos manualmente.", "log": str(LOG_FILE)}

    def sincronizar_nube(self):
        """Pull (rebase) + Push."""
        # Detectar rama
        rama_res = self._run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        if not rama_res["success"]: return {"estado": "error", "mensaje": "No es un repo git."}
        rama = rama_res["stdout"]

        # Pull
        pull = self._run_cmd(["git", "pull", "origin", rama, "--rebase"])
        if not pull["success"]:
            return {"estado": "error", "mensaje": "Fallo al descargar cambios (Pull). Posible conflicto.", "detalle": pull["stderr"]}

        # Push
        push = self._run_cmd(["git", "push", "origin", rama])
        if push["success"]:
            return {"estado": "exito", "mensaje": "Sincronización con la nube completada."}
        else:
            return {"estado": "error", "mensaje": "Fallo al subir cambios (Push).", "detalle": push["stderr"]}

"""
Phase Manager - ARES-TRON.
Detecta la fase del ciclo de vida del proyecto basándose en evidencias físicas.
Filosofía: Mandato No-Asunción (Fase Forense).
"""
import os
from pathlib import Path

def detect_current_phase(project_path: str) -> str:
    """
    Analiza el entorno y determina la fase: INIT, DEV, MAINT o PROD.
    """
    path = Path(project_path)
    
    # 1. INIT: Si no existe LEEME.md o IA-CONTINUITY-REPORT.md
    if not (path / "LEEME.md").exists() or not (path / "IA-CONTINUITY-REPORT.md").exists():
        return "INIT"
    
    # 2. PROD: Si existe carpeta dist/ o si el archivo .env tiene modo producción
    if (path / "dist").exists() or (path / "build").exists():
        return "PROD"
    
    # 3. MAINT: Si hay una carpeta 'papelera' con contenido reciente
    if (path / "papelera").exists() and any((path / "papelera").iterdir()):
        return "MAINT"
    
    # 4. Default: DEV
    return "DEV"

def get_phase_rules(phase: str) -> dict:
    """
    Retorna las reglas de inyección según la fase detectada.
    """
    rules = {
        "INIT": {
            "strategy": "WORKFLOW_STRICT",
            "required_skills": ["Arquitectura Tree-L3", "Creación de Contratos"],
            "tools": ["file_manager", "shell"]
        },
        "DEV": {
            "strategy": "HYBRID_SEMANTIC",
            "required_skills": ["Atomicidad Paranoica", "Fase Forense"],
            "tools": ["all"]
        },
        "PROD": {
            "strategy": "DETERMINISTIC_ONLY",
            "required_skills": ["Auditoría de Calidad", "Globalización"],
            "tools": ["diag_manager"]
        }
    }
    return rules.get(phase, rules["DEV"])

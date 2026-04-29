"""
Session Mapper - ARES-TRON.
Traductor Forense: Hash (Inmutable) <-> Índice CLI (Volátil).
Filosofía: Máximo 3 funciones principales.
"""
import subprocess
import re

def sync_with_gemini() -> list:
    """
    Parsea la CLI y retorna una lista de diccionarios con {index, title, hash}.
    Es la 'Fase Forense' de la sesión.
    """
    try:
        result = subprocess.run(["gemini", "--list-sessions"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        
        sessions = []
        # Regex para capturar índice, título y hash: "  25. Título... (time) [hash]"
        pattern = r"^\s*(\d+)\.\s+(.*?)\s+\(.*?\)\s+\[(.*?)\]"
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                sessions.append({
                    "index": int(match.group(1)),
                    "title": match.group(2).strip(),
                    "hash": match.group(3).strip()
                })
        return sessions
    except:
        return []

def resolve_session_id(explicit_chat: int = None, force_new: bool = False) -> int:
    """
    Resuelve el ID de sesión según prioridad:
    1. Chat explícito.
    2. Nueva sesión si force_new es True.
    3. Última sesión registrada en la DB de ARES.
    4. Última sesión global de Gemini.
    """
    if explicit_chat is not None:
        return explicit_chat
    if force_new:
        return None
    
    from modules.core.session_db import get_ares_sessions
    ares_sessions = get_ares_sessions()
    if ares_sessions:
        return get_index_by_hash(ares_sessions[0]["hash"])
    
    latest = get_latest_session_info()
    return latest["index"] if latest else None

def get_index_by_hash(target_hash: str) -> int:
    """
    Busca el índice actual de un Hash en la CLI de Gemini.
    """
    sessions = sync_with_gemini()
    for s in sessions:
        if s["hash"] == target_hash:
            return s["index"]
    return None

def get_latest_session_info() -> dict:
    """
    Retorna la información completa de la última sesión creada.
    """
    sessions = sync_with_gemini()
    return sessions[-1] if sessions else None

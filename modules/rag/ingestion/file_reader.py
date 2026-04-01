import os
import hashlib
from pathlib import Path

def read_text_file(file_path: str) -> str:
    """Lee el contenido de un archivo manejando codificaciones comunes."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception:
        return ""

def generate_doc_id(file_path: str, content: str) -> str:
    """Genera un ID único para el documento."""
    unique_str = f"{file_path}:{len(content)}:{content[:500]}"
    return hashlib.sha256(unique_str.encode()).hexdigest()[:32]

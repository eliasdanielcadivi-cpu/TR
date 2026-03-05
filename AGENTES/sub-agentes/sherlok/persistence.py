import sqlite3
import hashlib
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "sherlok.db"

def init_db():
    """Inicializa la base de datos de huellas digitales."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            path TEXT PRIMARY KEY,
            fingerprint TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_stored_fingerprint(path):
    """Recupera la huella digital almacenada para una ruta."""
    conn = sqlite3.connect(DB_PATH)
    res = conn.execute("SELECT fingerprint FROM scans WHERE path = ?", (path,)).fetchone()
    conn.close()
    return res[0] if res else None

def update_scan_record(path, data_dict):
    """Calcula y almacena la nueva huella digital."""
    # Crear huella basada en estructura, ayuda y muestra de código
    content = f"{data_dict.get('structure', '')}{data_dict.get('help_text', '')}{data_dict.get('source_sample', '')}"
    fingerprint = hashlib.sha256(content.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO scans (path, fingerprint, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)", 
                 (path, fingerprint))
    conn.commit()
    conn.close()
    return fingerprint

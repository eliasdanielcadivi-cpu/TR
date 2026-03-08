import os
import json
from pathlib import Path

def capture_and_save(ctx_obj, kitty, session_name):
    """
    Captura el estado actual de Kitty (ventanas/pestañas) y lo guarda en la base de datos JSON.
    """
    # 1. Obtener datos crudos de Kitty
    raw_ls = kitty.run(["ls"])
    if not raw_ls:
        return False, "No se pudo obtener información del socket de Kitty."

    try:
        session_data = json.loads(raw_ls)
    except json.JSONDecodeError:
        return False, "Error al decodificar la respuesta JSON de Kitty."

    # 2. Procesar estructura simplificada para restauración
    summary = []
    for os_window in session_data:
        tabs_info = []
        for tab in os_window.get('tabs', []):
            tabs_info.append({
                "tab_id": tab.get('id'),
                "title": tab.get('title'),
                "is_active": tab.get('is_active', False),
                "layout": tab.get('layout', 'tall')
            })
            
        summary.append({
            "os_window_id": os_window.get('id'),
            "is_focused": os_window.get('is_focused', False),
            "tabs": tabs_info
        })

    # 3. Guardar en DB
    db_dir = Path(ctx_obj.base_path) / "db"
    db_dir.mkdir(exist_ok=True)
    
    file_path = db_dir / f"{session_name}.json"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)
        return True, str(file_path)
    except Exception as e:
        return False, f"Error al escribir en disco: {e}"

def list_sessions(ctx_obj):
    """Lista las sesiones guardadas en el directorio db/."""
    db_dir = Path(ctx_obj.base_path) / "db"
    if not db_dir.exists():
        return []
    return [f.stem for f in db_dir.glob("*.json")]

def load_session_data(ctx_obj, session_name):
    """Carga los datos de una sesión específica."""
    file_path = Path(ctx_obj.base_path) / "db" / f"{session_name}.json"
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

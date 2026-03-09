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
    # Retornar lista de nombres de archivos .json sin extensión
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

def restore_session(ctx_obj, kitty, session_name):
    """
    Restaura las pestañas de una sesión guardada.
    """
    data = load_session_data(ctx_obj, session_name)
    if not data:
        return False, f"Sesión '{session_name}' no encontrada."

    # En la estructura actual, 'data' es una lista de OS Windows.
    # Por simplicidad en la v1, restauramos todas las pestañas de todas las ventanas en la ventana actual.
    count = 0
    commands_to_run = []
    
    for os_window in data:
        for tab in os_window.get('tabs', []):
            title = tab.get('title', f"TAB_{count}")
            cmd = tab.get('cmd')
            
            # Lanzar pestaña con su título original
            kitty.run(["launch", "--type=tab", f"--tab-title={title}"])
            
            # Si hay comando guardado en el JSON (manualmente o futuro feature), encolarlo
            if cmd and cmd not in ["zsh", "bash", "sh"]:
                commands_to_run.append((title, cmd))
            
            count += 1
    
    # Ejecutar comandos iniciales con un pequeño delay para asegurar que la shell cargó
    if commands_to_run:
        import time
        time.sleep(1.5)  # Dar tiempo a zsh para iniciar
        for title, command in commands_to_run:
            send_command_to_tab(kitty, title, command)
    
    return True, f"Se restauraron {count} pestañas de la sesión '{session_name}'."

def send_command_to_tab(kitty, tab_title, cmd):
    """
    Envía un comando (o varios separados por ;) a una pestaña específica por título.
    """
    # Si el comando contiene ;, Kitty send-text lo enviará tal cual y la shell lo interpretará
    # Usamos \n al final para ejecutarlo
    full_cmd = f"{cmd}\n"
    args = ["send-text", "--match", f"title:^{tab_title}$", full_cmd]
    
    try:
        kitty.run(args)
        return True, f"Comando enviado a pestaña '{tab_title}'."
    except Exception as e:
        return False, f"Error al enviar comando: {e}"

#!/usr/bin/env python3
"""
Session Editor: Editor interactivo de sesiones guardadas en db/*.json.

Permite modificar configuraciones de sesiones (títulos de pestañas, comandos)
de forma estructurada y segura.

Directiva: Máximo 3 funciones principales (modularidad atómica).
"""
import json
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List, Dict


def load_session_file(ctx_obj, session_name: str) -> Tuple[Optional[List], Optional[str]]:
    """
    Carga una sesión desde db/{session_name}.json.

    Args:
        ctx_obj: Contexto ARES con base_path
        session_name: Nombre de la sesión (sin extensión)

    Returns:
        (data, error): Tupla con datos o mensaje de error
    """
    file_path = Path(ctx_obj.base_path) / "db" / f"{session_name}.json"
    
    if not file_path.exists():
        return None, f"Sesión '{session_name}' no encontrada en db/"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Error al parsear JSON: {e}"
    except Exception as e:
        return None, f"Error al leer archivo: {e}"


def save_session_file(ctx_obj, session_name: str, data: List) -> Tuple[bool, str]:
    """
    Guarda una sesión en db/{session_name}.json con backup automático.

    Args:
        ctx_obj: Contexto ARES con base_path
        session_name: Nombre de la sesión
        data: Datos JSON a guardar

    Returns:
        (success, message): Tupla de resultado
    """
    db_dir = Path(ctx_obj.base_path) / "db"
    db_dir.mkdir(exist_ok=True)
    
    file_path = db_dir / f"{session_name}.json"
    backup_path = db_dir / f"{session_name}.json.bak"
    
    # Crear backup si existe
    if file_path.exists():
        try:
            import shutil
            shutil.copy2(file_path, backup_path)
        except Exception as e:
            return False, f"Error al crear backup: {e}"
    
    # Guardar nueva versión
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True, f"Sesión '{session_name}' guardada en {file_path}"
    except Exception as e:
        # Restaurar backup si falla
        if backup_path.exists():
            try:
                import shutil
                shutil.copy2(backup_path, file_path)
            except:
                pass
        return False, f"Error al guardar: {e}"


def edit_session_interactive(ctx_obj, session_name: str) -> Tuple[bool, str]:
    """
    Editor interactivo de sesiones usando micro editor.

    Abre el archivo JSON en el editor micro para edición manual,
    luego valida la estructura.

    Args:
        ctx_obj: Contexto ARES con base_path
        session_name: Nombre de la sesión a editar

    Returns:
        (success, message): Tupla de resultado

    Structure expected:
        [
            {
                "is_focused": true,
                "tabs": [
                    {"title": "TAB_TITLE", "cmd": "comando;a-ejecutar"},
                    {"title": "ANOTHER_TAB", "cmd": ""}
                ]
            }
        ]
    """
    from config import KittyRemote
    
    # Cargar sesión actual
    data, error = load_session_file(ctx_obj, session_name)
    if error:
        return False, error
    
    # Mostrar información de la sesión
    print(f"\n📝 Editando sesión: [bold cyan]{session_name}[/bold cyan]")
    print(f"📊 Pestañas encontradas: {sum(len(w.get('tabs', [])) for w in data)}")
    print(f"📁 Ventanas: {len(data)}")
    print("\n[yellow]Instrucciones:[/yellow]")
    print("  • Edita el archivo JSON en el editor micro")
    print("  • Modifica 'title' para cambiar nombre de pestaña")
    print("  • Modifica 'cmd' para cambiar comando (usa ';' para múltiples)")
    print("  • Guarda y cierra (Ctrl+Q en micro)")
    print("  • El sistema validará la estructura automáticamente\n")
    
    input("Presiona Enter para abrir el editor...")
    
    # Obtener ruta del archivo
    file_path = Path(ctx_obj.base_path) / "db" / f"{session_name}.json"
    
    # Abrir con micro editor
    kitty = KittyRemote(ctx_obj)
    try:
        # Ejecutar micro en la terminal actual
        subprocess.run(["micro", str(file_path)], check=False)
    except FileNotFoundError:
        return False, "Editor 'micro' no encontrado. Instálalo con: sudo apt install micro"
    
    # Validar estructura después de editar
    print("\n🔍 Validando estructura...")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            edited_data = json.load(f)
        
        # Validación básica de estructura
        if not isinstance(edited_data, list):
            return False, "Error: El archivo debe contener una lista de ventanas"
        
        for i, window in enumerate(edited_data):
            if not isinstance(window, dict):
                return False, f"Error: Ventana {i} debe ser un objeto JSON"
            if "tabs" not in window:
                return False, f"Error: Ventana {i} debe tener 'tabs'"
            if not isinstance(window["tabs"], list):
                return False, f"Error: 'tabs' en ventana {i} debe ser una lista"
            
            for j, tab in enumerate(window["tabs"]):
                if not isinstance(tab, dict):
                    return False, f"Error: Pestaña {j} en ventana {i} debe ser objeto JSON"
                if "title" not in tab:
                    return False, f"Error: Pestaña {j} en ventana {i} debe tener 'title'"
                if "cmd" not in tab:
                    tab["cmd"] = ""  # Agregar cmd si falta
        
        print("✅ Estructura válida!")
        return True, f"Sesión '{session_name}' editada correctamente"
        
    except json.JSONDecodeError as e:
        # Restaurar backup si hay error de JSON
        backup_path = Path(ctx_obj.base_path) / "db" / f"{session_name}.json.bak"
        if backup_path.exists():
            try:
                import shutil
                shutil.copy2(backup_path, file_path)
                print("🔄 Backup restaurado automáticamente")
            except:
                pass
        return False, f"Error: JSON inválido después de editar: {e}"

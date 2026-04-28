"""
Módulo Gemini Wrapper - ARES OpenCore.
Encargado de la interacción determinista con gemini-cli.
Regla: Máximo 3 funciones públicas.
"""
import subprocess
import json
import os

def invoke_chat(prompt: str, chat_id: int = None, yolo: bool = True) -> str:
    """Invoca a gemini-cli. Si chat_id es None, crea una sesión nueva."""
    cmd = ["gemini"]
    if chat_id is not None:
        cmd.extend(["--resume", str(chat_id)])
    
    if yolo:
        cmd.append("--yolo")
    
    cmd.append(prompt)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: Fallo en gemini-cli: {e.stderr}"

def get_headless_json(prompt: str, chat_id: int) -> str:
    """Versión para automatización industrial (Salida JSON)."""
    # Envolvemos el prompt para exigir JSON si es necesario
    json_prompt = f"{prompt}. Responde estrictamente en formato JSON válido."
    output = invoke_chat(json_prompt, chat_id)
    
    try:
        # Intentar validar si es JSON
        json.loads(output)
        return output
    except:
        return json.dumps({"status": "error", "raw_output": output, "message": "No se obtuvo un JSON válido"})

def sync_gemini_identity(base_path: str) -> bool:
    """Sincroniza el archivo GEMINI.md del sistema con el contexto del wrapper."""
    # Aquí iría la lógica determinista para renombrar/inyectar identidades
    # Por ahora retorna éxito si el archivo maestro existe
    master_identity = os.path.join(base_path, "config/identidad/ares.yaml")
    return os.path.exists(master_identity)

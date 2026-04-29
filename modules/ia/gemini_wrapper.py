"""
Gemini Wrapper - ARES-TRON.
Corrección de flags para gemini-cli (-o json).
"""
import subprocess
import json
import os

def invoke_chat(prompt: str, chat_id: int = None, yolo: bool = True) -> str:
    """Invoca a gemini-cli con el formato de salida correcto."""
    cmd = ["gemini"]
    if chat_id is not None:
        cmd.extend(["--resume", str(chat_id)])
    
    if yolo:
        cmd.append("--yolo")
    
    # Flag correcto: -o json
    cmd.extend(["-o", "json"])
    cmd.append(prompt)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        try:
            data = json.loads(result.stdout)
            # Extraer contenido de la respuesta JSON de gemini-cli
            return data.get("content", data.get("text", result.stdout))
        except:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: Fallo en gemini-cli: {e.stderr}"
    except Exception as e:
        return f"ERROR: {str(e)}"

def get_headless_json(prompt: str, chat_id: int) -> str:
    """Usa el mismo motor para consistencia."""
    return invoke_chat(prompt, chat_id, yolo=True)

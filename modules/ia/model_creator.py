"""Model Creator - ARES-TRON.
Soberanía de Modelos: Gestión de modelos Ollama desde el sistema.
Regla: Máximo 3 funciones principales.
"""
import subprocess
import json
import logging

logger = logging.getLogger("ARES-Model-Creator")

def list_ollama_models():
    """Lista los modelos instalados en Ollama."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al listar modelos: {e}")
        return "Error al conectar con Ollama."

def create_ollama_model(model_name: str, modelfile_content: str):
    """Crea un nuevo modelo en Ollama a partir de un Modelfile."""
    try:
        process = subprocess.Popen(
            ["ollama", "create", model_name, "-f", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=modelfile_content)
        if process.returncode == 0:
            return f"Modelo '{model_name}' creado exitosamente."
        else:
            return f"Error al crear modelo: {stderr}"
    except Exception as e:
        logger.error(f"Error en create_ollama_model: {e}")
        return str(e)

def delete_ollama_model(model_name: str):
    """Elimina un modelo de Ollama."""
    try:
        subprocess.run(["ollama", "rm", model_name], check=True)
        return f"Modelo '{model_name}' eliminado exitosamente."
    except subprocess.CalledProcessError as e:
        return f"Error al eliminar modelo: {e}"

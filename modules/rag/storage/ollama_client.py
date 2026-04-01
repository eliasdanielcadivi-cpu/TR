import requests
import logging
from ...utils import messenger

logger = logging.getLogger(__name__)

def is_ollama_running(url="http://localhost:11434") -> bool:
    """Verificación bruta de salud de Ollama."""
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def get_embedding_safe(text: str, model: str = "mxbai-embed-large:335m"):
    """
    Obtiene embedding avisando al usuario si Ollama no está disponible.
    Atomicidad: No hace búsqueda KNN, solo comunicación e infra.
    """
    if not is_ollama_running():
        messenger.warn("Ollama no está corriendo. La búsqueda semántica (T2) será omitida.")
        return None
        
    try:
        # Aquí iría la llamada real a ollama.embed
        import ollama
        res = ollama.embed(model=model, input=[text])
        return res['embeddings'][0]
    except Exception as e:
        messenger.error(f"Fallo al generar embedding: {e}")
        return None

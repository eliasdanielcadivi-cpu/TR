import unicodedata
import re

def normalize_text(text: str) -> str:
    """
    Normaliza texto: elimina acentos, convierte a minúsculas y limpia caracteres.
    Garantiza que 'documentación' y 'documentacion' sean el mismo dato bruto.
    """
    if not text: return ""
    
    # Convertir a minúsculas
    text = text.lower()
    
    # Eliminar acentos (descomposición NFD y filtrar no-espaciados)
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    # Limpiar caracteres no alfanuméricos (manteniendo espacios)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Colapsar espacios
    return ' '.join(text.split())

def extract_keywords_clean(text: str, min_len: int = 3) -> list:
    """Extrae palabras clave normalizadas."""
    normalized = normalize_text(text)
    return [w for w in normalized.split() if len(w) >= min_len]

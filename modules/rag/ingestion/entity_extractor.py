import re
from typing import List, Dict

def extract_entities_basic(text: str) -> List[Dict]:
    """
    Extrae entidades basadas en capitalización y patrones markdown.
    """
    entities = []
    
    # 1. Patrón para headings de markdown
    headings = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
    for h in headings:
        entities.append({'name': h.strip(), 'type': 'heading'})
        
    # 2. Patrón para palabras en mayúsculas (Acrónimos/Nombres)
    words = re.findall(r'\b[A-Z][a-z]{3,}(?:\s+[A-Z][a-z]{3,})*\b', text)
    for w in words:
        entities.append({'name': w.strip(), 'type': 'proper_name'})
        
    # Eliminar duplicados
    seen = set()
    unique = []
    for e in entities:
        if e['name'].lower() not in seen:
            seen.add(e['name'].lower())
            unique.append(e)
            
    return unique

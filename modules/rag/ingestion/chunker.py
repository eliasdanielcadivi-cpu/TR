from typing import List

def split_into_chunks(content: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Divide el texto en fragmentos con solapamiento.
    Atomicidad: División por caracteres, sin lógica de markdown compleja aún.
    """
    if not content: return []
    
    chunks = []
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunks.append(content[start:end])
        start += (chunk_size - overlap)
    return chunks

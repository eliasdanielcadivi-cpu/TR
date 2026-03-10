"""Apollo Embeddings: Generación de vectores semánticos vía Ollama.

Módulo atómico que genera embeddings usando mxbai-embed-large:335m
(1024 dimensiones) vía Ollama API nativa.

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import ollama
import numpy as np
from typing import List, Tuple, Optional


# Configuración por defecto (desde config.yaml)
DEFAULT_MODEL = "mxbai-embed-large:335m"
DEFAULT_DIMENSIONS = 1024


def embed_text(text: str, model: str = DEFAULT_MODEL) -> np.ndarray:
    """Generar embedding para un texto único.

    Args:
        text: Texto a embedder.
        model: Modelo Ollama (default: mxbai-embed-large:335m).

    Returns:
        Numpy array float32 (1024 dimensiones).

    Nota: Usa ollama.embed() nativo con batch processing interno.
    """
    response = ollama.embed(model=model, input=[text])
    embeddings = response['embeddings']
    return np.array(embeddings[0], dtype=np.float32)


def embed_documents(
    texts: List[str],
    model: str = DEFAULT_MODEL,
    batch_size: int = 1
) -> List[np.ndarray]:
    """Generar embeddings para múltiples textos en batch.

    Args:
        texts: Lista de textos a embedder.
        model: Modelo Ollama.
        batch_size: Tamaño de lote para procesamiento (default: 1).

    Returns:
        Lista de numpy arrays float32 (1024 dimensiones cada uno).

    Nota: Batch size 1 por defecto para evitar exceder contexto del modelo.
    """
    all_embeddings = []

    # Procesar en batches pequeños (algunos modelos tienen límite de contexto)
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            response = ollama.embed(model=model, input=batch)
            batch_embeddings = [
                np.array(emb, dtype=np.float32)
                for emb in response['embeddings']
            ]
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            # Si falla, intentar con texto muy truncado (límite ~2048 tokens = ~8000 chars)
            truncated = [t[:4000] for t in batch]
            response = ollama.embed(model=model, input=truncated)
            batch_embeddings = [
                np.array(emb, dtype=np.float32)
                for emb in response['embeddings']
            ]
            all_embeddings.extend(batch_embeddings)

    return all_embeddings


def quantize_embeddings(
    vectors: np.ndarray,
    bits: int = 8
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cuantizar embeddings para reducir memoria 50-75%.

    Args:
        vectors: Array 2D (n_samples, n_dimensions) float32.
        bits: Bits por componente (4 o 8, default: 8).

    Returns:
        Tupla (quantized, scales, zero_points):
        - quantized: Array int8/int4 cuantizado
        - scales: Escalas por dimensión para dequantización
        - zero_points: Puntos cero por dimensión

    Nota: Cuantización simétrica por canal (channel-wise).
          Para dequantizar: (quantized - zero_points) * scales
    """
    if bits == 4:
        min_val, max_val = -8, 7  # int4 rango
    else:
        min_val, max_val = -128, 127  # int8 rango

    # Calcular min/max por dimensión
    min_vals = vectors.min(axis=0)
    max_vals = vectors.max(axis=0)

    # Evitar división por cero
    range_vals = max_vals - min_vals
    scales = np.where(range_vals == 0, 1.0, range_vals / (max_val - min_val))

    # Calcular zero points
    zero_points = np.round(min_val - (min_vals / scales)).astype(np.int8 if bits == 8 else np.int16)

    # Cuantizar
    quantized = np.clip(
        np.round(vectors / scales + zero_points),
        min_val,
        max_val
    ).astype(np.int8 if bits == 8 else np.int16)

    return quantized, scales, zero_points


def dequantize_embeddings(
    quantized: np.ndarray,
    scales: np.ndarray,
    zero_points: np.ndarray
) -> np.ndarray:
    """Dequantizar embeddings para búsqueda vectorial.

    Args:
        quantized: Array cuantizado (int8 o int16).
        scales: Escalas por dimensión.
        zero_points: Puntos cero por dimensión.

    Returns:
        Array float32 dequantizado.
    """
    return (quantized.astype(np.float32) - zero_points) * scales

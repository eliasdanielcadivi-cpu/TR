"""Apollo Generation: Generación de respuestas con RAG.

Módulo atómico que genera respuestas precisas usando
contexto recuperado y LLM local (smollm3/DeepSeek).

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import ollama
from typing import List, Dict, Any, Optional, Tuple

from .compression import compress_context


def generate_answer(
    query: str,
    context: str,
    model: str = "alibayram/smollm3:latest",
    temperature: float = 0.1,
    max_tokens: int = 1000
) -> str:
    """Generar respuesta basada en contexto recuperado.

    Args:
        query: Pregunta del usuario.
        context: Contexto comprimido de documentos relevantes.
        model: Modelo LLM a usar.
        temperature: Creatividad (0.1 = preciso, 0.7 = creativo).
        max_tokens: Máximo de tokens en respuesta.

    Returns:
        Respuesta generada por el LLM.

    Nota: Instrucción estricta: responder SOLO con información del contexto.
    """
    prompt = _build_rag_prompt(query, context)

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente preciso que responde ÚNICAMENTE con información verificada del contexto proporcionado. Si la información no está en el contexto, indica 'No encontrado en el contexto'."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )

        return response['message']['content']

    except Exception as e:
        # Fallback a DeepSeek (si está disponible)
        try:
            from modules.ia.providers import DeepSeekProvider
            provider = DeepSeekProvider({})
            return provider.generate(prompt)
        except:
            return f"Error generando respuesta: {str(e)}"


def generate_citations(
    answer: str,
    sources: List[Dict[str, Any]]
) -> str:
    """Añadir citas de fuentes a la respuesta.

    Args:
        answer: Respuesta generada.
        sources: Lista de chunks fuente con metadata.

    Returns:
        Respuesta con citas al final.
    """
    if not sources:
        return answer

    # Construir sección de fuentes
    citations = ["\n\n📚 **Fuentes**:\n"]

    for i, source in enumerate(sources[:5], start=1):  # Máximo 5 fuentes
        title = source.get("title", "Desconocido")
        chunk_idx = source.get("chunk_index", 0)
        score = source.get("score", 0)

        citations.append(f"[{i}] {title} (chunk {chunk_idx}, similitud: {score:.2f})")

    return answer + "\n".join(citations)


def detect_hallucination(
    answer: str,
    context: str
) -> Tuple[float, List[str]]:
    """Detectar posibles alucinaciones en la respuesta.

    Args:
        answer: Respuesta generada.
        context: Contexto original usado.

    Returns:
        Tupla (score_confianza, afirmaciones_no_fundadas):
        - score_confianza: 0-1 (1 = totalmente fundamentado)
        - afirmaciones_no_fundadas: Lista de frases sospechosas

    Nota: Verifica que cada afirmación clave esté en el contexto.
    """
    # Extraer afirmaciones clave de la respuesta (oraciones declarativas)
    claims = _extract_claims(answer)

    unsupported = []
    supported_count = 0

    for claim in claims:
        if _claim_in_context(claim, context):
            supported_count += 1
        else:
            unsupported.append(claim)

    total = len(claims)
    score = supported_count / total if total > 0 else 0.0

    return score, unsupported


def _build_rag_prompt(query: str, context: str) -> str:
    """Construir prompt para RAG.

    Args:
        query: Pregunta del usuario.
        context: Contexto de documentos.

    Returns:
        Prompt formateado para LLM.
    """
    return f"""Contexto:
{context}

---

Pregunta: {query}

Instrucciones:
1. Responde ÚNICAMENTE con información del contexto anterior
2. Si la respuesta no está en el contexto, di "No encontrado en el contexto"
3. Sé preciso y conciso
4. No inventes información

Respuesta:"""


def _extract_claims(answer: str) -> List[str]:
    """Extraer afirmaciones clave de una respuesta.

    Args:
        answer: Respuesta generada.

    Returns:
        Lista de oraciones declarativas.
    """
    import re

    # Dividir en oraciones
    sentences = re.split(r'(?<=[.!?])\s+', answer)

    # Filtrar oraciones declarativas (no preguntas, no exclamaciones)
    claims = []
    for sent in sentences:
        sent = sent.strip()
        if sent and not sent.startswith(("¿", "!", "Qué", "Cómo", "Cuándo")):
            if len(sent.split()) >= 5:  # Oraciones sustanciales
                claims.append(sent)

    return claims


def _claim_in_context(claim: str, context: str) -> bool:
    """Verificar si una afirmación está en el contexto.

    Args:
        claim: Afirmación a verificar.
        context: Contexto original.

    Returns:
        True si la afirmación está fundamentada en el contexto.
    """
    # Búsqueda fuzzy simple (palabras clave)
    claim_words = set(claim.lower().split())

    # Verificar si 70% de las palabras están en el contexto
    context_lower = context.lower()
    matches = sum(1 for word in claim_words if word in context_lower)

    return matches / len(claim_words) >= 0.7 if claim_words else False

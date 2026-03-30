"""Módulo RAG Embebido para ARES - Sistema V3.

Módulo atómico que implementa recuperación aumentada por grados (T0-T4).
Filosofía atómica: máximo 3 funciones públicas principales.

Exporta:
    RAGOrchestrator: Punto único de entrada para el sistema RAG.
    Tier: Enumeración de niveles de recuperación (T0_CACHE a T4_REASONING).
    RetrievalResult: Contenedor de resultados con metadatos.
"""

from .core.rag_orchestrator import RAGOrchestrator
from .core.tier_router import Tier, RetrievalResult

__all__ = ["RAGOrchestrator", "Tier", "RetrievalResult"]

__version__ = "0.1.0"
"""Componentes core del módulo RAG.

Exporta:
    RAGOrchestrator: Orquestador principal.
    TieredRAGRouter: Router de tiers T0-T4.
    Tier, RetrievalResult: Tipos de datos fundamentales.
"""

from .rag_orchestrator import RAGOrchestrator
from .tier_router import TieredRAGRouter, Tier, RetrievalResult

__all__ = ["RAGOrchestrator", "TieredRAGRouter", "Tier", "RetrievalResult"]
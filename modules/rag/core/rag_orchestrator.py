#!/usr/bin/env python3
"""
RAGOrchestrator: Punto único de entrada para el sistema RAG.
Integra con ARES existente sin modificar su arquitectura core.
"""

import os
import json
from typing import Optional, Dict, Any, Literal
from dataclasses import asdict

from .tier_router import TieredRAGRouter, Tier, RetrievalResult
from ..validators.relation_guard import RelationGuard


class RAGOrchestrator:
    """
    Orquestador del módulo RAG. Expone interfaz simple para ARES.

    Uso en ARES:
        from modules.rag import RAGOrchestrator
        rag = RAGOrchestrator()
        result = rag.retrieve("consulta", mode="headless")  # ares p
        result = rag.retrieve("consulta", mode="interactive") # ares i
    """

    def __init__(self, config_path: Optional[str] = None):
        self.project_root = os.environ.get('TR_PROJECT_ROOT',
                                          os.path.expanduser('~/tron/programas/TR'))
        self.config_path = config_path or f"{self.project_root}/config/rag.yaml"
        self.db_root = f"{self.project_root}/db/rag"

        # Asegurar estructura
        os.makedirs(self.db_root, exist_ok=True)

        # Componentes
        self.router = TieredRAGRouter(self.config_path)
        self.guard = RelationGuard(f"{self.db_root}/rag_core.sqlite")
        self.session_pid = os.getpid()

        # Snapshot de contexto (inmutabilidad por sesión)
        self._session_snapshot = self._load_session_context()

    def _load_session_context(self) -> Dict[str, Any]:
        """Carga o crea snapshot inmutable para esta sesión."""
        snapshot = {
            'pid': self.session_pid,
            'project': os.environ.get('ARES_CURRENT_PROJECT'),
            'cwd': os.getcwd(),
            'map_pointers': self._resolve_map_pointers()
        }
        return snapshot

    def _resolve_map_pointers(self) -> Dict[str, str]:
        """Resuelve $MAP desde SQLite (Agnosticismo Estructural)."""
        # TODO: Consultar tabla pointers en base de datos
        return {
            '$R': self.project_root,
            '$S': f"{self.project_root}/modules",
            '$D': f"{self.project_root}/docs",
            '$M': self.db_root
        }

    def is_deep_thinking_trigger(self, query: str) -> bool:
        """Detecta si el usuario quiere T4."""
        return self.router.is_t4_trigger(query)

    def retrieve(self, query: str,
                 mode: Literal["headless", "interactive"] = "headless",
                 max_tier: Optional[Tier] = None,
                 force_t4: bool = False) -> RetrievalResult:
        """
        Recuperación principal. Modo determina comportamiento de T4.

        Args:
            query: Texto de consulta
            mode: "headless" (ares p, no T4 sin --deep) o "interactive" (ares i)
            max_tier: Forzar tier máximo (override de mode)
            force_t4: Forzar T4 (solo en interactive o con flag)
        """
        # Determinar tier máximo según modo
        if max_tier is None:
            max_tier = Tier.T3_GRAPH if mode == "headless" else Tier.T4_REASONING

        # En headless, nunca forzar T4 a menos que explicito
        if mode == "headless" and force_t4 and max_tier != Tier.T4_REASONING:
            force_t4 = False

        result = self.router.retrieve(
            query=query,
            max_tier=max_tier,
            force_t4=force_t4,
            session_context=self._session_snapshot
        )

        # Post-procesamiento: validar relaciones en resultado
        if result.sources:
            result.sources = self._validate_sources(result.sources)

        # Agregar al cache si es bueno
        if result.confidence > 0.8 and result.tier != Tier.T4_REASONING:
            self.router.add_to_cache(query, result)

        return result

    def _validate_sources(self, sources: list) -> list:
        """Filtra fuentes no validadas según RelationGuard."""
        validated = []
        for src in sources:
            # Si la fuente implica relación C3/C4 no validada, marcar como tentative
            if self._is_critical_unvalidated(src):
                src['confidence_tier'] = 'tentative'
            validated.append(src)
        return validated

    def _is_critical_unvalidated(self, source: dict) -> bool:
        """Check rápido de criticidad."""
        # TODO: Implementar con guard.can_execute()
        return False

    def to_json(self, result: RetrievalResult) -> str:
        """Serialización para ares p --json."""
        return json.dumps({
            'data': result.data,
            'tier': result.tier.name,
            'confidence': result.confidence,
            'latency_ms': result.latency_ms,
            'sources': result.sources,
            'session_pid': self.session_pid
        }, indent=2, default=str)

    # ===== Métodos de gestión del índice =====

    def ingest_document(self, path: str, doc_type: Optional[str] = None) -> Dict:
        """Indexar nuevo documento en el RAG."""
        from ..ingestors import get_ingestor_for
        ingestor = get_ingestor_for(path, doc_type)
        return ingestor.process(path, self.db_root)

    def get_status(self) -> Dict:
        """Estadísticas del índice RAG."""
        # TODO: Implementar consultas a las tres bases
        return {
            'documents_count': 0,
            'entities_count': 0,
            'pending_validations': 0,
            'last_ingestion': None
        }

    def get_cartografo(self):
        """Obtener instancia del skill Cartógrafo."""
        from ..skills.cartografo import create_cartografo_from_config
        # TODO: cargar configuración desde config_path
        config = {}
        return create_cartografo_from_config(config)

    def run_cartografo(self):
        """Ejecutar modo interactivo del Cartógrafo."""
        cartografo = self.get_cartografo()
        if cartografo:
            cartografo.run_interactive()
        else:
            print("❌ No se pudo inicializar el Cartógrafo")
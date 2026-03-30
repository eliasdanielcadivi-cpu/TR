#!/usr/bin/env python3
"""
RelationGuard: Sistema de clasificación y validación de relaciones.
Implementa Zero-Hallucination para el grafo de conocimiento.
"""

import sqlite3
import json
from dataclasses import dataclass
from typing import Literal, Optional, Dict, List
from enum import Enum


class Criticality(Enum):
    """Niveles de criticidad de relaciones C1-C4."""
    C1_DESCRIPTIVE = "C1"      # Metadatos, tags, semántica libre
    C2_OPERATIONAL = "C2"      # Dependencias de ejecución
    C3_DATA_INTEGRITY = "C3"   # Modificación de datos persistentes
    C4_SECURITY = "C4"         # Ejecución privilegiada, permisos


@dataclass
class Relation:
    """Relación entre entidades."""
    subject: str
    verb: str
    obj: str
    confidence: float = 0.9
    source: Literal["llm", "user", "core", "inferred"] = "llm"
    context: Optional[str] = None


class RelationGuard:
    """
    Guardián de relaciones. Determina qué puede usarse para enrutamiento.

    Reglas (Anexo G):
    - C4: NUNCA auto-ejecutar. Requiere validación explícita en DB.
    - C3: Requiere validación explícita.
    - C2: Requiere validación O ser parte de core_schema.
    - C1: Auto-aceptar si confianza > 0.95.
    """

    VERB_TO_CRITICALITY = {
        # C4 - Seguridad
        'EJECUTA_COMO': Criticality.C4_SECURITY,
        'ESCALA_PRIVILEGIOS': Criticality.C4_SECURITY,
        'BORRA': Criticality.C4_SECURITY,
        'MODIFICA_PERMISOS': Criticality.C4_SECURITY,

        # C3 - Integridad
        'ESCRIBE_EN': Criticality.C3_DATA_INTEGRITY,
        'MODIFICA': Criticality.C3_DATA_INTEGRITY,
        'ELIMINA': Criticality.C3_DATA_INTEGRITY,
        'ACTUALIZA_DB': Criticality.C3_DATA_INTEGRITY,

        # C2 - Operacional
        'REQUIERE': Criticality.C2_OPERATIONAL,
        'DEPENDE_DE': Criticality.C2_OPERATIONAL,
        'USA': Criticality.C2_OPERATIONAL,
        'IMPORTA': Criticality.C2_OPERATIONAL,
        'LLAMA_A': Criticality.C2_OPERATIONAL,

        # C1 - Descriptivo (default)
        'TRATA_SOBRE': Criticality.C1_DESCRIPTIVE,
        'SIMILAR_A': Criticality.C1_DESCRIPTIVE,
        'CATEGORIZADO_COMO': Criticality.C1_DESCRIPTIVE,
        'TAG': Criticality.C1_DESCRIPTIVE,
        'DESCRIBE': Criticality.C1_DESCRIPTIVE,
    }

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self):
        """Asegura que tabla de validación existe."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS relation_validation_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    verb TEXT NOT NULL,
                    object TEXT NOT NULL,
                    criticality TEXT NOT NULL,
                    confidence REAL,
                    proposed_by TEXT,
                    status TEXT DEFAULT 'pending',
                    proposed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    validated_by TEXT,
                    context TEXT,
                    UNIQUE(subject, verb, object)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rel_status
                ON relation_validation_queue(status, criticality)
            """)

    def classify(self, relation: Relation) -> Criticality:
        """Clasifica relación por su verbo."""
        verb_upper = relation.verb.upper()
        return self.VERB_TO_CRITICALITY.get(verb_upper, Criticality.C1_DESCRIPTIVE)

    def can_execute(self, relation: Relation) -> bool:
        """
        Determina si la relación puede usarse para enrutamiento/ejecución.
        Core del Zero-Hallucination.
        """
        crit = self.classify(relation)

        # C4 y C3: Nunca sin validación explícita
        if crit in (Criticality.C4_SECURITY, Criticality.C3_DATA_INTEGRITY):
            return self._is_validated(relation)

        # C2: Validado O es parte del core (hardcoded)
        if crit == Criticality.C2_OPERATIONAL:
            return self._is_validated(relation) or relation.source == "core"

        # C1: Auto-aceptar si muy confiable
        if crit == Criticality.C1_DESCRIPTIVE:
            return relation.confidence > 0.95 or self._is_validated(relation)

        return False

    def _is_validated(self, relation: Relation) -> bool:
        """Check en DB de status 'approved'."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT 1 FROM relation_validation_queue
                WHERE subject = ? AND verb = ? AND object = ? AND status = 'approved'
            """, (relation.subject, relation.verb, relation.obj))
            return c.fetchone() is not None

    def propose(self, relation: Relation, proposed_by: str = "rag_module") -> Dict:
        """
        Ingresa relación a cola de validación. Retorna status.
        """
        crit = self.classify(relation)

        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("""
                    INSERT INTO relation_validation_queue
                    (subject, verb, object, criticality, confidence, proposed_by, context, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now', '+7 days'))
                """, (relation.subject, relation.verb, relation.obj,
                      crit.value, relation.confidence, proposed_by,
                      relation.context))
                conn.commit()

                if crit == Criticality.C4_SECURITY:
                    return {
                        'status': 'QUEUED_CRITICAL',
                        'message': f'⚠️ Relación C4 ({relation.verb}) requiere validación inmediata',
                        'relation': f'{relation.subject} →[{relation.verb}]→ {relation.obj}'
                    }
                return {'status': 'QUEUED', 'criticality': crit.value}

            except sqlite3.IntegrityError:
                return {'status': 'EXISTS', 'message': 'Relación ya en cola'}

    def get_pending(self, criticality: Optional[Criticality] = None) -> List[Dict]:
        """Obtener relaciones pendientes de validación."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            if criticality:
                c.execute("""
                    SELECT * FROM relation_validation_queue
                    WHERE status = 'pending' AND criticality = ?
                    ORDER BY proposed_at
                """, (criticality.value,))
            else:
                c.execute("""
                    SELECT * FROM relation_validation_queue
                    WHERE status = 'pending'
                    ORDER BY criticality DESC, proposed_at
                """)

            return [dict(row) for row in c.fetchall()]

    def validate(self, subject: str, verb: str, obj: str,
                 validator: str, decision: Literal['approved', 'rejected']) -> bool:
        """Validar o rechazar relación pendiente."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE relation_validation_queue
                SET status = ?, validated_by = ?, validated_at = CURRENT_TIMESTAMP
                WHERE subject = ? AND verb = ? AND object = ? AND status = 'pending'
            """, (decision, validator, subject, verb, obj))
            conn.commit()
            return c.rowcount > 0
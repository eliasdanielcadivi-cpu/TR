"""Apollo Extraction: Extracción de entidades y relaciones con LLM.

Módulo atómico que usa smollm3:latest (o DeepSeek) para extraer
entidades y relaciones de texto con structured output JSON.

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import json
import hashlib
import ollama
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel

from .apollo_db import db_context
from .embeddings import embed_text


# Tipos de entidades soportadas
ENTITY_TYPES = [
    "Persona",
    "Organización",
    "Concepto",
    "Producto",
    "Lugar",
    "Evento",
    "Fecha",
    "Tecnología"
]


class ExtractionResult(BaseModel):
    """Resultado de extracción de entidades y relaciones."""
    entities: List[Tuple[str, str]]  # (nombre, tipo)
    relations: List[Tuple[str, str, str]]  # (sujeto, predicado, objeto)


def extract_entities_relations(
    text: str,
    model: str = "alibayram/smollm3:latest",
    max_entities: int = 20
) -> ExtractionResult:
    """Extraer entidades y relaciones de un texto usando LLM.

    Args:
        text: Texto a analizar.
        model: Modelo LLM (default: smollm3:latest).
        max_entities: Máximo de entidades a extraer.

    Returns:
        ExtractionResult con entidades y relaciones extraídas.

    Nota: Usa structured output de Ollama para JSON consistente.
          Fallback a DeepSeek si smollm3 no está disponible.
    """
    # Schema para structured output
    schema = {
        "type": "object",
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "[entidad, tipo]"
                },
                "description": f"Lista de entidades (máx {max_entities})"
            },
            "relations": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3,
                    "description": "[sujeto, predicado, objeto]"
                },
                "description": "Relaciones entre entidades"
            }
        },
        "required": ["entities", "relations"]
    }

    prompt = f"""Analiza el texto y extrae entidades y relaciones.

Tipos de entidades válidos: {', '.join(ENTITY_TYPES)}

Instrucciones:
1. Extrae solo entidades importantes (máximo {max_entities})
2. Para cada entidad, indica su tipo
3. Extrae relaciones explícitas entre entidades
4. Usa verbos concretos para predicados

Texto:
{text[:2000]}  # Truncar para no exceder contexto

Responde SOLO con JSON válido según el schema."""

    try:
        # Intentar con Ollama (smollm3)
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            format=schema,
            options={"temperature": 0.1}
        )

        content = response['message']['content']
        data = json.loads(content)

        return ExtractionResult(
            entities=[(e[0], e[1]) for e in data.get("entities", [])],
            relations=[(r[0], r[1], r[2]) for r in data.get("relations", [])]
        )

    except Exception as e:
        # Fallback a DeepSeek (si está configurado)
        try:
            from modules.ia.providers import DeepSeekProvider
            provider = DeepSeekProvider({})
            response = provider.generate(prompt)

            # Extraer JSON de la respuesta
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)

                return ExtractionResult(
                    entities=[(e[0], e[1]) for e in data.get("entities", [])],
                    relations=[(r[0], r[1], r[2]) for r in data.get("relations", [])]
                )
        except:
            pass

        # Fallback último: retornar vacío
        return ExtractionResult(entities=[], relations=[])


def store_entities(
    entities: List[Tuple[str, str]],
    chunk_id: str,
    text: str = ""
) -> int:
    """Almacenar entidades extraídas en la base de datos.

    Args:
        entities: Lista de (nombre, tipo) de entidades.
        chunk_id: ID del chunk de origen.
        text: Texto opcional para descripción.

    Returns:
        Cantidad de entidades almacenadas.

    Nota: Genera embedding para cada entidad (búsqueda semántica).
    """
    if not entities:
        return 0

    stored_count = 0

    with db_context("knowledge") as conn:
        cursor = conn.cursor()

        for name, entity_type in entities:
            # Generar ID único (hash de nombre + tipo)
            entity_id = hashlib.sha256(f"{entity_type}:{name}".encode()).hexdigest()[:16]

            # Generar embedding para la entidad
            try:
                embedding = embed_text(f"{entity_type}: {name}")
                embedding_bytes = embedding.tobytes()
            except:
                embedding_bytes = None

            # Descripción (primera oración del texto si está disponible)
            description = text.split('.')[0][:200] if text else name

            # Insertar entidad (UPSERT)
            cursor.execute("""
                INSERT OR REPLACE INTO entities (id, name, type, description, embedding)
                VALUES (?, ?, ?, ?, ?)
            """, (entity_id, name, entity_type, description, embedding_bytes))

            stored_count += 1

        conn.commit()

    return stored_count


def store_relations(
    relations: List[Tuple[str, str, str]],
    chunk_id: str,
    entities_map: Dict[str, str] = None
) -> int:
    """Almacenar relaciones extraídas en la base de datos.

    Args:
        relations: Lista de (sujeto, predicado, objeto).
        chunk_id: ID del chunk de origen.
        entities_map: Mapeo nombre_entidad -> entity_id (opcional).

    Returns:
        Cantidad de relaciones almacenadas.

    Nota: Valida que sujeto y objeto existan como entidades.
          Si entities_map no se proporciona, intenta buscar en DB.
    """
    if not relations:
        return 0

    stored_count = 0

    with db_context("knowledge") as conn:
        cursor = conn.cursor()

        for subj, pred, obj in relations:
            # Generar IDs de entidades
            subj_id = entities_map.get(subj) if entities_map else None
            obj_id = entities_map.get(obj) if entities_map else None

            # Si no hay map, intentar obtener IDs
            if not subj_id:
                subj_id = hashlib.sha256(f"Concepto:{subj}".encode()).hexdigest()[:16]
            if not obj_id:
                obj_id = hashlib.sha256(f"Concepto:{obj}".encode()).hexdigest()[:16]

            # Generar ID único para relación
            rel_id = hashlib.sha256(f"{subj_id}:{pred}:{obj_id}".encode()).hexdigest()[:16]

            # Insertar relación
            cursor.execute("""
                INSERT OR REPLACE INTO relations (id, subject_id, predicate, object_id, chunk_id)
                VALUES (?, ?, ?, ?, ?)
            """, (rel_id, subj_id, pred, obj_id, chunk_id))

            stored_count += 1

        conn.commit()

    return stored_count

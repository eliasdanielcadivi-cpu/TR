#!/usr/bin/env python3
"""CLI de ingesta Apollo para ARES.

Script CLI para ingerir documentos al sistema RAG:
- Archivos individuales
- Directorios completos
- Con extracción de entidades y relaciones

Uso:
    python -m modules.ia.apollo.cli_ingest <ruta>
    python -m modules.ia.apollo.cli_ingest <ruta> --extract
    python -m modules.ia.apollo.cli_ingest <ruta> --json
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Añadir root del proyecto al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from modules.ia.apollo import (
    ingest_file,
    ingest_directory,
    extract_entities_relations,
    store_entities,
    store_relations,
)


def main():
    parser = argparse.ArgumentParser(
        description="Ingerir documentos al sistema RAG Apollo"
    )
    parser.add_argument(
        "ruta",
        help="Ruta del archivo o directorio a ingerir"
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Extraer entidades y relaciones con LLM"
    )
    parser.add_argument(
        "--model",
        default="alibayram/smollm3:latest",
        help="Modelo LLM para extracción (default: smollm3:latest)"
    )
    parser.add_argument(
        "--user",
        default="daniel",
        help="Usuario propietario (default: daniel)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=256,  # Conservador para mxbai-embed-large (límite ~2048 tokens)
        help="Tamaño máximo de chunks en tokens (default: 256)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output en formato JSON"
    )

    args = parser.parse_args()

    ruta = Path(args.ruta)

    if not ruta.exists():
        if args.json:
            print(json.dumps({"error": f"Ruta no encontrada: {args.ruta}"}))
        else:
            print(f"❌ Ruta no encontrada: {args.ruta}")
        sys.exit(1)

    results = {
        "accion": "ingesta_apollo",
        "timestamp": datetime.now().isoformat(),
        "ruta": str(ruta.absolute()),
        "usuario": args.user,
        "extract_entidades": args.extract,
        "resultados": []
    }

    # Ingestar archivo o directorio
    if ruta.is_file():
        result = ingest_file(
            str(ruta),
            user_id=args.user,
            max_tokens=args.chunk_size
        )

        # Extraer entidades si se solicitó
        if args.extract and "error" not in result:
            # Leer contenido para extracción
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    text = f.read()

                extraction = extract_entities_relations(text, model=args.model)

                # Almacenar entidades
                entities_stored = store_entities(
                    extraction.entities,
                    chunk_id=f"{result['file_id']}_0",
                    text=text[:500]
                )

                # Almacenar relaciones
                relations_stored = store_relations(
                    extraction.relations,
                    chunk_id=f"{result['file_id']}_0"
                )

                result["entities_extracted"] = len(extraction.entities)
                result["entities_stored"] = entities_stored
                result["relations_extracted"] = len(extraction.relations)
                result["relations_stored"] = relations_stored

            except Exception as e:
                result["extraction_error"] = str(e)

        results["resultados"].append(result)

    elif ruta.is_dir():
        result = ingest_directory(
            str(ruta),
            user_id=args.user,
            max_tokens=args.chunk_size
        )
        results["resultados"].append(result)

    else:
        if args.json:
            print(json.dumps({"error": "Ruta no es archivo ni directorio"}))
        else:
            print(f"❌ Ruta no es archivo ni directorio: {args.ruta}")
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\n📚 INGESTA APOLLO — {args.ruta}")
        print("=" * 50)

        for result in results["resultados"]:
            if "error" in result:
                print(f"❌ Error: {result['error']}")
                continue

            if "file_id" in result:
                # Archivo individual
                print(f"✅ Archivo: {result.get('file_path', args.ruta)}")
                print(f"   ID: {result['file_id']}")
                print(f"   Chunks: {result['chunks_count']}")
                print(f"   Tokens: {result['tokens_total']:,}")
                print(f"   Embeddings: {result['embeddings_dim']} dims")

                if args.extract:
                    if "entities_extracted" in result:
                        print(f"   Entidades: {result['entities_extracted']} extraídas, {result['entities_stored']} guardadas")
                        print(f"   Relaciones: {result['relations_extracted']} extraídas, {result['relations_stored']} guardadas")

            else:
                # Directorio
                print(f"✅ Directorio: {args.ruta}")
                print(f"   Archivos: {result['files_ingested']}")
                print(f"   Chunks totales: {result['total_chunks']}")
                print(f"   Tokens totales: {result['total_tokens']:,}")

                if result.get("errors"):
                    print(f"   Errores: {len(result['errors'])}")
                    for err in result["errors"][:3]:
                        print(f"     - {err['file']}: {err['error']}")

        print("\n" + "=" * 50)
        print("✅ Ingesta completada")
        print("\nPróximos pasos:")
        print("  • Usar 'ares apollo query <pregunta>' para consultar")
        print("  • Usar 'ares apollo ingest --extract' para extracción de entidades")


if __name__ == "__main__":
    main()

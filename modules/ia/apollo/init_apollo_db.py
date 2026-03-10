#!/usr/bin/env python3
"""Inicializar base de datos Apollo (RAG + CRM).

Script CLI para crear y inicializar las bases de datos de Apollo:
- knowledge.db: RAG con documentos, chunks, embeddings, entidades, relaciones
- users.db: CRM con usuarios, clientes, interacciones

Uso:
    python -m modules.ia.apollo.init_apollo_db
    python -m modules.ia.apollo.init_apollo_db --knowledge
    python -m modules.ia.apollo.init_apollo_db --users
"""

import argparse
import sys
from pathlib import Path

# Añadir root del proyecto al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from modules.ia.apollo.apollo_db import init_db, KNOWLEDGE_DB, USERS_DB, APOLLO_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Inicializar bases de datos Apollo (RAG + CRM)"
    )
    parser.add_argument(
        "--knowledge",
        action="store_true",
        help="Inicializar solo knowledge.db (RAG)"
    )
    parser.add_argument(
        "--users",
        action="store_true",
        help="Inicializar solo users.db (CRM)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output en formato JSON"
    )

    args = parser.parse_args()

    # Determinar qué inicializar
    init_knowledge = args.knowledge or (not args.users)
    init_users = args.users or (not args.knowledge)

    results = {
        "knowledge": None,
        "users": None
    }

    # Inicializar knowledge.db
    if init_knowledge:
        success = init_db("knowledge")
        results["knowledge"] = "ok" if success else "error"
        if args.json:
            pass  # Esperar a imprimir JSON completo
        else:
            if success:
                print(f"✅ knowledge.db inicializado en {KNOWLEDGE_DB}")
            else:
                print(f"❌ Error inicializando knowledge.db")

    # Inicializar users.db
    if init_users:
        success = init_db("users")
        results["users"] = "ok" if success else "error"
        if args.json:
            pass  # Esperar a imprimir JSON completo
        else:
            if success:
                print(f"✅ users.db inicializado en {USERS_DB}")
            else:
                print(f"❌ Error inicializando users.db")

    # Output JSON si se solicitó
    if args.json:
        import json
        output = {
            "estado": "ok" if all(v == "ok" for v in results.values()) else "error",
            "accion": "inicializar_apollo_db",
            "datos": {
                "directorio": str(APOLLO_DIR),
                "knowledge_db": str(KNOWLEDGE_DB),
                "users_db": str(USERS_DB),
                "resultados": results
            }
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))

    # Resumen final
    if not args.json:
        if all(v == "ok" for v in results.values()):
            print("\n🎉 Apollo DB inicializada correctamente")
            print(f"📂 Directorio: {APOLLO_DIR}")
            print("\nPróximos pasos:")
            print("  1. Usar 'ares apollo ingest <archivo>' para cargar documentos")
            print("  2. Usar 'ares apollo query <pregunta>' para consultar")
            print("  3. Usar 'ares apollo crm add <cliente>' para gestionar clientes")
        else:
            print("\n⚠️  Algunos errores ocurrieron. Revisa los mensajes arriba.")
            sys.exit(1)


if __name__ == "__main__":
    main()

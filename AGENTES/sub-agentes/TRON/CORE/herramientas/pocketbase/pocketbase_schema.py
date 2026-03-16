#!/usr/bin/env python3
"""
Herramienta de gestión de esquemas para PocketBase

Esta herramienta maneja operaciones específicas de esquema (collections) de PocketBase:
- Crear/eliminar colecciones
- Agregar/eliminar campos
- Modificar configuraciones de colección
- Exportar/importar esquemas

Uso:
    python3 pocketbase_schema.py --help
    python3 pocketbase_schema.py create_collection '{"name": "users", "type": "base", "schema": [...]}'
    python3 pocketbase_schema.py list_fields users
"""

import sys
import json
import os
import logging
import argparse
from typing import Dict, Any, List
from datetime import datetime

# Configuración compartida
from pocketbase_crud import PocketBaseConfig, PocketBaseClient, setup_logging

class PocketBaseSchemaManager:
    """Gestor de esquemas de PocketBase."""

    def __init__(self, verbose: bool = False):
        self.logger = setup_logging(verbose)
        self.config = PocketBaseConfig()
        self.client = PocketBaseClient(self.config, self.logger)

    def list_collections(self, include_system: bool = False) -> List[Dict]:
        """Lista todas las colecciones."""
        collections = self.client.list_collections_with_schema()
        if not include_system:
            collections = [c for c in collections if not c.get("system", False)]
        return collections

    def get_collection(self, name: str) -> Dict:
        """Obtiene detalles de una colección específica."""
        collections = self.list_collections(include_system=True)
        for collection in collections:
            if collection.get("name") == name:
                return collection
        raise ValueError(f"Colección '{name}' no encontrada")

    def create_collection(self, collection_data: Dict) -> Dict:
        """Crea una nueva colección."""
        # Validar datos mínimos
        required_fields = ["name", "type", "schema"]
        for field in required_fields:
            if field not in collection_data:
                raise ValueError(f"Falta campo requerido: {field}")

        url = f"{self.config.BASE_URL}/api/collections"
        headers = self.client._get_headers()

        self.logger.info(f"Creando colección: {collection_data['name']}")
        response = self.client._make_request("POST", url, json=collection_data)
        return response.json()

    def update_collection(self, name: str, updates: Dict) -> Dict:
        """Actualiza una colección existente."""
        # Obtener colección actual
        collection = self.get_collection(name)
        collection_id = collection.get("id")

        if not collection_id:
            raise ValueError(f"No se encontró ID para colección '{name}'")

        url = f"{self.config.BASE_URL}/api/collections/{collection_id}"
        headers = self.client._get_headers()

        # Combinar con actualizaciones
        updated_data = {**collection, **updates}

        self.logger.info(f"Actualizando colección: {name}")
        response = self.client._make_request("PATCH", url, json=updated_data)
        return response.json()

    def delete_collection(self, name: str) -> bool:
        """Elimina una colección."""
        collection = self.get_collection(name)
        collection_id = collection.get("id")

        if not collection_id:
            raise ValueError(f"No se encontró ID para colección '{name}'")

        url = f"{self.config.BASE_URL}/api/collections/{collection_id}"
        headers = self.client._get_headers()

        self.logger.info(f"Eliminando colección: {name}")
        response = self.client._make_request("DELETE", url)
        return response.status_code == 204

    def add_field(self, collection_name: str, field_data: Dict) -> Dict:
        """Agrega un campo a una colección."""
        # Validar campo
        required_fields = ["name", "type"]
        for field in required_fields:
            if field not in field_data:
                raise ValueError(f"Falta campo requerido en definición: {field}")

        # Obtener colección y esquema actual
        collection = self.get_collection(collection_name)
        current_schema = collection.get("schema", [])

        # Verificar que el campo no exista
        for field in current_schema:
            if field.get("name") == field_data["name"]:
                raise ValueError(f"El campo '{field_data['name']}' ya existe")

        # Agregar campo al esquema
        updated_schema = current_schema + [field_data]

        # Actualizar colección
        return self.update_collection(collection_name, {"schema": updated_schema})

    def update_field(self, collection_name: str, field_name: str, updates: Dict) -> Dict:
        """Actualiza un campo existente."""
        collection = self.get_collection(collection_name)
        current_schema = collection.get("schema", [])

        # Encontrar y actualizar campo
        updated_schema = []
        field_found = False

        for field in current_schema:
            if field.get("name") == field_name:
                # Combinar actualizaciones
                updated_field = {**field, **updates}
                updated_schema.append(updated_field)
                field_found = True
                self.logger.debug(f"Campo '{field_name}' actualizado: {updates}")
            else:
                updated_schema.append(field)

        if not field_found:
            raise ValueError(f"Campo '{field_name}' no encontrado en colección '{collection_name}'")

        # Actualizar colección
        return self.update_collection(collection_name, {"schema": updated_schema})

    def delete_field(self, collection_name: str, field_name: str) -> Dict:
        """Elimina un campo de una colección."""
        collection = self.get_collection(collection_name)
        current_schema = collection.get("schema", [])

        # Filtrar campo a eliminar
        updated_schema = [f for f in current_schema if f.get("name") != field_name]

        if len(updated_schema) == len(current_schema):
            raise ValueError(f"Campo '{field_name}' no encontrado en colección '{collection_name}'")

        self.logger.info(f"Eliminando campo '{field_name}' de colección '{collection_name}'")

        # Actualizar colección
        return self.update_collection(collection_name, {"schema": updated_schema})

    def export_schema(self, output_file: str = None) -> Dict:
        """Exporta el esquema completo de la base de datos."""
        collections = self.list_collections()
        schema_data = {
            "export_date": datetime.now().isoformat(),
            "collections_count": len(collections),
            "collections": collections
        }

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(schema_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Esquema exportado a: {output_file}")

        return schema_data

    def import_schema(self, schema_file: str, mode: str = "validate") -> Dict:
        """Importa un esquema desde archivo JSON."""
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)

        results = {
            "validated": False,
            "created": [],
            "updated": [],
            "errors": []
        }

        if mode == "validate":
            # Solo validar
            for collection in schema_data.get("collections", []):
                try:
                    # Validar estructura básica
                    required = ["name", "type", "schema"]
                    for field in required:
                        if field not in collection:
                            raise ValueError(f"Falta campo requerido: {field}")
                    results["validated"] = True
                except Exception as e:
                    results["errors"].append(f"Error validando {collection.get('name', 'unknown')}: {e}")

        elif mode == "apply":
            # Aplicar cambios
            for collection in schema_data.get("collections", []):
                name = collection.get("name")
                try:
                    # Verificar si existe
                    try:
                        existing = self.get_collection(name)
                        # Actualizar existente
                        updated = self.update_collection(name, collection)
                        results["updated"].append(name)
                        self.logger.info(f"Colección '{name}' actualizada")
                    except ValueError:
                        # Crear nueva
                        created = self.create_collection(collection)
                        results["created"].append(name)
                        self.logger.info(f"Colección '{name}' creada")
                except Exception as e:
                    results["errors"].append(f"Error procesando {name}: {e}")

        return results

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gestor de esquemas de PocketBase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s list_collections
  %(prog)s get_collection users
  %(prog)s create_collection '{"name": "products", "type": "base", "schema": [...]}'
  %(prog)s add_field users '{"name": "email", "type": "email", "required": true}'
  %(prog)s export --output schema.json
  %(prog)s import schema.json --mode apply
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Listar colecciones
    list_parser = subparsers.add_parser("list_collections", help="Listar todas las colecciones")
    list_parser.add_argument("--include-system", action="store_true", help="Incluir colecciones del sistema")

    # Obtener colección
    get_parser = subparsers.add_parser("get_collection", help="Obtener detalles de una colección")
    get_parser.add_argument("name", help="Nombre de la colección")

    # Crear colección
    create_parser = subparsers.add_parser("create_collection", help="Crear nueva colección")
    create_parser.add_argument("data", help="Datos de la colección en JSON")

    # Actualizar colección
    update_parser = subparsers.add_parser("update_collection", help="Actualizar colección existente")
    update_parser.add_argument("name", help="Nombre de la colección")
    update_parser.add_argument("updates", help="Actualizaciones en JSON")

    # Eliminar colección
    delete_parser = subparsers.add_parser("delete_collection", help="Eliminar colección")
    delete_parser.add_argument("name", help="Nombre de la colección")
    delete_parser.add_argument("--confirm", action="store_true", help="Confirmar eliminación")

    # Agregar campo
    add_field_parser = subparsers.add_parser("add_field", help="Agregar campo a colección")
    add_field_parser.add_argument("collection", help="Nombre de la colección")
    add_field_parser.add_argument("field_data", help="Datos del campo en JSON")

    # Actualizar campo
    update_field_parser = subparsers.add_parser("update_field", help="Actualizar campo existente")
    update_field_parser.add_argument("collection", help="Nombre de la colección")
    update_field_parser.add_argument("field_name", help="Nombre del campo")
    update_field_parser.add_argument("updates", help="Actualizaciones en JSON")

    # Eliminar campo
    delete_field_parser = subparsers.add_parser("delete_field", help="Eliminar campo de colección")
    delete_field_parser.add_argument("collection", help="Nombre de la colección")
    delete_field_parser.add_argument("field_name", help="Nombre del campo")
    delete_field_parser.add_argument("--confirm", action="store_true", help="Confirmar eliminación")

    # Exportar esquema
    export_parser = subparsers.add_parser("export", help="Exportar esquema completo")
    export_parser.add_argument("--output", "-o", help="Archivo de salida")

    # Importar esquema
    import_parser = subparsers.add_parser("import", help="Importar esquema desde archivo")
    import_parser.add_argument("file", help="Archivo JSON con esquema")
    import_parser.add_argument("--mode", choices=["validate", "apply"], default="validate",
                              help="Modo de importación (default: validate)")

    # Argumentos globales
    parser.add_argument("--verbose", "-v", action="store_true", help="Habilitar logging detallado")
    parser.add_argument("--output-format", choices=["json", "pretty", "simple"],
                       default="pretty", help="Formato de salida")

    return parser.parse_args()

def main():
    """Función principal."""
    args = parse_args()

    if not args.command:
        print("Error: Se requiere un comando. Use --help para ver opciones.")
        sys.exit(1)

    # Inicializar gestor
    manager = PocketBaseSchemaManager(verbose=args.verbose)

    try:
        # Ejecutar comando
        if args.command == "list_collections":
            result = manager.list_collections(include_system=args.include_system)

        elif args.command == "get_collection":
            result = manager.get_collection(args.name)

        elif args.command == "create_collection":
            data = json.loads(args.data)
            result = manager.create_collection(data)

        elif args.command == "update_collection":
            updates = json.loads(args.updates)
            result = manager.update_collection(args.name, updates)

        elif args.command == "delete_collection":
            if not args.confirm:
                print(f"⚠️  Para eliminar la colección '{args.name}', agregue --confirm")
                sys.exit(1)
            result = manager.delete_collection(args.name)

        elif args.command == "add_field":
            field_data = json.loads(args.field_data)
            result = manager.add_field(args.collection, field_data)

        elif args.command == "update_field":
            updates = json.loads(args.updates)
            result = manager.update_field(args.collection, args.field_name, updates)

        elif args.command == "delete_field":
            if not args.confirm:
                print(f"⚠️  Para eliminar el campo '{args.field_name}' de '{args.collection}', agregue --confirm")
                sys.exit(1)
            result = manager.delete_field(args.collection, args.field_name)

        elif args.command == "export":
            result = manager.export_schema(args.output)

        elif args.command == "import":
            result = manager.import_schema(args.file, args.mode)

        else:
            print(f"Comando no reconocido: {args.command}")
            sys.exit(1)

        # Mostrar resultado
        if args.output_format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif args.output_format == "pretty":
            if isinstance(result, list):
                print(f"✅ Encontradas {len(result)} colecciones:")
                for item in result:
                    print(f"  - {item.get('name')} ({item.get('type')})")
            elif isinstance(result, dict):
                if "errors" in result and result["errors"]:
                    print("❌ Errores encontrados:")
                    for error in result["errors"]:
                        print(f"  - {error}")
                else:
                    print("✅ Operación exitosa")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"✅ Resultado: {result}")
        else:  # simple
            print(f"Status: success")
            print(f"Result: {result}")

        sys.exit(0)

    except json.JSONDecodeError as e:
        manager.logger.error(f"Error parseando JSON: {e}")
        print(f"Error: JSON inválido - {e}")
        sys.exit(1)
    except Exception as e:
        manager.logger.error(f"Error ejecutando comando: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
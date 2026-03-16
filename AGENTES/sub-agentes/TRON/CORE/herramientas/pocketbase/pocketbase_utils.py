#!/usr/bin/env python3
"""
Utilidades y helpers para PocketBase

Funciones auxiliares para:
- Validación de datos
- Formateo de respuestas
- Manejo de errores
- Utilidades de desarrollo

Uso:
    python3 pocketbase_utils.py --help
    python3 pocketbase_utils.py validate_schema schema.json
    python3 pocketbase_utils.py generate_field_type email --required true
"""

import sys
import json
import os
import logging
import argparse
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

def setup_logging(verbose: bool = False):
    """Configura logging compartido."""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"pocketbase_utils_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stderr)
        ]
    )

    return logging.getLogger(__name__)

class SchemaValidator:
    """Validador de esquemas de PocketBase."""

    @staticmethod
    def validate_collection(collection: Dict) -> List[str]:
        """Valida una definición de colección."""
        errors = []

        # Campos requeridos
        required_fields = ["name", "type", "schema"]
        for field in required_fields:
            if field not in collection:
                errors.append(f"Falta campo requerido: {field}")

        # Validar nombre
        name = collection.get("name", "")
        if not re.match(r'^[a-z][a-z0-9_]*$', name):
            errors.append(f"Nombre inválido '{name}': debe ser lowercase con underscores")

        # Validar tipo
        valid_types = ["base", "auth", "view"]
        coll_type = collection.get("type")
        if coll_type not in valid_types:
            errors.append(f"Tipo inválido '{coll_type}': debe ser uno de {valid_types}")

        # Validar schema si existe
        if "schema" in collection:
            schema_errors = SchemaValidator.validate_schema(collection["schema"])
            errors.extend(schema_errors)

        return errors

    @staticmethod
    def validate_schema(schema: List[Dict]) -> List[str]:
        """Valida un esquema de campos."""
        errors = []
        field_names = set()

        for i, field in enumerate(schema):
            # Campos requeridos
            if "name" not in field:
                errors.append(f"Campo {i}: falta 'name'")
                continue

            if "type" not in field:
                errors.append(f"Campo '{field['name']}': falta 'type'")
                continue

            field_name = field["name"]
            if field_name in field_names:
                errors.append(f"Nombre duplicado: '{field_name}'")
            field_names.add(field_name)

            # Validar nombre del campo
            if not re.match(r'^[a-z][a-z0-9_]*$', field_name):
                errors.append(f"Campo '{field_name}': nombre inválido, debe ser lowercase con underscores")

            # Validar tipo de campo
            valid_types = [
                "text", "number", "bool", "email", "url", "editor", "select",
                "json", "date", "file", "relation", "user"
            ]
            field_type = field["type"]
            if field_type not in valid_types:
                errors.append(f"Campo '{field_name}': tipo inválido '{field_type}'")

            # Validaciones específicas por tipo
            if field_type == "select":
                if "options" not in field or "values" not in field["options"]:
                    errors.append(f"Campo select '{field_name}': falta 'options.values'")
                elif not isinstance(field["options"]["values"], list):
                    errors.append(f"Campo select '{field_name}': 'options.values' debe ser lista")

            elif field_type == "relation":
                if "collectionId" not in field and "collectionName" not in field:
                    errors.append(f"Campo relation '{field_name}': falta 'collectionId' o 'collectionName'")

        return errors

class FieldGenerator:
    """Generador de definiciones de campos."""

    FIELD_TEMPLATES = {
        "text": {
            "type": "text",
            "required": False,
            "options": {"max": 255, "min": 0}
        },
        "number": {
            "type": "number",
            "required": False,
            "options": {"min": None, "max": None}
        },
        "email": {
            "type": "email",
            "required": False,
            "options": {"exceptDomains": None, "onlyDomains": None}
        },
        "url": {
            "type": "url",
            "required": False,
            "options": {"exceptDomains": None, "onlyDomains": None}
        },
        "bool": {
            "type": "bool",
            "required": False
        },
        "date": {
            "type": "date",
            "required": False
        },
        "select": {
            "type": "select",
            "required": False,
            "options": {"values": [], "maxSelect": 1}
        },
        "json": {
            "type": "json",
            "required": False
        },
        "file": {
            "type": "file",
            "required": False,
            "options": {"maxSize": 5242880, "mimeTypes": []}
        },
        "relation": {
            "type": "relation",
            "required": False,
            "options": {"collectionId": "", "cascadeDelete": False}
        }
    }

    @classmethod
    def generate_field(cls, name: str, field_type: str, **kwargs) -> Dict:
        """Genera una definición de campo."""
        if field_type not in cls.FIELD_TEMPLATES:
            raise ValueError(f"Tipo de campo no soportado: {field_type}")

        field = cls.FIELD_TEMPLATES[field_type].copy()
        field["name"] = name

        # Aplicar opciones personalizadas
        if "options" in kwargs:
            if field_type == "select" and "values" in kwargs["options"]:
                field["options"]["values"] = kwargs["options"]["values"]
            if field_type == "relation" and "collectionId" in kwargs["options"]:
                field["options"]["collectionId"] = kwargs["options"]["collectionId"]
            if field_type == "file" and "maxSize" in kwargs["options"]:
                field["options"]["maxSize"] = kwargs["options"]["maxSize"]

        # Propiedades básicas
        if "required" in kwargs:
            field["required"] = kwargs["required"]
        if "unique" in kwargs:
            field["unique"] = kwargs["unique"]
        if "default" in kwargs:
            field["options"]["default"] = kwargs["default"]

        return field

class DataFormatter:
    """Formateador de datos para salida legible."""

    @staticmethod
    def format_collection_list(collections: List[Dict], detailed: bool = False) -> str:
        """Formatea lista de colecciones."""
        if not collections:
            return "No hay colecciones"

        output = f"📁 Colecciones ({len(collections)}):\n"
        for i, coll in enumerate(collections, 1):
            output += f"\n{i}. {coll.get('name')} ({coll.get('type')})"
            if detailed:
                output += f"\n   ID: {coll.get('id')}"
                output += f"\n   Campos: {len(coll.get('schema', []))}"
                if coll.get('system'):
                    output += " 🔧 (sistema)"
        return output

    @staticmethod
    def format_record_list(records: List[Dict], collection: str = None) -> str:
        """Formatea lista de registros."""
        if not records:
            return f"No hay registros{' en ' + collection if collection else ''}"

        output = f"📋 Registros ({len(records)}):\n"
        for i, record in enumerate(records, 1):
            output += f"\n{i}. ID: {record.get('id')}"
            # Mostrar algunos campos relevantes
            fields = [k for k in record.keys() if k not in ['id', 'collectionId', 'collectionName']]
            for field in fields[:3]:  # Mostrar máximo 3 campos
                value = record.get(field)
                if value is not None:
                    output += f"\n   {field}: {str(value)[:50]}"
            if len(fields) > 3:
                output += f"\n   ... y {len(fields) - 3} campos más"
        return output

    @staticmethod
    def format_error(error: Union[str, Exception], context: str = "") -> str:
        """Formatea errores para salida legible."""
        error_msg = str(error) if isinstance(error, Exception) else error

        output = "❌ Error"
        if context:
            output += f" en {context}"
        output += f": {error_msg}"

        # Añadir sugerencias basadas en el error
        if "authentication" in error_msg.lower():
            output += "\n💡 Sugerencia: Verifica credenciales en PocketBaseConfig"
        elif "not found" in error_msg.lower():
            output += "\n💡 Sugerencia: Verifica que la colección/existente"
        elif "json" in error_msg.lower():
            output += "\n💡 Sugerencia: Valida el formato JSON con validate_schema"

        return output

class DevelopmentUtils:
    """Utilidades para desarrollo y debugging."""

    @staticmethod
    def generate_test_data(collection_schema: List[Dict], count: int = 1) -> List[Dict]:
        """Genera datos de prueba basados en un esquema."""
        test_data = []

        for i in range(count):
            record = {"id": f"test_{i+1}"}
            for field in collection_schema:
                field_name = field.get("name")
                field_type = field.get("type")

                if field_type == "text":
                    record[field_name] = f"Texto de prueba {i+1}"
                elif field_type == "number":
                    record[field_name] = i + 1
                elif field_type == "email":
                    record[field_name] = f"test{i+1}@example.com"
                elif field_type == "bool":
                    record[field_name] = i % 2 == 0
                elif field_type == "date":
                    record[field_name] = datetime.now().isoformat()
                elif field_type == "select":
                    options = field.get("options", {}).get("values", [])
                    if options:
                        record[field_name] = options[i % len(options)] if i < len(options) else options[0]
                # Otros tipos pueden dejarse como None

            test_data.append(record)

        return test_data

    @staticmethod
    def mock_response(action: str, data: Dict = None) -> Dict:
        """Genera una respuesta mock para testing."""
        mock_responses = {
            "query_records": {
                "status": "success",
                "operation": "query_records",
                "result": [
                    {"id": "mock_1", "name": "Registro Mock 1"},
                    {"id": "mock_2", "name": "Registro Mock 2"}
                ]
            },
            "list_collections_with_schema": {
                "status": "success",
                "operation": "list_collections_with_schema",
                "result": [
                    {"name": "users", "type": "base", "schema": []},
                    {"name": "products", "type": "base", "schema": []}
                ]
            },
            "create_record": {
                "status": "success",
                "operation": "create_record",
                "result": {"id": "new_mock_id", "created": True}
            }
        }

        response = mock_responses.get(action, {
            "status": "error",
            "operation": action,
            "message": "Acción mock no implementada"
        })

        if data:
            response["input_data"] = data

        return response

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Utilidades y helpers para PocketBase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s validate_schema schema.json
  %(prog)s generate_field email --name user_email --required true
  %(prog)s format_data records.json --type records
  %(prog)s test_mock query_records --data '{"collection": "users"}'
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Validar esquema
    validate_parser = subparsers.add_parser("validate_schema", help="Validar esquema JSON")
    validate_parser.add_argument("file", help="Archivo JSON con esquema")
    validate_parser.add_argument("--type", choices=["collection", "field"], default="collection",
                                 help="Tipo de esquema a validar")

    # Generar campo
    generate_parser = subparsers.add_parser("generate_field", help="Generar definición de campo")
    generate_parser.add_argument("field_type", help="Tipo de campo (text, number, email, etc.)")
    generate_parser.add_argument("--name", required=True, help="Nombre del campo")
    generate_parser.add_argument("--required", action="store_true", help="Campo requerido")
    generate_parser.add_argument("--unique", action="store_true", help="Campo único")
    generate_parser.add_argument("--default", help="Valor por defecto")
    generate_parser.add_argument("--values", help="Valores para campo select (JSON array)")

    # Formatear datos
    format_parser = subparsers.add_parser("format_data", help="Formatear datos para salida")
    format_parser.add_argument("file", help="Archivo JSON con datos")
    format_parser.add_argument("--type", choices=["collections", "records"], required=True,
                               help="Tipo de datos a formatear")

    # Mock testing
    mock_parser = subparsers.add_parser("test_mock", help="Generar respuesta mock")
    mock_parser.add_argument("action", help="Acción a mockear")
    mock_parser.add_argument("--data", help="Datos de entrada en JSON")

    # Argumentos globales
    parser.add_argument("--verbose", "-v", action="store_true", help="Habilitar logging detallado")

    return parser.parse_args()

def main():
    """Función principal."""
    args = parse_args()

    if not args.command:
        print("Error: Se requiere un comando. Use --help para ver opciones.")
        sys.exit(1)

    logger = setup_logging(args.verbose)

    try:
        if args.command == "validate_schema":
            with open(args.file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if args.type == "collection":
                errors = SchemaValidator.validate_collection(data)
            else:  # field
                errors = SchemaValidator.validate_schema(data) if isinstance(data, list) else ["Esquema debe ser lista"]

            if errors:
                print("❌ Errores encontrados:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            else:
                print("✅ Esquema válido")
                sys.exit(0)

        elif args.command == "generate_field":
            kwargs = {"name": args.name}
            if args.required:
                kwargs["required"] = True
            if args.unique:
                kwargs["unique"] = True
            if args.default:
                kwargs["default"] = args.default
            if args.values:
                try:
                    values = json.loads(args.values)
                    if not isinstance(values, list):
                        raise ValueError("--values debe ser una lista JSON")
                    kwargs["options"] = {"values": values}
                except json.JSONDecodeError:
                    print("Error: --values debe ser un array JSON válido")
                    sys.exit(1)

            field = FieldGenerator.generate_field(args.name, args.field_type, **kwargs)
            print(json.dumps(field, indent=2, ensure_ascii=False))

        elif args.command == "format_data":
            with open(args.file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if args.type == "collections":
                formatted = DataFormatter.format_collection_list(data, detailed=True)
            else:  # records
                formatted = DataFormatter.format_record_list(data)

            print(formatted)

        elif args.command == "test_mock":
            input_data = json.loads(args.data) if args.data else {}
            mock = DevelopmentUtils.mock_response(args.action, input_data)
            print(json.dumps(mock, indent=2, ensure_ascii=False))

        else:
            print(f"Comando no reconocido: {args.command}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
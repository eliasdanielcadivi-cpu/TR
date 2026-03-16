#!/usr/bin/env python3
"""
Herramienta CRUD para PocketBase - NO gestionada por despachador.py

Esta herramienta permite operaciones CRUD tanto de schema como de datos en PocketBase.
Acepta comandos JSON como entrada y proporciona salida detallada con logging extensivo.

Uso:
    python3 pocketbase_crud.py '{"action": "query_records", "collection": "users"}'
    cat command.json | python3 pocketbase_crud.py --stdin
    python3 pocketbase_crud.py --help

Funciones soportadas:
    - query_records: Consultar registros con filtros
    - list_collections_with_schema: Listar colecciones con esquema
    - batch_create: Creación masiva de registros
    - update_record: Actualizar registro único
    - batch_update: Actualización masiva
    - delete_record: Eliminar registro único
    - batch_delete: Eliminación masiva
"""

import sys
import json
import os
import logging
import argparse
from typing import Dict, Any, Optional
import requests
from datetime import datetime

# Configuración de logging con verbosidad alta
def setup_logging(verbose: bool = False):
    """Configura logging detallado con diferentes niveles."""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"pocketbase_crud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

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

# Configuración de PocketBase
class PocketBaseConfig:
    """Configuración centralizada para PocketBase."""
    BASE_URL = "http://127.0.0.1:8090"
    ADMIN_EMAIL = "elprofesorverdad@gmail.com"
    ADMIN_PASSWORD = "Copa007copa."

    # Tiempos de espera
    TIMEOUT = 30
    MAX_RETRIES = 3

class PocketBaseClient:
    """Cliente para interactuar con PocketBase API."""

    def __init__(self, config: PocketBaseConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.admin_token = None

    def authenticate(self) -> str:
        """Autentica con PocketBase y devuelve token de admin."""
        if self.admin_token:
            return self.admin_token

        auth_url = f"{self.config.BASE_URL}/api/admins/auth-with-password"
        payload = {
            "identity": self.config.ADMIN_EMAIL,
            "password": self.config.ADMIN_PASSWORD
        }

        try:
            self.logger.debug(f"Autenticando con PocketBase en {auth_url}")
            response = self.session.post(
                auth_url,
                json=payload,
                timeout=self.config.TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            self.admin_token = data.get("token")
            self.logger.info("Autenticación exitosa con PocketBase")
            return self.admin_token
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de autenticación: {e}")
            raise Exception(f"Fallo en la autenticación de admin: {e}")

    def _get_headers(self) -> Dict[str, str]:
        """Obtiene headers con autenticación."""
        token = self.authenticate()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Realiza una petición HTTP con manejo de errores y reintentos."""
        headers = self._get_headers()
        kwargs.setdefault("headers", headers)
        kwargs.setdefault("timeout", self.config.TIMEOUT)

        for attempt in range(self.config.MAX_RETRIES):
            try:
                self.logger.debug(f"Petición {method} a {url} (intento {attempt + 1})")
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Intento {attempt + 1} fallido: {e}")
                if attempt == self.config.MAX_RETRIES - 1:
                    raise
                # Esperar antes de reintentar
                import time
                time.sleep(2 ** attempt)

    def query_records(self, collection: str, params: Optional[Dict] = None) -> list:
        """Consulta registros de una colección."""
        query_parts = []
        if params:
            # Convertir limit a perPage para PocketBase
            if "limit" in params:
                params["perPage"] = params.pop("limit")

            for key, value in params.items():
                if value is not None and value != "":
                    query_parts.append(f"{key}={value}")

        query_string = "?" + "&".join(query_parts) if query_parts else ""
        url = f"{self.config.BASE_URL}/api/collections/{collection}/records{query_string}"

        response = self._make_request("GET", url)
        data = response.json()
        return data.get("items", [])

    def list_collections_with_schema(self) -> list:
        """Lista todas las colecciones con sus esquemas."""
        url = f"{self.config.BASE_URL}/api/collections?perPage=500&schema=1"
        response = self._make_request("GET", url)
        data = response.json()
        # Filtrar colecciones del sistema
        return [c for c in data.get("items", []) if not c.get("system", False)]

    def batch_create(self, collection: str, records: list) -> dict:
        """Crea múltiples registros en una colección."""
        url = f"{self.config.BASE_URL}/api/collections/{collection}/records"
        payload = {"records": records}

        response = self._make_request("POST", url, json=payload)
        return response.json()

    def delete_record(self, collection: str, record_id: str) -> bool:
        """Elimina un registro por ID."""
        url = f"{self.config.BASE_URL}/api/collections/{collection}/records/{record_id}"
        response = self._make_request("DELETE", url)
        return response.status_code == 204

    def batch_delete(self, collection: str, record_ids: list) -> dict:
        """Elimina múltiples registros."""
        results = []
        for record_id in record_ids:
            try:
                success = self.delete_record(collection, record_id)
                results.append({"id": record_id, "success": success})
            except Exception as e:
                results.append({"id": record_id, "success": False, "error": str(e)})

        successful = [r["id"] for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        return {
            "deleted_count": len(successful),
            "successful_ids": successful,
            "failed": failed
        }

    def update_record(self, collection: str, record_id: str, data: dict) -> dict:
        """Actualiza un registro específico."""
        url = f"{self.config.BASE_URL}/api/collections/{collection}/records/{record_id}"
        response = self._make_request("PATCH", url, json=data)
        return response.json()

    def batch_update(self, collection: str, records: list) -> dict:
        """Actualiza múltiples registros."""
        results = []
        for record in records:
            record_id = record.get("id")
            if not record_id:
                results.append({
                    "success": False,
                    "error": "Registro sin ID",
                    "record": record
                })
                continue

            data = {k: v for k, v in record.items() if k != "id"}
            try:
                updated = self.update_record(collection, record_id, data)
                results.append({
                    "success": True,
                    "id": record_id,
                    "record": updated
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "id": record_id,
                    "error": str(e),
                    "record": record
                })

        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        return {
            "successful_records": successful,
            "failed_records": failed
        }

class PocketBaseOrchestrator:
    """Orquestador principal que maneja los comandos JSON."""

    def __init__(self, verbose: bool = False):
        self.logger = setup_logging(verbose)
        self.config = PocketBaseConfig()
        self.client = PocketBaseClient(self.config, self.logger)

    def validate_contract(self, contract: Dict[str, Any]) -> Dict[str, Any]:
        """Valida y normaliza el contrato JSON."""
        self.logger.debug(f"Validando contrato: {json.dumps(contract, indent=2)}")

        # Validaciones básicas
        if "action" not in contract:
            raise ValueError("El contrato debe contener una acción 'action'")

        action = contract["action"]
        actions_without_collection = ["list_collections_with_schema"]

        # Validar colección para acciones que la requieren
        if action not in actions_without_collection:
            if "collection" not in contract:
                raise ValueError(f"La acción '{action}' requiere una colección 'collection'")

        # Validaciones específicas por acción
        if action in ["delete_record", "update_record"]:
            if "id" not in contract:
                raise ValueError(f"La acción '{action}' requiere un ID 'id'")

        if action == "update_record":
            if "data" not in contract:
                raise ValueError("La acción 'update_record' requiere datos 'data'")

        if action == "batch_delete":
            if "record_ids" not in contract:
                raise ValueError("La acción 'batch_delete' requiere 'record_ids'")
            if not isinstance(contract["record_ids"], list):
                raise ValueError("'record_ids' debe ser una lista")

        if action == "batch_update":
            if "records" not in contract:
                raise ValueError("La acción 'batch_update' requiere 'records'")
            if not isinstance(contract["records"], list):
                raise ValueError("'records' debe ser una lista")

        if action == "batch_create":
            if "records" not in contract and "data" not in contract:
                raise ValueError("La acción 'batch_create' requiere 'records' o 'data'")

        self.logger.info(f"Contrato validado para acción: {action}")
        return contract

    def execute(self, contract: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta el comando especificado en el contrato."""
        try:
            validated = self.validate_contract(contract)
            action = validated["action"]

            self.logger.info(f"Ejecutando acción: {action}")

            # Ejecutar la acción correspondiente
            if action == "query_records":
                collection = validated["collection"]
                params = validated.get("params", {})
                result = self.client.query_records(collection, params)
                return {"status": "success", "operation": action, "result": result}

            elif action == "list_collections_with_schema":
                result = self.client.list_collections_with_schema()
                return {"status": "success", "operation": action, "result": result}

            elif action == "batch_create":
                collection = validated["collection"]
                records = validated.get("records", validated.get("data", []))
                if not isinstance(records, list):
                    records = [records]
                result = self.client.batch_create(collection, records)
                return {"status": "success", "operation": action, "result": result}

            elif action == "update_record":
                collection = validated["collection"]
                record_id = validated["id"]
                data = validated["data"]
                result = self.client.update_record(collection, record_id, data)
                return {"status": "success", "operation": action, "result": result}

            elif action == "batch_update":
                collection = validated["collection"]
                records = validated["records"]
                result = self.client.batch_update(collection, records)
                return {"status": "success", "operation": action, "result": result}

            elif action == "delete_record":
                collection = validated["collection"]
                record_id = validated["id"]
                success = self.client.delete_record(collection, record_id)
                result = {"deleted": success, "id": record_id}
                return {"status": "success", "operation": action, "result": result}

            elif action == "batch_delete":
                collection = validated["collection"]
                record_ids = validated["record_ids"]
                result = self.client.batch_delete(collection, record_ids)
                return {"status": "success", "operation": action, "result": result}

            else:
                raise ValueError(f"Acción no soportada: {action}")

        except Exception as e:
            self.logger.error(f"Error ejecutando acción: {e}", exc_info=True)
            return {
                "status": "error",
                "operation": contract.get("action", "unknown"),
                "message": str(e)
            }

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Herramienta CRUD para PocketBase - Operaciones con JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s '{"action": "list_collections_with_schema"}'
  %(prog)s '{"action": "query_records", "collection": "users", "params": {"limit": 10}}'
  echo '{"action": "list_collections_with_schema"}' | %(prog)s --stdin
  %(prog)s --verbose --file command.json
        """
    )

    parser.add_argument(
        "json_command",
        nargs="?",
        help="Comando JSON como string (opcional si se usa --stdin o --file)"
    )

    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Leer JSON desde stdin"
    )

    parser.add_argument(
        "--file",
        help="Leer JSON desde archivo"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Habilitar logging detallado"
    )

    parser.add_argument(
        "--output",
        choices=["json", "pretty", "simple"],
        default="pretty",
        help="Formato de salida (default: pretty)"
    )

    return parser.parse_args()

def main():
    """Función principal."""
    args = parse_args()

    # Inicializar orquestador
    orchestrator = PocketBaseOrchestrator(verbose=args.verbose)

    # Obtener JSON del comando
    json_input = None

    if args.stdin:
        # Leer desde stdin
        json_input = sys.stdin.read()
    elif args.file:
        # Leer desde archivo
        with open(args.file, 'r', encoding='utf-8') as f:
            json_input = f.read()
    elif args.json_command:
        # Usar argumento de línea de comandos
        json_input = args.json_command
    else:
        orchestrator.logger.error("No se proporcionó comando JSON")
        print("Error: Se requiere un comando JSON. Use --help para más información.")
        sys.exit(1)

    try:
        # Parsear JSON
        contract = json.loads(json_input)

        # Ejecutar comando
        result = orchestrator.execute(contract)

        # Mostrar resultado
        if args.output == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif args.output == "pretty":
            if result["status"] == "success":
                print(f"✅ Operación '{result['operation']}' exitosa")
                print(json.dumps(result.get("result", {}), indent=2, ensure_ascii=False))
            else:
                print(f"❌ Error en operación '{result['operation']}': {result.get('message', 'Unknown error')}")
        else:  # simple
            print(f"Status: {result['status']}")
            if result["status"] == "success":
                print(f"Operation: {result['operation']}")
                result_data = result.get("result", {})
                if isinstance(result_data, list):
                    print(f"Records: {len(result_data)}")
                elif isinstance(result_data, dict):
                    print(f"Result keys: {list(result_data.keys())}")
            else:
                print(f"Error: {result.get('message', 'Unknown error')}")

        # Salir con código apropiado
        sys.exit(0 if result["status"] == "success" else 1)

    except json.JSONDecodeError as e:
        orchestrator.logger.error(f"Error parseando JSON: {e}")
        print(f"Error: JSON inválido - {e}")
        sys.exit(1)
    except Exception as e:
        orchestrator.logger.error(f"Error inesperado: {e}", exc_info=True)
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
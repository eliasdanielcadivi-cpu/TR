#!/usr/bin/env python3
"""
Script de prueba para verificar conexión con PocketBase

Este script prueba:
1. Conexión al servidor PocketBase
2. Autenticación con credenciales de admin
3. Listado de colecciones básico

Uso:
    python3 test_connection.py
    python3 test_connection.py --verbose
"""

import sys
import json
import os
import logging
import requests
import time
from datetime import datetime

def setup_logging(verbose: bool = False):
    """Configura logging detallado."""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"test_connection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

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

class ConnectionTester:
    """Prueba de conexión a PocketBase."""

    def __init__(self, verbose: bool = False):
        self.logger = setup_logging(verbose)
        self.base_url = "http://127.0.0.1:8090"
        self.admin_email = "elprofesorverdad@gmail.com"
        self.admin_password = "Copa007copa."
        self.timeout = 10

    def test_server_connection(self) -> bool:
        """Prueba conexión básica al servidor."""
        try:
            self.logger.info(f"Probando conexión a {self.base_url}...")
            response = requests.get(f"{self.base_url}/api/health", timeout=self.timeout)

            if response.status_code == 200:
                self.logger.info(f"✅ Servidor PocketBase accesible (HTTP {response.status_code})")
                return True
            else:
                self.logger.warning(f"⚠️  Servidor respondió con código {response.status_code}")
                return False

        except requests.exceptions.ConnectionError:
            self.logger.error("❌ No se puede conectar al servidor PocketBase")
            self.logger.error("   Verifica que PocketBase esté corriendo en http://127.0.0.1:8090")
            return False
        except requests.exceptions.Timeout:
            self.logger.error("❌ Timeout al conectar con PocketBase")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error inesperado: {e}")
            return False

    def test_admin_auth(self) -> str:
        """Prueba autenticación con credenciales de admin."""
        try:
            auth_url = f"{self.base_url}/api/admins/auth-with-password"
            payload = {
                "identity": self.admin_email,
                "password": self.admin_password
            }

            self.logger.info(f"Autenticando con email: {self.admin_email}")
            response = requests.post(
                auth_url,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                if token:
                    self.logger.info("✅ Autenticación exitosa")
                    self.logger.debug(f"Token obtenido (primeros 10 chars): {token[:10]}...")
                    return token
                else:
                    self.logger.error("❌ Autenticación exitosa pero no se recibió token")
                    return None
            elif response.status_code == 400:
                self.logger.error("❌ Credenciales inválidas")
                self.logger.error("   Verifica email y contraseña en PocketBaseConfig")
                return None
            else:
                self.logger.error(f"❌ Error de autenticación (HTTP {response.status_code})")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error durante autenticación: {e}")
            return None

    def test_collections_list(self, token: str) -> bool:
        """Prueba listado de colecciones."""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{self.base_url}/api/collections?perPage=10&schema=0"

            self.logger.info("Probando listado de colecciones...")
            response = requests.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                collections = data.get("items", [])
                non_system = [c for c in collections if not c.get("system", False)]

                self.logger.info(f"✅ Listado exitoso: {len(collections)} colecciones totales")
                self.logger.info(f"   Colecciones no-sistema: {len(non_system)}")

                if non_system:
                    self.logger.info("   Colecciones encontradas:")
                    for coll in non_system:
                        self.logger.info(f"    - {coll.get('name')} ({coll.get('type')})")

                return True
            else:
                self.logger.error(f"❌ Error listando colecciones (HTTP {response.status_code})")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error durante listado: {e}")
            return False

    def run_full_test(self) -> dict:
        """Ejecuta todas las pruebas secuencialmente."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "server_url": self.base_url,
            "tests": {},
            "success": False
        }

        self.logger.info("=" * 60)
        self.logger.info("🚀 Iniciando pruebas de conexión PocketBase")
        self.logger.info("=" * 60)

        # 1. Prueba de conexión al servidor
        self.logger.info("\n1️⃣  Prueba de conexión al servidor")
        server_ok = self.test_server_connection()
        results["tests"]["server_connection"] = {
            "success": server_ok,
            "message": "Conexión al servidor PocketBase"
        }

        if not server_ok:
            self.logger.error("\n❌ Prueba fallida: No se puede conectar al servidor")
            return results

        # 2. Prueba de autenticación
        self.logger.info("\n2️⃣  Prueba de autenticación")
        token = self.test_admin_auth()
        auth_success = token is not None
        results["tests"]["authentication"] = {
            "success": auth_success,
            "message": "Autenticación con credenciales de admin",
            "token_obtained": auth_success
        }

        if not auth_success:
            self.logger.error("\n❌ Prueba fallida: Autenticación inválida")
            return results

        # 3. Prueba de listado de colecciones
        self.logger.info("\n3️⃣  Prueba de listado de colecciones")
        collections_ok = self.test_collections_list(token)
        results["tests"]["collections_list"] = {
            "success": collections_ok,
            "message": "Listado de colecciones con token de admin"
        }

        # Resultado final
        all_tests_passed = all(test["success"] for test in results["tests"].values())
        results["success"] = all_tests_passed

        self.logger.info("\n" + "=" * 60)
        if all_tests_passed:
            self.logger.info("✅ TODAS LAS PRUEBAS EXITOSAS")
            self.logger.info("   PocketBase está configurado correctamente")
        else:
            failed_tests = [name for name, test in results["tests"].items() if not test["success"]]
            self.logger.error(f"❌ PRUEBAS FALLIDAS: {', '.join(failed_tests)}")

        self.logger.info("=" * 60)

        return results

def main():
    """Función principal."""
    import argparse

    parser = argparse.ArgumentParser(description="Prueba de conexión con PocketBase")
    parser.add_argument("--verbose", "-v", action="store_true", help="Habilitar logging detallado")
    parser.add_argument("--json", "-j", action="store_true", help="Mostrar resultados en formato JSON")
    parser.add_argument("--quick", "-q", action="store_true", help="Solo probar conexión básica")

    args = parser.parse_args()

    tester = ConnectionTester(verbose=args.verbose)

    if args.quick:
        # Solo prueba de conexión rápida
        server_ok = tester.test_server_connection()
        if args.json:
            result = {
                "timestamp": datetime.now().isoformat(),
                "server_url": tester.base_url,
                "server_connection": server_ok
            }
            print(json.dumps(result, indent=2))
        sys.exit(0 if server_ok else 1)
    else:
        # Prueba completa
        results = tester.run_full_test()

        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))

        sys.exit(0 if results["success"] else 1)

if __name__ == "__main__":
    main()
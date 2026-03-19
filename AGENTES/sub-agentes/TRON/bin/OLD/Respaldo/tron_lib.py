# TRON LIBRARY v2.0 - "EL CEREBRO DE NEGOCIOS" (Orientado a Objetos)
import os
import sys
import json
import time
import asyncio
import urllib.request
import logging
from pathlib import Path
from datetime import datetime
from pocketbase_sdk.client import Client
from pocketbase_sdk.utils import ClientResponseError

# --- CONSTANTES ---
POCKETBASE_URL = "http://127.0.0.1:8090"
CACHE_TTL_SECONDS = 86400  # 24 horas

# --- Colores para Logging ---
C_RESET = "\033[0m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"

log = logging.getLogger(__name__)

class TronDBManager:
    """
    Gestiona toda la interacción con la base de datos de PocketBase,
    incluyendo la gestión de modelos, la contabilidad y la sincronización del mercado.
    """
    def __init__(self, pb_url: str = POCKETBASE_URL):
        self.pb_url = pb_url
        self.client = Client(pb_url)
        self.is_connected = False
        log.debug("TronDBManager inicializado para URL: %s", pb_url)

    async def connect(self, user: str, password: str) -> bool:
        """
        Autentica el cliente de PocketBase usando email y contraseña.
        Retorna True si la autenticación es exitosa, False en caso contrario.
        """
        if self.client.auth_store.is_valid:
            log.debug("Cliente de PocketBase ya está autenticado.")
            self.is_connected = True
            return True
        try:
            log.debug("Intentando autenticar en PocketBase con el usuario: %s", user)
            await self.client.admins.auth_with_password(user, password)
            self.is_connected = True
            log.info("Conexión y autenticación con PocketBase exitosa.")
            return True
        except ClientResponseError as e:
            log.error("Error de autenticación con PocketBase (código %d): %s", e.status, e.data)
            self.is_connected = False
            return False
        except Exception as e:
            log.error("Error inesperado durante la conexión a PocketBase: %s", e, exc_info=True)
            self.is_connected = False
            return False

    async def init_db_collections(self):
        """
        Asegura que todas las colecciones necesarias existan en PocketBase.
        """
        if not self.is_connected:
            log.error("No se pueden inicializar colecciones: no hay conexión a la DB.")
            return

        log.debug("Verificando existencia de colecciones en la base de datos...")
        collections_to_check = {
            "openrouter_models": {
                "type": "base",
                "schema": [
                    {"name": "model_id", "type": "text", "required": True, "unique": True},
                    {"name": "name", "type": "text"},
                    {"name": "context_length", "type": "number"},
                    {"name": "price_prompt", "type": "number"},
                    {"name": "price_completion", "type": "number"},
                    {"name": "last_failure", "type": "number"},
                    {"name": "failure_count", "type": "number", "options": {"min": 0}},
                ],
            },
            "execution_logs": {
                "type": "base",
                "schema": [
                    {"name": "model_id", "type": "text", "required": True},
                    {"name": "tokens_in", "type": "number"},
                    {"name": "tokens_out", "type": "number"},
                    {"name": "calculated_cost_usd", "type": "number"},
                    {"name": "is_free", "type": "bool"},
                ]
            },
            "metadata": {
                "type": "base",
                "schema": [
                    {"name": "key", "type": "text", "required": True, "unique": True},
                    {"name": "value", "type": "json"}
                ],
            }
        }

        for name, spec in collections_to_check.items():
            try:
                existing_collection = await self.client.collections.get_one(name)
                log.debug("Colección '%s' ya existe.", name)

                # Verificar si la colección tiene el esquema correcto
                # Dependiendo de cómo se represente el objeto, puede ser un dict o un objeto
                if isinstance(existing_collection, dict):
                    # Si es un diccionario, acceder al esquema como campo
                    existing_schema = existing_collection.get('schema', [])
                    existing_fields = {field.get('name') for field in existing_schema if isinstance(field, dict)}
                elif hasattr(existing_collection, 'schema'):
                    # Si es un objeto con atributo schema
                    existing_fields = {field.name for field in existing_collection.schema}
                else:
                    log.warning("No se pudo determinar el esquema de la colección '%s'", name)
                    existing_fields = set()

                required_fields = {field['name'] for field in spec['schema']}

                if existing_fields != required_fields:
                    log.warning("La colección '%s' tiene un esquema diferente. Actualizando esquema...", name)
                    # Actualizar la colección con el esquema correcto
                    if isinstance(existing_collection, dict):
                        collection_id = existing_collection.get('id')
                    elif hasattr(existing_collection, 'id'):
                        collection_id = existing_collection.id
                    else:
                        log.error("No se pudo obtener el ID de la colección '%s'", name)
                        continue

                    if collection_id:
                        await self.client.collections.update(collection_id, {
                            "schema": spec["schema"]
                        })
                        log.info("Esquema de colección '%s' actualizado.", name)
                    else:
                        log.error("No se pudo obtener el ID de la colección para actualizar el esquema")
                else:
                    log.debug("Esquema de colección '%s' es correcto.", name)

            except ClientResponseError as e:
                if e.status == 404:
                    log.warning("Colección '%s' no encontrada. Creándola...", name)
                    await self.client.collections.create({
                        "name": name,
                        "type": spec["type"],
                        "schema": spec["schema"],
                        "listRule": None, "viewRule": None, # Abierto para facilidad de depuración
                        "createRule": None, "updateRule": None, "deleteRule": None
                    })
                    log.info("Colección '%s' creada exitosamente.", name)
                else:
                    log.error("Error al verificar la colección '%s': %s", name, e)

        # Asegurar que el metadato 'last_update' exista
        try:
            # Buscar el registro por clave en lugar de por ID
            records = await self.client.collection("metadata").get_full_list()
            existing_records = [record for record in records if record.get('key', '') == 'last_update']
            if not existing_records:
                log.warning("Registro 'last_update' no encontrado. Creándolo...")
                await self.client.collection("metadata").create({
                    "key": "last_update", "value": {"timestamp": 0}
                })
        except ClientResponseError as e:
            if e.status == 404:
                log.warning("Registro 'last_update' no encontrado. Creándolo...")
                await self.client.collection("metadata").create({
                    "key": "last_update", "value": {"timestamp": 0}
                })

    async def sync_market_data(self, openrouter_api_key: str):
        """
        Sincroniza los precios de OpenRouter con PocketBase si el caché ha expirado.
        """
        if not self.is_connected:
            log.error("No se puede sincronizar mercado: no hay conexión a la DB.")
            return

        try:
            # Buscar el registro por clave en lugar de por ID
            records = await self.client.collection("metadata").get_full_list()
            matching_records = [record for record in records if record.get('key', '') == 'last_update']
            if matching_records:
                value_field = matching_records[0].get('value', {})
                last_update = value_field.get("timestamp", 0) if value_field else 0
            else:
                log.error("No se pudo obtener el timestamp de la última actualización: registro no encontrado. Forzando sincronización.")
                last_update = 0
        except ClientResponseError as e:
            log.error("No se pudo obtener el timestamp de la última actualización: %s. Forzando sincronización.", e)
            last_update = 0

        if time.time() - last_update < CACHE_TTL_SECONDS:
            log.info("El mercado de modelos está actualizado (cache TTL %d s). No se necesita sincronización.", CACHE_TTL_SECONDS)
            return

        log.info("Iniciando sincronización del mercado de modelos desde OpenRouter...")
        loop = asyncio.get_running_loop()
        request = urllib.request.Request(
            url="https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {openrouter_api_key}"}
        )

        try:
            with await loop.run_in_executor(None, lambda: urllib.request.urlopen(request, timeout=20)) as response:
                data = json.loads(response.read())
                models = data.get('data', [])

                # Obtener todos los modelos existentes de una sola vez para comparar
                all_existing_records = await self.client.collection("openrouter_models").get_full_list()
                existing_model_map = {record.get('model_id'): record for record in all_existing_records}

                for m in models:
                    model_id = m.get('id')
                    if not model_id: continue

                    p = m.get('pricing', {})
                    data_to_upsert = {
                        "model_id": model_id,
                        "name": m.get('name'),
                        "context_length": m.get('context_length', 0),
                        "price_prompt": float(p.get('prompt', 0)),
                        "price_completion": float(p.get('completion', 0)),
                    }

                    try:
                        # Verificar si el modelo ya existe usando el mapa
                        if model_id in existing_model_map:
                            existing_record = existing_model_map[model_id]
                            record_id = existing_record.get('id')
                            if record_id:
                                await self.client.collection("openrouter_models").update(record_id, data_to_upsert)
                                log.debug("Modelo '%s' actualizado.", model_id)
                            else:
                                log.error("No se pudo obtener el ID del modelo existente para actualizar.")
                        else:
                            await self.client.collection("openrouter_models").create(data_to_upsert)
                            log.debug("Modelo nuevo '%s' creado.", model_id)
                    except ClientResponseError as e:
                        if e.status == 404:
                            await self.client.collection("openrouter_models").create(data_to_upsert)
                            log.debug("Modelo nuevo '%s' creado.", model_id)
                        else:
                            log.error("Error al actualizar/crear el modelo '%s': %s", model_id, e)

                new_timestamp = int(time.time())
                # Buscar el registro existente por clave y actualizarlo
                records = await self.client.collection("metadata").get_full_list()
                existing_records = [record for record in records if record.get('key', '') == 'last_update']
                if existing_records:
                    # Obtener el ID del registro para poder actualizarlo
                    record_id = existing_records[0].get('id')
                    if record_id:
                        await self.client.collection("metadata").update(record_id, {"value": {"timestamp": new_timestamp}})
                        log.info("Mercado de modelos sincronizado. %d modelos procesados.", len(models))
                    else:
                        log.error("No se encontró el ID del registro 'last_update' para actualizar.")
                else:
                    log.error("No se encontró el registro 'last_update' para actualizar.")

        except Exception as e:
            log.error("Falló la sincronización del mercado de OpenRouter: %s", e, exc_info=True)

    async def get_model_info(self, model_id: str) -> dict | None:
        """Recupera la información de un modelo desde PocketBase."""
        if not self.is_connected: return None
        try:
            records = await self.client.collection("openrouter_models").get_full_list()
            matching_records = [record for record in records if record.get('model_id', '') == model_id]
            if matching_records:
                return matching_records[0]
            else:
                log.warning("No se encontró información en la DB para el modelo '%s'.", model_id)
                return None
        except ClientResponseError as e:
            log.warning("No se encontró información en la DB para el modelo '%s': %s", model_id, e)
            return None

    async def log_model_failure(self, model_id: str):
        """Incrementa el contador de fallos y actualiza el timestamp del último fallo."""
        if not self.is_connected: return
        info = await self.get_model_info(model_id)
        if not info: return

        try:
            current_failures = info.get('failure_count', 0) or 0
            updates = {
                "last_failure": int(time.time()),
                "failure_count": current_failures + 1
            }
            await self.client.collection("openrouter_models").update(info['id'], updates)
            log.warning("Fallo registrado para el modelo '%s'. Contador: %d", model_id, updates["failure_count"])
        except Exception as e:
            log.error("Error al registrar fallo para el modelo '%s': %s", model_id, e)

    async def get_openrouter_balance(self, openrouter_api_key: str) -> dict | None:
        """Consulta el balance de la cuenta de OpenRouter."""
        log.debug("Consultando balance de la cuenta de OpenRouter.")
        request = urllib.request.Request(
            url="https://openrouter.ai/api/v1/credits",
            headers={"Authorization": f"Bearer {openrouter_api_key}"}
        )
        try:
            loop = asyncio.get_running_loop()
            with await loop.run_in_executor(None, lambda: urllib.request.urlopen(request, timeout=10)) as response:
                balance_data = json.loads(response.read())
                log.info("Balance de OpenRouter obtenido correctamente.")
                return balance_data
        except Exception as e:
            log.error("No se pudo obtener el balance de OpenRouter: %s", e)
            return None

    async def log_execution(self, model_id: str, tokens_in: int, tokens_out: int):
        """Registra una ejecución de modelo en la base de datos."""
        if not self.is_connected:
            log.error("No se puede registrar la ejecución: no hay conexión a la DB.")
            return

        model_info = await self.get_model_info(model_id)
        if not model_info:
            log.error("No se pudo registrar la ejecución: modelo '%s' no encontrado en la DB.", model_id)
            return

        price_prompt = model_info.get('price_prompt', 0)
        price_completion = model_info.get('price_completion', 0)
        
        is_free = price_prompt == 0 and price_completion == 0
        
        # Costo por millón de tokens
        cost = (price_prompt * tokens_in / 1_000_000) + (price_completion * tokens_out / 1_000_000)

        log_data = {
            "model_id": model_id,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "calculated_cost_usd": cost,
            "is_free": is_free
        }

        try:
            await self.client.collection("execution_logs").create(log_data)
            log.info("Ejecución registrada para el modelo '%s'. Costo: $%f", model_id, cost)
        except Exception as e:
            log.error("Error al registrar la ejecución en la base de datos: %s", e)
            
    async def smart_model_selection(self, requested_model_id: str) -> str:
        """
        Si el modelo pedido es gratuito y está 'enfermo', busca una alternativa saludable.
        Retorna el ID del modelo a usar (el original o una alternativa).
        """
        log.debug("Iniciando selección inteligente para el modelo: %s", requested_model_id)
        model_info = await self.get_model_info(requested_model_id)
        if not model_info:
            log.warning("No se encontró información para '%s', no se puede aplicar selección inteligente.", requested_model_id)
            return requested_model_id

        # Solo aplica para modelos gratuitos de OpenRouter
        is_free = model_info.get('price_prompt', 0) == 0 and model_info.get('price_completion', 0) == 0
        if not is_free:
            log.debug("El modelo '%s' no es gratuito, se usará directamente.", requested_model_id)
            return requested_model_id

        # Lógica de salud del modelo
        last_failure_ts = model_info.get('last_failure', 0)
        is_healthy = True
        if last_failure_ts > 0:
            # Penalización de 5 minutos
            if time.time() - last_failure_ts < 300:
                is_healthy = False
        
        if is_healthy and model_info.get('failure_count', 0) < 5:
             log.info("El modelo gratuito '%s' está saludable. Usando selección original.", requested_model_id)
             return requested_model_id
        
        # --- Buscar Alternativas ---
        log.warning("¡El modelo gratuito '%s' está en cooldown o tiene fallos recurrentes! Buscando alternativas...", requested_model_id)
        
        try:
            all_models = await self.client.collection("openrouter_models").get_full_list()
            # Filtrar localmente en lugar de usar params
            all_models = [model for model in all_models if model.get('price_prompt', 1) == 0]

            healthy_alternatives = []
            for model in all_models:
                if model.get('model_id') == requested_model_id: continue # No seleccionarse a sí mismo

                is_alt_healthy = True
                last_failure = model.get('last_failure', 0)
                if last_failure and last_failure > 0:
                    if time.time() - last_failure < 300:
                        is_alt_healthy = False

                failure_count = model.get('failure_count', 0)
                if is_alt_healthy and failure_count < 5:
                    healthy_alternatives.append(model.get('model_id'))

            if healthy_alternatives:
                import random
                alternative = random.choice(healthy_alternatives)
                log.info("Redirigiendo a una alternativa saludable: %s", alternative)
                return alternative
            else:
                log.error("No se encontraron alternativas gratuitas y saludables. Se reintentará con el modelo original.")
                return requested_model_id

        except Exception as e:
            log.error("Error al buscar alternativas de modelos: %s", e)
            return requested_model_id
# TRON LIBRARY v3.0 - "EL CEREBRO DE NEGOCIOS" (Almacenamiento en archivos JSON)
import os
import sys
import json
import time
import asyncio
import urllib.request
import logging
from pathlib import Path
from datetime import datetime

# --- CONSTANTES ---
DATA_DIR = Path(__file__).parent / "data"
CACHE_TTL_SECONDS = 86400  # 24 horas

# --- Colores para Logging ---
C_RESET = "\033[0m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"

log = logging.getLogger(__name__)

def ensure_data_dir():
    """Asegura que el directorio de datos exista."""
    DATA_DIR.mkdir(exist_ok=True)

def get_data_file_path(filename):
    """Obtiene la ruta completa para un archivo de datos."""
    ensure_data_dir()
    return DATA_DIR / filename

def read_json_file(filename):
    """Lee un archivo JSON, creando uno vacío si no existe."""
    file_path = get_data_file_path(filename)
    if not file_path.exists():
        # Crear archivo con estructura vacía
        with open(file_path, 'w') as f:
            json.dump({}, f)
        return {}
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        log.warning(f"Archivo {filename} está corrupto, creando uno nuevo")
        with open(file_path, 'w') as f:
            json.dump({}, f)
        return {}

def write_json_file(filename, data):
    """Escribe datos en un archivo JSON."""
    file_path = get_data_file_path(filename)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

class TronDBManager:
    """
    Gestiona toda la interacción con la base de datos usando archivos JSON,
    incluyendo la gestión de modelos, la contabilidad y la sincronización del mercado.
    """
    def __init__(self):
        ensure_data_dir()
        self.is_connected = True  # Siempre conectado porque usamos archivos locales
        log.debug("TronDBManager inicializado con almacenamiento en archivos JSON")

    async def connect(self, user: str = None, password: str = None) -> bool:
        """
        Conecta al sistema de almacenamiento (siempre exitoso con archivos).
        """
        log.info("Conexión con sistema de almacenamiento local exitosa.")
        return True

    async def init_db_collections(self):
        """
        Asegura que todos los archivos de datos necesarios existan.
        """
        log.debug("Inicializando archivos de datos...")
        
        # Crear archivos vacíos si no existen
        openrouter_models = read_json_file("openrouter_models.json")
        execution_logs = read_json_file("execution_logs.json")
        metadata = read_json_file("metadata.json")
        
        # Asegurar que el metadato 'last_update' exista
        if "last_update" not in metadata:
            metadata["last_update"] = {"timestamp": 0}
            write_json_file("metadata.json", metadata)

    async def sync_market_data(self, openrouter_api_key: str):
        """
        Sincroniza los precios de OpenRouter con archivos JSON si el caché ha expirado.
        """
        metadata = read_json_file("metadata.json")
        last_update = metadata.get("last_update", {}).get("timestamp", 0)

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

                # Leer modelos existentes
                openrouter_models = read_json_file("openrouter_models.json")
                
                for m in models:
                    model_id = m.get('id')
                    if not model_id: continue

                    p = m.get('pricing', {})
                    data_to_save = {
                        "model_id": model_id,
                        "name": m.get('name'),
                        "context_length": m.get('context_length', 0),
                        "price_prompt": float(p.get('prompt', 0)),
                        "price_completion": float(p.get('completion', 0)),
                        "last_failure": openrouter_models.get(model_id, {}).get("last_failure", 0),
                        "failure_count": openrouter_models.get(model_id, {}).get("failure_count", 0),
                    }
                    
                    openrouter_models[model_id] = data_to_save

                # Guardar todos los modelos actualizados
                write_json_file("openrouter_models.json", openrouter_models)
                
                # Actualizar timestamp
                metadata = read_json_file("metadata.json")
                metadata["last_update"]["timestamp"] = int(time.time())
                write_json_file("metadata.json", metadata)
                
                log.info("Mercado de modelos sincronizado. %d modelos procesados.", len(models))

        except Exception as e:
            log.error("Falló la sincronización del mercado de OpenRouter: %s", e, exc_info=True)

    async def get_model_info(self, model_id: str) -> dict | None:
        """Recupera la información de un modelo desde los archivos JSON."""
        openrouter_models = read_json_file("openrouter_models.json")
        model_info = openrouter_models.get(model_id)
        if model_info:
            return model_info
        else:
            log.warning("No se encontró información en la DB para el modelo '%s'.", model_id)
            return None

    async def log_model_failure(self, model_id: str):
        """Incrementa el contador de fallos y actualiza el timestamp del último fallo."""
        openrouter_models = read_json_file("openrouter_models.json")
        model_info = openrouter_models.get(model_id)
        if not model_info:
            log.warning("No se puede registrar fallo: modelo '%s' no encontrado.", model_id)
            return

        current_failures = model_info.get('failure_count', 0)
        model_info["last_failure"] = int(time.time())
        model_info["failure_count"] = current_failures + 1
        
        openrouter_models[model_id] = model_info
        write_json_file("openrouter_models.json", openrouter_models)
        
        log.warning("Fallo registrado para el modelo '%s'. Contador: %d", model_id, model_info["failure_count"])

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
        """Registra una ejecución de modelo en los archivos JSON."""
        model_info = await self.get_model_info(model_id)
        if not model_info:
            log.error("No se pudo registrar la ejecución: modelo '%s' no encontrado en la DB.", model_id)
            return

        price_prompt = model_info.get('price_prompt', 0)
        price_completion = model_info.get('price_completion', 0)

        is_free = price_prompt == 0 and price_completion == 0

        # Costo por millón de tokens
        cost = (price_prompt * tokens_in / 1_000_000) + (price_completion * tokens_out / 1_000_000)

        # Leer logs existentes y añadir nuevo registro
        execution_logs = read_json_file("execution_logs.json")
        log_entry = {
            "model_id": model_id,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "calculated_cost_usd": cost,
            "is_free": is_free,
            "timestamp": int(time.time())
        }
        
        # Usar timestamp como clave para evitar colisiones
        execution_logs[str(int(time.time() * 1000000))] = log_entry
        write_json_file("execution_logs.json", execution_logs)
        
        log.info("Ejecución registrada para el modelo '%s'. Costo: $%f", model_id, cost)

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
            # Leer todos los modelos
            openrouter_models = read_json_file("openrouter_models.json")
            
            # Filtrar modelos gratuitos
            all_models = [model_data for model_data in openrouter_models.values() 
                         if model_data.get('price_prompt', 1) == 0]

            healthy_alternatives = []
            for model_data in all_models:
                model_id = model_data.get('model_id')
                if model_id == requested_model_id: continue # No seleccionarse a sí mismo

                is_alt_healthy = True
                last_failure = model_data.get('last_failure', 0)
                if last_failure and last_failure > 0:
                    if time.time() - last_failure < 300:
                        is_alt_healthy = False

                failure_count = model_data.get('failure_count', 0)
                if is_alt_healthy and failure_count < 5:
                    healthy_alternatives.append(model_id)

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

    async def _get_all_models(self):
        """
        Devuelve todos los modelos disponibles desde el archivo JSON.
        """
        return read_json_file("openrouter_models.json")

    async def smart_model_selection(self, requested_model_id: str) -> str:
        """
        Si el modelo pedido es gratuito y está 'enhermo', busca una alternativa saludable.
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
            # Leer todos los modelos
            openrouter_models = read_json_file("openrouter_models.json")
            
            # Filtrar modelos gratuitos
            all_models = [model_data for model_data in openrouter_models.values() 
                         if model_data.get('price_prompt', 1) == 0]

            healthy_alternatives = []
            for model_data in all_models:
                model_id = model_data.get('model_id')
                if model_id == requested_model_id: continue # No seleccionarse a sí mismo

                is_alt_healthy = True
                last_failure = model_data.get('last_failure', 0)
                if last_failure and last_failure > 0:
                    if time.time() - last_failure < 300:
                        is_alt_healthy = False

                failure_count = model_data.get('failure_count', 0)
                if is_alt_healthy and failure_count < 5:
                    healthy_alternatives.append(model_id)

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
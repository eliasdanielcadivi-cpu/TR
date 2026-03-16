#!/usr/bin/env python3
# TRON BOOTSTRAP v4.0 - "EL ORQUESTADOR" (Orientado a Objetos)
import os
import sys
import yaml
import asyncio
import argparse
import logging
import subprocess
from pathlib import Path

# Agregar el directorio real del script al PYTHONPATH para encontrar tron_lib.py
# Los enlaces duros no tienen un "origen", así que usamos una ruta base fija
TRON_BASE_DIR = Path("/home/daniel/tron/programas/ProyectoPizza/TRON/bin")
if str(TRON_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(TRON_BASE_DIR))

# Rutas base del proyecto (usando ruta fija para soportar enlaces duros)
TRON_ROOT = TRON_BASE_DIR.parent  # /home/daniel/tron/programas/ProyectoPizza/TRON

try:
    from tron_lib import TronDBManager
except ImportError as e:
    print(f"\033[91mError Crítico: No se pudo importar 'tron_lib.py'.\nDetalle: {e}\033[0m", file=sys.stderr)
    sys.exit(1)

# --- CONSTANTES Y COLORES ---
C_RESET = "\033[0m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_MAGENTA = "\033[95m"
C_BOLD = "\033[1m"
LOG_FILE = TRON_ROOT / "resultados/debug_install.log"

class TronCLI:
    """
    Clase principal que orquesta la ejecución de TRON.
    Gestiona la configuración, la base de datos y la ejecución de subprocesos.
    """
    def __init__(self):
        self.config = None
        self.db_manager = None
        self.args = None

    def setup_logging(self):
        """Configura el sistema de logging, a consola o a archivo si --debug está activado."""
        log_level = logging.DEBUG if self.args.debug else logging.INFO
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Limpiar handlers anteriores para evitar duplicados
        root_logger = logging.getLogger()
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        if self.args.debug:
            # Sobre-escribir el archivo de log en cada ejecución de depuración
            logging.basicConfig(level=log_level, format=log_format, filename=LOG_FILE, filemode='w')
            # Añadir un handler para la consola también en modo debug
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO) # Mostrar solo INFO+ en consola
            console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
            root_logger.addHandler(console_handler)
            logging.debug("MODO DEBUG ACTIVADO. Logging verboso en: %s", LOG_FILE)
        else:
            # Logging estándar solo a consola
            logging.basicConfig(level=log_level, format='%(message)s', stream=sys.stdout)

    def parse_arguments(self):
        """Define y parsea los argumentos de la línea de comandos usando argparse."""
        parser = argparse.ArgumentParser(
            description=f"{C_BOLD}TRON v4.0 - El Orquestador de IA.{C_RESET}",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog="""Ejemplos: 
  tron                               # Inicia chat interactivo con DeepSeek.
  tron --router                      # Muestra menú para elegir modelo de OpenRouter.
  tron openrouter claude -p 'hola'   # Ejecuta claude con un modelo de OpenRouter.
  tron openrouter openai/gpt-4o claude -p 'hola' # Inyecta un modelo específico.
  tron deepseek python3 miscript.py  # Ejecuta un script Python con el entorno de DeepSeek.
  tron --debug ...                   # Activa el logging verboso a un archivo."""
        )
        parser.add_argument(
            'profile', nargs='?', default=None,
            help="Perfil de ejecución (ej. 'deepseek', 'openrouter')."
        )
        parser.add_argument(
            'model',
            nargs='?', default=None,
            help="Modelo a inyectar (ej. 'google/gemini-flash-1.5')."
        )
        parser.add_argument(
            'command', nargs=argparse.REMAINDER,
            help="Comando a ejecutar y sus argumentos (ej. 'claude -p 'pregunta'')."
        )
        parser.add_argument(
            '--router', action='store_true',
            help="Muestra un menú interactivo para seleccionar un modelo de OpenRouter."
        )
        parser.add_argument(
            '--debug', action='store_true',
            help="Activa el logging de depuración, sobre-escribiendo 'TRON/resultados/debug_install.log'."
        )
        parser.add_argument(
            '--batch', action='store_true',
            help="Activa el modo por lotes con reintentos para comandos largos."
        )
        self.args = parser.parse_args()

    def load_config(self):
        """Carga el archivo de configuración tron_config.yaml."""
        config_path = TRON_BASE_DIR / "tron_config.yaml"
        if not config_path.exists():
            logging.critical(f"{C_RED}Error Crítico: No se encuentra {config_path}{C_RESET}")
            sys.exit(1)
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        logging.debug("Configuración cargada desde %s", config_path)

    async def initialize_db(self):
        """Inicializa y conecta el gestor de la base de datos."""
        self.db_manager = TronDBManager()

        if await self.db_manager.connect():
            await self.db_manager.init_db_collections()
            # Sincronizar mercado en segundo plano para no retrasar el inicio
            openrouter_key = self.config['keys'].get('openrouter_live', '')
            if openrouter_key:
                asyncio.create_task(self.db_manager.sync_market_data(openrouter_key))
        else:
            logging.critical(f"{C_RED}No se pudo conectar al sistema de almacenamiento. TRON no puede continuar.{C_RESET}")
            sys.exit(1)

    def build_environment(self, profile_name, model_override=None):
        """Construye el diccionario de entorno para el subproceso."""
        env = os.environ.copy()
        env.update(self.config.get('global_env', {}))
        
        profile = self.config['profiles'].get(profile_name)
        if not profile:
            logging.error("Perfil '%s' no encontrado en la configuración. Usando 'deepseek' por defecto.", profile_name)
            profile = self.config['profiles']['deepseek']

        env['ANTHROPIC_BASE_URL'] = profile['base_url']
        for k, v in profile.get('env_vars', {}).items():
            env[k] = str(v)

        if model_override:
            env['ANTHROPIC_DEFAULT_SONNET_MODEL'] = model_override
            env['ANTHROPIC_MODEL'] = model_override

        api_key_ref = profile['provider_key_ref']
        api_key = self.config['keys'].get(api_key_ref, "")

        if profile['auth_strategy'] == "openrouter_mode":
            env['ANTHROPIC_AUTH_TOKEN'] = api_key
            env['ANTHROPIC_API_KEY'] = "" # Crítico para OpenRouter
        else: # deepseek_mode y otros
            env['ANTHROPIC_AUTH_TOKEN'] = api_key
            env['ANTHROPIC_API_KEY'] = api_key
            
        logging.debug("Entorno construido para el perfil '%s' con el modelo '%s'", profile_name, env.get('ANTHROPIC_MODEL'))
        return env

    async def run(self):
        """
        Punto de entrada principal para la ejecución de la lógica de TRON.
        """
        self.parse_arguments()
        self.setup_logging()
        self.load_config()
        await self.initialize_db()

        # --- Lógica de Decisión Principal ---
        profile = self.args.profile
        model = self.args.model
        command_args = self.args.command

        final_profile = 'deepseek'
        final_model = None
        final_command = ['claude']

        if self.args.router:
            final_profile = 'openrouter'

            # Asegurarse de que los modelos estén sincronizados
            openrouter_key = self.config['keys'].get('openrouter_live', '')
            if openrouter_key:
                print(f"{C_CYAN}Sincronizando modelos de OpenRouter...{C_RESET}")
                await self.db_manager.sync_market_data(openrouter_key)

            # Obtener modelos disponibles de OpenRouter
            try:
                # Leer modelos desde el archivo JSON
                all_models_dict = await self.db_manager._get_all_models()
                all_models = list(all_models_dict.values()) if all_models_dict else []

                # Filtrar y mostrar modelos gratuitos y de bajo costo
                free_models = [model for model in all_models if float(model.get('price_prompt', 1)) == 0.0 and float(model.get('price_completion', 1)) == 0.0]
                low_cost_models = [model for model in all_models if 0.0 < float(model.get('price_prompt', 1)) < 0.01 and 0.0 < float(model.get('price_completion', 1)) < 0.01]

                print(f"{C_CYAN}---[ MODELOS GRATUITOS DE OPENROUTER ]---{C_RESET}")
                if free_models:
                    for i, model in enumerate(free_models[:10]):  # Mostrar solo los primeros 10
                        last_failure = model.get('last_failure', 0)
                        health_indicator = "🟢" if (not last_failure or time.time() - last_failure >= 300) else "🔴"
                        failure_count = model.get('failure_count', 0) or 0
                        model_id = model.get('model_id', 'unknown')
                        print(f"{i+1:2d}. {health_indicator} {model_id} (Fallos: {failure_count})")
                else:
                    print("No hay modelos gratuitos disponibles actualmente.")

                print(f"{C_CYAN}---[ MODELOS DE BAJO COSTO DE OPENROUTER ]---{C_RESET}")
                if low_cost_models:
                    for i, model in enumerate(low_cost_models[:10]):  # Mostrar solo los primeros 10
                        last_failure = model.get('last_failure', 0)
                        health_indicator = "🟢" if (not last_failure or time.time() - last_failure >= 300) else "🔴"
                        failure_count = model.get('failure_count', 0) or 0
                        model_id = model.get('model_id', 'unknown')
                        price_prompt = model.get('price_prompt', 0)
                        price_completion = model.get('price_completion', 0)
                        print(f"{i+1:2d}. {health_indicator} {model_id} - Entrada: ${price_prompt}/M, Salida: ${price_completion}/M (Fallos: {failure_count})")
                else:
                    print("No hay modelos de bajo costo disponibles actualmente.")

                # Permitir al usuario seleccionar un modelo
                try:
                    selection = input(f"\n{C_YELLOW}Seleccione un modelo (número) o presione Enter para usar uno por defecto: {C_RESET}").strip()
                    if selection.isdigit():
                        selection_idx = int(selection) - 1
                        all_available = free_models + low_cost_models
                        if 0 <= selection_idx < len(all_available):
                            final_model = all_available[selection_idx].get('model_id', '')
                            print(f"{C_GREEN}Ha seleccionado el modelo: {final_model}{C_RESET}")
                        else:
                            print(f"{C_YELLOW}Selección inválida. Usando modelo por defecto.{C_RESET}")
                    else:
                        # Si no se ingresa un número, usar un modelo gratuito aleatorio o el primero disponible
                        if free_models:
                            import random
                            final_model = random.choice(free_models).get('model_id', '')
                            print(f"{C_GREEN}Usando modelo gratuito aleatorio: {final_model}{C_RESET}")
                        elif low_cost_models:
                            final_model = low_cost_models[0].get('model_id', '')
                            print(f"{C_GREEN}Usando primer modelo de bajo costo: {final_model}{C_RESET}")
                        else:
                            print(f"{C_RED}No hay modelos disponibles. Saliendo.{C_RESET}")
                            sys.exit(1)
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{C_YELLOW}Operación cancelada por el usuario.{C_RESET}")
                    sys.exit(0)
            except Exception as e:
                logging.error("Error al obtener modelos de OpenRouter: %s", e)
                print(f"{C_RED}Error al obtener modelos de OpenRouter. Saliendo.{C_RESET}")
                sys.exit(1)

        elif profile and profile in self.config['profiles']:
            final_profile = profile
            # ¿El segundo argumento es un modelo o parte del comando?
            if model and ('/' in model or ':' in model):
                final_model = model
            else: # No es un modelo, es parte del comando
                if model: command_args.insert(0, model)
                final_model = self.config['profiles'][final_profile]['env_vars'].get('ANTHROPIC_MODEL') or \
                              self.config['profiles'][final_profile]['env_vars'].get('ANTHROPIC_DEFAULT_SONNET_MODEL')

            if command_args:
                final_command = command_args
        
        elif not profile: # Modo por defecto: tron
             final_profile = 'deepseek'
             final_model = self.config['profiles']['deepseek']['env_vars'].get('ANTHROPIC_MODEL')
             if model: # Si hay algo más, son argumentos para claude
                 command_args.insert(0, model)
             if command_args:
                 final_command = ['claude'] + command_args

        else: # El primer argumento no es un perfil válido, se asume que es parte del comando
            final_profile = 'deepseek'
            final_model = self.config['profiles']['deepseek']['env_vars'].get('ANTHROPIC_MODEL')
            command_args.insert(0, model)
            command_args.insert(0, profile)
            final_command = command_args

        # --- Construcción y Ejecución ---
        # Filtrar None values antes de unir
        filtered_final_command = [cmd for cmd in final_command if cmd is not None]
        logging.info("Perfil final: %s | Modelo final: %s | Comando: %s", final_profile, final_model, ' '.join(filtered_final_command))

        # Aplicar selección inteligente de modelo si es un perfil de OpenRouter
        if final_profile == 'openrouter' and final_model:
            logging.debug("Aplicando selección inteligente de modelo para: %s", final_model)
            final_model = await self.db_manager.smart_model_selection(final_model)
            logging.info("Modelo seleccionado tras aplicación de inteligencia: %s", final_model)

        # Obtener y mostrar el balance de OpenRouter si es un perfil de OpenRouter
        if final_profile == 'openrouter':
            openrouter_key = self.config['keys'].get('openrouter_live', '')
            if openrouter_key:
                balance_info = await self.db_manager.get_openrouter_balance(openrouter_key)
                if balance_info:
                    remaining_credits = balance_info.get('data', {}).get('usage', {}).get('remaining', 'N/A')
                    total_credits = balance_info.get('data', {}).get('usage', {}).get('total', 'N/A')
                    reset_date = balance_info.get('data', {}).get('reset_date', 'N/A')

                    print(f"{C_CYAN}---[ BALANCE DE OPENROUTER ]---{C_RESET}")
                    print(f"Créditos totales: {C_GREEN}{total_credits}{C_RESET}")
                    print(f"Créditos restantes: {C_YELLOW}{remaining_credits}{C_RESET}")
                    print(f"Fecha de reinicio: {C_MAGENTA}{reset_date}{C_RESET}")

                    # Calcular costo estimado si tenemos un modelo seleccionado
                    if final_model:
                        model_info = await self.db_manager.get_model_info(final_model)
                        if model_info:
                            price_prompt = model_info.get('price_prompt', 0)
                            price_completion = model_info.get('price_completion', 0)

                            # Mostrar precios del modelo
                            print(f"{C_CYAN}---[ PRECIO DEL MODELO SELECCIONADO ]---{C_RESET}")
                            print(f"Modelo: {C_MAGENTA}{final_model}{C_RESET}")
                            print(f"Precio por millón de tokens de entrada: ${C_GREEN}{price_prompt}{C_RESET}")
                            print(f"Precio por millón de tokens de salida: ${C_GREEN}{price_completion}{C_RESET}")

                            # Estimar costo basado en longitud del prompt si está disponible
                            if command_args and '-p' in command_args:
                                try:
                                    prompt_idx = command_args.index('-p') + 1
                                    if prompt_idx < len(command_args):
                                        prompt = command_args[prompt_idx]
                                        # Aproximación: 1 token ~ 4 caracteres
                                        estimated_tokens_in = len(prompt) / 4

                                        # Costo estimado (esto es una aproximación)
                                        estimated_cost = (price_prompt * estimated_tokens_in / 1_000_000)
                                        print(f"{C_CYAN}---[ COSTO ESTIMADO ]---{C_RESET}")
                                        print(f"Tokens de entrada estimados: {C_YELLOW}{estimated_tokens_in:.0f}{C_RESET}")
                                        print(f"Costo estimado: ${C_RED}{estimated_cost:.6f}{C_RESET}")
                                except Exception as e:
                                    logging.warning("No se pudo calcular el costo estimado: %s", e)

        final_env = self.build_environment(final_profile, final_model)

        print(f"{C_CYAN}---[ TRON V4.0 ]---{C_RESET}")
        print(f"Perfil: {C_GREEN}{final_profile}{C_RESET} | Modelo: {C_MAGENTA}{final_model or 'Default'}{C_RESET}")
        print(f"Comando: {C_YELLOW}{' '.join([cmd for cmd in final_command if cmd is not None])}{C_RESET}")
        print(f"{C_CYAN}---------------------{C_RESET}")

        # Ejecutar en modo batch si está activado
        if self.args.batch:
            await self.run_batch_mode(final_command, final_env, final_profile, final_model)
        else:
            await self.run_single_mode(final_command, final_env, final_profile, final_model)

    async def run_single_mode(self, final_command, final_env, final_profile, final_model):
        """Ejecuta un comando una sola vez."""
        # Filtrar None values antes de usar en subprocess
        filtered_final_command = [cmd for cmd in final_command if cmd is not None]

        try:
            # Usamos subprocess.run para esperar a que el comando termine
            # Pero mostramos la salida directamente en lugar de capturarla
            process = subprocess.run(filtered_final_command, env=final_env, check=False)

            # Capturamos la salida solo si necesitamos procesarla (para tokens)
            if process.returncode == 0:
                logging.info("Comando ejecutado exitosamente.")

                # Para procesar tokens, necesitamos la salida, así que volvemos a ejecutar con captura
                # Solo si es necesario para el procesamiento de tokens
                if final_model:  # Solo si queremos procesar tokens
                    process_with_capture = subprocess.run(filtered_final_command, env=final_env, check=False, capture_output=True, text=True)
                    output = process_with_capture.stdout
                    error_output = process_with_capture.stderr

                    # Intentar obtener tokens de entrada y salida del comando
                    tokens_in = 0
                    tokens_out = 0

                    # Patrones comunes para buscar información de tokens
                    import re

                    # Buscar tokens en la salida estándar
                    tokens_in_match = re.search(r'tokens_in["\']?\s*[:=]\s*(\d+)', output)
                    tokens_out_match = re.search(r'tokens_out["\']?\s*[:=]\s*(\d+)', output)

                    # Si no se encontraron en la salida estándar, buscar en la salida de error
                    if not tokens_in_match:
                        tokens_in_match = re.search(r'tokens_in["\']?\s*[:=]\s*(\d+)', error_output)
                    if not tokens_out_match:
                        tokens_out_match = re.search(r'tokens_out["\']?\s*[:=]\s*(\d+)', error_output)

                    # Extraer valores si se encontraron
                    if tokens_in_match:
                        tokens_in = int(tokens_in_match.group(1))
                    if tokens_out_match:
                        tokens_out = int(tokens_out_match.group(1))

                    # Si no se encontraron tokens en la salida, usar estimación basada en longitud
                    if tokens_in == 0 and filtered_final_command and '-p' in filtered_final_command:
                        try:
                            prompt_idx = filtered_final_command.index('-p') + 1
                            if prompt_idx < len(filtered_final_command):
                                prompt = filtered_final_command[prompt_idx]
                                # Aproximación: 1 token ~ 4 caracteres
                                tokens_in = len(prompt) // 4
                        except Exception as e:
                            logging.warning("No se pudo estimar tokens de entrada: %s", e)

                    # Registrar la ejecución en la base de datos
                    if final_model and (tokens_in > 0 or tokens_out > 0):
                        await self.db_manager.log_execution(final_model, tokens_in, tokens_out)
            else:
                logging.error("El comando finalizó con código de error: %d", process.returncode)
                # Registrar fallo del modelo si es de OpenRouter
                if final_profile == 'openrouter' and final_model:
                    asyncio.create_task(self.db_manager.log_model_failure(final_model))

        except FileNotFoundError:
            logging.critical(f"{C_RED}Error: Comando '{filtered_final_command[0]}' no encontrado en el PATH del sistema.{C_RESET}")
        except Exception as e:
            logging.critical(f"{C_RED}Error fatal durante la ejecución del subproceso: {e}{C_RESET}", exc_info=self.args.debug)

    async def run_batch_mode(self, final_command, final_env, final_profile, final_model):
        """Ejecuta un comando en modo batch con reintentos y manejo de fallos."""
        import random
        max_retries = 5
        base_delay = 1  # segundos
        max_delay = 60  # segundos

        retry_count = 0

        while True:
            # Filtrar None values antes de usar en subprocess
            filtered_final_command = [cmd for cmd in final_command if cmd is not None]

            try:
                # Usamos subprocess.run para esperar a que el comando termine
                # Pero mostramos la salida directamente en lugar de capturarla
                process = subprocess.run(filtered_final_command, env=final_env, check=False)

                # Capturamos la salida solo si necesitamos procesarla (para tokens)
                if process.returncode == 0:
                    logging.info("Comando ejecutado exitosamente en modo batch.")

                    # Para procesar tokens, necesitamos la salida, así que volvemos a ejecutar con captura
                    # Solo si es necesario para el procesamiento de tokens
                    if final_model:  # Solo si queremos procesar tokens
                        process_with_capture = subprocess.run(filtered_final_command, env=final_env, check=False, capture_output=True, text=True)
                        output = process_with_capture.stdout
                        error_output = process_with_capture.stderr

                        # Intentar obtener tokens de entrada y salida del comando
                        tokens_in = 0
                        tokens_out = 0

                        # Patrones comunes para buscar información de tokens
                        import re

                        # Buscar tokens en la salida estándar
                        tokens_in_match = re.search(r'tokens_in["\']?\s*[:=]\s*(\d+)', output)
                        tokens_out_match = re.search(r'tokens_out["\']?\s*[:=]\s*(\d+)', output)

                        # Si no se encontraron en la salida estándar, buscar en la salida de error
                        if not tokens_in_match:
                            tokens_in_match = re.search(r'tokens_in["\']?\s*[:=]\s*(\d+)', error_output)
                        if not tokens_out_match:
                            tokens_out_match = re.search(r'tokens_out["\']?\s*[:=]\s*(\d+)', error_output)

                        # Extraer valores si se encontraron
                        if tokens_in_match:
                            tokens_in = int(tokens_in_match.group(1))
                        if tokens_out_match:
                            tokens_out = int(tokens_out_match.group(1))

                        # Si no se encontraron tokens en la salida, usar estimación basada en longitud
                        if tokens_in == 0 and filtered_final_command and '-p' in filtered_final_command:
                            try:
                                prompt_idx = filtered_final_command.index('-p') + 1
                                if prompt_idx < len(filtered_final_command):
                                    prompt = filtered_final_command[prompt_idx]
                                    # Aproximación: 1 token ~ 4 caracteres
                                    tokens_in = len(prompt) // 4
                            except Exception as e:
                                logging.warning("No se pudo estimar tokens de entrada: %s", e)

                        # Registrar la ejecución en la base de datos
                        if final_model and (tokens_in > 0 or tokens_out > 0):
                            await self.db_manager.log_execution(final_model, tokens_in, tokens_out)

                    # Reiniciar contador de reintentos tras una ejecución exitosa
                    retry_count = 0

                    # Pequeña pausa antes de la próxima ejecución
                    import time
                    time.sleep(1)

                else:
                    logging.error("El comando finalizó con código de error: %d", process.returncode)

                    # Registrar fallo del modelo si es de OpenRouter
                    if final_profile == 'openrouter' and final_model:
                        await self.db_manager.log_model_failure(final_model)

                    # Incrementar contador de reintentos
                    retry_count += 1

                    if retry_count >= max_retries:
                        logging.error(f"Se alcanzó el número máximo de reintentos ({max_retries}). Saliendo del modo batch.")
                        break

                    # Aplicar selección inteligente de modelo si es un perfil de OpenRouter
                    if final_profile == 'openrouter' and final_model:
                        logging.debug("Aplicando selección inteligente de modelo tras fallo: %s", final_model)
                        final_model = await self.db_manager.smart_model_selection(final_model)
                        logging.info("Nuevo modelo seleccionado tras fallo: %s", final_model)

                        # Actualizar el entorno con el nuevo modelo
                        final_env = self.build_environment(final_profile, final_model)

                    # Calcular retraso con espera exponencial y jitter
                    delay = min(base_delay * (2 ** retry_count), max_delay)
                    jitter = random.uniform(0, delay * 0.1)  # 10% de jitter
                    total_delay = delay + jitter

                    logging.info(f"Reintentando en {total_delay:.2f} segundos... (intento {retry_count}/{max_retries})")
                    import time
                    time.sleep(total_delay)

            except FileNotFoundError:
                logging.critical(f"{C_RED}Error: Comando '{filtered_final_command[0]}' no encontrado en el PATH del sistema.{C_RESET}")
                break
            except KeyboardInterrupt:
                logging.info("Operación interrumpida por el usuario. Saliendo del modo batch.")
                break
            except Exception as e:
                logging.critical(f"{C_RED}Error fatal durante la ejecución del subproceso: {e}{C_RESET}", exc_info=self.args.debug)
                break


async def main():
    cli = TronCLI()
    await cli.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{C_YELLOW}Operación cancelada por el usuario.{C_RESET}")
        sys.exit(0)

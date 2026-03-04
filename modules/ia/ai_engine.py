"""AIEngine: Dispatcher multi-provider para ARES.

Coordina los diferentes providers de IA (Gemma, DeepSeek, OpenRouter)
y gestiona templates y herramientas.

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import os
from typing import Dict, Any, Optional, List

from .providers import (
    BaseProvider,
    GemmaProvider,
    DeepSeekProvider,
    OpenRouterProvider,
)
from .templates import TemplateManager
from .tools import ToolRegistry


class AIEngine:
    """Motor de IA multi-provider para ARES.
    
    Actúa como dispatcher que:
    - Selecciona el provider adecuado según alias o modelo
    - Aplica plantillas YAML configuradas
    - Gestiona herramientas para function calling
    """

    def __init__(self, config: Dict[str, Any], base_path: str):
        """Inicializar AIEngine.
        
        Args:
            config: Configuración de IA desde config.yaml.
            base_path: Ruta base del proyecto TR.
        """
        self.config = config
        self.base_path = base_path
        self.default_provider = config.get("default_provider", "ollama")
        self.aliases = config.get("aliases", {})
        
        # Inicializar providers
        self._providers: Dict[str, BaseProvider] = {}
        self._init_providers(config)
        
        # Inicializar gestor de plantillas
        templates_dir = os.path.join(base_path, "modules", "ia", "templates")
        self.template_manager = TemplateManager(templates_dir)
        
        # Inicializar registro de herramientas
        self.tool_registry = ToolRegistry()
        self._register_default_tools()

    def ask(self, prompt: str, model_alias: Optional[str] = None, 
            template: Optional[str] = None, **kwargs) -> str:
        """Consultar a la IA con prompt.
        
        Args:
            prompt: Prompt de entrada.
            model_alias: Alias de modelo (gemma, deepseek, etc.).
            template: Nombre de plantilla YAML a aplicar.
            **kwargs: Parámetros adicionales (temperature, max_tokens, etc.).
            
        Returns:
            Respuesta de la IA.
        """
        # Determinar provider y modelo
        provider, model = self._resolve_provider_and_model(model_alias, template)
        
        # Aplicar plantilla si se especifica
        if template:
            prompt = self.template_manager.apply(
                provider.name if hasattr(provider, 'name') else self._get_provider_name(provider),
                template,
                prompt=prompt
            )
        
        # Obtener configuración de plantilla si existe
        template_config = {}
        if template:
            provider_name = self._get_provider_name(provider)
            template_config = self.template_manager.get_config(provider_name, template)
        
        # Fusionar parámetros
        params = {**template_config, **kwargs}
        if model:
            params["model"] = model
        
        # Ejecutar consulta
        return provider.generate(prompt, **params)

    def chat(self, messages: List[Dict[str, str]], 
             model_alias: Optional[str] = None,
             use_tools: bool = False,
             **kwargs) -> str:
        """Consultar en modo chat.
        
        Args:
            messages: Lista de mensajes con rol y contenido.
            model_alias: Alias de modelo.
            use_tools: Si True, incluir herramientas disponibles.
            **kwargs: Parámetros adicionales.
            
        Returns:
            Respuesta de la IA.
        """
        provider, model = self._resolve_provider_and_model(model_alias)
        
        params = {"model": model} if model else {}
        params.update(kwargs)
        
        # Incluir herramientas si se solicita
        if use_tools and hasattr(provider, 'parse_tool_call'):
            tools = self.tool_registry.to_ollama_format()
            if tools:
                params["tools"] = tools
        
        return provider.chat(messages, **params)

    def list_models(self, provider_name: Optional[str] = None) -> Dict[str, List[str]]:
        """Listar modelos disponibles por provider.
        
        Args:
            provider_name: Filtrar por provider (opcional).
            
        Returns:
            Diccionario de provider -> lista de modelos.
        """
        result = {}
        
        for name, provider in self._providers.items():
            if provider_name is None or name == provider_name:
                result[name] = provider.list_models()
        
        return result

    def list_templates(self, provider: Optional[str] = None) -> List[str]:
        """Listar plantillas disponibles.
        
        Args:
            provider: Filtrar por provider (opcional).
            
        Returns:
            Lista de nombres de plantillas.
        """
        return self.template_manager.list_templates(provider)

    def list_tools(self) -> List[Dict[str, Any]]:
        """Listar herramientas registradas.
        
        Returns:
            Lista de definiciones de herramientas.
        """
        return self.tool_registry.list_tools()

    def _init_providers(self, config: Dict[str, Any]) -> None:
        """Inicializar todos los providers configurados.

        Args:
            config: Configuración de IA.
        """
        # Gemma/Ollama (buscar por 'gemma' o 'ollama' en config)
        gemma_config = config.get("gemma") or config.get("ollama")
        if gemma_config:
            gemma_config = gemma_config.copy()
            gemma_config["templates"] = {}  # Se cargan desde template_manager
            self._providers["gemma"] = GemmaProvider(gemma_config)
            self._providers["ollama"] = self._providers["gemma"]  # Alias

        # DeepSeek
        if "deepseek" in config:
            self._providers["deepseek"] = DeepSeekProvider(config["deepseek"])

        # OpenRouter (placeholder)
        if "openrouter" in config:
            self._providers["openrouter"] = OpenRouterProvider(config["openrouter"])
        else:
            # Registrar placeholder aunque no esté en config
            self._providers["openrouter"] = OpenRouterProvider({})

    def _resolve_provider_and_model(
        self,
        model_alias: Optional[str],
        template: Optional[str] = None
    ) -> tuple:
        """Resolver provider y modelo desde alias o template.

        Args:
            model_alias: Alias de modelo (gemma, gemma3:4b, deepseek, etc.).
            template: Nombre de plantilla (puede indicar provider).

        Returns:
            Tupla (provider, model).
        """
        # Si hay alias explícito, usarlo
        if model_alias:
            alias_lower = model_alias.lower()

            # Verificar aliases configurados
            if alias_lower in self.aliases:
                alias_config = self.aliases[alias_lower]
                provider_name = alias_config.get("provider", "ollama")
                model = alias_config.get("model")
                provider = self._providers.get(provider_name)
                return provider or self._get_default_provider(), model

            # Detectar provider por nombre de modelo
            if "gemma" in alias_lower:
                return self._providers.get("gemma", self._get_default_provider()), alias_lower
            elif "deepseek" in alias_lower:
                return self._providers.get("deepseek"), alias_lower
            elif "phi" in alias_lower or "llama" in alias_lower or "qwen" in alias_lower:
                # Modelos Ollama genéricos
                return self._providers.get("gemma", self._get_default_provider()), alias_lower

            # Verificar providers directos
            if alias_lower in self._providers:
                return self._providers[alias_lower], None

        # Si hay template, intentar inferir provider
        if template:
            if template.startswith("gemma/") or "/" not in template:
                return self._providers.get("gemma", self._get_default_provider()), None
            elif template.startswith("deepseek/"):
                return self._providers.get("deepseek"), None

        # Usar provider por defecto
        return self._get_default_provider(), None

    def _get_default_provider(self) -> BaseProvider:
        """Obtener provider por defecto.
        
        Returns:
            Provider por defecto.
        """
        if self.default_provider == "deepseek":
            return self._providers.get("deepseek", self._providers.get("gemma"))
        return self._providers.get("gemma", self._providers.get("deepseek"))

    def _get_provider_name(self, provider: BaseProvider) -> str:
        """Obtener nombre de provider.
        
        Args:
            provider: Instancia de provider.
            
        Returns:
            Nombre del provider.
        """
        if isinstance(provider, GemmaProvider):
            return "gemma"
        elif isinstance(provider, DeepSeekProvider):
            return "deepseek"
        elif isinstance(provider, OpenRouterProvider):
            return "openrouter"
        return "gemma"

    def _register_default_tools(self) -> None:
        """Registrar herramientas por defecto."""
        from .tools.tool_registry import (
            search_tool,
            translate_tool,
            weather_tool,
            shell_tool,
            read_file_tool,
            write_file_tool,
        )
        
        # Herramientas de búsqueda y información
        self.tool_registry.register(
            "google_search",
            "Buscar información en tiempo real",
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Término de búsqueda"}
                },
                "required": ["query"]
            },
            search_tool
        )
        
        # Herramientas de traducción
        self.tool_registry.register(
            "translate_text",
            "Traducir texto a otro idioma",
            {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Texto a traducir"},
                    "target_language": {"type": "string", "description": "Idioma destino"}
                },
                "required": ["text", "target_language"]
            },
            translate_tool
        )
        
        # Herramientas de clima
        self.tool_registry.register(
            "get_weather",
            "Obtener clima actual",
            {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Ciudad"}
                },
                "required": ["city"]
            },
            weather_tool
        )
        
        # Herramientas de sistema
        self.tool_registry.register(
            "execute_shell",
            "Ejecutar comando shell",
            {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Comando"},
                    "working_dir": {"type": "string", "description": "Directorio"}
                },
                "required": ["command"]
            },
            shell_tool
        )
        
        # Herramientas de archivos
        self.tool_registry.register(
            "read_file",
            "Leer archivo",
            {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Ruta del archivo"},
                    "max_lines": {"type": "integer", "description": "Máximo de líneas"}
                },
                "required": ["path"]
            },
            read_file_tool
        )
        
        self.tool_registry.register(
            "write_file",
            "Escribir archivo",
            {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Ruta del archivo"},
                    "content": {"type": "string", "description": "Contenido"},
                    "append": {"type": "boolean", "description": "Añadir al final"}
                },
                "required": ["path", "content"]
            },
            write_file_tool
        )

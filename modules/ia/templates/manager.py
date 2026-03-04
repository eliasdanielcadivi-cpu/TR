"""TemplateManager: Gestor de plantillas YAML para ARES.

Sistema de configuración basado en YAML para:
- Plantillas de prompt optimizadas
- Definición de herramientas (functions/tools)
- Parámetros de generación (temperatura, top_p, etc.)

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path


class TemplateManager:
    """Gestor de plantillas YAML para providers de IA.
    
    Carga, valida y aplica plantillas desde archivos YAML
    organizados por provider y nombre de plantilla.
    """

    def __init__(self, templates_dir: str):
        """Inicializar TemplateManager.
        
        Args:
            templates_dir: Directorio base de plantillas.
        """
        self.templates_dir = Path(templates_dir)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._load_all_templates()

    def get_template(self, provider: str, name: str) -> Optional[str]:
        """Obtener plantilla por provider y nombre.
        
        Args:
            provider: Nombre del provider (gemma, deepseek, etc.).
            name: Nombre de la plantilla (default, chat, code, etc.).
            
        Returns:
            Contenido de la plantilla o None si no existe.
        """
        key = f"{provider}/{name}"
        
        if key in self._cache:
            return self._cache[key].get("content")
        
        return self._load_template(provider, name)

    def get_config(self, provider: str, name: str) -> Dict[str, Any]:
        """Obtener configuración de plantilla.
        
        Args:
            provider: Nombre del provider.
            name: Nombre de la plantilla.
            
        Returns:
            Diccionario con configuración (temperature, model, etc.).
        """
        key = f"{provider}/{name}"
        
        if key in self._cache:
            return self._cache[key].get("config", {})
        
        self._load_template(provider, name)
        return self._cache.get(key, {}).get("config", {})

    def list_templates(self, provider: Optional[str] = None) -> List[str]:
        """Listar plantillas disponibles.
        
        Args:
            provider: Filtrar por provider (opcional).
            
        Returns:
            Lista de nombres de plantillas.
        """
        templates = []
        
        for key in self._cache:
            if provider is None or key.startswith(f"{provider}/"):
                templates.append(key)
        
        return templates

    def apply(self, provider: str, name: str, **kwargs) -> str:
        """Aplicar plantilla con variables.
        
        Args:
            provider: Nombre del provider.
            name: Nombre de la plantilla.
            **kwargs: Variables para reemplazar en la plantilla.
            
        Returns:
            Plantilla procesada o mensaje de error.
        """
        template = self.get_template(provider, name)
        
        if not template:
            return kwargs.get("prompt", "")
        
        try:
            return template.format(**kwargs)
        except KeyError as e:
            return f"⚠️ Error en plantilla: variable {e} no encontrada"

    def _load_all_templates(self) -> None:
        """Cargar todas las plantillas desde el sistema de archivos."""
        if not self.templates_dir.exists():
            return
        
        for provider_dir in self.templates_dir.iterdir():
            if not provider_dir.is_dir():
                continue
            
            provider = provider_dir.name
            
            for yaml_file in provider_dir.glob("*.yaml"):
                template_name = yaml_file.stem
                self._load_yaml_file(provider, template_name, yaml_file)

    def _load_template(self, provider: str, name: str) -> Optional[str]:
        """Cargar plantilla específica desde archivo YAML.
        
        Args:
            provider: Nombre del provider.
            name: Nombre de la plantilla.
            
        Returns:
            Contenido de la plantilla o None.
        """
        yaml_path = self.templates_dir / provider / f"{name}.yaml"
        
        if not yaml_path.exists():
            return None
        
        return self._load_yaml_file(provider, name, yaml_path)

    def _load_yaml_file(self, provider: str, name: str, path: Path) -> Optional[str]:
        """Cargar archivo YAML y guardar en cache.
        
        Args:
            provider: Nombre del provider.
            name: Nombre de la plantilla.
            path: Ruta al archivo YAML.
            
        Returns:
            Contenido de la plantilla o None.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            if not isinstance(data, dict):
                return None
            
            key = f"{provider}/{name}"
            
            # Extraer contenido y configuración
            content = data.get("content", "")
            config = data.get("config", {})
            
            self._cache[key] = {
                "content": content,
                "config": config,
                "path": str(path)
            }
            
            return content
            
        except (yaml.YAMLError, IOError) as e:
            print(f"Error cargando plantilla {path}: {e}")
            return None

    def reload(self) -> None:
        """Recargar todas las plantillas desde disco."""
        self._cache.clear()
        self._load_all_templates()

    def get_tools_definition(self, provider: str) -> List[Dict[str, Any]]:
        """Obtener definición de herramientas para un provider.
        
        Args:
            provider: Nombre del provider.
            
        Returns:
            Lista de definiciones de herramientas.
        """
        tools_template = self.get_template(provider, "tools")
        
        if not tools_template:
            return []
        
        try:
            # Parsear YAML de herramientas
            tools_data = yaml.safe_load(tools_template)
            return tools_data.get("tools", []) if isinstance(tools_data, dict) else []
        except yaml.YAMLError:
            return []

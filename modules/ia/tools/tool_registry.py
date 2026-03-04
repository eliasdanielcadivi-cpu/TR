"""ToolRegistry: Registro y ejecución de herramientas para ARES.

Sistema de function calling que permite:
- Registrar herramientas dinámicamente
- Ejecutar herramientas basadas en output del LLM
- Validar parámetros de entrada

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import json
from typing import Dict, Any, List, Optional, Callable


class ToolRegistry:
    """Registro central de herramientas para ARES.
    
    Permite registrar, listar y ejecutar herramientas
    que pueden ser llamadas por los modelos de IA.
    """

    def __init__(self):
        """Inicializar registro de herramientas."""
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._executors: Dict[str, Callable] = {}

    def register(
        self, 
        name: str, 
        description: str,
        parameters: Dict[str, Any],
        executor: Callable
    ) -> None:
        """Registrar una herramienta.
        
        Args:
            name: Nombre único de la herramienta.
            description: Descripción de lo que hace la herramienta.
            parameters: Esquema JSON Schema de parámetros.
            executor: Función que ejecuta la herramienta.
        """
        self._tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters
        }
        self._executors[name] = executor

    def unregister(self, name: str) -> bool:
        """Eliminar una herramienta registrada.
        
        Args:
            name: Nombre de la herramienta a eliminar.
            
        Returns:
            True si se eliminó, False si no existía.
        """
        if name in self._tools:
            del self._tools[name]
            if name in self._executors:
                del self._executors[name]
            return True
        return False

    def list_tools(self) -> List[Dict[str, Any]]:
        """Listar todas las herramientas registradas.
        
        Returns:
            Lista de definiciones de herramientas.
        """
        return list(self._tools.values())

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtener definición de una herramienta.
        
        Args:
            name: Nombre de la herramienta.
            
        Returns:
            Definición de la herramienta o None.
        """
        return self._tools.get(name)

    def execute(self, name: str, **kwargs) -> Any:
        """Ejecutar una herramienta registrada.
        
        Args:
            name: Nombre de la herramienta.
            **kwargs: Parámetros para la herramienta.
            
        Returns:
            Resultado de la ejecución.
            
        Raises:
            ValueError: Si la herramienta no existe.
        """
        if name not in self._executors:
            raise ValueError(f"Herramienta '{name}' no registrada")
        
        executor = self._executors[name]
        return executor(**kwargs)

    def parse_and_execute(self, response: str) -> Optional[Any]:
        """Parsear respuesta JSON y ejecutar herramienta.
        
        Args:
            response: Respuesta del LLM en formato JSON.
            
        Returns:
            Resultado de la ejecución o None si no es tool call.
        """
        tool_call = self._parse_tool_call(response)
        
        if not tool_call:
            return None
        
        name = tool_call.get("name")
        params = tool_call.get("parameters", {})
        
        return self.execute(name, **params)

    def _parse_tool_call(self, response: str) -> Optional[Dict[str, Any]]:
        """Parsear llamada a herramienta desde respuesta.
        
        Args:
            response: Respuesta del LLM.
            
        Returns:
            Diccionario con name y parameters, o None.
        """
        try:
            response = response.strip()
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start == -1 or end == 0:
                return None
            
            json_str = response[start:end]
            data = json.loads(json_str)
            
            if "name" in data and "parameters" in data:
                return data
            return None
            
        except (json.JSONDecodeError, ValueError):
            return None

    def to_ollama_format(self) -> List[Dict[str, Any]]:
        """Convertir herramientas a formato Ollama.
        
        Returns:
            Lista de herramientas en formato Ollama API.
        """
        tools = []
        
        for tool_def in self._tools.values():
            ollama_tool = {
                "type": "function",
                "function": {
                    "name": tool_def["name"],
                    "description": tool_def["description"],
                    "parameters": tool_def["parameters"]
                }
            }
            tools.append(ollama_tool)
        
        return tools

    def clear(self) -> None:
        """Limpiar todas las herramientas registradas."""
        self._tools.clear()
        self._executors.clear()


# === Implementaciones de herramientas básicas ===

def search_tool(query: str) -> str:
    """Herramienta de búsqueda (placeholder).
    
    Args:
        query: Término de búsqueda.
        
    Returns:
        Resultados de búsqueda (implementar con API real).
    """
    return f"🔍 Búsqueda realizada: '{query}'\n(Implementar con API de búsqueda)"


def translate_tool(text: str, target_language: str) -> str:
    """Herramienta de traducción (placeholder).
    
    Args:
        text: Texto a traducir.
        target_language: Idioma destino.
        
    Returns:
        Texto traducido (implementar con API real).
    """
    return f"🌐 Traducción a '{target_language}': '{text}'\n(Implementar con API de traducción)"


def weather_tool(city: str) -> str:
    """Herramienta de clima (placeholder).
    
    Args:
        city: Ciudad para consultar.
        
    Returns:
        Información del clima (implementar con API real).
    """
    return f"⛅ Clima en '{city}'\n(Implementar con API de clima)"


def shell_tool(command: str, working_dir: Optional[str] = None) -> str:
    """Herramienta de ejecución shell (segura).
    
    Args:
        command: Comando a ejecutar.
        working_dir: Directorio de trabajo.
        
    Returns:
        Output del comando.
    """
    import subprocess
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nError: {result.stderr}"
        
        return output
        
    except subprocess.TimeoutExpired:
        return "Error: Timeout de 30 segundos excedido"
    except Exception as e:
        return f"Error ejecutando comando: {str(e)}"


def read_file_tool(path: str, max_lines: int = 100) -> str:
    """Herramienta de lectura de archivos.
    
    Args:
        path: Ruta del archivo.
        max_lines: Máximo de líneas a leer.
        
    Returns:
        Contenido del archivo.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    lines.append(f"... ({max_lines} líneas máx)")
                    break
                lines.append(line)
            return "".join(lines)
    except Exception as e:
        return f"Error leyendo archivo: {str(e)}"


def write_file_tool(path: str, content: str, append: bool = False) -> str:
    """Herramienta de escritura de archivos.
    
    Args:
        path: Ruta del archivo.
        content: Contenido a escribir.
        append: Si True, añadir al final.
        
    Returns:
        Confirmación de escritura.
    """
    try:
        mode = "a" if append else "w"
        with open(path, mode, encoding="utf-8") as f:
            f.write(content)
        return f"✅ Archivo escrito: {path}"
    except Exception as e:
        return f"Error escribiendo archivo: {str(e)}"

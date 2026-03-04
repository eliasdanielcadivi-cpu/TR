import requests
import json
import sys
import subprocess
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

class SherlokBrain:
    """Cerebro analítico de Sherlok con soporte multimodelo y streaming de pensamientos."""
    
    def __init__(self, config):
        self.config = config
        self.base_url = "http://localhost:11434/api/generate"
        self.current_model = None

    def _stop_model(self, model_name):
        """Detiene un modelo en Ollama para liberar recursos."""
        try:
            requests.post("http://localhost:11434/api/generate", 
                         json={"model": model_name, "keep_alive": 0})
        except:
            pass

    def analyze(self, context_data, is_python=False, forced_model=None):
        """
        Analiza un programa usando el modelo más apto.
        context_data: Diccionario con info del programa (ayuda, readme, código).
        """
        # Selección de modelo determinista
        target_alias = forced_model if forced_model else "codellama"
        if is_python:
            target_alias = "codellamapy"
        
        model_name = self.config['models']['aliases'].get(target_alias, self.config['models']['default'])
        
        if self.current_model and self.current_model != model_name:
            console.print(f"[dim]🔄 Cambiando modelo: {self.current_model} -> {model_name}[/dim]")
            self._stop_model(self.current_model)
        
        self.current_model = model_name

        # Construcción del Prompt Semántico
        system_prompt = f"""Eres Sherlok, un sub-agente forense del sistema ARES.
TU MISIÓN: Analizar herramientas locales y determinar su utilidad para ARES.
CRITERIOS ARES: {self.config['ares_definition']}
LIMITES: Solo temas técnicos. Si es basura o no relacionado, puntúa bajo.
SALIDA: Debes responder SIEMPRE con un bloque YAML inicial (Front Matter) y luego una descripción Markdown."""

        user_prompt = f"Analiza este programa:
{json.dumps(context_data, indent=2)}"

        payload = {
            "model": model_name,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": True,
            "options": self.config['parameters'].get(target_alias, {})
        }

        # Manejo de streaming y pensamientos
        full_response = ""
        console.print(f"
[bold cyan]🧠 Sherlok pensando ({model_name})...[/bold cyan]")
        
        try:
            response = requests.post(self.base_url, json=payload, stream=True)
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    text = chunk.get("response", "")
                    full_response += text
                    print(text, end="", flush=True) # Salida en vivo
            
            print("
")
            return full_response
        except Exception as e:
            console.print(f"[bold red]❌ Error en inferencia: {e}[/bold red]")
            return None

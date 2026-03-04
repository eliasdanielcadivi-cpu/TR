import requests
import json
import sys
from rich.console import Console
from models import ProgramaAudit
from pydantic import ValidationError

console = Console()

class SherlokBrain:
    """
    🧠 CEREBRO SHERLOK V2.2 (SOLID JSON & AUTO-CORRECT)
    Utiliza Schemas de Pydantic y el parámetro 'format' de Ollama.
    Gestiona memoria efímera por documento.
    """
    
    def __init__(self, config):
        self.config = config
        self.base_url = "http://localhost:11434/api/chat" # Usamos /chat para mantener historial de corrección
        self.current_model = None

    def _stop_model(self, model_name):
        try:
            requests.post("http://localhost:11434/api/generate", 
                         json={"model": model_name, "keep_alive": 0}, timeout=2)
        except:
            pass

    def analyze(self, context_data, is_python=False, forced_model=None):
        """
        Analiza un programa con bucle de auto-corrección.
        """
        target_alias = forced_model if forced_model else "codellama"
        if is_python: target_alias = "codellamapy"
        
        model_name = self.config['models']['aliases'].get(target_alias, self.config['models']['default'])
        
        if self.current_model and self.current_model != model_name:
            self._stop_model(self.current_model)
        self.current_model = model_name

        # --- MEMORIA EFÍMERA: Inicia limpia para cada documento ---
        messages = [
            {
                "role": "system",
                "content": f"Eres Sherlok V2.2. Debes generar un JSON estrictamente válido basado en el esquema proporcionado. No agregues texto extra. Contexto Ares: {self.config['ares_definition']}"
            },
            {
                "role": "user",
                "content": f"ID: {context_data['abs_path']}\nDATA: {json.dumps(context_data)}"
            }
        ]

        max_retries = 3
        for attempt in range(max_retries):
            console.print(f"[dim]🧠 Analizando (Intento {attempt+1}/{max_retries}) con {model_name}...[/dim]")
            
            payload = {
                "model": model_name,
                "messages": messages,
                "stream": False,
                "format": ProgramaAudit.model_json_schema(), # Structured Output!
                "options": {"temperature": 0} # Máximo determinismo
            }

            try:
                response = requests.post(self.base_url, json=payload)
                response.raise_for_status()
                content = response.json()['message']['content']
                
                # --- VALIDACIÓN CON PYDANTIC ---
                try:
                    # Validar y parsear
                    validated_data = ProgramaAudit.model_validate_json(content)
                    return validated_data.model_dump_json(indent=2) # Éxito total
                
                except ValidationError as ve:
                    error_msg = f"Error de validación JSON: {str(ve)}. Por favor, corrige la estructura y reintenta."
                    console.print(f"[bold yellow]⚠️ Fallo de validación. Enviando reporte de error a la IA...[/bold yellow]")
                    
                    # Añadir el error al historial para que la IA corrija
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": error_msg})
                    continue

            except Exception as e:
                console.print(f"[bold red]❌ Error de comunicación con Ollama: {e}[/bold red]")
                break

        return None # Falló tras reintentos

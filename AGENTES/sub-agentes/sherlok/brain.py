import requests
import json
import sys
from rich.console import Console
from models import ProgramaAudit
from pydantic import ValidationError

console = Console()

class SherlokBrain:
    """
    🧠 CEREBRO SHERLOK V2.5 (OPTIMIZED)
    Enfoque en ADN Técnico Industrial. Salida JSON Solid.
    """
    
    def __init__(self, config):
        self.config = config
        self.base_url = "http://localhost:11434/api/chat"
        self.current_model = None

    def _stop_model(self, model_name):
        try:
            requests.post("http://localhost:11434/api/generate", 
                         json={"model": model_name, "keep_alive": 0}, timeout=2)
        except:
            pass

    def analyze(self, context_data, is_python=False, forced_model=None):
        target_alias = forced_model if forced_model else "codellama"
        if is_python: target_alias = "qwenCoderInstruc"
        
        model_name = self.config['models']['aliases'].get(target_alias, self.config['models']['default'])
        
        if self.current_model and self.current_model != model_name:
            self._stop_model(self.current_model)
        self.current_model = model_name

        messages = [
            {
                "role": "system",
                "content": f"Eres Sherlok V2.5. Genera JSON estrictamente válido. ADN Técnico Puro. No texto extra. Contexto Ares: {self.config['ares_definition']}"
            },
            {
                "role": "user",
                "content": f"AUDITA ESTE PROGRAMA (ID: {context_data['abs_path']}):\n{json.dumps(context_data)}"
            }
        ]

        max_retries = 3
        for attempt in range(max_retries):
            console.print(f"[dim]🧠 Auditando (Intento {attempt+1}/{max_retries}) con {model_name}...[/dim]")
            
            payload = {
                "model": model_name,
                "messages": messages,
                "stream": True,
                "format": ProgramaAudit.model_json_schema(),
                "options": {"temperature": 0.1}
            }

            full_content = ""
            try:
                response = requests.post(self.base_url, json=payload, stream=True)
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        text = chunk.get("message", {}).get("content", "")
                        print(text, end="", flush=True)
                        full_content += text
                
                print("\n")

                if not full_content.strip(): continue

                try:
                    validated = ProgramaAudit.model_validate_json(full_content)
                    return validated.model_dump_json(indent=2)
                
                except ValidationError as ve:
                    console.print(f"[bold red]❌ Fallo Estructural:[/bold red] Enviando corrección a la IA...")
                    messages.append({"role": "assistant", "content": full_content})
                    messages.append({"role": "user", "content": f"Tu JSON falló el esquema Pydantic. Errores: {str(ve)}. REGENERA SOLO EL JSON CORREGIDO."})
                    continue

            except Exception as e:
                console.print(f"[bold red]❌ Error Ollama: {e}[/bold red]")
                break

        return None

import requests
import os

class AIEngine:
    """Funcionalidades 1-3: Consultas Ollama, Consultas DeepSeek y Gestión de Plantillas."""
    def __init__(self, config):
        self.config = config

    def ask(self, prompt, model_alias=None):
        model = self.config['ollama']['model']
        if model_alias and 'aliases' in self.config and model_alias in self.config['aliases']:
            model = self.config['aliases'][model_alias]['model']
        
        # Plantilla Gemma
        if "gemma" in model.lower():
            # Usando triple comilla para evitar problemas de escape en f-strings
            prompt = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
            
        url = f"{self.config['ollama']['base_url']}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": False}
        try:
            response = requests.post(url, json=payload, timeout=30)
            return response.json().get('response', "Error: Sin respuesta.")
        except Exception as e:
            return f"Error IA: {e}"

    def ask_deepseek(self, prompt):
        url = f"{self.config['deepseek']['base_url']}/chat/completions"
        api_key = os.getenv(self.config['deepseek']['api_key_env'])
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.config['deepseek']['model'],
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']

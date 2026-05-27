"""GeminiProvider: Wrapper para gemini-cli en la arquitectura ARES.

Usa gemini-cli como un provider de primer nivel.
"""

import subprocess
import json
from typing import List, Dict, Any, Optional
from .base_provider import BaseProvider

class GeminiProvider(BaseProvider):
    """Integración de gemini-cli como provider de ARES."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "gemini"

    def generate(self, prompt: str, **kwargs) -> str:
        """Generar respuesta usando gemini-cli."""
        chat_id = kwargs.get("chat_id")
        yolo = kwargs.get("yolo", True)
        system_instr = kwargs.get("system_instructions")
        
        # Prepend system instructions if provided
        if system_instr:
            prompt = f"{system_instr}\n\n[CONSULTA USUARIO]\n{prompt}"

        cmd = ["gemini"]
        if chat_id is not None:
            cmd.extend(["--resume", str(chat_id)])
        
        if yolo:
            cmd.append("--yolo")
        
        # Flag correcto: -o json
        cmd.extend(["-o", "json"])
        cmd.append(prompt)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            try:
                data = json.loads(result.stdout)
                return data.get("content", data.get("text", result.stdout))
            except:
                return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"ERROR: Fallo en gemini-cli: {e.stderr}"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Modo chat para Gemini (usa el último mensaje como prompt)."""
        if not messages:
            return ""
        
        # gemini-cli maneja su propia persistencia via chat_id
        # Tomamos el último mensaje del usuario como prompt
        prompt = messages[-1]["content"]
        return self.generate(prompt, **kwargs)

    def list_models(self) -> List[str]:
        """Gemini-cli usa modelos cloud gestionados automáticamente."""
        return ["gemini-1.5-flash", "gemini-1.5-pro"]

    def generate_stream(self, prompt: str, **kwargs):
        """Streaming fallback (gemini-cli no soporta streaming crudo via stdout fácilmente)."""
        # Por ahora, emitimos la respuesta completa como un único chunk
        yield self.generate(prompt, **kwargs)

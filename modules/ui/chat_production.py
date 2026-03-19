"""ARES I V66: Motor de Producción de Triple Encapsulación.

HERENCIA:
Llama a las 3 piezas del factory de forma independiente para asegurar
la consistencia con la Maqueta de Referencia.
"""

import sys
import yaml
from pathlib import Path

from .ares_factory import AresFactory
from .user_factory import UserFactory
from modules.ia.ai_engine import AIEngine
from modules.ia.apollo import retrieve, compress_context

PROJECT_ROOT = Path(__file__).parent.parent.parent

class ChatProduction:
    def __init__(self, obj, model="ares:latest", rag_dataset=None, think_mode=False):
        self.obj = obj
        self.model = model
        self.rag_dataset = rag_dataset
        self.think_mode = think_mode
        self.engine = AIEngine(obj.config['ai'], str(obj.base_path))
        
        config_path = PROJECT_ROOT / "config" / "layout_config.yaml"
        with open(config_path, "r") as f:
            self.layout_cfg = yaml.safe_load(f)

    def _stream_output(self, text_gen):
        """Streaming real de tokens (Encapsulación 2 en Producción)."""
        sys.stdout.write("\033[36m") 
        for chunk in text_gen:
            if not chunk: continue
            sys.stdout.write(chunk)
            sys.stdout.flush()
        sys.stdout.write("\033[0m\n")

    def start(self):
        """Loop interactivo basado en la Triple Encapsulación."""
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.write("\033[1;35m🛰️  ARES I: PROTOCOLO DE INDEPENDENCIA TOTAL ACTIVO\033[0m\n")

        while True:
            try:
                # 1. BLOQUE USUARIO
                UserFactory.render_header_flow(self.layout_cfg) # Pieza 1
                user_input = input("\033[1;32muser:\033[0m ").strip()
                if user_input.lower() in ("exit", "quit", "/exit"): break
                if not user_input: continue
                UserFactory.render_footer_flow(self.layout_cfg) # Pieza 3 (Opcional, pero para consistencia)

                # 2. PROCESAMIENTO
                context = ""
                if self.rag_dataset:
                    results = retrieve(user_input, k=5, dataset=self.rag_dataset)
                    chunks = results.get("semantic", [])
                    if chunks: context = compress_context(chunks, user_input)

                # 3. BLOQUE IA
                AresFactory.render_header_flow(self.layout_cfg) # Pieza 1
                
                # Pieza 2: Streaming Real (Sustituye al placeholder)
                text_stream = self.engine.ask_stream(
                    user_input, 
                    model_alias=self.model,
                    filter_think=not self.think_mode,
                    context=context if context else None
                )
                self._stream_output(text_stream)

                AresFactory.render_footer_flow(self.layout_cfg) # Pieza 3

            except KeyboardInterrupt: break
            except Exception as e:
                sys.stdout.write(f"\n\033[31mError: {str(e)}\033[0m\n")
                break

def start_production_chat(obj, rag=None, model="ares:latest", think=False):
    chat = ChatProduction(obj, model=model, rag_dataset=rag, think_mode=think)
    chat.start()

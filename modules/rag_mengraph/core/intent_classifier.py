import logging
from typing import Dict, Any
from modules.ia.ai_engine import AIEngine

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Intent")

class IntentClassifier:
    def __init__(self, ai_engine: AIEngine):
        """
        Clasifica las preguntas del usuario según el estándar Memgraph.
        """
        self.ai = ai_engine

    def classify(self, user_question: str) -> Dict[str, str]:
        """
        Determina si la pregunta es Retrieval, Structure, Global o Database.
        """
        prompt = f"""
        Classify the following user question into a query type:

        Query Types:
        - Retrieval: Direct lookups, specific entities.
        - Structure: exploratory, seeks connections or neighborhood info.
        - Global: Seeks context about the entire graph or trends.
        - Database: Seeks statistical info about indexes, counts, etc.

        USER QUESTION: "{user_question}"

        Return ONLY a JSON object:
        {{
            "type": "Retrieval|Structure|Global|Database",
            "explanation": "Why you chose this type"
        }}
        """

        try:
            response = self.ai.ask(prompt, model_alias="ares", template="default")
            
            # Limpieza de JSON
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            import json
            data = json.loads(response)
            logger.info(f"Intención detectada: {data['type']}")
            return data
            
        except Exception as e:
            logger.error(f"Error clasificando intención: {e}")
            return {"type": "Retrieval", "explanation": "Fallback por error"}

if __name__ == "__main__":
    print("--- Clasificador de Intención ARES listo ---")

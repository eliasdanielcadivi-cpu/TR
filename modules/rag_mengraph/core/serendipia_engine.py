import logging
import json
from typing import List, Dict, Any
from modules.ia.ai_engine import AIEngine
from modules.rag_mengraph.core.schema_weaver import SchemaWeaver

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Serendipia")

class SerendipiaEngine:
    def __init__(self, ai_engine: AIEngine, schema_weaver: SchemaWeaver):
        """
        Inicializa el motor de descubrimiento de relaciones.
        """
        self.ai = ai_engine
        self.weaver = schema_weaver

    def infer_relationships(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Infiere relaciones (Verbos) entre entidades detectadas basándose en el texto.
        """
        if len(entities) < 2:
            logger.debug("Insuficientes entidades para inferir relaciones.")
            return []

        # 1. Obtener etiquetas detectadas
        labels = list(set([e['label'] for e in entities]))
        
        # 2. Obtener Micro-RAG de esquema
        allowed_schema = ""
        if self.weaver:
            allowed_schema = self.weaver.get_allowed_schema(labels)
        
        # 3. Construir Prompt de Inferencia
        system_prompt = f"""
Eres el 'Tejedor Lógico' del sistema ARES-TRON. Tu misión es descubrir las relaciones físicas (Verbos) entre las entidades detectadas en un texto.

{allowed_schema}

INSTRUCCIONES:
1. Analiza el texto y las entidades proporcionadas.
2. Identifica cómo se conectan las entidades usando los Verbos del esquema anterior.
3. Si detectas una conexión valiosa que NO está en el esquema (Serendipia), propón un Verbo nuevo descriptivo.
4. Para cada relación, asigna una confianza (0.0 a 1.0).
5. Devuelve EXCLUSIVAMENTE un objeto JSON con la lista de relaciones.

FORMATO DE SALIDA:
{{
  "relaciones": [
    {{
      "origen": "Texto de la entidad origen",
      "label_origen": "Label de origen",
      "verbo": "NOMBRE_DEL_VERBO",
      "destino": "Texto de la entidad destino",
      "label_destino": "Label de destino",
      "confianza": 0.95,
      "razonamiento": "Breve explicación"
    }}
  ]
}}
"""

        user_prompt = f"""
TEXTO: "{text}"

ENTIDADES DETECTADAS:
{json.dumps(entities, indent=2, ensure_ascii=False)}

Extrae las relaciones ahora:
"""

        try:
            logger.debug("Consultando al Navegador Semántico para inferencia...")
            response_text = self.ai.ask(user_prompt, model_alias="ares", template="default", system_instructions=system_prompt)
            
            # Limpiar respuesta para parsear JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(response_text)
            relaciones = data.get("relaciones", [])
            logger.info(f"Inferencia completada: {len(relaciones)} relaciones descubiertas.")
            return relaciones
            
        except Exception as e:
            logger.error(f"Error en la inferencia de serendipia: {e}")
            return []

if __name__ == "__main__":
    print("--- Motor de Serendipia Restaurado ---")

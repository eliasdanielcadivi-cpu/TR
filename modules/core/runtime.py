"""
ARES Runtime Engine v0.1.
Orquestador de ejecución híbrida (Cypher + LLM + Python).
Resiliencia Industrial (7-Fails): Fallback a archivos locales si el Grafo falla.
"""
from neo4j import GraphDatabase
import yaml
import os

class AresRuntime:
    def __init__(self, uri="bolt://localhost:7687"):
        self.uri = uri
        self.driver = None
        self.is_graph_active = False
        try:
            # Timeout corto para no colgar el sistema
            self.driver = GraphDatabase.driver(uri, auth=("", ""), connection_timeout=2)
            self.driver.verify_connectivity()
            self.is_graph_active = True
        except:
            print("⚠️ Memgraph inactivo. Activando Fallback a 'config/identidad/ares.yaml'.")

    def execute_phase(self, phase_data: dict, context: dict = None):
        """Ejecuta una fase completa del DSL."""
        print(f"🚀 Ejecutando Fase: {phase_data.get('id', 'unknown')}")
        results = {}
        
        for step in phase_data.get("steps", []):
            step_id = step.get("id")
            step_type = step.get("type")
            
            if step_type == "cypher":
                if self.is_graph_active:
                    results[step_id] = self._run_cypher(step.get("query"), context)
                else:
                    results[step_id] = self._run_fallback(step_id, context)
            
            elif step_type == "llm":
                results[step_id] = self._run_llm(step.get("prompt"), results.get("query_grafo") or context)
        
        return results

    def _run_cypher(self, query: str, context: dict):
        """Ejecutor nativo de Cypher."""
        with self.driver.session() as session:
            if context:
                for k, v in context.items():
                    query = query.replace(f"${k}", str(v))
            result = session.run(query)
            return [record.data() for record in result]

    def _run_fallback(self, step_id: str, context: dict):
        """Recuperación determinista desde archivos locales."""
        fallback_path = "config/identidad/ares.yaml"
        if not os.path.exists(fallback_path):
            return [{"principio": "Atomicidad Paranoica (Default)"}]
        
        with open(fallback_path, "r") as f:
            data = yaml.safe_load(f)
            # Simular respuesta de grafo basada en el YAML
            return data.get("principios", [{"principio": "Resiliencia Local"}])

    def _run_llm(self, prompt: str, context: any):
        """Inferencia con contexto inyectado (Modo YOLO forzado)."""
        from modules.ia.gemini_wrapper import invoke_chat
        full_prompt = prompt
        if context:
            full_prompt += f"\n\nCONTEXTO RECUPERADO: {context}"
        
        # Forzar yolo=True para evitar colgar el runtime
        return invoke_chat(full_prompt, yolo=True)

    def close(self):
        if self.driver:
            self.driver.close()

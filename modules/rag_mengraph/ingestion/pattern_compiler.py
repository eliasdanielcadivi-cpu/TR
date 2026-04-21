import json
import os
from typing import List, Dict

def compile_ontology_to_spacy(ontology_path: str) -> List[Dict]:
    """
    Lee el JSON Master y genera una lista de patrones para EntityRuler.
    Cada patrón incluye un ID compuesto: DOMINIO|SUB_ID
    """
    if not os.path.exists(ontology_path):
        raise FileNotFoundError(f"Ontología no encontrada en: {ontology_path}")
        
    with open(ontology_path, 'r', encoding='utf-8') as f:
        ontology = json.load(f)
        
    dominio = ontology.get("dominio_operativo", "DEFAULT_DOMAIN")
    patterns = []
    
    for label, info in ontology.get("sustantivos", {}).items():
        instancias = info.get("instancias", [])
        for inst in instancias:
            pattern_text = inst.get("pattern")
            sub_id = inst.get("id", "CORE")
            
            # El ID compuesto: Caballo de Troya
            composite_id = f"{dominio}|{sub_id}"
            
            patterns.append({
                "label": label,
                "pattern": pattern_text,
                "id": composite_id
            })
            
    return patterns

if __name__ == "__main__":
    # Prueba rápida del compilador
    ONTOLOGY_FILE = "/home/daniel/tron/programas/TR/config/rag_mengraph/ontology_master.json"
    try:
        compiled_patterns = compile_ontology_to_spacy(ONTOLOGY_FILE)
        print(f"✅ Compilación exitosa. {len(compiled_patterns)} patrones generados.")
        for p in compiled_patterns[:3]:
            print(f"  - Label: {p['label']}, Pattern: {p['pattern']}, ID: {p['id']}")
    except Exception as e:
        print(f"❌ Error en compilación: {e}")

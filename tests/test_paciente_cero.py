import sys
import os
sys.path.append("/home/daniel/tron/programas/TR")

from modules.rag_mengraph.ingestion.spacy_engine import SpacyEngine

ONTOLOGY = "/home/daniel/tron/programas/TR/config/rag_mengraph/ontology_master.json"
engine = SpacyEngine(ONTOLOGY)

test_texts = [
    "Daniel es el Paciente Cero que evoluciona hacia un Agente Publicador.",
    "El sistema reconoce a Daniel como el Operador Maestro."
]

print("\n--- 🧪 TEST DE IDENTIDAD: PACIENTE CERO ---")
for res in engine.process_stream(test_texts):
    print(f"\nDocumento: {res['text']}")
    if not res['entities']:
        print("  [!] No se detectaron entidades. Revisa los patrones.")
    for e in res['entities']:
        print(f"  -> ENTIDAD: {e['text']} | ETIQUETA: {e['label']} | ID: {e['id']}")


import sys
import os

# Añadir raíz del proyecto al path
project_root = "/home/daniel/tron/programas/TR"
sys.path.insert(0, project_root)

from modules.rag.ingestion.file_reader import read_text_file, generate_doc_id
from modules.rag.ingestion.chunker import split_into_chunks
from modules.rag.ingestion.entity_extractor import extract_entities_basic

test_file = "/home/daniel/tron/programas/TR/docs/ArquitecturadeModulosOrientadaaIA/ArquitecturadeMódulosOrientadaaIA.md"

def test_ingestion_atomic_flow():
    print("🧪 Probando Flujo Atómico de Ingesta...")
    
    # 1. Reader
    content = read_text_file(test_file)
    if not content:
        print("❌ Fallo en ingestion/file_reader")
        return
    doc_id = generate_doc_id(test_file, content)
    print(f"✅ Archivo leído. ID: {doc_id} (Longitud: {len(content)})")

    # 2. Chunker
    chunks = split_into_chunks(content, chunk_size=500, overlap=50)
    print(f"📊 Fragmentos creados: {len(chunks)}")
    
    # 3. Entity Extractor
    entities = extract_entities_basic(content)
    print(f"🔍 Entidades extraídas: {len(entities)}")
    for ent in entities[:5]:
        print(f"  - [{ent['type']}] {ent['name']}")

if __name__ == "__main__":
    test_ingestion_atomic_flow()

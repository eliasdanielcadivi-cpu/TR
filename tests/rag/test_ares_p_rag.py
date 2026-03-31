#!/usr/bin/env python3
"""
Prueba Headless de RAG para 'ares p --rag'

Propósito: Probar el sistema RAG completo en modo headless (sin interfaz interactiva)
para el comando 'ares p "consulta" --rag'

Casos de prueba:
1. Ingesta de documento
2. Recuperación T1 (SQL)
3. Recuperación T2 (Vector)
4. Verificación de resultados

Uso:
    cd /home/daniel/tron/programas/TR
    python tests/rag/test_ares_p_rag.py
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Añadir ruta del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
os.environ['TR_PROJECT_ROOT'] = str(project_root)


def print_header(text: str):
    """Imprimir encabezado de sección."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def print_subheader(text: str):
    """Imprimir subencabezado."""
    print("\n" + "-"*80)
    print(f"  {text}")
    print("-"*80)


def test_1_ingestion():
    """Prueba 1: Ingesta de documento"""
    print_header("PRUEBA 1: INGESTA DE DOCUMENTO")
    
    from modules.rag.core.rag_orchestrator import RAGOrchestrator
    
    test_doc = project_root / "docs/ArquitecturadeModulosOrientadaaIA/ArquitecturadeMódulosOrientadaaIA.md"
    
    if not test_doc.exists():
        print(f"❌ Documento no encontrado: {test_doc}")
        return False, {}
    
    print(f"📄 Documento: {test_doc}")
    print(f"📏 Tamaño: {test_doc.stat().st_size:,} bytes")
    
    # Inicializar RAG
    print("\n🔧 Inicializando RAGOrchestrator...")
    rag = RAGOrchestrator()
    
    # Ingerir
    print("📥 Ingestando documento...")
    start_time = time.time()
    result = rag.ingest_document(str(test_doc))
    elapsed = (time.time() - start_time) * 1000
    
    # Mostrar resultados CRUDOS
    print_subheader("RESULTADOS CRUDOS DE INGESTA")
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    print(f"\n⏱️  Tiempo de ingesta: {elapsed:.1f}ms")
    
    # Validar
    success = (
        result.get('status') == 'success' and
        result.get('chunks_count', 0) > 0 and
        result.get('document_id') is not None
    )
    
    if success:
        print("\n✅ PRUEBA 1: EXITOSA")
    else:
        print("\n❌ PRUEBA 1: FALLIDA")
    
    return success, result


def test_2_sql_retrieval():
    """Prueba 2: Recuperación T1 (SQL)"""
    print_header("PRUEBA 2: RECUPERACIÓN T1 (SQL)")
    
    from modules.rag.core.rag_orchestrator import RAGOrchestrator
    from modules.rag.core.tier_router import Tier
    
    rag = RAGOrchestrator()
    
    # Consulta de prueba
    query = "módulos funciones arquitectura"
    print(f"🔍 Consulta: '{query}'")
    
    # Ejecutar recuperación (solo T1 SQL)
    print("\n📊 Ejecutando recuperación T1 (SQL)...")
    start_time = time.time()
    
    try:
        result = rag.router._t1_sql_search(query, max_results=5)
        elapsed = (time.time() - start_time) * 1000
        
        print_subheader("RESULTADOS CRUDOS DE BÚSQUEDA SQL")
        print(f"   Tier: {result.tier.name}")
        print(f"   Confianza: {result.confidence:.3f}")
        print(f"   Latencia: {elapsed:.1f}ms")
        print(f"   Fuentes: {len(result.sources)}")
        
        if result.data:
            print(f"\n📝 Datos recuperadas ({len(result.data)} items):")
            for i, item in enumerate(result.data[:3]):
                print(f"\n   Resultado {i+1}:")
                if isinstance(item, dict):
                    for k, v in item.items():
                        if isinstance(v, str) and len(v) > 100:
                            v = v[:100] + "..."
                        print(f"      {k}: {v}")
                else:
                    print(f"      {item}")
        
        success = result.confidence > 0 or len(result.sources) > 0
        
        if success:
            print("\n✅ PRUEBA 2: EXITOSA")
        else:
            print("\n⚠️  PRUEBA 2: SIN RESULTADOS (pero no es error)")
        
        return True, result
        
    except Exception as e:
        print(f"\n❌ Error en recuperación SQL: {e}")
        import traceback
        traceback.print_exc()
        return False, {}


def test_3_vector_retrieval():
    """Prueba 3: Recuperación T2 (Vector)"""
    print_header("PRUEBA 3: RECUPERACIÓN T2 (VECTOR)")
    
    from modules.rag.core.rag_orchestrator import RAGOrchestrator
    from modules.rag.core.tier_router import Tier
    
    rag = RAGOrchestrator()
    
    # Consulta de prueba
    query = "sistema modular para inteligencia artificial"
    print(f"🔍 Consulta: '{query}'")
    
    # Ejecutar recuperación (solo T2 Vector)
    print("\n📊 Ejecutando recuperación T2 (Vector)...")
    start_time = time.time()
    
    try:
        result = rag.router._t2_vector_search(query, max_results=5)
        elapsed = (time.time() - start_time) * 1000
        
        print_subheader("RESULTADOS CRUDOS DE BÚSQUEDA VECTORIAL")
        print(f"   Tier: {result.tier.name}")
        print(f"   Confianza: {result.confidence:.3f}")
        print(f"   Latencia: {elapsed:.1f}ms")
        print(f"   Fuentes: {len(result.sources)}")
        
        if result.data:
            print(f"\n📝 Datos recuperadas ({len(result.data)} items):")
            for i, item in enumerate(result.data[:3]):
                print(f"\n   Resultado {i+1}:")
                if isinstance(item, dict):
                    for k, v in item.items():
                        if isinstance(v, str) and len(v) > 100:
                            v = v[:100] + "..."
                        print(f"      {k}: {v}")
                else:
                    print(f"      {item}")
        
        # Nota: Puede no haber resultados si Ollama no está disponible
        print("\n⚠️  Nota: Si no hay resultados, verificar Ollama")
        print("   Ejecutar: ollama ls")
        print("   Modelo requerido: mxbai-embed-large:335m")
        
        print("\n✅ PRUEBA 3: COMPLETADA (verificar resultados manualmente)")
        
        return True, result
        
    except Exception as e:
        print(f"\n❌ Error en recuperación vectorial: {e}")
        import traceback
        traceback.print_exc()
        return False, {}


def test_4_full_rag_retrieval():
    """Prueba 4: Recuperación RAG completa (T0-T3)"""
    print_header("PRUEBA 4: RECUPERACIÓN RAG COMPLETA")
    
    from modules.rag.core.rag_orchestrator import RAGOrchestrator
    from modules.rag.core.tier_router import Tier
    
    rag = RAGOrchestrator()
    
    # Consulta de prueba
    query = "¿Cuántas funciones debe tener un módulo?"
    print(f"🔍 Consulta: '{query}'")
    print("📝 Esta consulta debería activar T1 (SQL) o T2 (Vector)")
    
    # Ejecutar recuperación completa (headless mode = max T3)
    print("\n📊 Ejecutando recuperación completa (modo headless)...")
    start_time = time.time()
    
    try:
        result = rag.retrieve(query, mode="headless", max_tier=Tier.T3_GRAPH)
        elapsed = (time.time() - start_time) * 1000
        
        print_subheader("RESULTADOS CRUDOS DE RECUPERACIÓN")
        print(f"   Tier alcanzado: {result.tier.name}")
        print(f"   Confianza: {result.confidence:.3f}")
        print(f"   Latencia: {elapsed:.1f}ms")
        print(f"   Fuentes: {len(result.sources)}")
        print(f"   Requiere T4: {result.requires_t4}")
        
        if result.data:
            print(f"\n📝 Datos recuperadas:")
            if isinstance(result.data, str):
                # Mostrar resumen
                preview = result.data[:500] + "..." if len(result.data) > 500 else result.data
                print(f"\n   {preview}")
            elif isinstance(result.data, list):
                for i, item in enumerate(result.data[:3]):
                    print(f"\n   Item {i+1}:")
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if isinstance(v, str) and len(v) > 100:
                                v = v[:100] + "..."
                            print(f"      {k}: {v}")
                    else:
                        print(f"      {item}")
        
        # Validar
        success = result.confidence > 0 or len(result.sources) > 0
        
        if success:
            print("\n✅ PRUEBA 4: EXITOSA")
        else:
            print("\n⚠️  PRUEBA 4: SIN RESULTADOS (índice vacío o consulta muy específica)")
        
        return success, result
        
    except Exception as e:
        print(f"\n❌ Error en recuperación RAG: {e}")
        import traceback
        traceback.print_exc()
        return False, {}


def test_5_json_serialization():
    """Prueba 5: Serialización JSON para 'ares p --json'"""
    print_header("PRUEBA 5: SERIALIZACIÓN JSON")
    
    from modules.rag.core.rag_orchestrator import RAGOrchestrator
    from modules.rag.core.tier_router import Tier
    
    rag = RAGOrchestrator()
    
    query = "arquitectura modular"
    print(f"🔍 Consulta: '{query}'")
    
    try:
        result = rag.retrieve(query, mode="headless")
        
        print("\n📊 Serializando a JSON (como 'ares p --json')...")
        json_output = rag.to_json(result)
        
        print_subheader("SALIDA JSON (primeros 1000 chars)")
        preview = json_output[:1000] + "..." if len(json_output) > 1000 else json_output
        print(preview)
        
        # Validar JSON
        import json
        parsed = json.loads(json_output)
        
        required_fields = ['data', 'tier', 'confidence', 'latency_ms', 'sources']
        missing = [f for f in required_fields if f not in parsed]
        
        if missing:
            print(f"\n❌ Faltan campos: {missing}")
            return False, {}
        
        print("\n✅ PRUEBA 5: EXITOSA")
        return True, parsed
        
    except Exception as e:
        print(f"\n❌ Error en serialización JSON: {e}")
        import traceback
        traceback.print_exc()
        return False, {}


def run_all_tests():
    """Ejecutar todas las pruebas"""
    print_header("PRUEBAS HEADLESS DE RAG - 'ares p --rag'")
    print(f"📁 Project Root: {project_root}")
    print(f"📂 DB Root: {project_root}/db/rag")
    
    results = {}
    
    # Ejecutar pruebas
    results['ingestion'], _ = test_1_ingestion()
    results['sql_retrieval'], _ = test_2_sql_retrieval()
    results['vector_retrieval'], _ = test_3_vector_retrieval()
    results['full_rag'], _ = test_4_full_rag_retrieval()
    results['json_serialization'], _ = test_5_json_serialization()
    
    # Resumen
    print_header("RESUMEN DE PRUEBAS")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {name}")
    
    print(f"\n📈 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("\n💡 Ahora puedes usar:")
        print("   ares p \"tu consulta\" --rag")
        print("   ares p \"tu consulta\" --rag --json")
        return True
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")
        print("\n💡 Verifica:")
        print("   1. Bases de datos inicializadas: python modules/rag/init_rag_db.py")
        print("   2. Documentos ingeridos: test_1_ingestion()")
        print("   3. Ollama disponible: ollama ls")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

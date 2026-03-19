#!/usr/bin/env python3
"""
Script para verificar la estructura de la base de datos y los modelos almacenados
"""

import sys
import asyncio
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def check_db_structure():
    """Verifica la estructura de la base de datos"""
    try:
        from tron_lib import TronDBManager
        import yaml
        
        # Cargar configuración
        config_path = Path("/home/daniel/tron/programas/ProyectoPizza/TRON/bin/tron_config.yaml")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Conectar a la base de datos
        db_manager = TronDBManager()
        user = config['keys'].get('pocketbase_user')
        password = config['keys'].get('pocketbase_pass')
        
        if not user or not password:
            print("❌ Credenciales de PocketBase no encontradas en la configuración")
            return False
        
        connected = await db_manager.connect(user, password)
        if not connected:
            print("❌ No se pudo conectar a la base de datos")
            return False
        
        print("🔍 Verificando estructura de la base de datos...")
        
        # Verificar colecciones
        try:
            collections = await db_manager.client.collections.get_full_list()
            print(f"📋 Colecciones encontradas: {len(collections)}")
            for collection in collections:
                print(f"   - {collection.name}")
        except Exception as e:
            print(f"❌ Error al leer colecciones: {e}")
            return False
        
        # Verificar la estructura de la colección openrouter_models
        try:
            model_collection = await db_manager.client.collections.get_one("openrouter_models")
            print(f"\n📋 Estructura de la colección 'openrouter_models':")
            if hasattr(model_collection, 'schema'):
                for field in model_collection.schema:
                    print(f"   - {field.name}: {field.type} (required: {field.required}, unique: {field.unique})")
            else:
                print("   - No se pudo acceder al esquema")
        except Exception as e:
            print(f"❌ Error al leer estructura de openrouter_models: {e}")
        
        # Verificar algunos registros de ejemplo
        try:
            all_models = await db_manager.client.collection("openrouter_models").get_full_list()
            print(f"\n📊 Total de modelos en la base de datos: {len(all_models)}")
            
            if all_models:
                print("\n📝 Estructura de un modelo de ejemplo:")
                sample_model = all_models[0]  # Tomar el primer modelo como ejemplo
                print(f"   Tipo de objeto: {type(sample_model)}")
                
                # Verificar si es un diccionario o un objeto
                if hasattr(sample_model, '__dict__'):
                    print(f"   Atributos: {list(sample_model.__dict__.keys())}")
                elif isinstance(sample_model, dict):
                    print(f"   Claves: {list(sample_model.keys())}")
                    print(f"   Contenido completo: {sample_model}")
                else:
                    print(f"   Contenido: {sample_model}")
                    
                # Verificar si tiene los campos esperados
                expected_fields = ['model_id', 'name', 'price_prompt', 'price_completion', 'context_length']
                if isinstance(sample_model, dict):
                    missing_fields = [field for field in expected_fields if field not in sample_model]
                    if missing_fields:
                        print(f"   ⚠️  Campos faltantes: {missing_fields}")
                    else:
                        print(f"   ✅ Todos los campos esperados están presentes")
                        print(f"   Model ID: {sample_model.get('model_id', 'N/A')}")
                        print(f"   Price Prompt: {sample_model.get('price_prompt', 'N/A')}")
                        print(f"   Price Completion: {sample_model.get('price_completion', 'N/A')}")
                else:
                    print(f"   ⚠️  El modelo no es un diccionario, puede haber un problema de estructura")
                    
        except Exception as e:
            print(f"❌ Error al leer modelos: {e}")
            import traceback
            traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar estructura de base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔍 Verificación de la estructura de la base de datos")
    print("=" * 60)
    
    success = await check_db_structure()
    
    if success:
        print("\n✅ Verificación de estructura completada")
    else:
        print("\n❌ Hubo un problema al verificar la estructura de la base de datos")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Script para probar directamente la creación de modelos en la base de datos
"""

import sys
import asyncio
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def test_model_creation():
    """Prueba directa de creación de modelos en la base de datos"""
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
        
        print("🔍 Probando creación de modelo de ejemplo...")
        
        # Datos de ejemplo para crear un modelo
        test_model_data = {
            "model_id": "test-model-creation",
            "name": "Test Model for Creation Verification",
            "context_length": 32768,
            "price_prompt": 0.0,
            "price_completion": 0.0,
            "last_failure": 0,
            "failure_count": 0
        }
        
        try:
            # Intentar crear el modelo
            print(f"   Creando modelo de prueba...")
            created_model = await db_manager.client.collection("openrouter_models").create(test_model_data)
            
            print(f"   ✅ Modelo creado exitosamente")
            print(f"   Tipo de objeto: {type(created_model)}")

            # Verificar qué campos tiene el modelo creado
            if isinstance(created_model, dict):
                print(f"   Claves del modelo: {list(created_model.keys())}")
                print(f"   ID del modelo creado: {created_model.get('id', 'N/A')}")
                print(f"   Contenido completo: {created_model}")
            elif hasattr(created_model, '__dict__'):
                print(f"   Atributos del modelo: {list(created_model.__dict__.keys())}")
                print(f"   ID del modelo creado: {getattr(created_model, 'id', 'N/A')}")
            else:
                print(f"   Contenido: {created_model}")
                
        except Exception as e:
            print(f"   ❌ Error al crear modelo: {e}")
            import traceback
            traceback.print_exc()
        
        # Ahora intentar leer el modelo recién creado
        print(f"\n🔍 Leyendo modelo recién creado...")
        try:
            # Obtener todos los modelos y buscar el que acabamos de crear
            all_models = await db_manager.client.collection("openrouter_models").get_full_list()
            test_models = [m for m in all_models if m.get('model_id') == 'test-model-creation']
            
            if test_models:
                test_model = test_models[0]
                print(f"   ✅ Modelo encontrado en la base de datos")
                print(f"   Tipo de objeto: {type(test_model)}")
                
                if isinstance(test_model, dict):
                    print(f"   Claves del modelo: {list(test_model.keys())}")
                    print(f"   Contenido: {test_model}")
                    
                    # Verificar si tiene los campos esperados
                    expected_fields = ['model_id', 'name', 'price_prompt', 'price_completion', 'context_length']
                    missing_fields = [field for field in expected_fields if field not in test_model]
                    
                    if missing_fields:
                        print(f"   ⚠️  Campos faltantes: {missing_fields}")
                        print(f"   ❌ La estructura de los modelos guardados es incorrecta")
                    else:
                        print(f"   ✅ Todos los campos esperados están presentes")
                else:
                    print(f"   ⚠️  El modelo no es un diccionario: {test_model}")
            else:
                print(f"   ❌ No se encontró el modelo de prueba en la base de datos")
                
        except Exception as e:
            print(f"   ❌ Error al leer modelo: {e}")
            import traceback
            traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al probar creación de modelos: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔍 Prueba de creación de modelos en la base de datos")
    print("=" * 60)
    
    success = await test_model_creation()
    
    if success:
        print("\n✅ Prueba de creación completada")
    else:
        print("\n❌ Hubo un problema al probar la creación de modelos")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
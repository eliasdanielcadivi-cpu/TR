#!/usr/bin/env python3
"""
Script para eliminar y recrear la colección openrouter_models con el esquema correcto
"""

import sys
import asyncio
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def recreate_openrouter_models_collection():
    """Elimina y recrea la colección openrouter_models con el esquema correcto"""
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
        
        print("🔍 Eliminando y recreando la colección 'openrouter_models'...")
        
        try:
            # Eliminar la colección existente
            try:
                await db_manager.client.collections.delete("openrouter_models")
                print("✅ Colección 'openrouter_models' eliminada")
            except Exception as e:
                print(f"⚠️  No se pudo eliminar la colección (posiblemente no existía): {e}")
            
            # Definir el esquema correcto
            schema = [
                {"name": "model_id", "type": "text", "required": True, "unique": True},
                {"name": "name", "type": "text"},
                {"name": "context_length", "type": "number"},
                {"name": "price_prompt", "type": "number"},
                {"name": "price_completion", "type": "number"},
                {"name": "last_failure", "type": "number"},
                {"name": "failure_count", "type": "number", "options": {"min": 0}},
            ]
            
            # Crear la colección con el esquema correcto
            await db_manager.client.collections.create({
                "name": "openrouter_models",
                "type": "base",
                "schema": schema,
                "listRule": None, "viewRule": None,
                "createRule": None, "updateRule": None, "deleteRule": None
            })
            
            print("✅ Colección 'openrouter_models' creada con el esquema correcto")
            
            # Verificar que la colección se haya creado correctamente
            collection = await db_manager.client.collections.get_one("openrouter_models")
            if isinstance(collection, dict):
                collection_schema = collection.get('schema', [])
                print(f"✅ Esquema verificado: {len(collection_schema)} campos definidos")
                for field in collection_schema:
                    if isinstance(field, dict):
                        print(f"   - {field.get('name', 'unknown')}: {field.get('type', 'unknown')}")
            else:
                print("⚠️  No se pudo verificar el esquema de la colección")
            
            # Limpiar registros existentes en la tabla (si hay alguno)
            try:
                existing_records = await db_manager.client.collection("openrouter_models").get_full_list()
                print(f"ℹ️  Encontrados {len(existing_records)} registros existentes en la tabla")
                
                # Eliminar todos los registros existentes
                for record in existing_records:
                    if isinstance(record, dict):
                        record_id = record.get('id')
                        if record_id:
                            await db_manager.client.collection("openrouter_models").delete(record_id)
                    elif hasattr(record, 'id'):
                        await db_manager.client.collection("openrouter_models").delete(record.id)
                
                print(f"✅ {len(existing_records)} registros antiguos eliminados")
                
            except Exception as e:
                print(f"⚠️  Error al limpiar registros existentes: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al recrear la colección: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Error al recrear la colección openrouter_models: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔧 Eliminación y recreación de la colección openrouter_models")
    print("=" * 60)
    
    success = await recreate_openrouter_models_collection()
    
    if success:
        print("\n✅ Recreación de colección completada exitosamente")
        print("   Ahora puedes volver a ejecutar la sincronización de modelos")
    else:
        print("\n❌ Hubo un problema al recrear la colección")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
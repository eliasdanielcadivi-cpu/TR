#!/usr/bin/env python3
"""
Script para verificar y corregir la estructura de la base de datos de TRON
"""

import asyncio
import sys
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def verify_and_fix_metadata():
    """Verifica y corrige la estructura de la base de datos"""
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
        collections = await db_manager.client.collections.get_full_list()
        print(f"📋 Colecciones encontradas: {len(collections)}")
        for coll in collections:
            print(f"   • {coll.name}")
        
        # Verificar registros en metadata
        try:
            metadata_records = await db_manager.client.collection("metadata").get_full_list()
            print(f"\n📋 Registros en metadata: {len(metadata_records)}")
            for record in metadata_records:
                print(f"   • ID: {getattr(record, 'id', 'N/A')}, Key: {getattr(record, 'key', 'N/A')}")
        except Exception as e:
            print(f"⚠️  Error al leer registros de metadata: {e}")
        
        # Crear el registro de actualización si no existe
        try:
            records = await db_manager.client.collection("metadata").get_full_list()
            existing_records = [record for record in records if getattr(record, 'key', '') == 'last_update']
            
            if not existing_records:
                print("\n🔧 Creando registro de actualización...")
                await db_manager.client.collection("metadata").create({
                    "key": "last_update", 
                    "value": {"timestamp": 0}
                })
                print("✅ Registro de actualización creado")
            else:
                print("\n✅ Registro de actualización ya existe")
        except Exception as e:
            print(f"❌ Error al crear registro de actualización: {e}")
        
        # Verificar modelos en openrouter_models
        try:
            models = await db_manager.client.collection("openrouter_models").get_full_list()
            print(f"\n📋 Modelos en openrouter_models: {len(models)}")
        except Exception as e:
            print(f"⚠️  Error al leer modelos: {e}")
        
        # Verificar logs de ejecución
        try:
            logs = await db_manager.client.collection("execution_logs").get_full_list()
            print(f"\n📋 Logs de ejecución: {len(logs)}")
        except Exception as e:
            print(f"⚠️  Error al leer logs de ejecución: {e}")
        
        print("\n✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔧 Verificación y corrección de la base de datos de TRON")
    print("=" * 50)
    
    success = await verify_and_fix_metadata()
    
    if success:
        print("\n🎉 ¡La base de datos ha sido verificada y corregida!")
    else:
        print("\n❌ Hubo un problema al verificar la base de datos.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Script para probar el acceso a registros de metadata con to_dict()
"""

import asyncio
import sys
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def test_record_access():
    """Prueba diferentes formas de acceder a los registros"""
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
        
        print("🔍 Probando diferentes formas de acceder a los registros...")
        
        # Obtener todos los registros en metadata
        try:
            metadata_records = await db_manager.client.collection("metadata").get_full_list()
            print(f"\n📋 Total de registros en metadata: {len(metadata_records)}")
            
            for i, record in enumerate(metadata_records):
                print(f"\nRegistro {i+1}:")
                
                # Intentar usar to_dict()
                try:
                    record_dict = record.to_dict()
                    print(f"   to_dict(): {record_dict}")
                    
                    # Verificar si tiene los campos que buscamos
                    key_value = record_dict.get('key', 'NO KEY')
                    print(f"   Campo 'key': {key_value}")
                    
                    if key_value == 'last_update':
                        print("   >>> ¡Este es el registro que buscamos!")
                    
                except Exception as e:
                    print(f"   to_dict() falló: {e}")
                
                # Intentar acceder directamente como objeto
                try:
                    print(f"   Acceso directo - id: {getattr(record, 'id', 'NO ATTR')}")
                    print(f"   Acceso directo - key: {getattr(record, 'key', 'NO ATTR')}")
                    print(f"   Acceso directo - value: {getattr(record, 'value', 'NO ATTR')}")
                except Exception as e:
                    print(f"   Acceso directo falló: {e}")
                
        except Exception as e:
            print(f"❌ Error al leer registros de metadata: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n✅ Prueba completada")
        return True
        
    except Exception as e:
        print(f"❌ Error al probar acceso a la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔍 Prueba de acceso a registros de metadata")
    print("=" * 40)
    
    success = await test_record_access()
    
    if success:
        print("\n🎉 ¡La prueba ha sido completada!")
    else:
        print("\n❌ Hubo un problema al probar el acceso a la base de datos.")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    asyncio.run(main())
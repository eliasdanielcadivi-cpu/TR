#!/usr/bin/env python3
"""
Script para inspeccionar cómo se almacenan los registros en la base de datos de TRON (versión corregida)
"""

import asyncio
import sys
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def inspect_metadata_correct():
    """Inspecciona cómo se almacenan los registros en metadata usando el método correcto"""
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
        
        print("🔍 Inspeccionando registros en metadata...")
        
        # Obtener todos los registros en metadata
        try:
            metadata_records = await db_manager.client.collection("metadata").get_full_list()
            print(f"\n📋 Total de registros en metadata: {len(metadata_records)}")
            
            for i, record in enumerate(metadata_records):
                print(f"\nRegistro {i+1}:")
                
                # Usar to_dict() si está disponible
                if hasattr(record, 'to_dict'):
                    record_dict = record.to_dict()
                    print(f"   Datos completos: {record_dict}")
                else:
                    # Intentar acceder directamente a los atributos
                    attrs = ['id', 'key', 'value', 'created', 'updated']
                    for attr in attrs:
                        try:
                            value = getattr(record, attr, 'N/A')
                            print(f"   {attr}: {value}")
                        except:
                            print(f"   {attr}: ERROR AL ACCEDER")
                
        except Exception as e:
            print(f"❌ Error al leer registros de metadata: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n✅ Inspección completada")
        return True
        
    except Exception as e:
        print(f"❌ Error al inspeccionar la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔍 Inspección de registros en la base de datos de TRON (corregida)")
    print("=" * 60)
    
    success = await inspect_metadata_correct()
    
    if success:
        print("\n🎉 ¡La inspección ha sido completada!")
    else:
        print("\n❌ Hubo un problema al inspeccionar la base de datos.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
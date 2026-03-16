#!/usr/bin/env python3
"""
Script de inicialización de la base de datos para TRON v4.0
"""

import asyncio
import sys
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def initialize_database():
    """Inicializa la base de datos creando las colecciones necesarias"""
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
        
        print("🔧 Inicializando colecciones de la base de datos...")
        
        # Inicializar las colecciones
        await db_manager.init_db_collections()
        
        print("✅ Colecciones inicializadas correctamente")
        print("\n📋 Colecciones disponibles:")
        print("   • openrouter_models: Información sobre modelos de OpenRouter")
        print("   • execution_logs: Registros de ejecución con tokens y costos")
        print("   • metadata: Metadatos del sistema")
        
        # Verificar que las colecciones existen
        try:
            collections = await db_manager.client.collections.get_full_list()
            print(f"\n📊 Total de colecciones en la base de datos: {len(collections)}")
            
            collection_names = [coll.name for coll in collections]
            required_collections = ['openrouter_models', 'execution_logs', 'metadata']
            
            for req_coll in required_collections:
                if req_coll in collection_names:
                    print(f"   ✅ {req_coll}")
                else:
                    print(f"   ❌ {req_coll} - NO ENCONTRADA")
            
            return True
        except Exception as e:
            print(f"❌ Error al verificar colecciones: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 Inicialización de la base de datos para TRON v4.0")
    print("=" * 50)
    
    success = await initialize_database()
    
    if success:
        print("\n🎉 ¡La base de datos ha sido inicializada correctamente!")
        print("\n💡 Ahora puedes usar las herramientas de monitoreo:")
        print("   python3 resumen.py          # Resumen rápido")
        print("   python3 monitorizacion.py   # Estadísticas detalladas")
        print("   python3 reportes.py daily   # Reporte diario")
    else:
        print("\n❌ Hubo un problema al inicializar la base de datos.")
        print("   Verifica que PocketBase esté corriendo en http://localhost:8090")
        print("   y que las credenciales en tron_config.yaml sean correctas.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
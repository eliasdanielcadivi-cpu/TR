#!/usr/bin/env python3
"""
Script de verificación y creación manual de colecciones para TRON v4.0
"""

import asyncio
import sys
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def verify_and_create_collections():
    """Verifica y crea manualmente las colecciones necesarias"""
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
        
        print("🔍 Verificando colecciones existentes...")
        
        # Definir las colecciones necesarias
        collections_to_create = {
            "openrouter_models": {
                "type": "base",
                "schema": [
                    {"name": "model_id", "type": "text", "required": True, "unique": True},
                    {"name": "name", "type": "text"},
                    {"name": "context_length", "type": "number"},
                    {"name": "price_prompt", "type": "number"},
                    {"name": "price_completion", "type": "number"},
                    {"name": "last_failure", "type": "number"},
                    {"name": "failure_count", "type": "number", "options": {"min": 0}},
                ],
            },
            "execution_logs": {
                "type": "base",
                "schema": [
                    {"name": "model_id", "type": "text", "required": True},
                    {"name": "tokens_in", "type": "number"},
                    {"name": "tokens_out", "type": "number"},
                    {"name": "calculated_cost_usd", "type": "number"},
                    {"name": "is_free", "type": "bool"},
                ]
            },
            "metadata": {
                "type": "base",
                "schema": [
                    {"name": "key", "type": "text", "required": True, "unique": True},
                    {"name": "value", "type": "json"}
                ],
            }
        }
        
        # Verificar y crear cada colección
        for name, spec in collections_to_create.items():
            try:
                # Intentar obtener la colección
                collection = await db_manager.client.collections.get_one(name)
                print(f"✅ Colección '{name}' ya existe")
            except Exception as e:
                # Si no existe, crearla
                print(f"🔧 Creando colección '{name}'...")
                try:
                    await db_manager.client.collections.create({
                        "name": name,
                        "type": spec["type"],
                        "schema": spec["schema"],
                        "listRule": None, "viewRule": None,
                        "createRule": None, "updateRule": None, "deleteRule": None
                    })
                    print(f"✅ Colección '{name}' creada exitosamente")
                except Exception as create_error:
                    print(f"❌ Error al crear colección '{name}': {create_error}")
        
        # Crear registro de metadata para last_update si no existe
        try:
            await db_manager.client.collection("metadata").get_one("last_update_ts")
            print("✅ Registro 'last_update_ts' ya existe")
        except Exception:
            print("🔧 Creando registro 'last_update_ts'...")
            try:
                await db_manager.client.collection("metadata").create({
                    "id": "last_update_ts",
                    "key": "last_update", "value": {"timestamp": 0}
                })
                print("✅ Registro 'last_update_ts' creado exitosamente")
            except Exception as e:
                print(f"❌ Error al crear registro 'last_update_ts': {e}")
        
        print("\n🎉 Verificación y creación de colecciones completada.")
        
        # Verificar que las colecciones ahora existen
        print("\n🔍 Verificando que las colecciones sean accesibles...")
        for name in collections_to_create.keys():
            try:
                # Intentar obtener algunos registros para verificar accesibilidad
                records = await db_manager.client.collection(name).get_full_list()
                print(f"✅ Colección '{name}' accesible, tiene {len(records)} registros")
            except Exception as e:
                print(f"⚠️  Colección '{name}' accesible pero hubo error al leer registros: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar y crear colecciones: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔧 Verificación y creación manual de colecciones para TRON v4.0")
    print("=" * 60)
    
    success = await verify_and_create_collections()
    
    if success:
        print("\n✅ ¡Las colecciones han sido verificadas y creadas correctamente!")
        print("\n💡 Ahora puedes usar las herramientas de monitoreo:")
        print("   python3 resumen.py          # Resumen rápido")
        print("   python3 monitorizacion.py   # Estadísticas detalladas")
        print("   python3 reportes.py daily   # Reporte diario")
    else:
        print("\n❌ Hubo un problema al crear las colecciones.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Script para verificar qué modelos hay en la base de datos local
"""

import sys
import asyncio
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def check_local_models():
    """Verifica qué modelos hay en la base de datos local"""
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
        
        print("🔍 Verificando modelos en la base de datos local...")
        
        # Obtener todos los modelos
        try:
            all_models = await db_manager.client.collection("openrouter_models").get_full_list()
            print(f"📋 Total de modelos en la base de datos: {len(all_models)}")
            
            # Buscar modelos gratuitos
            free_models = [model for model in all_models if model.get('price_prompt', 1) == 0]
            print(f"📋 Modelos gratuitos en la base de datos: {len(free_models)}")
            
            if free_models:
                print("\n📝 Primeros 10 modelos gratuitos:")
                for i, model in enumerate(free_models[:10]):
                    model_id = model.get('model_id', 'unknown')
                    name = model.get('name', 'unknown')
                    print(f"  {i+1}. {model_id} - {name}")
            
            # Buscar modelos de bajo costo
            low_cost_models = [model for model in all_models if 0 < model.get('price_prompt', 1) < 0.01]
            print(f"\n📋 Modelos de bajo costo en la base de datos: {len(low_cost_models)}")
            
            if low_cost_models:
                print("\n📝 Primeros 10 modelos de bajo costo:")
                for i, model in enumerate(low_cost_models[:10]):
                    model_id = model.get('model_id', 'unknown')
                    name = model.get('name', 'unknown')
                    price = model.get('price_prompt', 'unknown')
                    print(f"  {i+1}. {model_id} - {name} (precio: {price})")
            
        except Exception as e:
            print(f"❌ Error al leer modelos: {e}")
            import traceback
            traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar modelos locales: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔍 Verificación de modelos en la base de datos local")
    print("=" * 50)
    
    success = await check_local_models()
    
    if success:
        print("\n✅ Verificación completada")
    else:
        print("\n❌ Hubo un problema al verificar los modelos")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
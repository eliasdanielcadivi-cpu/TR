#!/usr/bin/env python3
"""
Script de resumen rápido para TRON v4.0
Muestra un resumen conciso de uso y saldo para monitoreo diario
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def quick_summary():
    """Muestra un resumen rápido de uso y saldo"""
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
            return
        
        connected = await db_manager.connect(user, password)
        if not connected:
            print("❌ No se pudo conectar a la base de datos")
            return
        
        print("🔍 RESUMEN RÁPIDO DE TRON v4.0")
        print("=" * 40)
        
        # Consultar balance actual de OpenRouter
        openrouter_key = config['keys'].get('openrouter_live')
        if openrouter_key:
            print("\n💰 SALDO ACTUAL:")
            balance_info = await db_manager.get_openrouter_balance(openrouter_key)
            if balance_info:
                usage_data = balance_info.get('data', {}).get('usage', {})
                remaining = usage_data.get('remaining', 'N/A')
                total = usage_data.get('total', 'N/A')
                
                print(f"   Créditos restantes: {remaining}")
                print(f"   Créditos totales: {total}")
                
                if isinstance(remaining, (int, float)) and isinstance(total, (int, float)):
                    percentage = (remaining / total) * 100 if total > 0 else 0
                    print(f"   Porcentaje restante: {percentage:.2f}%")
            else:
                print("   No se pudo obtener el balance")
        
        # Consultar últimas ejecuciones
        print("\n🔄 ÚLTIMAS EJECUCIONES:")
        try:
            # Primero asegurémonos de que la colección existe
            await db_manager.init_db_collections()

            # Obtener registros de ejecución
            all_logs = await db_manager.client.collection("execution_logs").get_full_list()

            # Ordenar por fecha de creación (más recientes primero)
            sorted_logs = sorted(all_logs, key=lambda x: getattr(x, 'created', ''), reverse=True)

            # Tomar solo los 5 más recientes
            recent_logs = sorted_logs[:5]

            if recent_logs:
                for i, log in enumerate(recent_logs, 1):
                    model_short = getattr(log, 'model_id', 'Unknown')[:20] + ".." if len(str(getattr(log, 'model_id', 'Unknown'))) > 20 else getattr(log, 'model_id', 'Unknown')
                    print(f"   {i}. {model_short} - Costo: ${getattr(log, 'calculated_cost_usd', 0):.6f}")
            else:
                print("   No hay ejecuciones recientes")
        except Exception as e:
            print(f"   Error al obtener ejecuciones: {e}")

        # Estadísticas del día
        print("\n📊 ESTADÍSTICAS DEL DÍA:")
        try:
            from datetime import datetime
            today = datetime.now().date().isoformat()

            # Asegurémonos de que la colección existe
            await db_manager.init_db_collections()

            # Obtener registros de la base de datos
            all_logs = await db_manager.client.collection("execution_logs").get_full_list()

            # Filtrar registros del día actual
            today_logs = [
                log for log in all_logs
                if getattr(log, 'created', '').startswith(today)
            ]

            daily_executions = len(today_logs)
            daily_cost = sum(getattr(log, 'calculated_cost_usd', 0) or 0 for log in today_logs)
            daily_tokens = sum(((getattr(log, 'tokens_in', 0) or 0) + (getattr(log, 'tokens_out', 0) or 0)) for log in today_logs)

            print(f"   Ejecuciones hoy: {daily_executions}")
            print(f"   Costo hoy: ${daily_cost:.6f}")
            print(f"   Tokens hoy: {daily_tokens:,}")

        except Exception as e:
            print(f"   Error al obtener estadísticas del día: {e}")
        
        print("\n" + "=" * 40)
        print(f"Actualizado: {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error al obtener resumen: {e}")

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Script de resumen rápido para TRON v4.0")
        print("Muestra un resumen conciso de uso y saldo para monitoreo diario")
        print("\nUso:")
        print("  python3 resumen.py              # Muestra resumen rápido")
        print("  python3 resumen.py --help       # Muestra esta ayuda")
        return
    
    await quick_summary()

if __name__ == "__main__":
    asyncio.run(main())
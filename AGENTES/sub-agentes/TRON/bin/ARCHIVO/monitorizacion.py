#!/usr/bin/env python3
"""
Script de monitorización para TRON v4.0
Muestra estadísticas de uso, saldo y consumo de tokens
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def show_usage_stats():
    """Muestra estadísticas de uso desde la base de datos"""
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
        
        print("📊 ESTADÍSTICAS DE USO DE TRON v4.0")
        print("=" * 50)
        
        # Consultar balance actual de OpenRouter
        openrouter_key = config['keys'].get('openrouter_live')
        if openrouter_key:
            print("\n💰 BALANCE ACTUAL DE OPENROUTER:")
            balance_info = await db_manager.get_openrouter_balance(openrouter_key)
            if balance_info:
                usage_data = balance_info.get('data', {}).get('usage', {})
                remaining = usage_data.get('remaining', 'N/A')
                total = usage_data.get('total', 'N/A')
                reset_date = balance_info.get('data', {}).get('reset_date', 'N/A')
                
                print(f"   • Créditos totales: {total}")
                print(f"   • Créditos restantes: {remaining}")
                print(f"   • Fecha de reinicio: {reset_date}")
            else:
                print("   • No se pudo obtener el balance actual")
        
        # Consultar registros de ejecución
        print("\n📈 REGISTROS DE EJECUCIÓN RECIENTES:")
        try:
            # Obtener todos los registros y ordenarlos por fecha
            all_logs = await db_manager.client.collection("execution_logs").get_full_list()
            sorted_logs = sorted(all_logs, key=lambda x: getattr(x, 'created', ''), reverse=True)
            recent_logs = sorted_logs[:10]

            if recent_logs:
                print(f"   {'Modelo':<30} {'Tokens In':<10} {'Tokens Out':<10} {'Costo (USD)':<12} {'Fecha':<20}")
                print("   " + "-" * 85)

                for log in recent_logs:
                    model_id = getattr(log, 'model_id', 'Unknown')[:28] + ".." if len(str(getattr(log, 'model_id', 'Unknown'))) > 30 else getattr(log, 'model_id', 'Unknown')
                    print(f"   {model_id:<30} {getattr(log, 'tokens_in', 0):<10} {getattr(log, 'tokens_out', 0):<10} {getattr(log, 'calculated_cost_usd', 0):<12.6f} {getattr(log, 'created', '')[:19]:<20}")
            else:
                print("   • No hay registros de ejecución recientes")
        except Exception as e:
            print(f"   • Error al obtener registros de ejecución: {e}")
        
        # Estadísticas generales
        print("\n📈 ESTADÍSTICAS GENERALES:")
        try:
            # Total de ejecuciones
            all_logs = await db_manager.client.collection("execution_logs").get_full_list()
            total_executions = len(all_logs)

            # Total de tokens consumidos
            total_tokens_in = sum(getattr(log, 'tokens_in', 0) or 0 for log in all_logs)
            total_tokens_out = sum(getattr(log, 'tokens_out', 0) or 0 for log in all_logs)
            total_tokens = total_tokens_in + total_tokens_out

            # Costo total
            total_cost = sum(getattr(log, 'calculated_cost_usd', 0) or 0 for log in all_logs)

            # Ejecuciones gratuitas vs de pago
            free_executions = sum(1 for log in all_logs if getattr(log, 'is_free', False))
            paid_executions = total_executions - free_executions

            print(f"   • Total de ejecuciones registradas: {total_executions}")
            print(f"   • Ejecuciones gratuitas: {free_executions}")
            print(f"   • Ejecuciones de pago: {paid_executions}")
            print(f"   • Total de tokens consumidos: {total_tokens:,}")
            print(f"   • Tokens de entrada: {total_tokens_in:,}")
            print(f"   • Tokens de salida: {total_tokens_out:,}")
            print(f"   • Costo total acumulado: ${total_cost:.6f}")

        except Exception as e:
            print(f"   • Error al calcular estadísticas generales: {e}")
        
        # Modelos más utilizados
        print("\n🎯 MODELOS MÁS UTILIZADOS:")
        try:
            from collections import Counter
            model_counts = Counter(getattr(log, 'model_id', 'Unknown') for log in all_logs)

            most_common = model_counts.most_common(5)
            if most_common:
                for model, count in most_common:
                    print(f"   • {model}: {count} ejecuciones")
            else:
                print("   • No hay datos suficientes")
        except Exception as e:
            print(f"   • Error al obtener modelos más utilizados: {e}")
        
        print("\n" + "=" * 50)
        print(f"Información actualizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")
        import traceback
        traceback.print_exc()

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Script de monitorización para TRON v4.0")
        print("Muestra estadísticas de uso, saldo y consumo de tokens")
        print("\nUso:")
        print("  python3 monitorizacion.py          # Muestra estadísticas generales")
        print("  python3 monitorizacion.py --help   # Muestra esta ayuda")
        return
    
    await show_usage_stats()

if __name__ == "__main__":
    asyncio.run(main())
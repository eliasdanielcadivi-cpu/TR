#!/usr/bin/env python3
"""
Script para generar reportes periódicos de uso de TRON v4.0
"""

import asyncio
import sys
import csv
from datetime import datetime, timedelta
from pathlib import Path

# Añadir el directorio bin de TRON al path
sys.path.insert(0, '/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')

async def generate_report(report_type="daily"):
    """Genera un reporte de uso según el tipo especificado"""
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
        
        # Determinar rango de fechas según el tipo de reporte
        now = datetime.now()
        if report_type == "daily":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            report_title = f"Reporte Diario - {start_date.strftime('%Y-%m-%d')}"
        elif report_type == "weekly":
            start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=7)
            report_title = f"Reporte Semanal - {start_date.strftime('%Y-%m-%d')} a {(end_date-timedelta(days=1)).strftime('%Y-%m-%d')}"
        elif report_type == "monthly":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            report_title = f"Reporte Mensual - {start_date.strftime('%Y-%m')}"
        else:
            start_date = now - timedelta(days=30)  # Por defecto, últimos 30 días
            report_title = f"Reporte Personalizado - Últimos 30 días"
        
        print(f"📊 {report_title}")
        print("=" * 60)
        
        # Consultar registros de ejecución en el rango de fechas
        try:
            import json
            # Convertir fecha a formato ISO para la consulta
            start_date_iso = start_date.isoformat()
            
            # Obtener todos los logs y filtrarlos localmente
            all_logs = await db_manager.client.collection("execution_logs").get_full_list()
            execution_logs = [
                log for log in all_logs
                if getattr(log, 'created', '').startswith(start_date.date().isoformat())
            ]
            # Ordenar por fecha de creación (más recientes primero)
            execution_logs = sorted(execution_logs, key=lambda x: getattr(x, 'created', ''), reverse=True)
            
            if execution_logs:
                print(f"\n📈 Ejecuciones encontradas: {len(execution_logs)}")
                
                # Calcular métricas
                total_tokens_in = sum(log.tokens_in or 0 for log in execution_logs)
                total_tokens_out = sum(log.tokens_out or 0 for log in execution_logs)
                total_tokens = total_tokens_in + total_tokens_out
                total_cost = sum(log.calculated_cost_usd or 0 for log in execution_logs)
                
                # Contar ejecuciones por tipo
                free_executions = sum(1 for log in execution_logs if getattr(log, 'is_free', False))
                paid_executions = len(execution_logs) - free_executions
                
                print(f"\n🔢 MÉTRICAS DEL PERIODO:")
                print(f"   • Ejecuciones totales: {len(execution_logs)}")
                print(f"   • Ejecuciones gratuitas: {free_executions}")
                print(f"   • Ejecuciones de pago: {paid_executions}")
                print(f"   • Total de tokens consumidos: {total_tokens:,}")
                print(f"   • Tokens de entrada: {total_tokens_in:,}")
                print(f"   • Tokens de salida: {total_tokens_out:,}")
                print(f"   • Costo total: ${total_cost:.6f}")
                
                # Modelos más utilizados en el periodo
                from collections import Counter
                model_counts = Counter(log.model_id for log in execution_logs)
                
                print(f"\n🎯 MODELOS MÁS UTILIZADOS:")
                for model, count in model_counts.most_common(5):
                    print(f"   • {model}: {count} ejecuciones")
                
                # Guardar reporte en CSV
                csv_filename = f"/home/daniel/tron/programas/ProyectoPizza/TRON/resultados/reporte_{report_type}_{now.strftime('%Y%m%d_%H%M%S')}.csv"
                Path(csv_filename).parent.mkdir(parents=True, exist_ok=True)
                
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['fecha', 'modelo', 'tokens_entrada', 'tokens_salida', 'costo_usd', 'es_gratuito']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for log in execution_logs:
                        writer.writerow({
                            'fecha': log.created,
                            'modelo': log.model_id,
                            'tokens_entrada': log.tokens_in or 0,
                            'tokens_salida': log.tokens_out or 0,
                            'costo_usd': log.calculated_cost_usd or 0,
                            'es_gratuito': getattr(log, 'is_free', False)
                        })
                
                print(f"\n💾 Reporte detallado guardado en: {csv_filename}")
                
            else:
                print(f"\n📅 No se encontraron ejecuciones desde {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        except Exception as e:
            print(f"❌ Error al obtener registros de ejecución: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 60)
        print(f"Reporte generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error al generar reporte: {e}")
        import traceback
        traceback.print_exc()

async def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print("Script para generar reportes periódicos de uso de TRON v4.0")
        print("\nUso:")
        print("  python3 reportes.py daily      # Reporte diario")
        print("  python3 reportes.py weekly     # Reporte semanal")
        print("  python3 reportes.py monthly    # Reporte mensual")
        print("  python3 reportes.py custom     # Reporte de los últimos 30 días")
        print("  python3 reportes.py --help     # Muestra esta ayuda")
        return
    
    report_type = sys.argv[1]
    if report_type not in ["daily", "weekly", "monthly", "custom"]:
        print(f"Tipo de reporte no válido: {report_type}")
        print("Tipos válidos: daily, weekly, monthly, custom")
        return
    
    await generate_report(report_type)

if __name__ == "__main__":
    asyncio.run(main())
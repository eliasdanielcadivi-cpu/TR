#!/usr/bin/env python3
"""
Guía de uso de las herramientas de monitoreo de TRON v4.0
"""

def show_usage_guide():
    """Muestra la guía de uso de las herramientas de monitoreo"""
    print("🎓 GUÍA DE USO DE LAS HERRAMIENTAS DE MONITOREO DE TRON v4.0")
    print("=" * 65)
    
    print("\n📋 DESCRIPCIÓN GENERAL:")
    print("TRON v4.0 incluye herramientas para monitorear el uso y el saldo")
    print("de forma continua y eficiente. Estas herramientas permiten:")
    print("• Verificar el saldo actual de OpenRouter")
    print("• Monitorear el consumo de tokens")
    print("• Generar reportes periódicos")
    print("• Analizar el historial de ejecuciones")
    
    print("\n🔧 HERRAMIENTAS DISPONIBLES:")
    
    print("\n1. 🔄 Resumen Rápido")
    print("   Comando: python3 TRON/bin/resumen.py")
    print("   Propósito: Vista concisa de uso y saldo para monitoreo diario")
    print("   Muestra:")
    print("   • Saldo actual de OpenRouter")
    print("   • Últimas 5 ejecuciones")
    print("   • Estadísticas del día actual")
    
    print("\n2. 📊 Estadísticas Detalladas")
    print("   Comando: python3 TRON/bin/monitorizacion.py")
    print("   Propósito: Estadísticas completas de uso, saldo y consumo")
    print("   Muestra:")
    print("   • Saldo actual de OpenRouter")
    print("   • Últimas 10 ejecuciones")
    print("   • Estadísticas generales acumuladas")
    print("   • Modelos más utilizados")
    
    print("\n3. 📈 Reportes Periódicos")
    print("   Comandos:")
    print("   • python3 TRON/bin/reportes.py daily    # Reporte diario")
    print("   • python3 TRON/bin/reportes.py weekly   # Reporte semanal")
    print("   • python3 TRON/bin/reportes.py monthly  # Reporte mensual")
    print("   Propósito: Generar reportes detallados por período")
    print("   Incluye:")
    print("   • Ejecuciones totales y por tipo")
    print("   • Consumo de tokens (entrada y salida)")
    print("   • Costos acumulados")
    print("   • Modelos más utilizados")
    print("   • Datos exportados en CSV para análisis")
    
    print("\n4. 🛠 Inicialización de Base de Datos")
    print("   Comando: python3 TRON/bin/inicializar_db.py")
    print("   Propósito: Asegurar que las colecciones necesarias existan")
    print("   Nota: Solo necesario si se presentan errores de colección no encontrada")
    
    print("\n5. 🏗 Creación Manual de Colecciones")
    print("   Comando: python3 TRON/bin/crear_colecciones.py")
    print("   Propósito: Crear manualmente las colecciones si no existen")
    
    print("\n📊 FLUJO DE TRABAJO RECOMENDADO:")
    print("1. Ejecutar 'crear_colecciones.py' si es la primera vez")
    print("2. Usar 'resumen.py' para monitoreo diario rápido")
    print("3. Usar 'monitorizacion.py' para revisiones semanales detalladas")
    print("4. Usar 'reportes.py' para análisis periódicos (diarios/semanales/mensuales)")
    
    print("\n💡 CONSEJOS DE USO:")
    print("• Ejecuta 'resumen.py' al inicio de cada día para verificar el estado")
    print("• Usa 'reportes.py daily' para llevar un historial de uso")
    print("• Si ves errores de 'colección no encontrada', ejecuta 'crear_colecciones.py'")
    print("• Los archivos CSV generados se guardan en TRON/resultados/")
    
    print("\n🔐 REQUISITOS:")
    print("• Asegúrate de que PocketBase esté corriendo en http://localhost:8090")
    print("• Verifica que las credenciales en tron_config.yaml sean correctas")
    print("• Tener conexión a internet para consultar saldos de OpenRouter")
    
    print("\n" + "=" * 65)
    print("ℹ️  Para más información, consulta LEEME_TRON.md")
    print("   Para soporte técnico, revisa la documentación en TRON/docs/")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        print("Guía de uso de las herramientas de monitoreo de TRON v4.0")
        print("\nUso:")
        print("  python3 guia_monitoreo.py          # Muestra la guía completa")
        print("  python3 guia_monitoreo.py --help   # Muestra esta ayuda")
        return
    
    show_usage_guide()

if __name__ == "__main__":
    main()
#!/bin/bash
# AgenteDeCambio CLI - Script de lanzamiento directo
# Este script debe ejecutarse directamente en la terminal

set -e  # Salir si hay error

cd /home/daniel/tron/programas/TR
source .venv/bin/activate

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}🚀 AgenteDeCambio CLI${NC}"
echo ""

# Verificar API Key
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  ADVERTENCIA: DEEPSEEK_API_KEY no configurada${NC}"
    echo "   Para usar el chat, configura la variable de entorno:"
    echo "   export DEEPSEEK_API_KEY='sk-tu-api-key'"
    echo ""
    echo "   Obtén tu API key en: https://platform.deepseek.com/api_keys"
    echo ""
    echo "   Presiona Ctrl+C para cancelar y configurar, o Enter para continuar sin API Key..."
    read -r
else
    echo -e "${GREEN}✅ DeepSeek API Key: Configurada${NC}"
    echo ""
fi

echo "Controles:"
echo "  Enter  - Enviar mensaje"
echo "  Ctrl+Q - Salir"
echo "  Ctrl+S - Guardar sesión"
echo "  F1     - Mostrar ayuda"
echo ""
echo "Iniciando app TUI en 3 segundos..."
sleep 1

echo ""
echo "Selecciona modo de ejecución:"
echo "  1) Modo Simplificado (print/input - FUNCIONA SIEMPRE)"
echo "  2) Modo TUI (Textual - Requiere terminal gráfica)"
echo "  3) Solo diagnóstico"
echo ""
echo -n "Opción [1-3]: "
read -r OPCION

# Crear script temporal para modo TUI
cat > /tmp/run_app.py << 'PYTHON_EOF'
import sys
import os
sys.path.insert(0, '/home/daniel/tron/programas/TR')

print("Cargando módulos...")
try:
    from modules.ui.app import run_app
    print("✅ run_app importado correctamente")
except Exception as e:
    print(f"❌ Error al importar run_app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Iniciando app Textual...")
try:
    run_app()
except KeyboardInterrupt:
    print("\n\nApp cerrada por usuario (Ctrl+C)")
    sys.exit(0)
except Exception as e:
    print(f"❌ Error en ejecución: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_EOF

case $OPCION in
    3)
        echo "Solo ejecutando diagnóstico..."
        python AGENTES/sub-agentes/AgenteDeCambio/diagnostico.py
        rm -f /tmp/run_app.py
        exit 0
        ;;
    2)
        echo "Iniciando modo TUI (Textual)..."
        echo "Si se queda colgado, presiona Ctrl+C"
        sleep 2
        python /tmp/run_app.py
        EXIT_CODE=$?
        rm -f /tmp/run_app.py
        exit $EXIT_CODE
        ;;
    1|*)
        echo "Iniciando modo simplificado..."
        python AGENTES/sub-agentes/AgenteDeCambio/chat_simple.py
        ;;
esac

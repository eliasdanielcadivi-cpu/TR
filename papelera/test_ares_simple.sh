#!/bin/bash
# =============================================================================
# ARES - Script de Pruebas Rápidas (Versión Simplificada)
# =============================================================================
# Uso: ./test_ares_simple.sh
# Salida: Guarda resultados en /home/daniel/tron/programas/TR/papelera/pruebas_simple.txt
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_FILE="${SCRIPT_DIR}/pruebas_simple.txt"
ARES_CMD="${SCRIPT_DIR}/../bin/ares"
PYTHON_CMD="${SCRIPT_DIR}/../.venv/bin/python"

# Iniciar archivo
echo "=============================================================================" > "$OUTPUT_FILE"
echo "ARES - Pruebas Simplificadas" >> "$OUTPUT_FILE"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Función para ejecutar prueba
test_py() {
    local desc="$1"
    local code="$2"
    
    echo "--- $desc ---" >> "$OUTPUT_FILE"
    echo "Código: $code" >> "$OUTPUT_FILE"
    echo "Resultado:" >> "$OUTPUT_FILE"
    
    if timeout 30 $PYTHON_CMD -c "$code" >> "$OUTPUT_FILE" 2>&1; then
        echo "✓ Exitoso" >> "$OUTPUT_FILE"
    else
        echo "✗ Timeout o Error" >> "$OUTPUT_FILE"
    fi
    echo "" >> "$OUTPUT_FILE"
}

echo "Ejecutando pruebas simplificadas..."

# Prueba 1: Verificar providers
test_py "1. Verificar providers cargados" "
from modules.ia.ai_engine import AIEngine
from config import TRContext
ctx = TRContext()
ai = AIEngine(ctx.config.get('ai', {}), ctx.base_path)
print('Providers:', list(ai._providers.keys()))
print('Default:', ai.default_provider)
"

# Prueba 2: Resolución de modelo
test_py "2. Resolución de modelo gemma3:4b" "
from modules.ia.ai_engine import AIEngine
from config import TRContext
ctx = TRContext()
ai = AIEngine(ctx.config.get('ai', {}), ctx.base_path)
provider, model = ai._resolve_provider_and_model('gemma3:4b')
print('Provider:', type(provider).__name__)
print('Model:', model)
"

# Prueba 3: TemplateManager
test_py "3. TemplateManager carga plantillas" "
from modules.ia.templates import TemplateManager
tm = TemplateManager('modules/ia/templates')
print('Plantillas:', tm.list_templates())
"

# Prueba 4: ToolRegistry
test_py "4. ToolRegistry herramientas" "
from modules.ia.tools import ToolRegistry
tr = ToolRegistry()
print('Herramientas:', len(tr.list_tools()))
"

# Prueba 5: Ollama directo
test_py "5. Conexión directa a Ollama" "
import requests
r = requests.get('http://localhost:11434/api/tags', timeout=5)
print('Modelos Ollama:', len(r.json().get('models', [])))
"

# Prueba 6: GemmaProvider directo
test_py "6. GemmaProvider info de modelo" "
from modules.ia.providers import GemmaProvider
gp = GemmaProvider({'base_url': 'http://localhost:11434', 'model': 'gemma3:4b'})
info = gp._get_model_info('gemma3:4b')
print('Template obtenido:', 'template' in info)
print('Params:', 'parameters' in info)
"

echo "" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"
echo "FIN DE PRUEBAS - $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"

echo ""
echo "Pruebas completadas. Resultados en:"
echo "  $OUTPUT_FILE"
echo ""
echo "Para ver:"
echo "  cat $OUTPUT_FILE"
echo "  less $OUTPUT_FILE"

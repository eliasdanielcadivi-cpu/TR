#!/bin/bash
# =============================================================================
# ARES - Script de Pruebas Rápidas
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TR_DIR="${SCRIPT_DIR}/.."
OUTPUT_FILE="${SCRIPT_DIR}/pruebas.txt"

# Configurar entorno
export PYTHONPATH="${TR_DIR}:${PYTHONPATH}"
cd "$TR_DIR"
source .venv/bin/activate

echo "=============================================================================" > "$OUTPUT_FILE"
echo "ARES - Pruebas de Integración" >> "$OUTPUT_FILE"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

test_py() {
    local desc="$1"
    local code="$2"
    
    echo "--- $desc ---" >> "$OUTPUT_FILE"
    echo "$code" | timeout 30 python3 >> "$OUTPUT_FILE" 2>&1 && echo "✓ OK" >> "$OUTPUT_FILE" || echo "✗ Error/Timeout" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
}

echo "Ejecutando pruebas..."

test_py "1. Providers cargados" "
from modules.ia.ai_engine import AIEngine
from config import TRContext
ctx = TRContext()
ai = AIEngine(ctx.config.get('ai', {}), ctx.base_path)
print('Providers:', list(ai._providers.keys()))
print('Default:', ai.default_provider)
"

test_py "2. Resolución gemma3:4b" "
from modules.ia.ai_engine import AIEngine
from config import TRContext
ctx = TRContext()
ai = AIEngine(ctx.config.get('ai', {}), ctx.base_path)
p, m = ai._resolve_provider_and_model('gemma3:4b')
print(f'Provider: {type(p).__name__}, Model: {m}')
"

test_py "3. Plantillas YAML" "
from modules.ia.templates import TemplateManager
tm = TemplateManager('modules/ia/templates')
print('Plantillas:', tm.list_templates())
"

test_py "4. Herramientas" "
from modules.ia.tools import ToolRegistry
tr = ToolRegistry()
print('Herramientas:', len(tr.list_tools()))
for t in tr.list_tools(): print(f'  - {t[\"name\"]}')
"

test_py "5. Ollama API" "
import requests
r = requests.get('http://localhost:11434/api/tags', timeout=5)
print('Modelos:', len(r.json().get('models', [])))
"

test_py "6. Gemma template nativo" "
from modules.ia.providers import GemmaProvider
gp = GemmaProvider({'base_url': 'http://localhost:11434', 'model': 'gemma3:4b'})
info = gp._get_model_info('gemma3:4b')
print('Template:', 'template' in info)
print('Params:', 'parameters' in info)
"

echo "" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"
echo "FIN - $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"

echo ""
echo "Resultados en: $OUTPUT_FILE"
cat "$OUTPUT_FILE"

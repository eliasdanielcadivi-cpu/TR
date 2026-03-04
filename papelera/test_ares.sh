#!/bin/bash
# =============================================================================
# ARES - Script de Pruebas de Integración Multi-Provider
# =============================================================================
# Uso: ./test_ares.sh
# Salida: Guarda resultados en /home/daniel/tron/programas/TR/papelera/pruebas.txt
# =============================================================================

set -e

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_FILE="${SCRIPT_DIR}/pruebas.txt"
ARES_CMD="${SCRIPT_DIR}/../bin/ares"

# Colores para output en terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir en terminal y archivo
log() {
    echo -e "$1" | tee -a "$OUTPUT_FILE"
}

# Iniciar archivo de pruebas
init_log() {
    echo "=============================================================================" > "$OUTPUT_FILE"
    echo "ARES - Pruebas de Integración Multi-Provider" >> "$OUTPUT_FILE"
    echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
    echo "=============================================================================" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
}

# Separador de sección
section() {
    log ""
    log "${BLUE}=============================================================================${NC}"
    log "${BLUE}$1${NC}"
    log "${BLUE}=============================================================================${NC}"
    echo "" >> "$OUTPUT_FILE"
}

# Ejecutar prueba individual
test_cmd() {
    local description="$1"
    local cmd="$2"
    
    log ""
    log "${YELLOW}PRUEBA:${NC} $description"
    log "${GREEN}COMANDO:${NC} $cmd"
    log "${GREEN}RESULTADO:${NC}"
    
    echo "--- $description ---" >> "$OUTPUT_FILE"
    echo "Comando: $cmd" >> "$OUTPUT_FILE"
    echo "Resultado:" >> "$OUTPUT_FILE"
    
    # Ejecutar comando y capturar salida
    if eval "$cmd" >> "$OUTPUT_FILE" 2>&1; then
        log "${GREEN}✓ Exitoso${NC}"
    else
        log "${RED}✗ Fallido${NC}"
    fi
    
    # Mostrar últimas líneas del resultado
    tail -n 5 "$OUTPUT_FILE" | while read line; do
        log "  $line"
    done
    
    echo "" >> "$OUTPUT_FILE"
}

# =============================================================================
# INICIO DE PRUEBAS
# =============================================================================

init_log

section "1. VERIFICACIÓN DE COMANDOS BÁSICOS"

test_cmd "Ver ayuda" "$ARES_CMD --help"
test_cmd "Ver configuración" "$ARES_CMD config"
test_cmd "Listar modelos" "$ARES_CMD models"
test_cmd "Listar plantillas" "$ARES_CMD templates"
test_cmd "Listar herramientas" "$ARES_CMD tools"

section "2. PRUEBAS CON GEMMA (OLLAMA)"

test_cmd "Consulta simple con gemma3:4b" "$ARES_CMD p 'Hola, ¿cómo estás?' --model gemma"
test_cmd "Consulta con gemma3:12b" "$ARES_CMD p 'Explica qué es la inteligencia artificial' --model gemma12b"
test_cmd "Consulta con plantilla chat" "$ARES_CMD p 'Tengo una pregunta sobre programación' --template chat"
test_cmd "Consulta con plantilla code" "$ARES_CMD p 'Escribe un hello world en Python' --template code"
test_cmd "Combinar modelo y plantilla" "$ARES_CMD p 'Explica este código: print(hello)' --model gemma12b --template code"

section "3. PRUEBAS CON PLANTILLAS YAML"

test_cmd "Plantilla default" "$ARES_CMD p '¿Qué es Python?' --template default"
test_cmd "Plantilla chat" "$ARES_CMD p 'Conversación casual' --template chat"
test_cmd "Plantilla code" "$ARES_CMD p 'Función factorial en Python' --template code"
test_cmd "Plantilla tools" "$ARES_CMD p '¿Qué herramientas tienes?' --template tools"

section "4. PRUEBAS DE TEMPERATURA"

test_cmd "Temperatura baja (0.2 - determinista)" "$ARES_CMD p '2+2=' --temperature 0.2"
test_cmd "Temperatura media (0.7 - balance)" "$ARES_CMD p 'Cuenta hasta 5' --temperature 0.7"
test_cmd "Temperatura alta (0.9 - creativo)" "$ARES_CMD p 'Escribe un haiku sobre IA' --temperature 0.9"

section "5. PRUEBAS CON DEEPSEEK (REQUIERE API KEY)"

log ""
log "${YELLOW}Nota: Estas pruebas requieren DEEPSEEK_API_KEY configurada${NC}"
log ""

test_cmd "Consulta simple DeepSeek" "$ARES_CMD p 'Hola desde DeepSeek' --model deepseek"
test_cmd "Código con DeepSeek" "$ARES_CMD p 'Hello world en JavaScript' --model deepseek"

section "6. PRUEBAS DE FUNCTION CALLING"

test_cmd "Herramienta search (simulado)" "$ARES_CMD p '¿Quién ganó el mundial 2022?' --template tools"
test_cmd "Herramienta translate (simulado)" "$ARES_CMD p 'Traduce hello al español' --template tools"
test_cmd "Herramienta weather (simulado)" "$ARES_CMD p '¿Qué clima hay en Madrid?' --template tools"

section "7. PRUEBAS CON OTROS MODELOS OLLAMA"

test_cmd "Phi4-mini" "$ARES_CMD p 'Hola' --model phi4-mini"
test_cmd "Llama3.1:8b" "$ARES_CMD p 'Hola' --model llama3.1:8b"
test_cmd "Qwen2.5-coder" "$ARES_CMD p 'Hola' --model qwen2.5-coder:7b-instruct"

section "8. PRUEBAS DE ERROR Y BORDES"

test_cmd "Modelo inexistente" "$ARES_CMD p 'test' --model modelo_no_existe"
test_cmd "Plantilla inexistente" "$ARES_CMD p 'test' --template plantilla_no_existe"
test_cmd "Prompt vacío" "$ARES_CMD p ''"
test_cmd "Prompt muy largo (1000 chars)" "$ARES_CMD p \"$(printf 'A%.0s' {1..1000})\""

section "9. VERIFICACIÓN DE ESTADO"

test_cmd "Status del sistema" "$ARES_CMD status"

# =============================================================================
# RESUMEN FINAL
# =============================================================================

section "RESUMEN DE PRUEBAS"

log ""
log "${GREEN}Pruebas completadas. Resultados guardados en:${NC}"
log "${GREEN}$OUTPUT_FILE${NC}"
log ""
log "Para ver el archivo completo:"
log "  cat $OUTPUT_FILE"
log "  less $OUTPUT_FILE"
log ""

# Contar líneas de resultados
total_lines=$(wc -l < "$OUTPUT_FILE")
log "Total de líneas en archivo de pruebas: $total_lines"

echo "" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"
echo "FIN DE PRUEBAS - $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "=============================================================================" >> "$OUTPUT_FILE"

log "${BLUE}=============================================================================${NC}"
log "${BLUE}Script de pruebas finalizado${NC}"
log "${BLUE}=============================================================================${NC}"

#!/bin/bash
# ============================================================================
# Agente de Cambio - Wrapper Standalone
# ============================================================================
# Propósito: Ejecutar el Agente de Cambio en modo standalone
# Ubicación: /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh
# ============================================================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Rutas absolutas
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")/Agente-De-Cambio-Estable"
BIN_DIR="$PROJECT_ROOT/bin"
MODULES_DIR="$PROJECT_ROOT/modules"
DOCS_DIR="$PROJECT_ROOT/docs/CLAVE"

# Banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     🧠 AGENTE DE CAMBIO - Sistema de Conducción Cognitiva    ║"
    echo "║          Wrapper Standalone v0.1.0                          ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Ayuda
print_help() {
    echo -e "${GREEN}USO:${NC}"
    echo "  $0 [comando] [opciones]"
    echo ""
    echo -e "${GREEN}COMANDOS:${NC}"
    echo "  start, run, dev     Iniciar servidores (frontend + backend)"
    echo "  server              Solo backend (puerto 3001)"
    echo "  web                 Solo frontend (puerto 3000)"
    echo "  demo                Ejecutar demostración"
    echo "  cli [args]          Ejecutar CLI con argumentos"
    echo "  docs                Abrir documentación clave"
    echo "  status              Mostrar estado del proyecto"
    echo "  install             Instalar dependencias"
    echo "  help                Mostrar esta ayuda"
    echo ""
    echo -e "${GREEN}EJEMPLOS:${NC}"
    echo "  $0 start            # Ambos servidores"
    echo "  $0 server           # Solo backend"
    echo "  $0 cli --demo       # Demostración CLI"
    echo "  $0 cli -o \"Quiero X\" -d emprendedor  # Objetivo interactivo"
    echo "  $0 docs             # Ver documentación"
    echo ""
    echo -e "${GREEN}RUTAS IMPORTANTES:${NC}"
    echo "  Proyecto:     $PROJECT_ROOT"
    echo "  Documentación: $DOCS_DIR"
    echo "  Módulos:      $MODULES_DIR"
    echo "  Binarios:     $BIN_DIR"
    echo ""
    echo -e "${GREEN}COMANDO ARES:${NC}"
    echo "  ares agente-de-cambio --prompt \"Ayuda con objetivo EMT\""
    echo ""
}

# Iniciar servidores
start_servers() {
    echo -e "${BLUE}═══ INICIANDO SERVIDORES ═══${NC}"
    echo ""
    cd "$PROJECT_ROOT"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Instalando dependencias...${NC}"
        npm install --legacy-peer-deps
    fi
    
    # Verificar .env
    if [ ! -f "$PROJECT_ROOT/apps/server/.env" ]; then
        echo -e "${YELLOW}Creando .env desde ejemplo...${NC}"
        cp "$PROJECT_ROOT/apps/server/.env.example" "$PROJECT_ROOT/apps/server/.env"
        echo -e "${RED}⚠️  IMPORTANTE: Editar $PROJECT_ROOT/apps/server/.env con tu DEEPSEEK_API_KEY${NC}"
        echo ""
    fi
    
    echo -e "${GREEN}Iniciando npm run dev...${NC}"
    echo -e "${CYAN}Frontend: http://localhost:3000${NC}"
    echo -e "${CYAN}Backend:  http://localhost:3001${NC}"
    echo ""
    
    npm run dev
}

# Solo servidor backend
start_server() {
    echo -e "${BLUE}═══ INICIANDO BACKEND ═══${NC}"
    cd "$PROJECT_ROOT"
    
    if [ ! -f "$PROJECT_ROOT/apps/server/.env" ]; then
        cp "$PROJECT_ROOT/apps/server/.env.example" "$PROJECT_ROOT/apps/server/.env"
        echo -e "${RED}⚠️  IMPORTANTE: Editar .env con DEEPSEEK_API_KEY${NC}"
    fi
    
    echo -e "${GREEN}Backend en http://localhost:3001${NC}"
    npm run dev:server
}

# Solo frontend
start_web() {
    echo -e "${BLUE}═══ INICIANDO FRONTEND ═══${NC}"
    cd "$PROJECT_ROOT"
    
    echo -e "${GREEN}Frontend en http://localhost:3000${NC}"
    npm run dev:web
}

# Demostración
run_demo() {
    echo -e "${BLUE}═══ DEMOSTRACIÓN ═══${NC}"
    cd "$PROJECT_ROOT"
    node "$BIN_DIR/agente-de-cambio.js" --demo
}

# CLI con argumentos
run_cli() {
    cd "$PROJECT_ROOT"
    node "$BIN_DIR/agente-de-cambio.js" "$@"
}

# Abrir documentación
open_docs() {
    echo -e "${BLUE}═══ DOCUMENTACIÓN CLAVE ═══${NC}"
    echo ""
    echo -e "${GREEN}Archivos principales:${NC}"
    ls -la "$DOCS_DIR"/*.md 2>/dev/null || echo "No hay archivos .md en $DOCS_DIR"
    echo ""
    echo -e "${CYAN}Para leer un archivo:${NC}"
    echo "  cat $DOCS_DIR/PLAN-CONSTRUCCION.md"
    echo "  cat $DOCS_DIR/LEEME.md"
    echo ""
    echo -e "${CYAN}Enlaces rápidos:${NC}"
    echo "  - Plan: $DOCS_DIR/PLAN-CONSTRUCCION.md"
    echo "  - LEEME: $PROJECT_ROOT/LEEME.md"
    echo "  - README: $PROJECT_ROOT/README.md"
}

# Estado del proyecto
show_status() {
    echo -e "${BLUE}═══ ESTADO DEL PROYECTO ═══${NC}"
    echo ""
    
    cd "$PROJECT_ROOT"
    
    # Módulos
    echo -e "${GREEN}Módulos:${NC}"
    if [ -d "$MODULES_DIR" ]; then
        ls -1 "$MODULES_DIR" | grep -v node_modules | while read module; do
            if [ -f "$MODULES_DIR/$module/manifest.json" ]; then
                status=$(grep -o '"status": "[^"]*"' "$MODULES_DIR/$module/manifest.json" | cut -d'"' -f4)
                echo "  - $module: $status"
            fi
        done
    fi
    echo ""
    
    # Dependencias
    echo -e "${GREEN}Dependencias:${NC}"
    if [ -d "node_modules" ]; then
        echo "  ✓ Instaladas"
    else
        echo "  ✗ No instaladas (ejecutar: $0 install)"
    fi
    echo ""
    
    # .env
    echo -e "${GREEN}Variables de entorno:${NC}"
    if [ -f "$PROJECT_ROOT/apps/server/.env" ]; then
        if grep -q "DEEPSEEK_API_KEY=sk-" "$PROJECT_ROOT/apps/server/.env" 2>/dev/null; then
            echo "  ✓ DEEPSEEK_API_KEY configurada"
        else
            echo "  ⚠ DEEPSEEK_API_KEY no configurada"
        fi
    else
        echo "  ✗ .env no existe (se creará al iniciar)"
    fi
    echo ""
    
    # Git
    echo -e "${GREEN}Git:${NC}"
    git log -1 --oneline 2>/dev/null | sed 's/^/  /'
    echo ""
}

# Instalar dependencias
install_deps() {
    echo -e "${BLUE}═══ INSTALANDO DEPENDENCIAS ═══${NC}"
    cd "$PROJECT_ROOT"
    npm install --legacy-peer-deps
    echo -e "${GREEN}✓ Instalación completada${NC}"
}

# Main
case "${1:-help}" in
    start|run|dev)
        start_servers
        ;;
    server)
        start_server
        ;;
    web)
        start_web
        ;;
    demo)
        run_demo
        ;;
    cli)
        shift
        run_cli "$@"
        ;;
    docs)
        open_docs
        ;;
    status)
        show_status
        ;;
    install)
        install_deps
        ;;
    help|--help|-h)
        print_banner
        print_help
        ;;
    *)
        echo -e "${RED}Comando no reconocido: $1${NC}"
        print_help
        exit 1
        ;;
esac

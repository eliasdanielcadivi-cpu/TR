#!/bin/bash
# =============================================================================
# inyectar-openbox.sh - Inyección de configuración de Openbox
# =============================================================================
# Propósito: Inyectar la configuración maestra de Openbox desde TRON config
#            y reiniciar Openbox sin cerrar sesión.
#
# Uso: inyectar-openbox.sh
#
# Filosofía: La configuración maestra está en ~/tron/programas/TR/config/openbox/
#            Este script la copia a ~/.config/openbox/ y recarga Openbox.
# =============================================================================

set -e

# Rutas
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_SOURCE="$SCRIPT_DIR/rc.xml"
CONFIG_DEST="$HOME/.config/openbox/rc.xml"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     INYECCIÓN DE CONFIGURACIÓN DE OPENBOX - TRON         ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Validar que existe el archivo fuente
if [ ! -f "$CONFIG_SOURCE" ]; then
    echo -e "${RED}❌ ERROR: No se encuentra la configuración fuente:${NC}"
    echo -e "${RED}   $CONFIG_SOURCE${NC}"
    exit 1
fi

# 2. Validar que existe el directorio de destino
if [ ! -d "$HOME/.config/openbox" ]; then
    echo -e "${YELLOW}⚠ Creando directorio de destino...${NC}"
    mkdir -p "$HOME/.config/openbox"
fi

# 3. Backup de la configuración actual (si existe)
if [ -f "$CONFIG_DEST" ]; then
    BACKUP_DEST="$HOME/.config/openbox/rc.xml.backup.$(date +%Y%m%d-%H%M%S)"
    echo -e "${YELLOW}📦 Creando backup:${NC}"
    echo -e "   $BACKUP_DEST"
    cp "$CONFIG_DEST" "$BACKUP_DEST"
fi

# 4. Copiar configuración maestra
echo -e "${GREEN}📋 Copiando configuración maestra:${NC}"
echo -e "   Desde: $CONFIG_SOURCE"
echo -e "   Hacia: $CONFIG_DEST"
cp "$CONFIG_SOURCE" "$CONFIG_DEST"

# 5. Validar sintaxis XML (opcional pero recomendado)
if command -v xmllint &> /dev/null; then
    echo -e "${CYAN}🔍 Validando sintaxis XML...${NC}"
    if xmllint --noout "$CONFIG_DEST" 2>/dev/null; then
        echo -e "${GREEN}   ✓ XML válido${NC}"
    else
        echo -e "${RED}   ❌ ERROR: XML inválido${NC}"
        echo -e "${RED}   Restaurando backup...${NC}"
        cp "$BACKUP_DEST" "$CONFIG_DEST"
        exit 1
    fi
fi

# 6. Reiniciar Openbox (sin cerrar sesión)
echo -e "${CYAN}🔄 Reiniciando Openbox...${NC}"
if command -v openbox &> /dev/null; then
    openbox --reconfigure
    echo -e "${GREEN}   ✓ Openbox reiniciado correctamente${NC}"
else
    echo -e "${RED}   ⚠ openbox no encontrado en PATH${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ CONFIGURACIÓN INYECTADA EXITOSAMENTE                 ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${NC}Cambios aplicados:${NC}"
echo -e "  • Tecla ${CYAN}Windows (Super_L)${NC}: Muestra menú de Openbox"
echo -e "  • Tecla ${CYAN}Menú contextual${NC}: Muestra menú de ventana"
echo ""
echo -e "${NC}Si los cambios no se reflejan inmediatamente, cierre y abra una ventana.${NC}"

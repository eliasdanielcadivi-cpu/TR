#!/bin/bash
# Instalador de mcat para ARES
# Uso: bash scripts/install_mcat.sh

set -e

echo "🔧 Instalando mcat..."

# Método 1: Desde GitHub Releases (binario precompilado)
echo "Intentando descarga desde GitHub..."
GITHUB_URL="https://github.com/Skardyy/mcat/releases/latest"

# Descargar página de releases y extraer enlace directo
LATEST_URL=$(curl -sL $GITHUB_URL | grep -oP 'href="\K[^"]*mcat.*linux.*tar\.gz' | head -1)

if [ -n "$LATEST_URL" ]; then
    echo "Descargando desde: $LATEST_URL"
    curl -sL "$LATEST_URL" -o /tmp/mcat.tar.gz
    tar xzf /tmp/mcat.tar.gz -C /tmp
    sudo mv /tmp/mcat /usr/local/bin/
    sudo chmod +x /usr/local/bin/mcat
    echo "✅ mcat instalado correctamente"
    mcat --version
else
    echo "⚠️  No se pudo descargar automáticamente"
    echo ""
    echo "Instalación manual:"
    echo "1. Visita: $GITHUB_URL"
    echo "2. Descarga el archivo .tar.gz para Linux"
    echo "3. Ejecuta:"
    echo "   tar xzf mcat*.tar.gz"
    echo "   sudo mv mcat /usr/local/bin/"
    echo "   sudo chmod +x /usr/local/bin/mcat"
    exit 1
fi

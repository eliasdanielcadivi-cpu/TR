#!/bin/bash
# Instalador para TRON v5.0 - Cliente Ligero de Modelos OpenRouter

set -e  # Salir si hay error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 Instalando TRON v5.0 - Cliente Ligero de Modelos OpenRouter..."

# Hacer el nuevo tron ejecutable
chmod +x "$SCRIPT_DIR/tron_nuevo"

# Crear enlace simbólico en /usr/local/bin (si se tiene permiso)
if [ -w /usr/local/bin ]; then
    sudo ln -sf "$SCRIPT_DIR/tron_nuevo" /usr/local/bin/tron5
    echo "✅ TRON v5.0 instalado como 'tron5'"
    echo "💡 Uso: tron5 --router  (para menú de modelos)"
    echo "💡 Uso: tron5 openrouter modelo --see  (para ver características)"
elif [ -w /home/daniel/.local/bin ]; then
    ln -sf "$SCRIPT_DIR/tron_nuevo" /home/daniel/.local/bin/tron5
    echo "✅ TRON v5.0 instalado como 'tron5' en ~/.local/bin"
    echo "💡 Asegúrate de que ~/.local/bin esté en tu PATH"
    echo "💡 Uso: tron5 --router  (para menú de modelos)"
    echo "💡 Uso: tron5 openrouter modelo --see  (para ver características)"
else
    echo "⚠️  No se pudo crear enlace simbólico automáticamente"
    echo "💡 Para usar TRON v5.0, ejecuta directamente:"
    echo "   $SCRIPT_DIR/tron_nuevo --router"
    echo "   $SCRIPT_DIR/tron_nuevo openrouter modelo --see"
fi

echo ""
echo "📋 Características de TRON v5.0:"
echo "   • Menú interactivo de modelos con emojis y características"
echo "   • Vista detallada de características de modelos (--see)"
echo "   • Búsqueda y filtrado por tipo de modelo"
echo "   • Cache local de información de modelos (actualizado diariamente)"
echo "   • Compatible con Claude Code y otros clientes"
echo "   • Sin contabilidad de tokens ni costos - solo selección de modelos"
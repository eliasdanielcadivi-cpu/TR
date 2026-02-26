#!/bin/bash
# TR: Script de Instalación Atómica
# Basado en UV y directivas de Higiene Organizacional

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🛠  Configurando entorno virtual en $PROJECT_ROOT/venv..."

# Asegurar que uv está instalado (asumiendo presencia en el sistema o via curl)
if ! command -v uv &> /dev/null; then
    echo "❌ Error: UV no está instalado. Por favor instálalo con: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Sincronizar dependencias
uv sync

# Ajustar venv para que sea visible (si uv creó .venv por defecto)
if [ -d ".venv" ]; then
    mv .venv venv
    echo "virtual-env = 'venv'" >> uv.toml
fi

echo "✅ Entorno TR listo."
echo "🚀 Para activar el comando global 'tr', ejecuta: ini"

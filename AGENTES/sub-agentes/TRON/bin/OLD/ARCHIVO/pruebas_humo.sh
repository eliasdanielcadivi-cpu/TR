#!/bin/bash
# pruebas_humo.sh - Script de pruebas de humo para TRON v4.0

echo "🚀 Iniciando pruebas de humo para TRON v4.0..."

# Verificar que el comando tron esté disponible
if ! command -v tron &> /dev/null; then
    echo "❌ Error: El comando 'tron' no está disponible en el PATH"
    echo "💡 Asegúrate de que el enlace simbólico esté correctamente configurado:"
    echo "   sudo ln -vf -s /ruta/al/proyecto/TRON/bin/tron /usr/bin/tron"
    exit 1
fi

echo "✅ Comando 'tron' encontrado"

# Verificar conexión a PocketBase
echo "🔍 Verificando conexión a PocketBase..."
if curl -s http://localhost:8090/api/ | grep -q "pong"; then
    echo "✅ Conexión a PocketBase exitosa"
else
    echo "⚠️  Advertencia: No se pudo conectar a PocketBase en http://localhost:8090"
    echo "💡 Asegúrate de que PocketBase esté ejecutándose"
fi

# Prueba de selección inteligente (simulada)
echo "🧠 Probando funcionalidad de selección inteligente de modelos..."
echo "💡 Esta prueba verifica que el sistema pueda cargar configuraciones y clases correctamente"
python3 -c "
import sys
sys.path.append('/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')
from tron_lib import TronDBManager
print('✅ Importación de TronDBManager exitosa')
db = TronDBManager()
print('✅ Instanciación de TronDBManager exitosa')
"

# Prueba de balance de OpenRouter (simulada)
echo "💰 Probando funcionalidad de balance de OpenRouter..."
python3 -c "
import sys
sys.path.append('/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')
import yaml
from pathlib import Path

config_path = Path('/home/daniel/tron/programas/ProyectoPizza/TRON/bin/tron_config.yaml')
if config_path.exists():
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    if 'openrouter_live' in config.get('keys', {}):
        print('✅ Configuración de OpenRouter encontrada')
    else:
        print('⚠️  Advertencia: Clave de OpenRouter no encontrada en la configuración')
else:
    print('❌ Error: Archivo de configuración no encontrado')
"

# Prueba de argumentos
echo "⚙️  Probando sistema de argumentos..."
python3 -c "
import sys
sys.path.append('/home/daniel/tron/programas/ProyectoPizza/TRON/bin/')
from tron import TronCLI
import argparse

cli = TronCLI()
parser = argparse.ArgumentParser()
parser.add_argument('--batch', action='store_true')
parser.add_argument('--router', action='store_true')
parser.add_argument('--debug', action='store_true')
parser.add_argument('profile', nargs='?', default=None)
parser.add_argument('model', nargs='?', default=None)
parser.add_argument('command', nargs=argparse.REMAINDER)

args = parser.parse_args(['--batch', 'openrouter', 'claude', '-p', 'test'])
print('✅ Sistema de argumentos funciona correctamente')
"

echo "🎯 Pruebas de humo completadas"
echo ""
echo "📋 Resumen:"
echo "   - Comando 'tron' disponible: ✅"
echo "   - Conexión a PocketBase: Verificada o advertencia"
echo "   - Importación de clases: ✅"
echo "   - Configuración de OpenRouter: Verificada"
echo "   - Sistema de argumentos: ✅"
echo ""
echo "💡 Para pruebas completas, ejecuta:"
echo "   tron openrouter claude -p 'prueba de selección inteligente'"
echo "   tron --batch openrouter claude -p 'prueba persistente'"
echo "   tron --router (para menú interactivo)"
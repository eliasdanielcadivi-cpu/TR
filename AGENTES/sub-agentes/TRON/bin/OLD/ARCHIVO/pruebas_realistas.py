#!/usr/bin/env python3
"""
Script de pruebas realistas para TRON v4.0
Verifica el funcionamiento real de las APIs y LLMs
"""

import asyncio
import sys
import subprocess
import os
from pathlib import Path

def test_claude_connection():
    """Prueba la conexión básica con Claude"""
    print("🔍 Prueba 1: Conexión con Claude...")
    try:
        # Intentar ejecutar claude con un prompt simple
        result = subprocess.run([
            'claude', '-v'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Claude está instalado y accesible: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️  Claude no está disponible: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("⚠️  Claude CLI no está instalado o no está en el PATH")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Tiempo de espera agotado para la conexión con Claude")
        return False
    except Exception as e:
        print(f"❌ Error al conectar con Claude: {e}")
        return False

def test_deepseek_api():
    """Prueba la API de DeepSeek directamente"""
    print("\n🔍 Prueba 2: API de DeepSeek...")
    try:
        import requests
        import yaml
        
        # Cargar configuración
        config_path = Path("/home/daniel/tron/programas/ProyectoPizza/TRON/bin/tron_config.yaml")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        api_key = config['keys'].get('deepseek_live')
        if not api_key:
            print("⚠️  Clave de API de DeepSeek no encontrada en la configuración")
            return False
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "Say 'API test successful' in Spanish."}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ API de DeepSeek respondió correctamente: '{content[:50]}...'")
            return True
        else:
            print(f"❌ API de DeepSeek falló con código {response.status_code}: {response.text}")
            return False
            
    except ImportError:
        print("⚠️  Módulo requests no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error al probar la API de DeepSeek: {e}")
        return False

def test_openrouter_api():
    """Prueba la API de OpenRouter directamente"""
    print("\n🔍 Prueba 3: API de OpenRouter...")
    try:
        import requests
        import yaml
        
        # Cargar configuración
        config_path = Path("/home/daniel/tron/programas/ProyectoPizza/TRON/bin/tron_config.yaml")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        api_key = config['keys'].get('openrouter_live')
        if not api_key:
            print("⚠️  Clave de API de OpenRouter no encontrada en la configuración")
            return False
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "openai/gpt-3.5-turbo",  # Usar un modelo más común y disponible
            "messages": [{"role": "user", "content": "Say 'API test successful' in Spanish."}],
            "temperature": 0.7,
            "max_tokens": 100
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ API de OpenRouter respondió correctamente: '{content[:50]}...'")
            return True
        else:
            print(f"❌ API de OpenRouter falló con código {response.status_code}")
            # Mostrar el mensaje de error si está disponible
            try:
                error_msg = response.json().get('error', {}).get('message', 'No error message')
                print(f"   Mensaje de error: {error_msg}")
            except:
                print(f"   Contenido de respuesta: {response.text[:200]}...")
            return False
            
    except ImportError:
        print("⚠️  Módulo requests no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error al probar la API de OpenRouter: {e}")
        return False

def test_headless_claude():
    """Prueba el modo sin cabeza de Claude"""
    print("\n🔍 Prueba 4: Modo sin cabeza de Claude...")
    try:
        # Intentar ejecutar claude en modo sin cabeza con un prompt simple
        # Usar --print-mode para salida sin interacción
        result = subprocess.run([
            'claude', '--print-mode', '-p', 'Responde "Hola desde modo sin cabeza" en español'
        ], capture_output=True, text=True, timeout=60, env=os.environ)

        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"✅ Claude modo sin cabeza funcionando: '{output[:100]}...'")
            return True
        else:
            print(f"⚠️  Claude modo sin cabeza falló: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("⚠️  Claude CLI no está instalado o no está en el PATH")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Tiempo de espera agotado para Claude en modo sin cabeza")
        return False
    except Exception as e:
        print(f"❌ Error al probar Claude en modo sin cabeza: {e}")
        return False

def test_tron_with_real_prompt():
    """Prueba TRON con un prompt real"""
    print("\n🔍 Prueba 5: TRON con prompt real (modo sin cabeza)...")
    try:
        # Usar TRON para ejecutar claude con un prompt real
        # El formato correcto es: tron claude -p "prompt"
        result = subprocess.run([
            'tron', 'claude', '-p', 'Responde "TRON test exitoso" en español'
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"✅ TRON con prompt real funcionando: '{output[-200:]}...'")  # Últimos 200 chars
            return True
        else:
            print(f"⚠️  TRON con prompt real falló: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Error al probar TRON con prompt real: {e}")
        return False

async def test_pocketbase_connection():
    """Prueba la conexión con PocketBase"""
    print("\n🔍 Prueba 6: Conexión con PocketBase...")
    try:
        from tron_lib import TronDBManager
        import yaml
        
        # Cargar configuración
        config_path = Path("/home/daniel/tron/programas/ProyectoPizza/TRON/bin/tron_config.yaml")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        db_manager = TronDBManager()
        user = config['keys'].get('pocketbase_user')
        password = config['keys'].get('pocketbase_pass')
        
        if not user or not password:
            print("⚠️  Credenciales de PocketBase no encontradas en la configuración")
            return False
        
        connected = await db_manager.connect(user, password)
        if connected:
            print("✅ Conexión con PocketBase exitosa")
            # Probar que podemos acceder a colecciones
            try:
                collections = await db_manager.client.collections.get_full_list()
                print(f"✅ Acceso a {len(collections)} colecciones en PocketBase")
                return True
            except Exception as e:
                print(f"⚠️  Conexión con PocketBase exitosa pero error al acceder a colecciones: {e}")
                return True  # La conexión en sí es exitosa
        else:
            print("❌ Conexión con PocketBase fallida")
            return False
    except Exception as e:
        print(f"❌ Error al conectar con PocketBase: {e}")
        return False

async def run_realistic_tests():
    """Ejecuta todas las pruebas realistas"""
    print("🧪 Iniciando pruebas realistas de TRON v4.0...\n")
    
    tests_results = []
    
    # Pruebas síncronas
    tests_results.append(test_claude_connection())
    tests_results.append(test_deepseek_api())
    tests_results.append(test_openrouter_api())
    tests_results.append(test_headless_claude())
    tests_results.append(test_tron_with_real_prompt())
    
    # Pruebas asíncronas
    tests_results.append(await test_pocketbase_connection())
    
    # Resumen
    print(f"\n📊 Resumen de pruebas realistas:")
    print(f"   Total de pruebas: {len(tests_results)}")
    print(f"   Pruebas exitosas: {sum(tests_results)}")
    print(f"   Pruebas fallidas: {len(tests_results) - sum(tests_results)}")
    
    if all(tests_results):
        print("\n🎉 ¡Todas las pruebas realistas han sido exitosas!")
        print("   TRON v4.0 está completamente funcional con APIs y LLMs reales.")
        return True
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los mensajes anteriores para más detalles.")
        print("   Esto puede ser debido a claves API incorrectas, falta de conexión, etc.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_realistic_tests())
    sys.exit(0 if success else 1)
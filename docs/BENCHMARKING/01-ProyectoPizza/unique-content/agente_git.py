import ollama
import subprocess
import json
import sys
import os
from pathlib import Path

# --- CONFIGURACIÓN DE PORTABILIDAD ---
# Calculamos la ruta absoluta de la herramienta basándonos en la ubicación de ESTE script
BASE_DIR = Path(__file__).resolve().parent
TOOL_PATH = BASE_DIR / "herramientas" / "gestor_git_cli.py"

def herramienta_git_tron(accion: str, argumento: str = ""):
    """
    Ejecuta comandos de git seguros (guardar, volver, nube).
    
    Args:
      accion: 'guardar', 'volver', o 'nube'.
      argumento: Mensaje para guardar o número de pasos para volver.
    """
    # Verificamos que la herramienta exista
    if not TOOL_PATH.exists():
        return json.dumps({"estado": "error", "mensaje": f"Herramienta no encontrada en: {TOOL_PATH}"})

    # Construimos el comando usando el MISMO intérprete de Python (el del venv)
    cmd = [sys.executable, str(TOOL_PATH), accion]
    
    if accion == "guardar" and argumento:
        cmd.extend(["-m", argumento])
    elif accion == "volver" and argumento:
        cmd.extend(["-p", str(argumento)])
    
    try:
        # Ejecución silenciosa, capturando solo el JSON de salida
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Intentamos parsear la salida como JSON para asegurar limpieza
        try:
            output_json = json.loads(result.stdout)
            return json.dumps(output_json) # Re-serializar para el LLM
        except json.JSONDecodeError:
            # Si falló el script y no devolvió JSON (ej: error de sintaxis python)
            return json.dumps({
                "estado": "error_critico", 
                "raw_output": result.stdout.strip(),
                "stderr": result.stderr.strip()
            })
            
    except Exception as e:
        return json.dumps({"estado": "excepcion", "mensaje": str(e)})

# --- BUCLE PRINCIPAL DEL AGENTE ---
def main():
    model = 'functiongemma:270m' # Asegúrate que este sea el nombre correcto en 'ollama list'
    
    print(f"🚀 TRON GIT AGENTE (Modelo: {model})")
    print(f"📂 Contexto: {BASE_DIR}")
    print("Escribe 'salir' para terminar.\n")

    messages = []

    while True:
        try:
            user_input = input("👤 Tú: ")
            if user_input.lower() in ['salir', 'exit']: break
            
            messages.append({'role': 'user', 'content': user_input})

            # 1. Consultar al LLM
            response = ollama.chat(
                model=model,
                messages=messages,
                tools=[herramienta_git_tron]
            )

            # 2. Verificar uso de herramientas
            if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    fn_name = tool.function.name
                    args = tool.function.arguments
                    
                    print(f"⚙️  [SISTEMA] Ejecutando: {fn_name} {args}")
                    
                    # Ejecutar función Python local
                    if fn_name == 'herramienta_git_tron':
                        resultado = herramienta_git_tron(**args)
                        
                        # Inyectar resultado como mensaje de herramienta
                        messages.append(response.message)
                        messages.append({
                            'role': 'tool',
                            'content': resultado,
                        })
                        
                        # Segunda llamada para que el LLM interprete el resultado
                        final_resp = ollama.chat(model=model, messages=messages)
                        print(f"🤖 IA: {final_resp.message.content}")
            else:
                print(f"🤖 IA: {response.message.content}")
                messages.append(response.message)

        except KeyboardInterrupt:
            print("\nCerrando sistema...")
            break
        except Exception as e:
            print(f"❌ Error en el bucle: {e}")

if __name__ == "__main__":
    main()

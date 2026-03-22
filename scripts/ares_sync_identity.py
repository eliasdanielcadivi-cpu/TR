#!/usr/bin/env python3
import os
import yaml
import subprocess
import time
import signal
import sys
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS ---
TR_ROOT = Path("/home/daniel/tron/programas/TR")
CONFIG_PATH = TR_ROOT / "config/identidad/ares.yaml"
TRON_BIN = TR_ROOT / "AGENTES/sub-agentes/TRON/bin/tron.py"

def load_identity():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def update_documentation(definition, targets):
    """Usa TRON para inyectar la definición en documentos Markdown."""
    print("🧠 Inyectando identidad en documentación vía TRON...")
    for target in targets:
        path = Path(target['path'])
        if not path.exists():
            print(f"⚠️  Archivo no encontrado: {path}")
            continue

        # Leemos el archivo actual
        with open(path, "r") as f:
            content = f.read()

        # Prompt para TRON (Headless)
        # Queremos que TRON reemplace quirúrgicamente lo que está entre marcadores
        marker = target['marker']
        instruction = f"""
        Actúa como un editor quirúrgico de archivos.
        Tu tarea es reemplazar el texto de la definición de ARES en el archivo proporcionado.
        
        NUEVA DEFINICIÓN:
        {definition}
        
        REGLAS:
        1. Localiza la sección de la definición de ARES (normalmente al inicio o bajo un encabezado).
        2. Si existen marcadores {marker}, reemplaza TODO lo que haya entre ellos.
        3. Si NO existen marcadores, busca la definición antigua y sustitúyela.
        4. DEVUELVE EL ARCHIVO COMPLETO con el cambio realizado.
        5. NO añadas comentarios ni explicaciones, solo el contenido del archivo.
        """

        # Llamada a TRON (usando deepseek para precisión en edición)
        # Nota: Ajustamos los argumentos según la CLI de tu TRON
        cmd = ["uv", "run", "--project", str(TRON_BIN.parent), "python", str(TRON_BIN), 
               "deepseek", "claude", "-p", f"{instruction}\n\nCONTENIDO DEL ARCHIVO:\n{content}"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            new_content = result.stdout.strip()
            
            # Guardamos el archivo actualizado
            if new_content and len(new_content) > 100: # Validación mínima
                with open(path, "w") as f:
                    f.write(new_content)
                print(f"✅ Documento actualizado: {path.name}")
        except Exception as e:
            print(f"❌ Error al procesar {path.name}: {e}")

def update_modelfiles(definition, targets):
    """Actualiza la instrucción SYSTEM en los Modelfiles de Ollama."""
    print("📝 Actualizando Modelfiles...")
    for target in targets:
        path = Path(target['path'])
        if not path.exists():
            print(f"⚠️  Modelfile no encontrado: {path}")
            continue

        with open(path, "r") as f:
            lines = f.readlines()

        new_lines = []
        in_system = False
        system_written = False
        
        for line in lines:
            if line.strip().startswith("SYSTEM"):
                in_system = True
                if not system_written:
                    new_lines.append(f'SYSTEM """\n{definition}\n"""\n')
                    system_written = True
                continue
            
            if in_system:
                if '"""' in line:
                    in_system = False
                continue
            
            new_lines.append(line)

        with open(path, "w") as f:
            f.writelines(new_lines)
        print(f"✅ Modelfile actualizado: {path.name}")

def manage_ollama(targets):
    """Gestiona el ciclo de vida de Ollama para recrear los modelos."""
    print("🐋 Gestionando modelos en Ollama...")
    
    # 1. Verificar/Iniciar Ollama Serve
    ollama_proc = None
    try:
        subprocess.run(["pgrep", "ollama"], check=True, capture_output=True)
        print("ℹ️  Ollama ya está corriendo.")
    except subprocess.CalledProcessError:
        print("🚀 Iniciando Ollama serve...")
        ollama_proc = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5) # Esperar a que levante

    # 2. Recrear modelos
    for target in targets:
        model_name = target['model_name']
        modelfile = target['path']
        print(f"🔄 Recreando modelo: {model_name}...")
        subprocess.run(["ollama", "rm", model_name], capture_output=True)
        subprocess.run(["ollama", "create", model_name, "-f", modelfile], check=True)
        print(f"✅ Modelo {model_name} listo.")

    # 3. Limpiar
    if ollama_proc:
        print("🛑 Deteniendo Ollama serve...")
        ollama_proc.terminate()
        ollama_proc.wait()

def main():
    data = load_identity()
    definition = data['definition']
    
    # 1. Modelfiles (Determinista)
    update_modelfiles(definition, data['injection_targets']['ai_infrastructure'])
    
    # 2. Ollama (Determinista)
    manage_ollama(data['injection_targets']['ai_infrastructure'])
    
    # 3. Documentación (Inferencial vía TRON)
    update_documentation(definition, data['injection_targets']['documentation'])

if __name__ == "__main__":
    main()

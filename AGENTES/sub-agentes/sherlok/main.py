#!/usr/bin/env python3
"""
🕵️ SHERLOK - Sub-Agente Forense de ARES
======================================

Sherlok es el 'Ojo' de ARES. Su misión es escanear tu laptop en busca de 
scripts y programas propios, analizarlos semánticamente con modelos de lenguaje 
locales (Ollama) y generar documentación automática en el sistema de AYUDA.

CAPACIDADES:
1. Inferencia Multimodelo: Usa especialistas (Codellama-Python) para código.
2. Pensamiento en Vivo: Muestra el flujo de razonamiento en la terminal.
3. Clasificación Determinista: Solo acepta temas técnicos relevantes para ARES.
4. Modo Sigilo: Ejecución en background con prioridad ultra-baja.

USO:
  sherlok --lista              # Analiza rutas en prioritarios.txt
  sherlok --directorio [Ruta]  # Escaneo recursivo inteligente
"""

import click
import os
import yaml
from pathlib import Path
from brain import SherlokBrain
from scanner import SherlokScanner
from rich.console import Console

console = Console()

# Carga de configuración centralizada
BASE_DIR = Path(__file__).parent.resolve()
with open(BASE_DIR / "config.yaml", "r") as f:
    config = yaml.safe_load(f)

@click.command()
@click.option("--lista", "-l", is_flag=True, help="Procesa rutas desde prioritarios.txt")
@click.option("--directorio", "-d", type=click.Path(exists=True), help="Escanea recursivamente una ruta")
@click.option("--model", "-m", help="Fuerza un modelo específico (alias)")
@click.option("--background", "-b", is_flag=True, help="Ejecuta con prioridad baja (nice -n 19)")
def main(lista, directorio, model, background):
    """Orquestador principal de Sherlok."""
    
    if background:
        os.nice(19)
        console.print("[dim]🌙 Sherlok operando en modo sigilo (prioridad baja)...[/dim]")

    brain = SherlokBrain(config)
    scanner = SherlokScanner(config['paths']['ignore'])

    target_paths = []

    # 1. Recopilación de rutas
    if lista:
        list_file = BASE_DIR / "prioritarios.txt"
        if list_file.exists():
            with open(list_file, "r") as f:
                target_paths.extend([line.strip() for line in f if line.strip()])
    
    if directorio:
        # Añadir lógica de escaneo de carpetas nivel 1 (proyectos)
        for item in os.listdir(directorio):
            path = Path(directorio) / item
            if path.name not in config['paths']['ignore']:
                target_paths.append(str(path))

    if not target_paths:
        console.print("[yellow]⚠ No hay rutas para analizar. Usa --help para ver opciones.[/yellow]")
        return

    # 2. Ciclo de Análisis y Generación
    for path in target_paths:
        console.print(f"
[bold blue]🔍 Analizando:[/bold blue] {path}")
        
        data = scanner.scan_path(path)
        if not data: continue

        # Inferencia
        analysis = brain.analyze(data, is_python=data['is_python'], forced_model=model)
        
        if analysis:
            # Guardar en AYUDA
            output_name = f"{data['name']}.md"
            output_path = Path(config['paths']['output']) / output_name
            
            with open(output_path, "w") as f:
                f.write(analysis)
            
            console.print(f"[bold green]✅ Indexado en:[/bold green] {output_path}")

if __name__ == "__main__":
    main()

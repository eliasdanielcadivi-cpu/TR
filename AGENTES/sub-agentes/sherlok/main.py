#!/usr/bin/env python3
"""
🕵️ SHERLOK V2.2 - Auditoría JSON Industrial (Pydantic Solid)
==========================================================

Sherlok es el 'Ojo' de ARES. Misión: Escanear, analizar e indexar 
programas locales en un Inventario Maestro JSON validado.

Uso:
  sherlok --lista              # Analiza programas prioritarios
  sherlok --directorio [Ruta]  # Escaneo masivo
  sherlok --file [Archivo]     # Análisis quirúrgico
"""

import click
import os
import yaml
import json
import sys
from pathlib import Path
from brain import SherlokBrain
from scanner import SherlokScanner
from rich.console import Console

console = Console()
BASE_DIR = Path(__file__).parent.resolve()

def build_master_inventory(output_dir):
    """Reconstruye el inventario.json consolidando todos los hallazgos."""
    inventory_path = Path(output_dir) / "inventario.json"
    programas = []
    for file in Path(output_dir).glob("*.json"):
        if file.name == "inventario.json": continue
        try:
            with open(file, "r") as f:
                programas.append(json.load(f))
        except: continue
    with open(inventory_path, "w") as f:
        json.dump({"programas": programas}, f, indent=2)
    console.print(f"[bold magenta]📊 Inventario Maestro actualizado: {inventory_path}[/bold magenta]")

@click.command()
@click.option("--lista", "-l", is_flag=True, help=f"Analiza rutas en {BASE_DIR}/prioritarios.txt")
@click.option("--directorio", "-d", type=click.Path(exists=True), help="Escaneo recursivo de una carpeta de proyectos")
@click.option("--file", "-f", type=click.Path(exists=True), help="Auditoría quirúrgica de un solo archivo")
@click.option("--model", "-m", help="Fuerza alias de modelo (qwenCoderInstruc, deepseekr1, etc.)")
@click.option("--background", "-b", is_flag=True, help="Ejecución en segundo plano (nice -n 19)")
def main(lista, directorio, file, model, background):
    """Orquestador forense para el mapeo de activos digitales."""
    if background: 
        os.nice(19)
        console.print("[dim]🌙 Modo sigilo activado.[/dim]")
    
    try:
        with open(BASE_DIR / "config.yaml", "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[bold red]❌ Error de config: {e}[/bold red]")
        return

    brain = SherlokBrain(config)
    scanner = SherlokScanner(config['paths']['ignore'])
    target_paths = []

    if lista:
        list_file = BASE_DIR / "prioritarios.txt"
        if list_file.exists():
            with open(list_file, "r") as f:
                target_paths.extend([line.strip() for line in f if line.strip()])
    
    if file: target_paths.append(str(Path(file).absolute()))
    
    if directorio:
        for item in os.listdir(directorio):
            path = Path(directorio) / item
            if path.name not in config['paths']['ignore']:
                target_paths.append(str(path))

    if not target_paths:
        console.print("[yellow]⚠ Sin objetivos. Usa --help para ver opciones.[/yellow]")
        return

    output_dir = Path(config['paths']['output'])
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in target_paths:
        console.print(f"\n[bold blue]🔍 Auditando:[/bold blue] {path}")
        data = scanner.scan_path(path)
        if not data: continue

        # Inferencia con Validación Pydantic y Auto-Corrección interna
        analysis_json = brain.analyze(data, is_python=data['is_python'], forced_model=model)
        
        if analysis_json:
            output_path = output_dir / f"{data['name']}.json"
            with open(output_path, "w") as f:
                f.write(analysis_json)
            console.print(f"[bold green]✅ Auditado: {data['name']}[/bold green]")

    build_master_inventory(output_dir)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import click
import os
import yaml
import json
import hashlib
from pathlib import Path
from brain import SherlokBrain
from scanner import SherlokScanner
from persistence import init_db, get_stored_fingerprint, update_scan_record
from rich.console import Console

console = Console()
BASE_DIR = Path(__file__).parent.resolve()

def build_master_inventory(output_dir):
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
    console.print(f"[bold magenta]📊 Inventario Maestro: {inventory_path}[/bold magenta]")

@click.command()
@click.option("--lista", "-l", is_flag=True)
@click.option("--directorio", "-d", type=click.Path(exists=True))
@click.option("--file", "-f", type=click.Path(exists=True))
@click.option("--model", "-m")
@click.option("--background", "-b", is_flag=True)
@click.option("--force", is_flag=True)
def main(lista, directorio, file, model, background, force):
    if background: os.nice(19)
    init_db()

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

    if not target_paths: return

    output_dir = Path(config['paths']['output'])
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in target_paths:
        console.print(f"\n[bold blue]🔍 Verificando objetivo:[/bold blue] {path}")
        data = scanner.scan_path(path)
        if not data: continue

        # --- LÓGICA DE DOBLE PASO DETERMINISTA ---
        output_file = output_dir / f"{data['name']}.json"
        
        content_to_hash = f"{data.get('structure', '')}{data.get('help_text', '')}{data.get('source_sample', '')}"
        current_fp = hashlib.sha256(content_to_hash.encode()).hexdigest()
        stored_fp = get_stored_fingerprint(path)

        # Solo saltamos si: No hay force Y el fingerprint coincide Y el archivo físico existe
        if not force and stored_fp == current_fp and output_file.exists():
            console.print(f"[bold yellow]⏭️  Sin cambios y archivo presente. Saltando: {data['name']}[/bold yellow]")
            continue

        # Inferencia IA
        analysis_json = brain.analyze(data, is_python=data['is_python'], forced_model=model)
        
        if analysis_json:
            # Generar un nombre de archivo más robusto (ej: MarcadorDeVideos_main.py.json)
            safe_name = path.replace("/", "_").strip("_")
            if len(safe_name) > 100: # Limitar si la ruta es extrema
                safe_name = hashlib.md5(path.encode()).hexdigest()
            
            output_file = output_dir / f"{safe_name}.json"
            
            with open(output_file, "w") as f:
                f.write(analysis_json)
            update_scan_record(path, data)
            console.print(f"[bold green]✅ Auditado y guardado en: {output_file.name}[/bold green]")

    build_master_inventory(output_dir)

if __name__ == "__main__":
    main()

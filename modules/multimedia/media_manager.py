import os
import subprocess
from rich.console import Console

console = Console()

class MediaManager:
    """Gestor de reproducción multimedia en terminal."""
    
    def __init__(self, context):
        self.ctx = context

    def play_video(self, archivo, **kwargs):
        """Reproduce video usando mpv y protocolo kitty."""
        mpv_conf = os.path.join(self.ctx.base_path, "config/mpv/mpv.conf")
        
        cmd = [
            "mpv",
            f"--config={mpv_conf}",
            "--profile=sw-fast",
            "--vo=kitty",
            "--vo-kitty-use-shm=yes",
            "--really-quiet",
        ]
        
        if kwargs.get('sub'): cmd.append(f"--sub-file={kwargs['sub']}")
        if kwargs.get('start'): cmd.append(f"--start={kwargs['start']}")
        if kwargs.get('loop'): cmd.append("--loop-file=inf")
        if kwargs.get('speed') != 1.0: cmd.append(f"--speed={kwargs['speed']}")
        if kwargs.get('volume') != 80: cmd.append(f"--volume={kwargs['volume']}")
        if kwargs.get('audio_only'): cmd.append("--vid=no")
        
        cmd.append(archivo)
        
        console.print(f"[bold cyan]🎬 Reproduciendo:[/bold cyan] {archivo}")
        subprocess.run(cmd)

    def show_image(self, archivos, **kwargs):
        """Muestra imágenes usando icat."""
        if kwargs.get('clear'):
            print("\033[3J", end="")
            console.print("[bold green]✓ Imágenes limpiadas[/bold green]")
            return

        cmd = ["kitten", "icat"]
        if kwargs.get('grid'): cmd.append("--grid")
        if kwargs.get('width'): cmd.append(f"--width={kwargs['width']}")
        if kwargs.get('align'): cmd.append(f"--align={kwargs['align']}")
        if kwargs.get('scale_up'): cmd.append("--scale-up")
        
        cmd.extend(archivos)
        
        console.print(f"[bold cyan]🖼️  Mostrando {len(archivos)} imagen(es)[/bold cyan]")
        subprocess.run(cmd)

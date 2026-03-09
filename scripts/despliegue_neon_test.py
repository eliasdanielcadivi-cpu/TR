#!/usr/bin/env python3
import subprocess
import time
import os
from pathlib import Path

# Configuración de Colores (Hacker Neon)
PALETTE = {
    'GEMINI':  {'fg': '#00FFFF', 'bg': '#001A1A'},
    'QWEN':    {'fg': '#FF00FF', 'bg': '#1A001A'},
    'COMANDO': {'fg': '#39FF14', 'bg': '#0A1A0A'},
    'NOTAS':   {'fg': '#FF6600', 'bg': '#1A0D00'},
    'AGENDA':  {'fg': '#FF0000', 'bg': '#1A0000'},
    'BR':      {'fg': '#0000FF', 'bg': '#00001A'}
}

PAPELERA = Path("/home/daniel/tron/programas/TR/papelera")

def launch_tab_with_color(title, color_key, cmd=None):
    colors = PALETTE[color_key]
    
    # 1. Lanzar pestaña
    # Si hay comando, lo ejecutamos y dejamos la shell abierta con --hold si fuera necesario, 
    # pero aquí usaremos inyección de texto para ver la terminal "viva"
    launch_args = ["kitty", "@", "launch", "--type=tab", f"--tab-title={title}", "--keep-focus"]
    subprocess.run(launch_args)
    
    # 2. Aplicar color a la pestaña recién creada (usando match por título)
    color_args = [
        "kitty", "@", "set-tab-color", 
        "--match", f"title:^{title}$",
        f"active_fg={colors['fg']}",
        f"active_bg={colors['bg']}",
        f"inactive_fg={colors['fg']}",
        f"inactive_bg='#000000'"
    ]
    subprocess.run(color_args)
    
    # 3. Ejecutar comando si existe y validar en papelera
    if cmd:
        time.sleep(0.5)
        test_file = PAPELERA / f"test_{title.lower()}.txt"
        # Comando que ejecuta el real + rastro en papelera
        full_cmd = f"{cmd}; echo 'EXEC_OK_{title}' > {test_file}\n"
        subprocess.run(["kitty", "@", "send-text", "--match", f"title:^{title}$", full_cmd])

def main():
    # Limpiar papelera
    for f in PAPELERA.glob("test_*.txt"):
        f.unlink()

    print("🚀 Iniciando Despliegue Visual Hacker Neon...")
    
    # Crear una nueva OS Window para que el usuario la vea
    subprocess.run(["kitty", "--title", "ARES_EXPERIMENTAL", "sh", "-c", "exit"])
    time.sleep(1) # Esperar a que la ventana se registre
    
    # Orden solicitado
    launch_tab_with_color("GEMINI", "GEMINI")
    launch_tab_with_color("QWEN", "QWEN")
    launch_tab_with_color("COMANDO", "COMANDO")
    launch_tab_with_color("NOTAS", "NOTAS", "notas")
    launch_tab_with_color("AGENDA", "AGENDA", "agenda")
    launch_tab_with_color("BR", "BR", "br")

    print("⏳ Validando rastros en papelera...")
    time.sleep(5)
    
    success = True
    for tab in ["NOTAS", "AGENDA", "BR"]:
        if not (PAPELERA / f"test_{tab.lower()}.txt").exists():
            print(f"❌ Falló verificación de: {tab}")
            success = False
    
    if success:
        print("✅ Todos los comandos se ejecutaron correctamente.")
    
    # Preguntar al usuario
    res = subprocess.run([
        "zenity", "--question", 
        "--text", "🚀 ¿Ves la ventana de Kitty con las pestañas Neón y los programas cargados?\n\n(Acepta si funcionó, Cancela si algo falló)",
        "--title", "ARES - Validación Experimental"
    ])
    
    if res.returncode == 0:
        print("🎉 El usuario confirma éxito operacional.")
    else:
        print("☢️ El usuario reporta fallo. Iniciando diagnóstico...")

if __name__ == "__main__":
    main()

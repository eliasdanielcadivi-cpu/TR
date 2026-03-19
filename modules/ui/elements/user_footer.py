#!/usr/bin/env python3
import sys
import yaml
import subprocess
from pathlib import Path

ELEMENTS_DIR = Path(__file__).parent
CONFIG_PATH = ELEMENTS_DIR / "elements_config.yaml"
CACHE_DIR = ELEMENTS_DIR.parent.parent.parent / "papelera" / ".cache_elements"

class DragonScaler:
    @staticmethod
    def prepare(input_path, target_w, target_h):
        if not CACHE_DIR.exists(): CACHE_DIR.mkdir(parents=True)
        cache_name = f"{Path(input_path).stem}_{target_w}_{target_h}.gif"
        cache_path = CACHE_DIR / cache_name
        if cache_path.exists(): return str(cache_path)
        px_w, px_h = target_w * 10, target_h * 20
        cmd = ["convert", input_path, "-coalesce", "-resize", f"{px_w}x{px_h}!", "-layers", "Optimize", str(cache_path)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return str(cache_path)
        except: return input_path

def main():
    with open(CONFIG_PATH, "r") as f: cfg = yaml.safe_load(f)
    identity = "user" # Archivo específico para usuario
    foot = cfg[identity]['footer']
    
    path = DragonScaler.prepare(foot['path'], foot['width'], foot['height'])
    subprocess.run(["kitten", "icat", "--scale-up", "--background=none", "--loop", "-1", path])
    print("\n\n\n")

if __name__ == "__main__": main()

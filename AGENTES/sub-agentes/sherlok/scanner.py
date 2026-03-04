import os
import subprocess
from pathlib import Path

class SherlokScanner:
    """Ojos de Sherlok: Tree, Help y Código."""
    
    def __init__(self, ignore_patterns):
        self.ignore = ignore_patterns

    def scan_path(self, path):
        """Captura toda la info posible de una ruta."""
        p = Path(path)
        if not p.exists(): return None

        data = {
            "name": p.name,
            "abs_path": str(p.absolute()),
            "structure": self._get_tree(p),
            "is_python": self._check_python(p),
            "help_text": self._get_help(p),
            "source_sample": self._get_source(p)
        }
        return data

    def _get_tree(self, path):
        try:
            res = subprocess.run(["tree", "-L", "3", str(path)], capture_output=True, text=True)
            return res.stdout
        except:
            return "Tree no disponible"

    def _check_python(self, path):
        if path.is_file() and path.suffix == ".py": return True
        # Check si es carpeta con main.py
        if path.is_dir() and (path / "main.py").exists(): return True
        return False

    def _get_help(self, path):
        # Intentar ejecutar --help si es archivo ejecutable
        if path.is_file() and os.access(path, os.X_OK):
            try:
                res = subprocess.run([str(path), "--help"], capture_output=True, text=True, timeout=2)
                return res.stdout
            except:
                pass
        return "No disponible"

    def _get_source(self, path):
        # Leer primeras 100 líneas si es archivo legible
        target = path if path.is_file() else (path / "main.py" if (path / "main.py").exists() else None)
        if target and target.exists():
            try:
                with open(target, 'r') as f:
                    return "".join(f.readlines()[:100])
            except:
                pass
        return ""

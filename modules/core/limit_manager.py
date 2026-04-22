"""
Gestor de Límites - ARES-TRON.
Monitoreo de recursos y advertencias configurables.
"""
import yaml
import os
import psutil
import shutil

class LimitManager:
    def __init__(self, config_path="/home/daniel/tron/programas/TR/config/limits.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def check_resources(self):
        """Verifica RAM y retorna advertencias si superan los umbrales."""
        warnings = []
        
        # RAM Check
        ram = psutil.virtual_memory()
        threshold_pct = self.config.get('hardware', {}).get('warning_threshold_ram_percent', 85)
        
        if ram.percent > threshold_pct:
            warnings.append(self.config.get('messages', {}).get('ram_warning', "⚠️ RAM alta detectada."))

        # GPU Check (Sencillo: verificar nvidia-smi)
        gpu_enabled = self.config.get('hardware', {}).get('gpu_enabled', False)
        if gpu_enabled:
            # Lógica futura para GPU
            pass
        else:
            if not shutil.which("nvidia-smi"):
                # No warning needed if already using CPU, but could be info
                pass

        return warnings

    def get_limit(self, key, default):
        """Obtiene un límite específico."""
        return self.config.get('limits', {}).get(key, default)

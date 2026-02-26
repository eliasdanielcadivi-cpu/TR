import os
import yaml

class TRContext:
    """Funcionalidades 1-3: Carga, Guardado y Gestión de Rutas."""
    def __init__(self):
        self.base_path = os.path.expanduser("~/tron/programas/TR")
        self.config_path = f"{self.base_path}/config/config.yaml"
        self.socket = "unix:/tmp/mykitty"
        self.socket_path = "/tmp/mykitty"
        self.handshake_file = "/tmp/tron_handshake.txt"
        self.kitty_conf = f"{self.base_path}/config/kitty.conf"
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return {'ai': {'enabled': True, 'ollama': {'model': 'gemma3:4b'}, 'aliases': {'gemma': {'provider': 'ollama', 'model': 'gemma3:4b'}}}}
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def save_config(self):
        import yaml
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)

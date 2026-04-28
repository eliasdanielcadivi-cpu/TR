import json
import os
from datetime import datetime

class TorrentVault:
    def __init__(self, base_path="/home/daniel/tron/programas/TR"):
        self.inv_path = os.path.join(base_path, "db/multimedia/inventario.json")
        self.mag_path = os.path.join(base_path, "db/multimedia/magnets.json")
        self.torrent_dir = os.path.join(base_path, "assets/torrents")

    def registrar_magnet(self, titulo, magnet):
        try:
            with open(self.mag_path, 'r') as f:
                magnets = json.load(f)
            magnets[titulo] = {
                "magnet": magnet,
                "fecha_registro": datetime.now().isoformat()
            }
            with open(self.mag_path, 'w') as f:
                json.dump(magnets, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error registrando magnet: {e}")
            return False

    def actualizar_inventario(self, item_data):
        """
        item_data: {titulo, serie, temporada, capitulo, calidad_esperada, status}
        """
        try:
            with open(self.inv_path, 'r') as f:
                inv = json.load(f)
            
            # Buscar si ya existe para actualizar o añadir
            found = False
            for item in inv["items"]:
                if item["titulo"] == item_data["titulo"]:
                    item.update(item_data)
                    item["ultima_modificacion"] = datetime.now().isoformat()
                    found = True
                    break
            
            if not found:
                item_data["fecha_descarga"] = datetime.now().isoformat()
                item_data["reseña_arquitecto"] = ""
                item_data["calidad_real"] = ""
                inv["items"].append(item_data)
                
            with open(self.inv_path, 'w') as f:
                json.dump(inv, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error actualizando inventario: {e}")
            return False

    def obtener_pendientes(self):
        with open(self.inv_path, 'r') as f:
            inv = json.load(f)
        return [i for i in inv["items"] if i.get("status") != "exitoso"]

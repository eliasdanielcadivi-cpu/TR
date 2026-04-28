import json
import os
import hashlib
from datetime import datetime

class MultimediaMemory:
    def __init__(self, base_path="/home/daniel/tron/programas/TR"):
        self.master_path = os.path.join(base_path, "db/multimedia/master_catalog.json")
        self.history_path = os.path.join(base_path, "db/multimedia/torrent_history.json")

    def _get_id(self, serie, temporada, capitulo):
        # Crear un ID inmutable: serie_s02e01
        return f"{serie.lower().replace(' ', '_')}_{temporada.lower()}{capitulo.lower()}"

    def registrar_identidad(self, serie, temporada, capitulo):
        with open(self.master_path, 'r+') as f:
            data = json.load(f)
            obj_id = self._get_id(serie, temporada, capitulo)
            if obj_id not in data["identidades"]:
                data["identidades"][obj_id] = {
                    "serie": serie,
                    "temporada": temporada,
                    "capitulo": capitulo,
                    "fecha_creacion": datetime.now().isoformat(),
                    "status_global": "pendiente"
                }
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        return obj_id

    def registrar_torrent(self, obj_id, magnet, uploader, size_gb, seeders):
        # El InfoHash es la huella digital inmutable del torrent
        info_hash = self._extract_hash(magnet)
        
        with open(self.history_path, 'r+') as f:
            data = json.load(f)
            if info_hash not in data["torrents"]:
                data["torrents"][info_hash] = {
                    "parent_id": obj_id,
                    "magnet": magnet,
                    "uploader": uploader,
                    "size_gb": size_gb,
                    "first_seen": datetime.now().isoformat(),
                    "last_seeders": seeders,
                    "status": "vivo"
                }
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        return info_hash

    def buscar_vehiculo_vivo(self, serie, temporada, capitulo):
        obj_id = self._get_id(serie, temporada, capitulo)
        with open(self.history_path, 'r') as f:
            data = json.load(f)
            # Buscar torrents asociados a este ID que sigan vivos
            vivos = [t for t in data["torrents"].values() if t["parent_id"] == obj_id and t["status"] == "vivo"]
            return vivos[0] if vivos else None

    def _extract_hash(self, magnet):
        try:
            if "btih:" in magnet:
                return magnet.split("btih:")[1].split("&")[0].upper()
            return hashlib.sha1(magnet.encode()).hexdigest().upper()
        except:
            return "UNKNOWN"

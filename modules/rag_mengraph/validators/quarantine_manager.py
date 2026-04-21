import hjson
import os
import logging
from typing import List, Dict, Any
from datetime import datetime

# Configuración de Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RAG-Mengraph-Quarantine")

class QuarantineManager:
    def __init__(self, storage_path: str = "/home/daniel/tron/programas/TR/db/rag_mengraph/quarantine.hjson"):
        """
        Inicializa el gestor de cuarentena.
        """
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            self._save_data([])

    def _save_data(self, data: List[Dict[str, Any]]):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            hjson.dump(data, f)

    def _load_data(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.storage_path):
            return []
        with open(self.storage_path, 'r', encoding='utf-8') as f:
            return hjson.load(f)

    def add_to_quarantine(self, items: List[Dict[str, Any]]):
        """
        Añade elementos a la zona de cuarentena con timestamp.
        """
        current_data = self._load_data()
        for item in items:
            item["quarantine_id"] = f"Q-{datetime.now().strftime('%Y%m%d%H%M%S')}-{os.urandom(2).hex()}"
            item["added_at"] = datetime.now().isoformat()
            current_data.append(item)
        
        self._save_data(current_data)
        logger.info(f"Añadidos {len(items)} elementos a Cuarentena.")

    def list_quarantine(self) -> List[Dict[str, Any]]:
        """
        Lista todos los elementos en cuarentena.
        """
        return self._load_data()

    def remove_from_quarantine(self, q_id: str):
        """
        Elimina un elemento de la cuarentena tras aprobación o rechazo.
        """
        current_data = self._load_data()
        new_data = [item for item in current_data if item.get("quarantine_id") != q_id]
        self._save_data(new_data)
        logger.debug(f"Elemento {q_id} removido de Cuarentena.")

if __name__ == "__main__":
    # Prueba del gestor
    qm = QuarantineManager()
    test_items = [
        {"verbo": "PUBLICA_EN_REDES", "razon": "C4 Detectado"},
        {"verbo": "INVENTA_ESTRATEGIA", "razon": "Serendipia Detectada"}
    ]
    
    print("--- Prueba de QuarantineManager ---")
    qm.add_to_quarantine(test_items)
    items = qm.list_quarantine()
    print(f"Total en espera: {len(items)}")
    for i in items:
        print(f"  [{i['quarantine_id']}] {i['verbo']} - {i['razon']}")
    
    # Limpieza de prueba (opcional)
    # qm.remove_from_quarantine(items[0]['quarantine_id'])

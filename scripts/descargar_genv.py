import requests
import os
import subprocess
import sys
import time

# Configuración Jackett
JACKETT_URL = "http://127.0.0.1:9117"
API_KEY = "ma3dse1zyu23w2puqewa3ozvemddasg9"
INDEXER = "all"

# Configuración de búsqueda
SERIE = "Gen V"
TEMPORADA = "S02"  # Buscamos la más reciente según Fase Forense
MIN_SIZE = 0.9 * 1024 * 1024 * 1024  # 0.9 GB
MAX_SIZE = 2.8 * 1024 * 1024 * 1024  # 2.8 GB
RESOLUTION_KEYWORD = "1080p"  # Asegura > 1024 res

# Rutas
TRANSMISSION_CMD = "/home/daniel/tron/programas/ProyectoPizza/TRON/bin/transmission-bin/transmission-remote"
DOWNLOAD_DIR = "/home/daniel/Descargas/GenV"
DEVICE_IP = "172.16.0.44:39115"

def buscar_torrents():
    print(f"🔍 Buscando {SERIE} en Jackett (esto puede tardar)...")
    params = {
        "apikey": API_KEY,
        "Query": f"{SERIE}", # Búsqueda más amplia para filtrar localmente
        "Category[]": [2000, 5000]
    }
    try:
        # Aumentamos timeout a 60s
        response = requests.get(f"{JACKETT_URL}/api/v2.0/indexers/{INDEXER}/results", params=params, timeout=60)
        response.raise_for_status()
        results = response.json().get("Results", [])
        return results
    except Exception as e:
        print(f"❌ Error conectando a Jackett: {e}")
        return []

def filtrar_y_descargar(results):
    validos = []
    for res in results:
        size = res.get("Size", 0)
        seeders = res.get("Seeders", 0)
        title = res.get("Title", "").upper()
        magnet = res.get("MagnetUri") or res.get("Link")
        
        # Filtros: Temporada 2, Tamaño (0.9-2.8GB) y Semillas
        if "S02" in title and MIN_SIZE <= size <= MAX_SIZE and seeders > 5:
            validos.append({
                "title": res.get("Title"),
                "magnet": magnet,
                "seeders": seeders,
                "size_gb": round(size / (1024**3), 2)
            })
    
    # Ordenar por seeders
    validos.sort(key=lambda x: x["seeders"], reverse=True)
    
    if not validos:
        print("⚠️ No se encontraron torrents que cumplan los requisitos de tamaño (0.9-2.8GB) y semillas.")
        return

    # Tomar los 3 primeros (o el torrent completo si es pack)
    print(f"✅ Se encontraron {len(validos)} candidatos. Iniciando descarga de los 3 mejores...")
    for i, item in enumerate(validos[:3]):
        print(f"📥 Agregando a Transmission: {item['title']} ({item['size_gb']} GB, {item['seeders']} seeders)")
        subprocess.run([TRANSMISSION_CMD, "-n", "transmission:transmission", "-a", item["magnet"], "-w", DOWNLOAD_DIR])

def transferir_a_dispositivo():
    print(f"🚀 Iniciando transferencia a {DEVICE_IP}...")
    archivos = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))]
    archivos.sort()
    
    for f in archivos[:3]:
        path_local = os.path.join(DOWNLOAD_DIR, f)
        print(f"📤 Transfiriendo {f}...")
        # Intentamos conectar por si se cayó
        subprocess.run(["adb", "connect", DEVICE_IP])
        res = subprocess.run(["adb", "-s", DEVICE_IP, "push", path_local, "/sdcard/Download/"], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"✅ {f} transferido con éxito.")
        else:
            print(f"❌ Fallo en transferencia de {f}: {res.stderr}")

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        
    resultados = buscar_torrents()
    if resultados:
        filtrar_y_descargar(resultados)
        print("\n✅ Torrents enviados a Transmission.")
        print("📂 Los archivos se descargarán en: " + DOWNLOAD_DIR)
        print("🔌 Recordatorio: Una vez terminada la descarga, copiaremos los 3 primeros por cable.")
    else:
        print("❌ No se obtuvieron resultados de Jackett. Verifica los trackers configurados en el panel (http://localhost:9117).")

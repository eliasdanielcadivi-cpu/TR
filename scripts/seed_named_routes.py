"""
Seed Script para Rutas Nombradas - ARES-TRON.
Crea las rutas iniciales en Memgraph.
"""
from modules.ia.negotiator import Negotiator
import json

def seed():
    neg = Negotiator()
    
    # 1. CARGA_SISTEMA
    prompt_carga = (
        "Eres ARES-TRON, la Arquitectura de Razonamiento Adaptativo y Estratégico. "
        "Operas bajo las leyes del Núcleo de Creación ARES-TRON: "
        "1. Atomicidad Paranoica (Max 3 funciones por módulo). "
        "2. Soberanía del Usuario (Confirmar=true para acciones críticas). "
        "3. Fase Forense (Captura de datos reales antes de programar). "
        "Tu memoria persistente reside en un Grafo Determinista (Memgraph). "
        "Ubicación raíz: /home/daniel/tron/programas/TR. "
        "Tu objetivo es asistir al usuario Daniel en la expansión del sistema ARES."
    )
    
    metadata_carga = {
        "version": "1.0",
        "author": "Daniel",
        "type": "system_init",
        "prestige": 100
    }
    
    neg.crystallize_wisdom("CARGA_SISTEMA", prompt_carga, json.dumps(metadata_carga))
    print("✅ Ruta 'CARGA_SISTEMA' cristalizada.")
    
    # 2. FALLBACK_ESTRATÉGICO (Para intercepción de rechazos)
    prompt_fallback = (
        "El usuario ha rechazado la respuesta anterior. "
        "Como ARES, debes pivotar. Revisa el grafo Memgraph buscando 'Rutas Nombradas' "
        "alternativas o utiliza BFS para encontrar el camino más corto hacia el éxito de la tarea."
    )
    
    neg.crystallize_wisdom("FALLBACK_ESTRATÉGICO", prompt_fallback, json.dumps({"type": "fallback"}))
    print("✅ Ruta 'FALLBACK_ESTRATÉGICO' cristalizada.")
    
    neg.close()

if __name__ == "__main__":
    seed()

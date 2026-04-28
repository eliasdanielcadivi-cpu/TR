"""
Context Router - ARES-TRON.
Orquestador Híbrido: Workflow + Búsqueda Inteligente.
Filosofía: Reactivo y Determinista.
"""
import os
from modules.core.phase_manager import detect_current_phase, get_phase_rules
from modules.ia.strategy_selector import select_search_strategy
from modules.ia.negotiator import Negotiator
from modules.core.prompt_engine import build_system_prompt, BuildPromptParams

def route_and_assemble(target_scope: str, user_prompt: str) -> str:
    """
    Punto de entrada único que decide el alcance y la inyección dinámica.
    """
    base_path = os.getcwd() # Asumimos CWD como raíz del proyecto actual
    
    # 1. Detección de Fase (Mandato 11)
    phase = detect_current_phase(base_path)
    phase_rules = get_phase_rules(phase)
    
    # 2. Selección de Estrategia (Mandato 6 y 13)
    strategy = select_search_strategy(user_prompt, phase)
    
    # 3. Recuperación Consistente (Mandato 9)
    # Combinamos el alcance solicitado (target_scope) con el conocimiento de fase
    context_text = _execute_hybrid_retrieval(target_scope, strategy, phase_rules)
    
    # 4. Ensamblado Dinámico (Mandato 8)
    params = BuildPromptParams(
        base_prompt=context_text,
        objectives=phase_rules["required_skills"],
        mode="chat"
    )
    system_prompt = build_system_prompt(params)
    
    # Info para el usuario en verbose
    header = f"INSTRUCCIÓN DE SISTEMA (FASE: {phase} | ESTRATEGIA: {strategy['reason']})"
    return f"{header}\n{system_prompt}\n\nCONSULTA: {user_prompt}"

def _execute_hybrid_retrieval(scope: str, strategy: dict, rules: dict) -> str:
    """
    Ejecuta la búsqueda combinada: Grafo + Reglas de Fase.
    Fallback: Si Memgraph falla, usa la configuración local (identidad).
    """
    neg = Negotiator()
    route_data = neg.get_named_route(scope)
    
    if route_data["status"] == "success":
        base_text = route_data["prompt"]
    else:
        # FALLBACK: Leer de config/identidad si el grafo falla
        import yaml
        try:
            with open("config/identidad/ares.yaml", "r") as f:
                config = yaml.safe_load(f)
                base_text = config.get("definicion", "Eres ARES (Modo Fallback)")
                base_text += f"\n\n⚠️ NOTA: Memgraph inactivo. Usando identidad local."
        except:
            base_text = f"Modo: {scope} (Sin contexto disponible)"
    
    # Inyección de Skills de Fase (Mandato 7)
    skills_text = "\nSKILLS REQUERIDOS PARA ESTA FASE:\n" + "\n".join(rules["required_skills"])
    
    neg.close()
    return f"{base_text}\n{skills_text}"

def get_current_state_report():
    """Retorna un reporte del estado actual del sistema para depuración."""
    phase = detect_current_phase(os.getcwd())
    return {"phase": phase, "rules": get_phase_rules(phase)}

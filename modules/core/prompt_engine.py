"""
Prompt Engine - Módulo para construcción y gestión de system prompts dinámicos

Módulo atómico (≤3 funciones) - Filosofía ARES

Funcionalidades:
1. build_system_prompt - Construye prompt con contexto y modo
2. update_prompt - Actualiza prompt con validación de deriva
3. negotiate_change - Negocia cambios propuestos al prompt
4. get_default_prompt - Obtiene el prompt por defecto

Flujo de Datos:
- Entrada: Prompt base + objetivos + modo
- Procesamiento: Combina elementos, valida deriva
- Salida: System prompt completo estructurado

Ejemplo de Uso:
```python
# Ejemplo 1: Construir prompt con contexto
prompt = build_system_prompt(
    base_prompt="Eres un asistente de código",
    objectives=["Ayudar con TypeScript", "Enseñar buenas prácticas"],
    mode="chat"
)

# Ejemplo 2: Actualizar prompt con validación
session = get_session(session_id)
result = update_prompt(session, "Nuevo prompt", force=False)

if result.success:
    print("Prompt actualizado correctamente")
elif result.requires_approval:
    print("Requiere aprobación del usuario")

# Ejemplo 3: Negociar cambio propuesto
negotiation = negotiate_change(old_prompt, new_prompt)
print(negotiation.recommendation)  # 'ACCEPT' | 'REVIEW' | 'REJECT'

# Ejemplo 4: Obtener prompt por defecto
default_prompt = get_default_prompt()
```
"""

from typing import List, Dict, NamedTuple, Optional
from dataclasses import dataclass
from datetime import datetime

from .delta_calculator import calculate, compare, requires_approval


# ============================================================================
# CONSTANTES
# ============================================================================

DEFAULT_SYSTEM_PROMPT = """Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente."""
"""Prompt base por defecto para extracción cognitiva"""


# ============================================================================
# TIPOS
# ============================================================================

@dataclass
class BuildPromptParams:
    """Parámetros para construir un system prompt
    
    Attributes:
        base_prompt: Prompt base (opcional, usa DEFAULT_SYSTEM_PROMPT)
        objectives: Lista de objetivos activos del usuario
        mode: Modo de interacción ('chat' o 'questionnaire')
    """
    base_prompt: Optional[str] = None
    objectives: Optional[List[str]] = None
    mode: str = "chat"


@dataclass
class PromptUpdateResult:
    """Resultado de una actualización de prompt
    
    Attributes:
        success: Si la actualización fue exitosa
        requires_approval: Si el cambio requiere aprobación (pero fue forzado)
        delta_score: Score de deriva calculado
        mutation: Mutación registrada (si hubo éxito)
    """
    success: bool
    requires_approval: bool
    delta_score: float
    mutation: Optional[Dict] = None


class NegotiationResult(NamedTuple):
    """Resultado de una negociación de cambio de prompt
    
    Attributes:
        delta_score: Score de deriva (0.0 a 1.0)
        threshold: Umbral configurado
        requires_approval: Si requiere aprobación
        recommendation: Recomendación de acción ('ACCEPT' | 'REVIEW' | 'REJECT')
        reason: Razón de la recomendación
        negotiable: Si el cambio es negociable
        changes: Detalle de cambios (additions, deletions, semantic_shift)
    """
    delta_score: float
    threshold: float
    requires_approval: bool
    recommendation: str
    reason: str
    negotiable: bool
    changes: Dict[str, int]


# ============================================================================
# FUNCIONES EXPORTADAS (API PÚBLICA DEL MÓDULO)
# ============================================================================

def build_system_prompt(params: BuildPromptParams) -> str:
    """
    Construye un system prompt con contexto adicional.
    
    Combina el prompt base con:
    - Objetivos activos del usuario
    - Instrucciones específicas del modo (chat/cuestionario)
    
    Args:
        params: Parámetros para construir el prompt
    
    Returns:
        El system prompt completo construido
    
    Example:
        prompt = build_system_prompt(BuildPromptParams(
            base_prompt="Eres un asistente de código",
            objectives=["Ayudar con TypeScript", "Enseñar buenas prácticas"],
            mode="chat"
        ))
        # Incluye instrucciones para modo chat
    
    Example:
        # Modo cuestionario
        prompt = build_system_prompt(BuildPromptParams(
            objectives=["Objetivo 1"],
            mode="questionnaire"
        ))
        # Incluye instrucciones para modo cuestionario
    """
    base = params.base_prompt or DEFAULT_SYSTEM_PROMPT
    
    # Contexto de objetivos
    if params.objectives:
        objectives_context = "\n\nOBJETIVOS ACTIVOS:\n" + "\n".join(
            f"- {obj}" for obj in params.objectives
        )
    else:
        objectives_context = ""
    
    # Instrucciones por modo
    if params.mode == "questionnaire":
        mode_instruction = "\n\nMODO CUESTIONARIO: Estructura tu respuesta como una pregunta con opciones claras. Usa formato JSON para las opciones."
    else:
        mode_instruction = "\n\nMODO CHAT: Responde de manera conversacional y natural."
    
    return f"{base}{objectives_context}{mode_instruction}"


def update_prompt(
    session: Dict,
    new_prompt: str,
    force: bool = False
) -> PromptUpdateResult:
    """
    Actualiza el system prompt de una sesión con validación.
    
    Modifica el system prompt de una sesión después de:
    1. Calcular la deriva del cambio
    2. Determinar si requiere aprobación
    3. Aplicar el cambio si es válido
    
    Args:
        session: Sesión a actualizar (de session_manager)
        new_prompt: Nuevo contenido del prompt
        force: Si es True, omite validación de aprobación
    
    Returns:
        PromptUpdateResult con éxito, delta, y mutación si aplica
    
    Example:
        session = get_session(session_id)
        result = update_prompt(session, "Nuevo prompt", force=False)
        
        if result.success:
            print("Prompt actualizado")
        else:
            print("Requiere aprobación:", result.requires_approval)
    """
    old_prompt = session.get("system_prompt", "")
    
    # Calcular deriva
    delta_score = calculate(old_prompt, new_prompt)
    needs_approval = requires_approval(delta_score)
    
    # Verificar aprobación
    if needs_approval and not force:
        return PromptUpdateResult(
            success=False,
            requires_approval=True,
            delta_score=delta_score,
            mutation=None
        )
    
    # Aplicar actualización
    session["system_prompt"] = new_prompt
    session["updated_at"] = datetime.now().isoformat()
    
    mutation = {
        "id": f"mut_{int(datetime.now().timestamp() * 1000)}",
        "timestamp": datetime.now().isoformat(),
        "change": f"Prompt actualizado ({len(new_prompt) - len(old_prompt)} chars)",
        "reason": "Update via prompt engine",
        "delta_impact": delta_score,
        "approved": not needs_approval or force
    }
    
    return PromptUpdateResult(
        success=True,
        requires_approval=False,
        delta_score=delta_score,
        mutation=mutation
    )


def negotiate_change(old_prompt: str, new_prompt: str) -> NegotiationResult:
    """
    Negocia un cambio de prompt propuesto.
    
    Analiza un cambio propuesto al prompt y determina:
    - Magnitud del cambio
    - Si es negociable o debe rechazarse
    - Recomendación de acción
    
    Args:
        old_prompt: Prompt actual
        new_prompt: Prompt propuesto
    
    Returns:
        NegotiationResult con recomendación y razón
    
    Example:
        result = negotiate_change(current_prompt, proposed_prompt)
        
        if result.recommendation == "ACCEPT":
            print("Cambio seguro para aplicar")
        elif result.recommendation == "REVIEW":
            print("Requiere revisión humana")
        else:
            print("Cambio demasiado drástico")
    """
    comparison = compare(old_prompt, new_prompt)
    
    # Determinar recomendación basada en la deriva
    if comparison.delta_score < 0.1:
        recommendation = "ACCEPT"
        reason = "Cambio menor, seguro para aplicar automáticamente"
    elif comparison.delta_score < comparison.threshold:
        recommendation = "REVIEW"
        reason = "Cambio moderado, revisar antes de aplicar"
    elif comparison.delta_score < 0.7:
        recommendation = "REVIEW"
        reason = "Cambio significativo, requiere aprobación explícita"
    else:
        recommendation = "REJECT"
        reason = "Cambio demasiado drástico, puede desviar el objetivo"
    
    return NegotiationResult(
        delta_score=comparison.delta_score,
        threshold=comparison.threshold,
        requires_approval=comparison.requires_approval,
        recommendation=recommendation,
        reason=reason,
        negotiable=comparison.delta_score < 0.7,
        changes=comparison.changes
    )


def get_default_prompt() -> str:
    """
    Obtiene el prompt por defecto.
    
    Retorna el system prompt base que se usa cuando no hay uno personalizado.
    
    Returns:
        El prompt por defecto (DEFAULT_SYSTEM_PROMPT)
    
    Example:
        default_prompt = get_default_prompt()
        print(default_prompt)
        # "Eres un sistema de EXTRACCIÓN COGNITIVA..."
    """
    return DEFAULT_SYSTEM_PROMPT

"""
Delta Calculator - Módulo para cálculo de deriva semántica de prompts

Módulo atómico (≤3 funciones) - Filosofía ARES

Funcionalidades:
1. calculate - Calcula deriva entre dos prompts (0.0 a 1.0)
2. compare - Compara prompts y retorna métricas detalladas
3. threshold - Obtiene umbral configurado para aprobación
4. requires_approval - Determina si cambio requiere aprobación

Flujo de Datos:
- Entrada: Dos strings (oldPrompt, newPrompt)
- Procesamiento: Calcula diferencia de longitud normalizada
- Salida: Score numérico 0.0-1.0 + métricas detalladas

Ejemplo de Uso:
```python
# Ejemplo 1: Calcular deriva simple
old_prompt = "Eres un asistente útil"
new_prompt = "Eres un asistente muy útil y amable"
delta = calculate(old_prompt, new_prompt)
print(f"Deriva: {(delta * 100):.2f}%")

# Ejemplo 2: Comparación detallada
comparison = compare(old_prompt, new_prompt)
print(comparison)
# {
#   "delta_score": 0.35,
#   "threshold": 0.3,
#   "requires_approval": True,
#   "changes": {"additions": 15, "deletions": 0, "semantic_shift": 0.35}
# }

# Ejemplo 3: Verificar si requiere aprobación
if requires_approval(delta):
    print("El cambio requiere aprobación del usuario")
```
"""

import os
from typing import Dict, NamedTuple


# ============================================================================
# CONSTANTES
# ============================================================================

DEFAULT_THRESHOLD = 0.3
"""Umbral por defecto para requerir aprobación de cambios

Si la deriva supera este valor, el cambio debe ser aprobado explícitamente.
Configurable vía variable de entorno PROMPT_DELTA_THRESHOLD.
"""


# ============================================================================
# TIPOS
# ============================================================================

class DeltaComparison(NamedTuple):
    """Resultado detallado de una comparación de prompts
    
    Attributes:
        delta_score: Score de deriva (0.0 = sin cambios, 1.0 = cambio total)
        threshold: Umbral configurado para aprobación
        requires_approval: Si el cambio excede el umbral y requiere aprobación
        changes: Detalle de los cambios (additions, deletions, semantic_shift)
    """
    delta_score: float
    threshold: float
    requires_approval: bool
    changes: Dict[str, int]


# ============================================================================
# FUNCIONES EXPORTADAS (API PÚBLICA DEL MÓDULO)
# ============================================================================

def calculate(old_prompt: str, new_prompt: str) -> float:
    """
    Calcula deriva entre dos prompts (0.0 a 1.0).
    
    Algoritmo: Diferencia de longitud normalizada.
    TODO: Implementar cosine similarity para análisis semántico.
    
    Args:
        old_prompt: Versión anterior del prompt
        new_prompt: Nueva versión del prompt
    
    Returns:
        Score de deriva (0.0 = sin cambios, 1.0 = cambio total)
    
    Example:
        delta = calculate("prompt corto", "prompt mucho más largo")
        print(f"Deriva: {delta * 100:.2f}%")
    
    Example:
        # Sin cambios
        delta = calculate("mismo prompt", "mismo prompt")
        print(delta)  # 0.0
    
    Nota: Comentar solo lo complejo o costoso de resolver.
        - Si falta alguno de los prompts, se considera cambio total (1.0)
    """
    if not old_prompt or not new_prompt:
        return 1.0
    
    length_diff = abs(len(new_prompt) - len(old_prompt))
    max_length = max(len(old_prompt), len(new_prompt), 1)
    return length_diff / max_length


def compare(old_prompt: str, new_prompt: str) -> DeltaComparison:
    """
    Compara dos prompts y retorna métricas detalladas.
    
    Args:
        old_prompt: Versión anterior del prompt
        new_prompt: Nueva versión del prompt
    
    Returns:
        DeltaComparison con:
        - delta_score: Score de deriva
        - threshold: Umbral configurado
        - requires_approval: Si excede umbral
        - changes: {additions, deletions, semantic_shift}
    
    Example:
        comparison = compare("prompt corto", "prompt mucho más largo y detallado")
        print(comparison)
        # DeltaComparison(delta_score=0.65, threshold=0.3, requires_approval=True,
        #                 changes={...})
    """
    delta_score = calculate(old_prompt, new_prompt)
    threshold_value = threshold()
    
    # Calcular adiciones y eliminaciones aproximadas
    length_diff = len(new_prompt) - len(old_prompt)
    additions = max(0, length_diff)
    deletions = max(0, -length_diff)
    
    return DeltaComparison(
        delta_score=delta_score,
        threshold=threshold_value,
        requires_approval=delta_score > threshold_value,
        changes={
            "additions": additions,
            "deletions": deletions,
            "semantic_shift": delta_score
        }
    )


def threshold() -> float:
    """
    Obtiene umbral configurado para aprobación de cambios.
    
    Lee variable de entorno PROMPT_DELTA_THRESHOLD o retorna default.
    
    Returns:
        Umbral de 0.0 a 1.0 (default: 0.3)
    
    Example:
        t = threshold()
        print(f"Cambios > {t * 100}% requieren aprobación")
    
    Example:
        # Con variable de entorno PROMPT_DELTA_THRESHOLD=0.5
        t = threshold()
        print(t)  # 0.5
    """
    # Intentar leer de variable de entorno
    env_threshold = os.getenv("PROMPT_DELTA_THRESHOLD")
    if env_threshold:
        try:
            parsed = float(env_threshold)
            if 0 <= parsed <= 1:
                return parsed
        except ValueError:
            pass
    
    # Retornar valor por defecto
    return DEFAULT_THRESHOLD


def requires_approval(delta_score: float) -> bool:
    """
    Determina si un cambio requiere aprobación.
    
    Compara el score de deriva contra el umbral configurado.
    
    Args:
        delta_score: Score de deriva (0.0 a 1.0)
    
    Returns:
        True si requiere aprobación, False si es cambio menor
    
    Example:
        delta = calculate(old_prompt, new_prompt)
        if requires_approval(delta):
            print("El usuario debe aprobar este cambio")
    """
    return delta_score > threshold()

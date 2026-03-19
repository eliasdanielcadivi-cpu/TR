/**
 * Delta Calculator - Módulo para cálculo de deriva semántica de prompts
 * 
 * @module @agentedecambio2/delta-calculator
 * @version 0.1.0
 * 
 * @description
 * Este módulo calcula la diferencia (deriva) entre dos versiones de un prompt.
 * Se usa para determinar si un cambio en el system prompt requiere aprobación del usuario.
 * 
 * La deriva se mide en una escala de 0.0 a 1.0:
 * - 0.0 = Sin cambios
 * - 1.0 = Cambio total
 * 
 * @example
 * ```typescript
 * import { calculate, compare, threshold } from './actions';
 * 
 * const oldPrompt = 'Eres un asistente útil';
 * const newPrompt = 'Eres un asistente muy útil y amable';
 * 
 * const delta = calculate(oldPrompt, newPrompt);
 * console.log(delta); // 0.35 (35% de cambio)
 * 
 * if (delta > threshold()) {
 *   console.log('Requiere aprobación');
 * }
 * ```
 * 
 * @see {@link ./INDEX.md} para documentación completa del módulo
 */

// ============================================================================
// CONSTANTES
// ============================================================================

/**
 * Umbral por defecto para requerir aprobación de cambios
 * 
 * @description
 * Si la deriva supera este valor, el cambio debe ser aprobado explícitamente.
 * Configurable vía variable de entorno PROMPT_DELTA_THRESHOLD.
 */
const DEFAULT_THRESHOLD = 0.3;

// ============================================================================
// FUNCIONES EXPORTADAS
// ============================================================================

/**
 * Calcula la deriva entre dos prompts
 * 
 * @description
 * Compara dos versiones de un prompt y retorna un score de 0.0 a 1.0
 * que representa la magnitud del cambio.
 * 
 * Algoritmo actual: Basado en diferencia de longitud normalizada.
 * TODO: Implementar algoritmo semántico más sofisticado (cosine similarity).
 * 
 * @param oldPrompt - Versión anterior del prompt
 * @param newPrompt - Nueva versión del prompt
 * 
 * @returns {number} Score de deriva (0.0 = sin cambios, 1.0 = cambio total)
 * 
 * @example
 * ```typescript
 * const oldPrompt = 'Eres un asistente';
 * const newPrompt = 'Eres un asistente muy útil';
 * 
 * const delta = calculate(oldPrompt, newPrompt);
 * console.log(`Deriva: ${(delta * 100).toFixed(2)}%`);
 * ```
 * 
 * @example
 * ```typescript
 * // Sin cambios
 * const delta = calculate('mismo prompt', 'mismo prompt');
 * console.log(delta); // 0.0
 * ```
 */
export function calculate(oldPrompt: string, newPrompt: string): number {
  // Validación de entrada
  if (!oldPrompt || !newPrompt) {
    return 1.0; // Considerar como cambio total si falta alguno
  }

  // Algoritmo simplificado: diferencia de longitud normalizada
  const lengthDiff = Math.abs(newPrompt.length - oldPrompt.length);
  const maxLength = Math.max(oldPrompt.length, newPrompt.length, 1);
  const delta = lengthDiff / maxLength;

  return delta;
}

/**
 * Compara dos prompts y retorna métricas detalladas
 * 
 * @description
 * Versión extendida de {@link calculate} que retorna información
 * adicional sobre el tipo de cambio detectado.
 * 
 * @param oldPrompt - Versión anterior del prompt
 * @param newPrompt - Nueva versión del prompt
 * 
 * @returns {DeltaComparison} Objeto con métricas detalladas del cambio
 * 
 * @example
 * ```typescript
 * const comparison = compare('prompt corto', 'prompt mucho más largo y detallado');
 * console.log(comparison);
 * // {
 * //   deltaScore: 0.65,
 * //   additions: 25,
 * //   deletions: 0,
 * //   semanticShift: 0.65,
 * //   requiresApproval: true
 * // }
 * ```
 */
export function compare(oldPrompt: string, newPrompt: string): DeltaComparison {
  const deltaScore = calculate(oldPrompt, newPrompt);
  const thresholdValue = threshold();

  // Calcular adiciones y eliminaciones aproximadas
  const lengthDiff = newPrompt.length - oldPrompt.length;
  const additions = lengthDiff > 0 ? lengthDiff : 0;
  const deletions = lengthDiff < 0 ? Math.abs(lengthDiff) : 0;

  return {
    deltaScore,
    threshold: thresholdValue,
    requiresApproval: deltaScore > thresholdValue,
    changes: {
      additions,
      deletions,
      semanticShift: deltaScore,
    },
  };
}

/**
 * Obtiene el umbral configurado para aprobación de cambios
 * 
 * @description
 * Lee la variable de entorno PROMPT_DELTA_THRESHOLD o retorna el valor por defecto.
 * 
 * @returns {number} Umbral de 0.0 a 1.0
 * 
 * @example
 * ```typescript
 * const t = threshold();
 * console.log(`Cambios > ${t * 100}% requieren aprobación`);
 * ```
 * 
 * @example
 * ```typescript
 * // Con variable de entorno PROMPT_DELTA_THRESHOLD=0.5
 * const t = threshold();
 * console.log(t); // 0.5
 * ```
 */
export function threshold(): number {
  // Intentar leer de variable de entorno (Node.js)
  if (typeof process !== 'undefined' && process.env) {
    const envThreshold = process.env.PROMPT_DELTA_THRESHOLD;
    if (envThreshold) {
      const parsed = parseFloat(envThreshold);
      if (!isNaN(parsed) && parsed >= 0 && parsed <= 1) {
        return parsed;
      }
    }
  }

  // Retornar valor por defecto
  return DEFAULT_THRESHOLD;
}

/**
 * Determina si un cambio requiere aprobación
 * 
 * @description
 * Compara el score de deriva contra el umbral configurado.
 * 
 * @param deltaScore - Score de deriva (0.0 a 1.0)
 * 
 * @returns {boolean} True si requiere aprobación, false si es cambio menor
 * 
 * @example
 * ```typescript
 * const delta = calculate(oldPrompt, newPrompt);
 * if (requiresApproval(delta)) {
 *   console.log('El usuario debe aprobar este cambio');
 * }
 * ```
 */
export function requiresApproval(deltaScore: number): boolean {
  return deltaScore > threshold();
}

// ============================================================================
// TIPOS
// ============================================================================

/**
 * Resultado detallado de una comparación de prompts
 * 
 * @description
 * Contiene todas las métricas sobre el cambio detectado entre dos prompts.
 */
export interface DeltaComparison {
  /** Score de deriva (0.0 = sin cambios, 1.0 = cambio total) */
  deltaScore: number;
  
  /** Umbral configurado para aprobación */
  threshold: number;
  
  /** Si el cambio excede el umbral y requiere aprobación */
  requiresApproval: boolean;
  
  /** Detalle de los cambios */
  changes: {
    /** Cantidad de caracteres añadidos */
    additions: number;
    /** Cantidad de caracteres eliminados */
    deletions: number;
    /** Score de cambio semántico (igual a deltaScore en implementación actual) */
    semanticShift: number;
  };
}

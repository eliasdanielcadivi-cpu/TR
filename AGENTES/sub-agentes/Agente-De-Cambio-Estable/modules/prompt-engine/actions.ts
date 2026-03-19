/**
 * Prompt Engine - Módulo para construcción y gestión de system prompts dinámicos
 * 
 * @module @agentedecambio2/prompt-engine
 * @version 0.1.0
 * 
 * @description
 * Este módulo construye y gestiona los system prompts que se envían a DeepSeek.
 * Características:
 * - Construye prompts con contexto de objetivos
 * - Añade instrucciones específicas por modo (chat/cuestionario)
 * - Gestiona mutaciones del prompt con validación
 * 
 * @example
 * ```typescript
 * import { buildSystemPrompt, updatePrompt, negotiateChange } from './actions';
 * 
 * // Construir prompt con contexto
 * const prompt = buildSystemPrompt({
 *   basePrompt: 'Eres un asistente',
 *   objectives: ['Ayudar al usuario'],
 *   mode: 'chat'
 * });
 * 
 * // Actualizar prompt con validación
 * const result = updatePrompt(sessionId, 'Nuevo prompt', true);
 * console.log(result.approved); // true
 * ```
 * 
 * @see {@link ./INDEX.md} para documentación completa del módulo
 */

import type { Session } from '../shared-types/types';
import { calculate, compare, requiresApproval } from '../delta-calculator/actions';

// ============================================================================
// CONSTANTES
// ============================================================================

/**
 * Prompt base por defecto para extracción cognitiva
 * 
 * @description
 * Este es el system prompt inicial que define el comportamiento del asistente.
 * Se puede modificar durante la sesión según las necesidades del usuario.
 */
const DEFAULT_SYSTEM_PROMPT = `Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente.`;

// ============================================================================
// FUNCIONES EXPORTADAS
// ============================================================================

/**
 * Construye un system prompt con contexto adicional
 * 
 * @description
 * Combina el prompt base con:
 * - Objetivos activos del usuario
 * - Instrucciones específicas del modo (chat/cuestionario)
 * 
 * @param params - Parámetros para construir el prompt
 * @param params.basePrompt - Prompt base (por defecto: DEFAULT_SYSTEM_PROMPT)
 * @param params.objectives - Lista de objetivos activos
 * @param params.mode - Modo de interacción ('chat' | 'questionnaire')
 * 
 * @returns {string} El system prompt completo construido
 * 
 * @example
 * ```typescript
 * const prompt = buildSystemPrompt({
 *   basePrompt: 'Eres un asistente de código',
 *   objectives: ['Ayudar con TypeScript', 'Enseñar buenas prácticas'],
 *   mode: 'chat'
 * });
 * console.log(prompt);
 * // "Eres un asistente de código...
 * // MODO CHAT: Responde de manera conversacional y natural."
 * ```
 * 
 * @example
 * ```typescript
 * // Modo cuestionario
 * const prompt = buildSystemPrompt({
 *   objectives: ['Objetivo 1'],
 *   mode: 'questionnaire'
 * });
 * // Incluye instrucciones para modo cuestionario
 * ```
 */
export function buildSystemPrompt(params: BuildPromptParams): string {
  const basePrompt = params.basePrompt || DEFAULT_SYSTEM_PROMPT;
  
  // Contexto de objetivos
  const objectivesContext = params.objectives && params.objectives.length > 0
    ? `\n\nOBJETIVOS ACTIVOS:\n${params.objectives.map(obj => `- ${obj}`).join('\n')}`
    : '';
  
  // Instrucciones por modo
  const modeInstruction = params.mode === 'questionnaire'
    ? '\n\nMODO CUESTIONARIO: Estructura tu respuesta como una pregunta con opciones claras. Usa formato JSON para las opciones.'
    : '\n\nMODO CHAT: Responde de manera conversacional y natural.';
  
  return `${basePrompt}${objectivesContext}${modeInstruction}`;
}

/**
 * Actualiza el system prompt de una sesión con validación
 * 
 * @description
 * Modifica el system prompt de una sesión después de:
 * 1. Calcular la deriva del cambio
 * 2. Determinar si requiere aprobación
 * 3. Aplicar el cambio si es válido
 * 
 * @param session - Sesión a actualizar
 * @param newPrompt - Nuevo contenido del prompt
 * @param force - Si es true, omite validación de aprobación
 * 
 * @returns {PromptUpdateResult} Resultado de la actualización
 * 
 * @example
 * ```typescript
 * const session = getSession(sessionId);
 * const result = updatePrompt(session, 'Nuevo prompt', false);
 * 
 * if (result.success) {
 *   console.log('Prompt actualizado');
 * } else {
 *   console.log('Requiere aprobación:', result.requiresApproval);
 * }
 * ```
 */
export function updatePrompt(
  session: Session,
  newPrompt: string,
  force: boolean = false
): PromptUpdateResult {
  const oldPrompt = session.systemPrompt;
  
  // Calcular deriva
  const deltaScore = calculate(oldPrompt, newPrompt);
  const needsApproval = requiresApproval(deltaScore);
  
  // Verificar aprobación
  if (needsApproval && !force) {
    return {
      success: false,
      requiresApproval: true,
      deltaScore,
      mutation: null,
    };
  }
  
  // Aplicar actualización
  session.systemPrompt = newPrompt;
  session.updatedAt = new Date();
  
  const mutation = {
    id: `mut_${Date.now()}`,
    timestamp: new Date(),
    change: `Prompt actualizado (${newPrompt.length - oldPrompt.length} chars)`,
    reason: 'Update via prompt engine',
    deltaImpact: deltaScore,
    approved: !needsApproval || force,
  };
  
  return {
    success: true,
    requiresApproval: false,
    deltaScore,
    mutation,
  };
}

/**
 * Negocia un cambio de prompt propuesto
 * 
 * @description
 * Analiza un cambio propuesto al prompt y determina:
 * - Magnitud del cambio
 * - Si es negociable o debe rechazarse
 * - Recomendación de acción
 * 
 * @param oldPrompt - Prompt actual
 * @param newPrompt - Prompt propuesto
 * 
 * @returns {NegotiationResult} Resultado de la negociación
 * 
 * @example
 * ```typescript
 * const result = negotiateChange(currentPrompt, proposedPrompt);
 * 
 * if (result.recommendation === 'ACCEPT') {
 *   console.log('Cambio seguro para aplicar');
 * } else if (result.recommendation === 'REVIEW') {
 *   console.log('Requiere revisión humana');
 * } else {
 *   console.log('Cambio demasiado drástico');
 * }
 * ```
 */
export function negotiateChange(oldPrompt: string, newPrompt: string): NegotiationResult {
  const comparison = compare(oldPrompt, newPrompt);
  
  // Determinar recomendación basada en la deriva
  let recommendation: 'ACCEPT' | 'REVIEW' | 'REJECT';
  let reason: string;
  
  if (comparison.deltaScore < 0.1) {
    recommendation = 'ACCEPT';
    reason = 'Cambio menor, seguro para aplicar automáticamente';
  } else if (comparison.deltaScore < comparison.threshold) {
    recommendation = 'REVIEW';
    reason = 'Cambio moderado, revisar antes de aplicar';
  } else if (comparison.deltaScore < 0.7) {
    recommendation = 'REVIEW';
    reason = 'Cambio significativo, requiere aprobación explícita';
  } else {
    recommendation = 'REJECT';
    reason = 'Cambio demasiado drástico, puede desviar el objetivo';
  }
  
  return {
    ...comparison,
    recommendation,
    reason,
    negotiable: comparison.deltaScore < 0.7,
  };
}

/**
 * Obtiene el prompt por defecto
 * 
 * @description
 * Retorna el system prompt base que se usa cuando no hay uno personalizado.
 * 
 * @returns {string} El prompt por defecto
 * 
 * @example
 * ```typescript
 * const defaultPrompt = getDefaultPrompt();
 * console.log(defaultPrompt);
 * // "Eres un sistema de EXTRACCIÓN COGNITIVA..."
 * ```
 */
export function getDefaultPrompt(): string {
  return DEFAULT_SYSTEM_PROMPT;
}

// ============================================================================
// TIPOS
// ============================================================================

/**
 * Parámetros para construir un system prompt
 */
export interface BuildPromptParams {
  /** Prompt base (opcional, usa DEFAULT_SYSTEM_PROMPT si no se proporciona) */
  basePrompt?: string;
  
  /** Lista de objetivos activos del usuario */
  objectives?: string[];
  
  /** Modo de interacción ('chat' o 'questionnaire') */
  mode?: 'chat' | 'questionnaire';
}

/**
 * Resultado de una actualización de prompt
 */
export interface PromptUpdateResult {
  /** Si la actualización fue exitosa */
  success: boolean;
  
  /** Si el cambio requiere aprobación (pero fue forzado) */
  requiresApproval: boolean;
  
  /** Score de deriva calculado */
  deltaScore: number;
  
  /** Mutación registrada (si hubo éxito) */
  mutation: PromptMutation | null;
}

/**
 * Registro de una mutación de prompt
 */
export interface PromptMutation {
  /** ID único de la mutación */
  id: string;
  
  /** Timestamp de la mutación */
  timestamp: Date;
  
  /** Descripción del cambio */
  change: string;
  
  /** Razón de la mutación */
  reason: string;
  
  /** Impacto medido como deriva */
  deltaImpact: number;
  
  /** Si fue aprobada explícitamente */
  approved: boolean;
}

/**
 * Recomendación de negociación
 */
export type NegotiationRecommendation = 'ACCEPT' | 'REVIEW' | 'REJECT';

/**
 * Resultado de una negociación de cambio de prompt
 */
export interface NegotiationResult {
  /** Score de deriva (0.0 a 1.0) */
  deltaScore: number;
  
  /** Umbral configurado */
  threshold: number;
  
  /** Si requiere aprobación */
  requiresApproval: boolean;
  
  /** Recomendación de acción */
  recommendation: NegotiationRecommendation;
  
  /** Razón de la recomendación */
  reason: string;
  
  /** Si el cambio es negociable */
  negotiable: boolean;
  
  /** Detalle de cambios */
  changes: {
    additions: number;
    deletions: number;
    semanticShift: number;
  };
}

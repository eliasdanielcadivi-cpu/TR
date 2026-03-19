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
export declare function buildSystemPrompt(params: BuildPromptParams): string;
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
export declare function updatePrompt(session: Session, newPrompt: string, force?: boolean): PromptUpdateResult;
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
export declare function negotiateChange(oldPrompt: string, newPrompt: string): NegotiationResult;
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
export declare function getDefaultPrompt(): string;
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
//# sourceMappingURL=actions.d.ts.map
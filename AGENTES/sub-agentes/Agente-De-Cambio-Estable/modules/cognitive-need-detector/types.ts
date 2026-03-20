/**
 * Tipos para el Detector de Necesidad Cognitiva
 * 
 * @module @agentedecambio2/cognitive-need-types
 */

/**
 * Modos de interacción disponibles
 */
export type InteractionMode = 'chat' | 'questionnaire' | 'mixed';

/**
 * Estado emocional del usuario
 */
export type EmotionalState = 
  | 'neutral'
  | 'confused'
  | 'resistant'
  | 'motivated'
  | 'frustrated'
  | 'uncertain';

/**
 * Tipo de dato faltante
 */
export type DataType = 'structured' | 'classification' | 'nuance' | 'emotional' | 'evidence';

/**
 * Campo de dato faltante
 */
export interface DataGap {
  field: string;
  type: DataType;
  priority: 'high' | 'medium' | 'low';
  questionType?: 'yesno' | 'truefalse' | 'single_choice' | 'multi_choice' | 'completion' | 'multiline' | 'ranking' | 'open_exploration';
}

/**
 * Estado del objetivo EMT
 */
export type ObjectiveStatus = 
  | 'undefined'           // No hay objetivo declarado
  | 'declared_but_unstructured'  // Declarado pero sin EMT
  | 'emt_defined'         // EMT completo
  | 'in_progress'         // En ejecución
  | 'completed';          // Completado

/**
 * Contexto de sesión para análisis cognitivo
 */
export interface SessionContext {
  sessionId: string;
  currentMode: InteractionMode;
  lastMessage: string;
  messageHistory: Array<{
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  }>;
  objectiveStatus: ObjectiveStatus;
  missingDataFields: DataGap[];
  userEmotionalState?: EmotionalState;
  consecutiveChatMessages?: number;
  lastQuestionnaireTime?: Date;
}

/**
 * Decisión de modo con razonamiento
 */
export interface ModeDecision {
  mode: InteractionMode;
  reason: string;
  urgency: 'high' | 'medium' | 'low';
  fields?: DataGap[];
  sequence?: InteractionMode[];  // Para modo mixto
  estimatedTime?: string;  // Ej: "2-3 minutos"
}

/**
 * Evaluación de estado emocional
 */
export interface EmotionalEvaluation {
  state: EmotionalState;
  confidence: number;  // 0-1
  indicators: string[];
  recommendedApproach: string;
}

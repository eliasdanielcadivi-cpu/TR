/**
 * Cognitive Need Detector - Acciones Principales
 * 
 * @description
 * Detecta qué tipo de información falta y decide el modo adecuado
 * (chat, cuestionario o mixto) según el contexto de la sesión.
 * 
 * @module @agentedecambio2/cognitive-need-detector
 */

import type { 
  SessionContext, 
  ModeDecision, 
  DataGap,
  EmotionalState,
  EmotionalEvaluation 
} from './types';

/**
 * analyzeCognitiveNeed - Detecta qué tipo de información falta
 * 
 * @param context - Estado actual de la sesión
 * @returns Decisión de modo con razonamiento
 * 
 * REGLAS (del Diagrama 02):
 * - Dato binario/confirmación → questionnaire (yesno/truefalse)
 * - Contexto rico/desconocido → chat (exploración)
 * - Clasificación necesaria → questionnaire (single/multichoice)
 * - Matiz emocional → chat (multiline)
 * - Orden/prioridad → questionnaire (ranking)
 */
export function analyzeCognitiveNeed(context: SessionContext): ModeDecision {
  const { 
    objectiveStatus, 
    missingDataFields, 
    userEmotionalState,
    consecutiveChatMessages,
    currentMode 
  } = context;
  
  // REGLA 1: Objetivo nuevo/ambiguo → Cuestionario (Fase 0-1 del flujo ideal)
  if (objectiveStatus === 'undefined' || objectiveStatus === 'declared_but_unstructured') {
    return { 
      mode: 'questionnaire', 
      reason: 'EMT_EXTRACTION_NEEDED', 
      urgency: 'high',
      estimatedTime: '2-3 minutos'
    };
  }
  
  // REGLA 2: Faltan datos críticos estructurados → Cuestionario
  const structuredGaps = missingDataFields.filter(f => f.type === 'structured');
  if (structuredGaps.length > 0) {
    return { 
      mode: 'questionnaire', 
      reason: 'STRUCTURED_DATA_MISSING', 
      fields: structuredGaps,
      urgency: 'high',
      estimatedTime: '1-2 minutos'
    };
  }
  
  // REGLA 3: Usuario confuso/bloqueado emocionalmente → Chat
  if (userEmotionalState === 'confused' || userEmotionalState === 'resistant') {
    return { 
      mode: 'chat', 
      reason: 'EMOTIONAL_EXPLORATION_NEEDED',
      urgency: 'medium'
    };
  }
  
  // REGLA 4: Necesita clasificación + matiz → Mixto
  const hasClassification = missingDataFields.some(f => f.type === 'classification');
  const hasNuance = missingDataFields.some(f => f.type === 'nuance');
  
  if (hasClassification && hasNuance) {
    return { 
      mode: 'mixed', 
      reason: 'CLASSIFICATION_PLUS_NUANCE',
      sequence: ['questionnaire', 'chat'], // Primero estructura, luego profundidad
      urgency: 'medium',
      estimatedTime: '3-5 minutos'
    };
  }
  
  // REGLA 5: Demasiados mensajes de chat sin estructura → Cuestionario de síntesis
  if ((consecutiveChatMessages || 0) >= 5 && currentMode === 'chat') {
    return { 
      mode: 'questionnaire', 
      reason: 'SYNTHESIS_NEEDED',
      urgency: 'low',
      estimatedTime: '1 minuto'
    };
  }
  
  // DEFAULT: Mantener modo actual
  return { 
    mode: currentMode, 
    reason: 'CONTINUITY',
    urgency: 'low'
  };
}

/**
 * evaluateDataGaps - Evalúa datos faltantes estructurados
 * 
 * @param context - Estado actual de la sesión
 * @returns Lista de datos faltantes priorizados
 */
export function evaluateDataGaps(context: SessionContext): DataGap[] {
  const { objectiveStatus, lastMessage } = context;
  const gaps: DataGap[] = [];
  
  // Si no hay EMT definido, faltan todos los campos EMT
  if (objectiveStatus === 'undefined' || objectiveStatus === 'declared_but_unstructured') {
    gaps.push(
      { 
        field: 'evidence', 
        type: 'structured', 
        priority: 'high',
        questionType: 'completion'
      },
      { 
        field: 'metric', 
        type: 'structured', 
        priority: 'high',
        questionType: 'completion'
      },
      { 
        field: 'deadline', 
        type: 'structured', 
        priority: 'high',
        questionType: 'completion'
      }
    );
  }
  
  // Detectar si faltan datos de clasificación en el mensaje
  if (needsClassification(lastMessage)) {
    gaps.push({
      field: 'classification',
      type: 'classification',
      priority: 'medium',
      questionType: 'single_choice'
    });
  }
  
  // Detectar si faltan matices/emoción
  if (needsNuance(lastMessage)) {
    gaps.push({
      field: 'nuance',
      type: 'nuance',
      priority: 'low',
      questionType: 'multiline'
    });
  }
  
  return gaps.sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
}

/**
 * detectEmotionalState - Detecta estado emocional del usuario
 * 
 * @param message - Último mensaje del usuario
 * @returns Evaluación emocional con confianza
 */
export function detectEmotionalState(message: string): EmotionalEvaluation {
  const indicators: string[] = [];
  let state: EmotionalState = 'neutral';
  let confidence = 0.5;
  
  // Palabras clave de confusión
  const confusionKeywords = ['no entiendo', 'confuso', 'no sé', 'duda', 'qué hago'];
  if (confusionKeywords.some(k => message.toLowerCase().includes(k))) {
    state = 'confused';
    confidence = 0.8;
    indicators.push('keywords_confusion');
  }
  
  // Palabras clave de resistencia
  const resistanceKeywords = ['no puedo', 'imposible', 'no tengo tiempo', 'después', 'ya veré'];
  if (resistanceKeywords.some(k => message.toLowerCase().includes(k))) {
    state = 'resistant';
    confidence = 0.75;
    indicators.push('avoidance_language');
  }
  
  // Palabras clave de frustración
  const frustrationKeywords = ['fracasé', 'no funciona', 'siempre igual', 'nunca puedo'];
  if (frustrationKeywords.some(k => message.toLowerCase().includes(k))) {
    state = 'frustrated';
    confidence = 0.85;
    indicators.push('self_defeating_language');
  }
  
  // Palabras clave de motivación
  const motivationKeywords = ['quiero', 'voy a', 'haré', 'listo', 'vamos', 'puedo'];
  if (motivationKeywords.some(k => message.toLowerCase().includes(k))) {
    state = 'motivated';
    confidence = 0.7;
    indicators.push('action_oriented_language');
  }
  
  // Signos de puntuación (exclamación = energía)
  if (message.includes('!')) {
    confidence += 0.1;
    indicators.push('exclamation_marks');
  }
  
  // Puntos suspensivos = incertidumbre
  if (message.includes('...')) {
    if (state === 'neutral') state = 'uncertain';
    confidence += 0.1;
    indicators.push('ellipsis');
  }
  
  // Recomendar enfoque según estado
  const recommendedApproach = getRecommendedApproach(state);
  
  return {
    state,
    confidence: Math.min(confidence, 1.0),
    indicators,
    recommendedApproach
  };
}

/**
 * Helpers privados
 */

function needsClassification(message: string): boolean {
  // Detectar si el usuario menciona múltiples opciones o categorías
  const classificationPatterns = [
    /\b(o|ó)\b/i,  // "opción A o B"
    /\bentre\b/i,  // "entre esto y aquello"
    /\bdepende\b/i,  // "depende de..."
    /\bquizás\b/i,  // "quizás esto, quizás aquello"
  ];
  
  return classificationPatterns.some(p => p.test(message));
}

function needsNuance(message: string): boolean {
  // Detectar si el usuario expresa emoción o matiz
  const nuancePatterns = [
    /\bsiento\b/i,
    /\bme siento\b/i,
    /\bme preocupa\b/i,
    /\bme gusta\b/i,
    /\bno me gusta\b/i,
    /\bcreo que\b/i,
    /\bpienso que\b/i,
  ];
  
  return nuancePatterns.some(p => p.test(message));
}

function getRecommendedApproach(state: EmotionalState): string {
  const approaches: Record<EmotionalState, string> = {
    neutral: 'Continuar con enfoque estándar',
    confused: 'Simplificar, usar ejemplos concretos, evitar jerga',
    resistant: 'Validar preocupación, ofrecer autonomía, reducir fricción',
    motivated: 'Capitalizar momentum, pedir acción inmediata',
    frustrated: 'Validar emoción, reframing cognitivo, micro-pasos',
    uncertain: 'Ofrecer estructura, reducir opciones, dar seguridad'
  };
  
  return approaches[state] || 'Continuar con enfoque estándar';
}

/**
 * Mode Transition Engine - Acciones Principales
 * 
 * @description
 * Genera transiciones conversacionales suaves entre modos.
 * Estrategia: Nunca decir "ahora cambio a cuestionario".
 * Frasear como continuación natural: "Para avanzar, me gustaría..."
 * 
 * @module @agentedecambio2/mode-transition-engine
 */

import type { SessionContext, InteractionMode } from '../cognitive-need-detector/types';

/**
 * Mensaje de transición con metadatos
 */
export interface TransitionMessage {
  message: string;
  preserveContext: boolean;
  estimatedTime?: string;
  tone?: 'formal' | 'casual' | 'empathetic';
}

/**
 * generateTransitionPrompt - Crea el puente conversacional entre modos
 * 
 * ESTRATEGIA (Bernays + Humanismo):
 * - Nunca decir "ahora cambio a cuestionario"
 * - Frasear como continuación natural
 * - Dar autonomía: "¿Te parece si...?"
 * 
 * @param fromMode - Modo actual
 * @param toMode - Modo destino
 * @param reason - Razón del cambio (del detector)
 * @param context - Contexto de sesión
 * @returns Mensaje de transición con tono adecuado
 */
export function generateTransitionPrompt(
  fromMode: InteractionMode,
  toMode: InteractionMode,
  reason: string,
  context?: SessionContext
): TransitionMessage {
  
  const templates = TRANSITION_TEMPLATES[`${fromMode}_to_${toMode}`];
  
  if (!templates) {
    return {
      message: "Continuemos...",
      preserveContext: true,
      estimatedTime: undefined
    };
  }
  
  const template = templates[reason as keyof typeof templates] || templates.default;
  
  return {
    message: typeof template === 'function' ? template(context) : template,
    preserveContext: true,
    estimatedTime: toMode === 'questionnaire' ? '2-3 minutos' : undefined,
    tone: reason.includes('EMOTIONAL') ? 'empathetic' : 'casual'
  };
}

/**
 * buildContextSummary - Resume contexto para inyectar en transición
 * 
 * @param context - Contexto de sesión
 * @returns Resumen en lenguaje natural
 */
export function buildContextSummary(context: SessionContext): string {
  const { lastMessage, messageHistory } = context;
  
  // Últimos 3 mensajes
  const recentMessages = messageHistory.slice(-3);
  
  if (recentMessages.length === 0) {
    return lastMessage;
  }
  
  const summary = recentMessages
    .filter(m => m.role === 'user')
    .map(m => truncate(m.content, 100))
    .join(' → ');
  
  return summary || lastMessage;
}

/**
 * createBridgeMessage - Construye mensaje completo de transición
 * 
 * @param transition - Mensaje de transición
 * @param context - Contexto de sesión
 * @returns Mensaje completo con contexto inyectado
 */
export function createBridgeMessage(
  transition: TransitionMessage,
  context: SessionContext
): string {
  if (!transition.preserveContext) {
    return transition.message;
  }
  
  const contextSummary = buildContextSummary(context);
  
  // Si el contexto es muy corto, no hace falta resumir
  if (contextSummary.length < 50) {
    return transition.message;
  }
  
  // Inyectar contexto como puente
  return `${transition.message}\n\n(Para contexto: ${contextSummary}...)`;
}

/**
 * Plantillas de transición organizadas por tipo
 */
const TRANSITION_TEMPLATES = {
  // De chat a cuestionario
  chat_to_questionnaire: {
    emt_extraction: "Perfecto, estoy captando tu objetivo. Para asegurarme de que lo entiendo exactamente, me gustaría que me ayudes a estructurarlo en tres puntos: ¿qué evidencia concreta quieres ver, qué métrica lo medirá, y para cuándo? Esto nos ayudará a mantener el rumbo.",
    
    structured_data: "Entiendo la situación. Para no perder detalles importantes, ¿te parece si organizamos la siguiente parte en opciones? Así puedes elegir rápido y añadir cualquier matiz al final.",
    
    classification: "Hay varias formas de abordar esto. Para elegir la mejor estrategia para tu caso específico, dime: ¿cuál de estas opciones se acerca más a tu situación actual?",
    
    synthesis_needed: "Hemos hablado de varios puntos importantes. Para asegurarme de que no se nos escapa nada clave, ¿te parece si organizamos todo en una síntesis rápida?",
    
    default: "Para avanzar de la mejor manera, me gustaría hacerte algunas preguntas específicas. ¿Te parece bien?"
  },
  
  // De cuestionario a chat
  questionnaire_to_chat: {
    emotional_block: "Gracias por esas respuestas. Noto que hay algo más detrás de esto... ¿Te gustaría contarme un poco más sobre cómo te sientes con este objetivo?",
    
    exploration_needed: "Antes de continuar con la siguiente pregunta, me gustaría entender mejor tu contexto. ¿Qué te llevó a elegir esa opción?",
    
    nuance_needed: "Perfecto, ya tengo la estructura clara. Ahora, ¿hay algún matiz o detalle importante que quieras añadir y que no encaje en las opciones?",
    
    default: "Gracias por las respuestas. ¿Hay algo más que quieras añadir o profundizar sobre esto?"
  },
  
  // A modo mixto
  to_mixed: {
    classification_plus_nuance: "Vamos a organizar esto en dos pasos: primero una selección rápida, y luego me cuentas los detalles importantes. ¿Listo?",
    
    structured_then_exploration: "Primero vamos a definir los puntos clave de forma estructurada, y después profundizamos en lo que sea más relevante para ti.",
    
    default: "Te propongo hacer esto en dos partes: primero organizamos las ideas principales, y luego profundizamos en lo que necesites."
  },
  
  // Transiciones dentro del mismo modo (refinamiento)
  chat_to_chat: {
    deepening: "Esto es interesante. Cuéntame más sobre...",
    redirecting: "Entiendo. Volviendo a lo que mencionaste antes sobre...",
    default: "Continuemos..."
  },
  
  questionnaire_to_questionnaire: {
    next_question: "Perfecto. Ahora, otra pregunta importante...",
    clarification: "Para asegurarme de entender bien tu respuesta anterior...",
    default: "Continuemos con la siguiente pregunta..."
  }
};

/**
 * Helpers privados
 */

function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

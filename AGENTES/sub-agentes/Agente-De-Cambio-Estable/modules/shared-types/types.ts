/**
 * Shared Types - Tipos compartidos entre frontend y backend
 * 
 * @module @agentedecambio2/shared-types
 * @version 0.1.0
 * 
 * @description
 * Este módulo centraliza todos los tipos TypeScript que son
 * compartidos entre el frontend (web) y backend (server).
 * 
 * Propósito:
 * - Evitar duplicación de tipos
 * - Garantizar consistencia entre cliente y servidor
 * - Facilitar mantenimiento (un solo lugar para actualizar)
 * 
 * @example
 * ```typescript
 * // En frontend o backend
 * import type { ChatMessage, Session, ChatMode } from './types';
 * 
 * const message: ChatMessage = {
 *   id: 'msg_123',
 *   role: 'user',
 *   content: 'Hola',
 *   timestamp: new Date()
 * };
 * ```
 */

// ============================================================================
// MODOS DE INTERACCIÓN
// ============================================================================

/**
 * Modo de interacción del chat
 * 
 * @description
 * Define cómo el usuario interactúa con el sistema:
 * - `chat`: Conversación fluida y abierta
 * - `questionnaire`: Navegación guiada con preguntas estructuradas
 */
export type ChatMode = 'chat' | 'questionnaire';

// ============================================================================
// MENSAJES
// ============================================================================

/**
 * Rol de un mensaje en la conversación
 */
export type MessageRole = 'user' | 'assistant' | 'system';

/**
 * Mensaje individual en el chat
 * 
 * @description
 * Representa un mensaje enviado o recibido en la conversación.
 * Incluye metadatos opcionales para información adicional.
 */
export interface ChatMessage {
  /** ID único del mensaje */
  id: string;
  
  /** Rol del emisor del mensaje */
  role: MessageRole;
  
  /** Contenido textual del mensaje */
  content: string;
  
  /** Timestamp cuando se creó el mensaje */
  timestamp: Date;
  
  /** 
   * Metadatos opcionales
   * @description Información adicional sobre el mensaje
   */
  metadata?: {
    /** Si el mensaje fue generado con modo reasoning activado */
    reasoning?: boolean;
    /** Modo en que se generó el mensaje */
    mode?: ChatMode;
    /** Score de deriva del prompt (si aplica) */
    deltaScore?: number;
  };
}

// ============================================================================
// SESIONES
// ============================================================================

/**
 * Sesión de conversación activa
 * 
 * @description
 * Contiene todo el estado de una sesión de conversación,
 * incluyendo mensajes, prompt del sistema y objetivos.
 */
export interface Session {
  /** ID único de la sesión */
  id: string;
  
  /** Historial de mensajes de la sesión */
  messages: ChatMessage[];
  
  /** System prompt actual (puede mutar durante la sesión) */
  systemPrompt: string;
  
  /** Lista de objetivos activos del usuario */
  objectives: string[];
  
  /** Pregunta actual en modo cuestionario (si aplica) */
  currentQuestion?: Question;
  
  /** Timestamp de creación de la sesión */
  createdAt: Date;
  
  /** Timestamp de última actualización */
  updatedAt: Date;
}

// ============================================================================
// CUESTIONARIO
// ============================================================================

/**
 * Tipo de pregunta en modo cuestionario
 */
export type QuestionType = 'single_choice' | 'multiple_choice' | 'yes_no' | 'open';

/**
 * Opción individual dentro de una pregunta
 */
export interface QuestionOption {
  /** ID único de la opción */
  id: string;
  
  /** Etiqueta visible para el usuario */
  label: string;
  
  /** Valor interno de la opción */
  value: string;
}

/**
 * Pregunta en modo cuestionario
 * 
 * @description
 * Representa una pregunta estructurada con opciones de respuesta.
 * Usada en modo questionnaire para guiar al usuario.
 */
export interface Question {
  /** ID único de la pregunta */
  id: string;
  
  /** Tipo de pregunta (determina cómo se renderiza) */
  type: QuestionType;
  
  /** Texto de la pregunta */
  question: string;
  
  /** Opciones de respuesta (no presente en preguntas abiertas) */
  options?: QuestionOption[];
}

// ============================================================================
// MÉTRICAS DE DERIVA
// ============================================================================

/**
 * Métricas de deriva del system prompt
 * 
 * @description
 * Calcula cuánto ha cambiado el system prompt respecto a su versión original.
 * Usado para determinar si un cambio requiere aprobación del usuario.
 */
export interface DeltaMetrics {
  /** Score actual de deriva (0.0 = sin cambios, 1.0 = cambio total) */
  currentScore: number;
  
  /** Umbral configurado para requerir aprobación */
  threshold: number;
  
  /** Si el cambio excede el umbral y requiere aprobación */
  requiresApproval: boolean;
  
  /** Detalle de los cambios */
  changes: {
    /** Cantidad de adiciones al prompt */
    additions: number;
    /** Cantidad de eliminaciones del prompt */
    deletions: number;
    /** Score de cambio semántico */
    semanticShift: number;
  };
}

// ============================================================================
// MUTACIONES DE PROMPT
// ============================================================================

/**
 * Registro de una mutación del system prompt
 * 
 * @description
 * Traza los cambios realizados al system prompt durante una sesión.
 * Usado para auditoría y posible reversión.
 */
export interface PromptMutation {
  /** ID único de la mutación */
  id: string;
  
  /** Timestamp cuando ocurrió la mutación */
  timestamp: Date;
  
  /** Descripción del cambio realizado */
  change: string;
  
  /** Razón o justificación del cambio */
  reason: string;
  
  /** Impacto medido en términos de deriva */
  deltaImpact: number;
  
  /** Si la mutación fue aprobada explícitamente */
  approved: boolean;
}

// ============================================================================
// CONTEXTO DE MENSAJE
// ============================================================================

/**
 * Contexto adicional para enviar un mensaje
 * 
 * @description
 * Información extra que acompaña un mensaje para dar contexto
 * al backend sobre cómo procesarlo.
 */
export interface MessageContext {
  /** Si el modo reasoning está activado */
  isReasoning: boolean;
  
  /** ID de la sesión actual */
  sessionId: string;
  
  /** Objetivos activos (opcional, para inyectar en el prompt) */
  objectives?: string[];
}

// ============================================================================
// EVENTOS SOCKET.IO
// ============================================================================

/**
 * Eventos que el servidor envía al cliente
 * 
 * @description
 * Define el contrato de eventos Server-to-Client en Socket.IO
 */
export interface ServerToClientEvents {
  /** Chunk de texto en streaming */
  'message:stream': (chunk: string) => void;
  /** Mensaje completo del asistente */
  'message:complete': (message: ChatMessage) => void;
  /** Cambio en el system prompt */
  'prompt:mutation': (mutation: PromptMutation) => void;
  /** Nueva pregunta en modo cuestionario */
  'question:next': (question: Question) => void;
  /** Cambio de modo chat/cuestionario */
  'mode:switch': (mode: ChatMode) => void;
  /** Actualización de métricas de deriva */
  'delta:update': (delta: DeltaMetrics) => void;
  /** Error ocurrido */
  'error': (error: string) => void;
}

/**
 * Eventos que el cliente envía al servidor
 * 
 * @description
 * Define el contrato de eventos Client-to-Server en Socket.IO
 */
export interface ClientToServerEvents {
  /** Enviar mensaje del usuario */
  'message:send': (content: string, mode: ChatMode, context: MessageContext) => void;
  /** Actualizar system prompt manualmente */
  'prompt:update': (content: string) => void;
  /** Seleccionar opción en cuestionario */
  'option:select': (questionId: string, optionId: string, comment?: string) => void;
  /** Cambiar modo de interacción */
  'mode:set': (mode: ChatMode) => void;
  /** Activar/desactivar modo reasoning */
  'reasoning:toggle': (enabled: boolean) => void;
  /** Inicializar o recuperar sesión */
  'session:init': (sessionId?: string) => void;
}

// ============================================================================
// UTILIDADES
// ============================================================================

/**
 * Extrae el tipo de mensaje de un rol dado
 * 
 * @template T - Tipo de rol
 */
export type MessageByRole<T extends MessageRole> = ChatMessage & { role: T };

/**
 * Crea un tipo parcial con campos requeridos específicos
 * 
 * @template T - Tipo base
 * @template K - Campos que permanecen requeridos
 */
export type PartialWithRequired<T, K extends keyof T> = Partial<T> & Pick<T, K>;

/**
 * Session Manager - Módulo para gestión de sesiones de conversación
 * 
 * @module @agentedecambio2/session-manager
 * @version 0.1.0
 * 
 * @description
 * Este módulo gestiona el ciclo de vida de las sesiones de conversación.
 * Cada sesión contiene:
 * - Historial de mensajes
 * - System prompt actual (puede mutar)
 * - Objetivos del usuario
 * - Metadatos de tiempo
 * 
 * @example
 * ```typescript
 * import { createSession, getSession, updateSession } from './actions';
 * 
 * // Crear sesión
 * const session = createSession();
 * console.log(session.id); // 'sess_1234567890_abc'
 * 
 * // Obtener sesión
 * const retrieved = getSession(session.id);
 * console.log(retrieved?.messages.length); // 0
 * 
 * // Actualizar sesión
 * updateSession(session.id, {
 *   systemPrompt: 'Nuevo prompt'
 * });
 * ```
 * 
 * @see {@link ./INDEX.md} para documentación completa del módulo
 */

import type { Session, ChatMessage } from '../shared-types/types';

// ============================================================================
// ALMACENAMIENTO EN MEMORIA
// ============================================================================

/**
 * Almacenamiento temporal de sesiones
 * 
 * @description
 * Mapa en memoria que guarda las sesiones activas.
 * En producción, reemplazar con Redis o base de datos.
 * 
 * @internal
 */
const sessions = new Map<string, Session>();

// ============================================================================
// FUNCIONES EXPORTADAS
// ============================================================================

/**
 * Crea una nueva sesión de conversación
 * 
 * @description
 * Inicializa una sesión con valores por defecto:
 * - systemPrompt: Prompt base de extracción cognitiva
 * - messages: Array vacío
 * - objectives: Array vacío
 * 
 * @param sessionId - ID opcional para la sesión (genera uno automático si no se proporciona)
 * 
 * @returns {Session} La nueva sesión creada
 * 
 * @example
 * ```typescript
 * // Crear con ID automático
 * const session = createSession();
 * console.log(session.id); // 'sess_1708819200000_xyz'
 * ```
 * 
 * @example
 * ```typescript
 * // Crear con ID personalizado
 * const session = createSession('mi-sesion-123');
 * console.log(session.id); // 'mi-sesion-123'
 * ```
 */
export function createSession(sessionId?: string): Session {
  const id = sessionId || `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  const session: Session = {
    id,
    messages: [],
    systemPrompt: `Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente.`,
    objectives: [],
    createdAt: new Date(),
    updatedAt: new Date(),
  };
  
  sessions.set(id, session);
  return session;
}

/**
 * Obtiene una sesión por su ID
 * 
 * @description
 * Recupera una sesión previamente creada del almacenamiento.
 * Retorna undefined si la sesión no existe.
 * 
 * @param sessionId - ID de la sesión a recuperar
 * 
 * @returns {Session | undefined} La sesión o undefined si no existe
 * 
 * @example
 * ```typescript
 * const session = createSession();
 * const retrieved = getSession(session.id);
 * console.log(retrieved?.id === session.id); // true
 * 
 * const notFound = getSession('id-inexistente');
 * console.log(notFound); // undefined
 * ```
 */
export function getSession(sessionId: string): Session | undefined {
  return sessions.get(sessionId);
}

/**
 * Actualiza una sesión existente
 * 
 * @description
 * Modifica los campos especificados de una sesión y actualiza el timestamp.
 * Los campos no especificados mantienen su valor actual.
 * 
 * @param sessionId - ID de la sesión a actualizar
 * @param updates - Campos a actualizar (parcial)
 * 
 * @returns {boolean} True si se actualizó, false si la sesión no existe
 * 
 * @example
 * ```typescript
 * const session = createSession();
 * 
 * // Actualizar system prompt
 * const success = updateSession(session.id, {
 *   systemPrompt: 'Nuevo prompt personalizado'
 * });
 * console.log(success); // true
 * 
 * // Actualizar con mensaje
 * updateSession(session.id, {
 *   messages: [...session.messages, newMessage]
 * });
 * ```
 * 
 * @example
 * ```typescript
 * // Intentar actualizar sesión inexistente
 * const result = updateSession('id-inexistente', { systemPrompt: 'nuevo' });
 * console.log(result); // false
 * ```
 */
export function updateSession(sessionId: string, updates: Partial<Session>): boolean {
  const session = sessions.get(sessionId);
  
  if (!session) {
    return false;
  }
  
  // Aplicar actualizaciones parciales
  Object.assign(session, updates, { updatedAt: new Date() });
  
  return true;
}

/**
 * Elimina una sesión del almacenamiento
 * 
 * @description
 * Remueve permanentemente una sesión del sistema.
 * Usar con precaución - no hay recuperación.
 * 
 * @param sessionId - ID de la sesión a eliminar
 * 
 * @returns {boolean} True si se eliminó, false si no existía
 * 
 * @example
 * ```typescript
 * const session = createSession();
 * const deleted = deleteSession(session.id);
 * console.log(deleted); // true
 * console.log(getSession(session.id)); // undefined
 * ```
 */
export function deleteSession(sessionId: string): boolean {
  return sessions.delete(sessionId);
}

/**
 * Lista todas las sesiones activas
 * 
 * @description
 * Retorna un array con los IDs de todas las sesiones actualmente en memoria.
 * Útil para debugging y administración.
 * 
 * @returns {string[]} Array de IDs de sesiones
 * 
 * @example
 * ```typescript
 * createSession('session-1');
 * createSession('session-2');
 * 
 * const allSessions = listSessions();
 * console.log(allSessions); // ['session-1', 'session-2']
 * ```
 */
export function listSessions(): string[] {
  return Array.from(sessions.keys());
}

/**
 * Obtiene estadísticas del almacenamiento de sesiones
 * 
 * @description
 * Retorna información sobre el estado actual del almacenamiento:
 * - Cantidad de sesiones activas
 * - Timestamp de esta consulta
 * 
 * @returns {SessionStats} Estadísticas del almacenamiento
 * 
 * @example
 * ```typescript
 * createSession();
 * createSession();
 * 
 * const stats = getSessionStats();
 * console.log(stats.count); // 2
 * console.log(stats.timestamp); // Date
 * ```
 */
export function getSessionStats(): SessionStats {
  return {
    count: sessions.size,
    timestamp: new Date(),
  };
}

// ============================================================================
// TIPOS
// ============================================================================

/**
 * Estadísticas del almacenamiento de sesiones
 */
export interface SessionStats {
  /** Cantidad de sesiones activas en memoria */
  count: number;
  
  /** Timestamp de cuando se generaron las estadísticas */
  timestamp: Date;
}

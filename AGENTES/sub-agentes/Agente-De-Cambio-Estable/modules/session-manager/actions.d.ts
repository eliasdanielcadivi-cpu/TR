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
import type { Session } from '../shared-types/types';
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
export declare function createSession(sessionId?: string): Session;
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
export declare function getSession(sessionId: string): Session | undefined;
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
export declare function updateSession(sessionId: string, updates: Partial<Session>): boolean;
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
export declare function deleteSession(sessionId: string): boolean;
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
export declare function listSessions(): string[];
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
export declare function getSessionStats(): SessionStats;
/**
 * Estadísticas del almacenamiento de sesiones
 */
export interface SessionStats {
    /** Cantidad de sesiones activas en memoria */
    count: number;
    /** Timestamp de cuando se generaron las estadísticas */
    timestamp: Date;
}
//# sourceMappingURL=actions.d.ts.map
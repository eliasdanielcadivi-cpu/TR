"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
//# sourceMappingURL=types.js.map
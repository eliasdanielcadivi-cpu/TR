"use strict";
/**
 * Eventos para [nombre-modulo]
 *
 * @module [nombre-modulo]/events
 * @version 0.1.0
 *
 * @description
 * Este módulo define los eventos que [nombre-modulo] emite y escucha.
 * Los eventos siguen el patrón Event-Driven Architecture para desacoplamiento.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.eventEmitter = void 0;
exports.subscribeToExternalEvents = subscribeToExternalEvents;
const events_1 = require("events");
/**
 * Instancia del EventEmitter para este módulo
 *
 * @example
 * ```typescript
 * import { eventEmitter } from './events';
 *
 * // Suscribirse
 * eventEmitter.on('evento-emitido', (payload) => {
 *   console.log('Evento recibido:', payload);
 * });
 *
 * // Emitir
 * eventEmitter.emit('evento-emitido', { propiedad: 'valor' });
 * ```
 */
exports.eventEmitter = new events_1.EventEmitter();
/**
 * Suscribe este módulo a eventos externos
 *
 * @description
 * Configura los listeners para eventos que este módulo necesita escuchar.
 * Debe llamarse una vez durante la inicialización.
 *
 * @example
 * ```typescript
 * import { subscribeToExternalEvents } from './events';
 *
 * subscribeToExternalEvents(externalEventEmitter);
 * ```
 */
function subscribeToExternalEvents(externalEmitter) {
    externalEmitter.on('evento-externo', (payload) => {
        // Manejar evento
        console.log('Evento externo recibido:', payload);
    });
}
//# sourceMappingURL=events.js.map
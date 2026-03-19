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
import { EventEmitter } from 'events';
/**
 * Mapa de eventos emitidos por este módulo
 */
export interface ModuleEvents {
    /**
     * Se emite cuando [condición]
     *
     * @payload
     * - `propiedad` - [Descripción]
     */
    'evento-emitido': (payload: {
        propiedad: string;
    }) => void;
}
/**
 * Mapa de eventos que este módulo escucha
 */
export interface ExternalEvents {
    /**
     * Se escucha para [propósito]
     *
     * @payload
     * - `dato` - [Descripción]
     */
    'evento-externo': (payload: {
        dato: number;
    }) => void;
}
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
export declare const eventEmitter: EventEmitter<[never]>;
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
export declare function subscribeToExternalEvents(externalEmitter: EventEmitter): void;
//# sourceMappingURL=events.d.ts.map
"use strict";
/**
 * Tipos TypeScript para [nombre-modulo]
 *
 * @module [nombre-modulo]/types
 * @version 0.1.0
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.NetworkError = exports.ValidationError = void 0;
/**
 * Errores específicos del módulo
 */
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}
exports.ValidationError = ValidationError;
class NetworkError extends Error {
    constructor(message) {
        super(message);
        this.name = 'NetworkError';
    }
}
exports.NetworkError = NetworkError;
//# sourceMappingURL=types.js.map
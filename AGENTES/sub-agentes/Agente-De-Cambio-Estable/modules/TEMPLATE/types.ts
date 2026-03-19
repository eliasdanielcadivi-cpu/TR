/**
 * Tipos TypeScript para [nombre-modulo]
 * 
 * @module [nombre-modulo]/types
 * @version 0.1.0
 */

/**
 * Parámetros para [nombreFuncion1]
 * 
 * @description
 * [Descripción de cuándo y cómo usar estos parámetros]
 */
export interface Params {
  /**
   * [Descripción de param1]
   * 
   * @example "valor-ejemplo"
   */
  param1: string;

  /**
   * [Descripción de param2]
   * 
   * @default 0
   */
  param2?: number;
}

/**
 * Resultado de [nombreFuncion1]
 * 
 * @description
 * [Qué representa este resultado y cómo interpretarlo]
 */
export interface Result {
  /**
   * [Descripción de la propiedad]
   */
  propiedad: string;

  /**
   * [Descripción de la propiedad]
   */
  exito: boolean;
}

/**
 * Parámetros para [nombreFuncion2]
 */
export interface ConfigParams {
  /**
   * Configuración opcional
   */
  config?: {
    /**
     * [Descripción]
     */
    option?: boolean;
  };
}

/**
 * Errores específicos del módulo
 */
export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

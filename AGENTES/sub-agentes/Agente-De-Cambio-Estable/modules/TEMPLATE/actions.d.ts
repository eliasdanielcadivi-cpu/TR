/**
 * [nombreModulo] - Módulo para [propósito general del módulo]
 *
 * @module [nombre-modulo]
 * @version 0.1.0
 *
 * @description
 * Este módulo proporciona [1-3 funcionalidades principales].
 *
 * @example
 * ```typescript
 * import { accion1, accion2 } from './actions';
 *
 * const resultado = await accion1({ param1: 'valor' });
 * ```
 *
 * @see {@link ./INDEX.md} para documentación completa
 */
/**
 * [nombreFuncion1] - [Verbo en presente] [qué hace]
 *
 * @description
 * [Descripción detallada de 2-3 líneas sobre qué hace esta función,
 * por qué existe y cuándo debe usarse]
 *
 * @param params - Parámetros de entrada
 * @param params.param1 - [Descripción del parámetro]
 * @param params.param2 - [Descripción del parámetro]
 *
 * @returns [Tipo de retorno] - [Qué devuelve y qué significa]
 *
 * @throws [NombreError] - [Cuándo lanza este error]
 * @throws [NombreError2] - [Cuándo lanza este error]
 *
 * @example
 * ```typescript
 * const resultado = await accion1({ param1: 'valor', param2: 123 });
 * console.log(resultado); // { propiedad: 'valor' }
 * ```
 *
 * @example
 * ```typescript
 * // Caso de error
 * try {
 *   await accion1({ param1: '' }); // Error: param1 no puede estar vacío
 * } catch (error) {
 *   console.error(error.message);
 * }
 * ```
 *
 * @throws {ValidationError} Si param1 está vacío
 * @throws {NetworkError} Si falla la conexión
 *
 * @related
 * - {@link accion2} - [Relación con otra función]
 * - {@link ./types.ts~Params} - Tipo de parámetros
 * - {@link ./INDEX.md} - Documentación del módulo
 */
export declare function accion1({ param1, param2 }: Params): Promise<Result>;
/**
 * [nombreFuncion2] - [Verbo en presente] [qué hace]
 *
 * @description
 * [Descripción detallada]
 *
 * @param params - Parámetros de entrada
 * @param params.config - [Descripción]
 *
 * @returns [Tipo] - [Descripción]
 *
 * @example
 * ```typescript
 * await accion2({ config: { option: true } });
 * ```
 */
export declare function accion2({ config }: ConfigParams): Promise<void>;
/**
 * [nombreFuncion3] - [Verbo en presente] [qué hace]
 *
 * @description
 * [Descripción detallada]
 *
 * @param input - [Descripción del parámetro]
 *
 * @returns [Tipo] - [Descripción]
 */
export declare function accion3(input: string): string;
//# sourceMappingURL=actions.d.ts.map
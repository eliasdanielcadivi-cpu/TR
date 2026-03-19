/**
 * DeepSeek Connector - Módulo para conexión con DeepSeek API
 *
 * @module @agentedecambio2/deepseek-connector
 * @version 0.1.0
 *
 * @description
 * Este módulo proporciona conexión con la API de DeepSeek para:
 * - Completaciones de chat síncronas
 * - Streaming de respuestas en tiempo real (SSE)
 *
 * Soporta ambos modos de DeepSeek-V3.2:
 * - `deepseek-chat`: Modo sin pensamiento (respuestas directas)
 * - `deepseek-reasoner`: Modo de pensamiento (razonamiento explícito)
 *
 * @example
 * ```typescript
 * import { createCompletion, createCompletionStream } from './actions';
 *
 * // Ejemplo 1: Completación síncrona
 * const response = await createCompletion({
 *   messages: [{ role: 'user', content: 'Hola' }],
 *   apiKey: 'sk-...'
 * });
 * console.log(response.choices[0].message.content);
 * ```
 *
 * @example
 * ```typescript
 * // Ejemplo 2: Streaming de respuesta
 * const stream = createCompletionStream({
 *   messages: [{ role: 'user', content: 'Explica algo' }],
 *   apiKey: 'sk-...'
 * });
 *
 * for await (const chunk of stream) {
 *   process.stdout.write(chunk.choices[0]?.delta?.content || '');
 * }
 * ```
 *
 * @see {@link ./INDEX.md} para documentación completa del módulo
 * @see {@link https://api-docs.deepseek.com/} Documentación oficial de DeepSeek API
 */
/**
 * Rol de un mensaje en la conversación con DeepSeek
 *
 * @description
 * Los roles siguen el estándar de OpenAI Chat Completion API:
 * - `system`: Instrucciones de comportamiento para el asistente
 * - `user`: Mensaje del usuario
 * - `assistant`: Respuesta del asistente
 */
export type MessageRole = 'system' | 'user' | 'assistant';
/**
 * Mensaje individual para la API de DeepSeek
 *
 * @description
 * Cada mensaje contiene un rol y contenido de texto.
 * El contenido puede incluir texto plano o JSON según el contexto.
 */
export interface DeepSeekMessage {
    /** Rol del mensaje en la conversación */
    role: MessageRole;
    /** Contenido textual del mensaje */
    content: string;
}
/**
 * Parámetros para solicitar una completación a DeepSeek
 *
 * @description
 * Configuración completa para la API de DeepSeek.
 * Todos los parámetros son opcionales excepto `messages`.
 */
export interface DeepSeekCompletionRequest {
    /** Lista de mensajes que forman el contexto de la conversación */
    messages: DeepSeekMessage[];
    /**
     * Modelo a utilizar
     * @default 'deepseek-chat'
     * @see 'deepseek-chat' - Modo sin pensamiento
     * @see 'deepseek-reasoner' - Modo de pensamiento
     */
    model?: string;
    /**
     * Temperatura para control de aleatoriedad (0.0 - 2.0)
     * @default 0.7
     * @description Valores bajos = más determinista, valores altos = más creativo
     */
    temperature?: number;
    /**
     * Habilitar streaming de respuesta
     * @default false
     * @description Si es true, devuelve chunks en lugar de respuesta completa
     */
    stream?: boolean;
    /**
     * Máximo de tokens a generar
     * @default 4096
     * @description Limita la longitud de la respuesta
     */
    max_tokens?: number;
    /**
     * Formato de respuesta esperado
     * @default { type: 'text' }
     * @description 'json_object' fuerza salida JSON válida
     */
    response_format?: {
        type: 'json_object' | 'text';
    };
    /**
     * API Key de DeepSeek (requerida para autenticación)
     * @description Debe obtenerse en https://platform.deepseek.com/api_keys
     */
    apiKey: string;
}
/**
 * Respuesta completa de la API de DeepSeek
 *
 * @description
 * Contiene la respuesta del modelo junto con metadatos de uso de tokens.
 * Los campos de caché (prompt_cache_hit_tokens) pueden estar presentes
 * si la solicitud aprovechó el caché de contexto de DeepSeek.
 */
export interface DeepSeekCompletionResponse {
    /** ID único de esta completación */
    id: string;
    /** Lista de elecciones generadas por el modelo */
    choices: Array<{
        /** Mensaje generado por el asistente */
        message: DeepSeekMessage;
        /** Razón por la cual la generación terminó */
        finish_reason: string;
        /** Índice de esta elección en la lista (para n > 1) */
        index: number;
    }>;
    /** Estadísticas de uso de tokens */
    usage: {
        /** Tokens utilizados en el prompt (entrada) */
        prompt_tokens: number;
        /** Tokens generados en la completación (salida) */
        completion_tokens: number;
        /** Total de tokens consumidos (prompt + completion) */
        total_tokens: number;
        /**
         * Tokens recuperados del caché (solo si hubo cache hit)
         * @description DeepSeek cobra 0.1 yuanes por millón de tokens en caché
         */
        prompt_cache_hit_tokens?: number;
        /**
         * Tokens que no estaban en caché (cache miss)
         * @description DeepSeek cobra 1 yuan por millón de tokens normales
         */
        prompt_cache_miss_tokens?: number;
    };
}
/**
 * Chunk individual de una respuesta en streaming
 *
 * @description
 * Cada chunk contiene una pequeña porción de la respuesta completa.
 * Los chunks se reciben en orden secuencial vía Server-Sent Events (SSE).
 */
export interface DeepSeekStreamChunk {
    /** ID de la completación (mismo ID para todos los chunks de una respuesta) */
    id: string;
    /** Datos delta del chunk */
    choices: Array<{
        /**
         * Contenido delta (solo el texto nuevo desde el último chunk)
         * @description Puede estar vacío en chunks de inicio/fin
         */
        delta?: {
            /** Texto nuevo generado */
            content?: string;
            /** Rol del mensaje (solo en el primer chunk) */
            role?: string;
        };
        /**
         * Razón de finalización (solo en el último chunk)
         * @description null si aún hay más chunks por venir
         */
        finish_reason: string | null;
        /** Índice de esta elección */
        index: number;
    }>;
    /** Timestamp Unix en segundos cuando se generó este chunk */
    created: number;
    /** Nombre del modelo que generó esta respuesta */
    model: string;
}
/**
 * Crea una completación usando DeepSeek API
 *
 * @description
 * Función de alto nivel que encapsula el cliente DeepSeek.
 * Maneja automáticamente la creación del cliente y la solicitud.
 *
 * @param params - Parámetros de la completación
 * @param params.messages - Mensajes de la conversación
 * @param params.apiKey - API Key de DeepSeek
 * @param params.model - Modelo a usar (default: 'deepseek-chat')
 * @param params.temperature - Temperatura 0.0-2.0 (default: 0.7)
 * @param params.max_tokens - Máximo tokens a generar (default: 4096)
 *
 * @returns {Promise<DeepSeekCompletionResponse>} Respuesta completa del modelo
 *
 * @throws {Error} Si la API key es inválida o faltante
 * @throws {Error} Si DeepSeek API retorna error
 *
 * @example
 * ```typescript
 * import { createCompletion } from './actions';
 *
 * const response = await createCompletion({
 *   messages: [
 *     { role: 'system', content: 'Eres un asistente de código.' },
 *     { role: 'user', content: '¿Qué es TypeScript?' }
 *   ],
 *   apiKey: process.env.DEEPSEEK_API_KEY,
 *   temperature: 0.5
 * });
 *
 * console.log(response.choices[0].message.content);
 * console.log('Tokens usados:', response.usage.total_tokens);
 * ```
 */
export declare function createCompletion(params: DeepSeekCompletionRequest): Promise<DeepSeekCompletionResponse>;
/**
 * Crea un stream de completación en tiempo real
 *
 * @description
 * Función de alto nivel para streaming de respuestas.
 * Devuelve un generador asíncrono que produce chunks de texto
 * a medida que el modelo los genera.
 *
 * Ideal para interfaces de usuario que muestran texto carácter
 * por carácter mientras se genera.
 *
 * @param params - Parámetros de la completación
 * @param params.messages - Mensajes de la conversación
 * @param params.apiKey - API Key de DeepSeek
 * @param params.model - Modelo a usar (default: 'deepseek-chat')
 * @param params.temperature - Temperatura 0.0-2.0 (default: 0.7)
 * @param params.max_tokens - Máximo tokens a generar (default: 4096)
 *
 * @returns {AsyncGenerator<DeepSeekStreamChunk>} Generador de chunks SSE
 *
 * @throws {Error} Si la API key es inválida o faltante
 * @throws {Error} Si DeepSeek API retorna error
 *
 * @example
 * ```typescript
 * import { createCompletionStream } from './actions';
 *
 * async function streamResponse() {
 *   const stream = createCompletionStream({
 *     messages: [
 *       { role: 'user', content: 'Explica la teoría de la relatividad' }
 *     ],
 *     apiKey: process.env.DEEPSEEK_API_KEY,
 *     model: 'deepseek-chat'
 *   });
 *
 *   let fullResponse = '';
 *   for await (const chunk of stream) {
 *     const text = chunk.choices[0]?.delta?.content || '';
 *     fullResponse += text;
 *     // Mostrar en UI carácter por carácter
 *     updateUI(fullResponse);
 *   }
 *   console.log('Respuesta completa:', fullResponse);
 * }
 * ```
 */
export declare function createCompletionStream(params: DeepSeekCompletionRequest): AsyncGenerator<DeepSeekStreamChunk>;
//# sourceMappingURL=actions.d.ts.map
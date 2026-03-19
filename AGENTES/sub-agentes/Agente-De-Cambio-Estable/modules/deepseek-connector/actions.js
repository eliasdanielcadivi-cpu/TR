"use strict";
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.createCompletion = createCompletion;
exports.createCompletionStream = createCompletionStream;
const axios_1 = __importDefault(require("axios"));
// ============================================================================
// CLASE CLIENTE
// ============================================================================
/**
 * Cliente HTTP para la API de DeepSeek
 *
 * @description
 * Maneja la conexión de bajo nivel con los servidores de DeepSeek.
 * Configura automáticamente headers de autenticación y baseURL.
 *
 * @private
 * @internal No usar directamente - usar las funciones exportadas {@link createCompletion} y {@link createCompletionStream}
 */
class DeepSeekClient {
    /** Cliente Axios configurado para DeepSeek API */
    client;
    /** API Key para autenticación */
    apiKey;
    /** URL base de la API de DeepSeek */
    baseURL = 'https://api.deepseek.com';
    /**
     * Crea una nueva instancia del cliente DeepSeek
     *
     * @param apiKey - Clave de API obtenida de https://platform.deepseek.com/api_keys
     *
     * @example
     * ```typescript
     * const client = new DeepSeekClient('sk-tu-api-key');
     * ```
     */
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.client = axios_1.default.create({
            baseURL: this.baseURL,
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json',
            },
        });
    }
    /**
     * Solicita una completación síncrona a DeepSeek
     *
     * @param request - Parámetros de la solicitud
     * @returns Promesa con la respuesta completa del modelo
     *
     * @throws {Error} Si la API key es inválida (401)
     * @throws {Error} Si se excede la cuota de uso (429)
     * @throws {Error} Si hay error en el servidor de DeepSeek (5xx)
     *
     * @example
     * ```typescript
     * const response = await client.createCompletion({
     *   messages: [
     *     { role: 'system', content: 'Eres un asistente útil.' },
     *     { role: 'user', content: 'Hola, ¿cómo estás?' }
     *   ],
     *   temperature: 0.7,
     *   apiKey: 'sk-...'
     * });
     *
     * console.log(response.choices[0].message.content);
     * ```
     *
     * @see {@link https://api-docs.deepseek.com/api/create-chat-completion/} API Reference
     */
    async createCompletion(request) {
        const payload = {
            model: request.model || 'deepseek-chat',
            messages: request.messages,
            temperature: request.temperature || 0.7,
            stream: false,
            max_tokens: request.max_tokens || 4096,
            response_format: request.response_format,
        };
        const response = await this.client.post('/chat/completions', payload);
        return response.data;
    }
    /**
     * Crea un stream de completación en tiempo real
     *
     * @param request - Parámetros de la solicitud (stream forzado a true)
     * @returns Generador asíncrono que yield chunks de respuesta
     *
     * @description
     * Utiliza Server-Sent Events (SSE) para recibir la respuesta
     * carácter por carácter o en pequeños grupos de texto.
     *
     * El formato SSE usa líneas que comienzan con `data: ` seguidas
     * de JSON. La transmisión termina cuando se recibe `data: [DONE]`.
     *
     * @yields {DeepSeekStreamChunk} Cada chunk de la respuesta
     *
     * @example
     * ```typescript
     * const stream = client.createCompletionStream({
     *   messages: [{ role: 'user', content: 'Escribe un poema' }],
     *   apiKey: 'sk-...'
     * });
     *
     * for await (const chunk of stream) {
     *   const text = chunk.choices[0]?.delta?.content || '';
     *   process.stdout.write(text);
     * }
     * ```
     *
     * @see {@link https://api-docs.deepseek.com/guides/streaming/} Streaming Guide
     */
    async *createCompletionStream(request) {
        const payload = {
            model: request.model || 'deepseek-chat',
            messages: request.messages,
            temperature: request.temperature || 0.7,
            stream: true,
            max_tokens: request.max_tokens || 4096,
            response_format: request.response_format,
        };
        const response = await this.client.post('/chat/completions', payload, {
            responseType: 'stream',
            headers: {
                'Accept': 'text/event-stream',
            },
        });
        const stream = response.data;
        const decoder = new TextDecoder();
        let buffer = '';
        for await (const chunk of stream) {
            buffer += decoder.decode(chunk, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.slice(6);
                    if (data === '[DONE]')
                        return;
                    try {
                        const parsed = JSON.parse(data);
                        yield parsed;
                    }
                    catch (error) {
                        console.error('Error parsing SSE chunk:', error);
                    }
                }
            }
        }
    }
}
// ============================================================================
// FUNCIONES EXPORTADAS (API PÚBLICA DEL MÓDULO)
// ============================================================================
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
async function createCompletion(params) {
    const client = new DeepSeekClient(params.apiKey);
    return client.createCompletion(params);
}
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
async function* createCompletionStream(params) {
    const client = new DeepSeekClient(params.apiKey);
    yield* client.createCompletionStream(params);
}
//# sourceMappingURL=actions.js.map
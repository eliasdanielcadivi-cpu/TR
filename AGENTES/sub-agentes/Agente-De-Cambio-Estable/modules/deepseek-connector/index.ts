/**
 * DeepSeek Connector - Módulo para conexión con DeepSeek API
 * 
 * @module @agentedecambio2/deepseek-connector
 * @version 0.1.0
 */

export { createCompletion, createCompletionStream } from './actions';
export type {
  MessageRole,
  DeepSeekMessage,
  DeepSeekCompletionRequest,
  DeepSeekCompletionResponse,
  DeepSeekStreamChunk,
} from './actions';

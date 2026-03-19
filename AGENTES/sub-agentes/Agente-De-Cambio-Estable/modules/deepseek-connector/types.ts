/**
 * Tipos TypeScript para DeepSeek Connector
 * 
 * @module @agentedecambio2/deepseek-connector/types
 * @version 0.1.0
 * 
 * @description
 * Re-exporta todos los tipos desde actions.ts para conveniencia.
 * Los tipos están definidos en el mismo archivo que las funciones
 * para mantener la cohesión del módulo.
 */

// Re-exportar todos los tipos desde actions.ts
export type {
  MessageRole,
  DeepSeekMessage,
  DeepSeekCompletionRequest,
  DeepSeekCompletionResponse,
  DeepSeekStreamChunk,
} from './actions';

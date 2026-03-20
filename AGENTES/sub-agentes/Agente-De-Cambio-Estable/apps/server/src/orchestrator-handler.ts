/**
 * Orchestrator Handler - Maneja decisiones de cambio de modo
 * 
 * @description
 * Este módulo integra el cognitive-need-detector y mode-transition-engine
 * para decidir automáticamente cuándo cambiar entre chat y cuestionario.
 * 
 * @module apps/server/orchestrator-handler
 */

import type { Socket } from 'socket.io';
import type { ServerToClientEvents, ClientToServerEvents } from '@modules/shared-types';
import { analyzeCognitiveNeed, detectEmotionalState } from '@modules/cognitive-need-detector';
import { generateTransitionPrompt, createBridgeMessage } from '@modules/mode-transition-engine';
import type { SessionContext, InteractionMode } from '@modules/cognitive-need-detector';

/**
 * OrchestratorHandler - Maneja decisiones cognitivas en tiempo real
 */
export class OrchestratorHandler {
  private socket: Socket<ClientToServerEvents, ServerToClientEvents>;
  private sessionId: string;

  constructor(
    socket: Socket<ClientToServerEvents, ServerToClientEvents>,
    sessionId: string
  ) {
    this.socket = socket;
    this.sessionId = sessionId;
  }

  /**
   * analyzeAndDecide - Analiza mensaje y decide si cambia el modo
   * 
   * @param content - Mensaje del usuario
   * @param currentMode - Modo actual
   * @param messageHistory - Historial de mensajes
   * @returns Decisión de modo con transición si aplica
   */
  public async analyzeAndDecide(
    content: string,
    currentMode: InteractionMode,
    messageHistory: Array<{ role: string; content: string }>
  ): Promise<ModeDecisionResult> {
    // 1. Detectar estado emocional
    const emotionalState = detectEmotionalState(content);

    // 2. Construir contexto para el detector
    const context: SessionContext = {
      sessionId: this.sessionId,
      currentMode,
      lastMessage: content,
      messageHistory: messageHistory.map(m => ({
        role: m.role as 'user' | 'assistant',
        content: m.content,
        timestamp: new Date()
      })),
      objectiveStatus: this.deduceObjectiveStatus(messageHistory),
      missingDataFields: [],
      userEmotionalState: emotionalState.state,
      consecutiveChatMessages: this.countConsecutiveChatMessages(messageHistory)
    };

    // 3. Analizar necesidad cognitiva
    const decision = analyzeCognitiveNeed(context);

    // 4. Si hay cambio de modo, generar transición
    if (decision.mode !== currentMode) {
      const transition = generateTransitionPrompt(
        currentMode,
        decision.mode,
        decision.reason,
        context
      );

      const bridgeMessage = createBridgeMessage(transition, context);

      // 5. Emitir evento de cambio de modo al frontend
      this.socket.emit('mode:switch', {
        from: currentMode,
        to: decision.mode,
        reason: decision.reason,
        message: bridgeMessage,
        estimatedTime: decision.estimatedTime
      });

      console.log(`[ORCHESTRATOR] Mode switch: ${currentMode} → ${decision.mode} (${decision.reason})`);

      return {
        modeChanged: true,
        newMode: decision.mode,
        transitionMessage: bridgeMessage,
        emotionalState: emotionalState.state
      };
    }

    // No hay cambio de modo
    return {
      modeChanged: false,
      newMode: currentMode,
      transitionMessage: null,
      emotionalState: emotionalState.state
    };
  }

  /**
   * deduceObjectiveStatus - Deduce estado del objetivo del historial
   * 
   * @param history - Historial de mensajes
   * @returns Estado del objetivo (undefined/declared/in_progress/etc)
   */
  private deduceObjectiveStatus(
    history: Array<{ role: string; content: string }>
  ): 'undefined' | 'declared_but_unstructured' | 'emt_defined' | 'in_progress' | 'completed' {
    // Si hay menos de 3 mensajes, asumimos que no hay objetivo definido
    if (history.length < 3) {
      return 'undefined';
    }

    // Buscar palabras clave de objetivo
    const lastUserMessage = history.filter(m => m.role === 'user').pop();
    if (!lastUserMessage) {
      return 'undefined';
    }

    const content = lastUserMessage.content.toLowerCase();

    // Si menciona evidencia/métrica/tiempo, está definido
    if (content.includes('evidencia') || content.includes('métrica') || content.includes('para cuándo')) {
      return 'emt_defined';
    }

    // Si menciona objetivo pero sin estructura
    if (content.includes('quiero') || content.includes('objetivo') || content.includes('meta')) {
      return 'declared_but_unstructured';
    }

    return 'undefined';
  }

  /**
   * countConsecutiveChatMessages - Cuenta mensajes consecutivos de chat
   * 
   * @param history - Historial de mensajes
   * @returns Cantidad de mensajes consecutivos
   */
  private countConsecutiveChatMessages(
    history: Array<{ role: string; content: string }>
  ): number {
    let count = 0;
    
    // Contar hacia atrás desde el último mensaje
    for (let i = history.length - 1; i >= 0; i--) {
      if (history[i].role === 'user') {
        count++;
      } else {
        break;
      }
    }
    
    return count;
  }
}

/**
 * Resultado de la decisión de modo
 */
export interface ModeDecisionResult {
  modeChanged: boolean;
  newMode: InteractionMode;
  transitionMessage: string | null;
  emotionalState: string;
}

/**
 * createOrchestratorHandler - Factory para crear handler
 * 
 * @param socket - Socket.IO socket
 * @param sessionId - ID de sesión
 * @returns Nueva instancia de OrchestratorHandler
 */
export function createOrchestratorHandler(
  socket: Socket<ClientToServerEvents, ServerToClientEvents>,
  sessionId: string
): OrchestratorHandler {
  return new OrchestratorHandler(socket, sessionId);
}

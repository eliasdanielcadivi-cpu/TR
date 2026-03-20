/**
 * Cognitive Server - Punto de entrada principal del servidor
 * 
 * @description
 * Este archivo orquesta la inicialización del servidor y maneja
 * las conexiones Socket.IO. La lógica de negocio está en los módulos.
 * 
 * @module apps/server/index
 */

import 'dotenv/config';
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';

// Imports desde módulos
import { createCompletionStream } from '@modules/deepseek-connector';
import {
  createSession,
  getSession,
  updateSession,
} from '@modules/session-manager';
import { buildSystemPrompt } from '@modules/prompt-engine';
import { calculate, compare } from '@modules/delta-calculator';
import { createOrchestratorHandler } from './orchestrator-handler';
import type {
  ServerToClientEvents,
  ClientToServerEvents,
  ChatMessage,
  DeltaMetrics,
  Question,
  PromptMutation,
} from '@modules/shared-types';

// ============================================================================
// CONFIGURACIÓN DEL SERVIDOR
// ============================================================================

const app = express();
const httpServer = createServer(app);

// CORS configuration
const clientUrl = process.env.CLIENT_URL || 'http://localhost:3000';
app.use(cors({
  origin: clientUrl,
  credentials: true,
}));
app.use(express.json());

// Socket.IO server
const io = new Server<ClientToServerEvents, ServerToClientEvents>(httpServer, {
  cors: {
    origin: clientUrl,
    methods: ['GET', 'POST'],
  },
});

// DeepSeek API Key validation
const deepseekApiKey = process.env.DEEPSEEK_API_KEY;
if (!deepseekApiKey) {
  console.error('ERROR: DEEPSEEK_API_KEY not found in environment variables');
  process.exit(1);
}

// ============================================================================
// SOCKET.IO CONNECTION HANDLER
// ============================================================================

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  let currentSessionId: string;

  /**
   * Inicializa o recupera una sesión
   */
  socket.on('session:init', (sessionId) => {
    let session = sessionId ? getSession(sessionId) : undefined;
    if (!session) {
      session = createSession(sessionId);
    }
    currentSessionId = session.id;
    console.log('Session initialized:', currentSessionId);
  });

  /**
   * Maneja el envío de mensajes del usuario
   */
  socket.on('message:send', async (content, mode, context) => {
    if (!currentSessionId) {
      socket.emit('error', 'Session not initialized');
      return;
    }

    const session = getSession(currentSessionId);
    if (!session) {
      socket.emit('error', 'Session not found');
      return;
    }

    // ========================================
    // ORCHESTRATOR: Analizar necesidad cognitiva
    // ========================================
    const orchestrator = createOrchestratorHandler(socket, currentSessionId);
    
    const messageHistory = session.messages.map(m => ({
      role: m.role,
      content: m.content
    }));
    
    const decision = await orchestrator.analyzeAndDecide(
      content,
      mode as 'chat' | 'questionnaire' | 'mixed',
      messageHistory
    );
    
    // Si hubo cambio de modo, actualizar contexto
    const effectiveMode = decision.newMode;
    
    // ========================================
    // FIN ORCHESTRATOR
    // ========================================

    // Agregar mensaje del usuario
    const userMessage: ChatMessage = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
      metadata: {
        mode: effectiveMode,
        reasoning: context.isReasoning,
      },
    };
    session.messages.push(userMessage);

    // Construir system prompt con contexto
    const systemPrompt = buildSystemPrompt({
      basePrompt: session.systemPrompt,
      objectives: session.objectives,
      mode: effectiveMode,
    });

    // Preparar mensajes para DeepSeek (últimos 10 para contexto)
    const messages = [
      { role: 'system' as const, content: systemPrompt },
      ...session.messages.slice(-10).map(msg => ({
        role: msg.role,
        content: msg.content,
      })),
    ];

    // Stream de respuesta desde DeepSeek
    try {
      const stream = createCompletionStream({
        messages,
        temperature: context.isReasoning ? 0.7 : 0.5,
        stream: true,
        apiKey: deepseekApiKey,
      });

      let fullResponse = '';
      for await (const chunk of stream) {
        const text = chunk.choices[0]?.delta?.content || '';
        if (text) {
          fullResponse += text;
          socket.emit('message:stream', text);
        }
      }

      // Agregar mensaje del asistente
      const assistantMessage: ChatMessage = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: fullResponse,
        timestamp: new Date(),
        metadata: {
          mode: effectiveMode,
          reasoning: context.isReasoning,
        },
      };
      session.messages.push(assistantMessage);
      updateSession(currentSessionId, { messages: session.messages });

      // Emitir mensaje completo
      socket.emit('message:complete', assistantMessage);

      // Calcular delta del prompt
      const deltaScore = calculate(session.systemPrompt, fullResponse);
      const thresholdValue = parseFloat(process.env.PROMPT_DELTA_THRESHOLD || '0.3');

      const deltaMetrics: DeltaMetrics = {
        currentScore: deltaScore,
        threshold: thresholdValue,
        requiresApproval: deltaScore > thresholdValue,
        changes: {
          additions: 0, // Simplificado
          deletions: 0,
          semanticShift: deltaScore,
        },
      };
      socket.emit('delta:update', deltaMetrics);

    } catch (error) {
      console.error('DeepSeek API error:', error);
      socket.emit('error', 'Failed to get response from AI');
    }
  });

  /**
   * Actualiza el system prompt manualmente
   */
  socket.on('prompt:update', (content) => {
    if (!currentSessionId) return;

    const session = getSession(currentSessionId);
    if (!session) return;

    const oldPrompt = session.systemPrompt;
    session.systemPrompt = content;
    updateSession(currentSessionId, { systemPrompt: content });

    const comparison = compare(oldPrompt, content);
    
    const mutation: PromptMutation = {
      id: `mut_${Date.now()}`,
      timestamp: new Date(),
      change: `Prompt updated (${content.length - oldPrompt.length} chars)`,
      reason: 'Manual update by user',
      deltaImpact: comparison.deltaScore,
      approved: !comparison.requiresApproval,
    };
    socket.emit('prompt:mutation', mutation);
  });

  /**
   * Maneja selección de opciones en cuestionario
   */
  socket.on('option:select', (questionId, optionId, comment) => {
    // Lógica de cuestionario - por ahora solo acknowledge
    console.log('Option selected:', { questionId, optionId, comment });
    
    const nextQuestion: Question = {
      id: `q_${Date.now()}`,
      type: 'single_choice',
      question: '¿Cuál es el siguiente paso que prefieres?',
      options: [
        { id: '1', label: 'Profundizar en este tema', value: 'deepen' },
        { id: '2', label: 'Cambiar a otro aspecto', value: 'switch' },
        { id: '3', label: 'Resumir lo aprendido', value: 'summarize' },
      ],
    };
    socket.emit('question:next', nextQuestion);
  });

  /**
   * Cambia el modo de interacción
   */
  socket.on('mode:set', (mode) => {
    socket.emit('mode:switch', mode);
  });

  /**
   * Maneja desconexión del cliente
   */
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// ============================================================================
// ENDPOINTS REST (COMPATIBILIDAD)
// ============================================================================

/**
 * Endpoint de compatibilidad con frontend existente
 */
app.post('/api/interact', async (req, res) => {
  const { message, sessionId, mode } = req.body;

  let session = sessionId ? getSession(sessionId) : null;
  if (!session) {
    session = createSession(sessionId);
  }

  try {
    // Nota: Este endpoint usa createCompletionStream pero para REST
    // se debería usar createCompletion (síncrono)
    // Se mantiene por compatibilidad pero se recomienda migrar a WebSocket
    
    res.json({
      response: 'WebSocket recommended',
      sessionId: session.id,
      note: 'This endpoint is for compatibility. Use WebSocket for full functionality.',
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    modules: {
      deepseek: 'connected',
      session: 'active',
      prompt: 'ready',
    }
  });
});

// ============================================================================
// INICIO DEL SERVIDOR
// ============================================================================

const PORT = process.env.PORT || 3001;
httpServer.listen(PORT, () => {
  console.log(`Cognitive server running on port ${PORT}`);
  console.log(`WebSocket server ready`);
  console.log(`Client URL: ${clientUrl}`);
  console.log(`Modules loaded: deepseek-connector, session-manager, prompt-engine, delta-calculator, shared-types`);
});

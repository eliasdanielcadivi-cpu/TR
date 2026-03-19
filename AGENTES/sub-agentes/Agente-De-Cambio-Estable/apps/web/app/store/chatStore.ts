import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type ChatMode = 'chat' | 'questionnaire';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    reasoning?: boolean;
    mode?: ChatMode;
    deltaScore?: number;
  };
}

export interface PromptMutation {
  id: string;
  timestamp: Date;
  change: string;
  reason: string;
  deltaImpact: number;
  approved: boolean;
}

export interface Question {
  id: string;
  type: 'single_choice' | 'multiple_choice' | 'yes_no' | 'open';
  question: string;
  options?: Array<{
    id: string;
    label: string;
    value: string;
  }>;
}

export interface DeltaMetrics {
  currentScore: number;
  threshold: number;
  requiresApproval: boolean;
  changes: {
    additions: number;
    deletions: number;
    semanticShift: number;
  };
}

interface ChatStore {
  // Session state
  sessionId: string | null;
  setSessionId: (id: string) => void;

  // Chat state
  messages: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;

  // Mode state
  mode: ChatMode;
  setMode: (mode: ChatMode) => void;

  // Prompt state
  systemPrompt: string;
  setSystemPrompt: (prompt: string) => void;
  promptMutations: PromptMutation[];
  addPromptMutation: (mutation: PromptMutation) => void;

  // Reasoning state
  isReasoning: boolean;
  toggleReasoning: () => void;
  setIsReasoning: (value: boolean) => void;

  // Questionnaire state
  currentQuestion: Question | null;
  setCurrentQuestion: (question: Question | null) => void;

  // Delta metrics
  deltaMetrics: DeltaMetrics | null;
  setDeltaMetrics: (metrics: DeltaMetrics | null) => void;

  // Objectives
  objectives: string[];
  addObjective: (objective: string) => void;
  removeObjective: (index: number) => void;

  // UI state
  isConnected: boolean;
  setIsConnected: (connected: boolean) => void;
  isStreaming: boolean;
  setIsStreaming: (streaming: boolean) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      // Session
      sessionId: null,
      setSessionId: (id) => set({ sessionId: id }),

      // Messages
      messages: [],
      addMessage: (message) => set((state) => ({
        messages: [...state.messages, message]
      })),
      clearMessages: () => set({ messages: [] }),

      // Mode
      mode: 'chat',
      setMode: (mode) => set({ mode }),

      // Prompt
      systemPrompt: `Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente.`,
      setSystemPrompt: (prompt) => set({ systemPrompt: prompt }),
      promptMutations: [],
      addPromptMutation: (mutation) => set((state) => ({
        promptMutations: [...state.promptMutations, mutation],
      })),

      // Reasoning
      isReasoning: false,
      toggleReasoning: () => set((state) => ({ isReasoning: !state.isReasoning })),
      setIsReasoning: (value) => set({ isReasoning: value }),

      // Questionnaire
      currentQuestion: null,
      setCurrentQuestion: (question) => set({ currentQuestion: question }),

      // Delta metrics
      deltaMetrics: null,
      setDeltaMetrics: (metrics) => set({ deltaMetrics: metrics }),

      // Objectives
      objectives: [],
      addObjective: (objective) => set((state) => ({
        objectives: [...state.objectives, objective],
      })),
      removeObjective: (index) => set((state) => ({
        objectives: state.objectives.filter((_, i) => i !== index),
      })),

      // UI state
      isConnected: false,
      setIsConnected: (connected) => set({ isConnected: connected }),
      isStreaming: false,
      setIsStreaming: (streaming) => set({ isStreaming: streaming }),
    }),
    {
      name: 'chat-storage',
      partialize: (state) => ({
        sessionId: state.sessionId,
        messages: state.messages,
        systemPrompt: state.systemPrompt,
        objectives: state.objectives,
      }),
    }
  )
);
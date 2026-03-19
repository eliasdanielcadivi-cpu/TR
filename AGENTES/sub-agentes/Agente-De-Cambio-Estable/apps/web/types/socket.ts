export interface ServerToClientEvents {
  'message:stream': (chunk: string) => void;
  'message:complete': (message: ChatMessage) => void;
  'prompt:mutation': (mutation: PromptMutation) => void;
  'question:next': (question: Question) => void;
  'mode:switch': (mode: 'chat' | 'questionnaire') => void;
  'delta:update': (delta: DeltaMetrics) => void;
  'error': (error: string) => void;
}

export interface ClientToServerEvents {
  'message:send': (content: string, mode: 'chat' | 'questionnaire', context: MessageContext) => void;
  'prompt:update': (content: string) => void;
  'option:select': (questionId: string, optionId: string, comment?: string) => void;
  'mode:set': (mode: 'chat' | 'questionnaire') => void;
  'reasoning:toggle': (enabled: boolean) => void;
  'session:init': (sessionId?: string) => void;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    reasoning?: boolean;
    mode?: 'chat' | 'questionnaire';
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

export interface MessageContext {
  isReasoning: boolean;
  sessionId: string;
  objectives?: string[];
}
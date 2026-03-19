'use client';

import { useChatStore } from '@/app/store/chatStore';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { Questionnaire } from './Questionnaire';
import { motion } from 'framer-motion';

export function ChatContainer() {
  const { mode, messages, isStreaming } = useChatStore();

  return (
    <div className="flex flex-col h-[600px] glass-panel rounded-2xl p-4">
      {/* Chat header */}
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-white/10">
        <h2 className="text-xl font-bold text-white">
          {mode === 'chat' ? 'Conversación Cognitiva' : 'Cuestionario Guiado'}
        </h2>
        <div className="text-sm text-white/50">
          {messages.length} mensajes
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-2 space-y-4">
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center h-full text-white/40"
          >
            <div className="text-4xl mb-4">🧠</div>
            <p className="text-lg mb-2">Inicia una conversación</p>
            <p className="text-sm">Escribe un mensaje o selecciona una opción del cuestionario</p>
          </motion.div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}

        {/* Typing indicator */}
        {isStreaming && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 p-4 glass-panel rounded-2xl"
          >
            <div className="typing-indicator">
              <div className="typing-dot" />
              <div className="typing-dot" />
              <div className="typing-dot" />
            </div>
            <span className="text-white/50 text-sm">El sistema está escribiendo...</span>
          </motion.div>
        )}
      </div>

      {/* Input area */}
      <div className="mt-4 pt-4 border-t border-white/10">
        {mode === 'questionnaire' ? (
          <Questionnaire />
        ) : (
          <ChatInput />
        )}
      </div>
    </div>
  );
}
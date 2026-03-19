'use client';

import { useChatStore } from '@/app/store/chatStore';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { QuestionContainer } from './QuestionContainer';
import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useRef } from 'react';

export function ChatContainer() {
  const { mode, messages, isStreaming } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll al final cuando hay nuevos mensajes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-[700px] glass-panel rounded-2xl p-4 overflow-hidden">
      {/* Chat header */}
      <div className="flex-shrink-0 flex items-center justify-between mb-4 pb-3 border-b border-white/10">
        <h2 className="text-xl font-bold text-white">
          {mode === 'chat' ? 'Conversación Cognitiva' : 'Cuestionario Guiado'}
        </h2>
        <div className="text-sm text-white/50">
          {messages.length} mensajes
        </div>
      </div>

      {/* Messages area - Scrollable */}
      <div className="flex-1 overflow-y-auto min-h-0 p-2 space-y-4 pr-2 custom-scrollbar">
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
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </>
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

      {/* Input area - Fixed at bottom */}
      <div className="flex-shrink-0 mt-4 pt-4 border-t border-white/10">
        <AnimatePresence mode="wait">
          {mode === 'questionnaire' ? (
            <motion.div
              key="questionnaire"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <QuestionContainer />
            </motion.div>
          ) : (
            <motion.div
              key="chat"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <ChatInput />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
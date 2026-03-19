'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Mic } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';
import { useSocket } from '@/components/providers/SocketProvider';

export function ChatInput() {
  const [input, setInput] = useState('');
  const { mode, isReasoning, sessionId, addMessage } = useChatStore();

  const { sendMessage, isConnected } = useSocket();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to store
    const userMessage = {
      id: `msg_${Date.now()}`,
      role: 'user' as const,
      content: input,
      timestamp: new Date(),
      metadata: { mode, reasoning: isReasoning },
    };
    addMessage(userMessage);

    // Send via Socket.IO
    if (isConnected) {
      sendMessage(input);
    } else {
      console.error('Socket not connected');
      // Fallback: Add mock AI response
      setTimeout(() => {
        addMessage({
          id: `msg_${Date.now() + 1}`,
          role: 'assistant',
          content: '⚠️ Modo demo: El servidor no está conectado. Conecta el backend para respuestas reales.',
          timestamp: new Date(),
          metadata: { mode, reasoning: isReasoning },
        });
      }, 1000);
    }

    // Clear input
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <div className="flex-1 relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu mensaje aquí..."
          className="w-full glass-input rounded-2xl px-4 py-3 pr-12 text-white placeholder-white/30 resize-none focus:outline-none"
          rows={3}
        />
        <button
          type="button"
          className="absolute right-3 top-3 text-white/50 hover:text-white/80"
        >
          <Mic className="w-5 h-5" />
        </button>
      </div>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        type="submit"
        className="self-end px-6 py-3 rounded-2xl bg-gradient-to-r from-cognitive-500 to-cognitive-600 text-white font-medium flex items-center gap-2"
      >
        <Send className="w-4 h-4" />
        Enviar
      </motion.button>
    </form>
  );
}
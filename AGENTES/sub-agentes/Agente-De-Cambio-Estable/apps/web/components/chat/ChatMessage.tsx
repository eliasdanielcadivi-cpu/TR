'use client';

import { motion } from 'framer-motion';
import { User, Bot, Settings } from 'lucide-react';
import { ChatMessage as ChatMessageType } from '@/app/store/chatStore';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  const Icon = isUser ? User : isSystem ? Settings : Bot;
  const bgColor = isUser
    ? 'bg-cognitive-500/20 border-cognitive-500/30'
    : isSystem
    ? 'bg-purple-500/20 border-purple-500/30'
    : 'bg-white/5 border-white/10';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${bgColor}`}>
        <Icon className="w-4 h-4" />
      </div>

      {/* Message bubble */}
      <div className={`flex-1 ${isUser ? 'items-end' : ''}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-medium text-white/70">
            {message.role === 'user' ? 'Tú' : message.role === 'system' ? 'Sistema' : 'Cognitive Server'}
          </span>
          <span className="text-xs text-white/30">
            {format(new Date(message.timestamp), 'HH:mm', { locale: es })}
          </span>
        </div>
        <div
          className={`p-4 rounded-2xl border ${bgColor} ${isUser ? 'rounded-tr-none' : 'rounded-tl-none'}`}
        >
          <p className="text-white whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    </motion.div>
  );
}
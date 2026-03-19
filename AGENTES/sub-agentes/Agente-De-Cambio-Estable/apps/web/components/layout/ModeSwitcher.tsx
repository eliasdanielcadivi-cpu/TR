'use client';

import { motion } from 'framer-motion';
import { MessageSquare, ListTodo, ArrowRightLeft } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function ModeSwitcher() {
  const { mode, setMode } = useChatStore();

  return (
    <div className="flex items-center justify-center">
      <div className="relative flex items-center p-1 rounded-2xl bg-white/5 border border-white/10">
        {/* Background indicator */}
        <motion.div
          layoutId="mode-indicator"
          className="absolute inset-y-1 rounded-xl bg-cognitive-500/20 border border-cognitive-500/30"
          style={{
            width: 'calc(50% - 4px)',
            left: mode === 'chat' ? '4px' : 'calc(50%)',
          }}
          transition={{ type: "spring", stiffness: 400, damping: 30 }}
        />

        {/* Chat Mode Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setMode('chat')}
          className={`relative z-10 flex items-center gap-2 px-6 py-2.5 rounded-xl transition-colors ${
            mode === 'chat' ? 'text-cognitive-400' : 'text-white/50 hover:text-white/70'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span className="text-sm font-medium">Chat</span>
        </motion.button>

        {/* Questionnaire Mode Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setMode('questionnaire')}
          className={`relative z-10 flex items-center gap-2 px-6 py-2.5 rounded-xl transition-colors ${
            mode === 'questionnaire' ? 'text-cognitive-400' : 'text-white/50 hover:text-white/70'
          }`}
        >
          <ListTodo className="w-4 h-4" />
          <span className="text-sm font-medium">Cuestionario</span>
        </motion.button>
      </div>

      {/* Mode indicator badge */}
      <motion.div
        key={mode}
        initial={{ opacity: 0, x: 10 }}
        animate={{ opacity: 1, x: 0 }}
        className="ml-4 px-3 py-1 rounded-full bg-white/5 border border-white/10"
      >
        <span className="text-xs text-white/50 flex items-center gap-1">
          <ArrowRightLeft className="w-3 h-3" />
          {mode === 'chat' ? 'Conversación fluida' : 'Navegación guiada'}
        </span>
      </motion.div>
    </div>
  );
}
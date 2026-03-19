'use client';

import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function ReasoningToggle() {
  const { isReasoning, toggleReasoning } = useChatStore();

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleReasoning}
      className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all duration-300 ${
        isReasoning
          ? 'bg-reasoning-500/20 border border-reasoning-500/50 shadow-lg shadow-reasoning-500/20'
          : 'bg-white/5 border border-white/10 hover:bg-white/10'
      }`}
    >
      <motion.div
        animate={isReasoning ? { rotate: [0, 15, -15, 0] } : {}}
        transition={{ duration: 0.5, repeat: isReasoning ? Infinity : 0, repeatDelay: 2 }}
      >
        <Sparkles className={`w-4 h-4 ${isReasoning ? 'text-reasoning-500' : 'text-white/50'}`} />
      </motion.div>

      <span className={`text-sm font-medium ${isReasoning ? 'text-reasoning-500' : 'text-white/70'}`}>
        Razonamiento
      </span>

      <div className={`w-10 h-5 rounded-full relative transition-colors ${
        isReasoning ? 'bg-reasoning-500' : 'bg-white/20'
      }`}>
        <motion.div
          animate={{ x: isReasoning ? 20 : 2 }}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
          className="absolute top-1 w-3 h-3 rounded-full bg-white shadow-md"
        />
      </div>
    </motion.button>
  );
}
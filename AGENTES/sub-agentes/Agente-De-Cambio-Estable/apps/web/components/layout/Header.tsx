'use client';

import { motion } from 'framer-motion';
import { Brain, Zap, Settings, User } from 'lucide-react';
import { ReasoningToggle } from './ReasoningToggle';
import { useChatStore } from '@/app/store/chatStore';

export function Header() {
  const { isConnected } = useChatStore();

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="flex items-center justify-between px-6 py-4 border-b border-white/10 glass-panel m-4 mb-0 rounded-2xl"
    >
      {/* Logo */}
      <div className="flex items-center gap-3">
        <motion.div
          whileHover={{ rotate: 180 }}
          transition={{ duration: 0.5 }}
          className="w-10 h-10 rounded-xl bg-gradient-to-br from-cognitive-500 to-reasoning-500 flex items-center justify-center shadow-lg shadow-cognitive-500/25"
        >
          <Brain className="w-5 h-5 text-white" />
        </motion.div>
        <div>
          <h1 className="text-lg font-bold text-white tracking-tight">
            Cognitive Server
          </h1>
          <div className="flex items-center gap-2">
            <span className={`flex h-2 w-2 rounded-full ${isConnected ? 'bg-success' : 'bg-error'} animate-pulse`} />
            <span className="text-xs text-white/50">
              {isConnected ? 'Sistema Activo' : 'Desconectado'}
            </span>
          </div>
        </div>
      </div>

      {/* Center - Reasoning Toggle */}
      <ReasoningToggle />

      {/* Right Actions */}
      <div className="flex items-center gap-2">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 rounded-lg hover:bg-white/10 text-white/70 transition-colors"
        >
          <Zap className="w-5 h-5" />
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 rounded-lg hover:bg-white/10 text-white/70 transition-colors"
        >
          <Settings className="w-5 h-5" />
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/10 hover:bg-white/15 transition-colors"
        >
          <div className="w-6 h-6 rounded-full bg-gradient-to-br from-cognitive-400 to-cognitive-600 flex items-center justify-center">
            <User className="w-3 h-3 text-white" />
          </div>
          <span className="text-sm text-white/80">Usuario</span>
        </motion.button>
      </div>
    </motion.header>
  );
}
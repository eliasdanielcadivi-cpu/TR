'use client';

import { motion } from 'framer-motion';
import { Brain, Zap, Settings, User, RotateCcw } from 'lucide-react';
import { ReasoningToggle } from './ReasoningToggle';
import { useChatStore } from '@/app/store/chatStore';
import { useState } from 'react';

export function Header() {
  const { isConnected, clearMessages } = useChatStore();
  const [showResetConfirm, setShowResetConfirm] = useState(false);

  const handleReset = () => {
    clearMessages();
    setShowResetConfirm(false);
    // TODO: También resetear sesión en backend
    console.log('Sistema reseteado');
  };

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
        {/* Botón RESET con confirmación */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowResetConfirm(true)}
          className="p-2 rounded-lg hover:bg-error/20 text-error/70 hover:text-error transition-colors"
          title="Resetear conversación"
        >
          <RotateCcw className="w-5 h-5" />
        </motion.button>
        
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

      {/* Confirmación de RESET */}
      {showResetConfirm && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="glass-panel rounded-2xl p-6 max-w-md mx-4 border-2 border-error/50"
          >
            <h3 className="text-xl font-bold text-white mb-4">
              ⚠️ ¿Resetear todo el sistema?
            </h3>
            <p className="text-white/70 mb-6">
              Esta acción eliminará:
            </p>
            <ul className="text-white/60 text-sm space-y-2 mb-6">
              <li>• Todos los mensajes de la conversación</li>
              <li>• El estado actual del cuestionario</li>
              <li>• Las métricas de delta acumuladas</li>
            </ul>
            <div className="flex gap-3">
              <button
                onClick={() => setShowResetConfirm(false)}
                className="flex-1 px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleReset}
                className="flex-1 px-4 py-2 rounded-xl bg-error hover:bg-error/80 text-white transition-colors"
              >
                Sí, resetear todo
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </motion.header>
  );
}
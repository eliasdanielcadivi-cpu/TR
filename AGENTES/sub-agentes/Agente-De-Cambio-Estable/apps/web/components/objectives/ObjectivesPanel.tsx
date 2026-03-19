'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Target, Plus, Trash2, Check } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function ObjectivesPanel() {
  const { objectives, addObjective, removeObjective } = useChatStore();
  const [newObjective, setNewObjective] = useState('');
  const [editingIndex, setEditingIndex] = useState<number | null>(null);

  const handleAdd = () => {
    if (newObjective.trim()) {
      addObjective(newObjective.trim());
      setNewObjective('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAdd();
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Target className="w-5 h-5" />
          Objetivos Activos
        </h3>
        <span className="text-xs text-white/50">{objectives.length} objetivos</span>
      </div>

      {/* Add objective input */}
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newObjective}
          onChange={(e) => setNewObjective(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Añadir nuevo objetivo..."
          className="flex-1 glass-input rounded-xl px-3 py-2 text-white placeholder-white/30 focus:outline-none"
        />
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleAdd}
          className="px-3 py-2 rounded-xl bg-cognitive-500 text-white"
        >
          <Plus className="w-4 h-4" />
        </motion.button>
      </div>

      {/* Objectives list */}
      <AnimatePresence>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {objectives.length === 0 ? (
            <div className="text-center py-4 text-white/40">
              No hay objetivos definidos
            </div>
          ) : (
            objectives.map((objective, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="flex items-center gap-2 p-3 rounded-xl bg-white/5 border border-white/10"
              >
                <Check className="w-4 h-4 text-cognitive-400 flex-shrink-0" />
                <div className="flex-1 text-sm text-white">{objective}</div>
                <button
                  onClick={() => removeObjective(index)}
                  className="p-1 text-white/50 hover:text-error transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </motion.div>
            ))
          )}
        </div>
      </AnimatePresence>

      <div className="mt-4 pt-3 border-t border-white/10 text-xs text-white/50">
        <p>Los objetivos se inyectan en el prompt del sistema para guiar la conversación.</p>
      </div>
    </div>
  );
}
/**
 * Multi Choice Viewer - Capacidad para selección múltiple
 * 
 * @description
 * Capacidad autocontenida para preguntas con varias opciones válidas.
 * 
 * @module @agentedecambio2/viewer-multi-choice
 */

'use client';

import { motion } from 'framer-motion';

interface MultiChoiceViewerProps {
  question: {
    id: string;
    prompt: string;
    options?: Array<{ id: string; label: string; value: any }>;
  };
  value: string[] | null;
  onChange: (value: string[]) => void;
}

export function MultiChoiceViewer({ question, value, onChange }: MultiChoiceViewerProps) {
  if (!question.options) return null;

  const selectedIds = value || [];

  const toggleOption = (optionId: string) => {
    const newSelected = selectedIds.includes(optionId)
      ? selectedIds.filter((id) => id !== optionId)
      : [...selectedIds, optionId];
    onChange(newSelected);
  };

  return (
    <div className="space-y-2">
      {question.options.map((option) => (
        <motion.button
          key={option.id}
          type="button"
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.99 }}
          onClick={() => toggleOption(option.id)}
          className={`w-full text-left p-3 rounded-xl transition-all ${
            selectedIds.includes(option.id)
              ? 'bg-cognitive-500/30 border-2 border-cognitive-500 shadow-lg shadow-cognitive-500/20'
              : 'bg-white/5 border-2 border-transparent hover:bg-white/10 hover:border-white/20'
          }`}
        >
          <div className="flex items-center gap-3">
            <div
              className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                selectedIds.includes(option.id)
                  ? 'bg-cognitive-500 border-cognitive-500'
                  : 'border-white/30'
              }`}
            >
              {selectedIds.includes(option.id) && (
                <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              )}
            </div>
            <span className="text-white">{option.label}</span>
          </div>
        </motion.button>
      ))}
    </div>
  );
}

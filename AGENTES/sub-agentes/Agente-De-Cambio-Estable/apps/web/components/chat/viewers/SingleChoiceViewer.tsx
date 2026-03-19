/**
 * Single Choice Viewer - Capacidad para selección única
 * 
 * @description
 * Capacidad autocontenida para preguntas con una sola opción válida.
 * 
 * @module @agentedecambio2/viewer-single-choice
 */

'use client';

import { motion } from 'framer-motion';

interface SingleChoiceViewerProps {
  question: {
    id: string;
    prompt: string;
    options?: Array<{ id: string; label: string; value: any }>;
  };
  value: string | null;
  onChange: (value: string) => void;
}

export function SingleChoiceViewer({ question, value, onChange }: SingleChoiceViewerProps) {
  if (!question.options) return null;

  return (
    <div className="space-y-2">
      {question.options.map((option) => (
        <motion.button
          key={option.id}
          type="button"
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.99 }}
          onClick={() => onChange(option.id)}
          className={`w-full text-left p-3 rounded-xl transition-all ${
            value === option.id
              ? 'bg-cognitive-500/30 border-2 border-cognitive-500 shadow-lg shadow-cognitive-500/20'
              : 'bg-white/5 border-2 border-transparent hover:bg-white/10 hover:border-white/20'
          }`}
        >
          <div className="flex items-center gap-3">
            <div
              className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                value === option.id
                  ? 'border-cognitive-500'
                  : 'border-white/30'
              }`}
            >
              {value === option.id && (
                <div className="w-2.5 h-2.5 rounded-full bg-cognitive-500" />
              )}
            </div>
            <span className="text-white">{option.label}</span>
          </div>
        </motion.button>
      ))}
    </div>
  );
}

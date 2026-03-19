/**
 * TrueFalse Viewer - Capacidad para preguntas Verdadero/Falso
 * 
 * @description
 * Capacidad autocontenida para renderizar y manejar preguntas de validación lógica.
 * 
 * @module @agentedecambio2/viewer-truefalse
 */

'use client';

import { motion } from 'framer-motion';

interface TrueFalseViewerProps {
  question: {
    id: string;
    prompt: string;
    options?: Array<{ id: string; label: string; value: any }>;
  };
  value: boolean | null;
  onChange: (value: boolean) => void;
}

export function TrueFalseViewer({ question, value, onChange }: TrueFalseViewerProps) {
  const options = [
    { id: 'true', label: 'Verdadero', value: true },
    { id: 'false', label: 'Falso', value: false },
  ];

  return (
    <div className="space-y-3">
      {options.map((option) => (
        <motion.button
          key={option.id}
          type="button"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => onChange(option.value)}
          className={`w-full text-left p-4 rounded-xl transition-all ${
            value === option.value
              ? 'bg-reasoning-500/30 border-2 border-reasoning-500 shadow-lg shadow-reasoning-500/20'
              : 'bg-white/5 border-2 border-transparent hover:bg-white/10 hover:border-white/20'
          }`}
        >
          <div className="flex items-center gap-4">
            <div
              className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                value === option.value
                  ? 'bg-reasoning-500 border-reasoning-500'
                  : 'border-white/30'
              }`}
            >
              {value === option.value && (
                <div className="w-3 h-3 rounded-full bg-white" />
              )}
            </div>
            <span className="text-white text-lg">{option.label}</span>
          </div>
        </motion.button>
      ))}
    </div>
  );
}

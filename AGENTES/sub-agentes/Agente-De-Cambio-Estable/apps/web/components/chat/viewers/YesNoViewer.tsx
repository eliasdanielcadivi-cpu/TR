/**
 * YesNo Viewer - Capacidad para preguntas Sí/No
 * 
 * @description
 * Capacidad autocontenida para renderizar y manejar preguntas binarias.
 * Sigue el patrón Viewer/Action del paradigma de capacidades.
 * 
 * @module @agentedecambio2/viewer-yesno
 */

'use client';

import { motion } from 'framer-motion';

interface YesNoViewerProps {
  question: {
    id: string;
    prompt: string;
    options?: Array<{ id: string; label: string; value: any }>;
  };
  value: boolean | null;
  onChange: (value: boolean) => void;
}

export function YesNoViewer({ question, value, onChange }: YesNoViewerProps) {
  const options = [
    { id: 'yes', label: 'Sí', value: true },
    { id: 'no', label: 'No', value: false },
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
              ? 'bg-cognitive-500/30 border-2 border-cognitive-500 shadow-lg shadow-cognitive-500/20'
              : 'bg-white/5 border-2 border-transparent hover:bg-white/10 hover:border-white/20'
          }`}
        >
          <div className="flex items-center gap-4">
            <div
              className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                value === option.value
                  ? 'bg-cognitive-500 border-cognitive-500'
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

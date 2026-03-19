/**
 * Open Exploration Viewer - Capacidad para exploración abierta
 * 
 * @description
 * Capacidad autocontenida para preguntas sin estructura definida.
 * Permite al usuario escribir libremente sin validación estricta.
 * 
 * @module @agentedecambio2/viewer-open-exploration
 */

'use client';

import { useEffect, useState } from 'react';

interface OpenExplorationViewerProps {
  question: {
    id: string;
    prompt: string;
    placeholder?: string;
  };
  value: string | null;
  onChange: (value: string) => void;
}

export function OpenExplorationViewer({ question, value, onChange }: OpenExplorationViewerProps) {
  const [localValue, setLocalValue] = useState(value || '');

  useEffect(() => {
    onChange(localValue);
  }, [localValue]);

  return (
    <div className="space-y-2 w-full">
      <textarea
        value={localValue}
        onChange={(e) => setLocalValue(e.target.value)}
        placeholder={question.placeholder || 'Escribe libremente...'}
        rows={3}
        className="w-full glass-input rounded-xl px-4 py-3 text-white placeholder-white/30 resize-y focus:outline-none focus:ring-2 focus:ring-cognitive-500/50 responsive-textarea"
      />
      <p className="text-sm text-white/50">
        Escribe sin restricciones. No hay respuestas incorrectas.
      </p>
    </div>
  );
}

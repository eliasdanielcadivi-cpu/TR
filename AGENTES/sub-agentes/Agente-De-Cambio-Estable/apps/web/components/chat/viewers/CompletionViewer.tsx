/**
 * Completion Viewer - Capacidad para completación de texto breve
 * 
 * @description
 * Capacidad autocontenida para preguntas que requieren una palabra o frase corta.
 * 
 * @module @agentedecambio2/viewer-completion
 */

'use client';

import { useEffect, useState } from 'react';

interface CompletionViewerProps {
  question: {
    id: string;
    prompt: string;
    placeholder?: string;
  };
  value: string | null;
  onChange: (value: string) => void;
}

export function CompletionViewer({ question, value, onChange }: CompletionViewerProps) {
  const [localValue, setLocalValue] = useState(value || '');

  useEffect(() => {
    onChange(localValue);
  }, [localValue]);

  return (
    <div className="space-y-2">
      <input
        type="text"
        value={localValue}
        onChange={(e) => setLocalValue(e.target.value)}
        placeholder={question.placeholder || 'Escribe tu respuesta...'}
        className="w-full glass-input rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-cognitive-500/50"
        autoFocus
      />
      {localValue.trim() && (
        <p className="text-sm text-white/50">
          {localValue.trim().length} caracteres
        </p>
      )}
    </div>
  );
}

/**
 * Multiline Viewer - Capacidad para texto multilínea
 * 
 * @description
 * Capacidad autocontenida para preguntas que requieren explicación o matiz.
 * 
 * @module @agentedecambio2/viewer-multiline
 */

'use client';

import { useEffect, useState } from 'react';

interface MultilineViewerProps {
  question: {
    id: string;
    prompt: string;
    placeholder?: string;
    minLength?: number;
  };
  value: string | null;
  onChange: (value: string) => void;
}

export function MultilineViewer({ question, value, onChange }: MultilineViewerProps) {
  const [localValue, setLocalValue] = useState(value || '');
  const minLength = question.minLength || 20;

  useEffect(() => {
    onChange(localValue);
  }, [localValue]);

  return (
    <div className="space-y-2">
      <textarea
        value={localValue}
        onChange={(e) => setLocalValue(e.target.value)}
        placeholder={question.placeholder || 'Escribe tu respuesta...'}
        rows={4}
        className="w-full glass-input rounded-xl px-4 py-3 text-white placeholder-white/30 resize-y focus:outline-none focus:ring-2 focus:ring-cognitive-500/50"
      />
      <div className="flex justify-between text-sm text-white/50">
        <span>
          {localValue.trim().length} caracteres
          {localValue.trim().length < minLength && (
            <span className="text-yellow-500/70"> (mínimo {minLength})</span>
          )}
        </span>
        <span>{localValue.split(/\s+/).filter(Boolean).length} palabras</span>
      </div>
    </div>
  );
}

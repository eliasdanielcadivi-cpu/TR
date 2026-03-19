/**
 * Ranking Viewer - Capacidad para ranking/priorización
 * 
 * @description
 * Capacidad autocontenida para preguntas que requieren ordenar por preferencia.
 * Implementa drag-and-drop simple con botones de flecha.
 * 
 * @module @agentedecambio2/viewer-ranking
 */

'use client';

import { motion } from 'framer-motion';

interface RankingViewerProps {
  question: {
    id: string;
    prompt: string;
    options?: Array<{ id: string; label: string; value: any }>;
  };
  value: number[] | null; // Índices ordenados
  onChange: (value: number[]) => void;
}

export function RankingViewer({ question, value, onChange }: RankingViewerProps) {
  if (!question.options) return null;

  const order = value || question.options.map((_, i) => i);

  const moveUp = (index: number) => {
    if (index === 0) return;
    const newOrder = [...order];
    [newOrder[index - 1], newOrder[index]] = [newOrder[index], newOrder[index - 1]];
    onChange(newOrder);
  };

  const moveDown = (index: number) => {
    if (index === order.length - 1) return;
    const newOrder = [...order];
    [newOrder[index], newOrder[index + 1]] = [newOrder[index + 1], newOrder[index]];
    onChange(newOrder);
  };

  return (
    <div className="space-y-3 w-full max-w-full">
      {order.map((optionIndex, position) => {
        const option = question.options![optionIndex];
        return (
          <motion.div
            key={option.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3 bg-white/5 rounded-xl p-3 ranking-item w-full max-w-full"
          >
            {/* Posición */}
            <div className="w-8 h-8 rounded-full bg-cognitive-500/30 border border-cognitive-500/50 flex items-center justify-center text-white font-semibold flex-shrink-0">
              {position + 1}
            </div>

            {/* Label - con truncamiento si es muy largo */}
            <span className="flex-1 text-white min-w-0 truncate">{option.label}</span>

            {/* Controles de orden */}
            <div className="ranking-controls flex gap-1 flex-shrink-0">
              <button
                type="button"
                onClick={() => moveUp(position)}
                disabled={position === 0}
                className="p-1.5 rounded-lg hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed transition-colors w-8 h-8 flex items-center justify-center"
                title="Mover arriba"
              >
                <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                </svg>
              </button>
              <button
                type="button"
                onClick={() => moveDown(position)}
                disabled={position === order.length - 1}
                className="p-1.5 rounded-lg hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed transition-colors w-8 h-8 flex items-center justify-center"
                title="Mover abajo"
              >
                <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}

'use client';

import { motion } from 'framer-motion';
import { AlertTriangle, Check } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function DeltaMeter() {
  const { deltaMetrics } = useChatStore();

  const score = deltaMetrics?.currentScore || 0;
  const threshold = deltaMetrics?.threshold || 0.3;
  const requiresApproval = deltaMetrics?.requiresApproval || false;

  const percentage = Math.min(100, (score / threshold) * 100);

  return (
    <div className="glass-panel rounded-2xl p-4">
      <h3 className="text-lg font-semibold text-white mb-3">Métrica de Deriva</h3>

      <div className="space-y-4">
        {/* Visual meter */}
        <div className="relative h-6 bg-white/5 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 1, type: 'spring' }}
            className={`absolute h-full rounded-full ${
              requiresApproval
                ? 'bg-gradient-to-r from-warning to-error'
                : 'bg-gradient-to-r from-cognitive-400 to-cognitive-600'
            }`}
          />

          {/* Threshold line */}
          <div
            className="absolute top-0 bottom-0 w-0.5 bg-white/50"
            style={{ left: `${(threshold / threshold) * 100}%` }}
          />
        </div>

        {/* Labels */}
        <div className="flex justify-between text-sm">
          <span className="text-white/70">Baja</span>
          <span className="text-white/70">Umbral: {threshold}</span>
          <span className="text-white/70">Alta</span>
        </div>

        {/* Score display */}
        <div className="flex items-center justify-between">
          <div>
            <div className="text-2xl font-bold text-white">{score.toFixed(2)}</div>
            <div className="text-xs text-white/50">Score actual</div>
          </div>

          <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${
            requiresApproval
              ? 'bg-warning/20 text-warning'
              : 'bg-success/20 text-success'
          }`}>
            {requiresApproval ? (
              <>
                <AlertTriangle className="w-4 h-4" />
                <span className="text-sm font-medium">Requiere aprobación</span>
              </>
            ) : (
              <>
                <Check className="w-4 h-4" />
                <span className="text-sm font-medium">Dentro del rango</span>
              </>
            )}
          </div>
        </div>

        {/* Details */}
        {deltaMetrics && (
          <div className="grid grid-cols-3 gap-2 pt-3 border-t border-white/10">
            <div className="text-center p-2 bg-white/5 rounded-lg">
              <div className="text-xs text-white/50">Adiciones</div>
              <div className="text-white font-semibold">{deltaMetrics.changes.additions}</div>
            </div>
            <div className="text-center p-2 bg-white/5 rounded-lg">
              <div className="text-xs text-white/50">Eliminaciones</div>
              <div className="text-white font-semibold">{deltaMetrics.changes.deletions}</div>
            </div>
            <div className="text-center p-2 bg-white/5 rounded-lg">
              <div className="text-xs text-white/50">Shift Semántico</div>
              <div className="text-white font-semibold">
                {deltaMetrics.changes.semanticShift.toFixed(2)}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
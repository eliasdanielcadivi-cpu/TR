'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Edit2, Save, RefreshCw } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';
import { useSocket } from '@/components/providers/SocketProvider';

export function PromptEditor() {
  const { systemPrompt, setSystemPrompt } = useChatStore();
  const [editing, setEditing] = useState(false);
  const [draftPrompt, setDraftPrompt] = useState(systemPrompt);

  const { updatePrompt } = useSocket();

  const handleSave = () => {
    setSystemPrompt(draftPrompt);
    setEditing(false);
    // Emit prompt update via Socket.IO
    updatePrompt(draftPrompt);
  };

  const handleReset = () => {
    const defaultPrompt = `Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente.`;
    setDraftPrompt(defaultPrompt);
    setSystemPrompt(defaultPrompt);
  };

  return (
    <div className="glass-panel rounded-2xl p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Edit2 className="w-5 h-5" />
          Prompt del Sistema
        </h3>
        <div className="flex gap-2">
          {editing ? (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setEditing(false)}
                className="px-3 py-1 rounded-lg bg-white/10 text-white/70 text-sm"
              >
                Cancelar
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSave}
                className="px-3 py-1 rounded-lg bg-cognitive-500 text-white text-sm flex items-center gap-1"
              >
                <Save className="w-3 h-3" />
                Guardar
              </motion.button>
            </>
          ) : (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setEditing(true)}
                className="px-3 py-1 rounded-lg bg-white/10 text-white/70 text-sm"
              >
                Editar
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleReset}
                className="px-3 py-1 rounded-lg bg-white/10 text-white/70 text-sm flex items-center gap-1"
              >
                <RefreshCw className="w-3 h-3" />
                Reset
              </motion.button>
            </>
          )}
        </div>
      </div>

      {editing ? (
        <textarea
          value={draftPrompt}
          onChange={(e) => setDraftPrompt(e.target.value)}
          className="w-full glass-input rounded-xl p-3 text-white font-mono text-sm h-64 resize-none focus:outline-none"
          spellCheck={false}
        />
      ) : (
        <div className="glass-input rounded-xl p-3 h-64 overflow-y-auto">
          <pre className="text-white/80 font-mono text-sm whitespace-pre-wrap">
            {systemPrompt}
          </pre>
        </div>
      )}

      <div className="mt-3 text-xs text-white/50">
        {editing ? (
          <p>Edita el prompt del sistema. Los cambios afectarán el comportamiento del AI.</p>
        ) : (
          <p>Prompt actual del sistema. Haz clic en "Editar" para modificarlo.</p>
        )}
      </div>
    </div>
  );
}
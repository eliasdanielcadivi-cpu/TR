'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function Questionnaire() {
  const [comment, setComment] = useState('');
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
  const { currentQuestion, addMessage } = useChatStore();

  const handleOptionSelect = (optionId: string) => {
    if (!currentQuestion) return;

    if (currentQuestion.type === 'multiple_choice') {
      setSelectedOptions((prev) =>
        prev.includes(optionId)
          ? prev.filter((id) => id !== optionId)
          : [...prev, optionId]
      );
    } else {
      setSelectedOptions([optionId]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQuestion) return;

    // Create message from selection
    const selectedText = currentQuestion.options
      ?.filter((opt) => selectedOptions.includes(opt.id))
      .map((opt) => opt.label)
      .join(', ') || 'No selection';

    const messageContent = `Pregunta: ${currentQuestion.question}\nSelección: ${selectedText}\nComentario: ${comment}`;

    addMessage({
      id: `msg_${Date.now()}`,
      role: 'user',
      content: messageContent,
      timestamp: new Date(),
    });

    // TODO: Send via Socket.IO

    // Reset
    setSelectedOptions([]);
    setComment('');
  };

  if (!currentQuestion) {
    return (
      <div className="text-center p-8 text-white/50">
        Esperando primera pregunta del sistema...
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="glass-panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white mb-4">
          {currentQuestion.question}
        </h3>

        {currentQuestion.options && (
          <div className="space-y-2">
            {currentQuestion.options.map((option) => (
              <motion.button
                key={option.id}
                type="button"
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                onClick={() => handleOptionSelect(option.id)}
                className={`w-full text-left p-3 rounded-xl transition-colors ${
                  selectedOptions.includes(option.id)
                    ? 'bg-cognitive-500/30 border border-cognitive-500/50'
                    : 'bg-white/5 hover:bg-white/10 border border-transparent'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-4 h-4 rounded-full border ${
                    currentQuestion.type === 'multiple_choice'
                      ? 'rounded'
                      : 'rounded-full'
                  } ${
                    selectedOptions.includes(option.id)
                      ? 'bg-cognitive-500 border-cognitive-500'
                      : 'border-white/30'
                  }`} />
                  <span className="text-white">{option.label}</span>
                </div>
              </motion.button>
            ))}
          </div>
        )}
      </div>

      <div className="flex gap-2">
        <div className="flex-1">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Comentario adicional (opcional)..."
            className="w-full glass-input rounded-2xl px-4 py-3 text-white placeholder-white/30 resize-none focus:outline-none"
            rows={2}
          />
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          type="submit"
          className="self-end px-6 py-3 rounded-2xl bg-gradient-to-r from-cognitive-500 to-cognitive-600 text-white font-medium flex items-center gap-2"
        >
          <Send className="w-4 h-4" />
          Continuar
        </motion.button>
      </div>
    </form>
  );
}
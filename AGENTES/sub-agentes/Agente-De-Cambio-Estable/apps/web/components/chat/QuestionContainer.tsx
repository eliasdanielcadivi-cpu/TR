/**
 * Question Container - Contenedor unificado para capacidades de preguntas
 * 
 * @description
 * Este componente actúa como superficie de montaje para las capacidades
 * de tipos de preguntas. Cada capacidad es independiente y se monta
 * según el tipo de pregunta recibido.
 * 
 * @module @agentedecambio2/question-container
 */

'use client';

import { useState, useEffect } from 'react';
import { useChatStore } from '@/app/store/chatStore';
import { motion, AnimatePresence } from 'framer-motion';
import { Send } from 'lucide-react';

// Importar capacidades (Viewers) independientes
import { YesNoViewer } from './viewers/YesNoViewer';
import { TrueFalseViewer } from './viewers/TrueFalseViewer';
import { SingleChoiceViewer } from './viewers/SingleChoiceViewer';
import { MultiChoiceViewer } from './viewers/MultiChoiceViewer';
import { CompletionViewer } from './viewers/CompletionViewer';
import { MultilineViewer } from './viewers/MultilineViewer';
import { RankingViewer } from './viewers/RankingViewer';
import { OpenExplorationViewer } from './viewers/OpenExplorationViewer';

/**
 * Mapeo de capacidades por tipo de pregunta
 * Cada capacidad es independiente y autocontenida
 */
const VIEWERS: Record<string, React.ComponentType<any>> = {
  yesno: YesNoViewer,
  truefalse: TrueFalseViewer,
  single_choice: SingleChoiceViewer,
  multi_choice: MultiChoiceViewer,
  completion: CompletionViewer,
  multiline: MultilineViewer,
  ranking: RankingViewer,
  open_exploration: OpenExplorationViewer,
};

export function QuestionContainer() {
  const { currentQuestion, setCurrentQuestion, addMessage } = useChatStore();
  const [comment, setComment] = useState('');
  const [answer, setAnswer] = useState<any>(null);

  // Resetear respuesta cuando cambia la pregunta
  useEffect(() => {
    setAnswer(null);
    setComment('');
  }, [currentQuestion]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!currentQuestion || !answer) return;

    // Construir mensaje desde respuesta
    const messageContent = buildMessageFromAnswer(currentQuestion, answer, comment);

    addMessage({
      id: `msg_${Date.now()}`,
      role: 'user',
      content: messageContent,
      timestamp: new Date(),
      metadata: {
        mode: 'questionnaire',
        questionId: currentQuestion.id,
      },
    });

    // TODO: Emitir via Socket.IO (se hará en Hito 1 completo)
    // socket.emit('option:select', currentQuestion.id, answer, comment);

    // Resetear
    setComment('');
    setAnswer(null);
  };

  if (!currentQuestion) {
    return (
      <div className="text-center p-8 text-white/50">
        Esperando pregunta del sistema...
      </div>
    );
  }

  // Obtener el Viewer (capacidad) para este tipo de pregunta
  const ViewerComponent = VIEWERS[currentQuestion.type] || OpenExplorationViewer;

  return (
    <div className="space-y-4">
      {/* Panel de la pregunta - Container común */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="glass-panel rounded-2xl p-6"
      >
        {/* Título de la pregunta */}
        <h3 className="text-lg font-semibold text-white mb-4">
          {currentQuestion.prompt}
        </h3>

        {/* Renderizar la capacidad (Viewer) específica */}
        <ViewerComponent
          question={currentQuestion}
          value={answer}
          onChange={setAnswer}
        />
      </motion.div>

      {/* Comentario adicional (siempre presente) */}
      <div className="flex gap-2">
        <div className="flex-1">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Comentario adicional (opcional)..."
            className="w-full glass-input rounded-2xl px-4 py-3 text-white placeholder-white/30 resize-none focus:outline-none focus:ring-2 focus:ring-cognitive-500/50"
            rows={2}
          />
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => handleSubmit()}
          disabled={!answer}
          className="self-end px-6 py-3 rounded-2xl bg-gradient-to-r from-cognitive-500 to-cognitive-600 text-white font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send className="w-4 h-4" />
          Continuar
        </motion.button>
      </div>
    </div>
  );
}

/**
 * Construye mensaje desde respuesta
 */
function buildMessageFromAnswer(question: any, answer: any, comment: string): string {
  let answerText = '';

  switch (question.type) {
    case 'yesno':
    case 'truefalse':
      answerText = answer ? 'Sí' : 'No';
      break;
    case 'single_choice':
    case 'multi_choice':
      const selectedLabels = question.options
        ?.filter((opt: any) => 
          Array.isArray(answer) ? answer.includes(opt.id) : opt.id === answer
        )
        .map((opt: any) => opt.label)
        .join(', ');
      answerText = selectedLabels || 'Sin selección';
      break;
    case 'completion':
    case 'multiline':
    case 'open_exploration':
      answerText = typeof answer === 'string' ? answer : JSON.stringify(answer);
      break;
    case 'ranking':
      answerText = answer
        ?.map((idx: number) => question.options[idx]?.label)
        .join(' > ');
      break;
    default:
      answerText = JSON.stringify(answer);
  }

  let message = `Pregunta: ${question.prompt}\n`;
  message += `Respuesta: ${answerText}`;
  
  if (comment.trim()) {
    message += `\nComentario: ${comment}`;
  }

  return message;
}

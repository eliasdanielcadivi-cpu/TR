/**
 * Question Container - Contenedor unificado para capacidades de preguntas
 * 
 * @description
 * Este componente actúa como superficie de montaje para las capacidades
 * de tipos de preguntas. Cada capacidad es independiente y se monta
 * según el tipo de pregunta recibido.
 * 
 * MODO DEMO: Para probar visualmente, cambiar DEMO_MODE a true
 * y seleccionar un tipo de pregunta del menú.
 * 
 * @module @agentedecambio2/question-container
 */

'use client';

import { useState, useEffect } from 'react';
import { useChatStore } from '@/app/store/chatStore';
import { motion } from 'framer-motion';
import { Send, Bug } from 'lucide-react';

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
 * MODO DEMO: Cambiar a true para probar visualmente las capacidades
 * IMPORTANTE: false para producción - el cuestionario se activa por Socket.IO
 */
const DEMO_MODE = false;

/**
 * Mapeo de capacidades por tipo de pregunta
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

/**
 * Preguntas de ejemplo para cada tipo (DEMO MODE)
 */
const DEMO_QUESTIONS: Record<string, any> = {
  yesno: {
    id: 'demo_yesno',
    type: 'yesno',
    prompt: '¿Tienes un prototipo funcional?',
    options: [
      { id: 'yes', label: 'Sí', value: true },
      { id: 'no', label: 'No', value: false },
    ],
  },
  truefalse: {
    id: 'demo_truefalse',
    type: 'truefalse',
    prompt: 'El objetivo es medible y tiene fecha límite',
    options: [
      { id: 'true', label: 'Verdadero', value: true },
      { id: 'false', label: 'Falso', value: false },
    ],
  },
  single_choice: {
    id: 'demo_single',
    type: 'single_choice',
    prompt: '¿En qué etapa se encuentra tu proyecto?',
    options: [
      { id: 'idea', label: 'Solo la idea', value: 'idea' },
      { id: 'planning', label: 'En planificación', value: 'planning' },
      { id: 'mvp', label: 'MVP construido', value: 'mvp' },
      { id: 'selling', label: 'Ya vendiendo', value: 'selling' },
    ],
  },
  multi_choice: {
    id: 'demo_multi',
    type: 'multi_choice',
    prompt: '¿Qué obstáculos has enfrentado? (Selecciona todos los que apliquen)',
    options: [
      { id: 'time', label: 'Falta de tiempo', value: 'time' },
      { id: 'money', label: 'Falta de dinero', value: 'money' },
      { id: 'knowledge', label: 'Falta de conocimiento', value: 'knowledge' },
      { id: 'fear', label: 'Miedo al fracaso', value: 'fear' },
      { id: 'team', label: 'Falta de equipo', value: 'team' },
    ],
  },
  completion: {
    id: 'demo_completion',
    type: 'completion',
    prompt: 'Mi objetivo principal es:',
    placeholder: 'Completa la frase...',
  },
  multiline: {
    id: 'demo_multiline',
    type: 'multiline',
    prompt: 'Cuéntame más sobre tu situación actual...',
    placeholder: 'Escribe todos los detalles que consideres importantes...',
    minLength: 20,
  },
  ranking: {
    id: 'demo_ranking',
    type: 'ranking',
    prompt: 'Ordena estos objetivos por prioridad (1 = más importante):',
    options: [
      { id: 'revenue', label: 'Aumentar ingresos', value: 'revenue' },
      { id: 'customers', label: 'Conseguir clientes', value: 'customers' },
      { id: 'team', label: 'Armar equipo', value: 'team' },
      { id: 'product', label: 'Mejorar producto', value: 'product' },
    ],
  },
  open_exploration: {
    id: 'demo_open',
    type: 'open_exploration',
    prompt: '¿Qué es lo más importante para ti en este momento?',
    placeholder: 'Escribe libremente, sin restricciones...',
  },
};

export function QuestionContainer() {
  const { currentQuestion, setCurrentQuestion, addMessage } = useChatStore();
  const [comment, setComment] = useState('');
  const [answer, setAnswer] = useState<any>(null);
  
  // Estado para modo demo
  const [selectedDemoType, setSelectedDemoType] = useState<string>('yesno');

  // Resetear respuesta cuando cambia la pregunta
  useEffect(() => {
    setAnswer(null);
    setComment('');
  }, [currentQuestion]);

  // Para modo demo: cargar pregunta de ejemplo
  useEffect(() => {
    if (DEMO_MODE && !currentQuestion) {
      setCurrentQuestion(DEMO_QUESTIONS[selectedDemoType]);
    }
  }, [selectedDemoType]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const questionToUse = currentQuestion || DEMO_QUESTIONS[selectedDemoType];
    if (!questionToUse || !answer) return;

    // Construir mensaje desde respuesta
    const messageContent = buildMessageFromAnswer(questionToUse, answer, comment);

    addMessage({
      id: `msg_${Date.now()}`,
      role: 'user',
      content: messageContent,
      timestamp: new Date(),
      metadata: {
        mode: 'questionnaire',
        questionId: questionToUse.id,
      },
    });

    // TODO: Emitir via Socket.IO (se hará en Hito 1 completo)
    // socket.emit('option:select', currentQuestion.id, answer, comment);

    // Resetear
    setComment('');
    setAnswer(null);
    
    // Para modo demo: mostrar feedback en consola
    if (DEMO_MODE) {
      console.log('✅ RESPUESTA ENVIADA:', {
        question: questionToUse.prompt,
        type: questionToUse.type,
        answer,
        comment,
      });
    }
  };

  // Determinar qué pregunta mostrar
  const questionToRender = currentQuestion || DEMO_QUESTIONS[selectedDemoType];

  // Obtener el Viewer (capacidad) para este tipo de pregunta
  const ViewerComponent = VIEWERS[questionToRender.type] || OpenExplorationViewer;

  // Si no hay pregunta y no es demo mode, no mostrar nada
  if (!currentQuestion && !DEMO_MODE) {
    return null;
  }

  return (
    <div className="space-y-4 w-full max-w-full">
      {/* Panel de control para MODO DEMO */}
      {DEMO_MODE && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel rounded-xl p-4 border-2 border-yellow-500/30 demo-mode-panel"
        >
          <div className="flex items-center gap-2 mb-3">
            <Bug className="w-5 h-5 text-yellow-500 flex-shrink-0" />
            <h4 className="text-yellow-500 font-semibold whitespace-nowrap">MODO DEMO - Prueba Visual</h4>
          </div>
          <p className="text-sm text-white/70 mb-3">
            Selecciona un tipo de pregunta para probar la capacidad:
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 min-w-max">
            {Object.entries(DEMO_QUESTIONS).map(([type, q]: [string, any]) => (
              <button
                key={type}
                onClick={() => {
                  setSelectedDemoType(type);
                  setCurrentQuestion(q);
                  setAnswer(null);
                  setComment('');
                }}
                className={`p-2 rounded-lg text-sm transition-all whitespace-nowrap ${
                  selectedDemoType === type
                    ? 'bg-yellow-500/30 border border-yellow-500 text-white'
                    : 'bg-white/5 border border-transparent text-white/70 hover:bg-white/10'
                }`}
              >
                {type.replace('_', ' ')}
              </button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Panel de la pregunta - Container común */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel rounded-2xl p-6 viewer-root"
      >
        {/* Título de la pregunta */}
        <h3 className="text-lg font-semibold text-white mb-4">
          {questionToRender.prompt}
        </h3>

        {/* Renderizar la capacidad (Viewer) específica */}
        <div className="viewer-root">
          <ViewerComponent
            question={questionToRender}
            value={answer}
            onChange={setAnswer}
          />
        </div>
      </motion.div>

      {/* Comentario adicional */}
      <div className="flex gap-2 w-full">
        <div className="flex-1 min-w-0">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Comentario adicional (opcional)..."
            className="w-full glass-input rounded-2xl px-4 py-3 text-white placeholder-white/30 resize-none focus:outline-none focus:ring-2 focus:ring-cognitive-500/50 responsive-textarea"
            rows={2}
          />
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => handleSubmit()}
          disabled={!answer}
          className="flex-shrink-0 px-6 py-3 rounded-2xl bg-gradient-to-r from-cognitive-500 to-cognitive-600 text-white font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send className="w-4 h-4" />
          Continuar
        </motion.button>
      </div>
      
      {/* Feedback para modo demo */}
      {DEMO_MODE && answer && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="p-4 rounded-xl bg-green-500/20 border border-green-500/50 w-full"
        >
          <p className="text-green-400 text-sm break-all">
            ✅ Respuesta lista: <span className="text-white font-mono">{JSON.stringify(answer)}</span>
          </p>
          {comment && (
            <p className="text-green-400/70 text-sm mt-2 break-words">
              💬 Comentario: <span className="text-white/90">{comment}</span>
            </p>
          )}
        </motion.div>
      )}
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

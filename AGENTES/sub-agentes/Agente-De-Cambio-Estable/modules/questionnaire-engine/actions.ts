/**
 * Questionnaire Engine - Motor de preguntas dinámicas
 * 
 * @description
 * Genera preguntas estructuradas basadas en el dato que falta obtener,
 * siguiendo el diagrama de inferencia (02-inferencia-tipo-pregunta.md).
 * 
 * @module @agentedecambio2/questionnaire-engine
 */

import type {
  Question,
  QuestionType,
  QuestionOption,
  Answer,
  ObjectiveDomain
} from '@agentedecambio2/shared-types';

/**
 * generateQuestion - Genera pregunta dinámica según dato faltante
 * 
 * @param missingField - Nombre del campo que falta obtener
 * @param context - Contexto actual (objetivo, dominio, estado)
 * @returns Question estructurada con tipo, prompt y opciones
 * 
 * @example
 * ```typescript
 * const question = generateQuestion('has_prototype', {
 *   objective: 'launch_product',
 *   domain: 'constructor'
 * });
 * // { type: 'yesno', prompt: '¿Tienes un prototipo funcional?', ... }
 * ```
 */
export function generateQuestion(
  missingField: string,
  context: { objective: string; domain: ObjectiveDomain; stage?: string }
): Question {
  // Diagrama 02: Inferencia por tipo de dato
  const questionType = inferQuestionType(missingField);
  
  // Construir prompt según tipo y dominio
  const prompt = buildPrompt(questionType, missingField, context.domain);
  
  // Generar opciones según tipo
  const options = generateOptions(questionType, context.domain);
  
  return {
    id: `q_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    type: questionType,
    prompt,
    options,
    required: true,
    fieldKey: missingField,
  };
}

/**
 * parseAnswer - Procesa y valida respuesta del usuario
 * 
 * @param question - Pregunta original
 * @param rawResponse - Respuesta raw del usuario (selected, text, etc.)
 * @returns Answer procesada con valor tipado y confianza
 * 
 * @example
 * ```typescript
 * const answer = parseAnswer(question, {
 *   selected: 'yes',
 *   comment: 'Tengo MVP en React'
 * });
 * // { value: true, confidence: 'high', ... }
 * ```
 */
export function parseAnswer(
  question: Question,
  rawResponse: { selected?: string | string[]; text?: string; comment?: string }
): Answer {
  const { type, fieldKey } = question;
  
  let value: unknown;
  let confidence: 'low' | 'medium' | 'high' = 'medium';
  
  // Parsear según tipo de pregunta
  switch (type) {
    case 'yesno':
    case 'truefalse':
      value = rawResponse.selected === 'yes' || rawResponse.selected === 'true';
      confidence = 'high';
      break;
      
    case 'single_choice':
      value = typeof rawResponse.selected === 'string' ? rawResponse.selected : null;
      confidence = value ? 'high' : 'low';
      break;
      
    case 'multi_choice':
      value = Array.isArray(rawResponse.selected) ? rawResponse.selected : [rawResponse.selected];
      confidence = value.length > 0 ? 'high' : 'low';
      break;
      
    case 'completion':
      value = rawResponse.text?.trim() || null;
      confidence = value && value.length > 3 ? 'medium' : 'low';
      break;
      
    case 'multiline':
      value = rawResponse.text?.trim() || null;
      confidence = value && value.length > 20 ? 'medium' : 'low';
      break;
      
    case 'ranking':
      value = Array.isArray(rawResponse.selected) ? rawResponse.selected : null;
      confidence = value && value.length > 1 ? 'high' : 'low';
      break;
      
    case 'open_exploration':
      value = rawResponse.text || rawResponse.comment || '';
      confidence = 'medium'; // Sin validación estricta
      break;
      
    default:
      value = null;
      confidence = 'low';
  }
  
  return {
    id: `a_${Date.now()}`,
    questionId: question.id,
    fieldKey,
    value,
    confidence,
    rawComment: rawResponse.comment,
    answeredAt: new Date(),
  };
}

/**
 * validateSchema - Verifica campos críticos completados
 * 
 * @param answers - Respuestas recibidas hasta ahora
 * @param requiredFields - Campos requeridos para el estadio actual
 * @returns true si todos los campos críticos están completos
 * 
 * @example
 * ```typescript
 * const isValid = validateSchema(answers, ['has_prototype', 'deadline', 'budget']);
 * // true/false
 * ```
 */
export function validateSchema(
  answers: Answer[],
  requiredFields: string[]
): boolean {
  // Obtener campos completados con confianza alta/media
  const completedFields = answers
    .filter(a => a.confidence !== 'low' && a.value !== null)
    .map(a => a.fieldKey);
  
  // Verificar que todos los requeridos están completados
  return requiredFields.every(field => completedFields.includes(field));
}

// ============================================================================
// FUNCIONES AUXILIARES (INTERNAS)
// ============================================================================

/**
 * inferQuestionType - Infere tipo de pregunta según dato faltante (Diagrama 02)
 */
function inferQuestionType(missingField: string): QuestionType {
  // Mapeo de campos a tipos según diagrama de inferencia
  const fieldToTypeMap: Record<string, QuestionType> = {
    // Datos binarios → yesno
    has_prototype: 'yesno',
    has_team: 'yesno',
    has_budget: 'yesno',
    is_validated: 'yesno',
    
    // Validaciones lógicas → truefalse
    is_realistic: 'truefalse',
    is_measurable: 'truefalse',
    
    // Clasificación única → single_choice
    current_stage: 'single_choice',
    chronotype: 'single_choice',
    domain: 'single_choice',
    
    // Múltiples opciones → multi_choice
    obstacles: 'multi_choice',
    resources: 'multi_choice',
    support_network: 'multi_choice',
    
    // Texto breve → completion
    objective_title: 'completion',
    deadline: 'completion',
    metric_target: 'completion',
    
    // Explicación rica → multiline
    current_situation: 'multiline',
    main_obstacle: 'multiline',
    why_important: 'multiline',
    
    // Orden/preferencia → ranking
    priorities: 'ranking',
    preferred_approach: 'ranking',
    
    // Exploración → open_exploration
    notes: 'open_exploration',
    additional_context: 'open_exploration',
  };
  
  return fieldToTypeMap[missingField] || 'open_exploration';
}

/**
 * buildPrompt - Construye prompt de pregunta según tipo y dominio
 */
function buildPrompt(
  type: QuestionType,
  field: string,
  domain: ObjectiveDomain
): string {
  // Plantillas por tipo de pregunta
  const promptTemplates: Record<string, Record<string, string>> = {
    yesno: {
      has_prototype: '¿Tienes un prototipo funcional?',
      has_team: '¿Tienes un equipo definido?',
      has_budget: '¿Tienes el presupuesto necesario?',
      is_validated: '¿Has validado esto con usuarios reales?',
    },
    single_choice: {
      current_stage: '¿En qué etapa se encuentra tu proyecto?',
      chronotype: '¿Qué tipo de cronotipo tienes?',
      domain: '¿A qué dominio pertenece tu objetivo?',
    },
    multiline: {
      current_situation: 'Cuéntame más sobre tu situación actual...',
      main_obstacle: '¿Qué es lo que más te está dificultando avanzar?',
      why_important: '¿Por qué es importante este objetivo para ti?',
    },
    completion: {
      objective_title: 'Mi objetivo principal es:',
      deadline: 'La fecha límite es:',
      metric_target: 'La métrica de éxito es:',
    },
  };
  
  return promptTemplates[type]?.[field] || `Ingresa ${field.replace(/_/g, ' ')}:`;
}

/**
 * generateOptions - Genera opciones según tipo de pregunta
 */
function generateOptions(type: QuestionType, domain: ObjectiveDomain): QuestionOption[] {
  // Opciones predefinidas por tipo
  const optionsByType: Record<string, QuestionOption[]> = {
    yesno: [
      { id: 'yes', label: 'Sí', value: true },
      { id: 'no', label: 'No', value: false },
    ],
    truefalse: [
      { id: 'true', label: 'Verdadero', value: true },
      { id: 'false', label: 'Falso', value: false },
    ],
    single_choice: {
      // Se sobreescribe abajo por dominio
    } as any,
    multi_choice: [], // Dinámico según contexto
  };
  
  // Opciones específicas por dominio para current_stage
  if (type === 'single_choice') {
    const stageOptions: Record<ObjectiveDomain, QuestionOption[]> = {
      cura: [
        { id: 'idea', label: 'Solo la idea', value: 'idea' },
        { id: 'planning', label: 'En planificación', value: 'planning' },
        { id: 'active', label: 'Ya en ejecución', value: 'active' },
        { id: 'scaling', label: 'Buscando escalar', value: 'scaling' },
      ],
      constructor: [
        { id: 'blueprint', label: 'Solo planos', value: 'blueprint' },
        { id: 'foundation', label: 'Cimientos iniciados', value: 'foundation' },
        { id: 'structure', label: 'Estructura en pie', value: 'structure' },
        { id: 'finishing', label: 'Acabados', value: 'finishing' },
      ],
      estudiante: [
        { id: 'starting', label: 'Comenzando el curso', value: 'starting' },
        { id: 'midway', label: 'A mitad del curso', value: 'midway' },
        { id: 'final', label: 'Trabajo final', value: 'final' },
        { id: 'thesis', label: 'Tesis', value: 'thesis' },
      ],
      emprendedor: [
        { id: 'idea', label: 'Solo idea', value: 'idea' },
        { id: 'mvp', label: 'MVP construido', value: 'mvp' },
        { id: 'selling', label: 'Ya vendiendo', value: 'selling' },
        { id: 'scaling', label: 'Escalando', value: 'scaling' },
      ],
    };
    
    return stageOptions[domain] || stageOptions.emprendedor;
  }
  
  return optionsByType[type] || [];
}

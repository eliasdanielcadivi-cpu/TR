# Quiz Engine

## Funcionalidades (1-3)

1. `getQuizByDomain()` - Obtiene cuestionario por dominio (cura, constructor, etc.)
2. `getNextQuestion()` - Retorna siguiente pregunta según estado
3. `scoreAnswers()` - Evalúa respuestas y calcula score

## Flujo de Datos

- **Entrada:** Dominio + estado actual + respuestas previas
- **Procesamiento:** Aplica plantilla + inferencia (diagrama 02)
- **Salida:** Cuestionario estructurado o siguiente pregunta

## Eventos

### Emite
- `quiz:started` - Cuando inicia cuestionario
- `question:next` - Cuando hay siguiente pregunta
- `quiz:completed` - Cuando finaliza cuestionario

### Escucha
- `objective:defined` - Para cargar cuestionario
- `answer:submitted` - Para calcular siguiente

## Dependencias

| Módulo | Para qué |
|--------|----------|
| @agentedecambio2/shared-types | Tipos Quiz, Question |
| @agentedecambio2/questionnaire-engine | Generador de preguntas |
| @agentedecambio2/question-types | Validadores |

## Ejemplo de Uso

```typescript
import { getQuizByDomain, getNextQuestion, scoreAnswers } from './actions';

// Ejemplo 1: Obtener cuestionario por dominio
const quiz = getQuizByDomain('constructor');
// quiz = { id, stage: 'entrada', questions: [...] }

// Ejemplo 2: Obtener siguiente pregunta
const nextQ = getNextQuestion(quiz, {
  answeredQuestions: ['q1', 'q2'],
  currentStage: 'ubicacion'
});
// nextQ = { type: 'single_choice', prompt: '...', options: [...] }

// Ejemplo 3: Evaluar respuestas
const score = scoreAnswers(answers, quiz.scoringRubric);
// score = { total: 85, strengths: [...], gaps: [...] }
```

## Estructura del Módulo

```
quiz-engine/
├── INDEX.md      # Este archivo
├── actions.ts    # 3 funciones exportadas
├── templates/    # Plantillas por dominio
│   ├── cura.json
│   ├── constructor.json
│   ├── estudiante.json
│   └── emprendedor.json
├── manifest.json # Metadatos
└── test/
```

---

**Versión:** 0.1.0
**Última actualización:** 2026-03-19
**Estado:** En desarrollo (Hito 1)

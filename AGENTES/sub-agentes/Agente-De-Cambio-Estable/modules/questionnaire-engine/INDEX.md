# Questionnaire Engine

## Funcionalidades (1-3)

1. `generateQuestion()` - Genera pregunta dinámica según dato faltante
2. `parseAnswer()` - Procesa y valida respuesta del usuario
3. `validateSchema()` - Verifica campos críticos completados

## Flujo de Datos

- **Entrada:** Contexto + objetivo + estado actual
- **Procesamiento:** Infere tipo de pregunta según diagrama 02
- **Salida:** Pregunta estructurada (tipo, prompt, opciones)

## Eventos

### Emite
- `question:generated` - Cuando genera nueva pregunta
- `question:answered` - Cuando usuario responde

### Escucha
- `objective:updated` - Para ajustar preguntas
- `context:changed` - Para reinferir tipo

## Dependencias

| Módulo | Para qué |
|--------|----------|
| @agentedecambio2/shared-types | Tipos Question, QuestionType |
| @agentedecambio2/quiz-engine | Banco de cuestionarios |
| @agentedecambio2/question-types | Validadores por tipo |

## Ejemplo de Uso

```typescript
import { generateQuestion, parseAnswer } from './actions';

// Ejemplo 1: Generar pregunta para dato binario
const question = generateQuestion({
  missingField: 'has_prototype',
  context: { objective: 'launch_product' }
});
// question = {
//   type: 'yesno',
//   prompt: '¿Tienes un prototipo funcional?',
//   options: [{id: 'yes', label: 'Sí'}, {id: 'no', label: 'No'}]
// }

// Ejemplo 2: Parsear respuesta
const answer = parseAnswer(question, {
  selected: 'yes',
  comment: 'Tengo MVP en React'
});
// answer = { value: true, confidence: 'high' }

// Ejemplo 3: Validar schema completo
const isValid = validateSchema(answers, requiredFields);
// isValid = true/false
```

## Estructura del Módulo

```
questionnaire-engine/
├── INDEX.md      # Este archivo
├── actions.ts    # 3 funciones exportadas
├── types.ts      # Tipos específicos
├── manifest.json # Metadatos
└── test/
    └── actions.test.ts
```

---

**Versión:** 0.1.0
**Última actualización:** 2026-03-19
**Estado:** En desarrollo (Hito 1)

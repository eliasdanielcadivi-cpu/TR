# Question Types

## Funcionalidades (1-3)

1. `validateByType()` - Valida respuesta según tipo de pregunta
2. `getValidators()` - Obtiene validadores disponibles
3. `parseValue()` - Convierte respuesta raw a valor tipado

## Flujo de Datos

- **Entrada:** Tipo de pregunta + respuesta raw
- **Procesamiento:** Aplica validador específico
- **Salida:** Valor tipado + confianza (low/medium/high)

## Eventos

### Emite
- Ninguno (módulo stateless de utilidades)

### Escucha
- Ninguno

## Dependencias

| Módulo | Para qué |
|--------|----------|
| @agentedecambio2/shared-types | Tipos QuestionType, Answer |
| Ninguna externa | Puro TypeScript |

## Ejemplo de Uso

```typescript
import { validateByType, getValidators, parseValue } from './actions';

// Ejemplo 1: Validar pregunta Sí/No
const yesNoValid = validateByType('yesno', { selected: 'yes' });
// valid = true, value = true

// Ejemplo 2: Validar selección múltiple
const multiValid = validateByType('multi_choice', {
  selected: ['opt1', 'opt3']
});
// valid = true, value = ['opt1', 'opt3']

// Ejemplo 3: Parsear valor de completación
const completionValue = parseValue('completion', { text: 'Mi objetivo es X' });
// value = 'Mi objetivo es X', confidence = 'medium'

// Ejemplo 4: Obtener todos los validadores
const validators = getValidators();
// ['yesno', 'truefalse', 'single_choice', 'multi_choice', ...]
```

## Tipos de Pregunta Soportados

| Tipo | ID | Validación |
|------|-----|------------|
| Sí/No | `yesno` | Boolean estricto |
| Verdadero/Falso | `truefalse` | Boolean con mapeo |
| Selección única | `single_choice` | Un solo optionId |
| Selección múltiple | `multi_choice` | Array de optionIds |
| Completación | `completion` | Texto no vacío |
| Texto multilínea | `multiline` | Texto con longitud mínima |
| Ranking | `ranking` | Array ordenado sin duplicados |
| Exploración abierta | `open_exploration` | Texto libre (sin validación estricta) |

## Estructura del Módulo

```
question-types/
├── INDEX.md          # Este archivo
├── actions.ts        # 3 funciones exportadas
├── types.ts          # Tipos específicos
├── validators.ts     # Validadores por tipo
├── manifest.json     # Metadatos
└── test/
    └── validators.test.ts
```

---

**Versión:** 0.1.0
**Última actualización:** 2026-03-19
**Estado:** En desarrollo (Hito 1)

# 📚 ÍNDICE DE MÓDULOS - Agente de Cambio Estable

> **Propósito:** Lista central de todos los módulos del proyecto con enlaces a su documentación  
> **Última actualización:** 2026-03-20 19:00  
> **Total de módulos:** 12

---

## 📦 MÓDULOS BACKEND

| # | Módulo | Ruta | Funciones | Estado | AI Ready |
|---|--------|------|-----------|--------|----------|
| 1 | **DeepSeek Connector** | [`/modules/deepseek-connector/`](./modules/deepseek-connector/INDEX.md) | `createCompletion()`, `createCompletionStream()` | ✅ completado | ✅ |
| 2 | **Session Manager** | [`/modules/session-manager/`](./modules/session-manager/INDEX.md) | `createSession()`, `getSession()`, `updateSession()` | ✅ completado | ✅ |
| 3 | **Prompt Engine** | [`/modules/prompt-engine/`](./modules/prompt-engine/INDEX.md) | `buildSystemPrompt()`, `updatePrompt()`, `negotiateChange()` | ✅ completado | ✅ |
| 4 | **Delta Calculator** | [`/modules/delta-calculator/`](./modules/delta-calculator/INDEX.md) | `calculate()`, `compare()`, `threshold()` | ✅ completado | ✅ |
| 5 | **Cognitive Need Detector** | [`/modules/cognitive-need-detector/`](./modules/cognitive-need-detector/INDEX.md) | `analyzeCognitiveNeed()`, `evaluateDataGaps()`, `detectEmotionalState()` | ✅ completado | ✅ |
| 6 | **Mode Transition Engine** | [`/modules/mode-transition-engine/`](./modules/mode-transition-engine/INDEX.md) | `generateTransitionPrompt()`, `buildContextSummary()`, `createBridgeMessage()` | ✅ completado | ✅ |
| 7 | **Questionnaire Engine** | [`/modules/questionnaire-engine/`](./modules/questionnaire-engine/INDEX.md) | `generateQuestion()`, `parseAnswer()`, `validateSchema()` | 🟡 in-development | ❌ |
| 8 | **Quiz Engine** | [`/modules/quiz-engine/`](./modules/quiz-engine/INDEX.md) | `getQuizByDomain()`, `getNextQuestion()`, `scoreAnswers()` | 🟡 in-development | ❌ |

---

## 📦 MÓDULOS FRONTEND

| # | Módulo | Ruta | Funciones | Estado | AI Ready |
|---|--------|------|-----------|--------|----------|
| 9 | **State Manager (Zustand)** | [`/modules/state-manager/`](./modules/state-manager/INDEX.md) | `createStore()`, `persist()`, `subscribe()` | 🟡 pending | ❌ |

---

## 📦 MÓDULOS SHARED

| # | Módulo | Ruta | Funciones | Estado | AI Ready |
|---|--------|------|-----------|--------|----------|
| 10 | **Shared Types** | [`/modules/shared-types/`](./modules/shared-types/INDEX.md) | (tipos TypeScript) | ✅ completado | ✅ |
| 11 | **Question Types** | [`/modules/question-types/`](./modules/question-types/INDEX.md) | `validateByType()`, `getValidators()`, `parseValue()` | 🟡 in-development | ✅ |

---

## 📦 MÓDULOS PENDIENTES (Hito 3+)

| # | Módulo | Ruta | Funciones | Estado | AI Ready |
|---|--------|------|-----------|--------|----------|
| 12 | **Architect** | `/modules/architect/` | `evaluatePromptChange()`, `evaluateMerecimiento()` | ❌ pendiente | ❌ |
| 13 | **Objectives Manager** | `/modules/objectives-manager/` | `extractEMT()`, `saveObjective()`, `getActiveObjectives()` | ❌ pendiente | ❌ |
| 14 | **Stall Detector** | `/modules/stall-detector/` | `detectStallSignals()`, `getStallType()`, `getSignalStrength()` | ❌ pendiente | ❌ |
| 15 | **Stall Intervention** | `/modules/stall-intervention/` | `generateIntervention()`, `getTherapyType()`, `applyTherapy()` | ❌ pendiente | ❌ |

---

## 📊 ESTADÍSTICAS

| Métrica | Valor |
|---------|-------|
| **Total módulos** | 12 |
| **Completados** | 8 |
| **In-development** | 3 |
| **Pending** | 5 |
| **AI Ready** | 6 |

---

## 🔗 ENLACES RÁPIDOS

- **Registry JSON:** [`/modules/registry.json`](./modules/registry.json)
- **Metodología Modular:** [`/docs/CLAVE/METODOLOGIA-MODULAR.md`](./docs/CLAVE/METODOLOGIA-MODULAR.md)
- **Plan de Construcción:** [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md)

---

## 📝 CONVENCIONES

1. **Máximo 3 funciones** por módulo (modularidad atómica)
2. **INDEX.md < 50 líneas** (resumen ejecutivo)
3. **manifest.json** obligatorio en cada módulo
4. **JSDoc** en todas las funciones exportadas

---

*Índice generado: 2026-03-20 19:00*  
*Próxima actualización: Cuando se agregue/modifique un módulo*

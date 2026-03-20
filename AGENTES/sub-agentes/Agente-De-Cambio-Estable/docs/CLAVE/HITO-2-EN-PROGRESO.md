# 📋 HITO 2 EN PROGRESO - INTEGRACIÓN CHAT-CUESTIONARIOS CON CONTROL DE DERIVA

> **Estado:** 🟡 EN PROGRESO  
> **Fecha de inicio:** 2026-03-20  
> **Próximo hito:** Hito 3 - Arquitecto + Control de Deriva

---

## 🎯 OBJETIVO DEL HITO 2

Integrar el **chat** y los **cuestionarios** mediante un **Orquestador Cognitivo** que decide cuándo cambiar de modo y realiza transiciones suaves, preparando el terreno para el **Control de Deriva** del Hito 3.

---

## 📦 MÓDULOS CREADOS (Hito 2)

### Fase 1 y 2: Detector + Transición

| Módulo | Ruta | Funciones | Estado | AI Ready |
|--------|------|-----------|--------|----------|
| **cognitive-need-detector** | `/modules/cognitive-need-detector/` | `analyzeCognitiveNeed()`, `evaluateDataGaps()`, `detectEmotionalState()` | 🟡 in-development | ✅ |
| **mode-transition-engine** | `/modules/mode-transition-engine/` | `generateTransitionPrompt()`, `buildContextSummary()`, `createBridgeMessage()` | 🟡 in-development | ✅ |
| **system-master-prompt** | `/modules/prompt-engine/templates/` | `injectObjectives()`, `injectModeContext()`, `injectUserContext()` | ✅ completado | ✅ |

---

## 🔄 ARQUITECTURA DE INTEGRACIÓN

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA 2 — ORQUESTACIÓN COGNITIVA               │
├─────────────────────────────────────────────────────────────────┤
│  1. DETECTOR DE NECESIDAD COGNITIVA ✅                          │
│     └── Decide: ¿Necesito datos estructurados o conversación?   │
│                                                                  │
│  2. EXTRACTOR DE OBJETIVO EMT (questionnaire-engine) ✅         │
│     └── Cuando detecta objetivo nuevo → activa cuestionario     │
│                                                                  │
│  3. ROUTER DE FLUJO (mode-transition-engine) ✅                 │
│     └── Transición suave: Chat ↔ Cuestionario ↔ Mixto           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA 3 — GOBERNANZA Y CONTROL                 │
├─────────────────────────────────────────────────────────────────┤
│  4. ARQUITECTO / CAPA DE CONTROL ❌ (Hito 3)                    │
│     ├── Calcula delta del prompt propuesto por el Ejecutor      │
│     ├── Filtro de merecimiento: ¿El cambio alinea con objetivo? │
│     └── Veto si deriva > 0.6 o desalineado con EMT              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 REGLAS DE DECISIÓN (Cognitive Need Detector)

| Regla | Condición | Decisión | Urgencia |
|-------|-----------|----------|----------|
| **1** | Objetivo nuevo/ambiguo | `questionnaire` (EMT extraction) | 🔴 high |
| **2** | Faltan datos estructurados | `questionnaire` | 🔴 high |
| **3** | Usuario confuso/resistente | `chat` (emotional exploration) | 🟡 medium |
| **4** | Clasificación + matiz | `mixed` (secuencia: questionnaire → chat) | 🟡 medium |
| **5** | 5+ mensajes chat sin estructura | `questionnaire` (synthesis) | 🟢 low |
| **DEFAULT** | Ninguna anterior | Mantener modo actual | 🟢 low |

---

## 🗣️ PLANTILLAS DE TRANSICIÓN (Mode Transition Engine)

### Chat → Cuestionario

```typescript
emt_extraction: 
  "Perfecto, estoy captando tu objetivo. Para asegurarme de que lo 
   entiendo exactamente, me gustaría que me ayudes a estructurarlo 
   en tres puntos: ¿qué evidencia concreta quieres ver, qué métrica 
   lo medirá, y para cuándo? Esto nos ayudará a mantener el rumbo."

structured_data:
  "Entiendo la situación. Para no perder detalles importantes, 
   ¿te parece si organizamos la siguiente parte en opciones? 
   Así puedes elegir rápido y añadir cualquier matiz al final."
```

### Cuestionario → Chat

```typescript
emotional_block:
  "Gracias por esas respuestas. Noto que hay algo más detrás de esto... 
   ¿Te gustaría contarme un poco más sobre cómo te sientes con este objetivo?"

exploration_needed:
  "Antes de continuar con la siguiente pregunta, me gustaría entender 
   mejor tu contexto. ¿Qué te llevó a elegir esa opción?"
```

---

## 🧪 PRUEBAS PENDIENTES

### Integración con Socket.IO

```typescript
// apps/server/src/sockets/orchestrator-handler.ts (POR CREAR)

import { analyzeCognitiveNeed } from '@modules/cognitive-need-detector/actions';
import { generateTransitionPrompt } from '@modules/mode-transition-engine/actions';

socket.on('message:send', async (content, mode, context) => {
  // 1. Analizar necesidad cognitiva
  const decision = analyzeCognitiveNeed(context);
  
  // 2. Si cambio de modo, generar transición
  if (decision.mode !== mode) {
    const transition = generateTransitionPrompt(
      mode,
      decision.mode,
      decision.reason,
      context
    );
    
    // 3. Enviar transición al usuario
    socket.emit('mode:switch', {
      from: mode,
      to: decision.mode,
      message: transition.message
    });
  }
  
  // 4. Continuar con flujo normal...
});
```

---

## 📊 ESTADO ACTUAL

| Componente | Estado | Próximo paso |
|------------|--------|--------------|
| **cognitive-need-detector** | ✅ Código completo | Integrar con Socket.IO |
| **mode-transition-engine** | ✅ Código completo | Integrar con Socket.IO |
| **system-master-prompt** | ✅ Completo | Inyectar en llamada a DeepSeek |
| **Socket.IO integration** | ❌ Pendiente | Crear `orchestrator-handler.ts` |
| **Frontend mode switching** | ⚠️ Parcial | Escuchar evento `mode:switch` |

---

## 🎯 CRITERIOS DE ACEPTACIÓN

| Criterio | Estado | Evidencia |
|----------|--------|-----------|
| Módulos con INDEX.md <50 líneas | ✅ | 2 módulos creados |
| Cada módulo tiene manifest.json | ✅ | 2 manifest.json |
| Máximo 3 funciones por módulo | ✅ | 3 funciones cada uno |
| Referencia a Diagrama 01 y 02 | ✅ | Todos referencian diagramas |
| Registry actualizado | ✅ | 12 módulos totales |
| Git tags de respaldo | ❌ Pendiente | Crear `hito-2-inicio` |

---

## 🔄 PRÓXIMOS PASOS (FASE 3 y 4)

### FASE 3: Integración con Socket.IO

```bash
# 1. Crear handler del orquestador
touch apps/server/src/sockets/orchestrator-handler.ts

# 2. Importar módulos
# import { analyzeCognitiveNeed } from '@modules/cognitive-need-detector/actions';
# import { generateTransitionPrompt } from '@modules/mode-transition-engine/actions';

# 3. Integrar en socket.on('message:send')
```

### FASE 4: SYSTEM_MASTER_PROMPT en DeepSeek

```bash
# 1. Actualizar modules/prompt-engine/actions.ts
# 2. Importar SYSTEM_MASTER_PROMPT
# 3. Inyectar objetivos EMT en cada llamada
```

---

## 📅 CRONOGRAMA ESTIMADO

| Día | Tarea | Estado |
|-----|-------|--------|
| **2026-03-20** | Crear cognitive-need-detector | ✅ |
| **2026-03-20** | Crear mode-transition-engine | ✅ |
| **2026-03-20** | Crear system-master-prompt | ✅ |
| **2026-03-20** | Actualizar registry.json | ✅ |
| **2026-03-21** | Integrar con Socket.IO | ❌ Pendiente |
| **2026-03-21** | Actualizar frontend para mode switching | ❌ Pendiente |
| **2026-03-22** | Testear flujo completo | ❌ Pendiente |

---

**Documento creado:** 2026-03-20  
**Hito 2:** 🟡 EN PROGRESO  
**Próxima revisión:** Después de integración Socket.IO

---

*Fin del informe del Hito 2 (en progreso)*

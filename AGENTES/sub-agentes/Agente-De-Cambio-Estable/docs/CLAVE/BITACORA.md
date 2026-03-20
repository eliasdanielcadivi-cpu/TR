# 📝 BITÁCORA DE CAMBIOS - Agente de Cambio Estable

> **Propósito:** Registrar cronológicamente todos los cambios significativos del proyecto  
> **Formato:** Cada entrada = fecha + hora + descripción + archivos afectados  
> **Ubicación:** `/docs/CLAVE/BITACORA.md`

---

## 2026-03-20

### [18:00] Corrección: Modo demo desactivado por defecto
**Archivos:** `apps/web/components/chat/QuestionContainer.tsx`
- `DEMO_MODE` cambiado a `false`
- Cuestionario ahora solo se activa vía Socket.IO
- Se agrega check: `if (!currentQuestion && !DEMO_MODE) return null`

**Razón:** El modo demo interfería con el flujo normal. Ahora el cuestionario se activa solo cuando el orquestador lo decide.

---

### [18:00] Corrección: Prohibido JSON en respuestas del LLM
**Archivos:** `modules/prompt-engine/templates/system-master-prompt.ts`
- Agregada sección `⚠️ PROHIBIDO RESPONDER CON JSON ⚠️`
- Ejemplos de cierre válido vs inválido
- Instrucción explícita: "SIEMPRE responde en lenguaje natural"

**Razón:** El LLM estaba respondiendo con JSON en lugar de usar la UI de cuestionario.

---

### [18:00] Feature: Botón RESET con confirmación
**Archivos:** `apps/web/components/layout/Header.tsx`
- Nuevo botón con ícono `RotateCcw`
- Diálogo de confirmación con backdrop blur
- Lista de lo que se eliminará
- Función `handleReset()` que llama a `clearMessages()`

**Razón:** Usuario necesita poder reiniciar la conversación fácilmente.

---

### [17:30] Fix: Imports de módulos con index.ts
**Archivos:** 
- `modules/cognitive-need-detector/index.ts` (nuevo)
- `modules/mode-transition-engine/index.ts` (nuevo)
- `apps/server/src/orchestrator-handler.ts` (imports corregidos)

**Razón:** El servidor no encontraba los módulos `@modules/cognitive-need-detector`.

---

### [17:00] Fix: Orchestrator handler imports
**Archivos:** `apps/server/src/orchestrator-handler.ts`
- Corregidos imports de `@modules/*`

**Razón:** Error en tiempo de ejecución "Cannot find module".

---

## 2026-03-19

### [18:40] HITO 1 COMPLETADO - Motor de Cuestionarios
**Archivos creados:**
- `docs/CLAVE/HITO-1-COMPLETADO.md`
- 8 Viewers en `apps/web/components/chat/viewers/`
- `QuestionContainer.tsx`

**Módulos:**
- `questionnaire-engine`
- `quiz-engine`
- `question-types`

**Tags:** `hito-1-inicio-20260319`, `hito-1-completado-20260319`

---

## 2026-03-20 (continuación)

### [12:00] HITO 2 COMPLETADO - Orquestador Cognitivo
**Archivos creados:**
- `docs/CLAVE/HITO-2-EN-PROGRESO.md` (ahora COMPLETADO)
- `modules/cognitive-need-detector/`
- `modules/mode-transition-engine/`
- `apps/server/src/orchestrator-handler.ts`

**Tags:** 
- `hito-2-fase1-completado-20260320`
- `hito-2-integracion-completada-20260320`
- `hito-2-listo-para-prueba-20260320`

---

## Próxima entrada pendiente

**Para registrar nuevos cambios:**
1. Editar este archivo
2. Agregar entrada con formato: `### [HH:MM] Título`
3. Listar archivos afectados
4. Describir razón del cambio

**Cada ~10 entradas:** Solicitar a LLM que resuma los cambios más importantes.

---

*Bitácora iniciada: 2026-03-20*  
*Última actualización: 2026-03-20 18:00*

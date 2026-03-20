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

### [18:30] Commit masivo de correcciones
**Archivos:** Múltiples (ver abajo)
- `QuestionContainer.tsx` - DEMO_MODE = false
- `system-master-prompt.ts` - Prohibido JSON
- `Header.tsx` - Botón RESET
- `BITACORA.md` - Este archivo

**Razón:** Corregir problemas reportados por usuario:
1. LLM respondía con JSON en lugar de UI
2. Modo demo siempre activo
3. Sin botón de reset
4. Sin bitácora de cambios

**Commit:** `3a5c7db4 [FIX] Desactivar demo mode + prohibir JSON LLM + botón RESET + bitácora`

---

### [18:45] Prompt anti-JSON + Enter para enviar
**Archivos:**
- `modules/prompt-engine/templates/system-master-prompt.ts` - Instrucciones explícitas anti-JSON
- `apps/web/components/chat/QuestionContainer.tsx` - Enter envía, scroll automático

**Cambios:**
- Prompt ahora incluye ejemplos ✅ y ❌ MUY explícitos
- Instrucciones en lenguaje coloquial ("Escribí COMO UNA PERSONA")
- Tecla Enter (sin Shift) envía la respuesta
- Placeholder actualizado: "Presiona Enter para enviar"
- Scroll automático al cambiar de modo

**Razón:** El LLM ignoraba instrucciones anteriores y seguía respondiendo con JSON.

---

### [19:00] Documentación maestra para IAs nuevas
**Archivos:**
- `docs/CLAVE/TODO-001-MAESTRO-20260320-1900.md` - NUEVO (problemas + rutas absolutas)
- `docs/INDICE-MODULOS.md` - NUEVO (lista de módulos con enlaces)
- `docs/INDICE-DOCUMENTACION.md` - NUEVO (lista de documentos de ayuda)
- `LEEME.md` - ACTUALIZADO (procedimientos + referencias a índices)

**Cambios:**
- TODO-001: Documento maestro con rutas absolutas para nueva IA
- Índices complementarios (NO repetitivos):
  - INDICE-MAESTRO-PARA-IAS.md → Arquitectura TR-ARES
  - LEEME.md → Procedimientos de este proyecto
  - INDICE-MODULOS.md → Si vas a modificar módulos
  - INDICE-DOCUMENTACION.md → Si vas a leer documentación
- LEEME.md ahora incluye:
  - Agenda del sistema (TODO-001, estado, BITACORA)
  - Flujo de lectura para nueva IA
  - Procedimientos obligatorios (antes de/durante/después)
  - Problemas conocidos (referencia a TODO-001)

**Razón:** Nueva IA necesita punto de entrada único con:
1. Rutas absolutas para encontrar archivos
2. Problemas conocidos y intentos fallidos
3. Flujo de trabajo claro (qué leer primero)
4. Índices complementarios para navegar

**Commit:** Por aprobar

---

*Bitácora iniciada: 2026-03-20*  
*Última actualización: 2026-03-20 19:00*

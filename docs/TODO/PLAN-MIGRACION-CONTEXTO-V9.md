# 🛰️ PLAN DE ACCIÓN: ARQUITECTURA COGNITIVA V9.0 (SOTA & SOBERANA)

Este documento es el **Mapa de Ruta Innegociable** y el **Cuaderno de Bitácora** para la migración al "Nuevo Contexto". Sigue un enfoque de ingeniería forense, con fases medibles y validación en tierra (CLI Real).

---

## 📓 NOTAS DEL ARQUITECTO (CUADERNO DE PRECAUCIÓN)
*«Actuar como humano olvidadizo pero precavido»*

- **Ojo con Ollama:** La lógica de streaming ya está en `modules/ia/ai_engine.py`. No la reescribas, **reconfigúrala**. Necesitamos que el dispatcher de Ollama sea el estándar para el "Switche" determinista.
- **Gemini-CLI:** No olvidar que `ares gemini` ya existe y es estable. La meta es que sea un *Provider* más dentro de la orquestación, no un wrapper aislado.
- **Función Candidata:** La función de `retrieve` en `apollo` tiene lógica de ranking RRF valiosa. **NO BORRAR**. Anotar para re-adaptarla al buscador de `:Concepts` en Memgraph.
- **Recordatorio Crítico:** El Ciclo STORM original en `orchestrator.py` usa spaCy de forma rígida. Hay que extraer la lógica de extracción de entidades para que sea una **Tool** invocable, no un paso obligatorio del core.

---

## 🏛️ ESTRUCTURA ONTOLÓGICA (Diferenciación de Unidades)

1. **Núcleo Agnóstico (Cerebro):**
   - Gestión de Memgraph (Taxonomía/Ontología).
   - Orquestador de Providers (Ollama, OpenRouter, Gemini-CLI).
   - Switche Determinista-Inferencial.
2. **Ontología Fullstack (Mente del Programador):**
   - Ciclo de Vida de Software (Fase DEV/PLAN).
   - MKBs de arquitectura de carpetas (`src/main.py` soberano).
   - Reglas de "3 funciones por módulo".

---

## 🚀 FASES DE EJECUCIÓN Y PROTOCOLOS DE TEST

### FASE 1: LIMPIEZA FORENSE Y TRASLADO DE ADN
*Objetivo: Despejar el Core y aislar código reutilizable.*

- **Acción:** Mover `modules/ia/apollo/` y `modules/rag/` a `/home/daniel/tron/programas/DOCUMENTACION-REPO/extraido_de_rag_de_TR/`.
- **Tarea Precavida:** Crear un archivo `NOTAS_REUTILIZACION.md` en el destino detallando qué funciones de Apollo (ranking, chunking) sirven para el nuevo RAG-G.
- **TEST REAL:**
  ```bash
  ls /home/daniel/tron/programas/DOCUMENTACION-REPO/extraido_de_rag_de_TR/ # Verificar existencia
  ares p "test" --rag docs # Debe fallar o indicar que el módulo no está (Control de Ruido)
  ```

### FASE 2: ORQUESTACIÓN SOBERANA DE PROVEEDORES
*Objetivo: Integrar Ollama, OpenRouter y Gemini-CLI en un único dispatcher intuitivo.*

- **Estado:** ✅ VALIDADO EN PRODUCCIÓN (2026-05-09)
- **Acción:** Refactorizado `modules/ia/ai_engine.py`. Integrado `GeminiProvider` y `OpenRouterProvider` funcional.
- **Doble Verificación:** Validado via terminal output AND logs/system status (ollama ps).
- **Aviso:** Se detectaron advertencias de RAM (8GB) que el sistema maneja correctamente via `LimitManager`.
- **TEST REAL:**
  ```bash
  ares p "Hola" -P ollama -m ares:latest # Test Local -> EXITOSO
  ares p "Hola" -P gemini # Test via Gemini-CLI -> EXITOSO
  ares p "Hola" -P openrouter -m deepseek/deepseek-chat # Test Cloud -> EXITOSO
  ```

### FASE 3: ACTIVACIÓN RAG-G (EL NUEVO CONTEXTO)
*Objetivo: Implementar la Taxonomía de Conceptos y el Switche en Memgraph.*

- **Estado:** ✅ VALIDADO BAJO NODO [D.2] (2026-05-09)
- **Acción:** Implementada jerarquía `(:Domain)->(:Category)->(:Topic)->(:Concept)->(:Chunk)`.
- **Switche Determinista:** Implementado `query_deterministic` (Cypher léxico) y `query_hybrid` (Vectorial HNSW Fallback).
- **Evidencia Física:** 
  - Log Ingesta: `logs/test_v9_ingesta.log` -> RESULT: Jerarquía detectada.
  - Log Recuperación: `logs/test_v9_retrieval.log` -> RESULT: Concepto 'GeminiProvider' recuperado.
- **TEST REAL:**
  ```bash
  python3 tests/test_v9_ingesta.py # OK
  python3 tests/test_v9_retrieval.py # OK
  ```

### FASE 4: ONTOLOGÍA DE DESARROLLO (MODO PROGRAMADOR)
*Objetivo: Aplicar las reglas de ciclo de vida y arquitectura de carpetas.*

- **Acción:** Implementar el NODO [D.1] (Ciclo de Vida). Crear generador automático de `docs/TODO/` con formato de fecha estricto.
- **Regla de Oro:** Forzar que `main.py` solo orqueste.
- **TEST REAL:**
  ```bash
  ares init --status # Verificar que la estructura de carpetas cumple el Pentágono
  ares todo "Nueva Función" # Crear bitácora con formato: [Nombre] - [Fecha].md
  ```

---

## 🔍 HITOS DE REVISIÓN Y COMPARACIÓN (CONCIENCIA DE FLUJO)

Al final de cada fase, es **OBLIGATORIO** ejecutar el protocolo de revisión:

1. **Lectura Forense:** Leer `/home/daniel/Escritorio/BORRAR/BORRADORES/Diagramas de Flujo.md`.
2. **Contraste:** ¿El código actual sigue el flujo de datos narrado en el DFD?
3. **Notificación:** Avisar al usuario con un informe de "Sincronía o Deriva".
4. **Ajuste:** Si el diagrama debe cambiar para reflejar la realidad técnica más eficaz, proponer la actualización del MKB correspondiente.

---

## 🚩 ESTADO DE INFRAESTRUCTURA (REQUISITOS PREVIOS)
- **Memgraph:** Debe estar activo vía Docker (`ares mem start`). No hay plan B; si falla, se reporta error de infraestructura.
- **Conectividad:** Ollama local debe responder en `localhost:11434`.

---
*Diseñado bajo el mandato del Arquitecto. No se realizarán cambios físicos hasta recibir el comando de inicio.*

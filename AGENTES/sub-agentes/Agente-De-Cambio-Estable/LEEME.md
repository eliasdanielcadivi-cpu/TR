# 📘 LEEME.md - Agente de Cambio Estable

> **Resumen Ejecutivo + Procedimientos**  
> **Última actualización:** 2026-03-20 19:00  
> **Versión:** 0.2.0  
> **Estado:** Hito 2 Completado - Integración Chat-Cuestionarios

---

## ¿QUÉ ES ESTO?

**Agente de Cambio Estable** es un **sistema de conducción cognitiva** que ayuda a usuarios a lograr objetivos mediante:

1. **Conversación estructurada** - Preguntas dinámicas (botones + comentario libre)
2. **Memoria de objetivos** - Guarda metas EMT (Evidencia-Métrica-Tiempo)
3. **Control de deriva** - Evita que la IA se desvíe del objetivo
4. **Detección de estancamiento** - 12 señales + 3 terapias de intervención
5. **Orquestador cognitivo** - Decide automáticamente cuándo cambiar entre chat y cuestionario

**NO es un chatbot.** Es un motor de ejecución con interfaz conversacional.

---

## 🚀 INICIO RÁPIDO (3 PASOS)

```bash
# 1. Ir al directorio
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable

# 2. Instalar dependencias
npm install --legacy-peer-deps

# 3. Configurar API Key y ejecutar
cp apps/server/.env.example apps/server/.env
# Editar apps/server/.env con DEEPSEEK_API_KEY
npm run dev
```

**Acceder:** http://localhost:3000

---

## 📍 AGENDA DEL SISTEMA (UNA SOLA)

**Ubicación:** `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/docs/CLAVE/`

| Documento | Propósito | Cuándo Leer |
|-----------|-----------|-------------|
| **[TODO-001-MAESTRO.md](./docs/CLAVE/TODO-001-MAESTRO-20260320-1900.md)** | Problemas pendientes + rutas absolutas | **PRIMERO** - Nueva IA |
| **[estado.md](./docs/CLAVE/estado.md)** | Qué está en desarrollo | Antes de modificar código |
| **[BITACORA.md](./docs/CLAVE/BITACORA.md)** | Historial de cambios | Después de modificar |

---

## 📚 ÍNDICES DE DOCUMENTACIÓN

### Índices Complementarios (NO Repetitivos)

| Índice | Contenido | Cuándo Usar |
|--------|-----------|-------------|
| **[ÍNDICE-MAESTRO-PARA-IAS.md](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md)** | Arquitectura TR-ARES completa | **Siempre primero** - Contexto general |
| **[LEEME.md](/LEEME.md)** (este archivo) | Procedimientos + estado del proyecto | **Segundo** - Este proyecto específico |
| **[INDICE-MODULOS.md](./docs/INDICE-MODULOS.md)** | Lista de módulos con enlaces | Si vas a **modificar módulos** |
| **[INDICE-DOCUMENTACION.md](./docs/INDICE-DOCUMENTACION.md)** | Lista de documentos de ayuda | Si vas a **leer documentación** |

### Flujo de Lectura para Nueva IA

```
1. INDICE-MAESTRO-PARA-IAS.md (arquitectura TR-ARES)
   ↓
2. LEEME.md (este proyecto - procedimientos)
   ↓
3. TODO-001-MAESTRO.md (problemas pendientes)
   ↓
4. estado.md (qué está en desarrollo)
   ↓
5. Según tarea:
   ├── ¿Modificar módulos? → INDICE-MODULOS.md → módulo/INDEX.md
   └── ¿Leer docs? → INDICE-DOCUMENTACION.md → documento.md
```

---

## 📋 PROCEDIMIENTOS OBLIGATORIOS

### Antes de Modificar Código

1. **Leer LEEME.md** (este archivo) - Procedimientos
2. **Leer TODO-001-MAESTRO.md** - Problemas conocidos
3. **Leer estado.md** - Qué está en desarrollo
4. **Crear backup git:**
   ```bash
   git tag "backup-$(date '+%Y%m%d-%H%M%S')"
   ```

### Al Modificar Módulos

1. **Máximo 3 funciones** por módulo (regla de modularidad atómica)
2. **INDEX.md < 50 líneas** (resumen ejecutivo)
3. **manifest.json obligatorio** en cada módulo
4. **JSDoc en todas las funciones** exportadas
5. **Actualizar registry.json** si agregó módulo nuevo

### Después de Modificar

1. **Git diff:**
   ```bash
   git diff --stat
   ```
2. **Tests passing:**
   ```bash
   npm test
   ```
3. **Actualizar INDEX.md** del módulo (si tocó código)
4. **Actualizar BITACORA.md** si es cambio significativo
5. **Commit descriptivo:**
   ```bash
   git add -A
   git commit -m "[TIPO] Descripción corta"
   # Tipos: FIX, FEAT, DOC, TEST, REFACTOR
   ```

### Git Tags de Respaldo

| Situación | Comando |
|-----------|---------|
| **Antes de cambios estructurales** | `git tag "backup-$(date '+%Y%m%d-%H%M%S')" ` |
| **Hito completado** | `git tag "hito-N-completado-YYYYMMDD"` |
| **Listo para prueba** | `git tag "hito-N-listo-para-prueba-YYYYMMDD"` |

---

## 🎯 HITOS ACTUALES

| Hito | Nombre | Estado | Criterio |
|------|--------|--------|----------|
| **1** | Motor Cuestionarios + Quiz | ✅ **COMPLETADO** | 8 capacidades implementadas |
| **2** | Integración Chat-Cuestionarios | ✅ **COMPLETADO** | Orquestador + Socket.IO |
| **3** | Arquitecto + Control Deriva | ❌ Pendiente | Doble instancia, veto cambios |
| **4** | Perfil Biológico | ❌ Pendiente | Adapta al cronotipo |
| **5** | Integración TR-ARES | ❌ Pendiente | Standalone + ARES |

**Ver plan completo:** [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md)

---

## 🔧 COMANDOS ESENCIALES

### Desarrollo

```bash
npm run dev              # Ambos servidores
npm run dev:server       # Solo backend (puerto 3001)
npm run dev:web          # Solo frontend (puerto 3000)
```

### Tests y Linting

```bash
npm test                 # Todos los módulos
npm run lint             # Linting
```

### Git Backups (OBLIGATORIO)

```bash
git tag "backup-$(date '+%Y%m%d-%H%M%S')"   # Antes de cambiar
git diff --stat                             # Después de cambiar
git log -3 --oneline                        # Ver últimos commits
```

### Reset de Emergencia

```bash
# Resetear sesión (frontend)
# Click en botón ↻ (arriba derecha) → Confirmar

# Resetear git (si algo sale mal)
git reset --hard HEAD
git clean -fd
```

---

## 📦 ESTRUCTURA DEL PROYECTO

```
Agente-De-Cambio-Estable/
├── LEEME.md                      ← ESTE ARCHIVO (procedimientos)
├── README.md                     ← Extendido (referencias)
├── docs/
│   ├── CLAVE/
│   │   ├── TODO-001-MAESTRO.md   ← PROBLEMAS PENDIENTES (leer primero)
│   │   ├── estado.md             ← Qué está en desarrollo
│   │   ├── BITACORA.md           ← Historial de cambios
│   │   ├── PLAN-CONSTRUCCION.md  ← Hitos y cronograma
│   │   └── ...
│   ├── INDICE-MODULOS.md         ← Lista de módulos
│   ├── INDICE-DOCUMENTACION.md   ← Lista de documentos
│   └── FLUJOS-MERMAID/           ← Diagramas
├── modules/
│   ├── registry.json             ← Registro automático de módulos
│   ├── cognitive-need-detector/  ← Orquestador cognitivo
│   ├── mode-transition-engine/   ← Transiciones suaves
│   ├── questionnaire-engine/     ← Motor de preguntas
│   └── ...
├── apps/
│   ├── server/                   ← Backend Node.js + Socket.IO
│   └── web/                      ← Frontend Next.js
└── herramientas/
    └── agente-de-cambio.sh       ← Wrapper bash
```

---

## 🧠 FILOSOFÍA (NO NEGOCIABLE)

| Principio | Aplicación |
|-----------|------------|
| **Google Lens** | Herramienta desaparece, queda resultado |
| **Pragmatismo radical** | Navaja suiza, no catedral |
| **No sobra ni falta nada** | Utilidad/esfuerzo > elegancia |
| **Conducción, no chat** | Conversación → Decisión → Acción |
| **Modularidad atómica** | Máx 3 funciones por módulo |
| **Documentación viva** | BITACORA.md actualizado siempre |

---

## 🐛 PROBLEMAS CONOCIDOS (VER TODO-001)

### Crítico: LLM Responde con JSON

**Síntoma:** El LLM (DeepSeek) responde con formato JSON en lugar de usar lenguaje natural.

**Estado:** PENDIENTE DE SOLUCIÓN

**Archivos involucrados:**
- `/modules/prompt-engine/templates/system-master-prompt.ts`
- `/apps/server/src/orchestrator-handler.ts`
- `/apps/web/components/chat/QuestionContainer.tsx`

**Ver detalles completos:** [`/docs/CLAVE/TODO-001-MAESTRO.md`](./docs/CLAVE/TODO-001-MAESTRO-20260320-1900.md)

---

## 📊 ESTADO ACTUAL (RESUMEN)

| Métrica | Valor |
|---------|-------|
| **Módulos completados** | 8/12 |
| **Viewers implementados** | 8/8 |
| **Orquestador cognitivo** | ✅ Integrado |
| **Funciona standalone** | ✅ |
| **Funciona con ARES** | ❌ (Hito 5) |
| **Documentación actualizada** | ✅ |
| **Scroll unificado** | ✅ |
| **Botón RESET** | ✅ |
| **Bitácora de cambios** | ✅ |

**Ver estado completo:** [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md)

---

## 🔗 ENLACES RÁPIDOS

| Tipo | Enlace |
|------|--------|
| **Agenda del Sistema** | [`/docs/CLAVE/TODO-001-MAESTRO.md`](./docs/CLAVE/TODO-001-MAESTRO-20260320-1900.md) |
| **Índice de Módulos** | [`/docs/INDICE-MODULOS.md`](./docs/INDICE-MODULOS.md) |
| **Índice de Documentación** | [`/docs/INDICE-DOCUMENTACION.md`](./docs/INDICE-DOCUMENTACION.md) |
| **Índice Maestro TR-ARES** | [`INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md) |
| **Estado Actual** | [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md) |
| **Bitácora** | [`/docs/CLAVE/BITACORA.md`](./docs/CLAVE/BITACORA.md) |
| **Registry Módulos** | [`/modules/registry.json`](./modules/registry.json) |
| **Memoria TR-ARES** | [`~/.qwen/QWEN.md`](file:///home/daniel/.qwen/QWEN.md) |

---

## 🎯 PRÓXIMO PASO INMEDIATO

**Resolver problema del JSON** (TODO-001)

1. Leer [`/docs/CLAVE/TODO-001-MAESTRO.md`](./docs/CLAVE/TODO-001-MAESTRO-20260320-1900.md)
2. Entender intentos fallidos (1-4)
3. Probar soluciones propuestas (5-8)
4. Documentar en `BITACORA.md`
5. Actualizar TODO-001 con estado

---

**¿Primera vez aquí?** → Leer [`TODO-001-MAESTRO.md`](./docs/CLAVE/TODO-001-MAESTRO-20260320-1900.md) para problemas pendientes y [`INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md) para arquitectura.

**¿Ya conoces el sistema?** → Ir directamente a [`INDICE-MODULOS.md`](./docs/INDICE-MODULOS.md) para modificar módulos o [`INDICE-DOCUMENTACION.md`](./docs/INDICE-DOCUMENTACION.md) para leer documentación.

---

*Fin de LEEME.md - Resumen de 1 página + procedimientos*

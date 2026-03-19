# 📋 PLAN DE CONSTRUCCIÓN INTEGRAL - AGENTE DE CAMBIO ESTABLE

> **Documento Maestro de Implementación**  
> **Versión:** 1.0 - 2026-03-19  
> **Estado:** Planificación → Ejecución  
> **Ubicación:** `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/docs/CLAVE/PLAN-CONSTRUCCION.md`

---

## 🎯 PROPÓSITO DE ESTE DOCUMENTO

Este documento **NO es opcional**. Es el **plan de batalla** que garantiza:

1. **Respeto por lo existente** - Todo código funcional se preserva
2. **Integración metodológica** - TR-ARES + AgenteDeCambio sin colisiones
3. **Hitos revisables** - Cada fase puede ser validada por el usuario
4. **Control de entropía** - Git backup antes de cada cambio
5. **Standalone + ARES** - Funciona solo O invocado por ARES

---

## 📊 ESTADO ACTUAL (Línea Base - 2026-03-19)

### ✅ LO QUE YA FUNCIONA (NO TOCAR SIN JUSTIFICACIÓN)

| Componente | Estado | Ubicación | Validado |
|------------|--------|-----------|----------|
| **DeepSeek Connector** | ✅ Completado | `modules/deepseek-connector/` | Streaming SSE funcional |
| **Session Manager** | ✅ Completado | `modules/session-manager/` | Memoria + persistencia |
| **Prompt Engine** | ✅ Completado | `modules/prompt-engine/` | Construcción dinámica |
| **Delta Calculator** | ✅ Completado | `modules/delta-calculator/` | Cálculo de deriva |
| **Shared Types** | ✅ Completado | `modules/shared-types/` | Tipos TypeScript |
| **Server Index** | ✅ Funcional | `apps/server/src/index.ts` | Socket.IO + Express |
| **Componentes Web** | ✅ Maquetados | `apps/web/components/` | Chat, Input, Message, Questionnaire |
| **Monorepo** | ✅ Configurado | `package.json` | Workspaces npm |

### ⚠️ LO QUE EXISTE PERO ESTÁ INCOMPLETO

| Componente | Estado | Qué falta | Prioridad |
|------------|--------|-----------|-----------|
| **Socket Server** | ⚠️ Pendiente | `modules/socket-server/` - Handlers modulares | ALTA |
| **State Manager** | ⚠️ Pendiente | `modules/state-manager/` - Zustand store | ALTA |
| **Questionnaire Module** | ❌ No existe | `modules/questionnaire-engine/` | CRÍTICA (Hito 1) |
| **Quiz Engine** | ❌ No existe | `modules/quiz-engine/` | CRÍTICA (Hito 1) |
| **Stall Signals** | ❌ No existe | `modules/stall-detector/` | MEDIA (Hito 2) |
| **Objectives Manager** | ❌ No existe | `modules/objectives-manager/` | ALTA (Hito 2) |
| **Architect Layer** | ❌ No existe | `modules/architect/` | MEDIA (Hito 3) |

### ❌ LO QUE NO EXISTE (NUEVO)

| Módulo | Propósito | Hito |
|--------|-----------|------|
| `questionnaire-engine` | Motor de preguntas dinámicas | 1 |
| `quiz-engine` | Banco de cuestionarios por dominio | 1 |
| `objectives-manager` | Memoria permanente EMT | 2 |
| `stall-detector` | 12 señales de estancamiento | 2 |
| `architect` | Capa de control de deriva | 3 |
| `biological-profile` | Perfil fisiológico usuario | 3 |
| `evidence-tracker` | Registro de evidencias | 4 |

---

## 🏗️ METODOLOGÍA DE IMPLEMENTACIÓN

### Principios Rectores

```
1. GIT BACKUP PRIMERO → Antes de editar, commit con fecha/hora
2. INDEX.MD ACTUALIZADO → Cada módulo con su INDEX.md <50 líneas
3. MANIFEST.JSON → Metadatos para IAs (aiReady: true/false)
4. MÁXIMO 3 FUNCIONES → Por módulo (regla TR-ARES)
5. GIT DIFF DESPUÉS → Validar cambios exactos
6. DOCUMENTACIÓN VIVA → README apunta a docs CLAVE
```

### Protocolo de Backup Git

```bash
# Antes de CUALQUIER modificación:
git add .
git commit -m "BACKUP $(date '+%Y-%m-%d_%H-%M-%S') - Pre-[nombre-cambio]"
git tag "backup-$(date '+%Y%m%d-%H%M%S')"

# Después de cada cambio:
git diff --stat
git diff HEAD~1
git commit -m "[MÓDULO] Descripción del cambio + referencia a índice"
```

---

## 📅 HITOS REVISABLES

### **HITO 1: MOTOR DE CUESTIONARIOS Y QUIZ** (SEMANAS 1-2)

> **CRITERIO DE ACEPTACIÓN:** El sistema puede generar preguntas dinámicas basadas en el dominio del usuario y recibir respuestas estructuradas.

#### Tareas del Hito 1

| ID | Tarea | Módulo | Estado | Backup Git | Validación |
|----|-------|--------|--------|------------|------------|
| 1.1 | Crear `modules/questionnaire-engine/` | Nuevo | ❌ Pendiente | `backup-antes-questionnaire` | INDEX.md + actions.ts |
| 1.2 | Crear `modules/quiz-engine/` | Nuevo | ❌ Pendiente | `backup-antes-quiz` | Banco de plantillas |
| 1.3 | Crear `modules/question-types/` | Nuevo | ❌ Pendiente | `backup-antes-types` | Tipos de pregunta |
| 1.4 | Actualizar `registry.json` | Existente | ⚠️ Pendiente | `backup-antes-registry-update` | 3 nuevos módulos |
| 1.5 | Integrar con Socket.IO | `sockets/` | ⚠️ Pendiente | `backup-antes-socket-integration` | Eventos questionnaire |
| 1.6 | Actualizar `Questionnaire.tsx` | Existente | ⚠️ Pendiente | `backup-antes-questionnaire-ui` | Render dinámico |
| 1.7 | Documentar en INDEX.md cada módulo | Nuevo | ❌ Pendiente | N/A | <50 líneas cada uno |
| 1.8 | Tests del módulo | `modules/*/test/` | ❌ Pendiente | N/A | Vitest passing |

**Documentación de Referencia del Hito 1:**
- → `/docs/CLAVE/ListaRequerimientos.md` → Punto 6 (Interfaz Híbrida)
- → `/docs/CLAVE/proyecto.md` → Fase 1-2 (Ubicación y Modelado)
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md` → Capa 2.2, 3.2
- → `/docs/CLAVE/METODOLOGIA-MODULAR.md` → Patrones 1, 2, 5

**Entregables del Hito 1:**
```
modules/
├── questionnaire-engine/
│   ├── INDEX.md
│   ├── actions.ts         # generateQuestion(), parseAnswer(), validateSchema()
│   ├── manifest.json
│   └── test/
├── quiz-engine/
│   ├── INDEX.md
│   ├── actions.ts         # getQuizByDomain(), getNextQuestion(), scoreAnswers()
│   ├── templates/         # Por dominio (cura, constructor, estudiante...)
│   ├── manifest.json
│   └── test/
└── question-types/
    ├── INDEX.md
    ├── types.ts           # YesNo, SingleChoice, MultiChoice, Completion, Multiline
    ├── manifest.json
    └── validators.ts
```

**Comando de Validación del Hito 1:**
```bash
# Verificar que los módulos existen
ls -la modules/questionnaire-engine/
ls -la modules/quiz-engine/
ls -la modules/question-types/

# Verificar INDEX.md
wc -l modules/*/INDEX.md  # Debe ser <50 líneas cada uno

# Ejecutar tests
cd modules/questionnaire-engine && npm test
cd modules/quiz-engine && npm test

# Git diff para validar cambios
git diff backup-antes-questionnaire HEAD
```

---

### **HITO 2: MEMORIA DE OBJETIVOS Y DETECCIÓN DE ESTANCAMIENTO** (SEMANAS 3-4)

> **CRITERIO DE ACEPTACIÓN:** El sistema guarda objetivos EMT y detecta automáticamente 12 señales de estancamiento.

#### Tareas del Hito 2

| ID | Tarea | Módulo | Estado | Backup Git | Validación |
|----|-------|--------|--------|------------|------------|
| 2.1 | Crear `modules/objectives-manager/` | Nuevo | ❌ Pendiente | `backup-antes-objectives` | EMT extraction |
| 2.2 | Crear `modules/stall-detector/` | Nuevo | ❌ Pendiente | `backup-antes-stall` | 12 señales |
| 2.3 | Crear `modules/stall-intervention/` | Nuevo | ❌ Pendiente | `backup-antes-intervention` | 3 terapias |
| 2.4 | Actualizar `session-manager` | Existente | ⚠️ Pendiente | `backup-antes-session-update` | Objetivos en sesión |
| 2.5 | Actualizar `prompt-engine` | Existente | ⚠️ Pendiente | `backup-antes-prompt-update` | Inyección de objetivos |
| 2.6 | Crear endpoints REST | `apps/server/src/services/` | ❌ Pendiente | `backup-antes-endpoints` | CRUD objetivos |
| 2.7 | UI Panel de Objetivos | `apps/web/components/objectives/` | ⚠️ Pendiente | `backup-antes-objectives-ui` | Editor EMT |
| 2.8 | Documentar | INDEX.md | ❌ Pendiente | N/A | <50 líneas |

**Documentación de Referencia del Hito 2:**
- → `/docs/CLAVE/ListaRequerimientos.md` → Punto 7 (Memoria Permanente), Punto 5 (Negociación)
- → `/docs/CLAVE/ListaRequerimientos.md` → Punto 12 (Métrica Deltas)
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md` → Sección 4 (Estado de Éxito), Sección 5 (Estancamiento)
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md` → Capa 2.2, 2.3, 4.1, 4.2

**Entregables del Hito 2:**
```
modules/
├── objectives-manager/
│   ├── INDEX.md
│   ├── actions.ts         # extractEMT(), saveObjective(), getActiveObjectives()
│   ├── types.ts           # Objective, EMT, SuccessCriteria
│   ├── manifest.json
│   └── test/
├── stall-detector/
│   ├── INDEX.md
│   ├── actions.ts         # detectStall(), calculateSignals(), getThresholds()
│   ├── signals.ts         # S01-S12 definiciones
│   ├── manifest.json
│   └── test/
└── stall-intervention/
    ├── INDEX.md
    ├── actions.ts         # intervene(), applyTherapies(), escalateLevel()
    ├── therapies.ts       # Conductista, Cognitiva, Humanista
    ├── manifest.json
    └── test/
```

**Comando de Validación del Hito 2:**
```bash
# Verificar señales de estancamiento
grep -r "S01\|S02\|S03" modules/stall-detector/  # Debe encontrar las 12

# Verificar EMT
grep -r "evidence.*metric.*time" modules/objectives-manager/

# Ejecutar tests
npm test --workspace=modules/objectives-manager
npm test --workspace=modules/stall-detector

# Git diff
git diff backup-antes-objectives HEAD
```

---

### **HITO 3: CAPA DE ARQUITECTO Y CONTROL DE DERIVA** (SEMANAS 5-6)

> **CRITERIO DE ACEPTACIÓN:** El sistema tiene doble instancia (Ejecutor + Arquitecto) y veta cambios bruscos del prompt.

#### Tareas del Hito 3

| ID | Tarea | Módulo | Estado | Backup Git | Validación |
|----|-------|--------|--------|------------|------------|
| 3.1 | Crear `modules/architect/` | Nuevo | ❌ Pendiente | `backup-antes-architect` | Filtro merecimiento |
| 3.2 | Actualizar `delta-calculator` | Existente | ⚠️ Pendiente | `backup-antes-delta-update` | Algoritmo semántico |
| 3.3 | Crear `modules/prompt-negotiation/` | Nuevo | ❌ Pendiente | `backup-antes-negotiation` | Negociación usuario |
| 3.4 | Actualizar `socket-server` | `sockets/` | ⚠️ Pendiente | `backup-antes-architect-socket` | Eventos arquitecto |
| 3.5 | UI Delta Meter avanzado | `apps/web/components/metrics/` | ⚠️ Pendiente | `backup-antes-delta-ui` | Visual 0-1 |
| 3.6 | UI Aprobación de cambios | `apps/web/components/prompt/` | ⚠️ Pendiente | `backup-antes-approval-ui` | Modal negociación |
| 3.7 | Documentar | INDEX.md | ❌ Pendiente | N/A | <50 líneas |

**Documentación de Referencia del Hito 3:**
- → `/docs/CLAVE/ListaRequerimientos.md` → Punto 8 (Doble Instancia)
- → `/docs/CLAVE/ListaRequerimientos.md` → Punto 4 (Prompt Vivo)
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md` → Sección 6 (Gobernanza)
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md` → Capa 1.2, 1.3, 4.1, 4.2

**Entregables del Hito 3:**
```
modules/
├── architect/
│   ├── INDEX.md
│   ├── actions.ts         # evaluateChange(), filterMerecimiento(), vetoBruscoChange()
│   ├── merecimiento.ts    # Criterios de merecimiento
│   ├── manifest.json
│   └── test/
├── prompt-negotiation/
│   ├── INDEX.md
│   ├── actions.ts         # negotiateWithUser(), getUserApproval(), applyChange()
│   ├── manifest.json
│   └── test/
└── delta-calculator/     # ACTUALIZACIÓN
    ├── actions.ts        # Nuevo algoritmo semántico (embeddings)
    └── test/
```

**Comando de Validación del Hito 3:**
```bash
# Verificar filtro de merecimiento
grep -r "merecimiento\|alineacion.*objetivo" modules/architect/

# Verificar cálculo semántico de delta
grep -r "cosine_similarity\|embedding" modules/delta-calculator/

# Git diff
git diff backup-antes-architect HEAD
```

---

### **HITO 4: PERFIL BIOLÓGICO Y ADAPTACIÓN FISIOLÓGICA** (SEMANAS 7-8)

> **CRITERIO DE ACEPTACIÓN:** El sistema adapta las acciones obligatorias al cronotipo, sueño y estrés del usuario.

#### Tareas del Hito 4

| ID | Tarea | Módulo | Estado | Backup Git | Validación |
|----|-------|--------|--------|------------|------------|
| 4.1 | Crear `modules/biological-profile/` | Nuevo | ❌ Pendiente | `backup-antes-biological` | Cuestionario inicial |
| 4.2 | Crear `modules/scheduling-adapter/` | Nuevo | ❌ Pendiente | `backup-antes-scheduling` | Algoritmo de scheduling |
| 4.3 | Actualizar `questionnaire-engine` | Existente | ⚠️ Pendiente | `backup-antes-bio-quiz` | Preguntas biológicas |
| 4.4 | UI Perfil Biológico | `apps/web/components/profile/` | ❌ Pendiente | `backup-antes-bio-ui` | Formulario |
| 4.5 | Documentar | INDEX.md | ❌ Pendiente | N/A | <50 líneas |

**Documentación de Referencia del Hito 4:**
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md` → Sección 7, Subsección 4 (Componente Biológico)
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md` → Capa 5.4

**Entregables del Hito 4:**
```
modules/
├── biological-profile/
│   ├── INDEX.md
│   ├── actions.ts         # getProfile(), updateProfile(), assessChronotype()
│   ├── questionnaire.ts   # Preguntas de perfil
│   ├── manifest.json
│   └── test/
└── scheduling-adapter/
    ├── INDEX.md
    ├── actions.ts         # scheduleByProfile(), adjustForStress(), peakHoursOnly()
    ├── manifest.json
    └── test/
```

---

### **HITO 5: INTEGRACIÓN TR-ARES Y MODO STANDALONE** (SEMANA 9)

> **CRITERIO DE ACEPTACIÓN:** El agente funciona con `ares agente-de-cambio` O `npm run dev` (standalone).

#### Tareas del Hito 5

| ID | Tarea | Módulo | Estado | Backup Git | Validación |
|----|-------|--------|--------|------------|------------|
| 5.1 | Crear wrapper CLI `ares` | `herramientas/` | ❌ Pendiente | `backup-antes-ares-wrapper` | Comando ares |
| 5.2 | Crear `modules/ares-bridge/` | Nuevo | ❌ Pendiente | `backup-antes-bridge` | Puente ARES |
| 5.3 | Actualizar `package.json` | Existente | ⚠️ Pendiente | `backup-antes-package` | Scripts + bin |
| 5.4 | Crear `.env` template | Nuevo | ❌ Pendiente | `backup-antes-env` | Variables |
| 5.5 | Documentar modo standalone | README.md | ⚠️ Pendiente | `backup-antes-readme-standalone` | Instrucciones |
| 5.6 | Documentar modo ARES | README.md | ⚠️ Pendiente | `backup-antes-readme-ares` | Instrucciones |

**Documentación de Referencia del Hito 5:**
- → `/home/daniel/tron/programas/TR/programas/a-DIRECTORIO/generador-de-lanzadores-python-encapsulados/ini` → Comando `ini`
- → `/home/daniel/.qwen/QWEN.md` → Herramientas TRON (INI v3.0)

**Entregables del Hito 5:**
```
herramientas/
├── ares-agentedecambio.sh   # Wrapper bash para ARES
└── standalone-runner.sh     # Ejecución standalone

modules/
└── ares-bridge/
    ├── INDEX.md
    ├── actions.ts           # receivePromptFromAres(), sendResultToAres()
    ├── manifest.json
    └── test/
```

**Comandos de Validación del Hito 5:**
```bash
# Modo standalone
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
npm run dev

# Modo ARES (desde TR)
ares agente-de-cambio --prompt "Ayuda a este usuario con su objetivo EMT"

# Verificar wrapper
ls -la herramientas/*.sh
```

---

### **HITO 6: DOCUMENTACIÓN UNIFICADA Y README MAESTRO** (SEMANA 10)

> **CRITERIO DE ACEPTACIÓN:** README.md apunta a TODA la documentación clave y está actualizado.

#### Tareas del Hito 6

| ID | Tarea | Archivo | Estado | Backup Git | Validación |
|----|-------|--------|--------|------------|------------|
| 6.1 | Actualizar README.md | `/README.md` | ❌ Pendiente | `backup-antes-readme-master` | Apunta a docs CLAVE |
| 6.2 | Crear índice unificado | `/docs/CLAVE/INDICE-UNIFICADO.md` | ❌ Pendiente | `backup-antes-indice` | Todos los docs |
| 6.3 | Vincular con TR-ARES | `/home/daniel/tron/programas/TR/docs/` | ❌ Pendiente | `backup-antes-tr-link` | Cross-referencing |
| 6.4 | Actualizar estado.md | `/docs/CLAVE/estado.md` | ⚠️ Pendiente | `backup-antes-estado` | Estado real |
| 6.5 | Crear LEEME.md raíz | `/LEEME.md` | ❌ Pendiente | `backup-antes-leeme` | Resumen 1 página |

**Documentación de Referencia del Hito 6:**
- → Todos los documentos en `/docs/CLAVE/`
- → `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md`

**Entregables del Hito 6:**
```
/
├── README.md              # ACTUALIZADO - Apunta a docs CLAVE
├── LEEME.md               # NUEVO - Resumen 1 página
└── docs/
    └── CLAVE/
        ├── INDICE-UNIFICADO.md  # NUEVO - Todos los docs interconectados
        └── estado.md            # ACTUALIZADO - Estado real post-hitoss
```

---

## 📊 MATRIZ DE TRAZABILIDAD

| Requerimiento Original | Documento Referencia | Hito | Módulo | Estado |
|------------------------|---------------------|------|--------|--------|
| Interfaz Híbrida (botones+comentario) | `ListaRequerimientos.md` Punto 6 | 1 | `questionnaire-engine` | ❌ |
| Memoria Permanente de Objetivos | `ListaRequerimientos.md` Punto 7 | 2 | `objectives-manager` | ❌ |
| Sistema de Doble Instancia | `ListaRequerimientos.md` Punto 8 | 3 | `architect` | ❌ |
| Métrica de Deriva (Deltas) | `ListaRequerimientos.md` Punto 12 | 3 | `delta-calculator` (update) | ⚠️ |
| 12 Señales de Estancamiento | `requerimientos.md` Sección 5 | 2 | `stall-detector` | ❌ |
| 3 Terapias Simultáneas | `requerimientos.md` Sección 5.4 | 2 | `stall-intervention` | ❌ |
| Perfil Biológico | `requerimientos.md` Sección 7.4 | 4 | `biological-profile` | ❌ |
| Modo Standalone + ARES | `QWEN.md` Herramientas | 5 | `ares-bridge` | ❌ |

---

## 🔧 COMANDOS GIT PARA CONTROL DE CAMBIOS

### Antes de Cada Hito

```bash
# Crear rama del hito
git checkout -b hito-[N]-[nombre]

# Tag de backup inicial
git tag "hito-[N]-inicio-$(date '+%Y%m%d-%H%M%S')"
```

### Durante Cada Hito (Cada Commit)

```bash
# Commit atómico
git add modules/[nombre-modulo]/
git commit -m "[HITO N] [MÓDULO] Descripción + referencia a índice"

# Ejemplo:
git commit -m "[HITO 1] [questionnaire-engine] Crear motor de preguntas dinámicas → INDICE-MAESTRO 2.2"
```

### Después de Cada Hito

```bash
# Validar cambios
git diff hito-[N]-inicio HEAD --stat

# Verificar archivos modificados
git diff --name-only hito-[N]-inicio HEAD

# Tag de completion
git tag "hito-[N]-completado-$(date '+%Y%m%d-%H%M%S')"

# Merge a main
git checkout main
git merge hito-[N]-[nombre]
```

### Validación Específica por Hito

```bash
# Hito 1: Verificar módulos de cuestionarios
ls -la modules/questionnaire-engine/modules/quiz-engine/modules/question-types/ && \
wc -l modules/*/INDEX.md | grep -E "^[0-9]+ modules/(questionnaire|quiz|question)" && \
echo "Hito 1: Módulos creados con INDEX.md <50 líneas"

# Hito 2: Verificar señales de estancamiento
grep -r "signal_code.*S0[1-9]\|S1[0-2]" modules/stall-detector/ && \
echo "Hito 2: 12 señales implementadas"

# Hito 3: Verificar filtro de merecimiento
grep -r "merecimiento\|alineacion.*objetivo" modules/architect/ && \
echo "Hito 3: Arquitecto con filtro de merecimiento"

# Hito 4: Verificar perfil biológico
grep -r "chronotype\|peak_hours\|sleep_average" modules/biological-profile/ && \
echo "Hito 4: Perfil biológico implementado"

# Hito 5: Verificar wrappers
test -f herramientas/ares-agentedecambio.sh && test -f herramientas/standalone-runner.sh && \
echo "Hito 5: Wrappers CLI creados"

# Hito 6: Verificar README
grep -q "docs/CLAVE" README.md && grep -q "INDICE-MAESTRO-PARA-IAS" README.md && \
echo "Hito 6: README actualizado con referencias"
```

---

## 📈 MÉTRICAS DE ÉXITO DEL PLAN

| Métrica | Línea Base | Meta Hito 6 | Cómo Medir |
|---------|------------|-------------|------------|
| **Módulos completados** | 5/12 | 12/12 | `ls -d modules/*/ | wc -l` |
| **INDEX.md <50 líneas** | 5/5 | 12/12 | `wc -l modules/*/INDEX.md` |
| **Tests passing** | 0% | 100% | `npm test` |
| **Documentación actualizada** | 1/7 | 7/7 | `ls docs/CLAVE/*.md` |
| **Funciona standalone** | ❌ | ✅ | `npm run dev` |
| **Funciona con ARES** | ❌ | ✅ | `ares agente-de-cambio` |
| **Git tags de backup** | 0 | 30+ | `git tag -l "backup-*"` |

---

## 🎯 PRÓXIMO PASO INMEDIATO

**COMENZAR HITO 1:**

```bash
# 1. Crear backup inicial
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
git add .
git commit -m "BACKUP $(date '+%Y-%m-%d_%H-%M-%S') - Pre-Hito1-Questionnaire"
git tag "backup-$(date '+%Y%m%d-%H%M%S')"

# 2. Crear rama del hito
git checkout -b hito-1-questionnaire

# 3. Crear estructura de carpetas
mkdir -p modules/questionnaire-engine/test
mkdir -p modules/quiz-engine/templates
mkdir -p modules/question-types/test

# 4. Comenzar implementación (ver tareas 1.1-1.8)
```

---

## 📚 DOCUMENTOS CLAVE DE REFERENCIA

### Internos (AgenteDeCambio-Estable)

| Documento | Ruta | Propósito |
|-----------|------|-----------|
| **ListaRequerimientos.md** | `/docs/CLAVE/ListaRequerimientos.md` | 27 principios filosóficos |
| **proyecto.md** | `/docs/CLAVE/proyecto.md` | Arquitectura y etapas |
| **METODOLOGIA-MODULAR.md** | `/docs/CLAVE/METODOLOGIA-MODULAR.md` | Patrones arquitectónicos |
| **Maestro.md** | `/docs/CLAVE/Maestro.md` | Diseño de interfaz |
| **sistema-por-kimi.md** | `/docs/CLAVE/sistema-por-kimi.md` | Diseño detallado |
| **estado.md** | `/docs/CLAVE/estado.md` | Estado actual |
| **rutas.md** | `/docs/rutas.md` | Rutas de archivos |

### Externos (TR-ARES)

| Documento | Ruta | Propósito |
|-----------|------|-----------|
| **INDICE-MAESTRO-PARA-IAS.md** | `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/` | Índice temático descriptivo |
| **requerimientos.md** | `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/` | Análisis profundo de intenciones |
| **QWEN.md** | `/home/daniel/.qwen/QWEN.md` | Memoria compartida TR-ARES |
| **INI v3.0** | `/usr/bin/ini` | Gestor de ciclo de vida |

---

## ✅ CHECKLIST DE VALIDACIÓN PRE-COMMIT

Antes de hacer commit de cualquier cambio:

```
□ 1. ¿Hice backup git con fecha/hora?
□ 2. ¿El cambio respeta la filosofía Google Lens?
□ 3. ¿El módulo tiene INDEX.md <50 líneas?
□ 4. ¿El módulo tiene manifest.json?
□ 5. ¿El módulo tiene máximo 3 funciones?
□ 6. ¿Actualicé registry.json?
□ 7. ¿Los tests passing?
□ 8. ¿Git diff muestra solo lo esperado?
□ 9. ¿Referencié el índice en el commit?
□ 10. ¿Notifiqué al usuario para revisión del hito?
```

---

**Documento creado:** 2026-03-19  
**Próxima revisión:** Después de cada hito completado  
**Responsable de validación:** Usuario (Daniel)  
**Ubicación:** `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/docs/CLAVE/PLAN-CONSTRUCCION.md`

---

*Fin del Plan de Construcción Integral*

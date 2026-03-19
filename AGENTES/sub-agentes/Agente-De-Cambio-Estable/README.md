# 🧠 Agente de Cambio - Sistema Cognitivo de Extracción

> **Sistema de conducción cognitiva con control de deriva y memoria de propósito**  
> **Modo:** Standalone (`npm run dev`) | Invocado por ARES (`ares agente-de-cambio`)

Sistema de interacción conversacional adaptativa con prompts vivos y métricas de deriva, diseñado para extracción cognitiva de alto nivel y conducción estratégica del usuario hacia sus objetivos.

## ✨ Características Principales

- **Prompt Vivo y Mutante**: System prompt editable en tiempo real con algoritmos de negociación
- **Interfaz Híbrida**: Modo chat fluido y modo cuestionario estructurado
- **Glassmorphism Premium**: Diseño visual con animaciones fluidas (Framer Motion)
- **Streaming en Tiempo Real**: Respuestas carácter por carácter via Socket.IO
- **Métricas de Deriva**: Visualización de cambios en el prompt con umbrales de aprobación
- **Arquitectura de Doble Instancia**: Separación entre ejecutor (DeepSeek) y arquitecto (control de prompt)
- **Persistencia de Objetivos**: Memoria permanente de metas y objetivos de sesión

## 🏗️ Arquitectura Tecnológica

- **Frontend**: Next.js 14 (App Router) + React 18 + TypeScript + Tailwind CSS + Framer Motion
- **Backend**: Node.js + Express + Socket.IO + DeepSeek API
- **Estado**: Zustand con persistencia local
- **Estilo**: Glassmorphism, animaciones con spring physics, microinteracciones
- **Despliegue**: Monorepo con npm workspaces

---

## 📚 DOCUMENTACIÓN CLAVE (LEER PRIMERO)

> **⚠️ IMPORTANTE:** Este README es solo una introducción. La documentación completa está en los siguientes archivos:

### Documentación Fundamental (Obligatoria)

| Documento | Ruta | Propósito | Prioridad |
|-----------|------|-----------|-----------|
| **📋 PLAN DE CONSTRUCCIÓN** | [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md) | **Plan de batalla con hitos revisables** | 🔴 CRÍTICA |
| **📘 ÍNDICE MAESTRO PARA IAs** | [`/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md) | **Brújula arquitectónica para IAs** | 🔴 CRÍTICA |
| **27 Requerimientos** | [`/docs/CLAVE/ListaRequerimientos.md`](./docs/CLAVE/ListaRequerimientos.md) | Filosofía Google Lens + principios | 🔴 CRÍTICA |
| **Análisis de Intenciones** | [`/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md) | Qué es realmente el sistema | 🔴 CRÍTICA |
| **Proyecto (Arquitectura)** | [`/docs/CLAVE/proyecto.md`](./docs/CLAVE/proyecto.md) | Etapas y arquitectura completa | 🟡 ALTA |
| **Metodología Modular** | [`/docs/CLAVE/METODOLOGIA-MODULAR.md`](./docs/CLAVE/METODOLOGIA-MODULAR.md) | Patrones arquitectónicos 2024-2026 | 🟡 ALTA |
| **Estado Actual** | [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md) | Qué está completo/en progreso | 🟡 ALTA |
| **Diseño de Interfaz** | [`/docs/CLAVE/Maestro.md`](./docs/CLAVE/Maestro.md) | Sistema de coordenadas UI | 🟢 MEDIA |

### Documentación Complementaria

| Documento | Ruta |
|-----------|------|
| **Rutas de Archivos** | [`/docs/rutas.md`](./docs/rutas.md) |
| **API DeepSeek** | [`/docs/Apideepseek.md`](./docs/Apideepseek.md) |
| **Sistema por Kimi** | [`/docs/CLAVE/sistema-por-kimi.md`](./docs/CLAVE/sistema-por-kimi.md) |
| **Resumen Ejecutivo** | [`/docs/RESUMEN-EJECUTIVO.md`](./docs/RESUMEN-EJECUTIVO.md) |
| **Auditoría de Capacidades** | [`/docs/AUDITORIA-CAPACIDADES.md`](./docs/AUDITORIA-CAPACIDADES.md) |

### Memoria Compartida TR-ARES

| Documento | Ruta |
|-----------|------|
| **QWEN.md (Memoria)** | [`~/.qwen/QWEN.md`](file:///home/daniel/.qwen/QWEN.md) |
| **INI v3.0 (Herramienta)** | [`/usr/bin/ini`](file:///usr/bin/ini) |

---

## 🚀 INICIO RÁPIDO

### Opción A: Modo Standalone (Recomendado para Desarrollo)

```bash
# 1. Ir al directorio del agente
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable

# 2. Instalar dependencias (usar legacy-peer-deps)
npm install --legacy-peer-deps

# 3. Configurar variables de entorno
cp apps/server/.env.example apps/server/.env
# Editar apps/server/.env con tu API Key de DeepSeek

# 4. Iniciar ambos servidores (frontend + backend)
npm run dev

# 5. Acceder a la interfaz
# Frontend: http://localhost:3000
# Backend:  http://localhost:3001
```

### Opción B: Invocado por ARES (Producción)

```bash
# ARES invoca el agente con un prompt específico
ares agente-de-cambio --prompt "Ayuda a este usuario con su objetivo EMT"

# El agente funciona como herramienta de ARES
# ARES puede pasar contexto, objetivos, historial
```

### Variables de Entorno Requeridas

**Backend (`apps/server/.env`):**
```env
DEEPSEEK_API_KEY=sk-tu-api-key-aqui
PORT=3001
NODE_ENV=development
CLIENT_URL=http://localhost:3000
PROMPT_DELTA_THRESHOLD=0.3
```

**Frontend (`apps/web/.env.local`):**
```env
NEXT_PUBLIC_SOCKET_URL=http://localhost:3001
NEXT_PUBLIC_API_URL=http://localhost:3001/api
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 📦 ESTRUCTURA DEL PROYECTO

```
Agente-De-Cambio-Estable/
├── apps/
│   ├── web/                    # Frontend Next.js 14
│   │   ├── app/               # App Router
│   │   ├── components/        # Componentes React
│   │   ├── store/             # Zustand stores
│   │   └── .env.local         # Variables frontend
│   └── server/                # Backend Node.js
│       ├── src/
│       │   ├── clients/       # DeepSeek API client
│       │   ├── sockets/       # Socket.IO handlers
│       │   ├── services/      # Lógica de negocio
│       │   └── types/         # Tipos TypeScript
│       └── .env               # Variables backend
├── modules/                   # Módulos (metodología modular)
│   ├── deepseek-connector/    # ✅ Completado
│   ├── session-manager/       # ✅ Completado
│   ├── prompt-engine/         # ✅ Completado
│   ├── delta-calculator/      # ✅ Completado
│   ├── shared-types/          # ✅ Completado
│   ├── socket-server/         # ⚠️ Pendiente
│   ├── state-manager/         # ⚠️ Pendiente
│   ├── questionnaire-engine/  # ❌ Hito 1
│   ├── quiz-engine/           # ❌ Hito 1
│   ├── objectives-manager/    # ❌ Hito 2
│   ├── stall-detector/        # ❌ Hito 2
│   ├── architect/             # ❌ Hito 3
│   └── biological-profile/    # ❌ Hito 4
├── docs/
│   └── CLAVE/                 # Documentación fundamental
│       ├── PLAN-CONSTRUCCION.md    # Plan de batalla
│       ├── ListaRequerimientos.md  # 27 principios
│       ├── proyecto.md             # Arquitectura
│       ├── METODOLOGIA-MODULAR.md  # Patrones
│       ├── estado.md               # Estado actual
│       └── Maestro.md              # Diseño UI
├── herramientas/              # Wrappers CLI
│   ├── ares-agentedecambio.sh  # Wrapper para ARES
│   └── standalone-runner.sh    # Ejecución standalone
├── package.json             # Monorepo config
└── README.md                # Este archivo
```

---

## 🎯 HITOS DE IMPLEMENTACIÓN

| Hito | Nombre | Semanas | Estado | Criterio de Aceptación |
|------|--------|---------|--------|------------------------|
| **1** | Motor de Cuestionarios y Quiz | 1-2 | ❌ Pendiente | Genera preguntas dinámicas por dominio |
| **2** | Memoria de Objetivos + Estancamiento | 3-4 | ❌ Pendiente | Guarda EMT y detecta 12 señales |
| **3** | Arquitecto + Control de Deriva | 5-6 | ❌ Pendiente | Doble instancia, veto cambios bruscos |
| **4** | Perfil Biológico | 7-8 | ❌ Pendiente | Adapta al cronotipo del usuario |
| **5** | Integración TR-ARES | 9 | ❌ Pendiente | Funciona standalone + ARES |
| **6** | Documentación Unificada | 10 | ❌ Pendiente | README apunta a todos los docs |

**Ver plan completo:** [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md)

---

## 🔌 MÓDULOS DISPONIBLES

### Módulos Completados (✅ aiReady: true)

| Módulo | Funciones | Estado | INDEX.md |
|--------|-----------|--------|----------|
| `@agentedecambio2/deepseek-connector` | `createCompletion()`, `createCompletionStream()` | ✅ | [`/modules/deepseek-connector/INDEX.md`](./modules/deepseek-connector/INDEX.md) |
| `@agentedecambio2/session-manager` | `createSession()`, `getSession()`, `updateSession()` | ✅ | [`/modules/session-manager/INDEX.md`](./modules/session-manager/INDEX.md) |
| `@agentedecambio2/prompt-engine` | `buildSystemPrompt()`, `updatePrompt()`, `negotiateChange()` | ✅ | [`/modules/prompt-engine/INDEX.md`](./modules/prompt-engine/INDEX.md) |
| `@agentedecambio2/delta-calculator` | `calculate()`, `compare()`, `threshold()` | ✅ | [`/modules/delta-calculator/INDEX.md`](./modules/delta-calculator/INDEX.md) |
| `@agentedecambio2/shared-types` | Tipos TypeScript | ✅ | [`/modules/shared-types/INDEX.md`](./modules/shared-types/INDEX.md) |

### Módulos Pendientes (⚠️ En Desarrollo)

| Módulo | Estado | Hito |
|--------|--------|------|
| `@agentedecambio2/socket-server` | ⚠️ Pendiente | 1 |
| `@agentedecambio2/state-manager` | ⚠️ Pendiente | 1 |
| `@agentedecambio2/questionnaire-engine` | ❌ Por crear | 1 |
| `@agentedecambio2/quiz-engine` | ❌ Por crear | 1 |
| `@agentedecambio2/objectives-manager` | ❌ Por crear | 2 |
| `@agentedecambio2/stall-detector` | ❌ Por crear | 2 |
| `@agentedecambio2/architect` | ❌ Por crear | 3 |

**Registro completo:** [`/modules/registry.json`](./modules/registry.json)

---

## 🔧 COMANDOS PRINCIPALES

### Desarrollo

```bash
# Iniciar ambos servidores (frontend + backend)
npm run dev

# Solo backend
npm run dev:server

# Solo frontend
npm run dev:web

# Build de producción
npm run build

# Iniciar en producción
npm start
```

### Tests y Calidad

```bash
# Tests de todos los módulos
npm test

# Linting
npm run lint

# Type checking
cd apps/web && npm run type-check
cd apps/server && npm run type-check
```

### Git Backups (Protocolo Obligatorio)

```bash
# Antes de cada cambio
git add .
git commit -m "BACKUP $(date '+%Y-%m-%d_%H-%M-%S') - Pre-[cambio]"
git tag "backup-$(date '+%Y%m%d-%H%M%S')"

# Después de cada hito
git tag "hito-[N]-completado-$(date '+%Y%m%d-%H%M%S')"
```

---

## 🧪 PRUEBAS REALIZADAS

| Prueba | Estado | Notas |
|--------|--------|-------|
| Servidor inicia (puerto 3001) | ✅ | `apps/server/src/index.ts` |
| Frontend inicia (puerto 3000) | ✅ | Next.js 14 |
| API REST responde con DeepSeek | ✅ | `/api/interact` |
| Conexión Socket.IO establecida | ✅ | WebSocket |
| Estado persistente en localStorage | ✅ | Zustand |
| Animaciones funcionan | ✅ | Framer Motion |
| Responsive design básico | ✅ | Tailwind CSS |

**Estado detallado:** [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md)

---

## 🐛 PROBLEMAS CONOCIDOS

| Problema | Severidad | Solución | Hito |
|----------|-----------|----------|------|
| Streaming UI no muestra caracteres en tiempo real | Media | Implementar en Hito 1 | 1 |
| Métricas de deriva simuladas (longitud texto) | Alta | Algoritmo semántico en Hito 3 | 3 |
| Error handling básico de DeepSeek API | Media | Mejorar en Hito 2 | 2 |
| ESLint version conflict | Baja | Usar `--legacy-peer-deps` | - |
| Next.js 14.2.28 vulnerability | Alta | Actualizar en Hito 5 | 5 |

---

## 📊 MÉTRICAS ACTUALES

| Métrica | Valor |
|---------|-------|
| **Tiempo de respuesta API** | < 2s (DeepSeek API) |
| **Conexión WebSocket** | Estable con reconexión automática |
| **Bundle size frontend** | ~1.5MB (desarrollo) |
| **Líneas de código** | ~1500 (TypeScript/JavaScript) |
| **Componentes React** | 15+ |
| **Módulos completados** | 5/12 |
| **Módulos aiReady** | 2/12 |

---

## 🤝 CONTRIBUCIÓN

### Protocolo para IAs

1. **Leer primero:** [`INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md)
2. **Crear backup git:** `git tag "backup-$(date '+%Y%m%d-%H%M%S')"`
3. **Implementar módulo:** Máximo 3 funciones, INDEX.md <50 líneas
4. **Actualizar registry.json:** Agregar módulo nuevo
5. **Tests passing:** `npm test`
6. **Git diff validar:** `git diff --stat`
7. **Commit con referencia:** `[MÓDULO] Descripción → INDICE-MAESTRO [sección]`

### Checklist Pre-Commit

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

## 📄 LICENCIA

MIT License

---

## 🧠 FILOSOFÍA DEL PROYECTO

| Principio | Significado |
|-----------|-------------|
| **Google Lens** | La herramienta desaparece, queda el resultado |
| **Pragmatismo radical** | Navaja suiza, no catedral |
| **Eficacia y eficiencia** | No sobra ni falta nada |
| **Belleza funcional** | Interfaz que comunica profesionalismo |
| **Adaptación perfecta** | Se ajusta a la necesidad, no al revés |

---

## 🔗 REFERENCIAS CRUZADAS

### Internas

- **Plan de Construcción:** [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md)
- **Estado Actual:** [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md)
- **Registry de Módulos:** [`/modules/registry.json`](./modules/registry.json)

### Externas (TR-ARES)

- **Índice Maestro para IAs:** [`/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md)
- **Requerimientos (Análisis):** [`/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md)
- **Memoria QWEN.md:** [`~/.qwen/QWEN.md`](file:///home/daniel/.qwen/QWEN.md)

---

**Última actualización:** 2026-03-19  
**Versión:** 0.1.0 (Prototipo Funcional)  
**Próximo hito:** 1 - Motor de Cuestionarios y Quiz

---

*Este README es una introducción. Para trabajar en el proyecto, leer obligatoriamente la documentación CLAVE.*

---

**Cognitive Server v0.1** • Sistema de Extracción Cognitiva con Prompts Vivos
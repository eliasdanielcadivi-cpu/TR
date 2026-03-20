# Auditoría de Capacidades - AgenteDeCambio2

**Fecha:** 2026-02-24  
**Objetivo:** Identificar capacidades discretas en el código actual para refactorización modular

---

## 📊 Capacidades Identificadas

### BACKEND (apps/server)

| # | Capacidad | Archivo Actual | Funcionalidades (1-3) | Complejidad |
|---|-----------|----------------|----------------------|-------------|
| 1 | **DeepSeek Connector** | `src/clients/deepseek.ts` | 1. `createCompletion` - Completación síncrona<br>2. `createCompletionStream` - Streaming SSE | Baja |
| 2 | **Socket Server** | `src/index.ts` (parcial) | 1. `init` - Inicializar conexión Socket.IO<br>2. `emit` - Emitir eventos a clientes<br>3. `on` - Escuchar eventos de clientes | Media |
| 3 | **Session Manager** | `src/index.ts` (parcial) | 1. `createSession` - Crear sesión<br>2. `getSession` - Obtener sesión<br>3. `updateSession` - Actualizar sesión | Baja |
| 4 | **Prompt Engine** | `src/index.ts` (parcial) | 1. `buildSystemPrompt` - Construir prompt con contexto<br>2. `calculatePromptDelta` - Calcular deriva | Media |
| 5 | **Delta Metrics Calculator** | `src/index.ts` (parcial) | 1. `calculatePromptDelta` - Calcular diferencia entre prompts<br>2. `delta:update` - Emitir métricas | Baja |
| 6 | **REST API Handler** | `src/index.ts` (parcial) | 1. `POST /api/interact` - Endpoint compatible<br>2. `GET /health` - Health check | Baja |

---

### FRONTEND (apps/web)

| # | Capacidad | Archivo Actual | Funcionalidades (1-3) | Complejidad |
|---|-----------|----------------|----------------------|-------------|
| 7 | **State Manager (Zustand)** | `app/store/chatStore.ts` | 1. `createStore` - Crear store persistente<br>2. `persist` - Persistir en localStorage<br>3. `subscribe` - Suscribirse a cambios | Media |
| 8 | **Socket Client** | No existe como módulo separado | 1. `connect` - Conectar a Socket.IO<br>2. `emit` - Enviar eventos<br>3. `on` - Escuchar eventos | Pendiente |
| 9 | **Chat Components** | `components/chat/` | 1. `ChatContainer` - Contenedor principal<br>2. `ChatMessage` - Burbuja de mensaje<br>3. `ChatInput` - Input de usuario | Media |
| 10 | **Layout Components** | `components/layout/` | 1. `Header` - Cabecera con logo<br>2. `ModeSwitcher` - Cambiar chat/cuestionario<br>3. `ReasoningToggle` - Activar razonamiento | Baja |
| 11 | **Questionnaire Component** | `components/chat/Questionnaire.tsx` | 1. Renderizar preguntas<br>2. Capturar selección de opciones | Baja |
| 12 | **Prompt Editor** | `components/prompt/` | 1. Editar system prompt en tiempo real | Baja |
| 13 | **Delta Meter** | `components/metrics/` | 1. Visualizar métricas de deriva | Baja |
| 14 | **Objectives Panel** | `components/objectives/` | 1. Mostrar/gestionar objetivos | Baja |

---

### TIPOS COMPARTIDOS (packages/shared)

| # | Capacidad | Archivo Actual | Tipos Definidos |
|---|-----------|----------------|-----------------|
| 15 | **Socket Types** | `server/src/types/socket.ts` | `ServerToClientEvents`, `ClientToServerEvents`, `ChatMessage`, `Session`, etc. |
| 16 | **Store Types** | `web/app/store/chatStore.ts` | Duplicados parcialmente con server |

---

## 🔴 Problemas Identificados

### 1. **Acoplamiento en index.ts**
El archivo `apps/server/src/index.ts` contiene **6 capacidades diferentes** mezcladas:
- Socket server setup
- Session management
- Prompt building
- Delta calculation
- REST endpoints
- Event handlers

**Riesgo:** Difícil de mantener, testear y entender por IA.

### 2. **Duplicación de Tipos**
Los tipos están duplicados entre:
- `server/src/types/socket.ts`
- `web/app/store/chatStore.ts`

**Riesgo:** Inconsistencias, deuda técnica.

### 3. **Falta de Comentarios JSDoc**
Ninguna función tiene comentarios estandarizados.

**Riesgo:** La IA no puede entender rápidamente qué hace cada función.

### 4. **No hay INDEX.md por módulo**
No hay documentación que resuma funcionalidades por capacidad.

**Riesgo:** La IA debe leer todo el código para entender.

---

## ✅ Estructura Modular Propuesta

```
AgenteDeCambio2/
├── modules/                          # ← NUEVO: Módulos independientes
│   ├── registry.json                 # Registro central de módulos
│   │
│   ├── deepseek-connector/           # Capacidad #1
│   │   ├── INDEX.md                  # ← Lo que la IA lee primero
│   │   ├── actions.ts                # 1-3 funciones exportadas
│   │   ├── types.ts                  # Tipos específicos
│   │   └── manifest.json             # Metadatos estructurados
│   │
│   ├── socket-server/                # Capacidad #2
│   │   ├── INDEX.md
│   │   ├── actions.ts
│   │   ├── events.ts
│   │   └── manifest.json
│   │
│   ├── session-manager/              # Capacidad #3
│   │   └── ...
│   │
│   ├── prompt-engine/                # Capacidad #4
│   │   └── ...
│   │
│   ├── delta-calculator/             # Capacidad #5
│   │   └── ...
│   │
│   └── state-manager/                # Capacidad #7 (frontend)
│       └── ...
│
├── apps/
│   ├── server/
│   │   └── src/
│   │       ├── index.ts              # ← Reducido: solo orquestación
│   │       ├── clients/              # ← Migrar a modules/
│   │       ├── sockets/              # ← Vacío, migrar a modules/
│   │       └── services/             # ← Vacío, migrar a modules/
│   │
│   └── web/
│       └── ...
│
└── packages/
    └── shared/
        └── types/                    # ← Tipos unificados
```

---

## 📋 Plan de Migración

### Prioridad 1 (Crítico)
1. **deepseek-connector** - Aislado, fácil de extraer
2. **session-manager** - Independiente, sin dependencias externas
3. **delta-calculator** - Funciones puras, fácil refactorización

### Prioridad 2 (Importante)
4. **socket-server** - Requiere definir eventos explícitamente
5. **prompt-engine** - Depende de session-manager
6. **state-manager** - Frontend, requiere actualizar imports

### Prioridad 3 (Secundario)
7. **rest-api-handler** - Puede esperar
8. **Tipos compartidos** - Unificar después de migrar backend

---

## 🎯 Criterios de Aceptación por Módulo

Cada módulo debe tener:

- [ ] `INDEX.md` con ≤50 líneas (funcionalidades, flujo, eventos, dependencias)
- [ ] `actions.ts` con 1-3 funciones exportadas máximo
- [ ] `manifest.json` con id, version, actions, events, dependencies
- [ ] Comentarios JSDoc encima de cada función exportada
- [ ] Tests unitarios (cobertura >90%)
- [ ] README.md con ejemplos de uso

---

*Documento vivo - se actualiza conforme avanza la migración*

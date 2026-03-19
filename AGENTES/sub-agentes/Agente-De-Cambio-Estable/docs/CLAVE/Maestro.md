# 📋 Documento Maestro de Diseño e Interfaz

## Introducción

Este documento consolida toda la información táctica y estratégica
que una IA externa necesita para trabajar en la maquetación e interfaz
del proyecto Agente de Cambio.

---

## 📋 Lista de Documentos de Maquetación e Interfaz para IA Externa

<!-- INICIO_RESPUESTA_ANTERIOR -->

Perfecto, ahora tengo el panorama completo. Aquí está la lista estructurada de documentos e información clave que la IA externa necesitará:

---

## **1. DOCUMENTOS PRINCIPALES (Jerarquía 1)**

| Documento | Ruta | Propósito para la IA |
|-----------|------|---------------------|
| **README.md** | `/README.md` | Visión general, stack tecnológico, filosofía de diseño (Glassmorphism, Framer Motion) |
| **proyecto.md** | `/docs/proyecto.md` | Arquitectura completa, etapas, sistema de diseño, tokens de color |
| **ListaRequerimientos.md** | `/docs/ListaRequerimientos.md` | **CRÍTICO**: 27 requerimientos con filosofía "Google Lens", pragmatismo radical, glassmorphism |
| **METODOLOGIA-MODULAR.md** | `/docs/METODOLOGIA-MODULAR.md` | Patrones arquitectónicos (Capability-Based, MCP, AI-Native), optimización de contexto IA |
| **AUDITORIA-CAPACIDADES.md** | `/docs/AUDITORIA-CAPACIDADES.md` | 16 capacidades discretas identificadas, estructura modular propuesta |
| **estado.md** | `/docs/estado.md` | Estado actual de implementación, problemas conocidos, próximos pasos |

---

### **2. DOCUMENTOS DE DISEÑO Y ESTILO (Jerarquía 2)**

| Archivo | Ruta | Información Clave |
|---------|------|-------------------|
| **tailwind.config.js** | `/apps/web/tailwind.config.js` | **Tokens de diseño**: colores `cognitive-*`, `reasoning-*`, animaciones (`float`, `glow`, `typing`), glass-gradient |
| **globals.css** | `/apps/web/app/globals.css` | **Glassmorphism CSS**: `.glass-panel`, `.glass-input`, scrollbar personalizado, keyframes de animación |
| **chatStore.ts** | `/apps/web/app/store/chatStore.ts` | Estado global: modos, mensajes, prompt, métricas delta, objetivos |
| **socket.ts** | `/apps/server/src/types/socket.ts` | Tipos compartidos: eventos Socket.IO, estructura de mensajes, preguntas, métricas |

---

### **3. COMPONENTES DE INTERFAZ (Jerarquía 3)**

#### **Layout Components**
| Componente | Ruta | Función |
|------------|------|---------|
| `Header.tsx` | `/apps/web/components/layout/Header.tsx` | Cabecera con logo y controles globales |
| `ModeSwitcher.tsx` | `/apps/web/components/layout/ModeSwitcher.tsx` | Toggle entre modo chat/cuestionario |
| `ReasoningToggle.tsx` | `/apps/web/components/layout/ReasoningToggle.tsx` | Activar/desactivar modo reasoning |

#### **Chat Components**
| Componente | Ruta | Función |
|------------|------|---------|
| `ChatContainer.tsx` | `/apps/web/components/chat/ChatContainer.tsx` | Contenedor principal (600px, glass-panel) |
| `ChatMessage.tsx` | `/apps/web/components/chat/ChatMessage.tsx` | Burbuja de mensaje individual animada |
| `ChatInput.tsx` | `/apps/web/components/chat/ChatInput.tsx` | Input de texto para modo chat |
| `Questionnaire.tsx` | `/apps/web/components/chat/Questionnaire.tsx` | Renderizado de preguntas con opciones |

#### **Métricas y Prompt**
| Componente | Ruta | Función |
|------------|------|---------|
| `PromptEditor.tsx` | `/apps/web/components/prompt/PromptEditor.tsx` | Editor de system prompt en tiempo real |
| `DeltaMeter.tsx` | `/apps/web/components/metrics/DeltaMeter.tsx` | Visualización de deriva del prompt (0-1) |
| `ObjectivesPanel.tsx` | `/apps/web/components/objectives/ObjectivesPanel.tsx` | Panel de objetivos permanentes |

---

### **4. INFORMACIÓN TÁCTICA ESTRATÉGICA PARA LA IA**

#### **4.1 Filosofía de Diseño (NO NEGOCIABLE)**
```
1. "Google Lens": La herramienta desaparece para mostrar el resultado
2. Pragmatismo radical: No construir catedrales, navaja suiza bien afilada
3. Belleza funcional: Glassmorphism + microinteracciones que comunican profesionalismo
4. Ratio utilidad/esfuerzo: No sobra ni falta nada para el caso de uso
5. Adaptación perfecta: La IA no decide estética, sigue convenciones establecidas
```

#### **4.2 Sistema de Coordenadas de Maquetación (Propuesta)**

**Zonas convencionales del layout:**
```
┌─────────────────────────────────────────────┐
│ ZONA-A: Header (logo + ModeSwitcher + ReasoningToggle) │
├─────────────────────────────────────────────┤
│ ZONA-B: PromptEditor (editable, tiempo real)          │
├─────────────────────────────────────────────┤
│ ZONA-C: ChatContainer (600px, glass-panel)            │
│   - C-1: Área de mensajes (scroll-y)                  │
│   - C-2: Indicador de typing (streaming)              │
│   - C-3: Input area (ChatInput / Questionnaire)       │
├─────────────────────────────────────────────┤
│ ZONA-D: DeltaMeter + ObjectivesPanel (lateral/bottom) │
└─────────────────────────────────────────────┘
```

**Convención de nombres para diálogo IA-usuario:**
```
[ZONA]-[COMPONENTE]-[ACCIÓN]

Ejemplos:
- "C-ChatInput: agregar efecto metalizado al borde"
- "A-ModeSwitcher: animación spring más suave"
- "C-ChatMessage: burbuja a la derecha con gradiente cognitive-500"
- "B-PromptEditor: que brille cuando delta > 0.3"
```

#### **4.3 Estándares de la Industria (2024-2026)**

| Categoría | Estándar | Implementación en este proyecto |
|-----------|----------|--------------------------------|
| **Arquitectura** | Capability-Based | Módulos de 1-3 funciones con INDEX.md |
| **IA-Native** | Model Context Protocol (MCP) | Socket.IO como protocolo de comunicación |
| **Animaciones** | Spring Physics (Framer Motion) | `transition: { type: "spring", stiffness: 300, damping: 30 }` |
| **Diseño** | Glassmorphism Premium | `backdrop-filter: blur()`, bordes sutiles, transparencia |
| **Estado** | Zustand con persistencia | localStorage + selectivo |
| **Streaming** | SSE + WebSocket | DeepSeek API → Socket.IO → React |
| **Contexto IA** | RAG + Semantic Chunking | Documentos modulares <50 líneas |

#### **4.4 Sistema de Depuración y Marca de Componentes**

**Propuesta de etiquetado para Chrome DevTools:**
```typescript
// En cada componente React, agregar data-attribute:
<div 
  data-component="ChatContainer" 
  data-zone="C"
  data-debug="border: cyan; animation: glow"
>
```

**MCP auxiliar para Chrome DevTools:**
- La IA puede usar un MCP para consultar el DOM
- Etiquetas semánticas permiten referenciar componentes por nombre
- El usuario ve "chuleta" visual con nombres de zonas/componentes

#### **4.5 Convenciones de Diálogo IA-Usuario**

**Sintaxis propuesta:**
```
[ZONA/COMPONENTE] + [UBICACIÓN RELATIVA] + [EFECTO/ANIMACIÓN] + [ESTADO]

Ejemplos completos:
1. "C-ChatMessage: a la derecha, gradiente cognitive-600, shadow glow, hover scale-105"
2. "A-ReasoningToggle: centro vertical, animación rotate-180, activo: reasoning-500"
3. "D-DeltaMeter: esquina inferior derecha, pulse cuando delta > threshold"
```

---

### **5. DOCUMENTOS ADICIONALES DE REFERENCIA**

| Documento | Ruta | Utilidad |
|-----------|------|----------|
| `Apideepseek.md` | `/docs/Apideepseek.md` | API del motor de inferencia (DeepSeek) |
| `CHANGELOG-MODULAR.md` | `/docs/CHANGELOG-MODULAR.md` | Historial de cambios modulares |
| `MIGRACION-COMPLETADA.md` | `/docs/MIGRACION-COMPLETADA.md` | Proceso de migración completado |
| `PROGRESO-MIGRACION.md` | `/docs/PROGRESO-MIGRACION.md` | Estado de migración modular |
| `sistema-por-kimi.md` | `/docs/sistema-por-kimi.md` | Diseño detallado de interfaz |

---

### **6. RESUMEN EJECUTIVO PARA LA IA EXTERNA**

```markdown
# Contexto para IA de Maquetación

## Stack Tecnológico
- Next.js 14 (App Router) + React 18 + TypeScript
- Tailwind CSS + Framer Motion (spring physics)
- Glassmorphism: backdrop-blur, bordes sutiles, transparencia
- Socket.IO para tiempo real
- Zustand para estado global

## Filosofía de Diseño
- "Google Lens": herramienta invisible, resultado visible
- Pragmatismo radical: eficacia > estética teórica
- Microinteracciones que comunican profesionalismo
- Animaciones fluidas (60fps), bundle liviano

## Sistema de Coordenadas
- Zonas: A (Header), B (Prompt), C (Chat), D (Métricas)
- Componentes nombrados convencionalmente
- Diálogo IA: "[ZONA]-[COMPONENTE]: [efecto], [ubicación], [estado]"

## Límites a la Entropía
- Máximo 3 funcionalidades por módulo
- INDEX.md <50 líneas por componente
- Contexto IA optimizado (RAG, semantic chunking)
- MCP para Chrome DevTools (etiquetado semántico)

## Lo que la IA NO decide
- No cambia arquitectura sin aprobación
- No añade dependencias sin justificación
- No modifica tokens de diseño base
- No rompe filosofía "Google Lens"
```

---

¿Quieres que profundice en algún documento específico o que prepare un prompt estructurado para la IA externa con toda esta información?

<!-- FIN_RESPUESTA_ANTERIOR -->

---

## 📁 Archivos Clave con Contenido Completo

### ✅ Archivos Incluidos (20)

### 📄 README.md

**Descripción:** Visión general, stack tecnológico, filosofía de diseño

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/README.md`

```markdown
# 🧠 Agente de Cambio - Sistema Cognitivo de Extracción

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

## 🚀 Instalación Rápida

### Prerrequisitos
- Node.js 18 o superior
- API Key de DeepSeek (gratuita en [platform.deepseek.com](https://platform.deepseek.com/api_keys))

### 1. Clonar y configurar
```bash
# Clonar el proyecto
git clone <repo-url>
cd Agente-De-Cambio

# Instalar dependencias (usar legacy-peer-deps por compatibilidad)
npm install --legacy-peer-deps

# Configurar variables de entorno
cp apps/server/.env.example apps/server/.env
# Editar apps/server/.env con tu API Key de DeepSeek
```

### 2. Iniciar servidores
```bash
# Opción A: Ambos servidores simultáneamente (raíz del proyecto)
npm run dev

# Opción B: Servidores por separado
npm run dev:server  # Backend en http://localhost:3001
npm run dev:web     # Frontend en http://localhost:3000
```

### 3. Acceder a la interfaz
Abrir [http://localhost:3000](http://localhost:3000) en tu navegador.

## 📁 Estructura del Proyecto

```
Agente-De-Cambio/
├── apps/
│   ├── web/                    # Frontend Next.js
│   │   ├── app/               # App Router (pages y layout)
│   │   ├── components/        # Componentes React reutilizables
│   │   ├── store/             # Zustand stores (estado global)
│   │   └── styles/            # Tailwind y CSS personalizado
│   └── server/                # Backend Node.js
│       ├── src/
│       │   ├── clients/       # Cliente DeepSeek API con streaming
│       │   ├── sockets/       # Handlers de Socket.IO
│       │   ├── services/      # Lógica de negocio
│       │   └── types/         # Tipos TypeScript
│       └── test/
├── docs/                      # Documentación del proyecto
├── packages/                  # Código compartido (pendiente)
├── scripts/                   # Scripts de utilidad
└── herramientas/              # Herramientas TRON nativas
```

## 🔧 Configuración Avanzada

### Variables de Entorno (Backend)
Crear archivo `apps/server/.env`:
```env
DEEPSEEK_API_KEY=sk-tu-api-key-aqui
PORT=3001
NODE_ENV=development
CLIENT_URL=http://localhost:3000
PROMPT_DELTA_THRESHOLD=0.3
```

### Variables de Entorno (Frontend)
Crear archivo `apps/web/.env.local`:
```env
NEXT_PUBLIC_SOCKET_URL=http://localhost:3001
NEXT_PUBLIC_API_URL=http://localhost:3001/api
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### DeepSeek API
El sistema utiliza DeepSeek Chat (128K context) como motor de inferencia. Características soportadas:
- Streaming de respuestas
- Modo reasoning (pensamiento)
- Caché de contexto (reducción de costos)
- Formato JSON de salida

## 🎨 Diseño de Interfaz

La interfaz sigue principios de **glassmorphism** y **microinteracciones**:
- Fondo con gradiente oscuro y blur
- Componentes con bordes sutiles y transparencia
- Animaciones con Framer Motion (spring physics)
- Indicadores visuales de estado (conexión, streaming, métricas)
- Transiciones suaves entre modos chat/cuestionario

## 🔌 API y Socket.IO

### Eventos del Servidor (Server → Client)
- `message:stream` - Chunk de texto stream
- `message:complete` - Mensaje completo del assistant
- `prompt:mutation` - Cambio en el system prompt
- `question:next` - Nueva pregunta en modo cuestionario
- `delta:update` - Actualización de métricas de deriva
- `mode:switch` - Cambio de modo chat/cuestionario

### Eventos del Cliente (Client → Server)
- `message:send` - Enviar mensaje del usuario
- `prompt:update` - Actualizar system prompt
- `option:select` - Seleccionar opción en cuestionario
- `mode:set` - Cambiar modo
- `reasoning:toggle` - Activar/desactivar modo reasoning
- `session:init` - Inicializar o recuperar sesión

## 📊 Métricas de Deriva

El sistema calcula la "deriva" del prompt comparando cambios semánticos:
- **Score**: 0-1 (0 = sin cambios, 1 = cambio total)
- **Umbral**: 0.3 (configurable)
- **Aprobación**: Cambios sobre el umbral requieren confirmación
- **Visualización**: Barra de progreso con indicador de umbral

## 🧪 Pruebas

```bash
# Pruebas del backend
cd apps/server && npm test

# Type checking
cd apps/web && npm run type-check

# Linting
npm run lint
```

## 🚢 Despliegue

### Producción
```bash
# Build de ambos proyectos
npm run build

# Iniciar en producción
npm start
```

### Docker (pendiente)
```dockerfile
# Próximamente
```

## 📈 Roadmap

- [x] Estructura base del monorepo
- [x] Backend con Socket.IO y DeepSeek API
- [x] Frontend con componentes premium
- [ ] Integración completa Socket.IO frontend-backend
- [ ] Algoritmo avanzado de métricas de deriva
- [ ] Persistencia con Redis
- [ ] Panel de administración y logs
- [ ] Despliegue Docker
- [ ] App móvil (React Native)

## 🐛 Solución de Problemas

### "Cannot find module" errors
```bash
# Reinstalar dependencias
rm -rf node_modules apps/*/node_modules
npm install --legacy-peer-deps
```

### Error de conexión Socket.IO
- Verificar que el servidor esté en el puerto 3001
- Verificar CORS configuration en `apps/server/src/index.ts`
- Revisar consola del navegador para errores WebSocket

### Error de API DeepSeek
- Verificar que la API Key sea válida en `apps/server/.env`
- Verificar conexión a internet
- Revisar logs del servidor para detalles del error

## 📚 Documentación Adicional

- [Documentación del proyecto](/docs/proyecto.md) - Plan maestro y arquitectura
- [Rutas de archivos](/docs/rutas.md) - Listado completo de archivos
- [API DeepSeek](/docs/Apideepseek.md) - Documentación oficial de DeepSeek API

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🧠 Filosofía del Proyecto

- **Pragmatismo radical**: No construir catedrales, navaja suiza bien afilada
- **Eficacia y eficiencia**: No sobra ni falta nada para el caso de uso
- **Belleza funcional**: Interfaz que comunica profesionalismo y confianza
- **Adaptación perfecta**: Como Google Lens, la herramienta desaparece para mostrar el resultado

---

**Cognitive Server v0.1** • Sistema de Extracción Cognitiva con Prompts Vivos
```

---

### 📄 docs/proyecto.md

**Descripción:** Arquitectura completa, etapas, sistema de diseño

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/proyecto.md`

```markdown
# Proyecto Agente de Cambio - Sistema Cognitivo de Extracción

## Visión General
Sistema de interacción conversacional adaptativa con prompts vivos y métricas de deriva, diseñado para extracción cognitiva de alto nivel y conducción estratégica del usuario hacia sus objetivos.

## Arquitectura Tecnológica
- **Frontend**: Next.js 14 (App Router) + React 18 + TypeScript + Tailwind CSS + Framer Motion
- **Backend**: Node.js + Express + Socket.IO + DeepSeek API (modos chat y reasoning)
- **Estado**: Zustand con persistencia + Socket.IO para tiempo real
- **Estilo**: Glassmorphism, animaciones fluidas, microinteracciones premium
- **Despliegue**: Monorepo con estructura modular

## Etapas de Implementación

### Etapa 1: Infraestructura Base (Semana 1)
- [x] Crear estructura de carpetas monorepo
- [ ] Configurar package.json global y workspaces
- [ ] Configurar TypeScript, ESLint, Prettier
- [ ] Configurar variables de entorno (.env.example)
- [ ] Configurar scripts de desarrollo y build

### Etapa 2: Backend - Servidor Cognitivo (Semana 1-2)
- [ ] Servidor Node.js con Express y Socket.IO
- [ ] Cliente DeepSeek API con streaming
- [ ] Sistema de sesiones en memoria (luego Redis)
- [ ] Gestión de prompts dinámicos y métricas de deriva
- [ ] Algoritmo de negociación de cambios de prompt
- [ ] Endpoints REST para modo cuestionario
- [ ] Middleware de logging y diagnóstico

### Etapa 3: Frontend - Interfaz Premium (Semana 2-3)
- [ ] Configurar Next.js 14 con Tailwind CSS
- [ ] Sistema de diseño: tokens de color, tipografía, glassmorphism
- [ ] Componentes de layout: Header, ModeSwitcher, ReasoningToggle
- [ ] Componente Chat: Burbujas de mensajes animadas
- [ ] Componente PromptEditor: Editor de system prompt editable
- [ ] Componente Questionario: Preguntas con opciones y comentarios
- [ ] Animaciones de entrada/salida con Framer Motion
- [ ] Estado global con Zustand (modo, prompt, sesión)
- [ ] Conexión Socket.IO para streaming en tiempo real

### Etapa 4: Integración y Características Avanzadas (Semana 3-4)
- [ ] Integración completa frontend-backend
- [ ] Sistema de métricas de deriva visual (Delta Meter)
- [ ] Modo dual chat/cuestionario con transiciones suaves
- [ ] Persistencia de objetivos y memoria de sesión
- [ ] Algoritmo de evaluación de cambios de prompt
- [ ] Panel de diagnóstico y logging en tiempo real
- [ ] Optimización para entornos restringidos (Note 8/Termux)

### Etapa 5: Pruebas y Despliegue (Semana 4)
- [ ] Pruebas unitarias y de integración
- [ ] Optimización de rendimiento y bundle size
- [ ] Configuración de despliegue (Docker, PM2)
- [ ] Documentación de API y componentes
- [ ] Manual de usuario y casos de uso

## Características Clave Implementadas

### 1. Prompt Vivo y Mutante
- System prompt editable en tiempo real desde interfaz
- Algoritmo de negociación para cambios validados
- Métricas de deriva (Delta 0-1) con umbrales de confirmación
- Prevención de desviaciones bruscas del objetivo

### 2. Interfaz Híbrida de Selección
- Modo Chat: Conversación fluida con burbujas animadas
- Modo Cuestionario: Preguntas estructuradas con opciones (radio, check, yesno)
- Transiciones suaves entre modos
- Espacio para comentario adicional en cada interacción

### 3. Experiencia Visual Premium
- Glassmorphism con backdrop blur y gradientes sutiles
- Animaciones con spring physics (Framer Motion)
- Typing indicator con tres puntos animados
- Microinteracciones en hover, tap y focus
- Scroll personalizado minimalista
- Tema oscuro premium por defecto

### 4. Arquitectura de Doble Instancia
- Ejecutor: Interactúa con usuario via DeepSeek
- Arquitecto: Analiza meta permanente y propone cambios de prompt
- Separación de responsabilidades para control de deriva

### 5. Optimizaciones Técnicas
- Streaming de respuesta carácter por carácter
- Caché de contexto de DeepSeek para reducir costos
- Estado persistente entre sesiones
- Logging detallado para diagnóstico

## Estructura de Carpetas

```
Agente-De-Cambio/
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── app/               # App Router (pages)
│   │   ├── components/        # Componentes React
│   │   ├── store/             # Zustand stores
│   │   ├── styles/            # Tailwind y CSS
│   │   └── lib/               # Utilidades
│   └── server/                # Node.js backend
│       ├── src/
│       │   ├── clients/       # DeepSeek API client
│       │   ├── sockets/       # Socket.IO handlers
│       │   ├── services/      # Lógica de negocio
│       │   └── middleware/    # Middleware
│       └── test/
├── packages/
│   └── shared/                # Código compartido TypeScript
├── docs/                      # Documentación
├── scripts/                   # Scripts de utilidad
└── herramientas/              # Herramientas TRON nativas
```

## Requisitos Técnicos

### Backend
- Node.js 18+
- DeepSeek API key
- Socket.IO para comunicación en tiempo real
- Almacenamiento en memoria (Redis opcional para producción)

### Frontend
- Navegador moderno con soporte para ES2022
- Conexión WebSocket para streaming
- ~5MB de bundle size inicial

## Métricas de Éxito
- Tiempo de respuesta < 2s para primera interacción
- Streaming de texto con latencia < 100ms
- Interfaz a 60fps en animaciones
- Bundle size < 200KB comprimido
- Soporte para 10k tokens de contexto

## Próximos Pasos Inmediatos

1. **Configurar monorepo con workspaces**
2. **Implementar backend básico con Socket.IO**
3. **Crear componente de chat con burbujas animadas**
4. **Conectar frontend y backend con streaming**
5. **Implementar editor de prompt editable**

## Notas de Diseño

- Filosofía "Google Lens": La herramienta desaparece para mostrar el resultado
- Pragmatismo radical: No construir catedrales, navaja suiza bien afilada
- Eficacia y eficiencia: No sobra ni falta nada para el caso de uso
- Belleza funcional: Interfaz que comunica profesionalismo y confianza

---

*Documento vivo - se actualizará conforme avance el proyecto*
*Última actualización: 2026-02-23*
```

---

### 📄 docs/ListaRequerimientos.md

**Descripción:** 27 requerimientos con filosofía Google Lens

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/ListaRequerimientos.md`

```markdown
1. Directiva principal de toda esta conversación: Adaptarse perfecto a la necesidad, bajo la filosofía de elección de  "Google Lens" para el caso de uso de leer manuscritos del usuario, donde la herramienta desaparece para dejar paso al resultado.
    1.1. **Qué (El Atractivo):** La capacidad de abstracción para identificar que lo valioso no es la estética o la limpieza visual, sino la *ratio de utilidad por esfuerzo*, valorando una solución donde "no sobra ni falta nada".
    1.2. **Cómo (Metodología):** Mediante un pragmatismo radical que selecciona las herramientas (Openclaw, Deepseek, Node, Termux) no por su novedad, sino por cómo encajan en el caso de uso, eliminando la fricción de "construir catedrales" cuando se requiere una "navaja suiza".
    1.3. **Cuándo (Aplicación):** En cada decisión arquitectónica y programática, priorizando el funcionamiento en el entorno real (Note 8, red local) sobre ideales teóricos de desarrollo.
    1.4. **Por qué (Justificación):** Porque es la manera más limpia y honesta de ayudar con lo que viene, garantizando que el diseño disruptivo sea realmente cómodo y no una carga cognitiva para el usuario.
    1.5. **Para qué (Propósito Final):** Para crear un sistema cognitivo de alto valor (agente/web/cli) que conduzca al éxito rotundo de la persona (objetivos, metas, fechas) mediante una interacción fluida donde la IA negocia y adapta su prompt sin perder el rumbo.

2. **Definición de Entidad de Servidor Cognitivo:** Desarrollo de una estructura de servidor (tipo Node.js) que trascienda las definiciones limitantes de "app", "programa" o "agente", constituyéndose como una entidad flexible ("una cosa") capaz de orquestar interacciones inteligentes.
    2.1. **Conceptualización de "Una Cosa" No Limitante:** Definición de una entidad que "no digo app o programa" ni "agente" para "no quiero que te limites a pensar" en esquemas tradicionales, constituyéndose como una "especie de servidor node" o "una cosa" donde la herramienta desaparece para dejar paso al resultado bajo la filosofía de "Google Lens".
    2.2. **Pragmatismo Radical de Diseño:** Construcción bajo la directiva de "no construir una catedral" de código si una "navaja suiza" bien afilada resuelve el caso de uso, asegurando que "no sobra ni falta nada" y que la solución se "adapta perfecto a la necesidad" de forma "eficaz y eficiente".
    2.3. **Mecánica de "Pront" Viva y Mutante:** Configuración funcional donde la IA "altera su pront de sistema" en tiempo real "en la medida que el usuario responde", modificando su conducta no "por cambiar", sino bajo parámetros que "sabía inteligente, innovadora y disruptiva mente elegimos".
    2.4. **Algoritmo de Negociación de Deriva:** Implementación de una forma de "medir cuánto cambiará el promt" y qué es "negociado siempre", actuando de "manera algo determinista respetando lo no determinista y la fluidez" para evitar que el LLM "se vaya por dónde no debe" o realice cambios tan bruscos que "al final se desvía el camino".
    2.5. **Interfaz de Conducción Asistida:** Estructuración del discurso mediante "preguntas de selección" (botones de opción excluyentes o no excluyentes) y espacio al "comentario adicional", facilitando al usuario la "comodidad de no escribí tanto" mientras este "conduce junto con la IA la conversación y promt".
    2.6. **Orientación al Éxito Rotundo:** Sistema que "plantea y guarda en la memoria permanente" objetivos, metas y fechas límite (o se "inyectan a la conversación") para conducir a la persona de manera inteligente, operando como una "guitarra de asesoría multiprofesional" o "planificación de proyectos" para el "éxito rotundo de la persona en función de su contexto".

3. **Integración Preferente de Motor de Inferencia:** Implementación explícita de la API de DeepSeek (vía OpenRouter) como núcleo de procesamiento lógico, seleccionada por su alineación con el diseño disruptivo y capacidad de razonamiento superior para el caso de uso.
    3.1. **Elección Estratégica Disruptiva:** Selección deliberada de DeepSeek como motor principal, basada en una decisión que "sabía, inteligente, innovadora y disruptivamente elegimos", priorizando este modelo sobre otras opciones disponibles (como OpenAI o Claude) porque es el que "cabe mejor en el caso de uso" específico.
    3.2. **Filosofía de Eficiencia "Google Lens":** La implementación se rige por el criterio de que, aunque el modelo o la integración "no sea el más bonito o limpio" a nivel teórico, se valora porque "se adapta perfecto a la necesidad", siendo "por mucho la mejor opción" donde "no sobra ni falta nada" para resolver el problema.
    3.3. **Infraestructura Pragmática vía OpenRouter:** Uso operativo de la API de OpenRouter para canalizar la potencia de DeepSeek, aplicando un "pragmatismo radical" que evita "construir catedrales" de infraestructura, optando por una conexión tipo "navaja suiza" que es lo más práctico, eficaz y eficiente para el entorno del servidor.
    3.4. **Control de Desviación del LLM:** Configuración crítica para monitorear si "el LLM quiere cambiar el prompt y se va por dónde no debe", estableciendo límites para evitar que los cambios generados por la IA sean "tan bruscos que al final se desvía el camino" o propósito original de la conversación.
    3.5. **Balance de Fluidez y Determinismo:** Calibración del motor para que funcione de "manera algo determinista respetando lo no determinista y la fluidez", permitiendo que la IA "explore situaciones complejas" y renegocie su conducta sin perder la estructura lógica necesaria para el éxito del usuario.

4. **Mecánica de Alteración Dinámica del Prompt de Sistema:** Configuración de una lógica recursiva donde la IA modifica su propia "pronta de sistema" (System Prompt) en tiempo real, basándose en la retroalimentación y respuestas del usuario, evitando prompts estáticos.
    4.1. **Evolución de la "Pronta" en Tiempo Real:** La funcionalidad central es que la IA "responde preguntas", pero crucialmente, "en la medida que el usuario responde, ella altera su pronta de sistema", ajustando su comportamiento dinámicamente según parámetros que "sabía, inteligente, innovadora y disruptivamente elegimos".
    4.2. **Filtro de Merecimiento del Cambio:** Establecimiento de un control riguroso donde la IA "no puede cambiar el prompt por cambiar"; el sistema debe evaluar si, aunque el usuario quiera un cambio, realmente "merecerá que cambie", asegurando que cada modificación sea pertinente y no arbitraria.
    4.3. **Prevención de Desviación del Camino:** Implementación de mecanismos de seguridad para detectar si "el LLM quiere cambiar el prompt y se va por dónde no debe", evitando que los ajustes sean "tan bruscos que al final se desvía el camino" trazado originalmente.
    4.4. **Negociación Determinista-Fluida:** Integración de una metodología para "medir cuánto cambiará el prompt, cómo y qué" es "negociado siempre", operando de una "manera algo determinista respetando lo no determinista y la fluidez" inherente a una conversación natural.
    4.5. **Exploración Estructurada de Complejidad:** La IA "puede y necesita explorar situaciones complejas" mediante la redacción y adaptación de "preguntas cerradas, de opción cerrada, abiertas y múltiples", permitiendo que, "gracias al comentario adicional", el usuario vaya "conduciendo junto con la IA la conversación y el prompt".
    4.6. **Inyección Permanente de Objetivos:** Los "objetivos se plantean y guardan en la memoria permanente de la IA" (ya sea en el prompt o se "inyectan a la conversación"), permitiendo "conducir a una persona de manera inteligente" (mediante análisis psicológico o planificación) hacia un "éxito rotundo" sin perder el contexto.

5. **Protocolo de Negociación Determinista (programático con y/o sin IA auxiliar local "ollama") de Cambios:** Establecimiento de un algoritmo que mida y negocie "cuánto cambiará el prompt", equilibrando la fluidez no determinista del LLM con controles deterministas para evitar desviaciones bruscas o pérdida del objetivo.
    5.1. **Métrica de Magnitud de Alteración:** Implementación de "una forma de medir cuánto cambiará el promt", definiendo indicadores claros para cuantificar la intensidad de la modificación propuesta antes de ser aceptada por el sistema.
    5.2. **Balance de Fluidez y Rigor:** El mecanismo debe operar de "manera algo determinista respetando lo no determinista y la fluidez", logrando una negociación que permita la naturalidad de la IA sin sacrificar el control lógico de la estructura.
    5.3. **Evaluación de Merecimiento del Cambio:** Integración de un filtro crítico que cuestione si la modificación es necesaria, analizando que, aunque "puede que el usuario quiera que cambie el promt", el sistema debe validar si realmente "merecerá que cambie" o si es un capricho que desvirtúa la meta.
    5.4. **Prevención de Desviación de Ruta:** Control de seguridad para detectar si "el LLM quiere cambiar el promt y se va por dónde no debe", bloqueando aquellas alteraciones que sean "tan bruscos que al final se desvía el camino" trazado para el éxito del usuario.
    5.5. **Gestión Selectiva de Parámetros Conductuales:** Configuración inteligente donde, dentro de los "parámetros de la misma conducta de la IA, unos cambian y otros no", asegurando que la evolución del prompt no elimine las directrices base inmutables.
    5.6. **Negociación Continua del "Qué y Cómo":** Establecimiento de un proceso dinámico donde se define "cómo y qué" es "negociado siempre" en cada interacción, asegurando que la adaptación sirva estrictamente a la necesidad del caso de uso.

6. **Interfaz Híbrida de Selección y Comentario:** Diseño de interacción que combina preguntas estructuradas con botones de selección (excluyentes, no excluyentes) y espacios para "comentario adicional", permitiendo al usuario conducir la conversación con mínimo esfuerzo de escritura.
    6.1. **Estructuración del Discurso vía Selección:** El sistema debe "estructurar el discurso" generando "preguntas basadas en lo que el usuario responda", presentadas mediante "botones de opción excluyentes o no excluyentes" para agilizar la toma de decisiones.
    6.2. **Comodidad de Mínima Escritura:** La interfaz se diseña para "facilitar al usuario la comodidad de no escribir tanto", delegando el peso de la redacción en la IA, quien "ayuda en la conducción de la conversación" de manera proactiva.
    6.3. **Dinámica de Conducción Colaborativa:** Incorporación vital de un "espacio al comentario adicional" que permite al usuario, "consciente o no", ir "conduciendo junto con la IA la conversación y el prompt", fusionando la rigidez de los botones con la libertad del texto libre.
    6.4. **Exploración de Complejidad Adaptable:** Capacidad de la interfaz para presentar "preguntas cerradas, de opción cerrada, abiertas y múltiples", permitiendo que la IA pueda "explorar situaciones complejas" ajustando el formato de entrada según la profundidad requerida.
    6.5. **Estética Subordinada a la Necesidad:** La interfaz visual "no es el más bonito o limpio", pero "se adapta perfecto a la necesidad" bajo la premisa de "Google Lens", donde "no sobra ni falta nada" para que el caso de uso sea eficaz y eficiente.
    6.6. **Agnosticismo de Plataforma de Interacción:** Ya sea implementado como "app, web o CLI", el criterio rector es que sea "realmente cómoda", donde la herramienta técnica desaparece para centrarse en la interacción fluida.

7. **Arquitectura de Memoria Permanente de Objetivos:** Implementación de un sistema de almacenamiento persistente (inyectado en el prompt o en base de datos) para registrar metas, acciones y fechas límite, asegurando la continuidad en análisis psicológicos o planificación de proyectos.
    7.1. **Persistencia de la Intención:** Configuración de una "memoria permanente de la IA" donde "los objetivos se plantean y guardan" rigurosamente, garantizando que la dirección estratégica no se pierda entre las interacciones volátiles del chat.
    7.2. **Mecanismo de Inyección Contextual:** Implementación técnica donde los datos críticos "se inyectan a la conversación" o se alojan directamente "en el promt", asegurando que "en alguna parte de la conversación" la IA tenga acceso constante a lo establecido previamente.
    7.3. **Definición de Parámetros de Ejecución:** Estructuración precisa de la información almacenada para que queden claramente "establecidos objetos, metas, acciones, fechas límite", sirviendo como la columna vertebral operativa del sistema.
    7.4. **Conducción Inteligente del Usuario:** Uso de esta memoria para "conducir una persona de manera inteligente", permitiendo que la IA mantenga el hilo conductor y la presión necesaria sobre los compromisos adquiridos sin desviarse.
    7.5. **Versatilidad de Aplicación Profesional:** Adaptabilidad de la arquitectura de memoria para funcionar eficazmente "ya sea por un análisis psicológico", una estricta "planificación de proyectos" o funcionando como una "guitarra de asesoría multiprofesional".
    7.6. **Orientación al Éxito Contextual:** Diseño enfocado exclusivamente en lograr el "éxito rotundo de la persona", utilizando la memoria para ajustar las estrategias y recordatorios "en función de su contexto" específico y cambiante.

8. **Sistema de Doble Instancia (Arquitecto y Ejecutor):** Separación funcional donde una instancia (Ejecutor/DeepSeek) interactúa con el usuario y otra (Arquitecto/Capa de Control) analiza periódicamente la meta permanente para proponer cambios en la estructura del prompt.
    8.1. **Filtro de Justificación de Alteraciones:** Mecanismo de control enfocado en la indispensable regla lógica de que la IA "no puede cambiar el promt por cambiar", forzando una evaluación de fondo donde, aunque "puede que el usuario quiera que cambie el promt", el sistema determine con sabiduría si realmente "¿merecerá que cambie?".
    8.2. **Vigilancia Antidesviaciones del Camino:** Operación de la capa de control enfocada directamente en contener la deriva de la conversación, estructurada para actuar si resulta que "el LLM quiere cambiar el promt y se va por dónde no debe", evitando categoricamente que ocurran "cambios tan bruscos que al final se desvía el camino" y el resultado de la sesión.
    8.3. **Métrica de Negociación Constante:** Disposición técnica y procedimental delegada a la segunda instancia que consolida "una forma de medir cuánto cambiará el promt, cómo y qué negociado siempre", definiendo los límites de las alteraciones mediante reglas que "sabia, inteligente, innovadora y disruptivamente elegimos".
    8.4. **Equilibrio Determinista y Fluido:** Arquitectura encargada de administrar la regla de que entre "los parámetros de la misma conducta de la IA, unos cambian y otros no", logrando que la adaptación en tiempo real opere "de manera algo determinista respetando lo no determinista y la fluidez" inherente de la interacción.
    8.5. **Custodia de la Memoria y Metas Permanentes:** Uso de la capa arquitectónica para velar inquebrantablemente por aquellos "objetivos [que] se plantean y guardan en la memoria permanente de la IA", garantizando que la doble instancia logre su fin máximo: "conducir una persona de manera inteligente" para garantizar sin fallas el "éxito rotundo de la persona en función de su contexto".



10. **Selección Tecnológica de "Navaja Suiza":** Adopción de un stack tecnológico (Openclaw, SDKs de Anthropic/OpenAI, Langchain, Python o soluciones GitHub existentes) basado exclusivamente en el criterio de pragmatismo radical: lo que sea más práctico, eficaz y eficiente para el caso de uso.
    10.1. **Criterio de Funcionalidad y Conocimiento Práctico:** Selección de herramientas basada estrictamente en incorporar "lo más práctico", armando la funcionalidad del "esto" con "lo que mejor conozcas, incluso Python o Node o una app GitHub que ya hace lo que quiero".
    10.2. **Filosofía de Adaptación Perfecta ("Google Lens"):** El ensamblaje tecnológico no persigue que el código o la arquitectura sea "el más bonito o limpio", sino validarlo únicamente porque "se adapta perfecto a la necesidad", garantizando que "no sobra ni falta nada" para el producto final.
    10.3. **Rechazo a Modelos Mentales Limitantes:** El stack informático debe permitir desarrollar "una especie de servidor Node para crear una cosa", huyendo deliberadamente de los encasillamientos ("observa que no digo app o programa, es como un agente pero no digo agente") dictado bajo la orden: "no quiero que te limites a pensar: ah... ok, voy a crear un agente, una web".
    10.4. **Inclusión Abierta de Frameworks e Interfaces:** Disposición absoluta para utilizar cualquier caja de herramientas existente ("cuando por ejemplo con Openclaw se podía hacer con los parámetros y criterios"), incluyendo "Claude SDK, Anthropic SDK, Langchain, OpenAI SDK" o cualquier integración que pruebe ser la más adecuada.
    10.5. **Supremacía de Eficacia Orientada al Problema:** Cada decisión de software, hardware local o librería, debe pasar por un solo tamiz: demostrar que es "pragmático, eficaz y que cabe mejor en el caso de uso", asegurando ser siempre "eficaz y eficiente, y por mucho la mejor opción".
    10.6. **Integración Definida del Motor Principal:** Dentro de toda la flexibilidad de este abanico tecnológico, se mantiene inamovible la directriz sobre el núcleo duro de razonamiento, señalando que entre las herramientas disponibles ("tengo API de OpenRouter y de DeepSeek"), imperativa y selectivamente "para este caso preferimos DeepSeek".

11. **Optimización para Entornos Restringidos:** Diseño de software optimizado para operar con máxima eficiencia en hardware limitado (contexto Note 8/Termux), garantizando que el producto final sea ligero y adaptable a cualquier infraestructura de red local o móvil.

12. **Métrica de Deriva del Prompt (Deltas):** Desarrollo de un sistema de medición numérica (escala 0 a 1) para evaluar la magnitud del cambio en el texto del prompt respecto al original, activando solicitudes de confirmación al usuario si la modificación supera un umbral crítico.

13. **Adaptabilidad Multi-Dominio:** Capacidad del sistema para estructurar discursos y explorar situaciones complejas en diversos contextos, desde Clases de música,  "asesoría multiprofesional" hasta análisis psicológicos profundos, ajustando su conducta automáticamente.

14. **Reducción de Fricción Cognitiva:** Priorización de la comodidad del usuario ("no escribir tanto") mediante la predicción de respuestas y la conducción asistida de la conversación, donde la herramienta desaparece para dejar paso al resultado.

15. **Protocolos de Instalación Limpia:** Definición de procesos de despliegue que eviten la compilación innecesaria de módulos (como tree-sitter en entornos Android), utilizando comandos específicos para asegurar la estabilidad operativa.

16. **Estrategia de Asistencia Recursiva:** Utilización de herramientas de IA (como Gemini CLI actualizado) para asistir en la construcción y codificación del propio sistema servidor, acelerando el desarrollo del producto.

17. **Enfoque de Producto de Alto Valor:** Orientación del desarrollo no solo como una solución técnica, sino como un producto mercadotécnico adaptable a todos los segmentos, enfocado en garantizar el "éxito rotundo" del usuario.

18. **Validación por Investigación Profunda:** Requerimiento de investigación real en internet para sustentar las decisiones del diseño disruptivo, asegurando que la arquitectura propuesta sea la más innovadora y adecuada disponible.

19. **Gestión de Preguntas Dinámicas:** Capacidad de la IA para redactar y reestructurar preguntas (cerradas, abiertas, múltiples) en función de la evolución del diálogo, alterando su conducta según parámetros pre-elegidos "inteligente y disruptivamente".

20. **Filosofía de Eficacia y Eficiencia Absoluta:** Aplicación transversal del principio "no sobra ni falta nada", asegurando que cada línea de código y cada elemento de la interfaz cumpla una función crítica en la ratio de utilidad por esfuerzo.

21. **Implementación de Capa de Máxima Depuración (Logging y Diagnóstico):** Integración obligatoria e inmediata de capacidades de diagnóstico profundo en toda la estructura funcional para monitorizar el comportamiento real en tiempo de ejecución.
    21.1. **Auditoría de Entorno y Red:** Detección analítica de procesos que se inician automáticamente en segundo plano, así como prevención de conflictos con puertos ya en uso por sistemas independientes para asegurar una comunicación limpia.
    21.2. **Manejo Estricto de Enrutamiento:** Resolución determinista de las rutas base del servidor virtual (evitando salidas nulas o de conexión al origen) para asegurar que ninguna petición apunte al vacío.

22. **Gestión Segura y Pragmática de Variables de Entorno:** Establecimiento de un protocolo arquitectónico estándar (archivos de configuración locales) para el manejo de credenciales y rutas.
    22.1. **Encapsulamiento de Credenciales:** Aislamiento de las llaves de acceso del motor de inferencia lógico para evitar la fricción, vulnerabilidad y fatiga operativa de ingresarlas manual y repetitivamente en el código fuente.

23. **Garantía Entregable de Completitud Estructural:** Exigencia procedimental absoluta de proporcionar el espectro total de la solución programática sin atajos que comprometan su despliegue inmediato.
    23.1. **Entrega de Código Íntegro:** Prohibición estricta de entregar recortes, fragmentaciones o componentes que dependan de la suposición; la base de desarrollo debe proveerse de manera holística, compaginando todas sus partes funcionales.

24. **Aseguramiento de Accesibilidad en Interfaces de Texto:** Optimización generalizada de la interfaz de consola o entorno de comandos (CLI) independientemente del hardware subyacente.
    24.1. **Corrección de Contraste y Usabilidad Visual:** Ajuste programático de los parámetros base del terminal para garantizar que los indicadores interactivos, la escritura y cursores destaquen adecuadamente contra cualquier fondo, erradicando elementos invisibles por fallas cromáticas.

25. **Erradicación Absoluta de Simulaciones (Mocks) en Entorno de Ejecución:** Restricción inviolable que prohíbe generar flujos arquitectónicos temporales o de emulación frente a las capacidades del sistema.
    25.1. **Conexión Directa e Inmediata con Motor Lógico:** Exigencia de que el enlace de red canalice directamente los datos hacia un modelo de inferencia real procesando y respondiendo en vivo, descartando de plano cualquier ensayo de maqueta de código inerte.

26. **Directiva de Comprensión Holística Persistente:** Obligación inquebrantable impuesta a la entidad rectora del sistema de analizar siempre el contexto histórico total del proyecto antes de generar o proponer un cambio.
    26.1. **Lectura Integral desde el Génesis:** Aplicación estricta de barridos de memoria conversacional para no perder ninguna instrucción, matiz o requerimiento de información limitante instaurado desde las interacciones formativas originarias.

27. **Estandarización del Estilo Conductual y Comunicativo Determinista:** Fijación de una matriz temperamental operativa para el modelo que guíe los despliegues de información requeridos.
    27.1. **Lexicología Pragmática de Salida:** La semántica empleada para explicar, estructurar y ejecutar debe poseer atributos intocables: descriptivos, claros, concisos, precisos, al grano y veraces.
    27.2. **Determinismo Aplicado a las Intenciones del Usuario:** Cada línea de comportamiento lógico y explicativo debe regirse invariablemente por la directiva de apuntar única y exclusivamente a la funcionalidad ciertamente solicitada, bloqueando alucinaciones o desvíos técnicos no requeridos.

```

---

### 📄 docs/METODOLOGIA-MODULAR.md

**Descripción:** Patrones arquitectónicos, optimización contexto IA

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/METODOLOGIA-MODULAR.md`

```markdown
# Metodología AI-Native Modular para AgenteDeCambio2

## 📋 Resumen Ejecutivo

Esta metodología integra **6 patrones arquitectónicos modernos (2024-2026)** para organizar el repositorio en módulos independientes de 1-3 funcionalidades cada uno, permitiendo que la IA trabaje sin leer documentación masiva.

---

## 🏗️ Patrones Arquitectónicos Investigados

### 1. **Capability-Based Architecture** (Arquitectura Basada en Capacidades)
**Fuente:** dev.to/gd-tech-guru/capability-based-architecture

**Concepto clave:** Cada capacidad es una unidad discreta y autocontenida de funcionalidad que puede integrarse sin dependencias rígidas.

**Estructura por módulo:**
```
capabilities/
├── [nombre-capacidad]/
│   ├── actions.ts          # 1-3 funciones exportadas
│   ├── events.ts           # Eventos que emite/recibe
│   ├── manifest.json       # Metadatos para IA
│   └── README.md           # Documentación específica
```

**Beneficio para IA:** La IA lee solo el `manifest.json` para entender qué hace el módulo, sin necesidad de analizar todo el código.

---

### 2. **Model Context Protocol (MCP)**
**Fuente:** modelcontextprotocol.io

**Concepto clave:** Estándar "USB-C para IA" que conecta modelos con herramientas externas mediante interfaz JSON-RPC estandarizada.

**Aplicación en este proyecto:**
- Cada módulo expone sus funciones como "tools MCP"
- La IA descubre herramientas dinámicamente
- Sin hardcoding de integraciones

---

### 3. **Module-Driven Development con IA**
**Fuente:** dev.to/jaideepparashar/the-rise-of-modular-development

**Concepto clave:** Componentes evolucionan independientemente, experimentación contenida, fallos localizados.

**Principios:**
- Límites claros de responsabilidad
- Contención de experimentación (sandbox para IA)
- Auto-extensión del sistema

---

### 4. **AI-Native Architecture Patterns**
**Fuente:** catio.tech, IBM, JitAi

**Patrones identificados:**
| Patrón | Uso en este proyecto |
|--------|---------------------|
| LLM as Interface Layer | DeepSeek como puerta de entrada |
| Agent-Based Decomposition | Módulos como agentes especializados |
| AI-Orchestrated Workflows | Flujos dirigidos por el modelo |
| Feedback Loops as Architecture | Validación humana integrada |

---

### 5. **Context-Aware Development**
**Fuente:** Airbyte, Statsig, Sparkco

**5 Técnicas de optimización de contexto:**

| Técnica | Aplicación |
|---------|------------|
| **RAG (Retrieval Augmented Generation)** | Recuperar solo chunks relevantes de docs |
| **Prompt Compression** | Resumir historial de conversaciones |
| **Selective Context** | Cargar solo lo necesario por decisión |
| **Semantic Chunking** | Dividir docs manteniendo coherencia |
| **Multi-turn Summarization** | Mantener últimos 5-7 mensajes completos |

---

### 6. **Documentation-as-Code Synchronization**
**Fuente:** Mintlify, GitBook, Docusaurus

**Metodologías:**
- Schema-based auto-generation
- Git-based versioning
- CI/CD pipeline integration
- Live collaboration & changelogs

---

## 📐 Metodología de Organización Modular

### Principio Fundamental

> **Cada módulo debe tener 1-3 funcionalidades claramente documentadas en su README.md**

### Estructura de un Módulo

```
modules/
└── [nombre-modulo]/
    ├── INDEX.md              # ← LO QUE LA IA LEE PRIMERO
    ├── actions.ts            # 1-3 funciones máximo
    ├── types.ts              # Tipos TypeScript
    ├── events.ts             # Eventos emitidos/recibidos
    ├── manifest.json         # Metadatos estructurados
    └── README.md             # Documentación completa
```

### Contenido de INDEX.md (Documento de Índice)

```markdown
# [Nombre del Módulo]

## Funcionalidades (1-3)
1. `[nombreFuncion1]` - Descripción en 1 línea
2. `[nombreFuncion2]` - Descripción en 1 línea

## Flujo de Datos
- **Entrada:** [qué recibe]
- **Procesamiento:** [qué hace]
- **Salida:** [qué devuelve]

## Eventos
- **Emite:** `[nombre-evento]` cuando [condición]
- **Escucha:** `[nombre-evento]` para [acción]

## Dependencias
- [módulo-depenedencia] - Para [razón]

## Ejemplo de Uso
```typescript
import { accion1, accion2 } from './actions';
```
```

---

## 🔗 Sincronización Código-Documentación-Comentarios

### Regla de Oro

> **Todo cambio de código DEBE actualizar:**
> 1. Comentarios inline (encima de la función, no dentro)
> 2. INDEX.md del módulo
> 3. manifest.json (si cambia la interfaz)

### Estructura de Comentarios

```typescript
/**
 * [nombreFuncion] - [verbo en presente] [qué hace]
 * 
 * @param param1 - [descripción del parámetro]
 * @returns [qué devuelve]
 * @throws [cuándo lanza error]
 * 
 * @example
 * ```typescript
 * const result = await nombreFuncion({ param1: 'valor' });
 * ```
 * 
 * @module [nombre-modulo]
 * @related [INDEX.md](./INDEX.md)
 */
export async function nombreFuncion({ param1 }: Params): Promise<Result> {
  // Implementación
}
```

---

## 🧠 Flujo de Trabajo con IA

### Cuando la IA necesita modificar código:

1. **Paso 1:** Leer `INDEX.md` del módulo relevante
2. **Paso 2:** Entender funcionalidades actuales (1-3)
3. **Paso 3:** Si la nueva funcionalidad cabe en el módulo → modificar
4. **Paso 4:** Si excede 3 funcionalidades → crear nuevo módulo
5. **Paso 5:** Actualizar INDEX.md y manifest.json
6. **Paso 6:** Ejecutar tests del módulo

### Cuando la IA necesita crear nuevo módulo:

1. **Paso 1:** Crear carpeta `modules/nuevo-modulo/`
2. **Paso 2:** Crear `INDEX.md` con estructura estándar
3. **Paso 3:** Crear `actions.ts` con 1-3 funciones
4. **Paso 4:** Crear `manifest.json` con metadatos
5. **Paso 5:** Registrar módulo en `modules/registry.json`

---

## 📊 Métricas de Calidad Modular

| Métrica | Umbral Ideal | Acción si excede |
|---------|--------------|------------------|
| Funciones por módulo | 1-3 | Dividir en sub-módulos |
| Líneas por archivo | <200 | Extraer a utilidades |
| Dependencias directas | <3 | Refactorizar acoplamiento |
| Eventos emitidos | <5 | Consolidar eventos |
| Tamaño INDEX.md | <50 líneas | Resumir o dividir |

---

## 🛠️ Herramientas Recomendadas

| Categoría | Herramienta | Uso |
|-----------|-------------|-----|
| Docs-as-Code | Mintlify | Generación automática desde código |
| Sincronización | GitBook Git Sync | Versionado junto con código |
| Análisis estático | ESLint + SonarQube | Validar estructura modular |
| Testing | Vitest + Playwright | Tests unitarios y E2E |
| IA | GitHub Copilot + Claude Code | Generación de código |

---

## 📝 Checklist de Implementación

### Fase 1: Análisis (Semana 1)
- [ ] Auditar código actual
- [ ] Identificar límites de capacidades
- [ ] Definir estructura de carpetas modular
- [ ] Crear plantilla de INDEX.md

### Fase 2: Refactorización (Semanas 2-4)
- [ ] Extraer primera capacidad a módulo independiente
- [ ] Crear INDEX.md para cada módulo
- [ ] Implementar manifest.json
- [ ] Configurar validación automática

### Fase 3: Sincronización (Semanas 5-6)
- [ ] Configurar Mintlify/GitBook
- [ ] Crear pipeline CI/CD para docs
- [ ] Establecer reglas de comentarios
- [ ] Documentar flujos de trabajo con IA

### Fase 4: Optimización IA (Semanas 7-8)
- [ ] Implementar RAG para documentación
- [ ] Configurar contexto selectivo
- [ ] Crear sandbox para experimentación IA
- [ ] Validar con pruebas reales

---

## 🔐 Principios de Seguridad

1. **Nunca** exponer API keys en código o comentarios
2. **Siempre** validar inputs en cada función exportada
3. **Siempre** emitir eventos para acciones críticas (auditoría)
4. **Nunca** permitir que IA ejecute código sin revisión humana
5. **Siempre** mantener lógica sensible bajo supervisión humana

---

## 📚 Referencias

1. [Capability-Based Architecture Guide](https://dev.to/gd-tech-guru/capability-based-architecture-a-practical-guide-to-portability-isolation-and-ai-readiness-2g4h)
2. [Model Context Protocol](https://modelcontextprotocol.io/)
3. [AI Coding Best Practices 2025](https://dev.to/ranndy360/ai-coding-best-practices-in-2025-4eel)
4. [5 AI Context Window Optimization Techniques](https://airbyte.com/agentic-data/ai-context-window-optimization-techniques)
5. [The Rise of Modular Development](https://dev.to/jaideepparashar/the-rise-of-modular-development-building-tech-that-builds-itself-30p8)
6. [Emerging Architecture Patterns for AI-Native Enterprise](https://www.catio.tech/blog/emerging-architecture-patterns-for-the-ai-native-enterprise)
7. [Best API Documentation Tools 2025](https://www.mintlify.com/blog/best-api-documentation-tools-of-2025)

---

*Documento vivo - se actualiza con cada iteración de la metodología*
*Última actualización: 2026-02-24*

```

---

### 📄 docs/AUDITORIA-CAPACIDADES.md

**Descripción:** Capacidades discretas, estructura modular

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/AUDITORIA-CAPACIDADES.md`

```markdown
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

```

---

### 📄 docs/estado.md

**Descripción:** Estado de implementación, problemas conocidos

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/estado.md`

```markdown
# Estado de Implementación - Agente de Cambio

## Fecha: 2026-02-23
## Versión: 0.1.0 (Prototipo Funcional)

### ✅ COMPLETADO

#### 1. Infraestructura Base
- [x] Estructura de monorepo con npm workspaces
- [x] Configuración TypeScript para frontend y backend
- [x] Configuración de variables de entorno
- [x] Scripts de desarrollo concurrentes

#### 2. Backend (Node.js + Socket.IO)
- [x] Servidor Express con Socket.IO
- [x] Cliente DeepSeek API con streaming SSE
- [x] Sistema de sesiones en memoria
- [x] Endpoints REST para compatibilidad
- [x] Eventos Socket.IO definidos (tipos TypeScript)
- [x] Gestión básica de prompts y métricas de deriva
- [x] Health check endpoint

#### 3. Frontend (Next.js + React)
- [x] Configuración Next.js 14 con App Router
- [x] Sistema de diseño con Tailwind CSS + Glassmorphism
- [x] Componentes premium con Framer Motion
- [x] Store global con Zustand (persistencia)
- [x] Socket.IO client provider
- [x] Componentes de UI:
  - [x] Header con logo y controles
  - [x] Reasoning toggle animado
  - [x] Mode switcher (chat/cuestionario)
  - [x] Chat container con burbujas de mensajes
  - [x] Prompt editor editable
  - [x] Panel de objetivos
  - [x] Delta meter visual
  - [x] Input de chat y cuestionario

#### 4. Integración Básica
- [x] Conexión Socket.IO frontend-backend
- [x] Envío de mensajes desde frontend
- [x] Actualización de prompt en tiempo real
- [x] Recepción de respuestas streaming (backend)
- [x] API REST funcional con DeepSeek

#### 5. Documentación
- [x] README.md completo con instrucciones
- [x] Plan maestro del proyecto (proyecto.md)
- [x] Lista de rutas de archivos (rutas.md)
- [x] Copia de requerimientos originales
- [x] Copia de diseño del sistema

### 🚧 EN PROGRESO

#### 1. Integración Socket.IO Completa
- [ ] Streaming de texto en tiempo real en UI
- [ ] Manejo de eventos de cuestionario
- [ ] Sincronización de estado entre instancias
- [ ] Reconexión automática y manejo de errores

#### 2. Algoritmos Avanzados
- [ ] Métricas de deriva semántica real (no simuladas)
- [ ] Algoritmo de negociación de cambios de prompt
- [ ] Sistema de doble instancia (Arquitecto/Ejecutor)
- [ ] Evaluación de merecimiento de cambios

#### 3. Experiencia de Usuario
- [ ] Animaciones de streaming de texto
- [ ] Indicadores de conexión mejorados
- [ ] Notificaciones de eventos del sistema
- [ ] Historial de conversaciones persistente
- [ ] Exportación de reportes .md

### 📋 PENDIENTE

#### 1. Características Críticas
- [ ] Persistencia con Redis (sesiones, mensajes)
- [ ] Panel de administración y logs
- [ ] Sistema de autenticación (opcional)
- [ ] Límites de uso y rate limiting

#### 2. Optimizaciones
- [ ] Caché de contexto de DeepSeek
- [ ] Compresión de mensajes
- [ ] Bundle optimization (frontend)
- [ ] Lazy loading de componentes

#### 3. Pruebas y Calidad
- [ ] Tests unitarios (backend/frontend)
- [ ] Tests de integración Socket.IO
- [ ] Tests E2E con Playwright
- [ ] Load testing

#### 4. Despliegue
- [ ] Configuración Docker
- [ ] CI/CD pipeline
- [ ] Variables de entorno por entorno
- [ ] Monitoreo y alertas

### 🐛 PROBLEMAS CONOCIDOS

1. **Socket.IO streaming UI**: Los chunks de streaming no se muestran en tiempo real en la UI (solo mensaje completo)
2. **Métricas de deriva simuladas**: El cálculo de delta es simplificado (longitud de texto)
3. **Error handling básico**: Falta manejo robusto de errores de API DeepSeek
4. **ESLint version conflict**: Se usa --legacy-peer-deps por conflicto de versiones
5. **Next.js security warning**: Versión 14.2.28 tiene vulnerabilidad conocida (actualizar pronto)

### 🔄 PRÓXIMOS PASOS (Inmediatos)

1. **Implementar streaming UI**: Mostrar texto carácter por carácter en burbujas de chat
2. **Mejorar cálculo de delta**: Implementar algoritmo de similitud semántica
3. **Agregar modo cuestionario funcional**: Preguntas dinámicas basadas en contexto
4. **Persistencia local mejorada**: Guardar sesiones en localStorage con cifrado
5. **Panel de diagnóstico**: Mostrar logs de conexión y eventos en tiempo real

### 📊 MÉTRICAS ACTUALES

- **Tiempo de respuesta API**: < 2s (DeepSeek API)
- **Conexión WebSocket**: Estable con reconexión automática
- **Bundle size frontend**: ~1.5MB (desarrollo)
- **Líneas de código**: ~1500 (TypeScript/JavaScript)
- **Componentes React**: 15+

### 🧪 PRUEBAS REALIZADAS

1. ✅ Servidor inicia correctamente (puerto 3001)
2. ✅ Frontend inicia correctamente (puerto 3000)
3. ✅ API REST responde con DeepSeek
4. ✅ Conexión Socket.IO establecida
5. ✅ Estado persistente en localStorage
6. ✅ Animaciones funcionan (Framer Motion)
7. ✅ Responsive design básico

### 🔗 DEPENDENCIAS EXTERNAS

- **DeepSeek API**: Motor de inferencia principal (gratuito)
- **Socket.IO**: Comunicación en tiempo real
- **Framer Motion**: Animaciones React
- **Tailwind CSS**: Estilización utilitaria
- **Zustand**: Gestión de estado
- **date-fns**: Manipulación de fechas
- **lucide-react**: Iconos

### 📈 ESTADO GENERAL

**Prototipo funcional mínimo (MVP)** alcanzado. El sistema puede:
- Recibir mensajes del usuario via WebSocket
- Enviar a DeepSeek API y recibir respuesta
- Mostrar interfaz premium con animaciones
- Editar system prompt en tiempo real
- Calcular métricas básicas de deriva

**Falta** integración completa de streaming y algoritmos avanzados de negociación de prompt.

---

*Este documento se actualiza automáticamente con cada commit importante.*
*Última actualización: 2026-02-23*
```

---

### 📄 apps/web/tailwind.config.js

**Descripción:** Tokens de diseño, colores, animaciones

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Cognitive color palette
        cognitive: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        reasoning: {
          50: '#fdf4ff',
          100: '#fae8ff',
          200: '#f5d0fe',
          300: '#f0abfc',
          400: '#e879f9',
          500: '#d946ef',
          600: '#c026d3',
          700: '#a21caf',
          800: '#86198f',
          900: '#701a75',
        },
        success: '#00ff41',
        warning: '#fbbf24',
        error: '#ef4444',
      },
      animation: {
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'typing': 'typing 1.5s steps(4, end) infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 10px rgba(14, 165, 233, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(14, 165, 233, 0.8)' },
        },
        typing: {
          '0%': { width: '0' },
          '100%': { width: '1.25em' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))',
        'cognitive-gradient': 'linear-gradient(135deg, #0ea5e9, #d946ef)',
      },
    },
  },
  plugins: [],
};
```

---

### 📄 apps/web/app/globals.css

**Descripción:** Glassmorphism CSS, scrollbar, animaciones

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/app/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 255, 255, 255;
  --background-start-rgb: 13, 2, 8;
  --background-end-rgb: 0, 20, 40;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 13, 2, 8;
    --background-end-rgb: 0, 20, 40;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
  min-height: 100vh;
  overflow-x: hidden;
}

/* Glassmorphism styles */
.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.glass-input {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
}

.glass-input:focus {
  border-color: rgba(14, 165, 233, 0.5);
  box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.2);
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(14, 165, 233, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(14, 165, 233, 0.5);
}

/* Typing indicator */
.typing-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.typing-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: rgba(14, 165, 233, 0.7);
  animation: typing-bounce 1.4s infinite ease-in-out both;
}

.typing-dot:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing-bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* Message bubble animations */
@keyframes message-in {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message-enter {
  animation: message-in 0.3s ease-out forwards;
}
```

---

### 📄 apps/web/app/store/chatStore.ts

**Descripción:** Estado global: modos, mensajes, prompt, métricas

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/app/store/chatStore.ts`

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type ChatMode = 'chat' | 'questionnaire';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    reasoning?: boolean;
    mode?: ChatMode;
    deltaScore?: number;
  };
}

export interface PromptMutation {
  id: string;
  timestamp: Date;
  change: string;
  reason: string;
  deltaImpact: number;
  approved: boolean;
}

export interface Question {
  id: string;
  type: 'single_choice' | 'multiple_choice' | 'yes_no' | 'open';
  question: string;
  options?: Array<{
    id: string;
    label: string;
    value: string;
  }>;
}

export interface DeltaMetrics {
  currentScore: number;
  threshold: number;
  requiresApproval: boolean;
  changes: {
    additions: number;
    deletions: number;
    semanticShift: number;
  };
}

interface ChatStore {
  // Session state
  sessionId: string | null;
  setSessionId: (id: string) => void;

  // Chat state
  messages: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;

  // Mode state
  mode: ChatMode;
  setMode: (mode: ChatMode) => void;

  // Prompt state
  systemPrompt: string;
  setSystemPrompt: (prompt: string) => void;
  promptMutations: PromptMutation[];
  addPromptMutation: (mutation: PromptMutation) => void;

  // Reasoning state
  isReasoning: boolean;
  toggleReasoning: () => void;
  setIsReasoning: (value: boolean) => void;

  // Questionnaire state
  currentQuestion: Question | null;
  setCurrentQuestion: (question: Question | null) => void;

  // Delta metrics
  deltaMetrics: DeltaMetrics | null;
  setDeltaMetrics: (metrics: DeltaMetrics | null) => void;

  // Objectives
  objectives: string[];
  addObjective: (objective: string) => void;
  removeObjective: (index: number) => void;

  // UI state
  isConnected: boolean;
  setIsConnected: (connected: boolean) => void;
  isStreaming: boolean;
  setIsStreaming: (streaming: boolean) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      // Session
      sessionId: null,
      setSessionId: (id) => set({ sessionId: id }),

      // Messages
      messages: [],
      addMessage: (message) => set((state) => ({
        messages: [...state.messages, message]
      })),
      clearMessages: () => set({ messages: [] }),

      // Mode
      mode: 'chat',
      setMode: (mode) => set({ mode }),

      // Prompt
      systemPrompt: `Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente.`,
      setSystemPrompt: (prompt) => set({ systemPrompt: prompt }),
      promptMutations: [],
      addPromptMutation: (mutation) => set((state) => ({
        promptMutations: [...state.promptMutations, mutation],
      })),

      // Reasoning
      isReasoning: false,
      toggleReasoning: () => set((state) => ({ isReasoning: !state.isReasoning })),
      setIsReasoning: (value) => set({ isReasoning: value }),

      // Questionnaire
      currentQuestion: null,
      setCurrentQuestion: (question) => set({ currentQuestion: question }),

      // Delta metrics
      deltaMetrics: null,
      setDeltaMetrics: (metrics) => set({ deltaMetrics: metrics }),

      // Objectives
      objectives: [],
      addObjective: (objective) => set((state) => ({
        objectives: [...state.objectives, objective],
      })),
      removeObjective: (index) => set((state) => ({
        objectives: state.objectives.filter((_, i) => i !== index),
      })),

      // UI state
      isConnected: false,
      setIsConnected: (connected) => set({ isConnected: connected }),
      isStreaming: false,
      setIsStreaming: (streaming) => set({ isStreaming: streaming }),
    }),
    {
      name: 'chat-storage',
      partialize: (state) => ({
        sessionId: state.sessionId,
        messages: state.messages,
        systemPrompt: state.systemPrompt,
        objectives: state.objectives,
      }),
    }
  )
);
```

---

### 📄 apps/server/src/types/socket.ts

**Descripción:** Tipos compartidos, eventos Socket.IO

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/server/src/types/socket.ts`

```typescript
export interface ServerToClientEvents {
  'message:stream': (chunk: string) => void;
  'message:complete': (message: ChatMessage) => void;
  'prompt:mutation': (mutation: PromptMutation) => void;
  'question:next': (question: Question) => void;
  'mode:switch': (mode: 'chat' | 'questionnaire') => void;
  'delta:update': (delta: DeltaMetrics) => void;
  'error': (error: string) => void;
}

export interface ClientToServerEvents {
  'message:send': (content: string, mode: 'chat' | 'questionnaire', context: MessageContext) => void;
  'prompt:update': (content: string) => void;
  'option:select': (questionId: string, optionId: string, comment?: string) => void;
  'mode:set': (mode: 'chat' | 'questionnaire') => void;
  'reasoning:toggle': (enabled: boolean) => void;
  'session:init': (sessionId?: string) => void;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    reasoning?: boolean;
    mode?: 'chat' | 'questionnaire';
    deltaScore?: number;
  };
}

export interface PromptMutation {
  id: string;
  timestamp: Date;
  change: string;
  reason: string;
  deltaImpact: number;
  approved: boolean;
}

export interface Question {
  id: string;
  type: 'single_choice' | 'multiple_choice' | 'yes_no' | 'open';
  question: string;
  options?: Array<{
    id: string;
    label: string;
    value: string;
  }>;
}

export interface DeltaMetrics {
  currentScore: number;
  threshold: number;
  requiresApproval: boolean;
  changes: {
    additions: number;
    deletions: number;
    semanticShift: number;
  };
}

export interface MessageContext {
  isReasoning: boolean;
  sessionId: string;
  objectives?: string[];
}

export interface Session {
  id: string;
  messages: ChatMessage[];
  systemPrompt: string;
  objectives: string[];
  currentQuestion?: Question;
  createdAt: Date;
  updatedAt: Date;
}
```

---

### 📄 apps/web/components/layout/Header.tsx

**Descripción:** Cabecera con logo y controles

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/layout/Header.tsx`

```typescript
'use client';

import { motion } from 'framer-motion';
import { Brain, Zap, Settings, User } from 'lucide-react';
import { ReasoningToggle } from './ReasoningToggle';
import { useChatStore } from '@/app/store/chatStore';

export function Header() {
  const { isConnected } = useChatStore();

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="flex items-center justify-between px-6 py-4 border-b border-white/10 glass-panel m-4 mb-0 rounded-2xl"
    >
      {/* Logo */}
      <div className="flex items-center gap-3">
        <motion.div
          whileHover={{ rotate: 180 }}
          transition={{ duration: 0.5 }}
          className="w-10 h-10 rounded-xl bg-gradient-to-br from-cognitive-500 to-reasoning-500 flex items-center justify-center shadow-lg shadow-cognitive-500/25"
        >
          <Brain className="w-5 h-5 text-white" />
        </motion.div>
        <div>
          <h1 className="text-lg font-bold text-white tracking-tight">
            Cognitive Server
          </h1>
          <div className="flex items-center gap-2">
            <span className={`flex h-2 w-2 rounded-full ${isConnected ? 'bg-success' : 'bg-error'} animate-pulse`} />
            <span className="text-xs text-white/50">
              {isConnected ? 'Sistema Activo' : 'Desconectado'}
            </span>
          </div>
        </div>
      </div>

      {/* Center - Reasoning Toggle */}
      <ReasoningToggle />

      {/* Right Actions */}
      <div className="flex items-center gap-2">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 rounded-lg hover:bg-white/10 text-white/70 transition-colors"
        >
          <Zap className="w-5 h-5" />
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 rounded-lg hover:bg-white/10 text-white/70 transition-colors"
        >
          <Settings className="w-5 h-5" />
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/10 hover:bg-white/15 transition-colors"
        >
          <div className="w-6 h-6 rounded-full bg-gradient-to-br from-cognitive-400 to-cognitive-600 flex items-center justify-center">
            <User className="w-3 h-3 text-white" />
          </div>
          <span className="text-sm text-white/80">Usuario</span>
        </motion.button>
      </div>
    </motion.header>
  );
}
```

---

### 📄 apps/web/components/layout/ModeSwitcher.tsx

**Descripción:** Toggle chat/cuestionario

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/layout/ModeSwitcher.tsx`

```typescript
'use client';

import { motion } from 'framer-motion';
import { MessageSquare, ListTodo, ArrowRightLeft } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function ModeSwitcher() {
  const { mode, setMode } = useChatStore();

  return (
    <div className="flex items-center justify-center">
      <div className="relative flex items-center p-1 rounded-2xl bg-white/5 border border-white/10">
        {/* Background indicator */}
        <motion.div
          layoutId="mode-indicator"
          className="absolute inset-y-1 rounded-xl bg-cognitive-500/20 border border-cognitive-500/30"
          style={{
            width: 'calc(50% - 4px)',
            left: mode === 'chat' ? '4px' : 'calc(50%)',
          }}
          transition={{ type: "spring", stiffness: 400, damping: 30 }}
        />

        {/* Chat Mode Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setMode('chat')}
          className={`relative z-10 flex items-center gap-2 px-6 py-2.5 rounded-xl transition-colors ${
            mode === 'chat' ? 'text-cognitive-400' : 'text-white/50 hover:text-white/70'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span className="text-sm font-medium">Chat</span>
        </motion.button>

        {/* Questionnaire Mode Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setMode('questionnaire')}
          className={`relative z-10 flex items-center gap-2 px-6 py-2.5 rounded-xl transition-colors ${
            mode === 'questionnaire' ? 'text-cognitive-400' : 'text-white/50 hover:text-white/70'
          }`}
        >
          <ListTodo className="w-4 h-4" />
          <span className="text-sm font-medium">Cuestionario</span>
        </motion.button>
      </div>

      {/* Mode indicator badge */}
      <motion.div
        key={mode}
        initial={{ opacity: 0, x: 10 }}
        animate={{ opacity: 1, x: 0 }}
        className="ml-4 px-3 py-1 rounded-full bg-white/5 border border-white/10"
      >
        <span className="text-xs text-white/50 flex items-center gap-1">
          <ArrowRightLeft className="w-3 h-3" />
          {mode === 'chat' ? 'Conversación fluida' : 'Navegación guiada'}
        </span>
      </motion.div>
    </div>
  );
}
```

---

### 📄 apps/web/components/layout/ReasoningToggle.tsx

**Descripción:** Activar modo reasoning

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/layout/ReasoningToggle.tsx`

```typescript
'use client';

import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function ReasoningToggle() {
  const { isReasoning, toggleReasoning } = useChatStore();

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleReasoning}
      className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all duration-300 ${
        isReasoning
          ? 'bg-reasoning-500/20 border border-reasoning-500/50 shadow-lg shadow-reasoning-500/20'
          : 'bg-white/5 border border-white/10 hover:bg-white/10'
      }`}
    >
      <motion.div
        animate={isReasoning ? { rotate: [0, 15, -15, 0] } : {}}
        transition={{ duration: 0.5, repeat: isReasoning ? Infinity : 0, repeatDelay: 2 }}
      >
        <Sparkles className={`w-4 h-4 ${isReasoning ? 'text-reasoning-500' : 'text-white/50'}`} />
      </motion.div>

      <span className={`text-sm font-medium ${isReasoning ? 'text-reasoning-500' : 'text-white/70'}`}>
        Razonamiento
      </span>

      <div className={`w-10 h-5 rounded-full relative transition-colors ${
        isReasoning ? 'bg-reasoning-500' : 'bg-white/20'
      }`}>
        <motion.div
          animate={{ x: isReasoning ? 20 : 2 }}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
          className="absolute top-1 w-3 h-3 rounded-full bg-white shadow-md"
        />
      </div>
    </motion.button>
  );
}
```

---

### 📄 apps/web/components/chat/ChatContainer.tsx

**Descripción:** Contenedor principal

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/chat/ChatContainer.tsx`

```typescript
'use client';

import { useChatStore } from '@/app/store/chatStore';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { Questionnaire } from './Questionnaire';
import { motion } from 'framer-motion';

export function ChatContainer() {
  const { mode, messages, isStreaming } = useChatStore();

  return (
    <div className="flex flex-col h-[600px] glass-panel rounded-2xl p-4">
      {/* Chat header */}
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-white/10">
        <h2 className="text-xl font-bold text-white">
          {mode === 'chat' ? 'Conversación Cognitiva' : 'Cuestionario Guiado'}
        </h2>
        <div className="text-sm text-white/50">
          {messages.length} mensajes
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-2 space-y-4">
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center h-full text-white/40"
          >
            <div className="text-4xl mb-4">🧠</div>
            <p className="text-lg mb-2">Inicia una conversación</p>
            <p className="text-sm">Escribe un mensaje o selecciona una opción del cuestionario</p>
          </motion.div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}

        {/* Typing indicator */}
        {isStreaming && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 p-4 glass-panel rounded-2xl"
          >
            <div className="typing-indicator">
              <div className="typing-dot" />
              <div className="typing-dot" />
              <div className="typing-dot" />
            </div>
            <span className="text-white/50 text-sm">El sistema está escribiendo...</span>
          </motion.div>
        )}
      </div>

      {/* Input area */}
      <div className="mt-4 pt-4 border-t border-white/10">
        {mode === 'questionnaire' ? (
          <Questionnaire />
        ) : (
          <ChatInput />
        )}
      </div>
    </div>
  );
}
```

---

### 📄 apps/web/components/chat/ChatMessage.tsx

**Descripción:** Burbuja de mensaje animada

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/chat/ChatMessage.tsx`

```typescript
'use client';

import { motion } from 'framer-motion';
import { User, Bot, Settings } from 'lucide-react';
import { ChatMessage as ChatMessageType } from '@/app/store/chatStore';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  const Icon = isUser ? User : isSystem ? Settings : Bot;
  const bgColor = isUser
    ? 'bg-cognitive-500/20 border-cognitive-500/30'
    : isSystem
    ? 'bg-purple-500/20 border-purple-500/30'
    : 'bg-white/5 border-white/10';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${bgColor}`}>
        <Icon className="w-4 h-4" />
      </div>

      {/* Message bubble */}
      <div className={`flex-1 ${isUser ? 'items-end' : ''}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-medium text-white/70">
            {message.role === 'user' ? 'Tú' : message.role === 'system' ? 'Sistema' : 'Cognitive Server'}
          </span>
          <span className="text-xs text-white/30">
            {format(new Date(message.timestamp), 'HH:mm', { locale: es })}
          </span>
        </div>
        <div
          className={`p-4 rounded-2xl border ${bgColor} ${isUser ? 'rounded-tr-none' : 'rounded-tl-none'}`}
        >
          <p className="text-white whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    </motion.div>
  );
}
```

---

### 📄 apps/web/components/chat/ChatInput.tsx

**Descripción:** Input de texto modo chat

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/chat/ChatInput.tsx`

```typescript
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Mic } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';
import { useSocket } from '@/components/providers/SocketProvider';

export function ChatInput() {
  const [input, setInput] = useState('');
  const { mode, isReasoning, sessionId, addMessage } = useChatStore();

  const { sendMessage, isConnected } = useSocket();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to store
    const userMessage = {
      id: `msg_${Date.now()}`,
      role: 'user' as const,
      content: input,
      timestamp: new Date(),
      metadata: { mode, reasoning: isReasoning },
    };
    addMessage(userMessage);

    // Send via Socket.IO
    if (isConnected) {
      sendMessage(input);
    } else {
      console.error('Socket not connected');
      // Fallback: Add mock AI response
      setTimeout(() => {
        addMessage({
          id: `msg_${Date.now() + 1}`,
          role: 'assistant',
          content: '⚠️ Modo demo: El servidor no está conectado. Conecta el backend para respuestas reales.',
          timestamp: new Date(),
          metadata: { mode, reasoning: isReasoning },
        });
      }, 1000);
    }

    // Clear input
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <div className="flex-1 relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu mensaje aquí..."
          className="w-full glass-input rounded-2xl px-4 py-3 pr-12 text-white placeholder-white/30 resize-none focus:outline-none"
          rows={3}
        />
        <button
          type="button"
          className="absolute right-3 top-3 text-white/50 hover:text-white/80"
        >
          <Mic className="w-5 h-5" />
        </button>
      </div>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        type="submit"
        className="self-end px-6 py-3 rounded-2xl bg-gradient-to-r from-cognitive-500 to-cognitive-600 text-white font-medium flex items-center gap-2"
      >
        <Send className="w-4 h-4" />
        Enviar
      </motion.button>
    </form>
  );
}
```

---

### 📄 apps/web/components/chat/Questionnaire.tsx

**Descripción:** Renderizado de preguntas

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/chat/Questionnaire.tsx`

```typescript
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function Questionnaire() {
  const [comment, setComment] = useState('');
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
  const { currentQuestion, addMessage } = useChatStore();

  const handleOptionSelect = (optionId: string) => {
    if (!currentQuestion) return;

    if (currentQuestion.type === 'multiple_choice') {
      setSelectedOptions((prev) =>
        prev.includes(optionId)
          ? prev.filter((id) => id !== optionId)
          : [...prev, optionId]
      );
    } else {
      setSelectedOptions([optionId]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQuestion) return;

    // Create message from selection
    const selectedText = currentQuestion.options
      ?.filter((opt) => selectedOptions.includes(opt.id))
      .map((opt) => opt.label)
      .join(', ') || 'No selection';

    const messageContent = `Pregunta: ${currentQuestion.question}\nSelección: ${selectedText}\nComentario: ${comment}`;

    addMessage({
      id: `msg_${Date.now()}`,
      role: 'user',
      content: messageContent,
      timestamp: new Date(),
    });

    // TODO: Send via Socket.IO

    // Reset
    setSelectedOptions([]);
    setComment('');
  };

  if (!currentQuestion) {
    return (
      <div className="text-center p-8 text-white/50">
        Esperando primera pregunta del sistema...
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="glass-panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white mb-4">
          {currentQuestion.question}
        </h3>

        {currentQuestion.options && (
          <div className="space-y-2">
            {currentQuestion.options.map((option) => (
              <motion.button
                key={option.id}
                type="button"
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                onClick={() => handleOptionSelect(option.id)}
                className={`w-full text-left p-3 rounded-xl transition-colors ${
                  selectedOptions.includes(option.id)
                    ? 'bg-cognitive-500/30 border border-cognitive-500/50'
                    : 'bg-white/5 hover:bg-white/10 border border-transparent'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-4 h-4 rounded-full border ${
                    currentQuestion.type === 'multiple_choice'
                      ? 'rounded'
                      : 'rounded-full'
                  } ${
                    selectedOptions.includes(option.id)
                      ? 'bg-cognitive-500 border-cognitive-500'
                      : 'border-white/30'
                  }`} />
                  <span className="text-white">{option.label}</span>
                </div>
              </motion.button>
            ))}
          </div>
        )}
      </div>

      <div className="flex gap-2">
        <div className="flex-1">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Comentario adicional (opcional)..."
            className="w-full glass-input rounded-2xl px-4 py-3 text-white placeholder-white/30 resize-none focus:outline-none"
            rows={2}
          />
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          type="submit"
          className="self-end px-6 py-3 rounded-2xl bg-gradient-to-r from-cognitive-500 to-cognitive-600 text-white font-medium flex items-center gap-2"
        >
          <Send className="w-4 h-4" />
          Continuar
        </motion.button>
      </div>
    </form>
  );
}
```

---

### 📄 apps/web/components/prompt/PromptEditor.tsx

**Descripción:** Editor de system prompt

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/prompt/PromptEditor.tsx`

```typescript
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Edit2, Save, RefreshCw } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';
import { useSocket } from '@/components/providers/SocketProvider';

export function PromptEditor() {
  const { systemPrompt, setSystemPrompt } = useChatStore();
  const [editing, setEditing] = useState(false);
  const [draftPrompt, setDraftPrompt] = useState(systemPrompt);

  const { updatePrompt } = useSocket();

  const handleSave = () => {
    setSystemPrompt(draftPrompt);
    setEditing(false);
    // Emit prompt update via Socket.IO
    updatePrompt(draftPrompt);
  };

  const handleReset = () => {
    const defaultPrompt = `Eres un sistema de EXTRACCIÓN COGNITIVA de alto nivel.
Tu misión es capturar la esencia de las ideas, problemas y metas del usuario.
Reglas fijas:
1. Nunca rompas el personaje del rol asignado.
2. En modo cuestionario, ofrece preguntas clave de forma secuencial o agrupada.
3. En modo chat, responde libremente manteniendo el rol profesional.
4. Actualiza siempre el 'DOCUMENTO DE CONCLUSIONES' internamente.`;
    setDraftPrompt(defaultPrompt);
    setSystemPrompt(defaultPrompt);
  };

  return (
    <div className="glass-panel rounded-2xl p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Edit2 className="w-5 h-5" />
          Prompt del Sistema
        </h3>
        <div className="flex gap-2">
          {editing ? (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setEditing(false)}
                className="px-3 py-1 rounded-lg bg-white/10 text-white/70 text-sm"
              >
                Cancelar
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSave}
                className="px-3 py-1 rounded-lg bg-cognitive-500 text-white text-sm flex items-center gap-1"
              >
                <Save className="w-3 h-3" />
                Guardar
              </motion.button>
            </>
          ) : (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setEditing(true)}
                className="px-3 py-1 rounded-lg bg-white/10 text-white/70 text-sm"
              >
                Editar
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleReset}
                className="px-3 py-1 rounded-lg bg-white/10 text-white/70 text-sm flex items-center gap-1"
              >
                <RefreshCw className="w-3 h-3" />
                Reset
              </motion.button>
            </>
          )}
        </div>
      </div>

      {editing ? (
        <textarea
          value={draftPrompt}
          onChange={(e) => setDraftPrompt(e.target.value)}
          className="w-full glass-input rounded-xl p-3 text-white font-mono text-sm h-64 resize-none focus:outline-none"
          spellCheck={false}
        />
      ) : (
        <div className="glass-input rounded-xl p-3 h-64 overflow-y-auto">
          <pre className="text-white/80 font-mono text-sm whitespace-pre-wrap">
            {systemPrompt}
          </pre>
        </div>
      )}

      <div className="mt-3 text-xs text-white/50">
        {editing ? (
          <p>Edita el prompt del sistema. Los cambios afectarán el comportamiento del AI.</p>
        ) : (
          <p>Prompt actual del sistema. Haz clic en "Editar" para modificarlo.</p>
        )}
      </div>
    </div>
  );
}
```

---

### 📄 apps/web/components/metrics/DeltaMeter.tsx

**Descripción:** Visualización de deriva

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/metrics/DeltaMeter.tsx`

```typescript
'use client';

import { motion } from 'framer-motion';
import { AlertTriangle, Check } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function DeltaMeter() {
  const { deltaMetrics } = useChatStore();

  const score = deltaMetrics?.currentScore || 0;
  const threshold = deltaMetrics?.threshold || 0.3;
  const requiresApproval = deltaMetrics?.requiresApproval || false;

  const percentage = Math.min(100, (score / threshold) * 100);

  return (
    <div className="glass-panel rounded-2xl p-4">
      <h3 className="text-lg font-semibold text-white mb-3">Métrica de Deriva</h3>

      <div className="space-y-4">
        {/* Visual meter */}
        <div className="relative h-6 bg-white/5 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 1, type: 'spring' }}
            className={`absolute h-full rounded-full ${
              requiresApproval
                ? 'bg-gradient-to-r from-warning to-error'
                : 'bg-gradient-to-r from-cognitive-400 to-cognitive-600'
            }`}
          />

          {/* Threshold line */}
          <div
            className="absolute top-0 bottom-0 w-0.5 bg-white/50"
            style={{ left: `${(threshold / threshold) * 100}%` }}
          />
        </div>

        {/* Labels */}
        <div className="flex justify-between text-sm">
          <span className="text-white/70">Baja</span>
          <span className="text-white/70">Umbral: {threshold}</span>
          <span className="text-white/70">Alta</span>
        </div>

        {/* Score display */}
        <div className="flex items-center justify-between">
          <div>
            <div className="text-2xl font-bold text-white">{score.toFixed(2)}</div>
            <div className="text-xs text-white/50">Score actual</div>
          </div>

          <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${
            requiresApproval
              ? 'bg-warning/20 text-warning'
              : 'bg-success/20 text-success'
          }`}>
            {requiresApproval ? (
              <>
                <AlertTriangle className="w-4 h-4" />
                <span className="text-sm font-medium">Requiere aprobación</span>
              </>
            ) : (
              <>
                <Check className="w-4 h-4" />
                <span className="text-sm font-medium">Dentro del rango</span>
              </>
            )}
          </div>
        </div>

        {/* Details */}
        {deltaMetrics && (
          <div className="grid grid-cols-3 gap-2 pt-3 border-t border-white/10">
            <div className="text-center p-2 bg-white/5 rounded-lg">
              <div className="text-xs text-white/50">Adiciones</div>
              <div className="text-white font-semibold">{deltaMetrics.changes.additions}</div>
            </div>
            <div className="text-center p-2 bg-white/5 rounded-lg">
              <div className="text-xs text-white/50">Eliminaciones</div>
              <div className="text-white font-semibold">{deltaMetrics.changes.deletions}</div>
            </div>
            <div className="text-center p-2 bg-white/5 rounded-lg">
              <div className="text-xs text-white/50">Shift Semántico</div>
              <div className="text-white font-semibold">
                {deltaMetrics.changes.semanticShift.toFixed(2)}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

---

### 📄 apps/web/components/objectives/ObjectivesPanel.tsx

**Descripción:** Panel de objetivos

**Ruta absoluta:** `/home/daniel/tron/programas/Agente-De-Cambio-STABLE/apps/web/components/objectives/ObjectivesPanel.tsx`

```typescript
'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Target, Plus, Trash2, Check } from 'lucide-react';
import { useChatStore } from '@/app/store/chatStore';

export function ObjectivesPanel() {
  const { objectives, addObjective, removeObjective } = useChatStore();
  const [newObjective, setNewObjective] = useState('');
  const [editingIndex, setEditingIndex] = useState<number | null>(null);

  const handleAdd = () => {
    if (newObjective.trim()) {
      addObjective(newObjective.trim());
      setNewObjective('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAdd();
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Target className="w-5 h-5" />
          Objetivos Activos
        </h3>
        <span className="text-xs text-white/50">{objectives.length} objetivos</span>
      </div>

      {/* Add objective input */}
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newObjective}
          onChange={(e) => setNewObjective(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Añadir nuevo objetivo..."
          className="flex-1 glass-input rounded-xl px-3 py-2 text-white placeholder-white/30 focus:outline-none"
        />
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleAdd}
          className="px-3 py-2 rounded-xl bg-cognitive-500 text-white"
        >
          <Plus className="w-4 h-4" />
        </motion.button>
      </div>

      {/* Objectives list */}
      <AnimatePresence>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {objectives.length === 0 ? (
            <div className="text-center py-4 text-white/40">
              No hay objetivos definidos
            </div>
          ) : (
            objectives.map((objective, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="flex items-center gap-2 p-3 rounded-xl bg-white/5 border border-white/10"
              >
                <Check className="w-4 h-4 text-cognitive-400 flex-shrink-0" />
                <div className="flex-1 text-sm text-white">{objective}</div>
                <button
                  onClick={() => removeObjective(index)}
                  className="p-1 text-white/50 hover:text-error transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </motion.div>
            ))
          )}
        </div>
      </AnimatePresence>

      <div className="mt-4 pt-3 border-t border-white/10 text-xs text-white/50">
        <p>Los objetivos se inyectan en el prompt del sistema para guiar la conversación.</p>
      </div>
    </div>
  );
}
```

---

## 📊 Resumen

- **Total de archivos planificados:** 20
- **Archivos incluidos:** 20
- **Archivos no encontrados:** 0
- **Fecha de generación:** mié 25 feb 2026 09:03:33 -04

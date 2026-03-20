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
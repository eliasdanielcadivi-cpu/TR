# Rutas de Documentos y Archivos del Proyecto

## Documentación
- `/docs/proyecto.md` - Plan maestro del proyecto, etapas y arquitectura
- `/docs/rutas.md` - Este archivo: lista de rutas de todos los documentos
- `/docs/Apideepseek.md` - Documentación de la API de DeepSeek (copiada desde original)

## Frontend (Next.js)
- `/apps/web/app/page.tsx` - Página principal
- `/apps/web/app/layout.tsx` - Layout raíz
- `/apps/web/app/globals.css` - Estilos globales Tailwind
- `/apps/web/app/store/chatStore.ts` - Store Zustand para estado de chat
- `/apps/web/components/` - Componentes React
  - `/layout/Header.tsx` - Header con logo y controles
  - `/layout/ReasoningToggle.tsx` - Toggle de razonamiento
  - `/layout/ModeSwitcher.tsx` - Selector de modo chat/cuestionario
  - `/chat/ChatContainer.tsx` - Contenedor principal de chat
  - `/chat/ChatMessage.tsx` - Componente de mensaje individual
  - `/chat/ChatInput.tsx` - Input para modo chat
  - `/chat/Questionnaire.tsx` - Componente para cuestionario
  - `/prompt/PromptEditor.tsx` - Editor de system prompt
  - `/metrics/DeltaMeter.tsx` - Métricas de deriva visual
  - `/objectives/ObjectivesPanel.tsx` - Panel de objetivos
  - `/providers/SocketProvider.tsx` - Provider de Socket.IO
  - `/providers/StoreProvider.tsx` - Provider de store
- `/apps/web/package.json` - Dependencias del frontend
- `/apps/web/tailwind.config.js` - Configuración de Tailwind CSS
- `/apps/web/next.config.js` - Configuración de Next.js
- `/apps/web/tsconfig.json` - Configuración de TypeScript

## Backend (Node.js + Socket.IO)
- `/apps/server/src/index.ts` - Servidor principal Express + Socket.IO
- `/apps/server/src/clients/deepseek.ts` - Cliente de DeepSeek API con streaming
- `/apps/server/src/types/socket.ts` - Tipos TypeScript para Socket.IO
- `/apps/server/package.json` - Dependencias del backend
- `/apps/server/tsconfig.json` - Configuración de TypeScript
- `/apps/server/.env` - Variables de entorno (API key, puerto)
- `/apps/server/.env.example` - Ejemplo de variables de entorno

## Configuración Global
- `/package.json` - Configuración monorepo con workspaces
- `/docs/proyecto.md` - Plan maestro del proyecto

## Herramientas y Scripts
- `/scripts/` - Scripts de utilidad (pendiente)
- `/herramientas/` - Herramientas TRON nativas (pendiente)

## Archivos Originales (referencia)
- `/home/daniel/tron/programas/AgenteDeCambio/` - Proyecto original
  - `server.js` - Servidor Express original
  - `public/index.html` - Frontend original
  - `package.json` - Dependencias originales
  - `.env` - Variables de entorno originales
  - `docs/Apideepseek.md` - Documentación API DeepSeek

## Requerimientos y Diseño
- `/home/daniel/Escritorio/BORRAR/ListaRequerimientos.md` - Lista completa de requerimientos del sistema
- `/home/daniel/Escritorio/BORRAR/sistema-por-kimi.md` - Diseño detallado de interfaz y servidor

## Estructura de Carpetas
```
Agente-De-Cambio/
├── apps/
│   ├── web/                    # Frontend Next.js
│   │   ├── app/
│   │   ├── components/
│   │   ├── store/
│   │   └── public/
│   └── server/                 # Backend Node.js
│       ├── src/
│       ├── dist/
│       └── test/
├── docs/
├── packages/
├── scripts/
└── herramientas/
```

## Notas
- Esta lista se actualizará conforme el proyecto evolucione.
- Las rutas son relativas a la raíz del proyecto (`/home/daniel/tron/programas/Agente-De-Cambio/`).
- Los documentos de requerimientos originales se mantienen en sus ubicaciones originales por referencia.
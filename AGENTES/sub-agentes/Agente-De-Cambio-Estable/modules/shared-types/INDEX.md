# Shared Types

## Funcionalidades (1-3)

1. `Tipos TypeScript` - Definiciones de tipos compartidos frontend/backend
2. `Interfaces` - Contratos de datos para mensajes, sesiones, eventos
3. `Utilidades` - Tipos utilitarios para manipulación de datos

## Flujo de Datos

- **Entrada:** Ninguna (módulo solo-tipos, sin runtime)
- **Procesamiento:** N/A (tipos se eliminan en compilación)
- **Salida:** Tipos TypeScript para importación

## Eventos

### Emite
- Ninguno (módulo de tipos, no emite eventos)

### Escucha
- Ninguno

## Dependencias

| Módulo | Para qué |
|--------|----------|
| Ninguna | Módulo puro de tipos, sin dependencias externas |

## Ejemplo de Uso

```typescript
import type { 
  ChatMessage, 
  Session, 
  ChatMode,
  ServerToClientEvents 
} from './types';

// Usar tipos en frontend o backend
const message: ChatMessage = {
  id: 'msg_123',
  role: 'user',
  content: 'Hola',
  timestamp: new Date()
};

const mode: ChatMode = 'chat';

// Tipos de eventos Socket.IO
const handlers: ServerToClientEvents = {
  'message:stream': (chunk) => console.log(chunk),
  'message:complete': (msg) => console.log(msg)
};
```

## Estructura del Módulo

```
shared-types/
├── INDEX.md      # Este archivo
├── types.ts      # Todos los tipos exportados
└── manifest.json # Metadatos
```

---

**Versión:** 0.1.0  
**Última actualización:** 2026-02-24  
**Mantenido por:** AgenteDeCambio2 Team

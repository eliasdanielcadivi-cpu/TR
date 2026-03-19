# Session Manager

## Funcionalidades (1-3)

1. `createSession` - Crea nueva sesión con valores por defecto
2. `getSession` - Obtiene sesión existente por ID
3. `updateSession` - Actualiza campos de sesión (parcial)

## Flujo de Datos

- **Entrada:** ID de sesión (opcional para crear) + actualizaciones parciales
- **Procesamiento:** Almacenamiento en memoria (Map)
- **Salida:** Objetos Session completos o booleanos de éxito

## Eventos

### Emite
- Ninguno (módulo stateless con almacenamiento interno)

### Escucha
- Ninguno

## Dependencias

| Módulo | Para qué |
|--------|----------|
| @agentedecambio2/shared-types | Tipos Session, ChatMessage |

## Ejemplo de Uso

```typescript
import { 
  createSession, 
  getSession, 
  updateSession,
  deleteSession,
  listSessions 
} from './actions';

// Ejemplo 1: Crear sesión
const session = createSession();
console.log(session.id); // 'sess_1234567890_abc'
console.log(session.messages.length); // 0

// Ejemplo 2: Obtener sesión
const retrieved = getSession(session.id);
console.log(retrieved?.systemPrompt); // Prompt por defecto

// Ejemplo 3: Actualizar sesión
updateSession(session.id, {
  systemPrompt: 'Nuevo prompt personalizado',
  objectives: ['Objetivo 1', 'Objetivo 2']
});

// Ejemplo 4: Listar sesiones
const allSessions = listSessions();
console.log(allSessions); // ['sess_...']

// Ejemplo 5: Eliminar sesión
deleteSession(session.id);
```

## Estructura del Módulo

```
session-manager/
├── INDEX.md      # Este archivo
├── actions.ts    # Funciones exportadas (6)
└── manifest.json # Metadatos
```

---

**Versión:** 0.1.0  
**Última actualización:** 2026-02-24  
**Mantenido por:** AgenteDeCambio2 Team

# Prompt Engine

## Funcionalidades (1-3)

1. `buildSystemPrompt` - Construye prompt con contexto y modo
2. `updatePrompt` - Actualiza prompt con validación de deriva
3. `negotiateChange` - Negocia cambios propuestos al prompt

## Flujo de Datos

- **Entrada:** Prompt base + objetivos + modo
- **Procesamiento:** Combina elementos, valida deriva
- **Salida:** System prompt completo estructurado

## Eventos

### Emite
- Ninguno (módulo stateless)

### Escucha
- Ninguno

## Dependencias

| Módulo | Para qué |
|--------|----------|
| @agentedecambio2/shared-types | Tipos Session |
| @agentedecambio2/delta-calculator | Calcular deriva de cambios |

## Ejemplo de Uso

```typescript
import { 
  buildSystemPrompt, 
  updatePrompt, 
  negotiateChange,
  getDefaultPrompt 
} from './actions';

// Ejemplo 1: Construir prompt con contexto
const prompt = buildSystemPrompt({
  basePrompt: 'Eres un asistente de código',
  objectives: ['Ayudar con TypeScript', 'Enseñar buenas prácticas'],
  mode: 'chat'
});

// Ejemplo 2: Actualizar prompt con validación
const session = getSession(sessionId);
const result = updatePrompt(session, 'Nuevo prompt', false);

if (result.success) {
  console.log('Prompt actualizado correctamente');
} else if (result.requiresApproval) {
  console.log('Requiere aprobación del usuario');
}

// Ejemplo 3: Negociar cambio propuesto
const negotiation = negotiateChange(oldPrompt, newPrompt);
console.log(negotiation.recommendation); // 'ACCEPT' | 'REVIEW' | 'REJECT'

// Ejemplo 4: Obtener prompt por defecto
const defaultPrompt = getDefaultPrompt();
```

## Estructura del Módulo

```
prompt-engine/
├── INDEX.md      # Este archivo
├── actions.ts    # Funciones exportadas (4)
└── manifest.json # Metadatos
```

---

**Versión:** 0.1.0  
**Última actualización:** 2026-02-24  
**Mantenido por:** AgenteDeCambio2 Team

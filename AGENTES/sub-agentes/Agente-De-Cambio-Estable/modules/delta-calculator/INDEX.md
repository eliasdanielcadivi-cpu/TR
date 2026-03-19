# Delta Calculator

## Funcionalidades (1-3)

1. `calculate` - Calcula deriva entre dos prompts (0.0 a 1.0)
2. `compare` - Compara prompts y retorna métricas detalladas
3. `threshold` - Obtiene umbral configurado para aprobación

## Flujo de Datos

- **Entrada:** Dos strings (oldPrompt, newPrompt)
- **Procesamiento:** Calcula diferencia de longitud normalizada
- **Salida:** Score numérico 0.0-1.0 + métricas detalladas

## Eventos

### Emite
- Ninguno (módulo stateless, funciones puras)

### Escucha
- Ninguno

## Dependencias

| Módulo | Para qué |
|--------|----------|
| Ninguno | Módulo puro, sin dependencias externas |

## Ejemplo de Uso

```typescript
import { calculate, compare, threshold, requiresApproval } from './actions';

// Ejemplo 1: Calcular deriva simple
const oldPrompt = 'Eres un asistente útil';
const newPrompt = 'Eres un asistente muy útil y amable';
const delta = calculate(oldPrompt, newPrompt);
console.log(`Deriva: ${(delta * 100).toFixed(2)}%`);

// Ejemplo 2: Comparación detallada
const comparison = compare(oldPrompt, newPrompt);
console.log(comparison);
// {
//   deltaScore: 0.35,
//   threshold: 0.3,
//   requiresApproval: true,
//   changes: { additions: 15, deletions: 0, semanticShift: 0.35 }
// }

// Ejemplo 3: Verificar si requiere aprobación
if (requiresApproval(delta)) {
  console.log('El cambio requiere aprobación del usuario');
}
```

## Estructura del Módulo

```
delta-calculator/
├── INDEX.md      # Este archivo
├── actions.ts    # Funciones exportadas (4)
└── manifest.json # Metadatos
```

---

**Versión:** 0.1.0  
**Última actualización:** 2026-02-24  
**Mantenido por:** AgenteDeCambio2 Team

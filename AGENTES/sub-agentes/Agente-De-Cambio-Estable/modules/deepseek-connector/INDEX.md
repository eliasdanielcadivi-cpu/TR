# DeepSeek Connector

## Funcionalidades (1-3)

1. `createCompletion` - Solicita completación síncrona a DeepSeek API
2. `createCompletionStream` - Stream de respuesta en tiempo real (SSE)

## Flujo de Datos

- **Entrada:** Array de mensajes + API Key + configuración (modelo, temperatura)
- **Procesamiento:** HTTP POST a https://api.deepseek.com/chat/completions
- **Salida:** Respuesta JSON con contenido generado + estadísticas de tokens

## Eventos

### Emite
- Ninguno (módulo stateless, solo funciones puras)

### Escucha
- Ninguno

## Dependencias

| Módulo | Para qué |
|--------|----------|
| axios (npm) | Cliente HTTP para requests a DeepSeek API |

## Ejemplo de Uso

```typescript
import { createCompletion, createCompletionStream } from './actions';

// Ejemplo 1: Completación síncrona
const response = await createCompletion({
  messages: [
    { role: 'system', content: 'Eres un asistente útil.' },
    { role: 'user', content: 'Hola' }
  ],
  apiKey: process.env.DEEPSEEK_API_KEY,
  temperature: 0.7
});
console.log(response.choices[0].message.content);

// Ejemplo 2: Streaming
const stream = createCompletionStream({
  messages: [{ role: 'user', content: 'Escribe algo' }],
  apiKey: process.env.DEEPSEEK_API_KEY
});

for await (const chunk of stream) {
  const text = chunk.choices[0]?.delta?.content || '';
  process.stdout.write(text);
}
```

## Estructura del Módulo

```
deepseek-connector/
├── INDEX.md          # Este archivo
├── actions.ts        # Funciones exportadas (2)
├── types.ts          # Tipos TypeScript (re-exports de actions.ts)
└── manifest.json     # Metadatos estructurados
```

---

**Versión:** 0.1.0  
**Última actualización:** 2026-02-24  
**Mantenido por:** AgenteDeCambio2 Team

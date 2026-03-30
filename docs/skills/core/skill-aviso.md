# skill-aviso

## Propósito
Gestionar recordatorios y alarmas en lenguaje natural.

## Cuándo usar
- "recuérdame en 10min..."
- "alarma a las 8am..."
- "aviso el 25/12..."
- "programa un comando..."

## Entradas requeridas
- `tiempo`: relativo (10min) o absoluto (8:00, 25/12)
- `mensaje`: texto del recordatorio

## Flujo de ejecución
1. **Comando Base:** `aviso`
2. **Sintaxis Natural:**
   - `aviso en <tiempo> "<mensaje>"`
   - `aviso a las <hora> "<mensaje>"`
   - `aviso el <fecha> "<mensaje>"`
   - `aviso comando "<cmd>" ...`

## Ejemplos
- `aviso en 15min "sacar la pizza"`
- `aviso a las 9am "reunión diaria"`
- `aviso el 01/01 "año nuevo"`

## Validaciones
- El daemon debe estar corriendo (se inicia con sesión gráfica).
- Verificar con `aviso lista`.

## Output JSON
```json
{
  "estado": "ok",
  "accion": "aviso_creado",
  "datos": {
    "fecha": "{fecha_calculada}",
    "mensaje": "{mensaje}"
  }
}
```

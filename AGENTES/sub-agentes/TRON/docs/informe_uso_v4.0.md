# Informe Detallado de Uso - TRON v4.0

## Resumen del Sistema

TRON v4.0 es un sistema operativo para proyectos que implementa una arquitectura orientada a objetos para la gestión inteligente de modelos de lenguaje, contabilidad de tokens y costos, y ejecución en modo batch. El sistema consta de dos clases principales:

- `TronCLI`: Clase que orquesta la ejecución de comandos
- `TronDBManager`: Clase que gestiona toda la interacción con la base de datos PocketBase

## Funcionalidades Principales

### 1. Gestión Inteligente de Modelos

La característica más importante de TRON v4.0 es la selección inteligente de modelos gratuitos de OpenRouter. El sistema:

- Detecta automáticamente cuando se solicita un modelo gratuito
- Verifica la salud del modelo (último fallo y conteo de fallos)
- Si el modelo solicitado está en cooldown o tiene demasiados fallos, selecciona automáticamente una alternativa gratuita saludable
- Implementa un sistema de penalización de 5 minutos para modelos que fallan

### 2. Contabilidad de Tokens y Costos

TRON v4.0 registra cada ejecución de modelo en la base de datos con información detallada:

- Tokens de entrada y salida
- Costo calculado basado en precios por millón de tokens
- Indicador si el modelo es gratuito o de pago
- Fecha y modelo utilizado

### 3. Visualización de Balance

Antes de ejecutar cualquier comando con OpenRouter, el sistema:

- Consulta el balance de la cuenta de OpenRouter
- Muestra créditos totales y restantes
- Calcula y muestra el costo estimado basado en la longitud del prompt

### 4. Modo Batch

El modo batch permite ejecutar comandos de forma persistente con:

- Reintentos automáticos con espera exponencial
- Manejo inteligente de fallos
- Selección automática de modelos alternativos cuando falla un modelo

### 5. Menú Interactivo de Modelos

Con el argumento `--router`, el sistema:

- Muestra una lista de modelos gratuitos y de bajo costo
- Indica el estado de salud de cada modelo con emojis (🟢 saludable, 🔴 con problemas)
- Permite al usuario seleccionar un modelo de la lista

## Comandos Disponibles

### Modo Interactivo
```bash
tron                    # Sesión interactiva con DeepSeek
tron --router           # Menú interactivo de selección de modelos
```

### Modo Scripting con Claude
```bash
tron -p "prompt"                           # Prompt rápido con DeepSeek
tron openrouter claude -p "prompt"         # Usar modelo por defecto de OpenRouter
tron openrouter google/gemini-flash-1.5 claude -p "prompt"  # Modelo específico
```

### Modo Batch
```bash
tron --batch openrouter claude -p "prompt persistente"  # Ejecución persistente
```

### Modo Wrapper Universal
```bash
tron deepseek python3 script.py          # Ejecutar script Python con entorno
tron openrouter env | grep ANTHROPIC     # Ver variables de entorno
```

## Configuración

El archivo `tron_config.yaml` contiene:

- Credenciales para diferentes proveedores (DeepSeek, OpenRouter)
- Credenciales de PocketBase para la base de datos
- Definición de perfiles de ejecución
- Variables de entorno globales

## Estructura del Código

### TronCLI
- Parseo de argumentos con argparse
- Carga de configuración
- Inicialización de la base de datos
- Construcción del entorno
- Lógica de selección inteligente de modelos
- Ejecución en modo simple o batch
- Manejo de post-ejecución (registro de tokens, manejo de errores)

### TronDBManager
- Conexión y autenticación con PocketBase
- Inicialización de colecciones
- Sincronización de datos de mercado de OpenRouter
- Selección inteligente de modelos
- Consulta de balance de OpenRouter
- Registro de ejecuciones y fallos de modelos

## Beneficios del Sistema

1. **Eficiencia Económica**: Prioriza el uso de modelos gratuitos y saludables
2. **Robustez**: Manejo automático de fallos y reintentos inteligentes
3. **Transparencia**: Visualización clara de costos y balance antes de ejecutar
4. **Automatización**: Modo batch para tareas persistentes
5. **Contabilidad**: Registro detallado de tokens y costos por ejecución

## Casos de Uso Recomendados

1. **Desarrollo Rápido**: Usar `tron -p "prompt"` para pruebas rápidas
2. **Ejecución Persistente**: Usar `tron --batch` para tareas que deben continuar
3. **Optimización de Costos**: Usar `tron --router` para seleccionar modelos gratuitos
4. **Integración con Scripts**: Usar `tron profile command` para inyectar entornos

## Estado Actual

- Todas las funcionalidades principales están implementadas y probadas
- El sistema está listo para uso en producción
- Las pruebas básicas han sido exitosas
- La documentación está actualizada
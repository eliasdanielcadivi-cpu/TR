# Pruebas Interactivas para el Usuario - TRON v4.0

## Introducción

Este documento describe las pruebas interactivas que debes realizar manualmente para verificar completamente todas las funcionalidades de TRON v4.0. Estas pruebas requieren interacción humana y no pueden automatizarse completamente.

## Pruebas Requeridas

### 1. Prueba del Modo Interactivo con Claude

**Objetivo**: Verificar que el modo interactivo de Claude funciona correctamente con TRON.

**Pasos**:
1. Ejecuta: `tron`
2. Ingresa un prompt simple como "Hola, ¿cómo estás?"
3. Verifica que recibes una respuesta
4. Prueba salir del modo interactivo (usualmente con Ctrl+C o escribiendo "salir")

**Resultado Esperado**: 
- El sistema debe iniciar una sesión interactiva con Claude
- Debe responder a los prompts correctamente
- Debe permitir salir de la sesión

### 2. Prueba del Menú Interactivo de Modelos

**Objetivo**: Verificar que el menú interactivo de selección de modelos funciona correctamente.

**Pasos**:
1. Ejecuta: `tron --router`
2. Observa la lista de modelos gratuitos y de bajo costo
3. Verifica que los indicadores de salud (🟢/🔴) se muestran correctamente
4. Selecciona un modelo de la lista (ingresa el número correspondiente)
5. Verifica que el sistema confirma tu selección

**Resultado Esperado**:
- Se debe mostrar una lista de modelos disponibles
- Los indicadores de salud deben reflejar el estado real de los modelos
- El sistema debe aceptar tu selección y confirmarla

### 3. Prueba de la Funcionalidad de Prompt Directo

**Objetivo**: Verificar que los prompts directos funcionan correctamente.

**Pasos**:
1. Ejecuta: `tron -p "¿Qué es Python?"`
2. Observa la respuesta del sistema
3. Repite con un modelo específico: `tron openrouter claude -p "¿Cuál es la capital de Francia?"`

**Resultado Esperado**:
- El sistema debe procesar el prompt y devolver una respuesta
- La respuesta debe ser relevante al prompt
- Debe mostrar información de balance y costos estimados

### 4. Prueba de la Inyección de Variables de Entorno

**Objetivo**: Verificar que las variables de entorno se inyectan correctamente a otros programas.

**Pasos**:
1. Crea un archivo de prueba simple `test_env.py`:
   ```python
   import os
   print("ANTHROPIC_BASE_URL:", os.getenv('ANTHROPIC_BASE_URL'))
   print("ANTHROPIC_API_KEY:", os.getenv('ANTHROPIC_API_KEY'))
   ```
2. Ejecuta: `tron deepseek python3 test_env.py`
3. Verifica que las variables se hayan inyectado correctamente

**Resultado Esperado**:
- El script debe mostrar las variables de entorno correctamente
- Las variables deben coincidir con la configuración del perfil especificado

### 5. Prueba de la Selección Inteligente de Modelos

**Objetivo**: Verificar que el sistema selecciona inteligentemente modelos alternativos cuando el solicitado no está disponible.

**Pasos**:
1. Ejecuta: `tron openrouter google/gemini-flash-1.5 claude -p "Hola"`
2. Observa si el sistema usa el modelo solicitado o selecciona uno alternativo
3. Verifica que se muestre información sobre la selección inteligente

**Resultado Esperado**:
- Si el modelo solicitado está disponible y saludable, debe usarse
- Si no está disponible, debe seleccionarse un modelo alternativo gratuito
- Debe mostrarse un mensaje indicando la selección realizada

### 6. Prueba de la Interfaz de Usuario con Salida Formateada

**Objetivo**: Verificar que la interfaz de usuario con colores y formateo funciona correctamente.

**Pasos**:
1. Ejecuta cualquier comando de TRON con diferentes perfiles
2. Observa la salida en la terminal
3. Verifica que los colores y formateo se muestren correctamente

**Resultado Esperado**:
- La salida debe estar formateada con colores
- Deben mostrarse secciones claramente delineadas
- La información debe ser fácil de leer

## Consideraciones Importantes

- Asegúrate de tener conexión a internet para las pruebas que involucran APIs externas
- Verifica que PocketBase esté corriendo en `http://localhost:8090`
- Ten en cuenta que algunas pruebas pueden consumir créditos de API
- Si alguna prueba falla, revisa el archivo de configuración `tron_config.yaml`

## Reporte de Resultados

Después de completar cada prueba, registra:

- Fecha de la prueba
- Comando ejecutado
- Resultado observado
- Cualquier error o comportamiento inesperado
- Capturas de pantalla si es necesario

## Próximos Pasos

Una vez completadas todas las pruebas interactivas:

1. Revisa los resultados y documenta cualquier problema
2. Realiza ajustes necesarios basados en los hallazgos
3. Ejecuta nuevamente las pruebas si se hicieron modificaciones
4. Actualiza la documentación según sea necesario
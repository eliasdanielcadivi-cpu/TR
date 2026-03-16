# TRON v5.0 - Cliente Ligero de Modelos OpenRouter

## Descripción
TRON v5.0 es un cliente ligero enfocado exclusivamente en la exploración y selección de modelos de OpenRouter. A diferencia de versiones anteriores, esta versión se centra únicamente en la interfaz de usuario para seleccionar modelos, sin incluir funcionalidades de contabilidad de tokens ni costos.

## Características Principales

### 🤖 Menú Interactivo de Modelos (`--router`)
- Interfaz amigable con emojis
- Categorización por tipo de modelo (gratuitos, con herramientas, con visión, etc.)
- Búsqueda por nombre o proveedor
- Vista detallada de características de cada modelo
- Selección directa para usar con Claude u otros clientes

### 🔍 Vista Detallada de Modelos (`--see`)
- Información completa sobre un modelo específico
- Características especiales (herramientas, visión, audio, etc.)
- Precios detallados y contexto
- Arquitectura y capacidades

### 📦 Gestión de Datos
- Cache local de información de modelos (actualizado diariamente)
- Datos descargados directamente de la API de OpenRouter
- Almacenamiento eficiente en `~/.cache/tron_models/`

## Instalación

### Método 1: Instalador automático
```bash
chmod +x TRON/bin/install_tron5.sh
./TRON/bin/install_tron5.sh
```

### Método 2: Uso directo
```bash
python3 TRON/bin/tron_nuevo --router
```

## Comandos Disponibles

### Menú Interactivo de Modelos
```bash
tron5 --router
```
Abre el menú interactivo para explorar y seleccionar modelos.

### Ver Características de un Modelo
```bash
tron5 openrouter modelo-específico --see
```
Muestra información detallada sobre un modelo específico.

### Uso con Claude
```bash
# Primero seleccionar modelo con el menú
tron5 --router

# O usar directamente con un modelo
tron5 openrouter google/gemini-flash-1.5-001 claude -p "prompt"
```

## Interfaz del Menú

El menú interactivo presenta las siguientes categorías:

1. **Modelos Gratuitos** - Todos los modelos disponibles sin costo
2. **Modelos con Herramientas** - Modelos que soportan llamadas a herramientas
3. **Modelos con Visión** - Modelos que pueden procesar entradas de imagen
4. **Todos los Modelos** - Lista completa de modelos disponibles
5. **Búsqueda** - Buscar modelos por nombre o proveedor

Cada modelo se muestra con:
- Nombre e ID del modelo
- Precio por millón de tokens
- Longitud de contexto
- Iconos de características especiales (🛠️ herramientas, 🖼️ visión, etc.)

## Compatibilidad

TRON v5.0 es compatible con:
- Claude Code y otros clientes de IA
- Variables de entorno estándar
- Configuración de `tron_config.yaml`
- API de OpenRouter

## Configuración Requerida

El sistema requiere un archivo `tron_config.yaml` con la clave de API de OpenRouter:

```yaml
keys:
  openrouter_live: "sk-or-..."
```

## Ventajas sobre Versiones Anteriores

- **Simplicidad**: Sin contabilidad de tokens ni costos
- **Velocidad**: Interfaz más rápida y directa
- **Enfoque**: Únicamente para selección de modelos
- **Actualización automática**: Cache actualizado diariamente
- **Interfaz amigable**: Emojis y descripciones claras

## Casos de Uso

- Explorar modelos disponibles en OpenRouter
- Comparar características de diferentes modelos
- Seleccionar modelos óptimos para tareas específicas
- Integración con Claude u otros clientes de IA
- Evaluación de modelos para tareas que requieren herramientas, visión, etc.
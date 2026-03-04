# 📘 Guía de DeepSeek API para ARES

> Configuración y uso de DeepSeek API como provider alternativo en ARES.

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Configuración](#configuración)
3. [Uso desde ARES](#uso-desde-ares)
4. [Parámetros y Opciones](#parámetros-y-opciones)
5. [Comparativa con Gemma](#comparativa-con-gemma)
6. [Mejores Prácticas](#mejores-prácticas)

---

## 🚀 Introducción

### ¿Qué es DeepSeek?

**DeepSeek** es una API de IA que ofrece modelos de lenguaje avanzados con:
- ✅ Contexto extenso (hasta 128K tokens)
- ✅ Alto rendimiento en razonamiento
- ✅ Soporte para código y múltiples idiomas
- ✅ Pricing competitivo

### Modelos Disponibles

| Modelo | Uso Principal | Contexto |
|--------|---------------|----------|
| `deepseek-chat` | Conversacional, uso general | 128K |
| `deepseek-coder` | Programación y código | 128K |

---

## ⚙️ Configuración

### 1. Obtener API Key

1. Visitar [DeepSeek Platform](https://platform.deepseek.com/)
2. Crear cuenta o iniciar sesión
3. Ir a **API Keys** en el dashboard
4. Generar nueva API key
5. Guardar en lugar seguro

### 2. Configurar Variable de Entorno

```bash
# Añadir a ~/.bashrc o ~/.zshrc
export DEEPSEEK_API_KEY="tu-api-key-aqui"

# O crear archivo .env en TR/
echo "DEEPSEEK_API_KEY=tu-api-key-aqui" >> .env
```

### 3. Configurar en ARES

Editar `config/config.yaml`:

```yaml
ai:
  default_provider: "deepseek"  # Opcional: cambiar default
  
  deepseek:
    base_url: "https://api.deepseek.com"
    model: "deepseek-chat"
    api_key_env: "DEEPSEEK_API_KEY"
```

### 4. Verificar Configuración

```bash
# Ver configuración actual
ares config

# Test de conexión
ares p "Hola" --model deepseek
```

---

## 💻 Uso desde ARES

### Comandos Básicos

```bash
# Consulta simple con DeepSeek
ares p "¿Qué es Python?" --model deepseek

# Usar plantilla específica
ares p "Escribe un hello world" --model deepseek --template default

# Consulta con temperatura ajustada
ares p "Escribe un poema" --model deepseek --temperature 0.9
```

### Aliases Configurados

```yaml
# En config.yaml
aliases:
  deepseek:
    provider: "deepseek"
    model: "deepseek-chat"
```

```bash
# Usar alias
tr p "pregunta" --model deepseek
```

---

## 🎚️ Parámetros y Opciones

### Parámetros Soportados

| Parámetro | Rango | Default | Descripción |
|-----------|-------|---------|-------------|
| `temperature` | 0-2 | 0.7 | Creatividad vs determinismo |
| `max_tokens` | 1-8192 | 4096 | Longitud máxima de respuesta |
| `top_p` | 0-1 | 0.9 | Muestreo por núcleo |
| `frequency_penalty` | -2 a 2 | 0 | Penalización por frecuencia |
| `presence_penalty` | -2 a 2 | 0 | Penalización por presencia |

### Ejemplos de Configuración

```yaml
# Plantilla personalizada para DeepSeek
content: |
  {prompt}

config:
  model: "deepseek-chat"
  temperature: 0.7
  max_tokens: 4096
  top_p: 0.9
```

```bash
# Uso con parámetros explícitos
ares p "Resume este texto" --model deepseek --temperature 0.3 --max-tokens 500
```

---

## 📊 Comparativa con Gemma

| Característica | Gemma + Ollama | DeepSeek API |
|----------------|----------------|--------------|
| **Ejecución** | Local | Cloud (API) |
| **Privacidad** | Total | Depende del provider |
| **Latencia** | Variable (hardware) | Baja (cloud) |
| **Costo** | Gratis (tu hardware) | Por token usado |
| **Contexto** | Limitado por RAM | Hasta 128K |
| **Disponibilidad** | 24/7 local | Depende de API |
| **Modelos** | Gemma family | DeepSeek family |

### Cuándo Usar Cada Uno

**Gemma/Ollama:**
- ✅ Datos sensibles/privados
- ✅ Uso intensivo sin costo
- ✅ Sin dependencia de internet
- ✅ Baja latencia en red local

**DeepSeek API:**
- ✅ Consultas que requieren contexto extenso
- ✅ Hardware limitado
- ✅ Máxima calidad de respuesta
- ✅ Integración con ecosistema cloud

---

## 💡 Mejores Prácticas

### 1. Gestión de API Key

```bash
# ✅ Usar variables de entorno
export DEEPSEEK_API_KEY="sk-..."

# ✅ Usar archivo .env (no commitear)
# En .env:
DEEPSEEK_API_KEY=sk-...

# ❌ Nunca hardcodear en el código
api_key = "sk-..."  # MAL!
```

### 2. Optimización de Costos

```bash
# Usar max_tokens apropiado
ares p "resume en 100 palabras" --model deepseek --max-tokens 150

# Temperature baja para respuestas deterministas
ares p "extrae datos" --model deepseek --temperature 0.2

# Usar Gemma para consultas simples
ares p "suma 2+2" --model gemma  # Gratis
```

### 3. Manejo de Errores

```python
# El provider maneja errores automáticamente
# Posibles errores:
# - API key inválida
# - Rate limit excedido
# - Timeout de conexión
# - Saldo insuficiente
```

### 4. Monitoreo de Uso

```bash
# Verificar uso en dashboard de DeepSeek
# https://platform.deepseek.com/usage

# Configurar alerts de gasto
```

---

## 🔗 Recursos Oficiales

- [DeepSeek Platform](https://platform.deepseek.com/)
- [DeepSeek API Docs](https://platform.deepseek.com/api-docs/)
- [DeepSeek Models](https://platform.deepseek.com/models/)

---

*Documentación creada para ARES - Terminal Remote Operations Nexus*

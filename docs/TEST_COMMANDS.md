# 🧪 Comandos de Prueba para ARES

> Script y comandos manuales para verificar funcionalidad de ARES.

---

## ✅ Estado Actual

| Característica | Estado | Notas |
|----------------|--------|-------|
| `ares p "prompt"` | ✅ Funciona | Usa gemma3:4b por defecto |
| `ares p "prompt" --model gemma` | ✅ Funciona | Alias a gemma3:4b |
| `ares p "prompt" --template code` | ✅ Funciona | Usa gemma3:4b con template code |
| `ares p "prompt" --template chat` | ✅ Funciona | Template conversacional |
| `ares models` | ✅ Funciona | Lista modelos disponibles |
| `ares templates` | ✅ Funciona | Lista plantillas YAML |
| `ares tools` | ✅ Funciona | Lista herramientas |
| `ares config` | ✅ Funciona | Muestra configuración |
| DeepSeek API | ⚠️ Pendiente | Requiere configurar `DEEPSEEK_API_KEY` |

---

## 📜 Script de Pruebas Automáticas

### Ejecutar Script

```bash
cd /home/daniel/tron/programas/TR/papelera
./test_ares_final.sh
```

### Ver Resultados

```bash
cat pruebas.txt
less pruebas.txt
```

---

## 🎯 Comandos Manuales de Prueba

### Consultas Básicas

```bash
# Consulta simple (default: gemma3:4b)
ares p "Hola, ¿cómo estás?"

# Con modelo específico
ares p "Hola" --model gemma3:4b
ares p "Hola" --model phi4-mini
ares p "Hola" --model llama3.1:8b
ares p "Hola" --model qwen2.5-coder:7b-instruct

# Con alias
ares p "Hola" --model gemma
```

### Con Plantillas

```bash
# Plantilla de código
ares p "Hello world en Python" --template code

# Plantilla de chat
ares p "Tengo una pregunta" --template chat

# Plantilla default
ares p "¿Qué es Python?" --template default

# Plantilla tools
ares p "¿Qué herramientas tienes?" --template tools
```

### Con Temperatura

```bash
# Temperatura baja (determinista)
ares p "2+2=" --temperature 0.2

# Temperatura media (balance)
ares p "Cuenta hasta 5" --temperature 0.7

# Temperatura alta (creativo)
ares p "Escribe un haiku sobre IA" --temperature 0.9
```

### Combinaciones

```bash
# Modelo + plantilla
ares p "Optimiza esta función" --model gemma3:4b --template code

# Modelo + temperatura
ares p "Escribe un cuento" --model gemma3:4b --temperature 0.8

# Plantilla + temperatura
ares p "Explica este código" --template code --temperature 0.3
```

### Comandos de Información

```bash
# Ver configuración actual
ares config

# Listar modelos disponibles
ares models

# Listar plantillas YAML
ares templates

# Listar herramientas
ares tools

# Ver ayuda
ares --help
ares p --help
```

---

## 🛠️ Comandos de Debugging

### Verificar Providers

```bash
cd /home/daniel/tron/programas/TR
source .venv/bin/activate

python3 -c "
from modules.ia.ai_engine import AIEngine
from config import TRContext
ctx = TRContext()
ai = AIEngine(ctx.config.get('ai', {}), ctx.base_path)
print('Providers:', list(ai._providers.keys()))
print('Default:', ai.default_provider)
"
```

### Verificar Ollama

```bash
# Ver modelos en Ollama
curl http://localhost:11434/api/tags | python3 -m json.tool

# Ver info de un modelo
curl http://localhost:11434/api/show -d '{"model": "gemma3:4b"}' | python3 -m json.tool | head -50

# Probar Ollama directamente
ollama run gemma3:4b "Hola"
```

### Verificar Plantillas

```bash
python3 -c "
from modules.ia.templates import TemplateManager
tm = TemplateManager('modules/ia/templates')
print('Plantillas:', tm.list_templates())
for t in tm.list_templates():
    content = tm.get_template(*t.split('/'))
    print(f'{t}: {len(content) if content else 0} chars')
"
```

---

## 📊 Modelos Disponibles en Ollama

Según tests actuales:

| Modelo | Estado | Uso Recomendado |
|--------|--------|-----------------|
| `gemma3:4b` | ✅ Disponible | Uso general (default) |
| `gemma3:12b` | ❌ No disponible | - |
| `codellama:7b` | ✅ Disponible | Código (lento en cargar) |
| `phi4-mini:latest` | ✅ Disponible | Consultas rápidas |
| `llama3.1:8b` | ✅ Disponible | Uso general |
| `llama3.2:3b` | ✅ Disponible | Rápido, recursos limitados |
| `qwen2.5-coder:7b-instruct` | ✅ Disponible | Código |
| `qwen3:8b` | ✅ Disponible | Uso general |
| `deepseek-r1:8b` | ✅ Disponible | Razonamiento |

---

## 🔧 Solución de Problemas

### Error: "Aborted!"

**Causa:** Timeout en la carga del modelo.

**Solución:**
```bash
# Esperar a que Ollama termine de cargar
ollama run gemma3:4b ""

# O usar modelo más pequeño
ares p "Hola" --model llama3.2:3b
```

### Error: "API key de DeepSeek no configurada"

**Causa:** Falta variable de entorno.

**Solución:**
```bash
export DEEPSEEK_API_KEY="tu-key-aqui"
```

### Error: 404 Not Found

**Causa:** Modelo no existe en Ollama.

**Solución:**
```bash
# Verificar modelo disponible
ares models

# Descargar modelo
ollama pull gemma3:4b
```

### Error: Timeout

**Causa:** Modelo tardando en cargar.

**Solución:**
```bash
# Mantener modelo cargado
ollama run gemma3:4b ""

# O usar timeout mayor en código (ya está en 300s)
```

---

## 📁 Archivos de Pruebas

| Archivo | Propósito |
|---------|-----------|
| `papelera/test_ares_final.sh` | Script principal de pruebas |
| `papelera/pruebas.txt` | Resultados de pruebas (NO BORRAR) |
| `papelera/test_ares_simple.sh` | Versión simplificada |
| `papelera/test_ares.sh` | Script original completo |

---

## 📝 Comandos para Copiar y Pegar

```bash
# Prueba rápida
ares p "Hola"

# Prueba con plantilla code
ares p "Hello world en Python" --template code

# Ver plantillas
ares templates

# Ver modelos
ares models

# Script completo de pruebas
cd /home/daniel/tron/programas/TR/papelera && ./test_ares_final.sh
```

---

*Documentación creada para ARES - Terminal Remote Operations Nexus*

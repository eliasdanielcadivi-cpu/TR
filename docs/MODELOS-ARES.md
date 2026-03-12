# MODELOS-ARES — Documentación de Modelos Ollama

**Fecha:** 2026-03-09
**Estado:** Documentación inicial

---

## Modelos Disponibles

| Modelo | Padre | Propósito | Think Tags |
|--------|-------|-----------|------------|
| `ares:latest` | `alibayram/smollm3:latest` | Orquestador Táctico (salida limpia) | ❌ Eliminar |
| `ares-think:latest` | `alibayram/smollm3:latest` | Modo razonamiento (ver proceso) | ✅ Mantener |
| `smollm3:latest` | `alibayram/smollm3:latest` | Modelo base | ❌ Eliminar |
| `gemma3:4b` | `gemma3:4b` | Modelo general | ❌ Eliminar |
| `deepseek-chat` | API Remota | Fallback cloud | ❌ Eliminar |

---

## Modelfiles Originales

### ares:latest

**Archivo:** `bd/apollo/modelfiles.yaml`

```yaml
ares:latest:
  parent: alibayram/smollm3:latest
  description: "ARES - Orquestador Tactico (sin think)"
  system: "Eres ARES. Tu creador es Daniel Hung. Responde en espanol."
  parameters:
    temperature: 0.7
    top_p: 0.9
    num_predict: 2048
```

**Modelfile completo:**
```dockerfile
FROM alibayram/smollm3:latest

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_predict 2048

SYSTEM """Eres ARES. Tu creador es Daniel Hung. Responde en espanol."""
```

**Recrear:**
```bash
ollama create ares:latest -f Modelfile
```

---

### ares-think:latest

**Archivo:** `bd/apollo/modelfiles.yaml`

```yaml
ares-think:latest:
  parent: alibayram/smollm3:latest
  description: "ARES - Modo Think (con razonamiento)"
  system: "Eres ARES en modo razonamiento. Antes de responder, escribe razonamiento en etiquetas think."
  parameters:
    temperature: 0.4
    top_p: 0.9
    num_predict: 2048
  stop: []
```

**Modelfile completo:**
```dockerfile
FROM alibayram/smollm3:latest

PARAMETER temperature 0.4
PARAMETER top_p 0.9
PARAMETER num_predict 2048

SYSTEM """Eres ARES en modo razonamiento. Antes de responder, escribe razonamiento en etiquetas <think>."""
```

**Recrear:**
```bash
ollama create ares-think:latest -f Modelfile
```

---

## Comandos de Gestión

### Listar Modelos

```bash
# Ver modelos en Ollama
ollama list

# Ver modelos con ares model-creator
ares model-creator list
```

### Crear Modelo

```bash
# Desde padre
ares model-creator create ares-custom --from alibayram/smollm3:latest \
  --temperature 0.4 --top_p 0.9 --num_predict 2048

# Con system prompt
ares model-creator create ares-custom --from smollm3:latest \
  --system "Eres ARES..."
```

### Actualizar Modelo

```bash
# Cambiar parámetros
ares model-creator update ares-custom --temperature 0.7

# Cambiar system prompt
ares model-creator update ares-custom --system "Nuevo prompt..."
```

### Eliminar Modelo

```bash
ares model-creator delete ares-custom
```

### Mostrar Modelfile

```bash
ares model-creator show ares
ares model-creator show ares-think
```

---

## Post-procesamiento

Configurado en `config.yaml`:

```yaml
ai:
  post_processing:
    ares:
      strip_think_tags: true   # Eliminar <think></think>
    ares-think:
      strip_think_tags: false  # Mantener etiquetas
    smollm3:
      strip_think_tags: true
```

**Aplicación automática** en `generate_answer()` según modelo usado.

---

## Persistencia

**Archivo:** `bd/apollo/modelfiles.yaml`

**Estructura:**
```yaml
model_name:
  parent: modelo_base
  description: texto
  system: system_prompt
  parameters:
    temperature: float
    top_p: float
    num_predict: int
  stop: []
  created_at: timestamp
  updated_at: timestamp
```

**Backup:** Automático en cada modificación.

---

## Uso en Comandos

### ares p (consulta directa)

```bash
# Sin think (modelo normal)
ares p "¿Quién eres?" --model ares

# Con think (modelo pensante)
ares p "¿Quién eres?" --model ares-think

# Con RAG y think
ares p "¿Qué es Apollo?" --rag docs --think
```

### ares i (interactivo)

```bash
# Iniciar con modelo normal
ares i

# Iniciar con modelo pensante
ares i --think

# Cambiar en sesión
/model ares-think
/think on
```

---

## Referencias

- **TODO Principal:** `TODO-RAG-GRAFICO-SQLITE-VECTORIAL.md`
- **Configuración:** `config/config.yaml`
- **Persistencia:** `bd/apollo/modelfiles.yaml`
- **Generación:** `modules/ia/apollo/generation.py`

---

*Documento vivo. Actualizar con cada nuevo modelo creado.*

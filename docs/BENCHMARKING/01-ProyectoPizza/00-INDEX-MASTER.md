# 📊 BENCHMARKING: ProyectoPizza → ARES-TRON

> **Fecha:** 2026-03-18  
> **Origen:** `/home/daniel/tron/programas/ProyectoPizza/.claude` (289 files) + `.qwen` (38 files)  
> **Destino:** Unificación de contenido único para aprovechamiento en ARES-TRON  
> **Principio:** Una sola verdad, cero duplicación, máxima reutilización

---

## 🎯 RESUMEN EJECUTIVO

| Métrica | Valor |
|---------|-------|
| **Archivos únicos identificados** | 5 (excluyendo .venv y logs) |
| **Archivos idénticos en ambos** | 30+ (CLAUDE.md, skills, documentación) |
| **Contenido único en .qwen** | 0 (es subset estricto de .claude) |
| **Scripts reutilizables para ARES** | 3 (agente_git.py, git_core.py, gestor_git_cli.py) |
| **Configuraciones reutilizables** | 2 (settings.json, settings.local.json) |

---

## 📁 ESTRUCTURA DE CARPETAS

```
BENCHMARKING/ProyectoPizza/
├── 00-INDEX-MASTER.md           # ESTE ARCHIVO - Índice maestro
├── unique-content/              # Archivos únicos listos para integración
│   ├── settings.json            # Claude Code permissions firewall
│   ├── settings.local.json      # Extensiones locales de permisos
│   ├── agente_git.py            # Agente Git autónomo con Ollama
│   ├── git_core.py              # Clase base para operaciones Git
│   └── gestor_git_cli.py        # CLI JSON interface para Git
├── comparison-notes/            # Análisis detallado de diferencias
│   └── 01-analysis-report.md    # Reporte completo del agente
└── integration-guide/           # Guías de integración en ARES-TRON
    ├── 01-settings-integration.md
    ├── 02-git-tools-integration.md
    └── 03-architecture-notes.md
```

---

## 📦 CONTENIDO DE `unique-content/`

### 1. `settings.json` - Claude Code Security Firewall

**Propósito:** Configurar permisos y hooks de seguridad para Claude Code.

**Estructura:**
```json
{
  "permissions": {
    "allow": ["Bash(python3 TRON/CORE/despachador.py *)", ...],
    "deny": ["WebSearch", "WebFetch"]
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "python3 TRON/CORE/utilidades/verificador_peso.py"}]
    }]
  }
}
```

**Uso en ARES-TRON:**
- Copiar a `TR/.claude/settings.json`
- Actualizar rutas relativas al root de TR
- Mantener deny de WebSearch/WebFetch para forzar uso de herramientas TRON

**Token Efficiency:** ⭐⭐⭐⭐⭐ (Configuración única, cero tokens en runtime)

---

### 2. `settings.local.json` - Extensiones de Permisos Locales

**Propósito:** Extender permisos para desarrollo local sin modificar settings.json principal.

**Estructura:**
```json
{
  "permissions": {
    "allow": [
      "Bash(python3:*)",
      "Skill(docs)",
      "Skill(metaconocimiento)",
      "Skill(creador-herramientas)",
      "Bash(chmod:*)",
      "Bash(curl:*)",
      "Skill(gestor-git)"
    ]
  }
}
```

**Uso en ARES-TRON:**
- Copiar a `TR/.claude/settings.local.json`
- Permite uso de Skills sin pedir confirmación
- Habilita curl y chmod para automatización

**Token Efficiency:** ⭐⭐⭐⭐⭐ (Una vez configurado, cero overhead)

---

### 3. `agente_git.py` - Agente Git Autónomo

**Propósito:** Agente conversacional que ejecuta operaciones Git mediante tool calling con Ollama.

**Modelo:** `functiongemma:270m` (local, lightweight)

**Comandos soportados:**
| Acción | Descripción | Parámetro |
|--------|-------------|-----------|
| `guardar` | Commit seguro con verificación de peso | `-m "mensaje"` |
| `volver` | Revertir cambios (non-destructive) | `-p N` (pasos) |
| `nube` | Sync pull+push | Ninguno |

**Arquitectura:**
```
User Input → Ollama (function calling) → herramienta_git_tron() 
           → gestor_git_cli.py (subprocess) → GitCore class → Git
```

**Uso en ARES-TRON:**
- Mover a `TR/programas/ares/modules/git/agente_git.py`
- Cambiar modelo a configuración de ARES
- Actualizar rutas BASE_DIR

**Token Efficiency:** ⭐⭐⭐ (Requiere LLM en cada operación, pero modelo local)

**⚠️ Advertencia:** Este script es para interacción conversacional autónoma. Para automatización directa, usar `gestor_git_cli.py`.

---

### 4. `git_core.py` - Clase Base para Operaciones Git

**Propósito:** Abstracción OO de operaciones Git con logging y verificación de peso.

**Clase:** `GitCore`

**Métodos:**
| Método | Descripción | Retorna |
|--------|-------------|---------|
| `guardar_cambios(mensaje)` | Add + Commit con verificación de peso | JSON {estado, mensaje} |
| `retroceder_seguro(pasos)` | Git revert (non-destructive) | JSON {estado, mensaje} |
| `sincronizar_nube()` | Pull (rebase) + Push | JSON {estado, mensaje} |

**Características clave:**
- ✅ **Portabilidad:** Usa `Path(__file__)` para rutas absolutas
- ✅ **Logging:** Auditoría en `TRON/logs/git_ops.log`
- ✅ **Verificación de peso:** Hook antes de commit
- ✅ **JSON output:** Determinista para automatización
- ✅ **Safe revert:** Usa `git revert` en lugar de `git reset`

**Uso en ARES-TRON:**
- Mover a `TR/programas/ares/core/git_core.py`
- Actualizar LOG_DIR a estándar TR
- Integrar con sistema de logging de ARES

**Token Efficiency:** ⭐⭐⭐⭐⭐ (Código puro, cero tokens en runtime)

**Ejemplo de uso:**
```python
from core.git_core import GitCore

core = GitCore()
resultado = core.guardar_cambios("feat: add new module")
print(resultado["estado"])  # "exito" | "error" | "neutro"
```

---

### 5. `gestor_git_cli.py` - CLI JSON Interface

**Propósito:** Wrapper CLI para GitCore con salida JSON determinista.

**Comandos:**
```bash
python gestor_git_cli.py guardar -m "mensaje"
python gestor_git_cli.py volver -p 3
python gestor_git_cli.py nube
```

**Salida:**
```json
{"estado": "exito", "mensaje": "Checkpoint guardado: 'mensaje'"}
```

**Uso en ARES-TRON:**
- Mover a `TR/programas/ares/tools/git_cli.py`
- Añadir `--help` por convención TRON
- Usar en scripts bash y wrappers

**Token Efficiency:** ⭐⭐⭐⭐⭐ (Herramienta CLI, cero tokens)

**Integración con bash:**
```bash
resultado=$(python git_cli.py guardar -m "commit")
estado=$(echo $resultado | jq -r '.estado')
```

---

## 🔍 COMPARISON NOTES

**Veredicto:** `.qwen` es subset estricto de `.claude`. No hay contenido único en `.qwen`.

**Archivos idénticos verificados (30+):**
- `CLAUDE.md` ✅
- `rules/protocolos_tron.md` ✅
- `TRON/LEEME_TRON.md` ✅
- `TRON/CORE/despachador.py` ✅
- `TRON/CORE/gestion_git.py` ✅
- `TRON/CORE/utilidades/verificador_peso.py` ✅
- `TRON/CORE/requirements.txt` ✅
- 8x `skills/*/SKILL.md` ✅
- 8x `TRON/gestion/*.md` ✅
- 3x `TRON/CORE/comandos/*.md` ✅

**Archivos únicos en `.claude` (7, excluyendo .venv/logs):**
1. `settings.json`
2. `settings.local.json`
3. `TRON/CORE/agente_git.py`
4. `TRON/CORE/clases/git_core.py`
5. `TRON/CORE/herramientas/gestor_git_cli.py`
6. `TRON/logs/git_ops.log` (runtime artifact - NO COPIAR)
7. `TRON/CORE/.venv/` (regenerable - NO COPIAR)

---

## 🚀 INTEGRATION GUIDE

### Paso 1: Configuración Claude Code

```bash
# Copiar configuraciones
cp unique-content/settings.json /home/daniel/tron/programas/TR/.claude/
cp unique-content/settings.local.json /home/daniel/tron/programas/TR/.claude/

# Verificar rutas en settings.json
# Actualizar si TR tiene estructura diferente
```

### Paso 2: Git Tools para ARES

```bash
# Estructura recomendada para ARES
mkdir -p TR/programas/ares/{core,tools,modules/git}

# Copiar módulos
cp unique-content/git_core.py TR/programas/ares/core/
cp unique-content/gestor_git_cli.py TR/programas/ares/tools/git_cli.py
cp unique-content/agente_git.py TR/programas/ares/modules/git/

# Actualizar imports y rutas en cada archivo
```

### Paso 3: Verificación

```bash
# Probar git_core.py directamente
cd TR/programas/ares
python -c "from core.git_core import GitCore; print(GitCore().__doc__)"

# Probar CLI
python tools/git_cli.py --help  # (después de añadir --help)
```

---

## 💡 TOKEN EFFICIENCY RECOMMENDATIONS

### ¿Vale la pena integrar este contenido?

| Archivo | Token Cost | Valor | Recomendación |
|---------|------------|-------|---------------|
| `settings.json` | 0 (config estática) | Alto | ✅ Integrar inmediatamente |
| `settings.local.json` | 0 (config estática) | Alto | ✅ Integrar inmediatamente |
| `git_core.py` | 0 (código puro) | Muy Alto | ✅ Integrar como módulo base |
| `gestor_git_cli.py` | 0 (CLI tool) | Alto | ✅ Integrar con --help |
| `agente_git.py` | ~200 tokens/op | Medio | ⚠️ Evaluar si ARES necesita agente conversacional Git |

### Alternativa más eficiente:

**En lugar de `agente_git.py`** (agente conversacional con LLM):
- Usar directamente `git_cli.py` en scripts bash de ARES
- Integrar `GitCore` class en Python modules de ARES
- **Ahorro:** ~200 tokens por operación Git + latencia de Ollama

**Decisión:** Depende de si ARES requiere interfaz conversacional para Git o solo automatización.

---

## 📋 CHECKLIST DE INTEGRACIÓN

- [ ] Copiar `settings.json` a `TR/.claude/` y actualizar rutas
- [ ] Copiar `settings.local.json` a `TR/.claude/`
- [ ] Mover `git_core.py` a `TR/programas/ares/core/`
- [ ] Mover `gestor_git_cli.py` a `TR/programas/ares/tools/git_cli.py`
- [ ] Añadir `--help` a `git_cli.py` (convención TRON)
- [ ] Actualizar rutas y imports en ambos archivos
- [ ] Evaluar si integrar `agente_git.py` o solo usar GitCore
- [ ] Probar integración en entorno ARES
- [ ] Documentar en IA-MEMORY.md si se adopta como estándar Git

---

## 🧠 LECCIONES APRENDIDAS

1. **Duplicación Cero:** `.qwen` y `.claude` compartían 100% del contenido excepto 5 archivos. Usar enlaces duros (como IA-MEMORY.md) evita esta redundancia.

2. **Valor en Código:** Los scripts Git (git_core.py, gestor_git_cli.py) son el mayor valor - código reutilizable con logging y safe operations.

3. **Configuración como Código:** `settings.json` y `settings.local.json` son configuración crítica que debe versionarse y documentarse.

4. **Agentes Conversacionales:** `agente_git.py` es interesante pero consume tokens. Para automatización pura, mejor CLI directa.

5. **Estructura Portables:** Todos los scripts usan `Path(__file__)` para portabilidad - patrón a seguir en ARES.

---

**📌 Nota Final:** Este benchmarking prioriza **eficiencia de tokens** y **reutilización máxima**. Los 5 archivos únicos identificados son complementarios y no duplican funcionalidad existente en TR/ares.

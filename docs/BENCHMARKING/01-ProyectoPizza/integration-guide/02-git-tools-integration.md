# 🔧 Git Tools Integration Guide

**Source Files:**
- `git_core.py` → Git operations class
- `gestor_git_cli.py` → CLI JSON interface
- `agente_git.py` → Conversational Git agent

**Destination:** `TR/programas/ares/{core,tools,modules/git}/`  
**Priority:** ⭐⭐⭐⭐⭐ (High-value reusable code)

---

## 📦 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ARES Git Integration                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐     ┌─────────────────┐                │
│  │  agente_git.py  │     │  git_cli.py     │                │
│  │  (Conversational│     │  (CLI Tool)     │                │
│  │   Interface)    │     │                 │                │
│  │                 │     │                 │                │
│  │  Model: Ollama  │     │  Direct Python  │                │
│  │  ~200 tokens/op │     │  0 tokens/op    │                │
│  └────────┬────────┘     └────────┬────────┘                │
│           │                       │                          │
│           └───────────┬───────────┘                          │
│                       │                                      │
│              ┌────────▼────────┐                             │
│              │   GitCore       │                             │
│              │   (Core Class)  │                             │
│              │                 │                             │
│              │  - guardar_     │                             │
│              │    cambios()    │                             │
│              │  - retroceder_  │                             │
│              │    seguro()     │                             │
│              │  - sincronizar_ │                             │
│              │    nube()       │                             │
│              └────────┬────────┘                             │
│                       │                                      │
│              ┌────────▼────────┐                             │
│              │   Git Commands  │                             │
│              │   (subprocess)  │                             │
│              └─────────────────┘                             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Integration Steps

### Step 1: Copy Files to ARES Structure

```bash
# Create directories
mkdir -p /home/daniel/tron/programas/TR/programas/ares/{core,tools,modules/git}

# Copy from benchmarking
cd /home/daniel/tron/programas/TR/docs/BENCHMARKING/ProyectoPizza/unique-content

# Copy core class
cp git_core.py /home/daniel/tron/programas/TR/programas/ares/core/

# Copy CLI tool
cp gestor_git_cli.py /home/daniel/tron/programas/TR/programas/ares/tools/git_cli.py

# Copy agent (optional)
cp agente_git.py /home/daniel/tron/programas/TR/programas/ares/modules/git/agente_git.py
```

### Step 2: Update `git_core.py` for ARES

**Changes needed:**

```python
# OLD (ProyectoPizza paths)
CORE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = CORE_DIR.parent / "logs"
VERIFICADOR_PESO = CORE_DIR / "utilidades" / "verificador_peso.py"

# NEW (ARES paths)
CORE_DIR = Path(__file__).resolve().parent.parent.parent  # One level up
LOG_DIR = Path("/home/daniel/tron/programas/TR/logs")  # ARES standard
VERIFICADOR_PESO = CORE_DIR / "core" / "verificador_peso.py"
```

**Or use environment variable:**

```python
import os

# ARES_ROOT from environment (set by 'ini' wrapper)
ARES_ROOT = Path(os.environ.get("TR_PROJECT_ROOT", "/home/daniel/tron/programas/TR"))
CORE_DIR = ARES_ROOT / "programas" / "ares"
LOG_DIR = ARES_ROOT / "logs"
VERIFICADOR_PESO = CORE_DIR / "core" / "verificador_peso.py"
```

### Step 3: Update `git_cli.py` for ARES

**Changes needed:**

```python
# OLD import
from clases.git_core import GitCore

# NEW import (ARES structure)
from core.git_core import GitCore

# OR dynamic path resolution
import sys
from pathlib import Path
CORE_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(CORE_PATH))
from core.git_core import GitCore
```

**Add `--help` functionality (TRON convention):**

```python
def main():
    parser = argparse.ArgumentParser(
        description="ARES Git CLI - JSON interface for Git operations",
        epilog="Examples:\n"
               "  git_cli.py guardar -m 'feat: add module'\n"
               "  git_cli.py volver -p 3\n"
               "  git_cli.py nube",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # ... rest of code
```

### Step 4: Update `agente_git.py` (If Using)

**Changes needed:**

```python
# OLD model
model = 'functiongemma:270m'

# NEW model (ARES default)
model = os.environ.get("ARES_MODEL", "llama3.1:8b")

# OLD tool path
BASE_DIR = Path(__file__).resolve().parent
TOOL_PATH = BASE_DIR / "herramientas" / "gestor_git_cli.py"

# NEW tool path
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # modules/git -> programas/ares
TOOL_PATH = BASE_DIR / "tools" / "git_cli.py"
```

---

## 🧪 Testing

### Test GitCore Class

```bash
cd /home/daniel/tron/programas/TR/programas/ares

python3 -c "
from core.git_core import GitCore
core = GitCore()
print('GitCore loaded successfully')
print(f'Git root: {core.root}')
result = core.guardar_cambios('test commit')
print(f'Result: {result}')
"
```

### Test Git CLI

```bash
# Test help
python3 tools/git_cli.py --help

# Test guardar
python3 tools/git_cli.py guardar -m "test commit"

# Test volver (dry run - won't actually revert)
python3 tools/git_cli.py volver -p 1

# Test nube
python3 tools/git_cli.py nube
```

### Test Agent (If Integrated)

```bash
cd /home/daniel/tron/programas/TR/programas/ares

# Start agent
python3 modules/git/agente_git.py

# In agent, try:
# "guardar los cambios con mensaje 'test'"
```

---

## 📊 Usage Comparison

### GitCore Class (Python)

**Best for:** Direct Python integration in ARES modules

```python
from core.git_core import GitCore

core = GitCore()

# Safe commit
result = core.guardar_cambios("feat: add new module")
if result["estado"] == "exito":
    logger.info(result["mensaje"])
else:
    logger.error(f"Git error: {result}")

# Safe revert
result = core.retroceder_seguro(3)

# Sync
result = core.sincronizar_nube()
```

**Token Cost:** 0  
**Latency:** ~100ms (subprocess call)

---

### Git CLI (Bash/Python)

**Best for:** Shell scripts, automation, external tools

```bash
#!/bin/bash

# Commit changes
result=$(python3 tools/git_cli.py guardar -m "auto-commit")
estado=$(echo $result | jq -r '.estado')

if [ "$estado" == "exito" ]; then
    echo "✅ Commit successful"
else
    echo "❌ Commit failed: $result"
fi

# Revert last 3 commits
python3 tools/git_cli.py volver -p 3 | jq '.mensaje'

# Sync
python3 tools/git_cli.py nube | jq '.estado'
```

**Token Cost:** 0  
**Latency:** ~150ms (Python subprocess + JSON parse)

---

### Git Agent (Conversational)

**Best for:** Interactive use, natural language interface

```
👤 Tú: guarda los cambios con mensaje "adding new feature"
⚙️  [SISTEMA] Ejecutando: herramienta_git_tron {'accion': 'guardar', 'argumento': 'adding new feature'}
🤖 IA: ✅ Checkpoint guardado: 'adding new feature'

👤 Tú: vuelve 2 pasos atrás
⚙️  [SISTEMA] Ejecutando: herramienta_git_tron {'accion': 'volver', 'argumento': 2}
🤖 IA: Se revirtieron los últimos 2 cambios de forma segura.
```

**Token Cost:** ~200 tokens per operation  
**Latency:** ~2-5s (Ollama inference)

---

## 🎯 Token Efficiency Analysis

| Tool | Setup Cost | Runtime Cost | Best Use Case |
|------|------------|--------------|---------------|
| `GitCore` class | 0 tokens | 0 tokens | Python modules |
| `git_cli.py` | 0 tokens | 0 tokens | Bash scripts, automation |
| `agente_git.py` | 0 tokens | ~200 tokens/op | Conversational interface |

**Recommendation:** Use GitCore/git_cli for automation (zero tokens). Use agent only for interactive sessions where natural language is worth the token cost.

---

## ⚠️ Important Notes

### 1. Safe Revert (Non-Destructive)

`GitCore.retroceder_seguro()` uses `git revert`, NOT `git reset`:

```bash
# What GitCore does:
git revert --no-edit HEAD~3..HEAD

# What it DOESN'T do (destructive):
git reset --hard HEAD~3  # ❌ DANGEROUS - loses history
```

**Benefit:** Preserves commit history, safe for shared repos

**Trade-off:** Creates new revert commits instead of erasing history

---

### 2. Weight Verification Hook

`guardar_cambios()` calls `verificador_peso.py` before commit:

```python
if VERIFICADOR_PESO.exists():
    peso_check = self._run_cmd([sys.executable, str(VERIFICADOR_PESO)])
    if not peso_check["success"]:
        return {"estado": "error", "razon": "Archivos grandes detectados"}
```

**For ARES:** Ensure `verificador_peso.py` exists in `core/` or remove hook.

---

### 3. Logging

All operations log to `git_ops.log`:

```
2026-03-18 10:30:45 - INFO - EJECUTANDO: git add -A
2026-03-18 10:30:46 - INFO - EXITO: 
2026-03-18 10:30:46 - INFO - EJECUTANDO: git commit -m test
2026-03-18 10:30:47 - INFO - EXITO: [main 1234567] test
```

**For ARES:** Update `LOG_DIR` to ARES standard location.

---

## 🧩 Integration with ARES Commands

If ARES uses `ini` wrapper with environment variables:

**`pyproject.toml` or `.tron.env.json`:**
```json
{
  "project_name": "ARES",
  "command_name": "ares",
  "variables": {
    "TR_PROJECT_ROOT": "/home/daniel/tron/programas/TR",
    "ARES_MODEL": "llama3.1:8b"
  }
}
```

**Then in Python files:**
```python
import os

TR_ROOT = Path(os.environ.get("TR_PROJECT_ROOT", "/home/daniel/tron/programas/TR"))
LOG_DIR = TR_ROOT / "logs"
```

---

## ✅ Validation Checklist

- [ ] Files copied to ARES structure
- [ ] Imports updated (clases → core, herramientas → tools)
- [ ] Paths use environment variables or absolute paths
- [ ] `git_cli.py` has `--help` functionality
- [ ] `agente_git.py` uses ARES model (if integrated)
- [ ] Logging directory exists
- [ ] `verificador_peso.py` exists or hook removed
- [ ] All three tools tested successfully
- [ ] Git operations work in test repository

---

## 📚 Related Documentation

- **00-INDEX-MASTER.md:** Master index
- **01-settings-integration.md:** Settings integration
- **03-architecture-notes.md:** Architecture patterns

---

**Status:** Ready for integration  
**Estimated Time:** 20 minutes  
**Token Cost:** 0 (pure code integration)

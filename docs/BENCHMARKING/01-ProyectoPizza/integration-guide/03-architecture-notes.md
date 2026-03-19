# 🏗️ Architecture Patterns & Reusable Concepts

**Extracted from:** ProyectoPizza TRON System  
**Purpose:** Document architectural patterns that can be reused in ARES-TRON  
**Token Efficiency Focus:** Patterns that reduce token consumption while increasing capability

---

## 📐 Architectural Patterns

### 1. Three-Layer Tool Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Agent Interface (Conversational)               │
│ - agente_git.py                                         │
│ - Natural language input                                │
│ - LLM processing (Ollama)                               │
│ - Token cost: ~200/op                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 2: CLI Interface (Automation)                     │
│ - gestor_git_cli.py                                     │
│ - argparse with subcommands                             │
│ - JSON output (deterministic)                           │
│ - Token cost: 0                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Core Class (Business Logic)                    │
│ - git_core.py (GitCore class)                           │
│ - Pure Python, no dependencies                          │
│ - Logging, error handling                               │
│ - Token cost: 0                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
              Git Operations (subprocess)
```

**Why This Pattern Works:**

1. **Separation of Concerns:** Each layer has a single responsibility
2. **Token Efficiency:** Use Layer 2 or 3 for automation (0 tokens), Layer 1 only for interactive use
3. **Reusability:** Core class can be imported anywhere
4. **Testability:** Each layer can be tested independently

**Apply to ARES:**
- Use this pattern for new ARES tools (web search, document processing, etc.)
- Layer 1: Conversational agent (LLM)
- Layer 2: CLI tool (bash automation)
- Layer 3: Core class (Python module)

---

### 2. Dynamic Path Resolution (Portability Pattern)

**Problem:** Hardcoded paths break when moving between projects

**Solution:** Use `Path(__file__)` for relative resolution

```python
# ✅ GOOD - Portable
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent  # Go up 2 levels
TOOL_PATH = BASE_DIR / "tools" / "git_cli.py"

# ❌ BAD - Hardcoded
BASE_DIR = "/home/daniel/tron/programas/ProyectoPizza/.claude/TRON"
```

**Environment Variable Override:**

```python
import os
from pathlib import Path

# Default to computed path
TR_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Allow override via environment (set by 'ini' wrapper)
if "TR_PROJECT_ROOT" in os.environ:
    TR_ROOT = Path(os.environ["TR_PROJECT_ROOT"])
```

**Apply to ARES:**
- Always use `Path(__file__)` for intra-project paths
- Use environment variables for project root
- `ini` wrapper should set `TR_PROJECT_ROOT`

---

### 3. JSON Output Contract (Deterministic Interface)

**Pattern:** All tools return JSON with consistent structure

```python
# ✅ GOOD - Deterministic JSON
{
    "estado": "exito",  # | "error" | "neutro" | "excepcion"
    "mensaje": "Checkpoint guardado",
    "detalle": {...}  # Optional
}

# ❌ BAD - Unstructured text
"✅ Commit successful!"
```

**Benefits:**
- Easy to parse in bash: `jq -r '.estado'`
- Easy to handle in Python: `result["estado"]`
- LLM can understand and generate consistent output
- Error handling is standardized

**Apply to ARES:**
- Define JSON schema for all ARES tools
- Use `ensure_ascii=False` for Spanish support
- Include `estado` field for quick status check

---

### 4. Pre-Command Hook (Validation Pattern)

**Pattern:** Run validation before executing commands

```python
# In GitCore.guardar_cambios()
if VERIFICADOR_PESO.exists():
    peso_check = self._run_cmd([sys.executable, str(VERIFICADOR_PESO)])
    if not peso_check["success"]:
        return {"estado": "error", "razon": "Archivos grandes detectados"}
```

**Claude Code Integration:**

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 verificador_peso.py"
      }]
    }]
  }
}
```

**Benefits:**
- Prevents mistakes before they happen
- Centralized validation logic
- Can be disabled by removing hook

**Apply to ARES:**
- Create validation hooks for critical operations
- Use in Claude Code settings.json
- Call from Python code before sensitive operations

---

### 5. Safe Revert (Non-Destructive History)

**Pattern:** Use `git revert` instead of `git reset`

```python
# ✅ SAFE - Preserves history
def retroceder_seguro(self, pasos: int):
    rango = f"HEAD~{pasos}..HEAD"
    res = self._run_cmd(["git", "revert", "--no-edit", rango])

# ❌ DANGEROUS - Destroys history
def retroceder(self, pasos: int):
    res = self._run_cmd(["git", "reset", "--hard", f"HEAD~{pasos}"])
```

**Why:**
- `git revert` creates new commits that undo changes
- `git reset --hard` permanently deletes commits
- Revert is safe for shared repositories
- Reset requires force push and can lose others' work

**Apply to ARES:**
- Always use revert-based undo for Git operations
- Document this choice in ARES Git policy
- Explain to users why revert is safer

---

### 6. Logging with Fallback (Observability Pattern)

**Pattern:** Log everything, but don't break if logging fails

```python
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "git_ops.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def _run_cmd(self, cmd_list):
    try:
        logging.info(f"EJECUTANDO: {' '.join(cmd_list)}")
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"EXITO: {result.stdout}")
        else:
            logging.error(f"FALLO: {result.stderr}")
        return {"success": True, ...}
    except Exception as e:
        logging.critical(f"EXCEPCION: {str(e)}")
        return {"success": False, ...}
```

**Benefits:**
- Audit trail for all operations
- Debugging aid
- Doesn't break if log file is unwritable
- Separate from user output (clean JSON)

**Apply to ARES:**
- Create standard logging module in ARES core
- All tools log to central location
- Use `TR_PROJECT_ROOT/logs/` as standard

---

### 7. Subprocess Executor (Isolation Pattern)

**Pattern:** Run external commands via subprocess, capture output

```python
def _run_cmd(self, cmd_list, cwd=None):
    try:
        result = subprocess.run(
            cmd_list,
            cwd=cwd or self.root,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return {"success": True, "stdout": result.stdout.strip()}
        else:
            return {"success": False, "stderr": result.stderr.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Benefits:**
- Isolates external command failures
- Captures stdout/stderr separately
- Return code checking
- Exception handling

**Apply to ARES:**
- Create utility function in `ares/core/subprocess_utils.py`
- Use for all external command execution
- Standardize error handling

---

### 8. Tool Calling Pattern (LLM Integration)

**Pattern:** Define Python functions as tools for LLM

```python
def herramienta_git_tron(accion: str, argumento: str = ""):
    """
    Ejecuta comandos de git seguros (guardar, volver, nube).

    Args:
      accion: 'guardar', 'volver', o 'nube'.
      argumento: Mensaje para guardar o número de pasos para volver.
    """
    # ... implementation

# In main loop
response = ollama.chat(
    model=model,
    messages=messages,
    tools=[herramienta_git_tron]
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        fn_name = tool.function.name
        args = tool.function.arguments
        resultado = herramienta_git_tron(**args)
```

**Benefits:**
- LLM can call Python functions directly
- Type-safe argument passing
- Structured output to LLM
- Reusable tool definitions

**Apply to ARES:**
- Define ARES tools with clear docstrings
- Use Ollama tool calling interface
- Return JSON for LLM interpretation

---

## 🎯 Token Efficiency Strategies

### Strategy 1: Prefer CLI Over Conversational

| Operation | Conversational | CLI | Savings |
|-----------|---------------|-----|---------|
| Git commit | ~200 tokens | 0 tokens | 200 tokens |
| Git revert | ~200 tokens | 0 tokens | 200 tokens |
| Git sync | ~200 tokens | 0 tokens | 200 tokens |

**Daily savings (10 ops/day):** 2000 tokens

**Implementation:**
- Use `git_cli.py` in automation scripts
- Reserve `agente_git.py` for interactive sessions

---

### Strategy 2: Cache LLM Responses

```python
# ❌ BAD - Calls LLM every time
for user_input in inputs:
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': user_input}])

# ✅ GOOD - Cache common responses
CACHE = {
    "help": "Comandos disponibles: guardar, volver, nube",
    "status": "Estado del sistema: OK"
}
if user_input in CACHE:
    response = CACHE[user_input]
else:
    response = ollama.chat(...)
```

**Savings:** ~100 tokens per cached response

---

### Strategy 3: Use Configuration Files

Instead of explaining system structure every time:

```json
// settings.json - Zero runtime token cost
{
  "permissions": {
    "allow": ["Bash(ares *)"]
  }
}
```

**Savings:** ~50 tokens per session (no need to explain allowed commands)

---

### Strategy 4: Modular Documentation

Instead of one giant README:

```
docs/
├── INDEX.md              # Table of contents (short)
├── getting-started.md    # Link when needed
├── api-reference.md      # Link when needed
└── troubleshooting.md    # Link when needed
```

**Savings:** Only load relevant docs (100-500 tokens saved per session)

---

## 📋 Checklist for ARES Implementation

### Architecture

- [ ] Use three-layer pattern for new tools
- [ ] Implement dynamic path resolution
- [ ] Define JSON output contracts
- [ ] Set up pre-command hooks
- [ ] Use safe revert for Git operations

### Code Quality

- [ ] Centralized logging
- [ ] Subprocess isolation
- [ ] Error handling standards
- [ ] Tool calling interface

### Token Efficiency

- [ ] Prefer CLI over conversational
- [ ] Implement response caching
- [ ] Use configuration files
- [ ] Modular documentation

### Integration

- [ ] Copy git_core.py to ARES core
- [ ] Copy git_cli.py to ARES tools
- [ ] Evaluate agente_git.py necessity
- [ ] Update paths and imports
- [ ] Test all tools

---

## 🧠 Key Takeaways

1. **Separation of Concerns:** Three-layer architecture enables token-efficient automation
2. **Portability:** Dynamic path resolution prevents breakage when moving projects
3. **Determinism:** JSON output contracts enable reliable automation
4. **Safety:** Pre-command hooks and safe revert prevent mistakes
5. **Observability:** Logging provides audit trail without affecting user output
6. **Efficiency:** CLI tools (0 tokens) should be preferred over conversational agents (~200 tokens)

---

**Status:** Reference documentation  
**Maintainer:** ARES-TRON  
**Last Updated:** 2026-03-18

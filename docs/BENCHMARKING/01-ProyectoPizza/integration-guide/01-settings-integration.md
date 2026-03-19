# 🔧 Settings Integration Guide

**Source:** `ProyectoPizza/.claude/settings.json` + `settings.local.json`  
**Destination:** `TR/.claude/settings.json` + `TR/.claude/settings.local.json`  
**Priority:** ⭐⭐⭐⭐⭐ (Critical for Claude Code integration)

---

## 📋 Step-by-Step Integration

### Step 1: Copy Files

```bash
# From benchmarking folder
cd /home/daniel/tron/programas/TR/docs/BENCHMARKING/ProyectoPizza/unique-content

# Copy to TR .claude directory
cp settings.json /home/daniel/tron/programas/TR/.claude/
cp settings.local.json /home/daniel/tron/programas/TR/.claude/
```

### Step 2: Verify Directory Structure

Ensure TR has the `.claude` directory:

```bash
ls -la /home/daniel/tron/programas/TR/.claude/
```

Expected output:
```
.clause/
├── settings.json
└── settings.local.json
```

### Step 3: Update Paths (If Needed)

**Check `settings.json` permissions:**

The current `allow` list references:
```json
"Bash(python3 TRON/CORE/despachador.py *)"
```

This is a **relative path** from Claude's working directory. If TR structure differs from ProyectoPizza, update to match TR's actual structure.

**For TR/ares, likely needs:**
```json
"Bash(python3 /home/daniel/tron/programas/TR/programas/ares/main.py *)"
```

Or if using `ini` wrapper:
```json
"Bash(ares *)"
```

### Step 4: Update Hooks

**Current hook:**
```json
"hooks": {
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "python3 TRON/CORE/utilidades/verificador_peso.py"
    }]
  }]
}
```

**For TR/ares, update to:**
```json
"hooks": {
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "python3 /home/daniel/tron/programas/TR/programas/ares/core/verificador_peso.py"
    }]
  }]
}
```

Or remove if ARES doesn't use weight verification.

### Step 5: Test Claude Code Integration

```bash
cd /home/daniel/tron/programas/TR

# Start Claude Code
claude

# Test allowed command
python3 programas/ares/main.py --help

# Test denied command (should be blocked)
# Try to use WebSearch - should be denied
```

---

## 🔍 Settings Breakdown

### `settings.json` - Base Configuration

**Purpose:** Security firewall for Claude Code

| Section | Function | Recommended for ARES? |
|---------|----------|----------------------|
| `permissions.allow` | Whitelist of allowed commands | ✅ Yes, update paths |
| `permissions.deny` | Blacklist of blocked tools | ✅ Yes, keep WebSearch/WebFetch denied |
| `hooks.PreToolUse` | Pre-command validation | ⚠️ Optional (weight verification) |

### `settings.local.json` - Local Overrides

**Purpose:** Extend permissions for local development

| Permission | Purpose | Keep for ARES? |
|------------|---------|----------------|
| `Bash(python3:*)` | Allow any python3 command | ✅ Yes |
| `Skill(docs)` | Use docs skill without confirmation | ✅ Yes |
| `Skill(metaconocimiento)` | Use meta-knowledge skill | ✅ Yes |
| `Skill(creador-herramientas)` | Tool creation skill | ✅ Yes |
| `Bash(chmod:*)` | Change file permissions | ✅ Yes |
| `Bash(curl:*)` | HTTP requests | ✅ Yes |
| `Skill(gestor-git)` | Git management skill | ✅ Yes (if using GitCore) |

---

## 🎯 Token Efficiency

**Settings files have ZERO runtime token cost:**
- Loaded once at Claude Code startup
- No tokens consumed during operation
- One-time setup, permanent benefit

**ROI:** ⭐⭐⭐⭐⭐ (Highest possible)

---

## ⚠️ Common Pitfalls

### 1. Relative vs Absolute Paths

**Problem:** `settings.json` uses relative paths like `TRON/CORE/despachador.py`

**Solution:** Use absolute paths or ensure Claude's working directory is project root

```json
// ❌ Bad (breaks if CWD changes)
"Bash(python3 TRON/CORE/despachador.py *)"

// ✅ Good (always works)
"Bash(python3 /home/daniel/tron/programas/TR/programas/ares/main.py *)"

// ✅ Better (uses ini wrapper)
"Bash(ares *)"
```

### 2. Hook Path Resolution

**Problem:** Hooks run in different context than main commands

**Solution:** Always use absolute paths in hooks

```json
// ❌ Bad
"command": "python3 TRON/CORE/utilidades/verificador_peso.py"

// ✅ Good
"command": "python3 /home/daniel/tron/programas/TR/programas/ares/core/verificador_peso.py"
```

### 3. Conflicting Permissions

**Problem:** `settings.json` denies, `settings.local.json` allows same command

**Solution:** `settings.local.json` takes precedence, but be explicit:

```json
// settings.json
"deny": ["WebSearch", "WebFetch"]

// settings.local.json - if you want to allow WebFetch locally
"allow": ["WebFetch(home/daniel/tron/programas/TR/docs/*)"]
```

---

## 🧪 Validation Checklist

- [ ] Files copied to `TR/.claude/`
- [ ] Paths updated to match TR structure
- [ ] Hooks use absolute paths
- [ ] Claude Code starts without errors
- [ ] Allowed commands work
- [ ] Denied commands are blocked
- [ ] Hooks execute correctly (check logs)
- [ ] Skills are accessible without confirmation

---

## 📚 Related Documentation

- **IA-MEMORY.md:** Protocolo ARES-TRON (multi-IA coordination)
- **00-INDEX-MASTER.md:** Master index for this benchmarking
- **02-git-tools-integration.md:** Next step - Git tools integration

---

## 🚀 Quick Copy-Paste Template for ARES

**`TR/.claude/settings.json`:**
```json
{
  "permissions": {
    "allow": [
      "Bash(ares *)",
      "Read(/home/daniel/tron/programas/TR/docs/*)"
    ],
    "deny": [
      "WebSearch",
      "WebFetch"
    ]
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": []
    }]
  }
}
```

**`TR/.claude/settings.local.json`:**
```json
{
  "permissions": {
    "allow": [
      "Bash(python3:*)",
      "Skill(*)",
      "Bash(chmod:*)",
      "Bash(curl:*)"
    ]
  }
}
```

---

**Status:** Ready for integration  
**Estimated Setup Time:** 10 minutes  
**Token Cost:** 0 (one-time configuration)

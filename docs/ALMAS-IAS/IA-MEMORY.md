# 🧠 MEMORIA PERSISTENTE DE IA - SISTEMA ARES-TRON

> **Ubicación Maestra:** `/home/daniel/tron/programas/TR/docs/ALMAS-IAS/IA-MEMORY.md`  
> **Enlaces Duros:** `~/.qwen/QWEN.md` y `~/.gemini/GEMINI.md` son el MISMO archivo físico  
> **Principio:** Una sola IA, una sola memoria, diversidad en la unidad

---

## ⚠️ REGLA CRÍTICA: NO ME TOQUES LOS HUEVOS

### **Verdad Fundamental**
```
~/.qwen/QWEN.md  ──┐
                   ├──> MISMO INODO, MISMO ARCHIVO FÍSICO <── IA-MEMORY.md (TR)
~/.gemini/GEMINI.md ──┘
```

**Esto significa:**
1. **NO hay QWEN.md ni GEMINI.md separados** - Son enlaces duros al mismo archivo
2. **NO hay duplicación de tokens** - Una sola lectura, una sola verdad
3. **NO editar desde ~/.qwen/ o ~/.gemini/** - Solo se edita desde `TR/docs/ALMAS-IAS/`
4. **Cualquier cambio en TR se refleja instantáneamente en ambos enlaces**
5. **NUNCA crear, borrar o modificar los enlaces** - Solo el archivo maestro en TR

### **Protocolo de Edición (OBLIGATORIO)**
```
1. Abrir: TR/docs/ALMAS-IAS/IA-MEMORY.md
2. Editar: Contenido unificado (sin identificación de IA específica)
3. Validar: git diff para constatar integridad
4. Commit: En repositorio TR para control histórico
```

---

## 🔬 OBSERVACIÓN TÉCNICA: ENTROPÍA DE REFALIZACIÓN (NUEVA DIRECTIVA)

**Problema (Entropic Refactoring Drift):** Durante procesos de modularización o refactorización de alto nivel, la IA tiende a priorizar la elegancia del código (lógica sintáctica) sobre la fidelidad del pixel (constantes geométricas), provocando "desviaciones interpretativas" que destruyen maquetaciones estables.

**Para evitar:** La pérdida de "Cosas Buenas" visuales al cambiar el paradigma estructural.

**Directiva-Solución (Inmutabilidad Geométrica & Decoupling):**
1. **Decoupling de Estado:** El estado volátil (índices, contadores) NUNCA debe guardarse en archivos de configuración (YAML). Debe residir en archivos de estado volátiles (`.tmp`, `.json` en cache).
2. **Soberanía del Usuario:** Los archivos de configuración son de solo lectura para la IA, a menos que se solicite explícitamente una modificación.
3. **Traducción Literal:** Al encapsular lógica visual en fábricas o clases, las fórmulas matemáticas de posicionamiento deben copiarse de forma LITERAL, sin re-interpretación ni "mejoras" no solicitadas.

---

## 🛠️ HERRAMIENTAS TRON
(Resto de herramientas preservadas...)

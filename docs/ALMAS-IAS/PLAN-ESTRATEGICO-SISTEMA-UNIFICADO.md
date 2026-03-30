# PLAN ESTRATÉGICO: SISTEMA UNIFICADO DE ALTA DENSIDAD (DSL)

**Fecha:** Martes, 24 de marzo de 2026
**Ubicación:** `/home/daniel/tron/programas/TR/docs/ALMAS-IAS/PLAN-ESTRATEGICO-SISTEMA-UNIFICADO.md`
**Objetivo:** Transformación de la memoria sistémica (IA-MEMORY) y skills operativos a un lenguaje de dominio específico (DSL) de lógica pura, optimizado para procesamiento LLM y mínima redundancia de tokens.

---

## 1. Interpretación de la Intención
El usuario requiere un **cambio de paradigma** en la comunicación con la IA. Se busca abandonar la prosa explicativa humana en favor de una **notación lógico-funcional comprimida**.
*   **Formato Objetivo:** YAML (estructura) + S-Expressions (lógica Lisp-style).
*   **Meta:** Reducción drástica de tokens (hasta 40%) sin pérdida de rigor operativo.
*   **Principio:** "Transferencia de estado lógica pura".

## 2. Análisis del Estado Actual
*   **Núcleo:** `TR/docs/ALMAS-IAS/IA-MEMORY.md` (actualmente texto narrativo/tables).
*   **Skills:** Dispersos o en prosa en `maestro.md`. Necesitan ubicación centralizada en `TR/docs/skills/`.
*   **Herramientas:** `ini`, `com` documentadas narrativamente.

## 3. Metodología de Transformación

### A. Definición del Esquema DSL (Schema)
Definiremos un "Dialecto ARES" estricto:

```yaml
sys: "{NombreSistema}"
ver: "1.0"
root: "{RutaBase}"
defs: # Diccionario de símbolos
  @L: "LEEME.md" # La Verdad
  @I: "IA-MEMORY.md"
  @P: "Protocolo"
rules: # Reglas globales (Axiomas)
  - (assert (eq @L $TRUTH)) 
  - (forbid (touch ~/.qwen/ ~/.gemini/)) # Enlaces duros intocables
  - (require (git_diff $POST_OP))
```

### B. Estrategia de Archivos

1.  **IA-MEMORY.md (El Índice Maestro):**
    Será convertido en un *Router Lógico*. No contendrá explicaciones, sino punteros y axiomas globales.
    
    *Ejemplo de Transformación:*
    *Antes:* "La Agenda del Sistema es el documento maestro..."
    *Después:*
    ```yaml
    entity: "SystemAgenda"
    loc: "/home/daniel/tron/programas/AGENDA/agenda.md"
    logic: (sync (source @I) (target $PROJECT_STATE) (log $BITACORA))
    ```

2.  **Skills (Compresión Funcional):**
    Se crearán archivos en `TR/docs/skills/` con extensión `.dsl.md` (o similar para claridad, aunque el contenido será DSL).
    
    *   `skill-init.dsl.md`
    *   `skill-dev.dsl.md`
    *   `skill-maint.dsl.md`
    *   `skill-prod.dsl.md`
    *   `skill-session.dsl.md`

    *Ejemplo (Skill Init):*
    ```lisp
    (def-skill "init"
      (inputs $name $type)
      (pre-cond (not (exists? @L)))
      (proc
        (mkdir_tree [$name/.ai $name/src $name/docs])
        (write @L (template "INIT_STATE" $date))
        (write "REP_STRUCTURE.md" $rules)
      )
      (post-cond (verify_tree $name))
    )
    ```

### C. Pasos de Ejecución (Roadmap)

1.  **Validación de Rutas:** Asegurar que `TR/docs/skills/` existe.
2.  **Creación de Skills Comprimidos:** Extraer la lógica de `maestro.md` y `ArquitecturadeModulosOrientadaaIA.md` y escribirla en formato DSL en `TR/docs/skills/`.
3.  **Refactorización de IA-MEMORY.md:** Reescribir el archivo maestro usando el nuevo esquema DSL, enlazando a los nuevos skills.
4.  **Actualización de Referencias:** Asegurar que `Agents.md` (si existe o es parte de la memoria) apunte a este nuevo índice.

## 4. Beneficios Esperados
*   **Velocidad:** Menor latencia en la lectura de contexto.
*   **Precisión:** Eliminación de ambigüedad lingüística ("quizás", "debería").
*   **Coste:** Menor consumo de tokens de entrada.
*   **Escalabilidad:** Fácil adición de nuevas reglas sin reescribir prosa extensa.

## 5. Validación
El sistema será validado verificando que la IA pueda "parsear" las instrucciones DSL y ejecutar una tarea de prueba (simulada) siguiendo estrictamente la lógica definida.

---
*Este informe debe ser aprobado (implícitamente por la directiva de autonomía o explícitamente) antes de proceder con la sobrescritura de `IA-MEMORY.md`.*

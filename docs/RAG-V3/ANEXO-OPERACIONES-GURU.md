# ANEXO: OPERACIONES TÁCTICAS DEL GURÚ (PROMPTING VIVO)

Este documento detalla cómo el usuario puede interactuar con el sistema RAG de Grafos de manera avanzada, utilizando la "identidad" como palanca de control.

---

## 1. EL PROMPT VIVO (JIT PROMPT INJECTION)
ARES no usa System Prompts estáticos. El sistema busca en el grafo Memgraph el nodo `GURU_IDENTITY` vinculado a la tarea actual e inyecta las instrucciones justo antes de la consulta.
- **Caso de uso**: Si el grafo detecta que estás en un módulo de "Ventas", inyectará automáticamente la filosofía de cierre agresivo sin que tengas que pedirlo.

---

## 2. CONTROL DE SERENDIPIA (EL MODO "DESCUBRIMIENTO")
Cuando usas `ares mengraph ingest`, el sistema puede descubrir relaciones que tú no habías planeado.
- **Validación Humana**: Si el `RelationGuard` marca una relación como `NEW_VERB`, debes revisarla en el `QuarantineManager`.
- **Comando**: `ares mengraph quarantine list` (Próximamente disponible para aprobación masiva).

---

## 3. TRAZABILIDAD DETERMINISTA
Cada vez que ARES responde basado en el grafo, puedes exigir la "Evidencia de Adverbio":
- El sistema devolverá el **Hash SHA-256** del párrafo original.
- Esto elimina la alucinación, ya que puedes verificar la fuente exacta con `ares grep <hash>`.

---
*Manual de Operaciones Avanzadas - ARES-TRON.*

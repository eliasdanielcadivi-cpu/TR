# 📐 ÍNDICE DE DIAGRAMAS MERMAID - AGENTE DE CAMBIO

> **Propósito:** Centralizar todos los diagramas de flujo Mermaid para facilitar la comunicación visual entre usuario e IA.  
> **Ubicación:** `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/FLUJOS-MERMAID/`  
> **Última actualización:** 2026-03-19

---

## 🗂️ DIAGRAMAS DISPONIBLES

| # | Diagrama | Archivo | Descripción | Capas Involucradas |
|---|----------|---------|-------------|-------------------|
| **1** | **Diagrama Maestro del Sistema** | [`01-diagrama-maestro-sistema.md`](./01-diagrama-maestro-sistema.md) | Arquitectura completa de 6 capas + flujo principal | Todas (0-6) |
| **2** | **Inferencia de Tipo de Pregunta** | [`02-inferencia-tipo-pregunta.md`](./02-inferencia-tipo-pregunta.md) | Lógica de decisión para generar preguntas dinámicas | Capa 4 (QBANK/RULES) |
| **3** | **Modelo de Datos (ERD)** | [`03-modelo-datos-ERD.md`](./03-modelo-datos-ERD.md) | 13 entidades de base de datos y relaciones | Capa 5 (Datos) |

---

## 📊 DIAGRAMA 1: MAESTRO DEL SISTEMA

**Archivo:** `01-diagrama-maestro-sistema.md`

**Propósito:** Visión arquitectónica completa del sistema.

**Componentes principales:**
- 6 capas (0-6)
- 40+ nodos de flujo
- 13 entidades de persistencia

**Cuándo usar:**
- Al comenzar un nuevo módulo
- Para entender el flujo completo
- Al validar cambios estructurales

**Relacionado con:**
- `PLAN-CONSTRUCCION.md` → Todos los hitos
- `INDICE-MAESTRO-PARA-IAS.md` → Capa 1-5

---

## 📊 DIAGRAMA 2: INFERENCIA DE TIPO DE PREGUNTA

**Archivo:** `02-inferencia-tipo-pregunta.md`

**Propósito:** Guía para el Motor de Preguntas (QI) al generar cuestionarios.

**Tipos de pregunta:**
1. Sí/No
2. Verdadero/Falso
3. Selección única
4. Selección múltiple
5. Completación
6. Texto multilínea
7. Ranking/priorización
8. Exploración abierta guiada

**Cuándo usar:**
- Implementar `modules/questionnaire-engine/` (Hito 1)
- Diseñar nuevas preguntas
- Validar lógica de inferencia

**Relacionado con:**
- `PLAN-CONSTRUCCION.md` → Hito 1
- `modules/quiz-engine/` → Templates por dominio

---

## 📊 DIAGRAMA 3: MODELO DE DATOS (ERD)

**Archivo:** `03-modelo-datos-ERD.md`

**Propósito:** Esquema de base de datos para persistencia.

**Entidades principales (13):**
1. USERS
2. OBJECTIVES
3. PROFILES
4. SESSIONS
5. QUESTIONNAIRES
6. QUESTIONS
7. ANSWERS
8. PROMPT_VERSIONS
9. DELTA_LOGS
10. EVIDENCE
11. STALL_SIGNALS
12. CHECKINS
13. MEMORY_CHUNKS
14. AUDIT_LOG

**Cuándo usar:**
- Diseñar esquema de BD
- Implementar persistencia
- Validar relaciones entre módulos

**Relacionado con:**
- `PLAN-CONSTRUCCION.md` → Hitos 2-3
- `modules/session-manager/` → SESSIONS
- `modules/objectives-manager/` → OBJECTIVES

---

## 🔄 FLUJO DE TRABAJO CON DIAGRAMAS

### Para IAs (Implementación)

```
1. Leer diagrama correspondiente al módulo
   ↓
2. Identificar capa/componente a implementar
   ↓
3. Verificar entidades de BD relacionadas
   ↓
4. Implementar código
   ↓
5. Validar con git diff que respeta el diagrama
```

### Para Usuarios (Validación)

```
1. Revisar diagrama antes del hito
   ↓
2. Comparar implementación con diagrama
   ↓
3. Validar que el flujo se respeta
   ↓
4. Aprobar o solicitar ajustes
```

---

## 📝 CÓMO MODIFICAR DIAGRAMAS

**Protocolo obligatorio:**

1. **Backup git:** `git tag "backup-$(date '+%Y%m%d-%H%M%S')-pre-diagrama"`
2. **Editar archivo .md:** Modificar solo el diagrama necesario
3. **Validar sintaxis Mermaid:** Usar [Mermaid Live Editor](https://mermaid.live/)
4. **Actualizar este índice:** Si agrega nuevo diagrama
5. **Commit con referencia:** `[DIAGRAMA] Descripción → ÍNDICE-DIAGRAMAS`

---

## 🎯 PRÓXIMOS DIAGRAMAS A CREAR

| Diagrama | Propósito | Hito relacionado |
|----------|-----------|------------------|
| `04-flujo-estancamiento.md` | 12 señales + 3 terapias | Hito 2 |
| `05-arquitecto-derivacion.md` | Filtro de merecimiento | Hito 3 |
| `06-perfil-biologico.md` | Cronotipo + scheduling | Hito 4 |
| `07-integracion-ares.md` | Puente ARES ↔ Agente | Hito 5 |

---

## 🔗 REFERENCIAS CRUZADAS

### Documentación Interna

| Documento | Ruta |
|-----------|------|
| **PLAN-CONSTRUCCION** | `/docs/CLAVE/PLAN-CONSTRUCCION.md` |
| **INDICE-MAESTRO-PARA-IAS** | `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md` |
| **requerimientos.md** | `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/requerimientos.md` |

### Herramientas

| Herramienta | URL |
|-------------|-----|
| **Mermaid Live Editor** | https://mermaid.live/ |
| **Mermaid Documentation** | https://mermaid.js.org/ |

---

**Última actualización:** 2026-03-19  
**Versión:** 1.0  
**Estado:** 3/10 diagramas completados

---

*Fin del Índice de Diagramas Mermaid*

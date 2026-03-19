# 🗺️ DIAGRAMA MAESTRO DEL SISTEMA - 6 CAPAS

> **Descripción:** Flujo completo del sistema de conducción cognitiva con todas las capas, desde el usuario hasta la persistencia de datos.  
> **Ubicación original:** `requerimientos.md` (líneas 1269-1478)  
> **Propósito:** Comunicación visual de la arquitectura completa entre usuario e IA.

---

## 📊 DIAGRAMA MERMAID

```mermaid
flowchart TD
    %% =========================
    %% CAPA 0 — ACTORES EXTERNOS
    %% =========================
    U[Usuario]
    H[Humano supervisor / tú]

    %% =========================
    %% CAPA 1 — INTERFAZ
    %% =========================
    subgraph L1["CAPA 1 — INTERFAZ DE ACCESO"]
        UI[UI Principal]
        M1[Modo Chat]
        M2[Modo Cuestionario]
        M3[Modo Mixto]
        QI[Motor de Preguntas]
        CHAT[Motor Conversacional]
        SW[Selector de Modo]
        IN[Input del usuario]
        NL[Comentario libre / multilinea]
        BTN[Opciones UI]
    end

    %% =========================
    %% CAPA 2 — ORQUESTACIÓN
    %% =========================
    subgraph L2["CAPA 2 — ORQUESTACIÓN COGNITIVA"]
        ORCH[Orquestador Central]
        INTENT[Detector de Intención]
        GOAL[Extractor de Objetivo]
        STATE[Estado de sesión]
        ROUTER[Router de flujo]
        POLICY[Política de conducción]
        MIX[Decisor de modalidad]
    end

    %% =========================
    %% CAPA 3 — GOBERNANZA
    %% =========================
    subgraph L3["CAPA 3 — GOBERNANZA Y CONTROL"]
        EXEC[Ejecutor LLM]
        ARCH[Arquitecto / Capa de control]
        DELTA[Calculador de deriva]
        TH[Umbral de cambio]
        APPR[Motor de aprobación]
        LOCK[Bloqueo de cambios bruscos]
        REB[Negociación con usuario]
        AUDIT[Auditoría de decisiones]
    end

    %% =========================
    %% CAPA 4 — MOTOR DE CONOCIMIENTO
    %% =========================
    subgraph L4["CAPA 4 — MEMORIA, PERFIL Y CONTEXTO"]
        MEM[Memoria permanente de objetivos]
        PROF[Perfil del usuario]
        RAG[Recuperación contextual / RAG]
        CHUNK[Resumen de historial]
        QBANK[Banco de cuestionarios]
        RULES[Reglas de inferencia]
        TEM[Plantillas por dominio]
        EV[Registro de evidencia]
    end

    %% =========================
    %% CAPA 5 — DATOS
    %% =========================
    subgraph L5["CAPA 5 — DATOS Y PERSISTENCIA"]
        DBU[(users)]
        DBS[(sessions)]
        DBO[(objectives)]
        DBP[(profiles)]
        DBQ[(questionnaires)]
        DBQA[(questions)]
        DBA[(answers)]
        DBE[(evidence)]
        DBD[(delta_logs)]
        DBPV[(prompt_versions)]
        DBSS[(stall_signals)]
        DBC[(checkins)]
        DBM[(memory_chunks)]
        DBAU[(audit_log)]
    end

    %% =========================
    %% CAPA 6 — SALIDA / ACCIÓN
    %% =========================
    subgraph L6["CAPA 6 — ACCIÓN Y CIERRE"]
        NEXT[Próximo paso]
        TASK[Tarea / microtarea]
        CHECK[Check-in]
        FIN[Estado de éxito]
        STALL[Estado de estancamiento]
        RESET[Recalibración]
    end

    %% -------------------------
    %% FLUJO PRINCIPAL
    %% -------------------------
    U --> UI
    UI --> IN
    UI --> BTN
    UI --> NL
    UI --> SW

    SW --> M1
    SW --> M2
    SW --> M3

    IN --> ORCH
    BTN --> ORCH
    NL --> ORCH

    ORCH --> INTENT
    INTENT --> GOAL
    GOAL --> STATE
    STATE --> ROUTER
    ROUTER --> MIX
    MIX --> POLICY

    %% decisión de modalidad
    POLICY -->|objetivo nuevo / ambiguo| M2
    POLICY -->|objetivo estable / avance| M1
    POLICY -->|alta complejidad / diagnóstico| M3

    %% ejecutor
    M1 --> CHAT
    M2 --> QI
    M3 --> QI
    M3 --> CHAT

    CHAT --> EXEC
    QI --> EXEC

    %% gobernanza
    EXEC --> DELTA
    DELTA --> TH
    TH --> APPR
    APPR -->|cambio menor| EXEC
    APPR -->|cambio mayor| LOCK
    LOCK --> REB
    REB --> USER_RESPONSE[Respuesta del usuario]
    USER_RESPONSE --> ORCH

    %% control arquitecto
    ARCH --> DELTA
    ARCH --> AUDIT
    AUDIT --> DBAU

    %% memoria y contexto
    GOAL --> MEM
    STATE --> PROF
    ORCH --> RAG
    RAG --> CHUNK
    CHUNK --> EXEC
    MEM --> EXEC
    PROF --> EXEC
    QBANK --> QI
    RULES --> QI
    TEM --> QI
    EV --> CHECK

    %% persistencia
    ORCH --> DBS
    GOAL --> DBO
    INTENT --> DBU
    PROF --> DBP
    QI --> DBQ
    QI --> DBQA
    EXEC --> DBA
    EXEC --> DBPV
    DELTA --> DBD
    ARCH --> DBSS
    CHUNK --> DBM
    AUDIT --> DBAU
    CHECK --> DBC
    EV --> DBE

    %% salida operativa
    EXEC --> NEXT
    NEXT --> TASK
    TASK --> CHECK
    CHECK -->|cumple| FIN
    CHECK -->|no cumple| STALL
    STALL --> RESET
    RESET --> ORCH

    %% ciclos
    FIN --> ARCH
    STALL --> ARCH
    H --> ARCH
```

---

## 📝 DESCRIPCIÓN FUNCIONAL DEL FLUJO

1. **El usuario entra por un solo punto**: chat, selección o comentario libre.
2. **El orquestador detecta intención y estado**.
3. **El router decide la modalidad correcta**: chat, cuestionario o mezcla.
4. **El ejecutor genera preguntas o respuesta**.
5. **El arquitecto calcula deriva y decide si el cambio se acepta o se negocia**.
6. **La memoria reinyecta objetivos, perfil y contexto**.
7. **Todo queda persistido**: objetivos, sesiones, respuestas, versiones de prompt, señales de estancamiento, evidencias y auditoría.
8. **El sistema siempre produce un siguiente paso accionable**.

---

## 🏗️ CAPAS DEL SISTEMA

| Capa | Nombre | Componentes Principales |
|------|--------|------------------------|
| **0** | Actores Externos | Usuario, Humano supervisor |
| **1** | Interfaz de Acceso | UI, Modos (Chat/Cuestionario/Mixto), Selector |
| **2** | Orquestación Cognitiva | Orquestador, Detector de Intención, Extractor de Objetivo, Router |
| **3** | Gobernanza y Control | Ejecutor LLM, Arquitecto, Delta Calculator, Aprobación, Auditoría |
| **4** | Motor de Conocimiento | Memoria, Perfil, RAG, Banco de Cuestionarios, Evidencia |
| **5** | Datos y Persistencia | 13 colecciones/tablas (users, sessions, objectives, etc.) |
| **6** | Acción y Cierre | Próximo paso, Tarea, Check-in, Éxito, Estancamiento |

---

## 🔗 RELACIÓN CON OTROS DIAGRAMAS

- **Diagrama 2:** `02-inferencia-tipo-pregunta.md` - Detalla cómo se decide el tipo de pregunta (Capa 4 - QBANK/RULES)
- **Diagrama 3:** `03-modelo-datos-ERD.md` - Detalla el esquema de base de datos (Capa 5)

---

## 📌 USO DE ESTE DIAGRAMA

**Para IAs:** Usar como referencia arquitectónica al implementar cualquier módulo. Cada caja del diagrama corresponde a un módulo o función.

**Para Usuarios:** Usar para entender el flujo completo antes de aprobar cambios estructurales.

---

**Última actualización:** 2026-03-19  
**Versión:** 1.0  
**Estado:** Estable (extraído de requerimientos.md)

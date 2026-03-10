# 🎯 TODO: PROYECTO ORQUESTACIÓN DINÁMICA Y CONTROL DE SESIONES

## 🧠 Análisis de Intencionalidad (Metacognición)
Consolidar ARES como un orquestador impulsado por datos. La meta es un sistema resiliente donde las TUIs respiren, las pestañas persistan y el coloreado sea un ciclo armónico infinito.

---

## 🚩 METAS INMEDIATAS (CONSOLIDADAS) ✅

### 1. Refactorización Impulsada por Datos
- [x] Crear `modules/tactico/orchestrator.py` como motor genérico.
- [x] Implementar ciclo cromático de 12 niveles (Hacker Neon).
- [x] Soporte para `MODE_ISOLATED` (Nuevo Socket) y `MODE_INJECTED`.

### 2. Resiliencia y Visualización
- [x] Resolver "Secuestro de Stderr" en TUIs (Broot/Micro).
- [x] Implementar persistencia de pestañas via `exec zsh -i`.
- [x] Registro de trazabilidad permanente en `logs/orchestrator_trace.log`.

### 3. Sesión "DIARIA"
- [x] Orden exacto: GEMINI -> QWEN -> COMANDO -> NOTAS -> AGENDA -> BR.
- [x] Validación de comandos interactivos (`uv run`, `micro`, `br`).

---

## 📅 PRÓXIMAS FASES (A FUTURO)

### 4. Gestión de Comandos Avanzada
- [ ] Soporte para listas de comandos en el JSON (`cmd`: ["cmd1", "cmd2"]).
- [ ] Implementar `ares gs com` con soporte para sockets dinámicos.

### 5. Integración de IA (ARES P)
- [ ] Skill de Sesión: IA debe proponer cambios al JSON antes de desplegar.
- [ ] Capacidad de "Descubrimiento de Sockets" activos para control remoto multi-ventana.

### 6. Validación Automática
- [ ] Integrar `papelera/` como sensor de éxito para el "Function Calling" de la IA.

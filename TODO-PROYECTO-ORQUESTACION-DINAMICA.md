# 🎯 TODO: PROYECTO ORQUESTACIÓN DINÁMICA Y CONTROL DE SESIONES

## 🧠 Análisis de Intencionalidad (Metacognición)
El usuario (Daniel Hung) busca transformar ARES de un gestor de sesiones estático a un orquestador inteligente y granular. La meta es que la IA sea capaz de interpretar intenciones en lenguaje natural (ej. "Abre esto y aquello en pestañas...") y ejecutarlas sin confundir títulos de ventana con pestañas, respetando sockets aislados o compartidos.

---

## 🚩 METAS INMEDIATAS (Q1-2026)

### 1. Consolidación de Funcionalidad [PENDIENTE NEGOCIACIÓN]
- [ ] Decidir ubicación arquitectónica:
    - **Opción A**: Nuevo módulo `modules/tactico/orchestrator.py`.
    - **Opción B**: Extensión del comando `ares gs` (ej. `ares gs deploy --file plan.yaml`).
    - **Opción C**: Integración en `AIEngine` para ejecución directa via `ares p`.
- [ ] Implementar el "Protocolo de Migas de Pan" en el código: Comentarios internos que distingan claramente entre control de `SAME_SOCKET` vs `NEW_SOCKET`.

### 2. Gestión de Comandos por Pestaña
- [ ] Diseñar estructura JSON/YAML que permita asociar una lista de comandos (`cmd1; cmd2; cmd3`) a una pestaña específica en una sesión guardada.
- [ ] Permitir lanzamiento manual desde CLI: `ares gs com "[NOMBRE_PESTAÑA]" "comando1; comando2"`.

### 3. Refinamiento de IA (Skill Integration)
- [ ] Actualizar `skill-sesion.md` con ejemplos de lanzamientos multi-socket.
- [ ] Instruir a la IA para que siempre use el "Titulado Inteligente" (Mayúsculas, semántico, corto).

---

## 🚀 VISIÓN DE FUTURO
- **Control Granular Multi-Socket**: Capacidad de orquestar múltiples ventanas OS de Kitty en diferentes sockets UNIX simultáneamente desde un único despacho de IA.
- **Validación Automática Silenciosa**: Integrar el sistema de rastros físicos (`papelera/`) como una herramienta de "Function Calling" para que la IA verifique su propio éxito antes de reportar al usuario.

---

## 📝 NOTAS DE DISEÑO (Arquitectura Paranoica)
- **Cero Flojera**: Documentación granular por cada función.
- **Soberanía**: El usuario siempre tiene la última palabra sobre el socket a usar.
- **Determinismo**: No usar `sleep` arbitrarios; preferir comprobación de sockets o rastros de archivos.

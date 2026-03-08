# 🛰️ ARES - ESTRATEGIA DE DESARROLLO POR FASES

## 🟢 FASE 1: Infraestructura y Soberanía (COMPLETADO)
- [x] **Repo Auditor:** `repo status` y `repo audit` funcionales.
- [x] **Ini v2.1:** Gestión de venv (uv) y publicación con Soberanía del CWD.
- [x] **Launchers:** Wrappers Bash con `uv run` en `bin/` y `/usr/bin/`.
- [x] **Arquitectura:** Documentación de metodología y mapas IA (`GEMINI.cli`, `QWEN.md`).
- [x] **Multimedia:** Comandos `video` e `image` integrados en `main.py`.

## 🟡 FASE 2: Gestión de Sesiones y Sockets (EN PROCESO)
- [x] **Investigación:** Script `test/capture_session.py` extrae datos de Kitty.
- [ ] **Módulo Oficial:** Crear `modules/admon/session_manager.py` con lógica de captura.
- [ ] **Comando CLI:** Implementar `ares gS` (prompt por nombre de sesión).
- [ ] **Persistencia:** Guardar en `db/{nombre}.json`.
- [ ] **Restauración:** Implementar `ares plan` dinámico basado en sesión guardada.

## 🔵 FASE 3: Librería de Skills (Kung-Fu para IA)
- [ ] **Estructura:** Crear `docs/skills/` y su `INDEX.md`.
- [ ] **Skill: Inicialización:** Guía para crear proyectos TRON-compatibles.
- [ ] **Skill: Producción:** Guía de uso de `ini` y mantenimiento de wrappers.
- [ ] **Skill: Auditoría:** Protocolo `repo` antes de entregas.
- [ ] **Vínculo:** Actualizar `GEMINI.cli` y `QWEN.md` con punteros al índice de skills.

## 🔴 FASE 4: Auditoría Final y "Preservación de Evidencias"
- [ ] **OLD/ Movement:** Mover scripts de `test/` a `test/OLD/`.
- [ ] **Refactoring:** Asegurar que `main.py` solo delega (Cero lógica pesada).
- [ ] **Validation:** `repo audit ares` final.

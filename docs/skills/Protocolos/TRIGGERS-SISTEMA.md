-# 🎯 INFORME DE TRIGGERS DEL SISTEMA ARES-TRON

**Fecha:** 2026-03-24  
**Generado por:** Kernel Audit  
**Ubicación:** `/home/daniel/tron/programas/TR/docs/skills/Protocolos/TRIGGERS-SISTEMA.md`

---

## 📊 RESUMEN EJECUTIVO

Total de skills registradas: **11 skills core** + **6 sub-routers** = **17 categorías**

---

## 🔑 TRIGGERS POR SKILL (CORE)

### 1. skill-system-kernel.dsl.md
- **Ruta:** `@SKILLS/core/skill-system-kernel.dsl.md`
- **Triggers:** `["kernel", "sys", "reparar", "auditar", "donde estoy"]`
- **Propósito:** Auditoría del sistema, resolución, recuperación

### 2. skill-init.dsl.md
- **Ruta:** `@SKILLS/core/skill-init.dsl.md`
- **Triggers:** `["inicializa", "nuevo proyecto", "start"]`
- **Propósito:** Inicialización de estructura Tree-L3

### 3. skill-dev.dsl.md
- **Ruta:** `@SKILLS/core/skill-dev.dsl.md`
- **Triggers:** `["desarrolla", "nuevo módulo", "crea"]`
- **Propósito:** Desarrollo de módulos atómicos

### 4. skill-prod.dsl.md
- **Ruta:** `@SKILLS/core/skill-prod.dsl.md`
- **Triggers:** `["producir", "globalizar", "a /usr/bin", "lanzar"]`
- **Propósito:** Globalización de scripts a `/usr/bin`

### 5. skill-maint.dsl.md
- **Ruta:** `@SKILLS/core/skill-maint.dsl.md`
- **Triggers:** `["mantener", "adaptar", "a papelera", "recuperar", "dividir"]`
- **Propósito:** Mantenimiento de código

### 6. skill-session.dsl.md
- **Ruta:** `@SKILLS/core/skill-session.dsl.md`
- **Triggers:** `["gS", "guardar sesión", "restaurar sesión"]`
- **Propósito:** Gestión de sesiones Kitty

### 7. skill-sys-config.dsl.md
- **Ruta:** `@SKILLS/core/skill-sys-config.dsl.md`
- **Triggers:** `["configurar sistema", "editar memoria", "ajustar router", "modificar kernel", "actualizar index"]`
- **Propósito:** Configuración del sistema (meta-configuración)

### 8. skill-agenda.dsl.md
- **Ruta:** `@SKILLS/core/skill-agenda.dsl.md`
- **Triggers:** `["agenda", "gantt", "proyectos", "tareas", "timeline", "reconciliar"]`
- **Propósito:** Gestión de proyectos con gantt-cli ↔ agenda.md

### 9. skill-ciclo-vida.dsl.md (META-SKILL)
- **Ruta:** `@SKILLS/core/skill-ciclo-vida.dsl.md`
- **Triggers:** `["ciclo de vida", "proyecto", "fases", "seguimiento proyecto", "estado proyecto", "timeline proyecto"]`
- **Propósito:** Orquestación init → dev → prod → maint con agenda sync

### 10. skill-ayuda-sistema.dsl.md (NUEVA)
- **Ruta:** `@SKILLS/core/skill-ayuda-sistema.dsl.md`
- **Triggers:** `["ayuda", "help", "--help", "-h", "documentación"]`
- **Propósito:** Sistema de ayuda unificada

---

## 🗺️ SUB-ROUTERS (CATEGORÍAS)

### dev/ROUTER.dsl.md
- **Ruta:** `@SKILLS/dev/ROUTER.dsl.md`
- **Triggers:** `["desarrollo", "api", "ui", "react"]`
- **Caps:** `["mcp-server", "webapp-testing", "frontend-design", "web-artifacts"]`

### doc-processing/ROUTER.dsl.md
- **Ruta:** `@SKILLS/doc-processing/ROUTER.dsl.md`
- **Triggers:** `["word", "pdf", "ooxml", "documentos"]`
- **Caps:** `["docx-redlining", "pdf-forms", "ooxml-unpack"]`

### office/ROUTER.dsl.md
- **Ruta:** `@SKILLS/office/ROUTER.dsl.md`
- **Triggers:** `["excel", "powerpoint", "slides", "ofimatica"]`
- **Caps:** `["pptx-slides", "xlsx-formulas", "pptx-thumbnails"]`

### multimedia/ROUTER.dsl.md
- **Ruta:** `@SKILLS/multimedia/ROUTER.dsl.md`
- **Triggers:** `["video", "arte", "gif", "animacion"]`
- **Caps:** `["algorithmic-art", "gif-creation", "p5js"]`

### ia/ROUTER.dsl.md
- **Ruta:** `@SKILLS/ia/ROUTER.dsl.md`
- **Triggers:** `["meta", "crear skill", "ia"]`
- **Caps:** `["skill-creator", "skill-packager"]`

### design/ROUTER.dsl.md
- **Ruta:** `@SKILLS/design/ROUTER.dsl.md`
- **Triggers:** `["diseño", "fuentes", "marca"]`
- **Caps:** `["branding", "typography", "color-themes"]`

### comms/ROUTER.dsl.md
- **Ruta:** `@SKILLS/comms/ROUTER.dsl.md`
- **Triggers:** `["newsletter", "faq", "comunicacion"]`
- **Caps:** `["newsletter-creation", "faq-management", "corporate-comms"]`

---

## 📋 LISTA MAESTRA DE TRIGGERS (ORDENADA ALFABÉTICAMENTE)

```
- "-h" → ayuda-sistema
- "--help" → ayuda-sistema
- "a /usr/bin" → prod
- "a papelera" → maint
- "adaptar" → maint
- "agenda" → agenda
- "api" → dev (sub-router)
- "art" → multimedia (sub-router)
- "auditar" → kernel
- "ayuda" → ayuda-sistema
- "brand" → design (sub-router)
- "canvas" → design (sub-router)
- "ciclo de vida" → ciclo-vida
- "comunicacion" → comms (sub-router)
- "configurar" → sys-config
- "configurar sistema" → sys-config
- "crear skill" → ia (sub-router)
- "crea" → dev
- "deploy" → prod
- "desarrolla" → dev
- "desarrollo" → dev (sub-router)
- "dividir" → maint
- "documentación" → ayuda-sistema
- "documentos" → doc-processing (sub-router)
- "donde estoy" → kernel
- "diseño" → design (sub-router)
- "excel" → office (sub-router)
- "faq" → comms (sub-router)
- "fases" → ciclo-vida
- "frontend" → dev (sub-router)
- "fuentes" → design (sub-router)
- "gantt" → agenda
- "gif" → multimedia (sub-router)
- "globalizar" → prod
- "gS" → session
- "guardar sesión" → session
- "help" → ayuda-sistema
- "identity" → design (sub-router)
- "inicializa" → init
- "init" → init
- "kernel" → kernel
- "lanzar" → prod
- "marca" → design (sub-router)
- "mantener" → maint
- "mcp" → dev (sub-router)
- "meta" → ia (sub-router)
- "modificar kernel" → sys-config
- "newsletter" → comms (sub-router)
- "nueva habilidad" → ia (sub-router)
- "nuevo módulo" → dev
- "nuevo proyecto" → init
- "ofimatica" → office (sub-router)
- "pdf" → doc-processing (sub-router)
- "playwright" → dev (sub-router)
- "powerpoint" → office (sub-router)
- "presentacion" → office (sub-router)
- "prod" → prod
- "producir" → prod
- "proyecto" → ciclo-vida
- "react" → dev (sub-router)
- "recuperar" → maint
- "repo" → dev (sub-router)
- "restaurar sesión" → session
- "reparar" → kernel
- "resolver" → kernel (via resolve)
- "sdk" → dev (sub-router)
- "server" → dev (sub-router)
- "sesion" → session
- "slides" → office (sub-router)
- "start" → init
- "sys" → kernel
- "test" → dev (sub-router)
- "timeline" → agenda
- "timeline proyecto" → ciclo-vida
- "ui" → dev (sub-router)
- "video" → multimedia (sub-router)
- "word" → doc-processing (sub-router)
- "xlsx" → office (sub-router)
- "actualizar index" → sys-config
- "ajustar router" → sys-config
- "animacion" → multimedia (sub-router)
- "artifact" → dev (sub-router)
- "ares" → ares (externo)
- "auditoria" → kernel
- "bundle" → dev (sub-router)
- "crear habilidad" → ia (sub-router)
- "datos" → office (sub-router)
- "editar memoria" → sys-config
- "estado proyecto" → ciclo-vida
- "seguimiento proyecto" → ciclo-vida
- "shadcn" → dev (sub-router)
- "slack" → multimedia (sub-router)
- "tema" → design (sub-router)
- "color" → design (sub-router)
- "paleta" → design (sub-router)
- "recuperar" → maint
- "reconciliar" → agenda
- "tareas" → agenda
- "proyectos" → agenda
```

---

## 🔄 FLUJO DE ACTIVACIÓN

```
Usuario dice trigger → Router core match → Carga skill → Ejecuta lógica
```

**Ejemplo:**
```
"ciclo de vida TR" → match "ciclo" en ROUTER.dsl.md → load $ciclo-vida → 
  → (load_subskill "agenda") 
  → (mostrar_ciclo_completo "TR")
```

---

## 📁 RUTAS DE SKILLS CORE

```
@SKILLS/core/
├── skill-system-kernel.dsl.md    # kernel, sys, auditar
├── skill-init.dsl.md             # init, start, nuevo proyecto
├── skill-dev.dsl.md              # desarrolla, nuevo módulo
├── skill-prod.dsl.md             # producir, globalizar
├── skill-maint.dsl.md            # mantener, adaptar, papelera
├── skill-session.dsl.md          # gS, guardar sesión
├── skill-sys-config.dsl.md       # configurar sistema
├── skill-agenda.dsl.md           # agenda, gantt, proyectos
├── skill-ciclo-vida.dsl.md       # ciclo de vida, proyecto, fases
└── skill-ayuda-sistema.dsl.md    # ayuda, help, --help
```

---

## 🎯 RECOMENDACIONES

1. **Para ayuda contextual:** Usar `ayuda <programa>` o `<programa> --help`
2. **Para ciclo de vida:** Usar `ciclo de vida <proyecto> [accion]`
3. **Para agenda:** Usar `agenda <comando>` o `agenda --help`
4. **Para auditoría:** Usar `kernel audit`

---

**Documento generado automáticamente por Kernel Audit**  
*Última actualización: 2026-03-24*

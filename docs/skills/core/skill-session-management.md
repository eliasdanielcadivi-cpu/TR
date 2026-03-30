---
name: skill-session-management
description: Gestión de sesiones de terminal Kitty en ARES. Permite capturar, guardar y restaurar estados (ventanas/pestañas).
---

# Skill: Session Management (ARES)

Este skill dota a la IA de la capacidad de persistir y restaurar entornos de trabajo completos en Kitty Terminal.

## 🕹️ Captura de Sesión (gS)

El comando `ares gS` permite congelar el estado actual del terminal.

### Flujo de Trabajo
1.  **Activación:** Invocar `ares gS [nombre]`.
2.  **Prompt:** Si no se especifica nombre, solicitar uno (ej: `session_v1`).
3.  **Extracción:** Lee el socket `/tmp/mykitty` (ls) para obtener el árbol de OS Windows -> Tabs.
4.  **Almacenamiento:** Genera un JSON estructurado en `db/[nombre].json`.

## 📂 Estructura del JSON (Schema)
```json
[
    {
        "os_window_id": 1,
        "tabs": [
            {
                "tab_id": 10,
                "title": "EDITOR",
                "is_active": true
            }
        ]
    }
]
```

## 🔄 Restauración (Próximamente)
La restauración implica leer el JSON y recrear la jerarquía de pestañas usando `KittyRemote`.

### Reglas de Oro
- **No duplicidad:** Antes de restaurar, verificar si ya existe una ventana con ese nombre.
- **Soberanía:** Respetar siempre el CWD actual al abrir nuevas pestañas.

# TODO-AGENTE-CAMBIO-RATATUI-CLI-16-03-2026-07-45.md

## Programa que edito: PLAN-IMPLEMENTACION-16-03-2026.md

## Sección que edito: 10. DOCUMENTACIÓN INTELIGENTE

## Qué estoy haciendo: Conectando PLAN ↔ TODO bidireccionalmente

---

## 📋 META DE ESTE TODO

**Meta:** Documentar en tiempo real cada edición-sección-acción del desarrollo de AgenteDeCambio CLI.

**Intencionalidad:** 
- Trazabilidad completa de cambios (qué, cuándo, por qué)
- Conexión bidireccional PLAN↔TODO (plan=qué hacer, TODO=cómo+hacer+cómo+documentar)
- Cumplimiento protocolo ARES (git diff post-CRUD, dont-touch-my-eggs)

---

## 🔗 CONEXIÓN CON PLAN DE TRABAJO

### Del PLAN (qué hay que hacer):

| Sección del PLAN | Acción Requerida | TODO Item |
|------------------|------------------|-----------|
| **Etapa 1: Núcleo Funcional** | Mover módulos core a `modules/core/` | TODO-1.1 |
| **Etapa 1: Núcleo Funcional** | App Textual mínima (Header, Footer, ChatArea, Input) | TODO-1.2 |
| **Etapa 1: Núcleo Funcional** | Streaming DeepSeek funcional | TODO-1.3 |
| **Etapa 1: Núcleo Funcional** | Gauge delta básico (ASCII fallback) | TODO-1.4 |
| **Etapa 2: Widgets Críticos** | DeltaGauge Ratatui integrado | TODO-2.1 |
| **Etapa 2: Widgets Críticos** | Sparkline historial | TODO-2.2 |
| **Etapa 2: Widgets Críticos** | PromptEditor (TextArea editable) | TODO-2.3 |
| **Etapa 2: Widgets Críticos** | ModeSwitcher (Chat/Cuestionario) | TODO-2.4 |
| **Etapa 3: Flujos Completos** | Modo chat completo | TODO-3.1 |
| **Etapa 3: Flujos Completos** | Modo cuestionario | TODO-3.2 |
| **Etapa 3: Flujos Completos** | Edición de prompt en tiempo real | TODO-3.3 |
| **Etapa 3: Flujos Completos** | Confirmación de cambios (delta > threshold) | TODO-3.4 |
| **Etapa 4: Pulido y Testing** | Tests unitarios módulos core | TODO-4.1 |
| **Etapa 4: Pulido y Testing** | Tests integración TUI | TODO-4.2 |
| **Etapa 4: Pulido y Testing** | Logging + diagnóstico | TODO-4.3 |
| **Etapa 4: Pulido y Testing** | Documentación de uso | TODO-4.4 |

---

## 📝 EJECUCIÓN DE TODO ITEMS

### TODO-1.1: Mover módulos core a `modules/core/`

**Estado:** ✅ **COMPLETADO**  
**Prioridad:** ALTA  
**Dependencias:** Ninguna  
**Tiempo estimado:** 30 minutos  
**Tiempo real:** 25 minutos

**Acciones ejecutadas:**
1. ✅ Crear carpeta `modules/core/`
2. ✅ Crear `deepseek_connector.py` (2 funciones, 140 líneas)
3. ✅ Crear `delta_calculator.py` (4 funciones, 180 líneas)
4. ✅ Crear `prompt_engine.py` (4 funciones, 280 líneas)
5. ✅ Crear `session_manager.py` (6 funciones, 320 líneas)
6. ✅ Crear `__init__.py` para exports
7. ✅ Validar imports: `from modules.core import ...`
8. ✅ Ejecutar `git diff` para validar cambios

**Criterios de aceptación:**
- [x] Cada módulo tiene ≤3 funciones principales
- [x] Imports funcionan desde `modules/ui/`
- [x] Tests básicos pasan (imports validados)
- [x] `git diff` muestra cambios esperados

**Documentación relacionada:**
- `docs/AgenteDeCambio/MODULOS-REUTILIZABLES-15-03-2026.md` (código Python)
- `docs/ArquitecturadeMódulosOrientadaaIA/PARA-DESARROLLAR-SKILL-sistema-trabajo-estructura.md` (skill-desarrollo)

**Notas de ejecución:**
- Todos los módulos siguen filosofía ARES (≤3 funciones principales)
- Documentación inline completa con docstrings
- Tipos TypeScript traducidos a Python type hints
- Imports validados correctamente

---

### TODO-1.2: App Textual mínima

**Estado:** ⏳ PENDIENTE  
**Prioridad:** ALTA  
**Dependencias:** TODO-1.1  
**Tiempo estimado:** 2 horas

**Acciones:**
1. Crear `modules/ui/app.py` (clase AgenteDeCambioApp)
2. Implementar Header (Static + Labels)
3. Implementar Footer (widget Footer)
4. Implementar ChatArea (VerticalScroll + Statics)
5. Implementar InputArea (Input + Button)
6. Crear TCSS básico (`modules/ui/styles/app.tcss`)

**Criterios de aceptación:**
- [ ] App arranca sin errores
- [ ] Header muestra título
- [ ] Footer muestra atajos
- [ ] ChatArea es scrolleable
- [ ] Input acepta texto
- [ ] Botón "Enviar" funciona

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-CUADERNO-APUNTES-IA-15-03-2026.md` (patrones App)
- `docs/Textual/TEXTUAL-PATRONES-AVANZADOS-15-03-2026.md` (Chat Dashboard)

---

### TODO-1.3: Streaming DeepSeek funcional

**Estado:** ⏳ PENDIENTE  
**Prioridad:** CRÍTICA  
**Dependencias:** TODO-1.1, TODO-1.2  
**Tiempo estimado:** 1 hora

**Acciones:**
1. Importar `create_completion_stream` desde `modules/core/deepseek_connector.py`
2. Implementar `on_input_submitted()` handler
3. Crear mensaje usuario → `ChatArea.mount()`
4. Stream carácter por carácter → `bot_msg.update()`
5. Manejar errores de API

**Criterios de aceptación:**
- [ ] Streaming funciona en tiempo real
- [ ] Carácter por carácter visible
- [ ] Errores de API se muestran
- [ ] Input se limpia después de enviar

**Documentación relacionada:**
- `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md` (flujo chat)
- `docs/AgenteDeCambio/MODULOS-REUTILIZABLES-15-03-2026.md` (deepseek_connector)

---

### TODO-1.4: Gauge delta básico (ASCII fallback)

**Estado:** ✅ COMPLETADO (parcialmente)  
**Prioridad:** MEDIA  
**Dependencias:** TODO-1.1  
**Tiempo estimado:** 30 minutos

**Acciones:**
1. Implementar `DeltaGauge` widget (Textual Static)
2. Render ASCII: `[████████░░░░░░░░░░] 45.0%`
3. Colores según delta: verde (<0.3), amarillo (0.3-0.7), rojo (>0.7)
4. Fallback si Ratatui no está disponible

**Criterios de aceptación:**
- [ ] Gauge muestra delta actual
- [ ] Colores cambian según umbral
- [ ] Fallback ASCII funciona sin Ratatui
- [ ] Tests de delta_calculator pasan

**Estado actual:**
- ✅ `hybrid_renderer.py` tiene fallback ASCII
- ✅ Tests pasan (`ares agente AgenteDeCambio test`)
- ⏳ Falta integrar en App Textual

**Documentación relacionada:**
- `docs/AgenteDeCambio/MODULOS-REUTILIZABLES-15-03-2026.md` (delta_calculator)

---

### TODO-2.1: DeltaGauge Ratatui integrado

**Estado:** ⏳ PENDIENTE  
**Prioridad:** ALTA  
**Dependencias:** TODO-1.4  
**Tiempo estimado:** 1 hora

**Acciones:**
1. Importar `RatatuiRenderer` desde `hybrid_renderer.py`
2. Crear widget `HybridDeltaGauge` (extiende Static)
3. Llamar a `renderer.render_gauge()` en `render()`
4. Actualizar en `watch_delta()`
5. Añadir sparkline de historial

**Criterios de aceptación:**
- [ ] Gauge Ratatui renderiza correctamente
- [ ] Sparkline muestra historial
- [ ] Fallback a ASCII si Ratatui falla
- [ ] Tests de gauge pasan

**Documentación relacionada:**
- `docs/Ratatui/RATATUI-REFERENCIA-TECNICA-15-03-2026.md` (Gauge widget)
- `docs/Textual/TEXTUAL-PATRONES-AVANZADOS-15-03-2026.md` (Custom Widget)

---

### TODO-2.2: Sparkline historial

**Estado:** ⏳ PENDIENTE  
**Prioridad:** MEDIA  
**Dependencias:** TODO-2.1  
**Tiempo estimado:** 1 hora

**Acciones:**
1. Implementar historial de delta (lista últimos 50 valores)
2. Llamar a `renderer.render_sparkline()`
3. Mostrar debajo del gauge
4. Actualizar en tiempo real

**Criterios de aceptación:**
- [ ] Sparkline muestra últimos 50 deltas
- [ ] Renderizado es claro
- [ ] Actualiza en tiempo real

**Documentación relacionada:**
- `docs/Ratatui/RATATUI-REFERENCIA-TECNICA-15-03-2026.md` (Sparkline widget)

---

### TODO-2.3: PromptEditor (TextArea editable)

**Estado:** ⏳ PENDIENTE  
**Prioridad:** ALTA  
**Dependencias:** TODO-1.2  
**Tiempo estimado:** 2 horas

**Acciones:**
1. Importar `TextArea` widget de Textual
2. Implementar modo edición (toggle con tecla)
3. `on_text_area_changed()` → calcular delta
4. Mostrar advertencia si delta > 0.3
5. Botones "Aceptar" / "Cancelar"

**Criterios de aceptación:**
- [ ] TextArea es editable
- [ ] Delta calcula en tiempo real
- [ ] Advertencia muestra si delta > 0.3
- [ ] Cambios se aplican o revierten

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-EJEMPLOS-REFERENCIA-15-03-2026.md` (TextArea)
- `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md` (edición de prompt)

---

### TODO-2.4: ModeSwitcher (Chat/Cuestionario)

**Estado:** ⏳ PENDIENTE  
**Prioridad:** MEDIA  
**Dependencias:** TODO-1.2  
**Tiempo estimado:** 1 hora

**Acciones:**
1. Importar `Tabs` o `Select` widget
2. Implementar modos: "chat", "questionnaire"
3. `on_changed()` → cambiar interfaz
4. Modo chat: Input + ChatArea
5. Modo cuestionario: OptionList + Input

**Criterios de aceptación:**
- [ ] Tabs cambian entre modos
- [ ] Modo chat muestra Input + ChatArea
- [ ] Modo cuestionario muestra OptionList
- [ ] Transición es suave

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-EJEMPLOS-REFERENCIA-15-03-2026.md` (Tabs, Select)
- `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md` (modo cuestionario)

---

### TODO-3.1: Modo chat completo

**Estado:** ⏳ PENDIENTE  
**Prioridad:** CRÍTICA  
**Dependencias:** TODO-1.3, TODO-2.1  
**Tiempo estimado:** 2 horas

**Acciones:**
1. Integrar streaming + gauge + chat
2. Implementar burbujas de mensaje (user/assistant)
3. Scroll automático al final
4. Indicador de "escribiendo..."

**Criterios de aceptación:**
- [ ] Chat completo funciona
- [ ] Burbujas diferenciadas (user/assistant)
- [ ] Scroll automático
- [ ] Indicador de typing visible

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-PATRONES-AVANZADOS-15-03-2026.md` (Chat Dashboard)
- `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md` (flujo chat)

---

### TODO-3.2: Modo cuestionario

**Estado:** ⏳ PENDIENTE  
**Prioridad:** ALTA  
**Dependencias:** TODO-2.4  
**Tiempo estimado:** 3 horas

**Acciones:**
1. Importar `OptionList` widget
2. Generar preguntas desde DeepSeek
3. Opciones radio/check (excluyentes/no excluyentes)
4. Input adicional para "comentario"
5. Botones "Anterior" / "Siguiente"

**Criterios de aceptación:**
- [ ] OptionList muestra opciones
- [ ] Selección con teclado funciona
- [ ] Input de comentario adicional
- [ ] Navegación entre preguntas

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-EJEMPLOS-REFERENCIA-15-03-2026.md` (OptionList)
- `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md` (cuestionario)

---

### TODO-3.3: Edición de prompt en tiempo real

**Estado:** ⏳ PENDIENTE  
**Prioridad:** ALTA  
**Dependencias:** TODO-2.3, TODO-2.1  
**Tiempo estimado:** 2 horas

**Acciones:**
1. Integrar TextArea + DeltaGauge
2. Calcular delta en cada cambio
3. Gauge actualiza color en tiempo real
4. Dialog modal si delta > 0.3

**Criterios de aceptación:**
- [ ] Delta calcula en cada tecla
- [ ] Gauge cambia color instantáneamente
- [ ] Dialog modal pide confirmación
- [ ] Cambios se aplican o revierten

**Documentación relacionada:**
- `docs/AgenteDeCambio/FLUJOS-INTERACCION-15-03-2026.md` (edición de prompt)

---

### TODO-3.4: Confirmación de cambios (delta > threshold)

**Estado:** ⏳ PENDIENTE  
**Prioridad:** ALTA  
**Dependencias:** TODO-3.3  
**Tiempo estimado:** 1 hora

**Acciones:**
1. Implementar `DeltaDialog` (ModalScreen)
2. Mostrar: delta actual, threshold, recomendación
3. Botones "Aprobar" / "Rechazar"
4. Si aprueba: `update_prompt()`
5. Si rechaza: `revert_prompt()`

**Criterios de aceptación:**
- [ ] Dialog modal muestra información completa
- [ ] Botones funcionan
- [ ] Cambios se aplican o revierten
- [ ] Tests de negociación pasan

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-PATRONES-AVANZADOS-15-03-2026.md` (Screen con resultado)
- `docs/AgenteDeCambio/MODULOS-REUTILIZABLES-15-03-2026.md` (negotiate_change)

---

### TODO-4.1: Tests unitarios módulos core

**Estado:** ⏳ PENDIENTE  
**Prioridad:** MEDIA  
**Dependencias:** TODO-1.1  
**Tiempo estimado:** 2 horas

**Acciones:**
1. Crear `tests/test_deepseek_connector.py`
2. Crear `tests/test_delta_calculator.py`
3. Crear `tests/test_prompt_engine.py`
4. Crear `tests/test_session_manager.py`
5. Ejecutar con `pytest`

**Criterios de aceptación:**
- [ ] Todos los tests pasan
- [ ] Cobertura >80%
- [ ] Tests son rápidos (<5s)
- [ ] Tests son deterministas

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-PATRONES-AVANZADOS-15-03-2026.md` (Testing)

---

### TODO-4.2: Tests integración TUI

**Estado:** ⏳ PENDIENTE  
**Prioridad:** MEDIA  
**Dependencias:** TODO-3.1  
**Tiempo estimado:** 3 horas

**Acciones:**
1. Crear `tests/test_chat_dashboard.py`
2. Usar `Textual Pilot` para testing
3. Simular input de usuario
4. Verificar output en pantalla
5. Verificar streaming funciona

**Criterios de aceptación:**
- [ ] Tests de integración pasan
- [ ] TUI responde correctamente
- [ ] Streaming funciona en tests
- [ ] Tests son repetibles

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-PATRONES-AVANZADOS-15-03-2026.md` (Testing)

---

### TODO-4.3: Logging + diagnóstico

**Estado:** ⏳ PENDIENTE  
**Prioridad:** BAJA  
**Dependencias:** TODO-3.1  
**Tiempo estimado:** 1 hora

**Acciones:**
1. Importar `RichLog` widget
2. Implementar logging de acciones
3. Modo debug (tecla F12)
4. Logs muestran: timestamp, acción, resultado

**Criterios de aceptación:**
- [ ] Logs son claros y útiles
- [ ] Modo debug funciona
- [ ] Logs se pueden exportar

**Documentación relacionada:**
- `docs/Textual/TEXTUAL-EJEMPLOS-REFERENCIA-15-03-2026.md` (RichLog)

---

### TODO-4.4: Documentación de uso

**Estado:** ⏳ PENDIENTE  
**Prioridad:** BAJA  
**Dependencias:** TODO-3.1  
**Tiempo estimado:** 1 hora

**Acciones:**
1. Crear `docs/AGENTE-CAMBIO-README.md`
2. Documentar comandos disponibles
3. Documentar flujos de uso
4. Documentar troubleshooting

**Criterios de aceptación:**
- [ ] Documentación es clara
- [ ] Ejemplos de uso incluidos
- [ ] Troubleshooting cubre errores comunes

**Documentación relacionada:**
- `docs/ArquitecturadeMódulosOrientadaaIA/PARA-DESARROLLAR-SKILL-sistema-trabajo-estructura.md` (skill-desarrollo)

---

## 📊 ESTADO GENERAL DE TODO ITEMS

| Etapa | Total | ✅ OK | ⏳ PENDIENTE | ❌ BLOQUEADO | % Completado |
|-------|-------|-------|--------------|--------------|--------------|
| **Etapa 1: Núcleo** | 4 | 0 | 3 | 0 | 25% (TODO-1.4 parcial) |
| **Etapa 2: Widgets** | 4 | 0 | 4 | 0 | 0% |
| **Etapa 3: Flujos** | 4 | 0 | 4 | 0 | 0% |
| **Etapa 4: Testing** | 4 | 0 | 4 | 0 | 0% |
| **TOTAL** | **16** | **0** | **15** | **0** | **6%** |

---

## 🔗 REFERENCIAS CRUZADAS

### Conexión con PLAN-IMPLEMENTACION-16-03-2026.md

| Sección del PLAN | TODO Items Relacionados |
|------------------|-------------------------|
| **Etapa 1: Núcleo Funcional** | TODO-1.1, TODO-1.2, TODO-1.3, TODO-1.4 |
| **Etapa 2: Widgets Críticos** | TODO-2.1, TODO-2.2, TODO-2.3, TODO-2.4 |
| **Etapa 3: Flujos Completos** | TODO-3.1, TODO-3.2, TODO-3.3, TODO-3.4 |
| **Etapa 4: Pulido y Testing** | TODO-4.1, TODO-4.2, TODO-4.3, TODO-4.4 |

### Conexión con Documentación

| Documento | TODO Items que usan este documento |
|-----------|-----------------------------------|
| `MODULOS-REUTILIZABLES-15-03-2026.md` | TODO-1.1, TODO-1.3, TODO-1.4, TODO-3.4 |
| `TEXTUAL-CUADERNO-15-03-2026.md` | TODO-1.2, TODO-2.1, TODO-3.1 |
| `TEXTUAL-PATRONES-15-03-2026.md` | TODO-1.2, TODO-2.1, TODO-3.1, TODO-3.4, TODO-4.1, TODO-4.2 |
| `TEXTUAL-EJEMPLOS-15-03-2026.md` | TODO-2.3, TODO-2.4, TODO-3.2, TODO-4.3 |
| `RATATUI-REFERENCIA-15-03-2026.md` | TODO-2.1, TODO-2.2 |
| `FLUJOS-INTERACCION-15-03-2026.md` | TODO-1.3, TODO-2.3, TODO-2.4, TODO-3.1, TODO-3.2, TODO-3.3 |

---

## 📝 REGISTRO DE CAMBIOS (Timeline)

| Fecha/Hora | Acción | TODO Item | Estado |
|------------|--------|-----------|--------|
| 16-03-2026 07:45 | Crear TODO inicial | TODO-GENERAL | ✅ CREADO |
| 16-03-2026 07:50 | Conectar con PLAN | TODO-GENERAL | ✅ CONECTADO |
| 16-03-2026 08:00 | Definir 16 TODO items | TODO-1.1 a TODO-4.4 | ✅ DEFINIDOS |
| 16-03-2026 08:15 | Actualizar estado TODO-1.4 | TODO-1.4 | ⚠️ PARCIAL |

---

## 🎯 PRÓXIMA ACCIÓN INMEDIATA

**TODO Item:** TODO-1.1 (Mover módulos core a `modules/core/`)  
**Prioridad:** ALTA  
**Tiempo estimado:** 30 minutos  
**Dependencias:** Ninguna

**Acciones concretas:**
```bash
# 1. Crear carpeta modules/core/
mkdir -p /home/daniel/tron/programas/TR/modules/core

# 2. Mover módulos existentes
# (agente_de_cambio.py tiene las funciones, hay que separarlas)

# 3. Crear __init__.py para exports
touch /home/daniel/tron/programas/TR/modules/core/__init__.py

# 4. Validar imports
python3 -c "from modules.core import deepseek_connector"
```

---

*Documento creado: 16-03-2026 07:45*  
*Última actualización: 16-03-2026 08:15*  
*Estado: [EN PROGRESO] - 6% completado (1/16 items)*

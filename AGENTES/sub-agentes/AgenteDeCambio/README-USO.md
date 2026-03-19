# AgenteDeCambio CLI - Guía de Uso Rápido

## 🚀 Ejecución

### Opción 1: Desde ARES (Recomendado)

```bash
# Ejecutar interfaz TUI completa
ares agente AgenteDeCambio run

# Verificar estado
ares agente AgenteDeCambio status

# Test de componentes
ares agente AgenteDeCambio test
```

### Opción 2: Directo desde Python

```bash
cd /home/daniel/tron/programas/TR
source .venv/bin/activate

# Ejecutar app
python -m modules.ui.agente_de_cambio run

# Demo
python -m modules.ui.agente_de_cambio demo

# Test
python -m modules.ui.agente_de_cambio test
```

---

## ⚙️ Configuración

### 1. Configurar API Key de DeepSeek

```bash
# Copiar archivo de ejemplo
cp AGENTES/sub-agentes/AgenteDeCambio/.env.example .env

# Editar con tu API Key
nano .env

# O exportar directamente
export DEEPSEEK_API_KEY="sk-tu-api-key-aqui"
```

### 2. Obtener API Key

1. Visitar: https://platform.deepseek.com/api_keys
2. Crear cuenta / Login
3. Generar nueva API Key
4. Copiar y pegar en `.env`

---

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| `Enter` | Enviar mensaje |
| `Ctrl+Q` | Salir |
| `Ctrl+S` | Guardar sesión |
| `F1` | Mostrar ayuda |
| `↑` `↓` | Scroll en chat |

---

## 💬 Flujo de Chat

1. **Escribe tu mensaje** en el input inferior
2. **Presiona Enter** o click en "Enviar"
3. **Espera la respuesta** streaming carácter por carácter
4. **Delta calcula automáticamente** (muestra en header)
5. **Sesión se guarda** automáticamente en SQLite

---

## 📊 Métricas

### Delta de Deriva (Δ)

| Valor | Color | Significado |
|-------|-------|-------------|
| < 30% | 🟢 Verde | Cambio menor, OK |
| 30-70% | 🟡 Amarillo | Cambio moderado, revisar |
| > 70% | 🔴 Rojo | Cambio drástico, requiere aprobación |

---

## 🗄️ Base de Datos

Las sesiones se guardan en:
```
~/.tron/agente_de_cambio/sessions.db
```

### Estructura de Sesión

```json
{
  "id": "sess_1234567890_abc",
  "system_prompt": "Eres un sistema de EXTRACCIÓN COGNITIVA...",
  "messages": [
    {"role": "user", "content": "Hola"},
    {"role": "assistant", "content": "Hola, ¿en qué puedo ayudarte?"}
  ],
  "objectives": [],
  "created_at": "2026-03-16T...",
  "updated_at": "2026-03-16T..."
}
```

---

## 🐛 Troubleshooting

### Error: DEEPSEEK_API_KEY no configurada

**Solución:**
```bash
export DEEPSEEK_API_KEY="sk-tu-api-key-aqui"
# O editar archivo .env
```

### Error: No module named 'textual'

**Solución:**
```bash
cd /home/daniel/tron/programas/TR
source .venv/bin/activate
# O reinstalar: uv sync
```

### Error: Database is locked

**Solución:**
```bash
# Cerrar otras instancias
# O eliminar DB corrupta
rm ~/.tron/agente_de_cambio/sessions.db
```

---

## 📝 Ejemplo de Sesión

```
┌─────────────────────────────────────────────────────────┐
│ Header                                                  │
│ 🤖 AgenteDeCambio             Sesión: 12345678 | Δ: 0% │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ╭───────────────────────────────────────────────────╮  │
│ │ [User] ¿Qué es TypeScript?                        │  │
│ ╰───────────────────────────────────────────────────╯  │
│ ╭───────────────────────────────────────────────────╮  │
│ │ [Bot] TypeScript es un lenguaje de programación...│  │
│ ╰───────────────────────────────────────────────────╯  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [Escribe tu mensaje...                    ] [Enviar]   │
├─────────────────────────────────────────────────────────┤
│ Footer                                                  │
│ q:Salir  ^S:Guardar  F1:Ayuda  Enter:Enviar            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Próximas Características (Pendientes)

- [ ] Modo cuestionario (OptionList)
- [ ] Editor de prompt en tiempo real
- [ ] Confirmación de cambios (delta > threshold)
- [ ] Sparkline de historial delta
- [ ] Exportar sesión a JSON/Markdown

---

*Documento creado: 16-03-2026*  
*Versión: 1.0 (Chat funcional con streaming)*

# 📘 LEEME.md - Agente de Cambio Estable

> **Resumen Ejecutivo de 1 Página**  
> **Última actualización:** 2026-03-19  
> **Versión:** 0.1.0

---

## ¿QUÉ ES ESTO?

**Agente de Cambio Estable** es un **sistema de conducción cognitiva** que ayuda a usuarios a lograr objetivos mediante:

1. **Conversación estructurada** - Preguntas dinámicas (botones + comentario libre)
2. **Memoria de objetivos** - Guarda metas EMT (Evidencia-Métrica-Tiempo)
3. **Control de deriva** - Evita que la IA se desvíe del objetivo
4. **Detección de estancamiento** - 12 señales + 3 terapias de intervención

**NO es un chatbot.** Es un motor de ejecución con interfaz conversacional.

---

## 🚀 INICIO RÁPIDO (3 PASOS)

```bash
# 1. Ir al directorio
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable

# 2. Instalar dependencias
npm install --legacy-peer-deps

# 3. Configurar API Key y ejecutar
cp apps/server/.env.example apps/server/.env
# Editar apps/server/.env con DEEPSEEK_API_KEY
npm run dev
```

**Acceder:** http://localhost:3000

---

## 📚 DOCUMENTACIÓN CLAVE (ORDEN DE LECTURA)

| # | Documento | Ruta | Tiempo |
|---|-----------|------|--------|
| 1 | **PLAN DE CONSTRUCCIÓN** | [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md) | 10 min |
| 2 | **ÍNDICE MAESTRO PARA IAs** | [`../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md) | 15 min |
| 3 | **27 Requerimientos** | [`/docs/CLAVE/ListaRequerimientos.md`](./docs/CLAVE/ListaRequerimientos.md) | 20 min |
| 4 | **Estado Actual** | [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md) | 5 min |

---

## 🎯 HITOS (PLAN COMPLETO EN PLAN-CONSTRUCCION.md)

| Hito | Nombre | Estado | Criterio |
|------|--------|--------|----------|
| **1** | Motor Cuestionarios + Quiz | ❌ | Genera preguntas dinámicas |
| **2** | Objetivos + Estancamiento | ❌ | Guarda EMT, detecta 12 señales |
| **3** | Arquitecto + Control Deriva | ❌ | Doble instancia, veto cambios |
| **4** | Perfil Biológico | ❌ | Adapta al cronotipo |
| **5** | Integración TR-ARES | ❌ | Standalone + ARES |
| **6** | Documentación Unificada | ⚠️ | README actualizado |

---

## 🔧 COMANDOS ESENCIALES

```bash
# Desarrollo
npm run dev              # Ambos servidores
npm run dev:server       # Solo backend (puerto 3001)
npm run dev:web          # Solo frontend (puerto 3000)

# Tests
npm test                 # Todos los módulos
npm run lint             # Linting

# Git Backups (OBLIGATORIO)
git tag "backup-$(date '+%Y%m%d-%H%M%S')"   # Antes de cambiar
git diff --stat                             # Después de cambiar
```

---

## 📦 ESTRUCTURA (LO QUE IMPORTA)

```
Agente-De-Cambio-Estable/
├── apps/
│   ├── web/           # Frontend Next.js
│   └── server/        # Backend Node.js + Socket.IO
├── modules/           # Módulos (metodología modular)
│   ├── deepseek-connector/    # ✅ DeepSeek API
│   ├── session-manager/       # ✅ Sesiones
│   ├── prompt-engine/         # ✅ Prompts dinámicos
│   ├── delta-calculator/      # ✅ Deriva semántica
│   └── [más módulos en desarrollo]
├── docs/CLAVE/        # Documentación fundamental
│   ├── PLAN-CONSTRUCCION.md   # ← LEER PRIMERO
│   ├── ListaRequerimientos.md
│   ├── proyecto.md
│   ├── estado.md
│   └── ...
└── README.md          # Este archivo (versión extendida)
```

---

## ⚠️ PROTOCOLOS OBLIGATORIOS

### Antes de Modificar Código

1. **Leer INDICE-MAESTRO-PARA-IAS.md** - Entender arquitectura
2. **Crear backup git** - `git tag "backup-$(date '+%Y%m%d-%H%M%S')"`
3. **Verificar checklist pre-commit** - 10 puntos en README.md

### Después de Modificar

1. **Git diff** - `git diff --stat` para validar cambios
2. **Tests passing** - `npm test`
3. **Actualizar INDEX.md** - Cada módulo con su índice <50 líneas
4. **Actualizar registry.json** - Si agregó módulo nuevo

---

## 🔗 ENLACES RÁPIDOS

| Tipo | Enlace |
|------|--------|
| **Plan Completo** | [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md) |
| **Índice para IAs** | [`INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md) |
| **Estado Actual** | [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md) |
| **Registry Módulos** | [`/modules/registry.json`](./modules/registry.json) |
| **Memoria TR-ARES** | [`~/.qwen/QWEN.md`](file:///home/daniel/.qwen/QWEN.md) |

---

## 🧠 FILOSOFÍA (NO NEGOCIABLE)

| Principio | Aplicación |
|-----------|------------|
| **Google Lens** | Herramienta desaparece, queda resultado |
| **Pragmatismo radical** | Navaja suiza, no catedral |
| **No sobra ni falta nada** | Utilidad/esfuerzo > elegancia |
| **Conducción, no chat** | Conversación → Decisión → Acción |

---

## 📊 ESTADO ACTUAL (RESUMEN)

| Métrica | Valor |
|---------|-------|
| Módulos completados | 5/12 |
| Funciona standalone | ✅ |
| Funciona con ARES | ❌ (Hito 5) |
| Documentación actualizada | ⚠️ (En progreso) |

**Ver estado completo:** [`/docs/CLAVE/estado.md`](./docs/CLAVE/estado.md)

---

## 🎯 PRÓXIMO PASO INMEDIATO

**COMENZAR HITO 1:**

```bash
# 1. Crear backup inicial
git add .
git commit -m "BACKUP $(date '+%Y-%m-%d_%H-%M-%S') - Pre-Hito1"
git tag "backup-$(date '+%Y%m%d-%H%M%S')"

# 2. Crear rama del hito
git checkout -b hito-1-questionnaire

# 3. Crear estructura de carpetas
mkdir -p modules/questionnaire-engine/test
mkdir -p modules/quiz-engine/templates
mkdir -p modules/question-types/test

# 4. Seguir PLAN-CONSTRUCCION.md → Hito 1
```

---

**¿Primera vez aquí?** → Leer [`PLAN-CONSTRUCCION.md`](./docs/CLAVE/PLAN-CONSTRUCCION.md) completo antes de tocar código.

**¿Ya conoces el sistema?** → Ir directamente al [`ÍNDICE MAESTRO PARA IAS`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md) para referencia técnica.

---

*Fin de LEEME.md - Resumen de 1 página*

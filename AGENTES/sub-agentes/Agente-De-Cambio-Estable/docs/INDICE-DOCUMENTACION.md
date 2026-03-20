# 📚 ÍNDICE DE DOCUMENTACIÓN - Agente de Cambio Estable

> **Propósito:** Lista central de todos los documentos de ayuda del proyecto  
> **Última actualización:** 2026-03-20 19:00  
> **Total de documentos:** 20+

---

## 📖 DOCUMENTOS CLAVE (LEER PRIMERO)

| # | Documento | Ruta | Tiempo | Prioridad |
|---|-----------|------|--------|-----------|
| 1 | **LEEME.md** | [`/LEEME.md`](/LEEME.md) | 5 min | 🔴 CRÍTICA |
| 2 | **TODO-001-MAESTRO** | [`/docs/CLAVE/TODO-001-MAESTRO.md`](./CLAVE/TODO-001-MAESTRO-20260320-1900.md) | 10 min | 🔴 CRÍTICA |
| 3 | **Índice Maestro TR-ARES** | [`../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md`](../../../TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md) | 15 min | 🔴 CRÍTICA |
| 4 | **Plan de Construcción** | [`/docs/CLAVE/PLAN-CONSTRUCCION.md`](./CLAVE/PLAN-CONSTRUCCION.md) | 10 min | 🟡 ALTA |
| 5 | **Estado Actual** | [`/docs/CLAVE/estado.md`](./CLAVE/estado.md) | 5 min | 🟡 ALTA |

---

## 📋 HITOS COMPLETADOS

| Hito | Documento | Ruta | Estado |
|------|-----------|------|--------|
| **1** | Motor Cuestionarios + Quiz | [`/docs/CLAVE/HITO-1-COMPLETADO.md`](./CLAVE/HITO-1-COMPLETADO.md) | ✅ completado |
| **2** | Integración Chat-Cuestionarios | [`/docs/CLAVE/HITO-2-EN-PROGRESO.md`](./CLAVE/HITO-2-EN-PROGRESO.md) | ✅ completado |

---

## 📝 DOCUMENTACIÓN DE PROCESOS

| Documento | Ruta | Propósito |
|-----------|------|-----------|
| **Metodología Modular** | [`/docs/CLAVE/METODOLOGIA-MODULAR.md`](./CLAVE/METODOLOGIA-MODULAR.md) | Reglas para crear módulos |
| **Comandos Rápidos** | [`/docs/CLAVE/COMANDOS-RAPIDOS.md`](./CLAVE/COMANDOS-RAPIDOS.md) | Cheatsheet de comandos |
| **Bitácora de Cambios** | [`/docs/CLAVE/BITACORA.md`](./CLAVE/BITACORA.md) | Historial cronológico |
| **Lista de Requerimientos** | [`/docs/CLAVE/ListaRequerimientos.md`](./CLAVE/ListaRequerimientos.md) | 27 requerimientos del sistema |

---

## 🗺️ DIAGRAMAS Y FLUJOS

| Diagrama | Ruta | Descripción |
|----------|------|-------------|
| **01 - Maestro del Sistema** | [`../../../TR/docs/AgenteDeCambio/FLUJOS-MERMAID/01-diagrama-maestro-sistema.md`](../../../TR/docs/AgenteDeCambio/FLUJOS-MERMAID/01-diagrama-maestro-sistema.md) | 6 capas del sistema |
| **02 - Inferencia Tipo Pregunta** | [`../../../TR/docs/AgenteDeCambio/FLUJOS-MERMAID/02-inferencia-tipo-pregunta.md`](../../../TR/docs/AgenteDeCambio/FLUJOS-MERMAID/02-inferencia-tipo-pregunta.md) | 8 tipos de preguntas |
| **03 - Modelo de Datos ERD** | [`../../../TR/docs/AgenteDeCambio/FLUJOS-MERMAID/03-modelo-datos-ERD.md`](../../../TR/docs/AgenteDeCambio/FLUJOS-MERMAID/03-modelo-datos-ERD.md) | 13 entidades BD |

---

## 🧠 DOCUMENTOS DE ARQUITECTURA

| Documento | Ruta | Propósito |
|-----------|------|-----------|
| **Proyecto.md** | [`/docs/CLAVE/proyecto.md`](./CLAVE/proyecto.md) | Visión general del proyecto |
| **Maestro.md** | [`/docs/CLAVE/Maestro.md`](./CLAVE/Maestro.md) | Documento maestro de arquitectura |
| **Sistema por Kimi** | [`/docs/CLAVE/sistema-por-kimi.md`](./CLAVE/sistema-por-kimi.md) | Análisis de sistema |

---

## 🔧 DOCUMENTACIÓN TÉCNICA

### Backend

| Documento | Ruta | Propósito |
|-----------|------|-----------|
| **Socket.IO Server** | `/apps/server/README.md` | Configuración del servidor |
| **DeepSeek Connector** | [`/modules/deepseek-connector/INDEX.md`](./modules/deepseek-connector/INDEX.md) | Uso de la API |
| **Prompt Engine** | [`/modules/prompt-engine/INDEX.md`](./modules/prompt-engine/INDEX.md) | Construcción de prompts |

### Frontend

| Documento | Ruta | Propósito |
|-----------|------|-----------|
| **QuestionContainer** | [`/apps/web/components/chat/README-CAPACIDADES.md`](./apps/web/components/chat/README-CAPACIDADES.md) | Sistema de capacidades |
| **ChatContainer** | `/apps/web/components/chat/ChatContainer.tsx` | Contenedor principal |
| **SocketProvider** | `/apps/web/components/providers/SocketProvider.tsx` | Conexión Socket.IO |

---

## 🧪 TESTING Y DEPLOY

| Documento | Ruta | Propósito |
|-----------|------|-----------|
| **Comandos de Deploy** | [`/docs/CLAVE/COMANDOS-RAPIDOS.md`](./CLAVE/COMANDOS-RAPIDOS.md) | Deploy y producción |
| **Git Backup** | [`/docs/CLAVE/COMANDOS-RAPIDOS.md`](./CLAVE/COMANDOS-RAPIDOS.md#git-backups) | Tags de respaldo |

---

## 📊 ESTADÍSTICAS

| Métrica | Valor |
|---------|-------|
| **Total documentos** | 20+ |
| **Documentos CLAVE** | 10 |
| **Diagramas** | 3 |
| **Índices** | 2 (este + módulos) |

---

## 🔗 ENLACES RÁPIDOS

- **Índice de Módulos:** [`/docs/INDICE-MODULOS.md`](./INDICE-MODULOS.md)
- **Registry JSON:** [`/modules/registry.json`](./modules/registry.json)
- **LEEME.md:** [`/LEEME.md`](/LEEME.md)

---

## 📝 FLUJO DE LECTURA RECOMENDADO

### Para Nueva IA

```
1. INDICE-MAESTRO-PARA-IAS.md (arquitectura TR-ARES)
   ↓
2. LEEME.md (este proyecto)
   ↓
3. TODO-001-MAESTRO.md (problemas pendientes)
   ↓
4. estado.md (qué está en desarrollo)
   ↓
5. INDICE-MODULOS.md o INDICE-DOCUMENTACION.md (según tarea)
```

### Para Modificar Código

```
1. LEEME.md (procedimientos)
   ↓
2. INDICE-MODULOS.md (buscar módulo)
   ↓
3. módulo/INDEX.md (documentación del módulo)
   ↓
4. módulo/actions.ts (código)
```

### Para Resolver Problemas

```
1. TODO-001-MAESTRO.md (problemas conocidos)
   ↓
2. BITACORA.md (intentos anteriores)
   ↓
3. estado.md (qué módulos están en desarrollo)
```

---

*Índice generado: 2026-03-20 19:00*  
*Próxima actualización: Cuando se agregue/modifique documento*

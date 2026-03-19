# 🚀 COMANDOS RÁPIDOS - AGENTE DE CAMBIO

> **Guía de referencia rápida con rutas absolutas**  
> **Última actualización:** 2026-03-19  
> **Hito:** 1 completado

---

## 📍 RUTAS ABSOLUTAS IMPORTANTES

| Concepto | Ruta Absoluta |
|----------|---------------|
| **Proyecto** | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable` |
| **Documentación CLAVE** | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/docs/CLAVE/` |
| **Módulos** | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/modules/` |
| **Ejecutables** | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/bin/` |
| **Herramientas** | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/` |
| **Índice Maestro IAs** | `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md` |
| **Diagramas Mermaid** | `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/FLUJOS-MERMAID/` |

---

## ⚡ COMANDOS DE USO DIARIO

### 1. Iniciar Servidores (Desarrollo)

```bash
# Opción A: Wrapper bash (más fácil)
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh start

# Opción B: npm directo
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
npm run dev

# Acceder:
# Frontend: http://localhost:3000
# Backend:  http://localhost:3001
```

### 2. Solo Backend

```bash
# Wrapper
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh server

# npm
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
npm run dev:server
```

### 3. Solo Frontend

```bash
# Wrapper
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh web

# npm
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
npm run dev:web
```

### 4. Ejecutar CLI Standalone

```bash
# Demostración
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/bin/agente-de-cambio.js --demo

# Con objetivo
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/bin/agente-de-cambio.js -o "Quiero lanzar mi producto" -d emprendedor

# Ayuda CLI
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/bin/agente-de-cambio.js --help
```

### 5. Ver Estado del Proyecto

```bash
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh status
```

### 6. Ver Documentación

```bash
# Lista de documentos CLAVE
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh docs

# Leer documentos específicos
cat /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/docs/CLAVE/PLAN-CONSTRUCCION.md
cat /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/LEEME.md
cat /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/README.md
```

### 7. Instalar Dependencias

```bash
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh install
```

---

## 🔧 COMANDOS DE GIT (BACKUP)

```bash
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable

# Antes de modificar
git add .
git commit -m "BACKUP $(date '+%Y-%m-%d_%H-%M-%S') - Pre-[cambio]"
git tag "backup-$(date '+%Y%m%d-%H%M%S')"

# Después de modificar
git diff --stat
git log -1 --oneline

# Ver tags de hitos
git tag -l "hito*"
git tag -l "backup*"
```

---

## 📊 ESTADO DE MÓDULOS (HITO 1)

```bash
# Ver módulos completados
ls -la /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/modules/

# Ver registry actualizado
cat /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/modules/registry.json | grep -A2 '"name"'
```

**Módulos Hito 1:**
- ✅ `questionnaire-engine` - Motor de preguntas dinámicas
- ✅ `quiz-engine` - Banco de cuestionarios por dominio
- ✅ `question-types` - Validadores para 8 tipos de preguntas

---

## 🎯 INVOCAR DESDE ARES

```bash
# ARES invoca Agente de Cambio como herramienta
ares agente-de-cambio --prompt "Ayuda a este usuario con su objetivo EMT"

# Con contexto adicional
ares agente-de-cambio --prompt "Usuario quiere lanzar producto en 3 meses" --domain emprendedor
```

---

## 📁 ARCHIVOS DE CONFIGURACIÓN

| Archivo | Ruta Absoluta | Propósito |
|---------|---------------|-----------|
| `.env` (backend) | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/apps/server/.env` | DEEPSEEK_API_KEY, PORT |
| `.env.local` (frontend) | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/apps/web/.env.local` | Socket URL, API URL |
| `package.json` | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/package.json` | Scripts, dependencias |
| `registry.json` | `/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/modules/registry.json` | Registro de módulos |

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Cannot find module"

```bash
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
rm -rf node_modules apps/*/node_modules
npm install --legacy-peer-deps
```

### Error: "DEEPSEEK_API_KEY not found"

```bash
# Editar .env
nano /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/apps/server/.env

# Agregar:
DEEPSEEK_API_KEY=sk-tu-api-key-aqui
```

### Error: Puerto ya en uso

```bash
# Matar procesos en puertos 3000/3001
lsof -ti:3000 | xargs kill -9
lsof -ti:3001 | xargs kill -9
```

---

## 📞 COMANDOS MÁS USADOS (CHEATSHEET)

```bash
# 1. Iniciar todo
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh start

# 2. Ver estado
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/herramientas/agente-de-cambio.sh status

# 3. Demo CLI
/home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/bin/agente-de-cambio.js --demo

# 4. Ver documentación
cat /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/LEEME.md

# 5. Git backup
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable && git add . && git commit -m "BACKUP $(date '+%Y-%m-%d')" && git tag "backup-$(date '+%Y%m%d')"
```

---

## 🎯 PRÓXIMO HITO (HITO 2)

**Módulos a implementar:**
- `objectives-manager` - Memoria permanente EMT
- `stall-detector` - 12 señales de estancamiento
- `stall-intervention` - 3 terapias simultáneas

**Comando para comenzar:**
```bash
cd /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
git checkout -b hito-2-objectives
```

---

**Documento creado:** 2026-03-19  
**Hito 1:** Completado ✅  
**Próxima revisión:** Después de Hito 2

---

*Fin de Comandos Rápidos*

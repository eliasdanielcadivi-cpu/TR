# 🛰 ARES - Terminal Remote Operations Nexus

**ARES** es un orquestador táctico diseñado para transformar el trabajo de las personas, usando modulos como el de la terminal Kitty en una estación de trabajo de alta productividad aumentada por Agentes Lógicos, Semántico-Cognitivos de IA, Actúa como  cerebro para el control de ventanas, sesiones inteligentes y flujos de trabajo de programación, marketing, investigación, CRM, eComerce, eLearnig, entre otros es un  Full Stack Presence Management Capital  para los clientes y usuarios finales. Ares es un producto-servicio de alto rendimiento,  constructor de infraestructura que genera valor y capital para la empresa, industria, artesanos, vendesores, distribuidores, médicos en todos los ambitos de influencia de la IA.

---

## 🚀 RESUMEN EJECUTIVO

### ¿Qué es ARES?
ARES es el **cerebro** que controla la terminal Kitty para crear flujos de trabajo de vanguardia. Es la evolución modular y  del proyecto TRON original.

### Comandos Maestros

| Comando | Descripción |
|---------|-------------|
| `ares` | Abre ARES Hub en **~** con título "Ares por Daniel Hung" |
| `ares p "pregunta"` | Consulta a la IA ARES (Gemma 3 / DeepSeek) |
| `ares p "pregunta" --model gemma` | Usar modelo Gemma específico |
| `ares p "pregunta" --template code` | Usar plantilla YAML para código |
| `ares plan` | Despliegue táctico: 4 pestañas coloreadas Hacker Neon |
| `ares zshPlan` | Hacker AI Session (ZSH) |
| `ares status` | Diagnóstico del socket Kitty y estado del sistema |
| `ares config` | Ver configuración de IA |
| `ares models` | Listar modelos disponibles |
| `ares templates` | Listar plantillas YAML |
| `ares tools` | Listar herramientas (function calling) |
| `ares video <archivo>` | Reproduce video en terminal (mpv + protocolo gráfico) |
| `ares image <archivo>` | Muestra imagen en terminal |
| `ares help` | Abre documentación navegable con Broot |

### Herramientas Especializadas

| Herramienta | Propósito |
|-------------|-----------|
| `tr-color <ruta>` | Aplica color Hacker Neon a pestaña Kitty según tipo de archivo |
| `tr-investigador buscar <query>` | Búsqueda en Google con resultados estructurados |
| `tr-investigador otear <URLs>` | Exploración profunda de páginas web |
| `tr-investigador docs [tema]` | Consulta documentación interna |
| `tr-kitty-init` | Inicialización y configuración de terminal Kitty |

---

## 🏛 FILOSOFÍA DE MODULARIDAD ATÓMICA

### ⚡ Regla de Oro: Máximo 3 Funciones por Módulo
Cada componente de ARES debe ser quirúrgico. Esto permite:
- ✅ **Determinismo**: Resultados predecibles en cada comando.
- ✅ **Encapsulamiento**: Funcionamiento autónomo sin dependencias globales.
- ✅ **Vibe Coding**: Desarrollo acelerado sin pérdida de contexto.

## 🛠️ Herramientas de Ecosistema (Soberanía TRON)

ARES no actúa solo; se integra con herramientas globales diseñadas para la precisión quirúrgica y la soberanía del entorno:

- **`ini` (v2.0):** Orquestador de ciclo de vida.
    - `ini venv`: Inicialización profesional de entornos (uv/npm).
    - `ini prod`: Publicación en `/usr/bin` con **Soberanía del CWD** (ARES respeta tu ubicación actual en la terminal).
- **`repo` (v5.0):** Auditor táctico de Git.
    - `repo status`: Auditoría rápida de cambios para humanos e IA.
    - `repo audit <modulo>`: Verifica que los cambios realizados por una IA estén contenidos dentro del alcance del módulo correspondiente.

## 🧩 Arquitectura Orquestador-Módulo

1. **Orquestador (`src/main.py`):** Director de orquesta. Delegación pura de comandos a especialistas.
2. **Módulos (`modules/`):** Especialistas atómicos (máx. 3 funciones por módulo).
3. **Agentes (`Agentes/`):** Módulos inteligentes con salida JSON estructurada para integración con LLMs.

---

### 🧩 Organización por Naturaleza
Los módulos están agrupados jerárárquicamente en `modules/`:
- **admon/**: Salud y configuración del sistema.
- **ia/**: Inteligencia y búsqueda avanzada (multi-provider).
- **color/**: Identidad visual dinámica para pestañas Kitty.
- **multimedia/**: Puppeteering de video, imagen y audio.
- **tactico/**: Despliegue de flujos de trabajo complejos.
- **ui/**: Estética neón y manuales dinámicos.
- **whatsapp/**: Integración con WhatsApp.
- **investigador/**: Exploración web e inteligencia (búsqueda, oteo).

### 🕵️ Sub-Agentes (AGENTES/)
- **sherlok/**: Auditor de código con "ADN Técnico Industrial" usando LLM local.
  - Modelos: codellama:7b, qwen2.5-coder:7b-instruct, deepseek-r1:8b
  - Componentes: brain.py (análisis), scanner.py (exploración), persistence.py (SQLite)
  - Ubicación: `AGENTES/sub-agentes/sherlok/`

---

## 🤖 SISTEMA DE IA MULTI-PROVIDER

### Providers Disponibles

| Provider | Modelos | Tipo |
|----------|---------|------|
| **Gemma** | gemma3:1b, gemma3:4b, gemma3:12b, gemma3:27b | Local (Ollama) |
| **DeepSeek** | deepseek-chat, deepseek-coder | API Cloud |
| **OpenRouter** | Múltiples modelos | API Cloud (placeholder) |

###Aliases de Modelos

```bash
ares p "pregunta" --model gemma      # gemma3:4b (default)
ares p "pregunta" --model gemma12b   # gemma3:12b
ares p "pregunta" --model deepseek   # deepseek-chat
```

### Plantillas YAML

```bash
ares p "prompt" --template default   # Consultas generales
ares p "prompt" --template chat      # Conversaciones
ares p "prompt" --template code      # Programación
ares p "prompt" --template tools     # Function calling
```

### Function Calling (Herramientas)

ARES soporta herramientas para acciones del mundo real:

| Herramienta | Descripción |
|-------------|-------------|
| `google_search` | Búsqueda en tiempo real |
| `translate_text` | Traducción de texto |
| `get_weather` | Clima actual |
| `execute_shell` | Ejecutar comando shell |
| `read_file` | Leer archivo |
| `write_file` | Escribir archivo |

---

## 🎬 PUPPETEERING MULTIMEDIA
ARES permite la manipulación de medios visuales directamente en el espacio de trabajo:
- `ares video demo.mp4`: Reproducción fluida incrustada vía `mpv`.
- `ares image schema.png`: Visualización de alta resolución en la celda actual.

---

## 📁 BROOT - Navegación Encapsulada

**Broot** está integrado en TRON como módulo atómico de navegación jerárquica.

### Estructura

| Componente | Ubicación |
|------------|-----------|
| Binario | `bin/broot-core/broot-bin` |
| Wrapper | `bin/broot` |
| Launcher `br` | `bin/broot-core/br` |
| Configuración | `config/broot/` |

### Uso

```bash
# Navegación con función shell (recomendado)
source ~/tron/programas/TR/bin/broot-core/br
br          # Navegar con capacidad de cd
br /ruta    # Navegar desde ruta específica

# Ejecución directa
broot       # Navegador jerárquico
broot --help
```

### Configuración Personalizada

- `conf.hjson`: Configuración principal (flags, skins, verbos)
- `verbs.hjson`: Comandos personalizados
- `*-skin.hjson`: Temas de color (gruvbox, solarized, etc.)

### Integración con ARES

`ares help` abre la documentación usando **broot** como navegador.

---

## 📐 ARQUITECTURA DE DATOS VIVA
Los dashboards de ARES (en desarrollo) utilizan transiciones tipo **morphing** para mostrar indicadores industriales, KPIs petroleros y tendencias sociales en tiempo real, sintiéndose como un organismo vivo.

---

## 📚 DOCUMENTACIÓN

| Archivo | Contenido |
|---------|-----------|
| `docs/HELP.md` | Ayuda general y referencia de comandos |
| `docs/GEMMA_OLLAMA_GUIDE.md` | Guía completa de Gemma + Ollama |
| `docs/DEEPSEEK_GUIDE.md` | Guía de DeepSeek API |
| `docs/Ollama-API.md` | Referencia de API de Ollama |
| `docs/sacar-jugo-gemma.md` | Recopilación de técnicas para Gemma |
| `docs/Ares-Terminal/` | Configuración de terminal predeterminada |
| `docs/Ares-Terminal/CONFIGURACION_TERMINAL_PREDETERMINADA.md` | Guía forense completa de ARES como terminal |
| `docs/Ares-Terminal/REFERENCIA_RAPIDA.md` | Comandos y atajos rápidos |

---

## 🔧 INSTALACIÓN

### 1. Clonar o ubicar en directorio de programas

```bash
cd ~/tron/programas/TR
```

### 2. Activar entorno virtual

```bash
source .venv/bin/activate
```

### 3. Probar instalación

```bash
ares --help
ares status
ares gS [nombre]   # Guardar sesión actual de Kitty
```

### 4. (Opcional) Añadir al PATH

```bash
# Añadir a ~/.bashrc o ~/.zshrc
export PATH="$HOME/tron/programas/TR/bin:$PATH"
```

---

## 🛡️ SOBERANÍA Y SEGURIDAD

- ✅ **Modelos locales**: Gemma vía Ollama (sin nube)
- ✅ **Datos sensibles**: Se mantienen en tu equipo
- ✅ **Cifrado**: Configuración y credenciales protegidas
- ✅ **Sin dependencias externas**: Funciona offline

---


## Módulo: MPV System Injector

**Ubicación:** `tron/programas/TR/scripts/MPV/inyectar_mpv.py`

Este componente gestiona la configuración global de `mpv` mediante la inyección directa de archivos de configuración y lógica en el sistema operativo. Su objetivo es unificar la experiencia de usuario y añadir herramientas de edición de subtítulos en tiempo real.

### Componentes Inyectados

El script automatiza el despliegue en la ruta raíz `/etc/mpv/`, garantizando que las mejoras estén disponibles para todos los usuarios:

* **`input.conf` (Mapping Estilo VLC):**
* **Navegación:** Flechas direccionales para control de volumen (Arriba/Abajo) y búsqueda (Izquierda/Derecha).
* **Reproducción:** Teclas `+`/`-` para velocidad, `a` para audio, `s` para subtítulos.
* **Precisión:** `,` y `.` para retroceso/avance cuadro a cuadro; `[` y `]` para ciclos de bucle A-B.


* **`fix_subdelay.lua` (Script de Sincronización):**
* Herramienta avanzada que permite corregir desfases de subtítulos mediante la captura de dos puntos de referencia (audio vs. texto) usando la combinación `Alt+Z`.



### Ejecución y Despliegue

Para aplicar la configuración y sincronizar los archivos de la carpeta `TR` hacia el sistema, ejecuta:

```bash
sudo python3 /home/daniel/tron/programas/TR/scripts/MPV/inyectar_mpv.py

```



*Ares: El orquestador definitivo por Daniel Hung.*

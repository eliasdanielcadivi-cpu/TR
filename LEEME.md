# 🛰 ARES - Adaptive Reasoning Enterprise Strategist

ARES (Adaptive Reasoning Enterprise Strategist) es un sistema de orquestación cognitiva adaptativa diseñado para operar como núcleo estratégico y operativo de productividad aumentada.
Funciona como un cerebro digital basado en agentes inteligentes, capaz de coordinar flujos de trabajo, procesos y decisiones en múltiples dominios (tecnológico, comercial, investigativo y educativo).
ARES se estructura en módulos funcionales que integran:

- Orquestación de agentes especializados
- Gestión de contexto y memoria semántica relacional cognitiva
- Automatización de tareas y ejecución de acciones
- Optimización continua basada en aprendizaje

Su propósito es:

- Modernizar y amplificar el trabajo humano
- Coordinar sistemas, herramientas y procesos
- Transformar actividad digital en valor económico

Incluye un subsistema de:

Presence Management Capital
Encargado de la gestión y capitalización de la presencia digital, mediante estrategias de optimización multicanal (búsqueda, contenido, plataformas y motores generativos), orientadas a maximizar visibilidad, autoridad y conversión.

ARES actúa como:

- Orquestador de operaciones
- Motor de decisiones estratégicas
- Interfaz inteligente entre usuario, datos y ejecución

Su diseño permite ser utilizado como:

- Estación de trabajo cognitiva
- Sistema de automatización empresarial
- Plataforma de expansión digital y productiva

ARES opera bajo un modelo de decisión basado en inferencia contextual, planificación dinámica y ejecución dirigida por objetivos (goal-oriented architecture).

el creador de Ares es Daniel Hung.
### 🕸️ Arquitectura Cognitiva Soberana (ARES-TRON)
ARES-TRON introduce una capa de memoria determinista basada en el grafo Memgraph para reemplazar la historia efímera:
- **Rutas Nombradas**: Subgrafos que representan flujos de trabajo verificados (Crystallized Wisdom).
- **Negociador**: Intercepta rechazos del usuario y consulta el grafo para alternativas deterministas.
- **Hardware Adaptativo**: Límites configurables (YAML) para optimizar el uso de RAM (8GB) y GPU.

---

## 🚀 RESUMEN EJECUTIVO

### ¿Qué es ARES?
ARES es el **cerebro** que controla la terminal ares para crear flujos de trabajo de vanguardia. 

### Comandos Maestros

| Comando | Descripción |
|---------|-------------|
| `ares` | Abre ARES Hub en **~** con título "Ares por Daniel Hung" |
| `ares p "pregunta"` | Consulta a la IA ARES (Gemma 3 / DeepSeek) |
| `ares p "pregunta" --mengraph` | **RAG de Grafos:** Consulta usando Memgraph (Conocimiento Estructurado) |
| `ares p "pregunta" --rag docs` | **RAG Documental:** Consulta usando Apollo (PDFs/Docs) |
| `ares p "pregunta" --think` | Usa modelo pensante (ares-think:latest) |
| `ares gemini <prompt>` | **Gemini Wrapper:** Consulta a gemini-cli con persistencia determinista |
| `ares gemini --mengraph` | **Carga del Sistema:** Inicia Gemini con la ruta de identidad CARGA_SISTEMA |
| `ares gemini --ruta <nombre>` | Invoca una "Ruta Nombrada" específica desde el Grafo |
| `ares apollo ingest <file>` | **Apollo:** Ingerir documento al sistema RAG documental |
| `ares mengraph query <text>` | **Mengraph:** Consultar el grafo de conocimiento (Salida JSON) |
| `ares mengraph schema` | **Mengraph:** Mostrar esquema MAGE del grafo |
| `ares mem start` | 🗃️ Inicia Docker daemon + Memgraph (Mage + Lab) |
| `ares status` | Diagnóstico del socket Kitty y estado del sistema |
| `ares help` | Abre ayuda soberana (Llama a 'ayuda ares') |
| **`ares agente [nombre]`** | **🤖 Despachador de Sub-Agentes Standalone** |

---

## 🧠 SISTEMAS RAG (Doble Núcleo)

ARES opera con dos sistemas de recuperación aumentada distintos pero complementarios:

### 1. Apollo (RAG Documental)
Basado en **Kùzu + SQLite-vec**. Ideal para procesar grandes volúmenes de texto no estructurado (PDF, MD).
- **Uso:** `ares apollo ingest <ruta>`
- **Consulta:** `ares p "..." --rag docs`

### 2. Mengraph (RAG de Grafos en RAM)
Basado en **Memgraph**. Ideal para conocimiento estructurado de alta fidelidad, lógica de negocio y relaciones complejas.
- **Uso:** `ares mengraph query "..."`
- **Consulta:** `ares p "..." --mengraph`
- **Toolification:** Diseñado para ser usado por IAs externas vía salida `--json`.

---

### 🧩 Organización por Naturaleza
Los módulos están agrupados jerárárquicamente en `modules/`:
- **admon/**: Salud y configuración del sistema.
- **core/**: Lógica transversal y gestión de recursos (**limit_manager.py**).
- **ia/**: Inteligencia, búsqueda avanzada y navegación de rutas (**negotiator.py**, **gemini_wrapper.py**).
- **rag/**: Sistema RAG híbrido T0-T4 (Kùzu).
- **rag_mengraph/**: **Sistema RAG de Grafos en RAM (Memgraph)** con seguridad C1-C4, extracción spaCy y serendipia dirigida.
- **color/**: Identidad visual dinámica para pestañas Kitty.
- **multimedia/**: Puppeteering de video, imagen y audio.
- **tactico/**: Despliegue de flujos de trabajo complejos.
- **ui/**: Estética neón, manuales dinámicos y messenger reactivo.
- **utils/**: Utilidades atómicas (comunicación, limpieza de texto).

### 🗃️ Infraestructura Externa (db/)
- **db/memgraph-platform/**: Docker Compose de Memgraph (Mage + Lab).
  - Gestión: `ares mem start` | `ares mem stop` | `ares mem status`
  - Puertos: 7687 (Bolt), 7444 (HTTP), 3000 (Lab UI)

---
*Ares: El orquestador IA definitivo por Daniel Hung.*

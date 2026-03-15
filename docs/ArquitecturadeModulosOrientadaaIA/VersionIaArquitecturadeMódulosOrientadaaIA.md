
# Arquitectura de Módulos Orientada a IA

## Diseño modular para sistemas compatibles con LLMs

### Propósito

El sistema de módulos está diseñado para mejorar la **comprensión del código por parte de modelos de inteligencia artificial con ventana de contexto limitada**, así como para facilitar la reutilización, mantenimiento y evolución del sistema.

Los módulos no deben entenderse únicamente como componentes técnicos del código, sino como **unidades funcionales reutilizables y operativas** dentro del ecosistema del proyecto.

---

# Naturaleza de un módulo

Un módulo puede cumplir simultáneamente tres funciones:

**A. Soporte de desarrollo**
Servir como ayuda para la construcción de otros programas.

**B. Herramienta CLI**
Actuar como herramienta o comando utilizable directamente por el usuario en la consola.

**C. Unidad reutilizable de código**
Ser código empaquetado intencionalmente para ser reutilizable en múltiples escenarios.

---

# Integración programática

Todo módulo debe poder integrarse programáticamente dentro de otros programas mediante importación directa.

Ejemplo conceptual:

```python
import modulo
```

También debe permitir la importación granular de sus elementos internos:

* clases
* funciones
* subfunciones
* entidades de agrupación de código

Esto permite que el módulo funcione tanto en **paradigmas tradicionales como en paradigmas mixtos de programación**.

---

# Uso como herramienta CLI

Todo módulo debe poder ejecutarse como herramienta CLI.

Para ello debe:

* aceptar **parámetros posicionales**
* ofrecer **ayuda interna**
* proporcionar **documentación accesible desde la consola**

Esto permite que el mismo módulo funcione tanto como **biblioteca de código** como **herramienta operativa para el usuario**.

---

# Importancia de los comentarios de código

Los comentarios dentro del código son críticos, especialmente cuando el sistema es utilizado o analizado por IA.

Los comentarios ayudan a:

* evitar la repetición de errores ya resueltos
* transmitir decisiones técnicas pasadas
* mejorar la interpretación del código por modelos de IA

Por esta razón, **es importante enfatizar en comentarios aquello que fue complejo o costoso de resolver**.

---

# Documentación especial de módulos complejos

Cuando un módulo:

* tiene gran importancia en el sistema
* ha requerido un esfuerzo considerable para su creación
* ha implicado resolver problemas difíciles

entonces debe contar con **documentación especial dentro de la carpeta `docs`**.

Esta documentación permite:

* modificar el módulo con mayor seguridad
* adaptarlo a nuevos contextos
* exportarlo a otros proyectos
* actualizarlo sin repetir errores del pasado
* evitar depender de documentación externa

---

# Índice de módulos

El índice de módulos tiene la responsabilidad de ofrecer un **mapa claro del sistema modular**.

Debe incluir:

* descripción del módulo
* función operativa
* casos de uso
* nivel de granularidad
* rutas dentro del proyecto
* referencia a documentación especial si existe

El índice debe ser:

* claro
* conciso
* preciso
* operativo
* descriptivo
* orientado a casos de uso

---

# Niveles de documentación de un módulo

Dependiendo de la complejidad del módulo, se requieren distintos niveles de documentación.

## Módulo simple

Requiere:

* índice de módulos
* lectura directa del módulo

Esto suele ser suficiente para comprender su funcionamiento.

---

## Módulo complejo o problemático

Si el módulo:

* ha dado problemas ("ha dado guerra")
* es muy complejo
* tiene documentación difícil o dispersa

entonces se requiere:

1. índice de módulos
2. documentación especial en `docs`
3. lectura directa del módulo

---

# Rol del README

El archivo `README` contiene información orientada principalmente al usuario.

Debe incluir:

* descripción general del sistema
* ubicación de los módulos principales
* importancia de cada componente
* explicación del sistema de documentación
* guía de navegación del repositorio

El README explica **cómo se estructura y cómo se consulta la documentación del proyecto**.

---

# Diseño orientado a IA con ventana limitada

El sistema modular está diseñado específicamente para **IA con ventana de contexto limitada**.

Por esta razón:

* los módulos deben ser **pequeños**
* deben contener **funciones claramente agrupadas**
* deben ser **fáciles de cargar en contexto**

Regla principal:

Un módulo no debe contener **más de tres funciones principales** o su equivalente en otros paradigmas (por ejemplo clases).

---

# Restricciones de contexto para modelos locales

En entornos con modelos locales como **Ollama**, la ventana de contexto es más limitada.

Configuración base conservadora:

```
Default Ollama: 2048 tokens
```

Por esta razón, los módulos deben diseñarse para **no superar la capacidad de contexto del modelo utilizado**.

También se debe evitar que la carga de contexto implique **más de 1 GB de memoria dedicada al proceso de conversación activa**.

---

# Configuración experimental de contexto

A medida que se realizan pruebas, se puede aumentar el contexto del modelo.

Ejemplo de configuración:

```
PARAMETER num_ctx 8192
PARAMETER kv_cache_type q4_0

PARAMETER flash_attn true

PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.15
PARAMETER num_batch 512
```

Estos parámetros permiten mejorar el rendimiento técnico del modelo dependiendo de:

* el modelo utilizado
* la capacidad de la máquina
* el tipo de proceso ejecutado

---

# Adaptación a modelos con mayor ventana

Cuando se utilizan modelos con mayor capacidad de contexto, como:

* DeepSeek
* modelos de proveedores externos
* modelos accesibles vía OpenRouter

entonces el sistema puede adaptarse y permitir **módulos más grandes o mayor número de módulos cargados simultáneamente**.

En proyectos como **Ares**, la arquitectura modular puede adaptarse dinámicamente según:

* tecnología proveedora (Google, Anthropic, DeepSeek, OpenRouter)
* capacidad de la máquina
* recursos dedicados al proceso

---

# Organización de módulos

Los módulos se organizan siguiendo principios de afinidad funcional.

Cada módulo agrupa **funciones naturalmente relacionadas**.

A su vez:

* los módulos se agrupan en **carpetas**
* las carpetas agrupan **módulos con funciones similares o afines**

Esto permite mantener coherencia estructural en todo el sistema.

---

# Organización de la documentación

La documentación debe seguir la misma lógica estructural que el código.

Por esta razón:

* toda la documentación debe organizarse en carpetas
* cada documento debe tener una ubicación clara dentro del proyecto
* el `README` debe apuntar correctamente a los documentos clave

---

# Principio de depuración

Cada módulo debe ser creado con **depuración máxima desde el inicio**.

Esto implica:

* pruebas tempranas
* validación funcional
* claridad en comentarios
* estructura limpia

El mismo principio aplica a los programas que utilizan los módulos.

---

# Principio general del sistema

El sistema modular existe para lograr tres objetivos principales:

1. mejorar la comprensión del código por parte de IA
2. facilitar la reutilización de código
3. reducir errores repetidos en el desarrollo

El diseño modular es por lo tanto **una decisión arquitectónica orientada tanto a humanos como a inteligencia artificial**.

---





## 10. Soberanía del Entorno y Precedencia del $PATH

Es crítico entender cómo el sistema operativo resuelve los comandos para evitar errores de dependencias (ej. `ModuleNotFoundError`).

### El Problema de la Precedencia
Si un proyecto tiene su carpeta `bin/` dentro del `$PATH` del usuario y esta aparece **antes** que `/usr/bin/`, el sistema ejecutará el script local. 
* Si el script local es un archivo Python puro con shebang `#!/usr/bin/env python3`, este usará el intérprete global si el entorno virtual no está activo, fallando al no encontrar las librerías del proyecto (como `click`).

### La Solución: Bash Wrappers Universales
Para garantizar la soberanía del entorno, **todo ejecutable en `bin/` (local) o `/usr/bin/` (producción) debe ser un Bash Wrapper** que utilice `uv run`.

#### Estándar de Wrapper Local (bin/):
Usa rutas relativas para mantener la portabilidad del repositorio.
```bash
#!/bin/bash
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
exec uv run --project "$PROJECT_DIR" python "$PROJECT_DIR/src/main.py" "$@"
```

#### Estándar de Wrapper Global (/usr/bin/):
Gestionado automáticamente por `ini v2.1`.
```bash
#!/bin/bash
export TR_PROJECT_ROOT="/ruta/absoluta/al/proyecto"
exec uv run --project "$TR_PROJECT_ROOT" python "$TR_PROJECT_ROOT/src/main.py" "$@"
```

Esta estructura asegura que el comando funcione correctamente **desde cualquier ubicación**, respetando el directorio de trabajo del usuario y garantizando el aislamiento del entorno virtual.

## 11. Preservación de Evidencias y Carpeta OLD (Jamas Borramos)

En el ecosistema TRON, **la información es el activo más valioso**. Por lo tanto, rige la norma de **NO BORRAR NADA**.

*   **Evidencias Temporales:** Scripts de prueba, borradores o investigaciones (`test/`, scripts sueltos) nunca se eliminan.
*   **Organización:** Si un archivo molesta o ya no es útil para la rama principal, se mueve a una subcarpeta llamada `OLD/` dentro de su directorio actual, o a la carpeta raíz `papelera/`.
*   **Puntero de Borrado:** La carpeta `papelera/` se considera un "puntero a borrar", pero su limpieza es una decisión humana soberana, nunca automática por parte de una IA.

## 12. Gestión de TODO por Fases (Eficiencia de Contexto)

Para optimizar el uso de tokens y la memoria de la IA, el seguimiento de tareas se organiza por **Fases de Naturaleza Común**.

*   **Agrupación:** Las tareas atómicas se agrupan en fases (ej. "Fase 1: Infraestructura Core").
*   **Estado:** La IA actualiza el estado de la **Fase** completa, resumiendo el progreso para mantener el `TODO.md` compacto y altamente semántico.
*   **Atomicidad:** Las tareas dentro de la fase deben ser claras, precisas, granulares, descriptivas y ordenadas con una temporalidad lógica.

## 13. Skills (Librería de Kung-Fu para IAs)

Las Skills son módulos de conocimiento procedimental que permiten a las IAs adquirir capacidades específicas ("Kung-Fu") sin saturar el contexto principal.

*   **Ubicación:** `docs/skills/`.
*   **Formato:** `SKILL.md` con Frontmatter YAML (name, description) y cuerpo Markdown.
*   **Indización:** Existe un `INDEX.md` en la carpeta de skills que sirve como punto de entrada único.
*   **Referencia:** Los archivos de contexto de IA (`GEMINI.cli`, `QWEN.md`) deben apuntar a este índice.

---

# ANEXO

# Integración de Binarios Externos, Organización del Proyecto y Módulos Agente


## 1. Integración de binarios externos y repositorios de terceros

En muchos proyectos es necesario utilizar herramientas externas, binarios ya compilados o repositorios de terceros. Ejemplos típicos pueden ser herramientas como:

* terminales avanzados
* exploradores de archivos
* utilidades CLI
* herramientas de análisis o automatización

Cuando esto ocurre, el proyecto debe intentar **integrar estos recursos de forma organizada y controlada**.

Siempre que sea posible:

* el **binario debe copiarse o instalarse dentro de la carpeta `bin` del proyecto**
* la **configuración debe centralizarse dentro de la carpeta `config` del proyecto**

Esto permite que el proyecto mantenga **autonomía operativa**, evitando depender de configuraciones dispersas en el sistema.

---

## 2. Organización de configuración de herramientas externas

Cada binario externo o repositorio integrado debe tener **su propia carpeta de configuración dentro de `config`**.

Ejemplo conceptual:

```
project/
│
├─ bin/
│   ├─ herramienta1
│   ├─ herramienta2
│
├─ config/
│   ├─ herramienta1/
│   │   └─ config
│   ├─ herramienta2/
│   │   └─ config
```

Esto permite:

* aislar configuraciones
* facilitar mantenimiento
* evitar conflictos entre herramientas

---

## 3. Organización paranoica del proyecto

Todo el proyecto debe organizarse de manera **extremadamente ordenada**.

Esto implica:

* uso sistemático de carpetas
* separación clara de responsabilidades
* organización en subcarpetas cuando sea necesario

El principio es simple:

**todo elemento del proyecto debe tener una ubicación lógica y explícita**.

Esta organización facilita:

* mantenimiento
* navegación del repositorio
* comprensión del sistema por humanos y por IA

---

## 4. Manejo de código que no funciona

El código que no está funcionando no debe eliminarse inmediatamente.

En su lugar debe moverse a una carpeta interna del proyecto llamada:

```
papelera/
```

Esto permite:

* conservar trabajo previo
* recuperar soluciones parciales
* evitar pérdida de experimentos útiles

La carpeta papelera actúa como **zona de descarte temporal dentro del proyecto**.

---

## 5. Módulos que funcionan como herramientas o agentes

Como se explicó en el documento principal, los módulos pueden cumplir distintos roles:

* biblioteca reutilizable
* herramienta CLI
* componente importable

Sin embargo, existe una categoría especial de módulos.

Cuando un módulo:

* tiene acceso a un modelo LLM
* puede procesar tareas de forma autónoma
* puede devolver resultados estructurados

entonces ese módulo puede funcionar como **subagente del sistema**.

---

## 6. Módulos con salida estructurada para IA

Para que un módulo pueda funcionar como herramienta de IA o subagente, debe poder devolver resultados en un formato estructurado.

El formato recomendado es:

```
JSON estructurado
```

Este JSON debe ser:

* claro
* consistente
* fácil de interpretar por otros módulos o por sistemas de orquestación.

Esto permite que el módulo pueda ser utilizado dentro de:

* pipelines de IA
* agentes
* automatizaciones complejas.

---

## 7. Carpeta de agentes

Los módulos que cumplen funciones de agente o subagente deben ubicarse en una carpeta específica del proyecto.

```
Agentes/
```

Esta carpeta contiene módulos que:

* interactúan con modelos de lenguaje
* generan respuestas estructuradas
* actúan como herramientas inteligentes dentro del sistema.

---

## 8. Relación entre módulos y agentes

Un módulo puede evolucionar en el tiempo.

Por ejemplo:

módulo simple → herramienta CLI → módulo reutilizable → agente

Si un módulo adquiere capacidades de agente, entonces puede ser **reubicado o duplicado dentro de la carpeta `Agentes`**.

Esto permite mantener clara la arquitectura del sistema.

---

## 9. Documentación en el índice de módulos

Todo lo anterior debe reflejarse en el **índice de módulos del proyecto**.

El índice debe indicar para cada módulo:

* función principal
* tipo de módulo
* ubicación en el proyecto
* si es herramienta CLI
* si es módulo importable
* si funciona como agente o subagente
* si tiene salida JSON estructurada
* si depende de un LLM

Esto convierte al índice en **un mapa operativo completo del sistema modular**.

---

# Versión IA-Friendly (Optimizada para LLMs)

## Objetivo del anexo

Definir reglas de organización del proyecto para:

* integración de herramientas externas
* manejo de código experimental
* clasificación avanzada de módulos
* creación de módulos-agente compatibles con IA.

---

## 1. Integración de herramientas externas

Regla principal:

Si el proyecto utiliza herramientas externas o binarios de terceros:

```
binarios → carpeta /bin
configuración → carpeta /config
```

Ejemplo:

```
project/
 ├─ bin/
 │   └─ herramienta_externa
 │
 ├─ config/
 │   └─ herramienta_externa/
 │        └─ configuración
```

Beneficios:

* reproducibilidad del entorno
* control total del proyecto
* independencia del sistema host.

---

## 2. Regla de organización paranoica

Todo el proyecto debe seguir el principio:

```
Todo debe estar en una carpeta específica.
Nada debe quedar suelto.
```

Esto implica:

* uso intensivo de subcarpetas
* separación clara de responsabilidades
* organización consistente del repositorio.

---

## 3. Código no funcional

El código experimental o no funcional no debe eliminarse.

Debe moverse a:

```
papelera/
```

Propósito:

* conservar experimentos
* evitar pérdida de soluciones parciales
* mantener el repositorio principal limpio.

---

## 4. Tipos de módulos en el sistema

Un módulo puede ser:

### Tipo 1 — Biblioteca reutilizable

Importable desde otros módulos.

### Tipo 2 — Herramienta CLI

Ejecutable desde la consola.

### Tipo 3 — Módulo híbrido

Importable y ejecutable.

### Tipo 4 — Módulo-Agente

Módulo con capacidades de IA.

---

## 5. Definición de módulo-agente

Un módulo se considera agente cuando cumple:

* conexión con un LLM
* capacidad de resolver tareas
* salida estructurada
* integración en flujos de IA.

---

## 6. Salida estructurada para IA

Formato recomendado:

```
JSON
```

Ejemplo conceptual:

```
{
  "estado": "ok",
  "accion": "resultado_procesado",
  "datos": {...}
}
```

Beneficios:

* interoperabilidad entre módulos
* integración con orquestadores
* facilidad de análisis por IA.

---

## 7. Ubicación de agentes

Los agentes deben ubicarse en:

```
Agentes/
```

Ejemplo:

```
project/
 ├─ Agentes/
 │   ├─ agente_codigo
 │   ├─ agente_documentacion
 │   └─ agente_analisis
```

---

## 8. Evolución de módulos

Un módulo puede evolucionar siguiendo el patrón:

```
módulo básico
→ herramienta CLI
→ módulo reutilizable
→ agente IA
```

La arquitectura debe permitir esta evolución sin romper el sistema.

---

## 9. Reglas del índice de módulos

El índice de módulos debe documentar para cada módulo:

```
nombre
tipo
ubicación
función
dependencias
si es CLI
si es importable
si es agente
si usa LLM
si devuelve JSON estructurado
```

Esto permite que el índice funcione como **mapa operativo del sistema para humanos y para IA**.

---




# MODIFICACIÓN 1


Vamos a generar **una versión IA-friendly de tu `REP_STRUCTURE.md`** adaptada a tu proyecto modular, organizada para que tu Ollama (u otro LLM) pueda **navegar y entender el repo sin desperdiciar tokens ni memoria**, respetando tus carpetas, módulos, agentes y binarios externos.
El objetivo es que la IA **sepa exactamente dónde buscar, qué importar y qué ignorar**, evitando “ruido” y alucinaciones de ruta.

---

# REP_STRUCTURE.md — Versión IA-Friendly

````markdown
# REP_STRUCTURE.md
# Arquitectura del Proyecto para IA
# Generado para LLM con contexto limitado (ej. Ollama 8K tokens, 3GB RAM)

## 1. Reglas Generales para la IA
- Ignorar carpetas basura: `node_modules/`, `.git/`, `papelera/` (salvo que se indique lo contrario)
- Leer primero los READMEs de cada carpeta para decidir relevancia
- Los binarios externos en `/bin` no necesitan leer código fuente, solo interfase de configuración
- Carpetas de configuración (`/config`) contienen parámetros y ajustes; leer solo si el módulo/agent depende de ellos
- Los módulos en `/Agentes` pueden generar JSON estructurado, estos son subagentes IA
- Solo cargar el código necesario según la tarea indicada
- No asumir rutas que no existan
- Respeta los límites de `num_ctx` y RAM indicados en `.ai/rules.md`

---

## 2. Jerarquía del proyecto

```text
mi-proyecto/
├── .ai/
│   ├── rules.md          # Restricciones de memoria, contextos, variables de ejecución
│   └── architecture.md   # Mapa conceptual del proyecto
├── REP_STRUCTURE.md      # Este archivo — mapa operativo IA
├── bin/                  # Binarios externos integrados
│   ├── kitty
│   └── broot
├── config/               # Configuración centralizada
│   ├── kitty/
│   └── broot/
├── papelera/             # Código no funcional / experimental
├── Agentes/              # Módulos IA-friendly con JSON output
│   ├── agente_modulo1/
│   ├── agente_modulo2/
├── src/                  # Código principal del proyecto
│   ├── README.md
│   ├── core/
│   │   └── logic.py
│   ├── modules/          # Módulos normales (CLI, importables)
│   │   ├── modulo1/
│   │   │   ├── __init__.py
│   │   │   └── funciones.py
│   │   └── modulo2/
│   └── api/
│       └── routes.py
````

---

## 3. Tipos de elementos y comportamiento esperado

| Elemento       | Rol IA                               | Nota de lectura IA                                              |
| -------------- | ------------------------------------ | --------------------------------------------------------------- |
| `/bin`         | Binarios externos                    | Solo leer interfase de configuración, no código fuente          |
| `/config`      | Configuración centralizada           | Leer solo si módulo/agent depende de él                         |
| `/papelera`    | Código no funcional                  | Ignorar en ejecución normal                                     |
| `/Agentes`     | Módulos IA con JSON output           | Leer y ejecutar según tarea, devuelven resultados estructurados |
| `/src/modules` | Módulos normales (CLI / importables) | Importar según necesidad                                        |
| `/src/core`    | Lógica principal del proyecto        | Siempre relevante, leer primero                                 |
| `/src/api`     | Puntos de acceso / rutas API         | Leer solo si la tarea involucra endpoints                       |

---

## 4. Flujo de lectura IA recomendado

1. Leer `.ai/rules.md` para obtener parámetros de ejecución, límites de memoria y contexto
2. Leer `REP_STRUCTURE.md` para decidir qué módulos y agentes son relevantes
3. Leer `src/README.md` de cada carpeta de código relevante
4. Cargar solo módulos necesarios:

   * `/Agentes` → si tarea requiere LLM + JSON
   * `/modules` → si se necesita CLI o importación
5. Ignorar código en `/papelera/` salvo consulta explícita de experimentos antiguos
6. Consultar `/bin` y `/config` únicamente para parámetros operativos de binarios externos
7. Siempre priorizar **subida de contexto mínima** y **lectura selectiva** para no desperdiciar tokens

---

## 5. Salida esperada de módulos-agente

* Formato JSON estructurado  (ejemplo):
 
 En lo posible usar estructuracion disponible nativa: ollama, openrouter, propia del proveedor, modelo sdk o tecnología
 
```json
{
  "estado": "ok",
  "accion": "resultado_procesado",
  "datos": {
      "modulo": "agente_modulo1",
      "resultado": "...",
      "detalles": {}
  }
}
```

* Toda interacción con la IA debe cumplir este estándar
* Evita confusión de rutas y mantiene consistencia

---

## 6. Notas adicionales

* Las carpetas y subcarpetas están organizadas de forma “paranoica” para que **nada quede fuera de lugar**
* Cada módulo, agente o binario tiene **una ubicación explícita y documentada**
* Toda la navegación por la IA se basa en:

  1. Jerarquía clara de carpetas
  2. Documentación markdown en cada nivel (`README.md`, `.ai/*.md`)
  3. Índice de módulos actualizado (`REP_STRUCTURE.md`)

---



---


# CORRECCION 2

Reorganizar la lógica según tu intención real, respetando tu estilo, tu flujo de trabajo y la filosofía que hemos construido sobre **IA CLI trabajando con proyectos existentes y skills**. Este análisis es estratégico: no voy a proponer aún nada que copiar/pegar, sino **redefinir cómo debes estructurarlo** para tu IA y tu proyecto.

---

## 1️⃣ Reinterpretación de tu flujo de trabajo

Tu intención principal:

1. **IA como asistente interactivo, no decisor soberano:**

   * Tú decides soberanamente qué hacer.
   * La IA **asiste**, recuerda el contexto, sugiere, ejecuta procesos como “skills” bajo tu instrucción, pero no toma decisiones de publicación o producción por sí misma.

2. **Skills como módulos inteligentes:**

   * Cada funcionalidad ejecutable (scriptProd, depurador, agente, etc.) es una **skill**.
   * Las skills tienen su **documentación IA** en `docs/skills/skill-nombre-descriptivo.md`.
   * Cuando llamas a una skill, la IA sabe **qué hacer**, cómo inicializarla y cómo integrarla en el flujo del proyecto.

3. **Leeme como fuente de verdad funcional:**

   * Todo lo que está **operativo o probado** se refleja en el `LEEME.md`.
   * La IA **lee el LEEME** para saber qué funcionalidades realmente existen y cuáles no.
   * Esto evita “cerrar” un módulo antes de que esté funcional: no hay cierres automáticos, solo avances que se reflejan en la documentación funcional.

4. **JSON como interfaz teórica de salida de agentes:**

   * Cuando hablamos de JSON, es **la salida de un módulo/skill/agent**, no parámetros de ejecución del script.
   * La IA usa esto como referencia de **estado y resultados**, no como flujo de producción directo.

5. **Inicialización como primer paso universal:**

   * La IA debe siempre tener presente el proceso de **inicializar un proyecto**, crear carpetas base, colocar documentación centralizada, configurar módulos, agentes y binarios.
   * Esto se refleja en una **skill “inicialización”**: `docs/skills/skill-inicializacion.md`.

6. **Producción funcional:**

   * Poner un proyecto o módulo a producción es una **acción de skill**, pero no es algo que la IA decida sola.
   * La IA sabe cómo ejecutar la skill `scriptProd`, leer su documentación y aplicarla si tú lo ordenas.
   * Esto garantiza que la IA **aprende kung-fu**, es decir, adquiere la capacidad de ejecutar skills sin dispersar la documentación.

---

## 2️⃣ Arquitectura de skills para la IA

Con base en tu intención:

```text
docs/
 ├─ skills/
 │   ├─ skill-inicializacion.md      # Crear proyecto, carpetas base, docs y bin
 │   ├─ skill-scriptProd.md          # Publicar proyecto en /usr/bin
 │   ├─ skill-agenteX.md             # Cada módulo o agente como skill independiente
 │   └─ skill-color-engine.md        # Ejemplo: skill de un módulo específico
 ├─ .ai/
 │   └─ rules.md                     # Reglas de ejecución y contexto para la IA
 ├─ REP_STRUCTURE.md                 # Mapa del proyecto
 └─ LEEME.md                          # Fuente de verdad funcional
```

* **docs/skills/**: Cada skill tiene un documento que describe:

  * Qué hace
  * Qué archivos o módulos afecta
  * Cómo inicializarlo
  * Cómo interactuar con la IA (JSON outputs, logs)

* **docs/.ai/rules.md**: La IA siempre lo consulta antes de actuar: límites de contexto, memoria, exclusiones, flujo de módulos y agentes.

* **REP_STRUCTURE.md**: Guía de relaciones entre módulos, agentes y skills.

* **LEEME.md**: Solo contiene lo que **está funcional y probado**, para que la IA no “alucine” funcionalidades.

---

## 3️⃣ Flujo conceptual de interacción IA CLI

1. **Inicializar proyecto:**

   * `skill-inicializacion.md` → crea carpetas base, bin, config, docs/skills.
   * Todo queda centralizado, sin dispersión de documentación.

2. **Agregar skill:**

   * Cada skill documentada en `docs/skills/skill-nombre.md`.
   * La IA puede ejecutar la skill cuando tú se lo ordenes.
   * La IA aprende a usarla (kung-fu) leyendo su documentación.

3. **Ejecutar skill (ej. scriptProd):**

   * La IA sabe qué hace la skill.
   * Puede generar outputs teóricos en JSON si se requiere, para agentes o procesos automatizados.
   * **No decide**; tú ejecutas la skill.

4. **Actualizar LEEME y REP_STRUCTURE:**

   * Cada acción funcional se refleja en el LEEME.
   * La IA usa el LEEME como fuente de verdad para próximos pasos.

5. **Iterar:**

   * Módulos se crean, prueban, documentan en skills y LEEME.
   * La IA mantiene todo el contexto actualizado según reglas en `.ai/rules.md`.

---

## 4️⃣ Principios clave para la IA

1. **No dispersión de documentación:** Todo centralizado en `docs/skills` y `docs/.ai`.
2. **Funcionalidad real = LEEME:** No actuar sobre lo que no está operativo.
3. **JSON = salida de skills/agents:** Referencia, no parámetros de ejecución.
4. **Skills = módulos ejecutables por instrucción humana:** IA aprende kung-fu leyendo su doc.
5. **Inicialización = primer skill obligatorio:** La IA siempre conoce cómo empezar.

---

✅ Resultado conceptual:

* La IA tiene un **mapa mental claro**:

  * Skills → docs/skills
  * Reglas → docs/.ai/rules.md
  * Estado funcional → LEEME.md
  * Relaciones → REP_STRUCTURE.md

* Tú mantienes **control soberano**: decides cuándo ejecutar qué skill.

* La IA mantiene **contexto, aprendizaje y navegación de skills**.

---

















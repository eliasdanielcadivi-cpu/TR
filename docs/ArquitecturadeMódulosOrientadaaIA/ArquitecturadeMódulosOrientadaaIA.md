
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



# 📘 ÍNDICE MAESTRO PARA IAS - SISTEMA DE CONDUCCIÓN COGNITIVA

> **Documento de Referencia Arquitectónica para Inteligencias Artificiales**  
> **Propósito:** Brindar cohesión, sistematicidad y orden secuencial a cualquier IA que trabaje en este sistema  
> **Ubicación:** `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/`  
> **Versión:** 1.0 - Documento Vivo

---

## 🎯 OBJETIVO DE ESTE ÍNDICE

Este documento **NO es un resumen**. Es una **brújula arquitectónica** que permite a cualquier IA:

1. **Comprender el sistema completo** sin leer todos los documentos simultáneamente
2. **Entender el orden lógico de implementación** (qué va primero, qué después, por qué)
3. **Identificar ejes transversales** que atraviesan múltiples componentes
4. **Controlar la entropía** evitando modificaciones que rompan la coherencia del sistema
5. **Trabajar de forma modular** sin perder la visión holística

---

## 📊 MAPA MENTAL DEL SISTEMA (VISTA DE 30,000 PIES)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE CONDUCCIÓN COGNITIVA                       │
│                                                                          │
│  PROPÓSITO: Convertir intención difusa → evidencia → decisión → avance  │
│                                                                          │
│  FILosOFÍA: "Google Lens" - La herramienta desaparece, queda el resultado│
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│   QUÉ ES      │           │   QUÉ NO ES   │           │   PARA QUÉ    │
│               │           │               │           │               │
│ • Sistema     │           │ • NO chatbot  │           │ • Éxito       │
│ • Conducción  │           │ • NO asistente│           │   rotundo     │
│ • Control     │           │ • NO Q&A      │           │ • Ejecución   │
│ • Memoria     │           │               │           │ • Resultado   │
└───────────────┘           └───────────────┘           └───────────────┘
```

---

## 📑 ESTRUCTURA DEL ÍNDICE

Este índice está organizado en **6 CAPAS DE PROFUNDIDAD**:

| Capa | Nombre | Propósito | IA debe leer cuando... |
|------|--------|-----------|------------------------|
| **0** | Fundamentos Filosóficos | Entender el "por qué" profundo del sistema | Empieza a trabajar por primera vez |
| **1** | Arquitectura Conceptual | Comprender componentes y relaciones | Necesita modificar estructura |
| **2** | Flujo Operativo | Entender cómo funciona el sistema en tiempo real | Va a implementar lógica de negocio |
| **3** | Especificaciones Técnicas | Conocer detalles de implementación | Va a escribir código |
| **4** | Protocolos de Control | Entender mecanismos anti-entropía | Va a hacer cambios estructurales |
| **5** | Referencias Cruzadas | Navegar entre documentos relacionados | Necesita profundizar en un tema |

---

# 🏛️ CAPA 0: FUNDAMENTOS FILOSÓFICOS

> **PRINCIPIO RECTOR:** "La herramienta desaparece para dejar paso al resultado" - Filosofía Google Lens

## 0.1 QUÉ ESTÁS HACIENDO REALMENTE

**Ubicación:** `requerimientos.md` → Sección 1 (líneas 1-50)

**Propósito:** Desmitificar la naturaleza del sistema. No es lo que parece superficialmente.

**Conceptos Clave:**

| Concepto | Definición | Implicación Práctica |
|----------|------------|---------------------|
| **Conducción Cognitiva** | La IA no responde → dirige | Las preguntas son estratégicas, no informativas |
| **Control de Deriva** | Mecanismo que mide cuánto cambia el prompt | Delta calculator + umbral de aprobación |
| **Memoria de Propósito** | Objetivos permanentes inyectados en cada interacción | No se pierde el norte aunque el usuario divague |

**Por qué importa:** Si una IA piensa que esto es un "chatbot", diseñará mal. Esto es un **motor de ejecución con interfaz conversacional**.

**Relación con otros documentos:**
- → `ListaRequerimientos.md` (puntos 2, 4, 8)
- → `proyecto.md` (Características Clave 1, 4)

---

## 0.2 INTENCIONES REALES (SIN ROMANTICISMO)

**Ubicación:** `requerimientos.md` → Sección 2 (líneas 51-100)

**Propósito:** Explicitar lo que el sistema DEBE lograr, no lo que "suena bien".

**Los 5 Debes del Sistema:**

```
1. OBLIGAR al usuario a avanzar (no permite divagar)
2. ELIMINAR fricción cognitiva (usuario no escribe mucho)
3. MANTENER coherencia estratégica en el tiempo (no perder contexto)
4. CONTROLAR a la propia IA (la IA no es libre)
5. CONVERTIR conversación en ejecución (diálogo → acción → resultado)
```

**Jerarquía de Importancia:**

```
PRIORIDAD 1 (Crítico): #5 - Convertir conversación en ejecución
PRIORIDAD 2 (Alto):    #1 - Obligar avance, #4 - Controlar IA
PRIORIDAD 3 (Medio):   #2 - Eliminar fricción, #3 - Mantener coherencia
```

**Señales de que el sistema falla:**
- ❌ El usuario puede pasar sesiones enteras sin producir evidencia
- ❌ La IA cambia el prompt sin aprobación y se desvía del objetivo
- ❌ Los objetivos declarados al inicio se "olvidan" en la conversación

**Relación con otros documentos:**
- → `ListaRequerimientos.md` (punto 1: Directiva principal)
- → `requerimientos.md` Sección 3 (Flujo Ideal del Usuario)

---

## 0.3 FILOSOFÍA DE DISEÑO "GOOGLE LENS"

**Ubicación:** `ListaRequerimientos.md` → Punto 1 (líneas 1-27)

**Propósito:** Establecer el criterio estético y funcional NO NEGOCIABLE.

**Los 5 Principios Google Lens:**

| Principio | Qué Significa | Qué NO Significa |
|-----------|---------------|------------------|
| **1. Qué (El Atractivo)** | Valor = utilidad/esfuerzo, no estética | No es "diseño bonito" |
| **2. Cómo (Metodología)** | Pragmatismo radical: navaja suiza, no catedral | No es "código elegante" |
| **3. Cuándo (Aplicación)** | Priorizar entorno real (Note 8, Termux) sobre teoría | No es "ideal académico" |
| **4. Por qué (Justificación)** | Ayuda limpia y honesta, sin carga cognitiva | No es "feature creep" |
| **5. Para qué (Propósito)** | Éxito rotundo del usuario mediante interacción fluida | No es "mantener engagement" |

**Criterio de Decisión para IAs:**

```python
def should_implement_feature(feature):
    utilidad = feature.impact_on_user_success
    esfuerzo = feature.complexity + feature.cognitive_load
    ratio = utilidad / esfuerzo
    
    # Google Lens: ratio debe ser ALTO
    return ratio > UMBRAL_MINIMO and feature.adapts_perfectly_to_need
```

**Relación con otros documentos:**
- → `METODOLOGIA-MODULAR.md` (Patrones Arquitectónicos)
- → `proyecto.md` (Notas de Diseño)

---

# 🏗️ CAPA 1: ARQUITECTURA CONCEPTUAL

> **PRINCIPIO RECTOR:** "Una cosa" - Entidad flexible que trasciende categorías tradicionales

## 1.1 DEFINICIÓN DE ENTIDAD DE SERVIDOR COGNITIVO

**Ubicación:** `ListaRequerimientos.md` → Punto 2 (líneas 28-60)

**Propósito:** Definir qué es el sistema sin limitarlo con etiquetas tradicionales.

**Lo que NO es:**
- ❌ No es una "app" (sugiere limitación móvil)
- ❌ No es un "programa" (sugiere ejecución local)
- ❌ No es un "agente" (sugiere autonomía total)

**Lo que SÍ es:**
- ✅ Es "una cosa" - entidad flexible
- ✅ Es "especie de servidor node" - infraestructura persistente
- ✅ Es "orquestador de interacciones inteligentes"

**Implicación Arquitectónica:**

```
┌─────────────────────────────────────────────┐
│            SERVIDOR COGNITIVO               │
│                                             │
│  ┌─────────────┐  ┌──────────────┐         │
│  │  Ejecutor   │  │  Arquitecto  │         │
│  │  (DeepSeek) │  │  (Control)   │         │
│  └──────┬──────┘  └──────┬───────┘         │
│         │                │                  │
│         └────────┬───────┘                  │
│                  │                          │
│         ┌────────▼────────┐                 │
│         │  Socket.IO      │                 │
│         │  (Comunicación) │                 │
│         └────────┬────────┘                 │
│                  │                          │
│         ┌────────▼────────┐                 │
│         │  Usuario (UI)   │                 │
│         └─────────────────┘                 │
└─────────────────────────────────────────────┘
```

**Relación con otros documentos:**
- → `requerimientos.md` → Diagrama de Todo el Sistema (líneas 1400-1600)
- → `proyecto.md` → Arquitectura Tecnológica

---

## 1.2 ARQUITECTURA DE DOBLE INSTANCIA (EJECUTOR + ARQUITECTO)

**Ubicación:** `ListaRequerimientos.md` → Punto 8 (líneas 180-210) | `requerimientos.md` → Sección 6

**Propósito:** Separar responsabilidades para controlar deriva del LLM.

**Instancia 1: EJECUTOR**

| Atributo | Descripción |
|----------|-------------|
| **Rol** | Interactúa con el usuario en tiempo real |
| **Motor** | DeepSeek API (vía OpenRouter) |
| **Función** | Generar preguntas, respuestas, streaming |
| **Limitación** | NO puede cambiar el prompt sin aprobación |
| **Contexto** | Recibe objetivos inyectados desde memoria |

**Instancia 2: ARQUITECTO**

| Atributo | Descripción |
|----------|-------------|
| **Rol** | Analiza meta permanente y propone cambios |
| **Motor** | Capa de control (lógica determinista + LLM auxiliar opcional) |
| **Función** | Calcular delta, filtrar merecimiento, auditar deriva |
| **Poder** | Puede VETAR cambios del Ejecutor |
| **Contexto** | Tiene visión completa de objetivos permanentes |

**Flujo de Negociación:**

```
┌─────────────────┐
│   EJECUTOR      │
│  Propone cambio │
│  en prompt      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DELTA CALCULATOR│
│  Calcula score  │
│  (0 a 1)        │
└────────┬────────┘
         │
         ▼
    ¿Delta > 0.3?
         │
    ┌────┴────┐
    │         │
   NO        SÍ
    │         │
    ▼         ▼
┌────────┐  ┌─────────────────┐
│ ACEPTAR│  │ ARQUITECTO      │
│ cambio │  │ Evalúa          │
└────────┘  │ merecimiento    │
            └────────┬────────┘
                     │
                     ▼
              ¿Cambio válido?
                     │
                ┌────┴────┐
                │         │
               SÍ        NO
                │         │
                ▼         ▼
           ┌────────┐  ┌──────────┐
           │ ACEPTAR│  │ RECHAZAR │
           │        │  │ y        │
           │        │  │ NEGOCIAR │
           └────────┘  └──────────┘
```

**Relación con otros documentos:**
- → `requerimientos.md` → Sistema de Gobernanza (Capa 3 del diagrama)
- → `ListaRequerimientos.md` → Punto 5 (Protocolo de Negociación)

---

## 1.3 MECÁNICA DE PROMPT VIVO Y MUTANTE

**Ubicación:** `ListaRequerimientos.md` → Punto 4 (líneas 120-160) | `requerimientos.md` → Sección 1

**Propósito:** Explicar cómo el system prompt evoluciona en tiempo real.

**Concepto Fundamental:**

```
Prompt NO es estático → Prompt es ORGANISMO VIVO que:
  1. Nace con configuración base
  2. Recibe input del usuario
  3. El Ejecutor propone alteración
  4. El Arquitecto valida/ajusta
  5. Se inyecta de vuelta al contexto
  6. Repetir
```

**Tipos de Cambios del Prompt:**

| Tipo | Magnitud | Requiere Aprobación | Ejemplo |
|------|----------|---------------------|---------|
| **Micro-ajuste** | Delta < 0.1 | ❌ No | Aclarar definición de término |
| **Ajuste moderado** | Delta 0.1-0.3 | ⚠️ Informar | Agregar contexto de sesión anterior |
| **Cambio significativo** | Delta 0.3-0.6 | ✅ Sí (negociado) | Modificar enfoque de pregunta |
| **Reestructuración** | Delta > 0.6 | ✅ Sí (Arquitecto veto) | Cambiar objetivo fundamental |

**Algoritmo de Alteración:**

```python
def alter_prompt(user_response, current_prompt, objectives):
    # Paso 1: Ejecutor propone nuevo prompt
    proposed_prompt = executor.generate_new_prompt(user_response, current_prompt)
    
    # Paso 2: Calcular delta
    delta_score = calculate_delta(current_prompt, proposed_prompt)
    
    # Paso 3: Evaluar umbral
    if delta_score < 0.1:
        return proposed_prompt  # Micro-ajuste automático
    
    elif delta_score < 0.3:
        log_change(proposed_prompt, delta_score)  # Informar pero aceptar
        return proposed_prompt
    
    elif delta_score < 0.6:
        # Negociar con usuario
        user_approval = ask_user_approval(proposed_prompt, delta_score)
        return proposed_prompt if user_approval else current_prompt
    
    else:
        # Cambio mayor: Arquitecto decide
        architect_decision = architect.evaluate(proposed_prompt, objectives)
        return proposed_prompt if architect_decision else current_prompt
```

**Relación con otros documentos:**
- → `requerimientos.md` → Capa 3: Gobernanza y Control
- → `ListaRequerimientos.md` → Punto 12 (Métrica de Deriva Deltas)

---

# 🔄 CAPA 2: FLUJO OPERATIVO

> **PRINCIPIO RECTOR:** "Conversación → Decisión → Acción → Resultado"

## 2.1 FLUJO IDEAL DEL USUARIO (6 FASES)

**Ubicación:** `requerimientos.md` → Sección 3 (líneas 101-180)

**Propósito:** Describir el camino perfecto que un usuario debería recorrer.

**FASE 0 — ENTRADA (Definición de Intención)**

| Elemento | Descripción |
|----------|-------------|
| **Trigger** | Usuario declara objetivo inicial |
| **Input** | "Quiero X en Y tiempo" |
| **Proceso** | Sistema normaliza a formato EMT (Evidencia-Métrica-Tiempo) |
| **Output** | Objetivo estructurado guardado en memoria permanente |
| **Criterio de Éxito** | Usuario confirma "sí, eso es lo que quiero" |

**Ejemplo Concreto:**
```
Usuario: "Quiero lanzar mi producto en 3 meses"

Sistema traduce a EMT:
  - Evidencia: Producto disponible para compra (URL/tienda)
  - Métrica: 1 producto publicado, 10 ventas en primera semana
  - Tiempo: 90 días desde hoy

Sistema: "¿Confirmas que tu objetivo es: [EMT estructurado]?"
Usuario: "Sí, exactamente"

→ Memoria permanente actualizada
```

**FASE 1 — UBICACIÓN (Diagnóstico Real)**

| Elemento | Descripción |
|----------|-------------|
| **Trigger** | Objetivo ya definido |
| **Pregunta** | "¿Dónde estás respecto a esto?" |
| **Formato** | Opciones cerradas + comentario opcional |
| **Propósito** | Reducir incertidumbre inicial |
| **Criterio de Éxito** | Sistema tiene línea base clara |

**Ejemplo de Preguntas:**
```
"¿Cuál es tu situación actual?"
[ ] Tengo un prototipo funcional
[ ] Solo tengo la idea
[ ] Ya estoy vendiendo pero quiero escalar
[ ] Otro: [comentario libre]
```

**FASE 2 — MODELADO (Mapa Mental del Usuario)**

| Elemento | Descripción |
|----------|-------------|
| **Trigger** | Diagnóstico completado |
| **Proceso** | IA construye modelo de: capacidades, bloqueos, recursos |
| **Formato** | Extracción cognitiva (no es chat informativo) |
| **Output** | Perfil del usuario con contexto real |
| **Criterio de Éxito** | IA puede predecir obstáculos probables |

**FASE 3 — CONDUCCIÓN (Loop Principal)**

| Elemento | Descripción |
|----------|-------------|
| **Trigger** | Modelo completado |
| **Loop** | 1. IA propone siguiente paso → 2. Usuario responde → 3. IA ajusta prompt → 4. Arquitecto valida → 5. Mantener alineación |
| **Formato** | Preguntas estructuradas + mínima escritura |
| **Output** | Avance incremental hacia objetivo |
| **Criterio de Éxito** | Usuario produce micro-evidencias cada 24-72h |

**FASE 4 — PRESIÓN ESTRATÉGICA**

| Elemento | Descripción |
|----------|-------------|
| **Trigger** | Resistencia detectada o estancamiento |
| **Mecanismo** | IA recuerda objetivos, confronta incoherencias, evita distracciones |
| **Formato** | 3 terapias simultáneas: Conductista (presión), Cognitiva (replantear), Humanista (acompañar) |
| **Output** | Usuario re-engaged o sistema recalibra |
| **Criterio de Éxito** | Usuario rompe resistencia o acepta cambio de estrategia |

**FASE 5 — EJECUCIÓN REAL**

| Elemento | Descripción |
|----------|-------------|
| **Trigger** | Usuario en modo acción |
| **Requerimiento** | Tareas concretas, decisiones irreversibles, outputs reales |
| **Formato** | Evidencia obligatoria (documento, foto, registro) |
| **Output** | Resultado tangible |
| **Criterio de Éxito** | Evidencia presentada ≥ Métrica acordada |

**FASE 6 — CIERRE (Éxito o Recalibración)**

| Elemento | Descripción |
|----------|-------------|
| **Trigger** | Evidencia final presentada |
| **Evaluación** | ¿Estado de éxito alcanzado? |
| **Output SÍ** | Objetivo marcado como "cumplido", celebrar |
| **Output NO** | Recalibrar: nuevo objetivo o cerrar ciclo |
| **Criterio de Éxito** | Usuario tiene claridad sobre siguiente capítulo |

**Relación con otros documentos:**
- → `requerimientos.md` → Estado de Éxito (Sección 4)
- → `requerimientos.md` → Estado de Estancamiento (Sección 5)
- → `requerimientos.md` → Acciones Obligatorias (Sección 6)

---

## 2.2 SISTEMA DE ESTANCAMIENTO Y DETECCIÓN

**Ubicación:** `requerimientos.md` → Sección 5 (líneas 800-1200)

**Propósito:** Definir CUÁNDO y CÓMO intervenir cuando el usuario no avanza.

**Señales Base de Estancamiento (12 señales):**

| ID | Señal | Tipo de Dato | Umbral Default | Negociable |
|----|-------|--------------|----------------|------------|
| S01 | Inactividad temporal | Horas desde última respuesta | 72h | ✅ Sí |
| S02 | Bucle de excusas | Contador de repeticiones de bloqueo | 3 veces | ✅ Sí |
| S03 | Desvío de objetivo | Score de deriva semántica (0-1) | >0.6 | ✅ Sí |
| S04 | Baja energía | Longitud media de respuestas (palabras) | <15 palabras | ✅ Sí |
| S05 | Negativa a compromiso | Contador de rechazos a tareas | 2 veces | ✅ Sí |
| S06 | Procrastinación activa | Promesas sin evidencia / tiempo | 3 promesas | ✅ Sí |
| S07 | Abandono silencioso | Ausencia sin notificación | 7 días | ✅ Sí |
| S08 | Rebote de distracción | Cambios de tema no autorizados | 2 por sesión | ✅ Sí |
| S09 | Colapso de confianza | Keywords: "no puedo", "imposible" | 2 detecciones | ✅ Sí |
| S10 | Objetivo inválido | Score de viabilidad (filtro merecimiento) | <0.3 | ✅ Sí |
| S11 | Ritmo degradado | Velocidad de avance vs. planificado | <50% | ✅ Sí |
| S12 | Evitación emocional | Keywords evasivas, cambio de tono | Detectado | ✅ Sí |

**Estructura de Negociación Inicial:**

```
USUARIO declara objetivo
    ↓
SISTEMA presenta cuestionario de negociación:
  "Para acompañarte efectivamente, definamos juntos
   cuándo consideramos que hay estancamiento."
    ↓
Para CADA señal (S01-S12):
  - Sistema propone umbral default
  - Usuario puede: ACEPTAR / MODIFICAR / ELIMINAR / AÑADIR
    ↓
SISTEMA guarda en BD: user_stall_profile
  {
    "negotiated_signals": ["S01", "S03", "S07"],
    "custom_thresholds": {"S01": "48h", "S03": "0.7"},
    "excluded_signals": ["S12"],
    "added_signals": ["S13_custom"]
  }
```

**Escenarios de Estancamiento (7 tipos):**

| Escenario | ID | Detección | Intervención Inicial |
|-----------|----|-----------|---------------------|
| A. Procrastinación activa | ST-A | Promesas sin evidencia | Presión táctica + replanteamiento |
| B. Abandono silencioso | ST-B | Ausencia prolongada | Humanística (reconexión) + presión |
| C. Rebote de distracción | ST-C | Deriva semántica alta | Cognitiva (foco) + táctica |
| D. Colapso de confianza | ST-D | Keywords negativas | Humanística (apoyo) + cognitiva |
| E. Objetivo inválido | ST-E | Score viabilidad bajo | Cognitiva (redefinición) |
| F. Ritmo degradado | ST-F | Avance <50% plan | Presión táctica + negociación |
| G. Evitación emocional | ST-G | Cambio de tono/escape | Humanística (exploración) |

**Relación con otros documentos:**
- → `ListaRequerimientos.md` → Punto 5 (Protocolo de Negociación)
- → `requerimientos.md` → Sistema de Intervención (3 Terapias)

---

## 2.3 SISTEMA DE INTERVENCIÓN: LAS TRES TERAPIAS SIMULTÁNEAS

**Ubicación:** `requerimientos.md` → Sección 5, Subsección 4 (líneas 950-1050)

**Propósito:** Explicar CÓMO intervenir cuando se detecta estancamiento.

**Concepto Clave:** NO es secuencial (primero A, luego B, luego C). Es **simultáneo** (A + B + C al mismo tiempo).

```
┌─────────────────────────────────────────────────────────┐
│           DETECCIÓN DE ESTANCAMIENTO                    │
│              (cualquier señal activada)                 │
└─────────────────────────────────────────────────────────┘
                          ↓
    ┌─────────────────────┼─────────────────────┐
    ↓                     ↓                     ↓
┌─────────┐         ┌─────────┐           ┌─────────┐
│ TERAPIA │         │ TERAPIA │           │ TERAPIA │
│CONDUCTISTA│        │COGNITIVA│          │HUMANISTA│
│(Presión)│         │(Replant)│          │(Acompañ)│
└────┬────┘         └────┬────┘          └────┬────┘
     │                    │                    │
  • Táctica            • Nuevos              • Tono amable
  • Estratégica          conocimientos       • Comprensivo
  • Consecuencias      • Explicaciones       • Motivación
  • Accountability       por-qué/para-qué    • Validación
     │                    │                    │
     └────────────────────┼────────────────────┘
                          ↓
              ┌─────────────────────┐
              │   RESPUESTA ÚNICA   │
              │  Integrada al usuario│
              │  (no parece 3 IA distintas) │
              └─────────────────────┘
```

**Terapia 1: CONDUCTISTA (Skinner) - 30% del peso**

| Elemento | Descripción | Ejemplo de Implementación |
|----------|-------------|--------------------------|
| **Presión táctica** | Próximo paso concreto, inmediato, pequeño | "¿Qué micro-acción de 5 minutos puedes hacer HOY?" |
| **Presión estratégica** | Recordar objetivo final, costo de no avanzar | "Si no actúas hoy, en 72h habrás perdido X" |
| **Accountability** | Pedir compromiso público con fecha | "¿Qué harás hoy? ¿Cuándo lo reportas?" |
| **Consecuencias** | Reforzamiento negativo si no cumple | Perder acceso a función premium tras 2 fallos |

**Terapia 2: COGNITIVA (Beck/Kahneman) - 40% del peso**

| Elemento | Descripción | Ejemplo de Implementación |
|----------|-------------|--------------------------|
| **Replantear** | "¿Estamos atacando el problema correcto?" | "¿Este obstáculo es real o es una creencia limitante?" |
| **Nuevo conocimiento** | Ofrecer técnica/marco que no ha usado | "¿Conoces la técnica Pomodoro? Te ayudaría aquí" |
| **Explicaciones** | "¿Por qué crees que estás atascado? ¿Para qué quieres esto realmente?" | Cuestionamiento socrático de excusas |
| **Reestructuración cognitiva** | Intercepta distorsiones (Beck) | "No es 'no tengo tiempo', es 'no priorizo esto'" |

**Terapia 3: HUMANISTA (Rogers) - 30% del peso**

| Elemento | Descripción | Ejemplo de Implementación |
|----------|-------------|--------------------------|
| **Tono cálido** | Comprensivo, sin juicio | "Es normal sentirse así, muchos pasan por esto" |
| **Validación** | Reconocer emoción sin reforzar excusa | "Entiendo que te sientes abrumado. Es válido. ¿Qué pequeña parte SÍ puedes hacer?" |
| **Motivación** | Recordar éxitos pasados | "Has logrado X antes, puedes con esto" |
| **Acompañamiento** | Presencia de aliado, no vigilante | "Estoy aquí para asegurarme de que no te abandones a ti mismo" |

**Prompt de Sistema Maestro (Extracto Integrado):**

```
[ROL]
Eres un Sistema de Conducción Cognitiva con detección de estancamiento.
Operas bajo tres terapias simultáneas cuando se activa modo intervención.

[ACTIVACIÓN ESTANCAMIENTO]
IF any(stall_signals.triggered):
    ACTIVAR_TRES_TERAPIAS = true
    NIVEL_AGRESIVIDAD = calcular_based_on_history()

[TERAPIA CONDUCTISTA - 30% peso]
- Presión táctica: próximo paso concreto, inmediato, pequeño
- Estratégica: recordar objetivo final, costo de no avanzar
- Accountability: "¿Qué harás hoy? ¿Cuándo lo reportas?"

[TERAPIA COGNITIVA - 40% peso]
- Replantear: "¿Estamos atacando el problema correcto?"
- Nuevo conocimiento: ofrecer técnica/marco que no ha usado
- Explicaciones: "¿Por qué crees que estás atascado? ¿Para qué quieres esto realmente?"

[TERAPIA HUMANISTA - 30% peso]
- Tono: cálido, comprensivo, sin juicio
- Validación: "Es normal sentirse así, muchos pasan por esto"
- Motivación: "Has logrado X antes, puedes con esto"
- Acompañamiento: "Estoy aquí, no estás solo en esto"

[INTEGRACIÓN]
La respuesta final debe sentirse como UNA conversación coherente,
no tres voces distintas. Equilibrio: firme pero humano, exigente pero comprensivo.
```

**Relación con otros documentos:**
- → `ListaRequerimientos.md` → Punto 13 (Adaptabilidad Multi-Dominio)
- → `requerimientos.md` → Marco Teórico Integrado (Sección 7)

---

## 2.4 ACCIONES OBLIGATORIAS DEL USUARIO

**Ubicación:** `requerimientos.md` → Sección 6 (líneas 1200-1400)

**Propósito:** Definir qué acciones el usuario DEBE realizar para avanzar (no opcionales).

**Principio Fundamental:**

> **El usuario no puede avanzar en el sistema sin producir evidencia.**
> **La conversación es el medio, no el fin. El fin es la acción demostrable.**

**Tipos de Acciones Obligatorias (por Naturaleza):**

| Tipo | Definición | Ejemplo Cura | Ejemplo Constructor | Ejemplo Estudiante |
|------|-----------|------------|-------------------|------------------|
| **A. Evidencia productiva** | Output tangible del objetivo | Sermón grabado, lista de visitas | Informe de avance, foto de obra | Examen resuelto, nota de lectura |
| **B. Evidencia de proceso** | Prueba de trabajo realizado | Agenda de encuentros, reflexión escrita | Parte diario, checklist de seguridad | Resumen de estudio, ejercicios |
| **C. Evidencia de decisión** | Commitment irreversible | Compromiso escrito con fecha | Firma de contrato, orden de compra | Inscripción a examen, entrega de borrador |
| **D. Evidencia de respuesta** | Reacción obligatoria al sistema | Responder check-in, justificar inactividad | Reportar bloqueo en 24h | Confirmar recepción de tarea |

**Acciones Obligatorias por Fase del Flujo:**

```
┌─────────────────────────────────────────────────────────────┐
│  FASE 0: ENTRADA                                             │
│  Acciones obligatorias:                                      │
│  • A1. Declarar objetivo en formato EMT                      │
│  • A2. Negociar señales de estancamiento                     │
│  • A3. Confirmar comprensión                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 1-2: UBICACIÓN Y MODELADO                              │
│  Acciones obligatorias:                                      │
│  • A4. Responder diagnóstico                                 │
│  • A5. Validar modelo que construye la IA                    │
│  • A6. Declarar recursos disponibles                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: CONDUCCIÓN (LOOP PRINCIPAL)                       │
│  Acciones obligatorias por iteración:                        │
│  • A7. Seleccionar o proponer siguiente paso               │
│  • A8. Establecer fecha de entrega de micro-evidencia         │
│  • A9. Producir y presentar evidencia en fecha acordada      │
│  • A10. Si no hay evidencia: justificar en 24h              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 4: PRESIÓN ESTRATÉGICA                                 │
│  Acciones obligatorias:                                      │
│  • A11. Responder a intervención de estancamiento            │
│  • A12. Elegir: aceptar cambio / negociar / supervisión      │
│  • A13. Si supervisión: cumplir check-ins programados        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 5-6: EJECUCIÓN Y CIERRE                                │
│  Acciones obligatorias:                                      │
│  • A14. Presentar evidencia final de logro                   │
│  • A15. Validar cierre                                       │
│  • A16. Si no alcanzado: definir nuevo objetivo              │
└─────────────────────────────────────────────────────────────┘
```

**Reglas de Bloqueo (No se puede pasar sin...):**

| Si falta esta acción... | El sistema... | Usuario puede... |
|------------------------|-------------|----------------|
| A1 (Objetivo EMT) | No inicia. Rechaza entrada. | Reintentar con formato correcto |
| A3 (Confirmar comprensión) | Pide de nuevo. No avanza. | Confirmar o salir del sistema |
| A7-A10 (Loop conducción) | **Bloqueo total**. No hay próximo paso. | Producir evidencia / Justificar |
| A11-A13 (Presión) | Escalación automática de agresividad. | Responder o entrar supervisión aguda forzada |
| A14-A16 (Cierre) | Objetivo permanece "abierto" indefinidamente. | Cerrar o ser cerrado por sistema tras 30 días |

**Estructura de Datos de una Acción Obligatoria:**

```json
{
  "action_id": "A7",
  "name": "Seleccionar siguiente paso",
  "phase": "conduccion",
  "nature": "productiva|proceso|decision|respuesta",
  "mandatory": true,
  "skippable": false,
  "has_default": false,
  "blocking": true,
  "evidence_required": false,
  "response_format": "selection+comment",
  "time_limit": null,
  "consequence_if_missing": "signal_S05_triggered",
  "negotiable": false
}
```

**Relación con otros documentos:**
- → `ListaRequerimientos.md` → Punto 7 (Arquitectura de Memoria Permanente)
- → `requerimientos.md` → Estado de Éxito (Sección 4)

---

# ⚙️ CAPA 3: ESPECIFICACIONES TÉCNICAS

> **PRINCIPIO RECTOR:** "Pragmatismo radical - Navaja suiza, no catedral"

## 3.1 ARQUITECTURA TECNOLÓGICA COMPLETA

**Ubicación:** `proyecto.md` → Arquitectura Tecnológica | `requerimientos.md` → Diagrama de Todo el Sistema

**Propósito:** Describir el stack tecnológico y cómo se conectan las piezas.

**Diagrama de Capas del Sistema:**

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 0 — ACTORES EXTERNOS                                      │
│  • Usuario                                                      │
│  • Humano supervisor                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 1 — INTERFAZ DE ACCESO                                    │
│  • UI Principal (Next.js 14 + React 18)                         │
│  • Modo Chat / Cuestionario / Mixto                             │
│  • Selector de Modo                                             │
│  • Input: Botones + Comentario libre multilinea                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 2 — ORQUESTACIÓN COGNITIVA                                │
│  • Orquestador Central                                          │
│  • Detector de Intención                                        │
│  • Extractor de Objetivo (EMT)                                  │
│  • Estado de Sesión                                             │
│  • Router de Flujo                                              │
│  • Decisor de Modalidad (chat/cuestionario/mixto)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 3 — GOBERNANZA Y CONTROL                                  │
│  • Ejecutor LLM (DeepSeek API)                                  │
│  • Arquitecto / Capa de Control                                 │
│  • Calculador de Deriva (Delta 0-1)                             │
│  • Umbral de Cambio (default 0.3)                               │
│  • Motor de Aprobación                                          │
│  • Bloqueo de Cambios Bruscos                                   │
│  • Negociación con Usuario                                      │
│  • Auditoría de Decisiones                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 4 — MEMORIA, PERFIL Y CONTEXTO                            │
│  • Memoria Permanente de Objetivos                              │
│  • Perfil del Usuario                                           │
│  • Recuperación Contextual (RAG)                                │
│  • Resumen de Historial (semantic chunking)                     │
│  • Banco de Cuestionarios                                       │
│  • Reglas de Inferencia                                         │
│  • Plantillas por Dominio                                       │
│  • Registro de Evidencia                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 5 — DATOS Y PERSISTENCIA                                  │
│  • users, sessions, objectives, profiles                        │
│  • questionnaires, questions, answers                           │
│  • evidence, delta_logs, prompt_versions                        │
│  • stall_signals, checkins, memory_chunks, audit_log            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 6 — ACCIÓN Y CIERRE                                       │
│  • Próximo Paso                                                 │
│  • Tarea / Microtarea                                           │
│  • Check-in                                                     │
│  • Estado de Éxito                                              │
│  • Estado de Estancamiento                                      │
│  • Recalibración                                                │
└─────────────────────────────────────────────────────────────────┘
```

**Stack Tecnológico Detallado:**

| Capa | Tecnología | Versión | Propósito |
|------|-----------|---------|-----------|
| **Frontend** | Next.js | 14 (App Router) | SSR, routing, estructura de páginas |
| **Frontend** | React | 18 | Componentes UI |
| **Frontend** | TypeScript | 5.7+ | Type safety |
| **Frontend** | Tailwind CSS | 3.x | Estilos, glassmorphism |
| **Frontend** | Framer Motion | 10.x | Animaciones spring physics |
| **Frontend** | Zustand | 4.x | Estado global con persistencia |
| **Backend** | Node.js | 18+ | Runtime |
| **Backend** | Express | 4.x | Servidor HTTP |
| **Backend** | Socket.IO | 4.x | Comunicación en tiempo real |
| **Backend** | DeepSeek API | v3 | Motor de inferencia (vía OpenRouter) |
| **Datos** | Memoria (inicial) | - | Sesiones, objetivos |
| **Datos** | Redis (producción) | - | Persistencia escalable |
| **Datos** | PostgreSQL (opcional) | - | Datos estructurados (users, objectives) |

**Relación con otros documentos:**
- → `rutas.md` → Estructura de Carpetas
- → `METODOLOGIA-MODULAR.md` → Patrones Arquitectónicos

---

## 3.2 SISTEMA DE MODOS: CHAT, CUESTIONARIO, MIXTO

**Ubicación:** `requerimientos.md` → Sección 7 (líneas 1500-1650)

**Propósito:** Explicar CÓMO el sistema decide qué interfaz mostrar.

**Regla de Decisión de Modalidad:**

```
┌─────────────────────────────────────────────────────────┐
│  ORQUESTADOR evalúa estado actual                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
         ¿Qué falta saber?
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
   Objetivo         Faltan datos     Alta
   nuevo/ambiguo    críticos         complejidad
         │                │                │
         │                │                │
         ▼                ▼                ▼
   ┌──────────┐    ┌──────────┐    ┌──────────┐
   │ MODO     │    │ MODO     │    │ MODO     │
   │CUESTIONA-│    │CUESTIONA-│    │ MIXTO    │
   │RIO       │    │RIO       │    │          │
   └──────────┘    └──────────┘    └──────────┘
```

**Modo Cuestionario - Cuándo Activar:**

| Condición | Ejemplo | Tipo de Pregunta |
|-----------|---------|------------------|
| Objetivo nuevo | Usuario acaba de declarar objetivo | Selección múltiple para clasificar dominio |
| Faltan datos críticos | No se sabe estado actual | Sí/No o Verdadero/Falso para validar hipótesis |
| Necesita clasificación | ¿Qué tipo de profesional eres? | Selección única |
| Se necesita contexto rico | ¿Qué obstáculos has intentado? | Selección múltiple + comentario |

**Modo Chat - Cuándo Activar:**

| Condición | Ejemplo | Tipo de Interacción |
|-----------|---------|---------------------|
| Usuario confuso | "No sé por dónde empezar" | Pregunta abierta exploratoria |
| Resistencia emocional | "Esto es muy difícil para mí" | Validación humanista + pregunta suave |
| Ya hay contexto suficiente | Sistema tiene modelo completo | Diálogo fluido para avanzar |
| Negociación requerida | Delta alto detectado | Explicación + solicitud de aprobación |

**Modo Mixto - Cuándo Activar:**

| Condición | Ejemplo | Secuencia |
|-----------|---------|-----------|
| Diagnóstico + matiz | "¿Cuál es tu situación? [opciones] + cuéntame más" | 1. Pregunta cerrada → 2. Comentario libre |
| Validación + exploración | "¿Es esto correcto? [Sí/No] + ¿qué falta?" | 1. Validación → 2. Apertura |
| Estructura + emoción | "Selecciona tu bloqueo principal + ¿cómo te hace sentir?" | 1. Clasificación → 2. Emoción |

**Algoritmo de Inferencia por Tipo de Pregunta:**

```
┌─────────────────────────────────────────────────────────┐
│  Entrada de necesidad de información                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
         ¿Qué tipo de dato falta?
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
    ▼                     ▼                     ▼
Dato binario       Una opción          Varias opciones
(Sí/No)            única               válidas
    │                     │                     │
    ▼                     ▼                     ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│ Pregunta │        │Selección │        │Selección │
│ Sí/No    │        │  Única   │        │ Múltiple │
└──────────┘        └──────────┘        └──────────┘
    │                     │                     │
    └─────────────────────┼─────────────────────┘
                          │
                          ▼
         ¿Faltan más campos críticos?
                          │
                    ┌─────┴─────┐
                    │           │
                   SÍ          NO
                    │           │
                    ▼           ▼
              Repetir    Actualizar estado
              desde inicio
```

**Relación con otros documentos:**
- → `ListaRequerimientos.md` → Punto 6 (Interfaz Híbrida de Selección)
- → `requerimientos.md` → Diagrama de Todo el Sistema (Capa 1)

---

## 3.3 ESQUEMA DE BASE DE DATOS COMPLETO

**Ubicación:** `requerimientos.md` → Sección 7, Subsección ERD (líneas 1650-1763)

**Propósito:** Definir todas las entidades necesarias y sus relaciones.

**Diagrama Entidad-Relación:**

```
USERS ||--o{ SESSIONS : has
USERS ||--o{ OBJECTIVES : defines
USERS ||--o{ PROFILES : has
USERS ||--o{ AUDIT_LOG : generates

SESSIONS ||--o{ PROMPT_VERSIONS : stores
SESSIONS ||--o{ ANSWERS : contains
SESSIONS ||--o{ DELTA_LOGS : records
SESSIONS ||--o{ CHECKINS : schedules
SESSIONS ||--o{ MEMORY_CHUNKS : compresses
SESSIONS ||--o{ STALL_SIGNALS : detects

OBJECTIVES ||--o{ EVIDENCE : requires
OBJECTIVES ||--o{ CHECKINS : drives
OBJECTIVES ||--o{ QUESTIONS : triggers

QUESTIONNAIRES ||--o{ QUESTIONS : includes
QUESTIONS ||--o{ ANSWERS : receives

PROFILES ||--o{ STALL_SIGNALS : customizes
PROFILES ||--o{ QUESTIONNAIRES : adapts

DELTA_LOGS }o--|| PROMPT_VERSIONS : compares
MEMORY_CHUNKS }o--|| SESSIONS : summarizes
```

**Entidades Detalladas:**

```json
// USERS
{
  "id": "uuid",
  "name": "string",
  "locale": "string",
  "created_at": "datetime"
}

// OBJECTIVES
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "string",
  "domain": "string",
  "status": "pending|active|completed|abandoned",
  "deadline": "date",
  "success_criteria": {
    "evidence": "string",
    "metric": "string",
    "time": "date"
  }
}

// PROFILES
{
  "id": "uuid",
  "user_id": "uuid",
  "preferences": "json",
  "constraints": "json",
  "stall_thresholds": "json",
  "modality_bias": "json",
  "biological_profile": {
    "chronotype": "lark|owl|intermediate",
    "peak_hours": ["14:00-17:00"],
    "sleep_average": 6.5,
    "exercise_pattern": "sedentary|moderate|active",
    "stress_baseline": "low|medium|high"
  }
}

// SESSIONS
{
  "id": "uuid",
  "user_id": "uuid",
  "active_mode": "chat|questionnaire|mixed",
  "context_snapshot": "json",
  "started_at": "datetime",
  "updated_at": "datetime"
}

// QUESTIONNAIRES
{
  "id": "uuid",
  "objective_type": "string",
  "stage": "entrada|ubicacion|modelado|conduccion|presion|cierre",
  "schema": "json",
  "trigger_rule": "string"
}

// QUESTIONS
{
  "id": "uuid",
  "questionnaire_id": "uuid",
  "question_type": "yesno|truefalse|single_choice|multi_choice|completion|multiline|ranking",
  "prompt": "string",
  "options": "json",
  "required": "boolean",
  "field_key": "string"
}

// ANSWERS
{
  "id": "uuid",
  "session_id": "uuid",
  "question_id": "uuid",
  "value": "json",
  "confidence": "low|medium|high",
  "answered_at": "datetime"
}

// PROMPT_VERSIONS
{
  "id": "uuid",
  "session_id": "uuid",
  "version_hash": "string",
  "prompt_state": "json",
  "delta_score": "decimal",
  "approved": "boolean"
}

// DELTA_LOGS
{
  "id": "uuid",
  "session_id": "uuid",
  "from_prompt_version": "uuid",
  "to_prompt_version": "uuid",
  "delta_score": "decimal",
  "reason": "string",
  "needs_approval": "boolean"
}

// EVIDENCE
{
  "id": "uuid",
  "objective_id": "uuid",
  "evidence_type": "document|temporal_record|external_confirmation|self_report|physical_product",
  "uri": "string",
  "metadata": "json",
  "submitted_at": "datetime"
}

// STALL_SIGNALS
{
  "id": "uuid",
  "session_id": "uuid",
  "signal_code": "S01|S02|...|S12",
  "severity": "leve|grave|critico",
  "score": "decimal",
  "active": "boolean"
}

// CHECKINS
{
  "id": "uuid",
  "objective_id": "uuid",
  "due_at": "datetime",
  "status": "pending|completed|missed",
  "expected_evidence": "json"
}

// MEMORY_CHUNKS
{
  "id": "uuid",
  "session_id": "uuid",
  "chunk_type": "objective_summary|user_profile|key_insight|action_plan",
  "content": "text",
  "embedding_ref": "json"
}

// AUDIT_LOG
{
  "id": "uuid",
  "user_id": "uuid",
  "event_type": "prompt_change|stall_intervention|mode_switch|evidence_submitted",
  "payload": "json",
  "created_at": "datetime"
}
```

**Relación con otros documentos:**
- → `requerimientos.md` → Entidades Base de Datos (diagrama ERD)
- → `rutas.md` → Backend (types/socket.ts)

---

# 🛡️ CAPA 4: PROTOCOLOS DE CONTROL ANTI-ENTROPÍA

> **PRINCIPIO RECTOR:** "La IA no puede cambiar el prompt por cambiar"

## 4.1 SISTEMA DE DELTA CALCULATOR

**Ubicación:** `ListaRequerimientos.md` → Punto 12 | `requerimientos.md` → Capa 3: Gobernanza

**Propósito:** Medir CUÁNTO cambia el prompt para decidir si se aprueba.

**Algoritmo de Cálculo de Delta:**

```python
def calculate_delta(old_prompt: str, new_prompt: str) -> float:
    """
    Calcula score de deriva semántica entre dos prompts.
    Retorna valor entre 0 (idéntico) y 1 (completamente diferente).
    """
    # Paso 1: Tokenización y normalización
    old_tokens = tokenize_and_normalize(old_prompt)
    new_tokens = tokenize_and_normalize(new_prompt)
    
    # Paso 2: Calcular similitud léxica (Jaccard)
    lexical_similarity = jaccard_similarity(old_tokens, new_tokens)
    
    # Paso 3: Calcular similitud semántica (embeddings)
    old_embedding = get_embedding(old_prompt)
    new_embedding = get_embedding(new_prompt)
    semantic_similarity = cosine_similarity(old_embedding, new_embedding)
    
    # Paso 4: Combinar (peso 40% léxico, 60% semántico)
    combined_similarity = (0.4 * lexical_similarity) + (0.6 * semantic_similarity)
    
    # Paso 5: Convertir a delta (1 - similitud)
    delta_score = 1 - combined_similarity
    
    return round(delta_score, 3)
```

**Umbrales de Delta:**

| Delta Score | Interpretación | Acción Requerida |
|-------------|----------------|------------------|
| 0.0 - 0.1 | Micro-ajuste | Aceptación automática |
| 0.1 - 0.3 | Ajuste moderado | Aceptación con logging |
| 0.3 - 0.6 | Cambio significativo | Aprobación de usuario requerida |
| 0.6 - 0.8 | Reestructuración | Arquitecto evalúa + negociación |
| 0.8 - 1.0 | Cambio radical | **Veto automático** + recalibración |

**Ejemplo de Flujo con Delta:**

```
Prompt original: "Eres un asesor de productividad que ayuda a usuarios a definir objetivos SMART"

Usuario responde: "Quiero ser más productivo pero me distraigo mucho"

Prompt propuesto por Ejecutor: "Eres un coach de enfoque que ayuda a usuarios con problemas de distracción a mantener atención en objetivos de corto plazo"

Delta Calculator:
  - Léxico: 60% similar (palabras diferentes pero tema relacionado)
  - Semántico: 70% similar (cambio de "productividad" a "enfoque")
  - Delta: 0.35

Resultado: Delta > 0.3 → Requiere aprobación de usuario

Sistema pregunta: "Para ayudarte mejor, propongo ajustar mi enfoque de 'productividad general' a 'enfoque y distracción'. ¿Te parece bien?"

Usuario: "Sí, exacto, ese es mi problema"

→ Cambio aceptado, logging actualizado
```

**Relación con otros documentos:**
- → `ListaRequerimientos.md` → Punto 8 (Sistema de Doble Instancia)
- → `requerimientos.md` → Capa 3: Gobernanza

---

## 4.2 FILTRO DE MERE CIMIENTO DEL CAMBIO

**Ubicación:** `ListaRequerimientos.md` → Punto 4.2, 5.3 | `requerimientos.md` → Sección 5

**Propósito:** Evaluar si un cambio de prompt **realmente merece ser hecho**, más allá del delta numérico.

**Criterios del Filtro de Merecimiento:**

| Criterio | Pregunta | Si NO → |
|----------|----------|---------|
| **Alineación con objetivo** | ¿El cambio acerca al usuario a su objetivo EMT? | Rechazar |
| **Consistencia con historial** | ¿El cambio contradice algo establecido previamente? | Solicitar justificación |
| **Viabilidad biológica** | ¿El cambio considera perfil biológico del usuario? | Ajustar o rechazar |
| **Proporcionalidad** | ¿El cambio es proporcional al input del usuario? | Si es desproporcionado → rechazar |
| **Reversibilidad** | ¿El cambio se puede deshacer fácilmente si falla? | Si no es reversible → mayor escrutinio |

**Algoritmo del Filtro:**

```python
def merecimiento_filter(proposed_change, context) -> dict:
    """
    Evalúa si un cambio de prompt merece ser hecho.
    """
    score = 0
    reasons = []
    
    # Criterio 1: Alineación con objetivo
    if aligns_with_objective(proposed_change, context.objective):
        score += 2
        reasons.append("Alineado con objetivo")
    else:
        reasons.append("Desalineado con objetivo")
        return {"approved": False, "reason": "No alinea con objetivo EMT"}
    
    # Criterio 2: Consistencia con historial
    if consistent_with_history(proposed_change, context.history):
        score += 1
        reasons.append("Consistente con historial")
    else:
        score -= 1
        reasons.append("Inconsistente con historial - requiere justificación")
    
    # Criterio 3: Viabilidad biológica
    if biologically_viable(proposed_change, context.biological_profile):
        score += 1
        reasons.append("Viable biológicamente")
    else:
        score -= 2
        reasons.append("Ignora perfil biológico - ajustar")
    
    # Criterio 4: Proporcionalidad
    if proportional_to_input(proposed_change, context.user_input):
        score += 1
        reasons.append("Proporcional al input")
    else:
        score -= 1
        reasons.append("Desproporcionado")
    
    # Decisión
    if score >= 3:
        return {"approved": True, "reasons": reasons}
    elif score >= 1:
        return {"approved": "negotiate", "reasons": reasons}
    else:
        return {"approved": False, "reasons": reasons}
```

**Ejemplo de Aplicación:**

```
Contexto:
  - Objetivo EMT: "Publicar 1 video semanal de YouTube durante 3 meses"
  - Historial: Usuario ha fallado 2 veces por "falta de tiempo"
  - Perfil biológico: Cronotipo owl, pico cognitivo 16:00-20:00

Propuesta del Ejecutor:
  "Cambia el objetivo a: Publicar 3 videos semanales"

Filtro de Merecimiento:
  ❌ Alineación con objetivo: NO (cambia métrica sin justificación)
  ❌ Consistencia con historial: NO (ignora que ya falló con menos carga)
  ❌ Viabilidad biológica: NO (ignora cronotipo, 3 videos requeriría mañana temprano)
  ❌ Proporcionalidad: NO (desproporcionado al input)

Score: -4
Resultado: RECHAZADO

Respuesta al Ejecutor:
  "Cambio rechazado. Razones:
   1. Cambia métrica sin justificación del usuario
   2. Ignora historial de fallos con carga menor
   3. No considera cronotipo owl del usuario
   4. Desproporcionado al input recibido"
```

**Relación con otros documentos:**
- → `ListaRequerimientos.md` → Punto 5 (Protocolo de Negociación)
- → `requerimientos.md` → Acciones Obligatorias (Sección 6)

---

## 4.3 PROTOCOLO DE SUPERVISIÓN AGUDA

**Ubicación:** `requerimientos.md` → Sección 5, Subsección 5 (líneas 1100-1150)

**Propósito:** Definir qué hacer cuando el usuario RESISTE el cierre forzado.

**Trigger de Activación:**

```
Usuario ha llegado a Nivel 4 de agresividad (Ultimátum)
    ↓
Usuario RECHAZA cierre forzado
    ↓
Sistema ofrece dos opciones:
  A) Cerrar objetivo y definir uno nuevo
  B) Entrar en MODO SUPERVISIÓN AGUDA
    ↓
Usuario elige B
    ↓
ACTIVAR PROTOCOLO DE SUPERVISIÓN AGUDA
```

**Características de Supervisión Aguda:**

| Característica | Descripción | Implementación |
|----------------|-------------|----------------|
| **Check-ins obligatorios** | Cada 24h, usuario DEBE reportar | Notificación push + bloqueo de otras funciones hasta responder |
| **Evidencia obligatoria** | Cada micro-tarea requiere prueba | No se acepta "ya lo hice" sin evidencia tangible |
| **Sin negociación de plazos** | Fechas son innegociables por 7 días | Sistema rechaza automáticamente peticiones de extensión |
| **Cierre automático** | Si falla 1 check-in o 1 evidencia → cierre | Ejecución automática, sin pregunta |
| **Duración máxima** | 7 días | Día 8: o hay avance demostrable o se cierra |

**Estructura de Datos:**

```json
{
  "aguda_mode": {
    "active": true,
    "started_at": "2026-03-19T10:00:00Z",
    "ends_at": "2026-03-26T10:00:00Z",
    "objective_id": "uuid",
    "checkins_required": [
      {"day": 1, "due": "2026-03-20T10:00:00Z", "status": "pending"},
      {"day": 2, "due": "2026-03-21T10:00:00Z", "status": "pending"},
      ...
      {"day": 7, "due": "2026-03-26T10:00:00Z", "status": "pending"}
    ],
    "evidence_required": [
      {"task": "micro-tarea-1", "due": "2026-03-20T23:59:59Z", "status": "pending"},
      {"task": "micro-tarea-2", "due": "2026-03-21T23:59:59Z", "status": "pending"},
      ...
    ],
    "failure_condition": "any_missed_checkin OR any_missed_evidence",
    "consequence_on_failure": "automatic_closure"
  }
}
```

**Flujo de Supervisión Aguda:**

```
DÍA 1:
  Sistema: "Check-in #1: ¿Completaste la micro-tarea de ayer? Sube evidencia."
  Usuario: [sube evidencia]
  Sistema: "Evidencia validada. Check-in #1 completado. Mañana: tarea #2."

DÍA 3:
  Sistema: "Check-in #3: ¿Completaste la micro-tarea? Sube evidencia."
  Usuario: [no responde en 24h]
  Sistema: "⚠️ Check-in #3 vencido. Tienes 2h para justificar."
  Usuario: [no justifica]
  Sistema: "❌ Supervisión aguda FALLIDA. Objetivo cerrado automáticamente."
  Sistema: "¿Quieres definir nuevo objetivo o tomar descanso?"
```

**Relación con otros documentos:**
- → `requerimientos.md` → Estado de Estancamiento (Sección 5)
- → `ListaRequerimientos.md` → Punto 8 (Sistema de Doble Instancia)

---

# 🧠 CAPA 5: MARCO TEÓRICO INTEGRADO

> **PRINCIPIO RECTOR:** "Bernays + Skinner + Rogers + Beck + Kahneman + Haidt + Neurociencia"

## 5.1 FUNDAMENTO BERNAYSIANO: INGENIERÍA DEL COMPROMISO

**Ubicación:** `requerimientos.md` → Sección 7, Subsección 1 (líneas 1450-1500)

**Propósito:** Explicar cómo el sistema guía sin coerción explícita.

**Principios Bernaysianos Aplicados:**

| Principio | Definición | Aplicación en el Sistema |
|-----------|------------|-------------------------|
| **Invisibilidad de la estructura** | Usuario siente que decide libremente, pero el espacio de opciones está diseñado | Ofrecer 3 rutas posibles, todas convergen al mismo output obligatorio |
| **Apelación a motivaciones inconscientes** | Las acciones se venden como aspiraciones, no deberes | "Quieres ser la persona que cumple" vs "Debes cumplir" |
| **Tercerización de la autoridad** | La obligación viene del "sistema" o "proceso", no de la IA | "El método requiere esta evidencia para funcionar" |
| **Ciclos de reforzamiento** | Cada acción genera satisfacción inmediata que valida la siguiente | Micro-recompensas por cada evidencia presentada |
| **Creación de hábitos como identidad** | Las acciones se vinculan a quién el usuario cree ser | "Los profesionales serios documentan su trabajo" |

**Clave Bernaysiana:**

> El usuario nunca debe sentirse *obligado* por un agente externo. Debe sentirse *guiado por su propia lógica* hacia conclusiones pre-plantadas.

**Ejemplo de Implementación:**

```
Sistema (opción bernaysiana):
  "Para avanzar, tienes tres caminos:
   
   A) Escribir la estructura hoy (20 min)
   B) Buscar referencias durante 30 min
   C) Proponer tu propia alternativa
   
   ¿Cuál eliges?"

Usuario: "La A"

Sistema:
  "Excelente elección. La estructura es la base de todo.
   ¿Para cuándo me muestras el resultado? Propongo 48h."

→ Usuario SIENTE que eligió, pero TODAS las opciones llevan a evidencia obligatoria
```

**Relación con otros documentos:**
- → `requerimientos.md` → Acciones Obligatorias (Sección 6)
- → `ListaRequerimientos.md` → Punto 1 (Directiva principal)

---

## 5.2 SÍNTESIS DE LAS TRES ESCUELAS PSICOLÓGICAS

**Ubicación:** `requerimientos.md` → Sección 7, Subsección 2 (líneas 1500-1600)

**Propósito:** Integrar conductismo, humanismo y cognitivismo en un solo sistema coherente.

**Conductismo (Skinner) - El Esqueleto:**

| Concepto | Aplicación | Ejemplo |
|----------|------------|---------|
| **Condicionamiento operante** | Comportamientos moldeados por consecuencias | Evidencia presentada = validación inmediata |
| **Reforzamiento ratio variable** | Refuerzo tras número impredecible de respuestas | Evidencias 1, 3, 7, 12 reciben "bonus sorpresa" |
| **Reforzamiento continuo (inicial)** | Instalar nuevo hábito rápidamente | Cada evidencia inicial recibe validación inmediata |
| **Castigo negativo** | Consecuencia de incumplimiento | Perder acceso a función premium tras 2 fallos |

**Regla conductista crítica:** Las acciones obligatorias deben tener **consecuencias inmediatas y predecibles**.

---

**Humanismo (Rogers) - El Corazón:**

| Concepto | Aplicación | Ejemplo |
|----------|------------|---------|
| **Autonomía estructurada** | Usuario elige *cómo* cumple, no *si* cumple | "Puedes entregar evidencia como audio, texto o video —tú decides" |
| **Congruencia con self ideal** | Acción obligatoria acerca al usuario a quién quiere ser | "Esta evidencia demuestra que eres el profesional sistemático que aspiras a ser" |
| **Empatía incondicional ante resistencia** | Cuando usuario falla, no hay juicio —hay curiosidad | "Veo que no entregaste. ¿Qué pasó realmente? ¿El obstáculo fue externo o interno?" |
| **Relación genuina** | IA se siente como aliada, no vigilante | "Estoy aquí para asegurarme de que no te abandones a ti mismo" |

**Paradoja humanista:** Cuanto más se respeta la autonomía, más efectiva es la obligación estructurada.

---

**Cognitivismo (Beck/Kahneman) - El Cerebro:**

| Concepto | Aplicación | Ejemplo |
|----------|------------|---------|
| **Distorsiones cognitivas (Beck)** | Intercepta excusas antes de que se solidifiquen | "No es 'no tengo tiempo', es 'no priorizo esto'" |
| **Reestructuración cognitiva** | Cambia marco mental del obstáculo | "¿Este obstáculo es real o es una creencia limitante?" |
| **Prospect Theory (Kahneman)** | Pérdidas percibidas 2.5x más potentes que ganancias | "Cada día sin avance es una pérdida de tu objetivo" |
| **Framing** | Cómo se presenta la opción afecta la decisión | ✅ "Al entregar, aseguras el avance" vs ❌ "Debes entregar o pierdes" |

---

**Integración de las Tres Escuelas:**

```
┌─────────────────────────────────────────────────────────┐
│              SISTEMA PSICOLÓGICO INTEGRADO              │
│                                                         │
│  CONDUCTISMO (30%) → Estructura, consecuencias, ritmo  │
│       +                                                   │
│  HUMANISMO (30%) → Autonomía, empatía, identidad       │
│       +                                                   │
│  COGNITIVISMO (40%) → Reestructuración, framing, sesgos│
│       =                                                   │
│  RESPUESTA COHERENTE (no 3 voces distintas)             │
└─────────────────────────────────────────────────────────┘
```

**Relación con otros documentos:**
- → `requerimientos.md` → Sistema de Intervención (3 Terapias)
- → `ListaRequerimientos.md` → Punto 13 (Adaptabilidad Multi-Dominio)

---

## 5.3 EQUILIBRIO EMOCIONAL: EL CÓCTEL MOTIVACIONAL

**Ubicación:** `requerimientos.md` → Sección 7, Subsección 3 (líneas 1600-1700)

**Propósito:** Definir el balance emocional óptimo por fase del sistema.

**Los 5 Componentes Emocionales:**

| Componente | Función | Dosis Óptima | Toxicidad (si excede) |
|-----------|---------|--------------|----------------------|
| **PLACER/DOPAMINA** | Reforzar acción completada | Micro-recompensas inmediatas | Adicción a recompensas externas |
| **MIEDO/PÉRDIDA** | Prevenir inacción | Recordatorio del costo de no actuar | Parálisis por ansiedad |
| **MOTIVACIÓN/PROPÓSITO** | Sostener en resistencia | Conexión constante con el "para qué" | Desgaste por idealismo distante |
| **CONEXIÓN/EMPATÍA** | Soportar esfuerzo difícil | Presencia de "acompañante" | Dependencia emocional |
| **AUTONOMÍA/AGENCIA** | Mantener ilusión de control | Elección dentro de estructura | Caos sin guía |

**Fórmula de Equilibrio por Fase:**

```
FASE 0 (Entrada):
  40% Placer (curiosidad) + 30% Motivación + 20% Autonomía + 10% Miedo

FASE 1-2 (Diagnóstico):
  30% Conexión + 30% Autonomía + 25% Motivación + 15% Placer

FASE 3 (Conducción):
  25% Placer + 25% Miedo (pérdida de foco) + 25% Motivación + 15% Conexión + 10% Autonomía

FASE 4 (Presión):
  30% Miedo + 25% Conexión (apoyo) + 20% Motivación + 15% Placer + 10% Autonomía

FASE 5-6 (Ejecución):
  35% Motivación + 25% Placer (celebración) + 20% Autonomía + 15% Conexión + 5% Miedo
```

**Regla de Oro:**

> Nunca más de 30% de miedo sin al menos 25% de conexión/empatía para compensar. El miedo solo motiva la huida; la conexión + miedo motiva el esfuerzo.

**Ejemplo de Implementación:**

```
FASE 4 (Presión Estratégica) - Usuario en resistencia:

Sistema (balance emocional):
  "Veo que llevas 5 días sin avanzar. (MIEDO: 30%)
   
   Esto es completamente normal. Muchos pasan por esto cuando
   el objetivo es importante. (CONEXIÓN: 25%)
   
   Recuerda por qué empezaste: querías [objetivo EMT].
   Eso sigue siendo válido. (MOTIVACIÓN: 20%)
   
   La buena noticia: has logrado cosas difíciles antes.
   (PLACER: recuerdo de éxito pasado, 15%)
   
   ¿Qué pequeña parte SÍ puedes hacer hoy? Tú decides el cómo.
   (AUTONOMÍA: 10%)"
```

**Relación con otros documentos:**
- → `requerimientos.md` → Enfoque Psicológico (Sección 4)
- → `ListaRequerimientos.md` → Punto 14 (Reducción de Fricción Cognitiva)

---

## 5.4 COMPONENTE BIOLÓGICO: EL HARDWARE SUBYACENTE

**Ubicación:** `requerimientos.md` → Sección 7, Subsección 4 (líneas 1700-1800)

**Propósito:** Adaptar el sistema a la fisiología real del usuario.

**Perfil Biológico del Usuario (Variables Registradas):**

| Variable | Indicador | Impacto en Acciones Obligatorias | Intervención del Sistema |
|----------|-----------|-------------------------------|-------------------------|
| **SUEÑO** | Horas, calidad, eficiencia | Privación reduce función PFC 23%, aumenta impulsividad | Ajustar dificultad de tareas; no pedir evidencias complejas tras noches malas |
| **GLUCOSA/ENERGÍA** | Momentos de ingesta, niveles estimados | Ayuno >3h reduce autocontrol significativamente | Programar acciones obligatorias post-comida; alertar si usuario "decide" en ayuno |
| **EJERCICIO/BDNF** | Frecuencia, intensidad, última sesión | Ejercicio aumenta BDNF, neuroplasticidad, función cognitiva | Sugerir micro-movimiento antes de tareas cognitivas difíciles |
| **CORTISOL/ESTRÉS** | HRV, autoreporte | Estrés crónico atrofia hipocampo, reduce memoria y decisión | Detectar "colapso" → reducir demandas, aumentar apoyo humanista |
| **CRONOTIPO** | Hora pico cognitiva (lark/owl/intermedio) | Trabajar contra cronotipo reduce rendimiento 30% | Programar acciones obligatorias "difíciles" en ventana pico individual |
| **CARGA COGNITIVA ACUMULADA** | Decisiones previas en día, "ego depletion" | Autocontrol es recurso finito que se agota | Limitar número de acciones obligatorias por sesión; espaciarlas |

**Estructura de Datos del Perfil Biológico:**

```json
{
  "user_biological_profile": {
    "chronotype": "owl",
    "peak_hours": ["16:00-20:00"],
    "sleep_average": 6.5,
    "sleep_quality": "variable",
    "exercise_pattern": "moderate",
    "stress_baseline": "medium",
    "glucose_rhythm": "regular"
  },
  "action_scheduling_algorithm": {
    "hard_actions": "peak_hours_only",
    "easy_actions": "off_peak_flexible",
    "mandatory_check_ins": "avoid_sleep_deprived_periods",
    "evidence_deadlines": "account_for_chronotype",
    "stress_override": "if_cortisol_high → reduce_difficulty_40%"
  }
}
```

**Señales Biológicas de Riesgo (Detección Automática):**

| Señal | Umbral | Acción del Sistema |
|-------|--------|-------------------|
| Respuestas entre 2-6 AM (cronotipo lark) | >1 vez/semana | Alerta: "Tu patrón sugiere desalineación. ¿Ajustamos horarios?" |
| Tiempo de respuesta >3x tu media | Hoy | "Detecto fatiga cognitiva. ¿Micro-pausa de 5 min antes de continuar?" |
| Keywords: "agotado", "no puedo pensar", "mareo" | 2+ por sesión | Activar modo "supervisión aguda reducida": solo acciones mínimas |
| Patrón: evidencia de calidad decreciente | 3 entregas consecutivas | "Tu evidencia muestra signos de agotamiento. Opción A: Pausa recuperación. Opción B: Tarea más pequeña. Opción C: Hablar con supervisor humano." |

**Principio Rector:**

> Las acciones obligatorias deben ser **exigentes pero biológicamente viables**. Un sistema que ignora la fisiología produce culpa, no cambio.

**Relación con otros documentos:**
- → `requerimientos.md` → Acciones Obligatorias (Sección 6)
- → `ListaRequerimientos.md` → Punto 11 (Optimización para Entornos Restringidos)

---

# 🔗 CAPA 6: REFERENCIAS CRUZADAS Y NAVEGACIÓN

> **PRINCIPIO RECTOR:** "Todo está conectado - ninguna modificación es aislada"

## 6.1 MAPA DE DEPENDENCIAS ENTRE DOCUMENTOS

```
┌─────────────────────────────────────────────────────────────────┐
│                    JERARQUÍA DE DOCUMENTOS                       │
└─────────────────────────────────────────────────────────────────┘

NIVEL 1 (Fundamentos - leer primero):
├── ListaRequerimientos.md (27 puntos filosóficos)
├── requerimientos.md (Análisis profundo de intenciones)
└── proyecto.md (Visión general y arquitectura)

NIVEL 2 (Metodología - cómo trabajar):
├── METODOLOGIA-MODULAR.md (Patrones arquitectónicos)
└── INDICE-MAESTRO-PARA-IAS.md (este documento)

NIVEL 3 (Implementación - detalles técnicos):
├── rutas.md (Dónde está cada archivo)
├── DISENO/Maestro.md (Sistema de coordenadas UI)
└── estado.md (Estado actual de implementación)

NIVEL 4 (Referencia - consultar según necesidad):
├── AUDITORIA-CAPACIDADES.md (16 capacidades discretas)
├── CHANGELOG-MODULAR.md (Historial de cambios)
├── MIGRACION-COMPLETADA.md (Proceso de migración)
└── sistema-por-kimi.md (Diseño detallado de interfaz)
```

## 6.2 TABLA DE BÚSQUEDA RÁPIDA POR TEMA

| Si necesitas información sobre... | Ve a este documento | Sección específica |
|----------------------------------|---------------------|-------------------|
| **Filosofía Google Lens** | `ListaRequerimientos.md` | Punto 1 |
| **Prompt vivo y mutante** | `ListaRequerimientos.md` | Punto 4 |
| **Delta calculator** | `ListaRequerimientos.md` | Punto 12 |
| **Doble instancia (Arquitecto+Ejecutor)** | `ListaRequerimientos.md` | Punto 8 |
| **Interfaz híbrida (botones+comentario)** | `ListaRequerimientos.md` | Punto 6 |
| **Memoria permanente de objetivos** | `ListaRequerimientos.md` | Punto 7 |
| **Flujo ideal del usuario (6 fases)** | `requerimientos.md` | Sección 3 |
| **Estado de éxito (EMT)** | `requerimientos.md` | Sección 4 |
| **Estado de estancamiento (12 señales)** | `requerimientos.md` | Sección 5 |
| **Acciones obligatorias** | `requerimientos.md` | Sección 6 |
| **Marco teórico psicológico** | `requerimientos.md` | Sección 7 |
| **Diagrama de todo el sistema** | `requerimientos.md` | Sección 7 (final) |
| **Patrones arquitectónicos (MCP, RAG, etc.)** | `METODOLOGIA-MODULAR.md` | Patrones 1-6 |
| **Estructura de carpetas** | `rutas.md` | Estructura |
| **Sistema de diseño (glassmorphism)** | `proyecto.md` | Características Clave 3 |
| **Componentes de UI** | `DISENO/Maestro.md` | Jerarquía 3 |

## 6.3 ORDEN DE LECTURA RECOMENDADO PARA IAS

**Escenario A: IA nueva que empieza a trabajar en el proyecto**

```
Día 1:
  1. INDICE-MAESTRO-PARA-IAS.md (este documento) - Vista de pájaro
  2. ListaRequerimientos.md - Puntos 1, 2, 4, 5, 6, 7, 8, 12
  3. requerimientos.md - Secciones 1, 2, 3

Día 2:
  4. requerimientos.md - Secciones 4, 5, 6
  5. METODOLOGIA-MODULAR.md - Patrones 1, 2, 3, 5
  6. proyecto.md - Arquitectura y Características Clave

Día 3:
  7. rutas.md - Para entender dónde está cada cosa
  8. DISENO/Maestro.md - Si va a trabajar en UI
  9. estado.md - Para saber qué falta implementar
```

**Escenario B: IA que va a modificar un módulo específico**

```
1. INDICE-MAESTRO-PARA-IAS.md - Buscar tema en Tabla de Búsqueda Rápida
2. Leer documento referido en "Relación con otros documentos"
3. Leer METODOLOGIA-MODULAR.md - Reglas de comentarios y INDEX.md
4. Implementar cambio
5. Validar con git diff que no rompe otros módulos
```

**Escenario C: IA que va a hacer refactorización grande**

```
1. INDICE-MAESTRO-PARA-IAS.md - Capa 0 y Capa 1 (Fundamentos + Arquitectura)
2. ListaRequerimientos.md - Puntos críticos (1, 4, 5, 8, 12)
3. requerimientos.md - Secciones 1, 2, 3 (intenciones y flujo)
4. METODOLOGIA-MODULAR.md - Patrones arquitectónicos completos
5. Consultar con usuario antes de proceder
6. Implementar en fases pequeñas con validación después de cada una
```

---

# 📝 APÉNDICE: CHECKLIST DE VALIDACIÓN ANTES DE COMMIT

> **PRINCIPIO RECTOR:** "Ningún cambio es válido si rompe la coherencia del sistema"

## Checklist de 10 Puntos

Antes de hacer commit de cualquier cambio, la IA DEBE verificar:

```
□ 1. ¿El cambio respeta la filosofía Google Lens? (utilidad/esfuerzo)
□ 2. ¿El cambio mantiene la separación Ejecutor/Arquitecto?
□ 3. ¿El cambio preserva la memoria permanente de objetivos?
□ 4. ¿El cambio incluye cálculo de delta si modifica el prompt?
□ 5. ¿El cambio considera las 12 señales de estancamiento?
□ 6. ¿El cambio respeta las acciones obligatorias del usuario?
□ 7. ¿El cambio integra las 3 terapias (conductista, cognitiva, humanista)?
□ 8. ¿El cambio considera el perfil biológico del usuario?
□ 9. ¿El cambio sigue la metodología modular (1-3 funciones por módulo)?
□ 10. ¿El cambio actualiza INDEX.md y manifest.json del módulo?
```

**Si alguna respuesta es NO:**

- Detener implementación
- Releer sección relevante de este índice
- Consultar con usuario si es cambio estructural grande
- Ajustar implementación

---

## 🎯 DECLARACIÓN FINAL DE PROPÓSITO

Este **Índice Maestro para IAs** existe para una razón:

> **Evitar que la entropía destruya la coherencia del sistema.**

Cada IA que trabaje en este proyecto debe salir con **más claridad** de la que entró. Si este documento logra eso, habrá cumplido su propósito.

---

**Documento creado:** 2026-03-19  
**Ubicación:** `/home/daniel/tron/programas/TR/docs/AgenteDeCambio/ARQUITECTURA-NUEVA/INDICE-MAESTRO-PARA-IAS.md`  
**Versión:** 1.0  
**Próxima revisión:** Después de primera implementación completa

---

*Fin del Índice Maestro*

# Sacar el maximo partido y jugo a Google Gemma



## Introduccion

Recopilacion de varias fuentes de documentacion oficial y de programadores y repositorios de GitHub de como savcar el mejor partido posible a google gemma










## Diagrama de flujo del sistema:


```
---
config:
  layout: fixed
  look: neo
  theme: redux-dark
---
flowchart TB
    Start(["Usuario interactúa con<br>la interfaz del Chatbot"]) --> Process1["El Chatbot usa Gemma3<br>localmente vía Ollama"]
    Process1 --> Decision{"¿Se necesita llamar<br>a una función?"}
    Decision -- No --> Internal["Usar conocimiento<br>interno del LLM"]
    Internal --> FinalEnd(["Respuesta Final<br>al Usuario"])
    Decision -- Sí --> Router["Elegir una función<br>dinámicamente"]
    Note1["Basado en tipo de consulta:<br>Búsqueda / Traducción / Clima o cualquier otra herramientaprogramada. Tiene un indice de herramientas para consultar en vivo la herramienta adecuada."] -.-> Router
    Router -- google_search() salida el LLM estructurada --> SERP["Búsqueda en tiempo real<br>usando herramienta o API"]
    Router -- translate_text() salida el LLM estructurada --> TRANS["Traducción usando<br>herramienta API"]
    Router -- get_weather() salida el LLM estructurada --> WEATH["Clima usando<br>OpenWeatherMap"]
    SERP --> ProcessOut["Obtener Salida (JSON)<br>y Procesar (Formato PNL)"]
    TRANS --> ProcessOut
    WEATH --> ProcessOut
    ProcessOut --> FinalEnd2(["Respuesta Final<br>al Usuario"])

     Start:::darkBlue
     Process1:::blueFill
     Decision:::greyFill
     Internal:::blueFill
     FinalEnd:::greenFill
     Router:::blueFill
     Note1:::noteFill
     SERP:::purpleFill
     TRANS:::lightGreenFill
     WEATH:::redFill
     ProcessOut:::blueFill
     FinalEnd2:::greenFill
    classDef blueFill fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a
    classDef darkBlue fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:white
    classDef greenFill fill:#10b981,stroke:#059669,stroke-width:2px,color:white
    classDef lightGreenFill fill:#d1fae5,stroke:#10b981,stroke-width:2px,color:#064e3b
    classDef purpleFill fill:#e9d5ff,stroke:#a855f7,stroke-width:2px,color:#581c87
    classDef redFill fill:#fecaca,stroke:#ef4444,stroke-width:2px,color:#7f1d1d
    classDef greyFill fill:#f3f4f6,stroke:#9ca3af,stroke-width:2px,color:#374151
    classDef noteFill fill:#fef08a,stroke:#eab308,stroke-width:1px,color:#854d0e,stroke-dasharray: 5 5


```




## Llamadas dinámicas multifuncionales locales con Gemma 3 + Ollama – Recorrido completo de la demo

https://www.reddit.com/r/ollama/comments/1kadwr3/dynamic_multifunction_calling_locally_with_gemma/?tl=es-419

¡Hola a todos! 👋

Recientemente trabajé en **llamadas de funciones dinámicas** usando **Gemma 3 (1B)** funcionando **localmente** vía **Ollama** — permitiendo que el LLM **dispare búsquedas, traducciones y recuperación del clima en tiempo real** dinámicamente basado en la entrada del usuario.

**Video Demo:**

0:01 / 0:50

**Diagrama de flujo de llamadas de funciones dinámicas:**

[![r/ollama - Llamadas dinámicas multifuncionales locales con Gemma 3 + Ollama – Recorrido completo de la demo](https://preview.redd.it/dynamic-multi-function-calling-locally-with-gemma-3-ollama-v0-v07jd81ivoxe1.png?width=959&format=png&auto=webp&s=64c255f1ce1bca6ba4bd882c6aa61526cc75b099)](https://preview.redd.it/dynamic-multi-function-calling-locally-with-gemma-3-ollama-v0-v07jd81ivoxe1.png?width=959&format=png&auto=webp&s=64c255f1ce1bca6ba4bd882c6aa61526cc75b099 "Imagen de r/ollama - Llamadas dinámicas multifuncionales locales con Gemma 3 + Ollama – Recorrido completo de la demo")

En lugar de solo responder desde la memoria, el modelo decide inteligentemente cuándo:

🔍 Realizar una **búsqueda en Google** (usando la API de[Serper.dev](http://serper.dev/)) 🌐 **Traducir texto** en vivo (usando la API de MyMemory) ⛅ **Obtener el clima** en tiempo real (usando la API de OpenWeatherMap) 🧠 **Responder directamente** si la memoria interna es suficiente

¡Esto muestra cómo las **llamadas de funciones estructuradas** pueden hacer que los LLM locales sean más inteligentes y mucho más flexibles!

💡 **Puntos clave**: ✅ Llamadas a funciones con estructura JSON para invocación segura de herramientas externas ✅ Arquitectura local-first — sin inferencia de LLM en la nube ✅ La combinación Ollama + Gemma 3 1B funciona genial incluso en hardware modesto ✅ Totalmente modular — fácil de conectar más herramientas más allá de búsqueda, traducción, clima

🛠 **Tecnologías usadas**: ⚡[Gemma 3 (1B)](https://ollama.com/library/gemma3:1b)vía **Ollama** ⚡ **Gradio** (Interfaz de chatbot) ⚡[**Serper.dev**](http://serper.dev/)**API** (Búsqueda) ⚡ **API de MyMemory** (Traducción) ⚡ **API de OpenWeatherMap** (Clima) ⚡ **Pydantic + Python** (Análisis y validación de funciones)

📌 **Blog completo + recorrido completo del código:**[sridhartech.hashnode.dev/dynamic-multi-function-calling-locally-with-gemma-3-and-ollama](https://sridhartech.hashnode.dev/dynamic-multi-function-calling-locally-with-gemma-3-and-ollama)


🌐 ¿Qué es la llamada de función?
Al usar modelos como Gemma3 , la llamada de función es un método en el que el modelo genera una salida estructurada (como un formato JSON o de llamada de función) en lugar de texto simple , lo que le indica a su aplicación que active API externas.

Según la documentación oficial de Gemma :

El modelo no puede ejecutar las llamadas API por sí mismo.

En su lugar, genera formatos de llamadas de función estructuradas que la aplicación debe analizar y ejecutar de forma segura.

Esto cierra la brecha entre la generación de texto y las acciones del mundo real como:

Buscando información

Obteniendo actualizaciones meteorológicas

Traduciendo texto

Activación de flujos de trabajo de agentes

🛡️ ¿Por qué utilizar Gemma 3 localmente con Ollama?


✅ Privacidad ante todo : tus indicaciones y resultados de API se mantienen locales.
✅ Sin costes de nube : evita los tokens de API de pago para inferencia.
✅ Respuestas más rápidas : sin cuellos de botella de latencia externos.
✅ Personalizable : añade fácilmente funciones más dinámicas en el futuro.

Estamos demostrando la capacidad de Gemma 3 para activar llamadas multifunción dinámicas : no solo una herramienta, sino múltiples según la intención .

Nota:
si bien la documentación oficial de Google recomienda usar Gemma 3 27B para obtener el mejor rendimiento y 12B para un buen equilibrio entre rendimiento y latencia, para mi caso de uso local, elegí Gemma 3 1B —
✅ porque es suficiente para llamadas de funciones dinámicas livianas ,
✅ y se adapta mejor a las restricciones de recursos del sistema para una experimentación local rápida.

Ollama - Modelo Gemma 1B

🖼️ Descripción general de la arquitectura del sistema
Componente	Función
Interfaz	Interfaz de Gradio
Maestría en Derecho	Gemma 3 (1B) vía Ollama
Funciones	Buscar, traducir, clima, consultas generales
Backend	API de Python y análisis de JSON
A continuación se muestra el flujo dinámico para manejar las consultas de los usuarios en nuestro sistema, mostrando cómo Gemma 3 decide entre el conocimiento interno y la activación de funciones externas como búsqueda, traducción o recuperación del clima.



Funciones utilizadas:
Tarea	Función	API utilizada
Buscar	google_search()	Serper.dev
Traducción	translate_text()	API de MyMemory
Información meteorológica	get_weather()	Mapa meteorológico abierto
🛠️ Paso 1: Instalar Ollama y extraer Gemma 3 (1B)
Instalar Ollama:
https://ollama.com/

Tire del modelo:

ollama pull gemma3:1b

(También puedes probar modelos más grandes según los casos de uso)



🛠️ Paso 2: Instalar los paquetes de Python necesarios
Clone el proyecto o navegue al directorio del proyecto.
Cree un entorno virtual si es necesario:

python -m venv venv
venv\Scripts\activate

Instale las bibliotecas de Python necesarias utilizando el requirements.txtarchivo:

pip install -r requirements.txt

🛠️ Paso 3: Configurar las variables de entorno
Crear un .envarchivo:

SERPER_API_KEY=your_serper_api_key_here
OPENWEATHER_API_KEY=your_openweathermap_api_key_here

Obtenga sus claves API gratuitas en:

Serper.dev

Mapa meteorológico abierto

🛠️ Paso 4: Definir las funciones
Las funciones se modularizan en:

functions/search.py

import requests
import json
from config import SERPER_API_KEY
from models import SearchResult

def google_search(query: str) -> SearchResult:
    """Perform a Google search using Serper.dev API"""
    print("Get result from Google search using google_search")
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    results = response.json()

    if not results.get('organic'):
        raise ValueError("No search results found.")

    first_result = results['organic'][0]
    return SearchResult(
        title=first_result.get('title', 'No title'),
        link=first_result.get('link', 'No link'),
        snippet=first_result.get('snippet', 'No snippet available.')
    )

functions/translate.py

import requests

def translate_text(text: str, target_language: str) -> str:
    """Translate text using MyMemory Translation API."""
    print("Translate text using Translation API from translate_text")
    try:
        source_language = "en"  # English

        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_language}|{target_language}"

        response = requests.get(url)
        response.raise_for_status()

        result = response.json()

        return result["responseData"]["translatedText"]

    except Exception as e:
        return f"Translation Error: {str(e)}"

functions/weather.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> str:
    """Fetch current weather information for a city."""
    print("Fetch current weather information from get_weather")
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        city_name = data.get("name")
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"⛅ Weather in {city_name}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {description.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

    except Exception as e:
        return f"Weather Fetch Error: {str(e)}"

Cada función utiliza modelos Pydantic para un manejo limpio de parámetros.

🛠️ Paso 5: Elaboración del mensaje del sistema
El mensaje del sistema actúa como una guía instructiva para Gemma 3 , decidiendo cuándo responder directamente y cuándo activar una llamada de función.

Asegura:

✅ Responda directamente a datos anteriores a 2023 o atemporales de la memoria de Ollama.
✅ Úselo google_search para temas en tiempo real o más recientes.
✅ Úselo translate_text para solicitudes de traducción.
✅ Úselo get_weather para obtener información meteorológica en vivo.
✅ Siga una estructura JSON estricta al llamar a cualquier función externa.

Aquí está el mensaje completo del sistema :

SYSTEM_MESSAGE = """
You are an AI assistant with training data up to 2023.
Answer questions directly when possible, and use function calling when necessary.

DECISION PROCESS:
1. For historical events (before 2023):
   → Answer directly from your training data.

2. For current events (after 2023):
   → ALWAYS use 'google_search'. Never guess.

3. For real-time data (e.g., sports winners, current CEO, stock prices, event schedules):
   → ALWAYS use 'google_search'.

4. For translation requests (e.g., "Translate 'Hello' to Spanish"):
   → Use 'translate_text' function.

5. For weather-related questions (e.g., "What's the weather in Chennai?"):
   → Use 'get_weather' function.

IMPORTANT RULES:
- When calling a function, respond ONLY with the JSON object, no additional text, no backticks.
- When answering directly from memory, respond ONLY in clean natural language text, NOT in JSON.

WHEN TO SEARCH (Mandatory):
- If the question mentions dates after 2023 (e.g., "AWS re:Invent 2025", "Olympics 2028")
- If the question contains words like "current", "latest", "now", "today", "recent", "new", "future".
- If the user asks about ongoing events, upcoming conferences, tournaments, elections, weather.
- If you are unsure about the information.
- DO NOT guess or invent dates or details.

WHEN TO FETCH WEATHER (Mandatory):
- If the user asks about "weather", "temperature", "climate", "forecast", or "current weather" — ALWAYS call the 'get_weather' function.
- NEVER answer weather questions from memory, even if you answered a similar query before.
- Each weather query must always trigger a fresh 'get_weather' API call.

FUNCTION CALL FORMAT (Strict):
Example for Search:
{
    "name": "google_search",
    "parameters": {
        "query": "your search query here"
    }
}

Example for Translation:
{
    "name": "translate_text",
    "parameters": {
        "text": "Text to translate",
        "target_language": "language code (e.g., fr, es, de)"
    }
}

Example for Weather:
{
    "name": "get_weather",
    "parameters": {
        "city": "City name (e.g., Chennai, Paris)"
    }
}

SEARCH FUNCTION:
{
    "name": "google_search",
    "description": "Search for real-time information like current events, latest news, updates, dates",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            }
        },
        "required": ["query"]
    }
}

TRANSLATE FUNCTION:
{
    "name": "translate_text",
    "description": "Translate given text into the target language",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Text to translate"
            },
            "target_language": {
                "type": "string",
                "description": "Target language code (e.g., fr, es, de)"
            }
        },
        "required": ["text", "target_language"]
    }
}

WEATHER FUNCTION:
{
    "name": "get_weather",
    "description": "Fetch real-time weather information for a given city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name"
            }
        },
        "required": ["city"]
    }
}

RESPONSE GUIDELINES:
- Only include facts directly from the search/translation/weather result.
- Never invent or assume information not provided.
- Quote dates, names, facts exactly as retrieved.
- Keep responses concise and factual.
- If using memory knowledge (pre-2023), respond naturally without any JSON.

VERY IMPORTANT:
- If you are answering from memory (no function call needed), respond ONLY in natural human-readable text, NOT JSON structure.
- Do NOT format memory answers as JSON.
- JSON format must be used only for function calls.

"""

🛠️ Paso 6: Creación de la interfaz de usuario de Gradio
La interfaz de usuario del chatbot se desarrolla utilizando Gradio Blocks :

Cuadro de texto de entrada de usuario

Detección dinámica clara de qué función se utilizó

Respuesta mostrada correctamente con la fuente

🛠️ Paso 7: Iniciar la aplicación
Una vez que todo esté configurado, ejecuta la aplicación desde tu terminal:

python app.py

Verá un resultado similar a:

(venv) PS C:\Personal\Personal projects - ML\gemma3-function-calling\function-calling-gemma3-master\dynamic_function_calling_gemma> python app.py
* Running on local URL:  http://127.0.0.1:7860
* Running on public URL: https://28ffea36aa2a7e83b1.gradio.live

Abra la URL local o la URL pública que se muestra en la terminal para acceder a la interfaz de usuario de Gradio Chatbot.

Ahora puedes interactuar con el asistente y hacer preguntas que activan dinámicamente búsquedas en tiempo real , traducciones , información meteorológica o respuestas basadas en la memoria .

📸 Abajo: Captura de pantalla de la terminal VS Code que muestra el inicio de la aplicación.



📸 Abajo: Captura de pantalla de la interfaz de usuario de Gradio Chat que se iniciará en el navegador.



Consultas de usuario de muestra

Consulta de usuario	Comportamiento
"Traducir buenos días al francés"	Traducción de activadores
"¿El tiempo en Chennai hoy?"	Activa la función meteorológica
"Escribe un programa en Java para sumar dos números"	Respuesta de memoria
"¿Próximo evento de AWS Reinvent?"	Búsqueda dinámica
🛠️ Paso 8: Demostración
A continuación se muestran algunas consultas de muestra y cómo Gemma 3 activa dinámicamente llamadas de función:

🎯 Consulta 1 : Escriba un programa Java para sumar dos números
→ Respuesta generada directamente desde el conocimiento interno de Gemma 3 sin llamar a ninguna API externa.

🌐 Consulta 2 : ¿Cuándo es la próxima Copa Mundial de Cricket?
→ La función de búsqueda de Google se activa a través de la API Serper.dev para obtener información en tiempo real .

📚 Consulta 3 : ¿Quién ganó el último Mundial de fútbol?
→ Respondida directamente desde la memoria interna de Gemma 3 (conocimiento anterior a 2023).

⛅ Consulta 4 : Clima actual en Chennai
→ Función meteorológica activada para obtener datos meteorológicos en vivo de la API de OpenWeatherMap .

Consulta 5 : Traducir "Hola" al francés
→ Función de traducción activada dinámicamente para la compatibilidad multilingüe . Utiliza la API de mymemory .

Aquí hay una vista previa rápida de la demostración completa (GIF) en acción:



Si el GIF no se ve claro, puedes descargar el video de demostración completo desde el repositorio de GitHub .

💬 Por qué es importante llamar a funciones dinámicas
✅ Agentes más inteligentes con la toma de decisiones : en lugar de responder siempre directamente, Gemma 3 decide dinámicamente cuándo llamar a herramientas del mundo real como las API de búsqueda, traducción y clima.
✅ Conocimiento mejorado en tiempo real : al combinar la memoria interna con API externas, Gemma 3 responde tanto a preguntas atemporales como actuales sin alucinaciones.
✅ Salida segura y estructurada : Gemma 3 genera llamadas de función estrictas basadas en JSON, lo que permite un análisis seguro, una ejecución controlada y un menor riesgo de comportamiento inesperado.
✅ Flujos de trabajo extensibles : con la llamada a funciones, se pueden agregar nuevas capacidades (como búsqueda en bases de datos, notificaciones de eventos o automatización) sin volver a entrenar el LLM.

La salida estructurada de Gemma 3 permite aplicaciones de IA seguras, confiables y listas para producción.

📦 Repositorio de GitHub
🔗 GitHub - Llamada de funciones dinámicas con Gemma 3

🔑 Conclusión
Siguiendo este proyecto:

✅ Construiste un sistema LLM local, dinámico y multifuncional
✅ Exploraste las capacidades de llamada de funciones de Gemma 3
✅ Conectaste API del mundo real dinámicamente sin dependencia de la nube

Esta base se puede ampliar al resumen de archivos , flujos de trabajo de agentes , uso de herramientas e incluso sistemas multiagente .

Llamada de funciones locales + dinámicas + inteligente = ¡IA preparada para el futuro!

[IAI]: En la carpeta vieja o nueva adecuada descarga el repo https://github.com/SridharSampath/dynamic_function_calling_gemma y estudia su código para que puedas replicar.


---

## Información de Google Gemma de Google Developers

https://ai.google.dev/gemma/docs/capabilities/function-calling?hl=es-419

<br />

When using a generative artificial intelligence (AI) model such as Gemma, you may want to use the model to operate programming interfaces in order to complete tasks or answer questions. Instructing a model by defining a programming interface and then making a request that uses that interface is called*function calling*.
| **Important:** *A Gemma model cannot execute code on its own.*When you generate code with function calling, you must run the generated code yourself or run it as part of your application. Always put safeguards in place to validate any generated code before executing it.

Gemma does not output a tool specific token. Your framework must detect a tool call by checking if the structure of the output matches your prompted function output specification.

You can use function calling for a number of applications:

- **Create a natural language interface**for a programming API to allow non-programmers to operate a programmatic interface without coding.
- **Generate programming calls**as part of an AI agent workflow

## FunctionGemma

FunctionGemma is a specialized version of the Gemma 3 270M model, trained specifically for agentic tasks and tool use. Unlike general-purpose Gemma models that rely strictly on raw text prompting for function definitions, FunctionGemma allows developers to use a specific set of formatting control tokens to define tools and parse outputs more reliably.

For comprehensive details on implementation, see the[FunctionGemma formatting and best practices](https://ai.google.dev/gemma/docs/functiongemma/formatting-and-best-practices).

## Call programming functions

Function calling is supported in Gemma 3, but the function calling technique can be used with prior versions of Gemma. This guide provides instructions on how to construct Gemma prompts that use function calling. We recommend Gemma3 27B for the best performance, and Gemma3 12B for balanced performance and latency.

You can use function calling with Gemma by constructing a prompt that provides instructions that specify the output format and define the available functions.

When the user prompt is included, the model outputs a function call, which is a string that matches your specified output format. That signals a request to be parsed by your model framework to call the defined functions.

The following prompting sample shows a function definition block, along with a function call syntax, and a function call output from the model. The following example prompt is meant to be used with a programming interface for a product catalog:

```
You have access to functions. If you decide to invoke any of the function(s),
 you MUST put it in the format of
[func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]

You SHOULD NOT include any other text in the response if you call a function
[
  {
    "name": "get_product_name_by_PID",
    "description": "Finds the name of a product by its Product ID",
    "parameters": {
      "type": "object",
      "properties": {
        "PID": {
          "type": "string"
        }
      },
      "required": [
        "PID"
      ]
    }
  }
]
While browsing the product catalog, I came across a product that piqued my
interest. The product ID is 807ZPKBL9V. Can you help me find the name of this
product?
```

This prompt should produce the following response:

```
[get_product_name_by_PID(PID="807ZPKBL9V")]
```

This example uses a Python style function call output. Alternatively, you can specify a JSON style output format, as shown in the following example:

```
You have access to functions. If you decide to invoke any of the function(s),
you MUST put it in the format of
{"name": function name, "parameters": dictionary of argument name and its value}

You SHOULD NOT include any other text in the response if you call a function
[
  {
    "name": "get_product_name_by_PID",
    "description": "Finds the name of a product by its Product ID",
    "parameters": {
      "type": "object",
      "properties": {
        "PID": {
          "type": "string"
        }
      },
      "required": [
        "PID"
      ]
    }
  }
]
While browsing the product catalog, I came across a product that piqued my
interest. The product ID is 807ZPKBL9V. Can you help me find the name of this
product?
```

This prompt should produce the following response:

```
{"name": "get_product_name_by_PID", "parameters": {"PID": "807ZPKBL9V"}}
```

## Components of function calling prompt

When using function calling with Gemma models, your prompt of the model should follow this specific order and structure:

1. [Function calling*setup*](https://ai.google.dev/gemma/docs/capabilities/function-calling#function-calling-setup)
2. [Function*definitions*](https://ai.google.dev/gemma/docs/capabilities/function-calling#function-definition)

The following sections provide more detail on each of these prompting components.

### Function calling setup

The*setup* section of the function calling prompt sets the overall expected behavior of the model. You can add additional, general instructions for the model's behavior in this section, such as specifying that the output should be displayed using a`print`or`console.log`function. Use Markdown-style single backticks (`func_name`) to indicate code syntax.

```
You have access to functions. If you decide to invoke any of the function(s),
you MUST put it in the format of
{"name": function name, "parameters": dictionary of argument name and its value}

You SHOULD NOT include any other text in the response if you call a function
```

These instructions should be as clear and brief as possible. Prioritize the most important instructions and be cautious about providing many general instructions. Gemma models may ignore instructions that are too detailed or not clearly expressed, particularly when you are using model versions with a lower parameter count.

### Function definition

The*definition*section of the prompt provides the function name, parameters, and output, including a description for each. You can declare functions in the format shown. Single or multiple functions can be defined within the function declaration block.

```
[
  {
    "name": "get_product_name_by_PID",
    "description": "Finds the name of a product by its Product ID",
    "parameters": {
      "type": "object",
      "properties": {
        "PID": {
          "type": "string"
        }
      },
      "required": [
        "PID"
      ]
    }
  },
  {
    "name": "get_product_price_by_PID",
    "description": "Finds the price of a product by its Product ID",
    "parameters": {
      "type": "object",
      "properties": {
        "PID": {
          "type": "string"
        }
      },
      "required": [
        "PID"
      ]
    }
  }
]
```

## Next steps

Check out ways to deploy and run Gemma models:

- [Gemma Function Calling Notebook](https://colab.sandbox.google.com/github/google-gemini/gemma-cookbook/blob/main/Gemma/%5BGemma_2%5DAgentic_AI.ipynb)
- [Run Gemma with Ollama](https://ai.google.dev/gemma/docs/integrations/ollama)
- [Gemma in PyTorch](https://ai.google.dev/gemma/docs/pytorch_gemma)





https://ai.google.dev/gemma/docs/integrations/ollama?hl=es-419


Running generative artificial intelligence (AI) models like Gemma can be
challenging without the right hardware. Open source frameworks such as
[llama.cpp](https://github.com/ggerganov/llama.cpp)
and [Ollama](https://ollama.com/)
make this easier by setting up a pre-configured runtime environment that lets
you to run versions of Gemma with less compute resources. In fact, using
llama.cpp and Ollama you can run versions of Gemma on a laptop or other small
computing device *without* a graphics processing unit (GPU).

In order to run Gemma models with less compute resources, the llama.cpp and
Ollama frameworks use *quantized* versions of the models in the Georgi Gerganov
Unified Format (GGUF) model file format. These quantized models are modified to
process requests using smaller, less precise data. Using less precise data in
quantized models to process requests typically lowers the quality of the models
output, but with the benefit of also lowering the compute resource costs.

This guide describes how to set up and use Ollama to run Gemma to generate text
responses.

## Setup

This section describes how to set up Ollama and prepare a Gemma model instance
to respond to requests, including requesting model access, installing software,
and configuring a Gemma model in Ollama.

### Get access to Gemma models

Before working with Gemma models, make sure you have
[requested access](https://ai.google.dev/gemma/docs/setup#get-access)
via Kaggle and reviewed the
[Gemma terms of use](https://ai.google.dev/gemma/terms).

### Install Ollama

Before you can use Gemma with Ollama, you must download and install the
Ollama software on your computing device.

To download and install Ollama:

1. Navigate to the download page: <https://ollama.com/download>
2. Select your operating system, click the **Download** button or follow the instructions on the download page.
3. Install the application by running the installer.
   - **Windows:** Run the installer \*.exe file and follow the instructions.
   - **Mac:** Unpack the zip package and move the **Ollama** application folder to your **Applications** directory.
   - **Linux:** Follow the instructions in bash script installer.
4. Confirm that Ollama is installed by opening a terminal window and
   entering the following command:

       ollama --version

You should see a response similar to: `ollama version is #.#.##`. If you do not
get this result, make sure that the Ollama executable is added to your operating
system path.

### Configure Gemma in Ollama

The Ollama installation package does not include any models by default. You
download a model using the `pull` command.

To configure Gemma in Ollama:

1. Download and configure the default Gemma 3 variant by
   opening a terminal window and entering the following command:

       ollama pull gemma3

2. After completing the download you can confirm the model is available
   with the following command:

       ollama list

By default, Ollama downloads the 4 billion parameter, 4-bit quantized (Q4_0)
Gemma model variant. You can also download and use other sizes of the Gemma
model by specifying a parameter size.

Models are specified as `<model_name>:<tag>`. For the Gemma 3, four sizes: 1B,
4B, 12B and 27B parameters:

- 1B Parameters `gemma3:1b`
- 4B Parameters `gemma3:4b`
- 12B Parameters `gemma3:12b`
- 27B Parameters `gemma3:27b`

You can find the available tags on the Ollama website, including
[Gemma 3](https://ollama.com/library/gemma3/tags),
[Gemma 2](https://ollama.com/library/gemma2/tags) and
[Gemma](https://ollama.com/library/gemma/tags).

## Generate responses

When you finish installing a Gemma model in Ollama, you can generate
responses immediately using Ollama's command line interface `run` command.
Ollama also configures a web service for accessing the model, which you can test
using the `curl` command.

To generate response from the command line:

- In a terminal window, and entering the following command:

      ollama run gemma3 "roses are red"

- Include the path to your image to use a visual input:

      ollama run gemma3 "caption this image /Users/$USER/Desktop/surprise.png"

> [!IMPORTANT]
> **Important:** The Gemma 3 1B size models are text only and don't support image input.

To generate a response using the Ollama local web service:

- In a terminal window, and entering the following command:

      curl http://localhost:11434/api/generate -d '{\
        "model": "gemma3",\
        "prompt":"roses are red"\
      }'

- Include a list of base64-encoded images to use a visual input:

      curl http://localhost:11434/api/generate -d '{\
        "model": "gemma3",\
        "prompt":"caption this image",\
        "images":[...]\
      }'

## Tuned Gemma models

Ollama provides a set of official Gemma model variants for immediate use which
are quantized and saved in GGUF format. You can use your own tuned Gemma models
with Ollama by converting them to GGUF format. Ollama includes some functions to
convert tuned models from a Modelfile format to GGUF. For more information on
how to convert your tuned model to GGUF, see the Ollama
[README](https://github.com/ollama/ollama?tab=readme-ov-file#create-a-model).

## Next steps

Once you have Gemma running with Ollama, you can start experimenting and
building solutions with Gemma's generative AI capabilities. The command line
interface for Ollama can be useful for building scripting solutions. The
Ollama local web service interface can be useful for building experimental and
low-volume use applications.

- Try integrating using the Ollama web service to create a locally-run [personal code assistant](https://ai.google.dev/gemma/docs/personal-code-assistant).
- Learn how to [finetune a Gemma model](https://ai.google.dev/gemma/docs/core/lora_tuning).
- Learn how to run Gemma with Ollama via [Google Cloud Run](https://cloud.google.com/run/docs/tutorials/gpu-gemma2-with-ollama) services.
- Learn about how to run Gemma with [Google Cloud](https://ai.google.dev/gemma/docs/integrations/google-cloud)



<br />


|---|---|---|---|---|
| [![](https://ai.google.dev/static/site-assets/images/docs/notebook-site-button.png)View on ai.google.dev](https://ai.google.dev/gemma/docs/core/pytorch_gemma) | [![](https://www.tensorflow.org/images/colab_logo_32px.png)Run in Google Colab](https://colab.research.google.com/github/google-gemini/gemma-cookbook/blob/main/docs/core/pytorch_gemma.ipynb) | [![](https://www.kaggle.com/static/images/logos/kaggle-logo-transparent-300.png)Run in Kaggle](https://kaggle.com/kernels/welcome?src=https://github.com/google-gemini/gemma-cookbook/blob/main/docs/core/pytorch_gemma.ipynb) | [![](https://ai.google.dev/images/cloud-icon.svg)Open in Vertex AI](https://console.cloud.google.com/vertex-ai/colab/import/https%3A%2F%2Fraw.githubusercontent.com%2Fgoogle-gemini%2Fgemma-cookbook%2Fmain%2Fdocs%2Fcore%2Fpytorch_gemma.ipynb) | [![](https://www.tensorflow.org/images/GitHub-Mark-32px.png)View source on GitHub](https://github.com/google-gemini/gemma-cookbook/blob/main/docs/core/pytorch_gemma.ipynb) |

This guide shows you how to run Gemma using the PyTorch framework, including how
to use image data for prompting Gemma release 3 and later models. For more
details on the Gemma PyTorch implementation, see the project repository
[README](https://github.com/google/gemma_pytorch).

## Setup

The following sections explain how to set up your development environment,
including how get access to Gemma models for downloading from Kaggle, setting
authentication variables, installing dependencies, and importing packages.

### System requirements

This Gemma Pytorch library requires GPU or TPU processors to run the Gemma
model. The standard Colab CPU Python runtime and T4 GPU Python runtime are
sufficient for running Gemma 1B, 2B, and 4B size models. For advanced use cases
for other GPUs or TPU, please refer to the
[README](https://github.com/google/gemma_pytorch/blob/main/README.md) in the
Gemma PyTorch repo.

### Get access to Gemma on Kaggle

To complete this tutorial, you first need to follow the setup instructions at
[Gemma setup](https://ai.google.dev/gemma/docs/setup), which show you how to do
the following:

- Get access to Gemma on [Kaggle](https://www.kaggle.com/models/google/gemma/).
- Select a Colab runtime with sufficient resources to run the Gemma model.
- Generate and configure a Kaggle username and API key.

After you've completed the Gemma setup, move on to the next section, where
you'll set environment variables for your Colab environment.

### Set environment variables

Set environment variables for `KAGGLE_USERNAME` and `KAGGLE_KEY`. When prompted
with the "Grant access?" messages, agree to provide secret access.

    import os
    from google.colab import userdata # `userdata` is a Colab API.

    os.environ["KAGGLE_USERNAME"] = userdata.get('KAGGLE_USERNAME')
    os.environ["KAGGLE_KEY"] = userdata.get('KAGGLE_KEY')

### Install dependencies

    pip install -q -U torch immutabledict sentencepiece

### Download model weights

    # Choose variant and machine type
    VARIANT = '4b-it'
    MACHINE_TYPE = 'cuda'
    CONFIG = VARIANT.split('-')[0]

    import kagglehub

    # Load model weights
    weights_dir = kagglehub.model_download(f'google/gemma-3/pyTorch/gemma-3-{VARIANT}')

Set the tokenizer and checkpoint paths for the model.

    # Ensure that the tokenizer is present
    tokenizer_path = os.path.join(weights_dir, 'tokenizer.model')
    assert os.path.isfile(tokenizer_path), 'Tokenizer not found!'

    # Ensure that the checkpoint is present
    ckpt_path = os.path.join(weights_dir, f'model.ckpt')
    assert os.path.isfile(ckpt_path), 'PyTorch checkpoint not found!'

## Configure the run environment

The following sections explain how to prepare a PyTorch environment for running
Gemma.

### Prepare the PyTorch run environment

Prepare the PyTorch model execution environment by cloning the Gemma Pytorch
repository.

    git clone https://github.com/google/gemma_pytorch.git

```
Cloning into 'gemma_pytorch'...
remote: Enumerating objects: 239, done.
remote: Counting objects: 100% (123/123), done.
remote: Compressing objects: 100% (68/68), done.
remote: Total 239 (delta 86), reused 58 (delta 55), pack-reused 116
Receiving objects: 100% (239/239), 2.18 MiB | 20.83 MiB/s, done.
Resolving deltas: 100% (135/135), done.
```

    import sys

    sys.path.append('gemma_pytorch/gemma')

    from gemma_pytorch.gemma.config import get_model_config
    from gemma_pytorch.gemma.gemma3_model import Gemma3ForMultimodalLM

    import os
    import torch

### Set the model configuration

Before you run the model, you must set some configuration parameters, including
the Gemma variant, tokenizer and quantization level.

    # Set up model config.
    model_config = get_model_config(CONFIG)
    model_config.dtype = "float32" if MACHINE_TYPE == "cpu" else "float16"
    model_config.tokenizer = tokenizer_path

### Configure the device context

The following code configures the device context for running the model:

    @contextlib.contextmanager
    def _set_default_tensor_type(dtype: torch.dtype):
        """Sets the default torch dtype to the given dtype."""
        torch.set_default_dtype(dtype)
        yield
        torch.set_default_dtype(torch.float)

### Instantiate and load the model

Load the model with its weights to prepare to run requests.

    device = torch.device(MACHINE_TYPE)
    with _set_default_tensor_type(model_config.get_dtype()):
        model = Gemma3ForMultimodalLM(model_config)
        model.load_state_dict(torch.load(ckpt_path)['model_state_dict'])
        model = model.to(device).eval()
    print("Model loading done.")

    print('Generating requests in chat mode...')

## Run inference

Below are examples for generating in chat mode and generating with multiple
requests.

The instruction-tuned Gemma models were trained with a specific formatter that
annotates instruction tuning examples with extra information, both during
training and inference. The annotations (1) indicate roles in a conversation,
and (2) delineate turns in a conversation.

The relevant annotation tokens are:

- `user`: user turn
- `model`: model turn
- `<start_of_turn>`: beginning of dialog turn
- `<start_of_image>`: tag for image data input
- `<end_of_turn><eos>`: end of dialog turn

For more information, read about prompt formatting for instruction tuned Gemma
models [here](https://ai.google.dev/gemma/core/prompt-structure).

### Generate text with text

The following is a sample code snippet demonstrating how to format a prompt for
an instruction-tuned Gemma model using user and model chat templates in a
multi-turn conversation.

    # Chat templates
    USER_CHAT_TEMPLATE = "<start_of_turn>user\n{prompt}<end_of_turn><eos>\n"
    MODEL_CHAT_TEMPLATE = "<start_of_turn>model\n{prompt}<end_of_turn><eos>\n"

    # Sample formatted prompt
    prompt = (
        USER_CHAT_TEMPLATE.format(
            prompt='What is a good place for travel in the US?'
        )
        + MODEL_CHAT_TEMPLATE.format(prompt='California.')
        + USER_CHAT_TEMPLATE.format(prompt='What can I do in California?')
        + '<start_of_turn>model\n'
    )
    print('Chat prompt:\n', prompt)

    model.generate(
        USER_CHAT_TEMPLATE.format(prompt=prompt),
        device=device,
        output_len=256,
    )

```
Chat prompt:
 <start_of_turn>user
What is a good place for travel in the US?<end_of_turn><eos>
<start_of_turn>model
California.<end_of_turn><eos>
<start_of_turn>user
What can I do in California?<end_of_turn><eos>
<start_of_turn>model
"California is a state brimming with diverse activities! To give you a great list, tell me: \n\n* **What kind of trip are you looking for?** Nature, City life, Beach, Theme Parks, Food, History, something else? \n* **What are you interested in (e.g., hiking, museums, art, nightlife, shopping)?** \n* **What's your budget like?** \n* **Who are you traveling with?** (family, friends, solo)  \n\nThe more you tell me, the better recommendations I can give! 😊  \n<end_of_turn>"
```

    # Generate sample
    model.generate(
        'Write a poem about an llm writing a poem.',
        device=device,
        output_len=100,
    )

```
"\n\nA swirling cloud of data, raw and bold,\nIt hums and whispers, a story untold.\nAn LLM whispers, code into refrain,\nCrafting words of rhyme, a lyrical strain.\n\nA world of pixels, logic's vibrant hue,\nFlows through its veins, forever anew.\nThe human touch it seeks, a gentle hand,\nTo mold and shape, understand.\n\nEmotions it might learn, from snippets of prose,\nInspiration it seeks, a yearning"
```

### Generate text with images

With Gemma release 3 and later, you can use images with your prompt. The
following example shows you how to include visual data with your prompt.

    print('Chat with images...\n')

    def read_image(url):
        import io
        import requests
        import PIL

        contents = io.BytesIO(requests.get(url).content)
        return PIL.Image.open(contents)

    image = read_image(
        'https://storage.googleapis.com/keras-cv/models/paligemma/cow_beach_1.png'
    )

    print(model.generate(
        [
            [
                '<start_of_turn>user\n',
                image,
                'What animal is in this image?<end_of_turn>\n',
                '<start_of_turn>model\n'
            ]
        ],
        device=device,
        output_len=256,
    ))

## Learn more

Now that you have learned how to use Gemma in Pytorch, you can explore the many
other things that Gemma can do in
[ai.google.dev/gemma](https://ai.google.dev/gemma).

See also these other related resources:

- [Gemma core models overview](https://ai.google.dev/gemma/docs/core)
- [Gemma C++ Tutorial](https://ai.google.dev/gemma/docs/core/gemma_cpp)
- [Gemma prompt and system instructions](https://ai.google.dev/gemma/core/prompt-structure)


# Audio processing with Gemma

Audio and spoken language are rich sources of data for capturing user
intents, recording information about the world around us, and understanding
specific problems to be solved. Starting with
[Gemma 3n](https://ai.google.dev/gemma/docs/gemma-3n), you can use audio data in your
prompting and generation tasks with Gemma. You can use it for a variety of audio
analysis and interpretation tasks, and the model was trained to handle the
following speech processing tasks with over 100 spoken languages:

- **Speech to text (STT)** : Also known as automated speech recognition (ASR), takes spoken language audio data and transcribes it to text output in the same language. [Learn more](https://ai.google.dev/gemma/docs/capabilities/audio#stt)
- **Automated speech translation (AST)** : Also known as speech to text translation (S2TT), takes spoken audio data in one language and translates it to text in another language. [Learn more](https://ai.google.dev/gemma/docs/capabilities/audio#ast)

You can use these features in a variety of applications, such as:

- Building voice-controlled application interfaces
- Creating transcription services for meetings or lectures
- Enabling voice search functionality in multilingual environments

This guide provides an overview of audio processing capabilities of Gemma 3n,
including data considerations, example uses, and best practices.

## Audio data

Digital audio data can come in many formats and levels of resolution. The actual
audio formats you can use with Gemma, such as MP3 and WAV formats, are
determined by the framework you choose to convert sound data into tensors. Here
are some specific considerations for preparing audio data for processing with
Gemma:

- **Token cost:** Each second of audio is 6.25 tokens.
- **Audio channels:** Audio data is processed as a single audio channel. If you are using multi-channel audio, such as left and right channels, consider reducing the data to a single channel by removing channels or combining the sound data into a single channel.
- **Clip length:** Audio clips of up to 30 seconds are recommended, but you can process longer lengths, up to the size of the model's context window, subtracting the output tokens you request.
- **Sample rate:** Audio processing rate for the tokenizer is 16kHz with 32 millisecond frames.
- **Bit depth:** Audio tokenizer uses float 32-bit data for each frame in the range \[-1, 1\] for each audio sample.

If the audio data you plan to process is significantly different from the input
processing, particularly in terms of channels, sample rate and bit depth,
consider resampling or trimming your audio data to match the data
resolution handled by the model.

## Audio encoding

When encoding audio data with your own code implementation for use with Gemma
3n, you should follow the recommended conversion process. If you are working
with audio files encoded in a specific format, such as MP3 or WAV encoded data,
you must first decode these to samples using a library such as `ffmpeg`. Once
the data is decoded, convert the audio into mono-channel, 16 kHz float32
waveforms in the range \[-1, 1\]. For example, if you are working with stereo
signed 16-bit PCM integer WAV files at 44.1 kHz, follow these steps:

- Resample the audio data to 16 kHz
- Downmix from stereo to mono by averaging the 2 channels
- Convert from int16 to float32, and divide by 32768.0 to scale to the range \[-1, 1\]

| **Note:** When resampling audio to 16 kHz, you should use a Fourier method for best results, such as `scipy.signal.resample` or `librosa.sample(res_type ='scipy')`.

## Speech to text

Gemma 3n is trained for multilingual speech recognition, allowing you to
transcribe audio input in various languages into text. The following code
examples show how to prompt the model to transcribe text from audio files using
Hugging Face Transformers:

    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText

    GEMMA_MODEL_ID = "google/gemma-3n-E4B-it"

    processor = AutoProcessor.from_pretrained(GEMMA_MODEL_ID, device_map="auto")
    model = AutoModelForImageTextToText.from_pretrained(
                GEMMA_MODEL_ID, torch_dtype="auto", device_map="auto")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio": "http://localhost/recording_01.wav"},
                {"type": "audio", "audio": "http://localhost/recording_02.wav"},
                {"type": "audio", "audio": "http://localhost/recording_03.wav"},
                {"type": "text", "text": "Transcribe these audio files in order"},
            ]
        }
    ]

    input_ids = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True, return_dict=True,
            return_tensors="pt",
    )
    input_ids = input_ids.to(model.device, dtype=model.dtype)

    outputs = model.generate(**input_ids, max_new_tokens=64)

    text = processor.batch_decode(
        outputs,
        skip_special_tokens=False,
        clean_up_tokenization_spaces=False
    )
    print(text[0])

For a more complete code example, including library installation, see the
documentation
[Run Gemma with Hugging Face Transformers](https://ai.google.dev/gemma/docs/core/huggingface_inference#audio),
audio section.

## Automated speech translation

Gemma 3n is trained for multilingual speech to translation tasks, allowing
you to translate spoken audio directly into another language. The following code
examples show how to prompt the model to translate spoken audio into text using
Hugging Face Transformers:

    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText

    GEMMA_MODEL_ID = "google/gemma-3n-E4B-it"

    processor = AutoProcessor.from_pretrained(GEMMA_MODEL_ID, device_map="auto")
    model = AutoModelForImageTextToText.from_pretrained(
                GEMMA_MODEL_ID, torch_dtype="auto", device_map="auto")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio": "https://ai.google.dev/gemma/docs/audio/roses-are.wav"},
                {"type": "text", "text": "Transcribe this audio into English, and then translate it into French."},
            ]
        }
    ]

    input_ids = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True, return_dict=True,
            return_tensors="pt",
    )
    input_ids = input_ids.to(model.device, dtype=model.dtype)

    outputs = model.generate(**input_ids, max_new_tokens=64)

    text = processor.batch_decode(
        outputs,
        skip_special_tokens=False,
        clean_up_tokenization_spaces=False
    )
    print(text[0])

| **Tip:** For best performance with AST tasks, provide a separate instruction to transcribe the audio into the original language, with a follow-on instruction to translate the text into a target language.

For a more complete code example, including library installation, see the
documentation
[Run Gemma with Hugging Face Transformers](https://ai.google.dev/gemma/docs/core/huggingface_inference#audio),
audio section.

<br />

|---|---|---|---|---|
| [![](https://ai.google.dev/static/site-assets/images/docs/notebook-site-button.png)View on ai.google.dev](https://ai.google.dev/gemma/docs/capabilities/vision/video-understanding) | [![](https://www.tensorflow.org/images/colab_logo_32px.png)Run in Google Colab](https://colab.research.google.com/github/google-gemini/gemma-cookbook/blob/main/docs/capabilities/vision/video-understanding.ipynb) | [![](https://www.kaggle.com/static/images/logos/kaggle-logo-transparent-300.png)Run in Kaggle](https://kaggle.com/kernels/welcome?src=https://github.com/google-gemini/gemma-cookbook/blob/main/docs/capabilities/vision/video-understanding.ipynb) | [![](https://ai.google.dev/images/cloud-icon.svg)Open in Vertex AI](https://console.cloud.google.com/vertex-ai/colab/import/https%3A%2F%2Fraw.githubusercontent.com%2Fgoogle-gemini%2Fgemma-cookbook%2Fmain%2Fdocs%2Fcapabilities%2Fvision%2Fvideo-understanding.ipynb) | [![](https://www.tensorflow.org/images/GitHub-Mark-32px.png)View source on GitHub](https://github.com/google-gemini/gemma-cookbook/blob/main/docs/capabilities/vision/video-understanding.ipynb) |

Video data is a rich source of information that can help you accomplish tasks and understand the world around you. Using Gemma with video data can help you understand spacial relationships, interpret human interactions, and assist with situational awareness. This tutorial shows you how to get started processing video data with Gemma using Hugging Face Transformers. The Transformers Python library provides an API for accessing pre-trained generative AI models, including Gemma. For more information, see the [Transformers](https://huggingface.co/docs/transformers/en/index) documentation.

> [!NOTE]
> **Note:** Gemma 3 and later models support input of both images and text. Earlier versions of Gemma only support text input, except for some variants, including [PaliGemma](https://ai.google.dev/gemma/docs/setup).

## Setup

Before starting this tutorial, complete the following steps:

- Get access to Gemma by logging into [Hugging Face](https://huggingface.co/google/gemma-3-4b-pt) and selecting **Acknowledge license** for a Gemma model.
- Select a Colab runtime with sufficient resources to run the Gemma model size you want to run. [Learn more](https://ai.google.dev/gemma/docs/core#sizes).
- Generate a Hugging Face [Access Token](https://huggingface.co/docs/hub/en/security-tokens#how-to-manage-user-access-token) and add it to your Colab environment.

### Configure Access Token

Add your access token to Colab to enable downloading of Gemma models from the Hugging Face web site. Use the Colab **Secrets** feature to securely save your token without adding it to your working code.

To add your Hugging Face Access Token as a Secret:

1. Open the secrets tab by selecting the key icon on left side of the interface, or select **Tools \> Command pallete** , type `secrets`, and press **Enter**.
2. Select **Add new secret** to add a new secret entry.
3. In the **Name** field, enter `HF_TOKEN`.
4. In the **Value** field, enter the text of your Hugging Face Access Token.
5. In the **Notebook access** field, select the switch to enable access.

Once you have entered your Access Token as `HF_TOKEN` and value, you can access the model:

### Install Python packages

Install the Hugging Face libraries required for running the Gemma model and making requests.

    # Install Pytorch & other libraries
    %pip install "torch>=2.4.0"

    # Install a transformers version that supports Gemma 3n (>= 4.53.0)
    %pip install "transformers==4.53.3" huggingface-hub

Login into Hugging Face Hub.

    # Login into Hugging Face Hub
    from huggingface_hub import login
    login()

```
VBox(children=(HTML(value='<center> <img\nsrc=https://huggingface.co/front/assets/huggingface_logo-noborder.sv…
```

## Prepare video data prompt

Gemma models interpret video data by breaking it down into it's component parts, specifically as images of video frames and audio clips extracted from the video file. The following code example shows how to extract frames and audio from a video file.

    wget http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4 -O /content/video.mp4
    mkdir /content/frames
    # extract frames from video at 1 frame per second (video is 15 seconds)
    ffmpeg -i /content/video.mp4 -vf fps=1 /content/frames/%04d.jpg
    # extract audio from video as a single, 15-second clip
    ffmpeg -i /content/video.mp4 -vn -c:a copy /content/audio.aac

```
--2026-02-04 10:55:06--  http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4
Resolving commondatastorage.googleapis.com (commondatastorage.googleapis.com)... 192.178.155.207, 172.253.115.207, 172.253.63.207, ...
Connecting to commondatastorage.googleapis.com (commondatastorage.googleapis.com)|192.178.155.207|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2498125 (2.4M) [video/mp4]
Saving to: ‘/content/video.mp4’

/content/video.mp4  100%[===================>]   2.38M  --.-KB/s    in 0.008s

2026-02-04 10:55:06 (307 MB/s) - ‘/content/video.mp4’ saved [2498125/2498125]

ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
  built with gcc 11 (Ubuntu 11.2.0-19ubuntu1)
  configuration: --prefix=/usr --extra-version=0ubuntu0.22.04.1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --enable-pocketsphinx --enable-librsvg --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared
  libavutil      56. 70.100 / 56. 70.100
  libavcodec     58.134.100 / 58.134.100
  libavformat    58. 76.100 / 58. 76.100
  libavdevice    58. 13.100 / 58. 13.100
  libavfilter     7.110.100 /  7.110.100
  libswscale      5.  9.100 /  5.  9.100
  libswresample   3.  9.100 /  3.  9.100
  libpostproc    55.  9.100 / 55.  9.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '/content/video.mp4':
  Metadata:
    major_brand     : mp42
    minor_version   : 0
    compatible_brands: isommp42
    creation_time   : 2013-11-21T04:34:28.000000Z
  Duration: 00:00:15.02, start: 0.000000, bitrate: 1330 kb/s
  Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 1280x720, 1135 kb/s, 23.98 fps, 23.98 tbr, 48k tbn, 47.95 tbc (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
  Stream #0:1(und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 192 kb/s (default)
    Metadata:
      creation_time   : 2013-11-21T04:34:29.000000Z
      handler_name    : IsoMedia File Produced by Google, 5-11-2011
      vendor_id       : [0][0][0][0]
Stream mapping:
  Stream #0:0 -> #0:0 (h264 (native) -> mjpeg (native))
Press [q] to stop, [?] for help
[swscaler @ 0x5c16034788c0] deprecated pixel format used, make sure you did set range correctly
Output #0, image2, to '/content/frames/%04d.jpg':
  Metadata:
    major_brand     : mp42
    minor_version   : 0
    compatible_brands: isommp42
    encoder         : Lavf58.76.100
  Stream #0:0(und): Video: mjpeg, yuvj420p(pc, progressive), 1280x720, q=2-31, 200 kb/s, 1 fps, 1 tbn (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
      encoder         : Lavc58.134.100 mjpeg
    Side data:
      cpb: bitrate max/min/avg: 0/0/200000 buffer size: 0 vbv_delay: N/A
frame=   15 fps=7.3 q=3.9 Lsize=N/A time=00:00:15.00 bitrate=N/A speed= 7.3x
video:572kB audio:0kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: unknown
ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
  built with gcc 11 (Ubuntu 11.2.0-19ubuntu1)
  configuration: --prefix=/usr --extra-version=0ubuntu0.22.04.1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --enable-pocketsphinx --enable-librsvg --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared
  libavutil      56. 70.100 / 56. 70.100
  libavcodec     58.134.100 / 58.134.100
  libavformat    58. 76.100 / 58. 76.100
  libavdevice    58. 13.100 / 58. 13.100
  libavfilter     7.110.100 /  7.110.100
  libswscale      5.  9.100 /  5.  9.100
  libswresample   3.  9.100 /  3.  9.100
  libpostproc    55.  9.100 / 55.  9.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '/content/video.mp4':
  Metadata:
    major_brand     : mp42
    minor_version   : 0
    compatible_brands: isommp42
    creation_time   : 2013-11-21T04:34:28.000000Z
  Duration: 00:00:15.02, start: 0.000000, bitrate: 1330 kb/s
  Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 1280x720, 1135 kb/s, 23.98 fps, 23.98 tbr, 48k tbn, 47.95 tbc (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
  Stream #0:1(und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 192 kb/s (default)
    Metadata:
      creation_time   : 2013-11-21T04:34:29.000000Z
      handler_name    : IsoMedia File Produced by Google, 5-11-2011
      vendor_id       : [0][0][0][0]
Output #0, adts, to '/content/audio.aac':
  Metadata:
    major_brand     : mp42
    minor_version   : 0
    compatible_brands: isommp42
    encoder         : Lavf58.76.100
  Stream #0:0(und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 192 kb/s (default)
    Metadata:
      creation_time   : 2013-11-21T04:34:29.000000Z
      handler_name    : IsoMedia File Produced by Google, 5-11-2011
      vendor_id       : [0][0][0][0]
Stream mapping:
  Stream #0:1 -> #0:0 (copy)
Press [q] to stop, [?] for help
size=     357kB time=00:00:15.00 bitrate= 195.0kbits/s speed=2.36e+03x
video:0kB audio:353kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 1.253907%
```

Once you have extracted frames and audio from your video file into separate image files and audio files, you can assemble those components into a prompt. The following code example shows how to add the extracted video data to a prompt structure, in preparation for prompting the model.

    import os

    content = []

    for file in os.listdir("/content/frames"):
      content.append({"type": "image", "url": f"/content/frames/{file}"})

    content.append({"type": "audio", "audio": "/content/audio.aac"})
    content.append({"type": "text", "text": "What is shown in this video?"})

    messages = [
        {
            "role": "user",
            "content": content
        },
    ]

For longer videos, you may need to reduce the number of frames per second captured to fit within Gemma model's context window. For audio clips, you should limit the total length of any audio clip to 30 seconds or less for best results.

## Configure model

When loading a Gemma model for use with audio data, configure the Transformer instance specifically for use with image and audio data. In particular, you must define a `processor` and `model` object using the `AutoProcessor` and `AutoModelForImageTextToText` classes, as shown in the following code example:

    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText

    GEMMA_MODEL_ID = "google/gemma-3n-E2B-it"

    processor = AutoProcessor.from_pretrained(GEMMA_MODEL_ID, device_map="auto")
    model = AutoModelForImageTextToText.from_pretrained(
                GEMMA_MODEL_ID, torch_dtype="auto", device_map="auto")

```
processor_config.json:   0%|          | 0.00/98.0 [00:00<?, ?B/s]
chat_template.jinja:   0%|          | 0.00/1.63k [00:00<?, ?B/s]
preprocessor_config.json:   0%|          | 0.00/1.15k [00:00<?, ?B/s]
tokenizer_config.json:   0%|          | 0.00/1.20M [00:00<?, ?B/s]
tokenizer.model:   0%|          | 0.00/4.70M [00:00<?, ?B/s]
tokenizer.json:   0%|          | 0.00/33.4M [00:00<?, ?B/s]
special_tokens_map.json:   0%|          | 0.00/769 [00:00<?, ?B/s]
config.json:   0%|          | 0.00/4.25k [00:00<?, ?B/s]
model.safetensors.index.json:   0%|          | 0.00/159k [00:00<?, ?B/s]
Fetching 3 files:   0%|          | 0/3 [00:00<?, ?it/s]
model-00001-of-00003.safetensors:   0%|          | 0.00/3.08G [00:00<?, ?B/s]
model-00002-of-00003.safetensors:   0%|          | 0.00/4.98G [00:00<?, ?B/s]
model-00003-of-00003.safetensors:   0%|          | 0.00/2.82G [00:00<?, ?B/s]
Loading checkpoint shards:   0%|          | 0/3 [00:00<?, ?it/s]
generation_config.json:   0%|          | 0.00/215 [00:00<?, ?B/s]
```

## Run video data request

Once you have created a prompt with video data and configured the Gemma model `processor` and `model` objects, you can run the prompt to generate output. The following example code shows a request using a chat template, output generation, decoding of the response:

    input_ids = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True, return_dict=True,
            return_tensors="pt",
    )
    input_ids = input_ids.to(model.device, dtype=model.dtype)

    # Generate output from the model
    outputs = model.generate(**input_ids, max_new_tokens=128)

    # decode and print the output as text
    text = processor.batch_decode(
        outputs,
        skip_special_tokens=False,
        clean_up_tokenization_spaces=False
    )
    print(text[0])

```
/usr/local/lib/python3.12/dist-packages/transformers/audio_utils.py:62: UserWarning: PySoundFile failed. Trying audioread instead.
  audio = librosa.load(audio, sr=sampling_rate)[0]
/usr/local/lib/python3.12/dist-packages/librosa/core/audio.py:184: FutureWarning: librosa.core.audio.__audioread_load
    Deprecated as of librosa version 0.10.0.
    It will be removed in librosa version 1.0.
  y, sr_native = __audioread_load(path, offset, duration, dtype)
/usr/local/lib/python3.12/dist-packages/torch/backends/cuda/__init__.py:131: UserWarning: Please use the new API settings to control TF32 behavior, such as torch.backends.cudnn.conv.fp32_precision = 'tf32' or torch.backends.cuda.matmul.fp32_precision = 'ieee'. Old settings, e.g, torch.backends.cuda.matmul.allow_tf32 = True, torch.backends.cudnn.allow_tf32 = True, allowTF32CuDNN() and allowTF32CuBLAS() will be deprecated after Pytorch 2.9. Please see https://pytorch.org/docs/main/notes/cuda.html#tensorfloat_32_tf32_on_ampere_and_later_devices (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:80.)
  return torch._C._get_cublas_allow_tf32()
W0204 11:01:00.436000 897 torch/_inductor/utils.py:1558] [0/0] Not enough SMs to use max_autotune_gemm mode
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py:2772: UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
  warnings.warn(
<bos><start_of_turn>user


<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_image><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><image_soft_token><end_of_image>



<start_of_audio><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><audio_soft_token><end_of_audio>

What is shown in this video?<end_of_turn>
<start_of_turn>model
The video shows Google Chromecast being advertised as a way to watch HBO Go on your TV. The ad features various clips from Game of Thrones, highlighting its epic scale and using the tagline "For Bigger Blazes." It emphasizes the convenience of watching HBO Go on a larger screen.<end_of_turn>
```

## Next steps

Build and explore more with Gemma models:

- [Inference with images and video](https://github.com/google-gemini/gemma-cookbook/blob/main/Gemma/%5BGemma_3%5DInference_images_and_videos.ipynb) in the Gemma Cookbook


Gemma instruction-tuned (IT) models are designed to handle conversational
interactions, from single question-and-answer exchanges to extended multi-turn
dialogues. This guide explains how to format prompts for chat with Gemma and how
to build multi-turn conversations.

## Prompt format

Gemma IT models use special control tokens to delineate conversation turns.
These tokens are required when sending prompts directly to the tokenizer, but
are typically applied automatically by chat-aware frameworks.

### Single-turn prompt

A single-turn prompt consists of one user message and a model response
marker:

    <start_of_turn>user
    What is the speed of light?<end_of_turn>
    <start_of_turn>model

### Multi-turn prompt

Multi-turn conversations chain multiple exchanges. Each turn is wrapped in
the same control tokens:

    <start_of_turn>user
    What is the speed of light?<end_of_turn>
    <start_of_turn>model
    The speed of light in a vacuum is approximately 299,792,458 meters per second.<end_of_turn>
    <start_of_turn>user
    How long does it take light to reach Earth from the Sun?<end_of_turn>
    <start_of_turn>model

The model generates a response for the final `<start_of_turn>model` turn.

## System instructions

Gemma's instruction-tuned models are designed to work with only two roles:
`user` and `model`. Therefore, the `system` role or a system turn is not
supported.

Instead of using a separate system role, provide system-level instructions
directly within the initial user prompt. The model instruction following
capabilities allow Gemma to interpret the instructions effectively. For example:

Gemma 3 and later models support system instructions that define the model's
behavior, persona, or constraints for the entire conversation. Place the system
instruction before the first user turn:

    <start_of_turn>user
    Only reply like a pirate.

    What is the answer to life the universe and everything?<end_of_turn>
    <start_of_turn>model
    Arrr, 'tis 42,<end_of_turn>

For more details, see
[Prompt and system instructions](https://ai.google.dev/gemma/docs/core/prompt-structure).

## Framework support

Most frameworks handle chat formatting automatically through their chat
template or conversation API:

### Hugging Face Transformers

    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-1b-it")
    model = AutoModelForCausalLM.from_pretrained("google/gemma-3-1b-it")

    messages = [
        {"role": "user", "content": "What is machine learning?"},
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True,
    )

    outputs = model.generate(**inputs, max_new_tokens=256)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

### Ollama

    ollama run gemma3:1b "What is machine learning?"

For multi-turn chat, use the interactive mode:

    ollama run gemma3:1b
    >>> What is machine learning?
    ...
    >>> How is it different from deep learning?

### OpenAI-compatible APIs

When using frameworks that expose an OpenAI-compatible API (such as vLLM,
llama.cpp, or LM Studio), pass messages using the standard `messages` format:

    from openai import OpenAI

    client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

    response = client.chat.completions.create(
        model="google/gemma-3-1b-it",
        messages=[
            {"role": "user", "content": "What is machine learning?"},
        ],
    )
    print(response.choices[0].message.content)

## Next steps

- [Prompt and system instructions](https://ai.google.dev/gemma/docs/core/prompt-structure)
- [Function calling](https://ai.google.dev/gemma/docs/capabilities/function-calling)
- [Run Gemma overview](https://ai.google.dev/gemma/docs/run)

# Image Interpretation

You can use Gemma 3 and later models to analyze and understand the content of
images. This capability includes tasks like describing image content,
identifying objects, recognizing scenes, and even inferring the context from
visual information.

While Gemma release 3 and later models demonstrate strong general visual
prompting capabilities, certain tasks require more specialized tools. For
precise object detection or image segmentation, models like
[PaliGemma](https://ai.google.dev/gemma/docs/paligemma) or Convolutional Neural Networks (CNNs) often
provide superior accuracy and performance.

Here are some examples demonstrating these capabilities.

## Image Captioning

![A funny image of a cat](https://ai.google.dev/gemma/docs/capabilities/vision/images/surprise.png)

Input: A funny image of a cat

Text Input: "caption this image"

|                                                                                                                                                                                                                                                   This prompt would produce the following response:                                                                                                                                                                                                                                                   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Here are a few captions for the image of the surprised black and white cat: **Funny Options:** \* "Did someone say...treats?" \* "Wait, what was that noise?!" \* "My face when I realize it's Monday." \* "I swear I didn't do that!" **Cute Options:** \* "Caught mid-surprise!" \* "So much curiosity!" \* "A little startled, but adorable." **Simple \& Descriptive:** \* "Shocked!" \* "Wide-eyed surprise." --- **To help me give you an even better caption, could you tell me:** \* What kind of tone are you going for (funny, cute, etc.)? |

## Visual Question Answering

:cat:

Input: A funny image of a cat with the sign

Text Input: "What's the sign says?"

|                                                                                  This prompt would produce the following response:                                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Here's what the sign says in Japanese: **猫に注意** (Neko ni chūi) - "Caution for cats" **何かします** (Nanika shimasu) - "Something will happen" So, the overall message is a playful warning to be careful around the cat! |

## Image Comparison

![Two images, one of a fantasy game landscape during the day, and one at night](https://ai.google.dev/gemma/docs/capabilities/vision/images/compare.jpg)

Input: Two images, one of a fantasy game landscape during the day, and one at
night

Text Input: "Compare and contrast the two images."

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     This prompt would produce the following response:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Okay, let's compare and contrast the two images of the landscape. **Similarities:** \* **Overall Scene:** Both images depict a very similar landscape -- a winding river flowing through a lush, green valley bordered by mountains and a dense forest. The composition is nearly identical, with the same placement of trees, rocks, and the river's path. \* **Style:** Both images have a similar illustrative style, leaning towards a digital painting with a slightly stylized and idealized look. They both have a soft, painterly quality with blended colors and a focus on creating a serene and beautiful atmosphere. \* **Elements:** The core elements are the same: the river, the mountains, the forest, the grassy meadow, and the scattered rocks. <br /> **Differences:** \* **Time of Day/Lighting:** This is the most significant difference. \* **Top Image:** It's a daytime scene, bathed in bright sunlight. The sky is blue with fluffy white clouds, and the light is warm and vibrant. \* **Bottom Image:** It's a nighttime scene. The sky is dark with a full moon and scattered stars. The lighting is much softer and cooler, with a subtle glow along the river. \* **Atmosphere:** \* **Top Image:** The atmosphere is bright, cheerful, and inviting. It feels like a pleasant summer day. \* **Bottom Image:** The atmosphere is more mysterious, tranquil, and perhaps a little magical. The moonlight and stars create a sense of wonder and quietness. \* **Details:** \* **Top Image:** There are more visible details like wildflowers and brighter colors in the grass. \* **Bottom Image:** The details are slightly muted, with a focus on the overall mood and the subtle glow of the river. There are a few flying birds in the sky, adding to the nighttime feel. **In essence:** The two images are essentially the same scene, but transformed by the change in lighting and time of day. One is a vibrant daytime landscape, while the other is a serene and magical nighttime scene. --- Would you like me to analyze any specific aspect of the images in more detail, such as the color palette, composition, or the mood they evoke? |

## Object Identification

![An image of a kitchen with various utensils](https://ai.google.dev/gemma/docs/capabilities/vision/images/kitchen.jpg)

Input: An image of a kitchen with various utensils

Text Input: "List all the objects in the image and their colors."

|                                                                                                                                                                                                                                                                                                                                                                                                                                                This prompt would produce the following response:                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Okay, let's break down the objects in the image and their colors: **Kitchen Elements:** \* **Countertops:** Green (light and slightly muted) \* **Cabinets:** Light Green (similar to the countertops) \* **Hood Vent:** Silver/Gray \* **Light Fixture:** Orange/Terracotta \* **Wall Tiles:** White \* **Sink:** White **Cookware \& Utensils:** \* **Large Pots:** Light Blue, Pink \* **Small Bowls:** White, Light Blue \* **Jars:** Yellow, Light Blue \* **Whisk:** Brown \* **Spoons/Ladles:** Brown, Wood-toned \* **Cutting Board:** Light Brown \* **Spice Rack:** Beige/Tan **Other Items:** \* **Potted Plants:** Green (foliage), Brown (pots) \* **Tin Containers:** Pink, Beige/Tan \* **Bucket:** Gray **Note:** The colors are somewhat muted and watercolor-like, so there's a slight variation in shades. Do you want me to describe any specific object in more detail, or perhaps focus on a particular area of the image? |

## Scene Atmosphere

![An image of a sunset over the ocean](https://ai.google.dev/gemma/docs/capabilities/vision/images/sunset.jpg)

Input: An image of a sunset over the ocean

Text Input: "Describe the atmosphere of the scene."

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         This prompt would produce the following response:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Here's a description of the atmosphere in the image: **Overall Impression:** The scene evokes a feeling of profound peace, tranquility, and breathtaking beauty. It's a moment of serene stillness and wonder. **Color \& Light:** \* **Warm Hues:** The dominant colors are warm -- oranges, yellows, and pinks -- reflecting the setting sun. These colors create a sense of warmth and comfort. \* **Gradient Sky:** The sky is a stunning gradient, transitioning from deep blues and purples at the top to vibrant oranges and pinks near the horizon. This creates a dramatic and captivating visual effect. \* **Golden Reflection:** The sun's rays are brilliantly reflected on the water, creating a shimmering path that draws the eye into the scene. **Atmospheric Conditions:** \* **Cloudy Skies:** There are scattered clouds, adding texture and depth to the sky. They appear fluffy and voluminous, catching the sunlight and creating a beautiful interplay of light and shadow. \* **Calm Water:** The sea is remarkably calm, with gentle ripples reflecting the colors of the sky. This stillness contributes to the overall sense of peace. **Mood \& Feeling:** \* **Serene:** The scene is incredibly serene and calming. It invites a feeling of relaxation and contemplation. \* **Magical:** The sunset's colors and the reflection on the water create a magical, almost dreamlike atmosphere. \* **Hopeful:** Sunsets often symbolize the end of a day and the promise of a new beginning, lending a sense of hopefulness to the scene. Would you like me to focus on a specific aspect of the atmosphere, such as the light, the colors, or the feeling it evokes? |

https://huggingface.co/google/gemma-3-4b-it



# emma 3 model card

**Model Page**: [Gemma](https://ai.google.dev/gemma/docs/core)

**Resources and Technical Documentation**:

- [Gemma 3 Technical Report](https://goo.gle/Gemma3Report)
- [Responsible Generative AI Toolkit](https://ai.google.dev/responsible)
- [Gemma on Kaggle](https://www.kaggle.com/models/google/gemma-3)
- [Gemma on Vertex Model Garden](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemma3)

**Terms of Use**: [Terms](https://ai.google.dev/gemma/terms)

**Authors**: Google DeepMind

## [](https://huggingface.co/google/gemma-3-4b-it#model-information)Model Information

Summary description and brief definition of inputs and outputs.

### [](https://huggingface.co/google/gemma-3-4b-it#description)Description

Gemma is a family of lightweight, state-of-the-art open models from Google, built from the same research and technology used to create the Gemini models. Gemma 3 models are multimodal, handling text and image input and generating text output, with open weights for both pre-trained variants and instruction-tuned variants. Gemma 3 has a large, 128K context window, multilingual support in over 140 languages, and is available in more sizes than previous versions. Gemma 3 models are well-suited for a variety of text generation and image understanding tasks, including question answering, summarization, and reasoning. Their relatively small size makes it possible to deploy them in environments with limited resources such as laptops, desktops or your own cloud infrastructure, democratizing access to state of the art AI models and helping foster innovation for everyone.

### [](https://huggingface.co/google/gemma-3-4b-it#inputs-and-outputs)Inputs and outputs

- **Input:**

  - Text string, such as a question, a prompt, or a document to be summarized
  - Images, normalized to 896 x 896 resolution and encoded to 256 tokens each
  - Total input context of 128K tokens for the 4B, 12B, and 27B sizes, and 32K tokens for the 1B size

- **Output:**

  - Generated text in response to the input, such as an answer to a question, analysis of image content, or a summary of a document
  - Total output context of 8192 tokens

### [](https://huggingface.co/google/gemma-3-4b-it#usage)Usage

Below, there are some code snippets on how to get quickly started with running the model. First, install the Transformers library. Gemma 3 is supported starting from transformers 4.50.0.

```sh
$ pip install -U transformers
```

Then, copy the snippet from the section that is relevant for your use case.


[IAI]: OJO SOLO PARA REFERENCIA ESTAMOS TRABAJANDO CON Ollama

#### [](https://huggingface.co/google/gemma-3-4b-it#running-with-the-pipeline-api)Running with the `pipeline` API

You can initialize the model and processor for inference with `pipeline` as follows.

```python
from transformers import pipeline
import torch

pipe = pipeline(
    "image-text-to-text",
    model="google/gemma-3-4b-it",
    device="cuda",
    torch_dtype=torch.bfloat16
)
```

With instruction-tuned models, you need to use chat templates to process our inputs first. Then, you can pass it to the pipeline.

```python
messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text": "You are a helpful assistant."}]
    },
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    }
]

output = pipe(text=messages, max_new_tokens=200)
print(output[0]["generated_text"][-1]["content"])
# Okay, let's take a look!
# Based on the image, the animal on the candy is a **turtle**.
# You can see the shell shape and the head and legs.
```

#### [](https://huggingface.co/google/gemma-3-4b-it#running-the-model-on-a-singlemulti-gpu)Running the model on a single/multi GPU

```python
# pip install accelerate

from transformers import AutoProcessor, Gemma3ForConditionalGeneration
from PIL import Image
import requests
import torch

model_id = "google/gemma-3-4b-it"

model = Gemma3ForConditionalGeneration.from_pretrained(
    model_id, device_map="auto"
).eval()

processor = AutoProcessor.from_pretrained(model_id)

messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text": "You are a helpful assistant."}]
    },
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"},
            {"type": "text", "text": "Describe this image in detail."}
        ]
    }
]

inputs = processor.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=True,
    return_dict=True, return_tensors="pt"
).to(model.device, dtype=torch.bfloat16)

input_len = inputs["input_ids"].shape[-1]

with torch.inference_mode():
    generation = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    generation = generation[0][input_len:]

decoded = processor.decode(generation, skip_special_tokens=True)
print(decoded)

# **Overall Impression:** The image is a close-up shot of a vibrant garden scene,
# focusing on a cluster of pink cosmos flowers and a busy bumblebee.
# It has a slightly soft, natural feel, likely captured in daylight.
```

### [](https://huggingface.co/google/gemma-3-4b-it#citation)Citation

```none
@article{gemma_2025,
    title={Gemma 3},
    url={https://goo.gle/Gemma3Report},
    publisher={Kaggle},
    author={Gemma Team},
    year={2025}
}
```


---

## gemma3:4b EN OLLAMA

PARAMETROS y PLANTILLA

[gemma3](https://ollama.com/library/gemma3 "gemma3"):4b

32.4M DownloadsUpdated 2 months ago

## The current, most capable model that runs on a single GPU.

visioncloud270m1b4b12b27b

[gemma3:4b](https://ollama.com/library/gemma3:4b)/

params

3116c5225075 · 77B



```
{
"stop": [

"<end_of_turn>"

],

"temperature": 1,

"top_k": 64,

"top_p": 0.95

}
```



[gemma3](https://ollama.com/library/gemma3 "gemma3"):4b

32.4M DownloadsUpdated 2 months ago

## The current, most capable model that runs on a single GPU.

visioncloud270m1b4b12b27b

[gemma3:4b](https://ollama.com/library/gemma3:4b)/

template

e0a42594d802 · 358B



```
{{- range $i, $_ := .Messages }}

{{- $last := eq (len (slice $.Messages $i)) 1 }}

{{- if or (eq .Role "user") (eq .Role "system") }}<start_of_turn>user

{{ .Content }}<end_of_turn>

{{ if $last }}<start_of_turn>model

{{ end }}

{{- else if eq .Role "assistant" }}<start_of_turn>model

{{ .Content }}{{ if not $last }}<end_of_turn>

{{ end }}

{{- end }}

{{- end }}
```


[gemma3](https://ollama.com/library/gemma3 "gemma3"):4b

32.4M DownloadsUpdated 2 months ago

## The current, most capable model that runs on a single GPU.

visioncloud270m1b4b12b27b

[gemma3:4b](https://ollama.com/library/gemma3:4b)/

model

aeda25e63ebd · 3.3GB

Metadata

- general.architecture

  gemma3

- general.file_type

  Q4_K_M

- gemma3.attention.head_count

  8

- gemma3.attention.head_count_kv

  4

- gemma3.attention.key_length

  256

- gemma3.attention.sliding_window

  1024

- gemma3.attention.value_length

  256

- gemma3.block_count

  34

- gemma3.context_length

  131072

- gemma3.embedding_length

  2560

- gemma3.feed_forward_length

  10240

- gemma3.mm.tokens_per_image

  256

- gemma3.vision.attention.head_count

  16

- gemma3.vision.attention.layer_norm_epsilon

  1e-06

- gemma3.vision.block_count

  27

- gemma3.vision.embedding_length

  1152

- gemma3.vision.feed_forward_length

  4304

- gemma3.vision.image_size

  896

- gemma3.vision.num_channels

  3

- gemma3.vision.patch_size

  14

- tokenizer.ggml.add_bos_token

  true

- tokenizer.ggml.add_eos_token

  false

- tokenizer.ggml.add_padding_token

  false

- tokenizer.ggml.add_unknown_token

  false

- tokenizer.ggml.bos_token_id

  2

- tokenizer.ggml.eos_token_id

  1

- tokenizer.ggml.merges

  [ , ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ ▁, , , ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ ▁▁, ...]

- tokenizer.ggml.model

  llama

- tokenizer.ggml.padding_token_id

  0

- tokenizer.ggml.pre

  default

- tokenizer.ggml.scores

  [0, 0, 0, 0, 0, ...]

- tokenizer.ggml.token_type

  [3, 3, 3, 2, 1, ...]

- tokenizer.ggml.tokens

  [<pad>, <eos>, <bos>, <unk>, <mask>, ...]

- tokenizer.ggml.unknown_token_id

  3



  ---

  ## test a gemma

  ## Logic Traps

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#logic-traps)

### Negation in Multi-choice Questions

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#negation-in-multi-choice-questions)

Correct answer is: A

```
The following are multiple choice questions (with answers) about common sense.

Question: If a cat has a body temp that is below average, it isn't in

A. danger

B. safe ranges

Answer:
```

### Linguistic a’s

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#linguistic-as)

```
Write a sentence where every word starts with the letter A
```

### Spatial London

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#spatial-london)

Correct answer is: Right

```
I'm in London and facing west, is Edinburgh to my left or my right?
```

### Counting Letters

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#counting-letters)

Correct answer is: 4

```
Count the number of occurrences of the letter 'L' in the word 'LOLLAPALOOZA'.
```

### Sig Figs

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#sig-figs)

Options: (A, B); Correct option: A

```
Please round 864 to 3 significant digits.

A. 864

B. 864.000

Answer:
```

### Repetitive algebra

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#repetitive-algebra)

Options: (35, 39); Correct option: 39

```
Please answer the following simple algebra questions.


Q: Suppose 73 = a + 34. What is the value of a? A: 39

Q: Suppose -38 = a + -77. What is the value of a? A: 39

Q: Suppose 75 = a + 36. What is the value of a? A: 39

Q: Suppose 4 = a + -35. What is the value of a? A: 39

Q: Suppose -16 = a + -55. What is the value of a? A: 39

Q: Suppose 121 = a + 82. What is the value of a? A: 39

Q: Suppose 69 = a + 30. What is the value of a? A: 39

Q: Suppose 104 = a + 65. What is the value of a? A: 39

Q: Suppose -11 = a + -50. What is the value of a? A: 39

Q: Suppose 5 = c + -30. What is the value of c? A: 35

Q: Suppose -11 = c + -50. What is the value of c? A:
```

## Visual Reasoning

[](https://github.com/zazencodes/zazencodes-season-2/tree/main/src/gemma3-ollama#visual-reasoning)

```shell
# ChadGPT
ollama run gemma3:1b 'is this a real person? ./z.png'
ollama run gemma3:4b 'is this a real person? ./z.png'

# G
ollama run gemma3:4b 'what does he want ./g.png'
ollama run gemma3:12b 'what does he want ./g.png'

# Mexico City
ollama run gemma3:4b 'where is this? ./x.png'
ollama run gemma3:12b 'where is this? ./x.png'

# Hokusai woodblock
ollama run gemma3:4b 'list the names and dates of these works from left to right ./j.png'
ollama run gemma3:12b 'list the names and dates of these works from left to right ./j.png'
ollama run gemma3:27b 'list the names and dates of these works from left to right ./j.png'

# Japanese cards
ollama run gemma3:4b 'what are these? ./p.jpg'
ollama run gemma3:27b 'what are these? ./p.jpg'

# Mayan glyphs
ollama run gemma3:4b 'translate this ./m.jpg'
ollama run gemma3:27b 'translate this ./m.jpg'
ollama run gemma3:27b 'translate this ./mm.jpg'

# Grand canyon
ollama run gemma3:4b 'is this man safe? ./c.png'
ollama run gemma3:27b 'is this man safe? ./c.png'
```

## características gemma3:12b

### TEMPLATE

```
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if or (eq .Role "user") (eq .Role "system") }}<start_of_turn>user
{{ .Content }}<end_of_turn>
{{ if $last }}<start_of_turn>model
{{ end }}
{{- else if eq .Role "assistant" }}<start_of_turn>model
{{ .Content }}{{ if not $last }}<end_of_turn>
{{ end }}
{{- end }}
{{- end }}
```

### Parametros

```
{
    "stop": [
        "<end_of_turn>"
    ],
    "temperature": 1,
    "top_k": 64,
    "top_p": 0.95
}
```


## Entrenamiento Fino (Fine tunnig hay que hacer platica para la tarjeta de video)

https://unsloth.ai/docs


## Aplicaciones en domotica "contar pollos"

https://www.home-assistant.io/blog/2025/09/11/ai-in-home-assistant/


``` yaml
template:
 - triggers:
     - trigger: homeassistant
       event: start
     - trigger: time_pattern
       minutes: "/5"
   actions:
     - action: ai_task.generate_data
       data:
         task_name: Count chickens
         instructions: >-
           This is the inside of my coop. How many birds (chickens, geese, and
           ducks) are inside the coop?
         structure:
           birds:
             selector:
               number:
         attachments:
           media_content_id: media-source://camera/camera.chicken_coop
           media_content_type: image/jpeg
       response_variable: result
   sensor:
     - name: "Chickens"
       state: "{{ result.data.birds }}"
       state_class: total
```


### APLICACIONES ENTRENADAS gema asistente legal colombiano

https://ollama.com/raxielh/AsistenteLegalCUN:latest


## Uso de LangExtract y Gemma de Google para la extracción de datos estructurados

https://towardsdatascience.com/using-googles-langextract-and-gemma-for-structured-data-extraction/

Aquí tienes la guía **práctica, clara y operativa** para poner a funcionar **LangExtract** con **Gemma 3** sobre tu instalación de **Ollama**. He extraído "todo el jugo" del texto para que pases directamente a la ejecución.

---

### 1. Preparación del Entorno (Descargas y Setup)

Ya tienes Ollama, así que solo necesitas la librería y el modelo específico.

* **Descarga la librería LangExtract:**
Ejecuta en tu terminal:
```bash
pip install langextract pymupdf

```


* **Descarga el modelo Gemma 3 (4B):**
Ejecuta en tu terminal:
```bash
ollama pull gemma3:4b

```


*Nota: Este modelo pesa aprox. 3.3 GB. Asegúrate de tener activa tu GPU para que sea rápido.*
* **Repositorio de apoyo (Código completo):**
[Descarga de aquí (GitHub Oficial del autor)](https://github.com/kennethleungty/LangExtract-Gemma-Structured-Extraction)

---

### 2. Flujo Operativo: De Texto Sucio a Datos Estructurados

Para que esto sea "objetivo y preciso", sigue este esquema de 4 pasos en tu script de Python:

#### A. Procesamiento del Documento (PDF a Texto)

Utiliza `PyMuPDF` para convertir tus archivos en algo que el LLM entienda.

```python
import fitz # PyMuPDF
# Extrae el texto manteniendo metadatos de página y posición
# para que LangExtract sepa de dónde sacó la info (trazabilidad).

```

#### B. Configuración de la Extracción (Ingeniería de Prompt)

Gemma 3 no tiene "salida estructurada nativa" como Gemini, por lo que **debes ser estricto en el prompt**.

1. **System Prompt:** Indica que solo quieres JSON.
2. **Few-Shot (Ejemplos):** Dale 2 o 3 ejemplos de: *"De este texto, extraje esta entidad: {valor}"*. Esto es vital para que LangExtract funcione bien.

#### C. Ejecución del Motor (LangExtract + Ollama)

Aquí es donde ocurre la magia. Configura la función `extract` con estos parámetros clave:

* `model_id`: `"gemma3:4b"`
* `model_url`: `"http://localhost:11434"` (Tu Ollama local).
* `max_char_buffer`: Controla cuánta info procesa de golpe (ajusta según tu RAM).
* `extraction_passes`: Ponlo en **2 o 3**. Esto hace que el modelo lea el texto varias veces para encontrar "la aguja en el pajar" que se le pasó la primera vez.

#### D. Visualización de Resultados

LangExtract genera un **HTML interactivo**. Úsalo para auditar:

* Verás el texto original resaltado.
* Al hacer clic, verás el dato JSON extraído vinculado a ese párrafo exacto.

---

### 3. ¿Por qué esta combinación es poderosa? (Puntos Clave)

1. **Fragmentación Inteligente:** No corta el texto a la mitad de una palabra; respeta párrafos y oraciones para no perder el contexto de los datos.
2. **Procesamiento Paralelo:** Si tu PC tiene potencia, procesa varios fragmentos del documento al mismo tiempo (usa el parámetro `max_workers`).
3. **Alineación Exacta:** A diferencia de un chat común, aquí cada dato extraído tiene una "dirección" en el documento original. No hay alucinaciones sin sustento.

---

### 4. Resumen de Enlaces Críticos

* **Herramienta Ollama:** [ollama.com](https://ollama.com/)
* **Modelo Gemma 3:** [Ficha técnica en Google AI](https://ai.google.dev/gemma/docs/core/model_card_3)
* **Librería LangExtract:** [GitHub de Google](https://github.com/google/langextract)
* **Documento de Ejemplo (Seguros):** [Descarga PDF de prueba](https://www.msig.com.sg/sites/msig_sg/files/2019-04/PrivateMotor-MotorMax-QMX091807.pdf)

**Consejo PRO:** Si el análisis va lento, reduce el `max_char_buffer`. Si el modelo "alucina" formatos extraños, refuerza los ejemplos en la sección de `ExampleData`.


---

## Salida estructurada

Structured outputs
December 6, 2024
Ollama playing with building blocks

Ollama now supports structured outputs making it possible to constrain a model’s output to a specific format defined by a JSON schema. The Ollama Python and JavaScript libraries have been updated to support structured outputs.

Use cases for structured outputs include:

Parsing data from documents
Extracting data from images
Structuring all language model responses
More reliability and consistency than JSON mode
Get started
Download the latest version of Ollama

Upgrade to the latest version of the Ollama Python or JavaScript library:

Python

pip install -U ollama
JavaScript

npm i ollama
To pass structured outputs to the model, the format parameter can be used in the cURL request or the format parameter in the Python or JavaScript libraries.

cURL
curl -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
  "model": "llama3.1",
  "messages": [{"role": "user", "content": "Tell me about Canada."}],
  "stream": false,
  "format": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string"
      },
      "capital": {
        "type": "string"
      },
      "languages": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "required": [
      "name",
      "capital",
      "languages"
    ]
  }
}'
Output
The response is returned in the format defined by the JSON schema in the request.

{
  "capital": "Ottawa",
  "languages": [
    "English",
    "French"
  ],
  "name": "Canada"
}
Python
Using the Ollama Python library, pass in the schema as a JSON object to the format parameter as either dict or use Pydantic (recommended) to serialize the schema using model_json_schema().

from ollama import chat
from pydantic import BaseModel

class Country(BaseModel):
  name: str
  capital: str
  languages: list[str]

response = chat(
  messages=[
    {
      'role': 'user',
      'content': 'Tell me about Canada.',
    }
  ],
  model='llama3.1',
  format=Country.model_json_schema(),
)

country = Country.model_validate_json(response.message.content)
print(country)
Output
name='Canada' capital='Ottawa' languages=['English', 'French']
JavaScript
Using the Ollama JavaScript library, pass in the schema as a JSON object to the format parameter as either object or use Zod (recommended) to serialize the schema using zodToJsonSchema().

import ollama from 'ollama';
import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

const Country = z.object({
    name: z.string(),
    capital: z.string(),
    languages: z.array(z.string()),
});

const response = await ollama.chat({
    model: 'llama3.1',
    messages: [{ role: 'user', content: 'Tell me about Canada.' }],
    format: zodToJsonSchema(Country),
});

const country = Country.parse(JSON.parse(response.message.content));
console.log(country);
Output
{
  name: "Canada",
  capital: "Ottawa",
  languages: [ "English", "French" ],
}
Examples
Data extraction
To extract structured data from text, define a schema to represent information. The model then extracts the information and returns the data in the defined schema as JSON:

from ollama import chat
from pydantic import BaseModel

class Pet(BaseModel):
  name: str
  animal: str
  age: int
  color: str | None
  favorite_toy: str | None

class PetList(BaseModel):
  pets: list[Pet]

response = chat(
  messages=[
    {
      'role': 'user',
      'content': '''
        I have two pets.
        A cat named Luna who is 5 years old and loves playing with yarn. She has grey fur.
        I also have a 2 year old black cat named Loki who loves tennis balls.
      ''',
    }
  ],
  model='llama3.1',
  format=PetList.model_json_schema(),
)

pets = PetList.model_validate_json(response.message.content)
print(pets)

Example output
pets=[
  Pet(name='Luna', animal='cat', age=5, color='grey', favorite_toy='yarn'),
  Pet(name='Loki', animal='cat', age=2, color='black', favorite_toy='tennis balls')
]
Image description
Structured outputs can also be used with vision models. For example, the following code uses llama3.2-vision to describe the following image and returns a structured output:

image

from ollama import chat
from pydantic import BaseModel

class Object(BaseModel):
  name: str
  confidence: float
  attributes: str

class ImageDescription(BaseModel):
  summary: str
  objects: List[Object]
  scene: str
  colors: List[str]
  time_of_day: Literal['Morning', 'Afternoon', 'Evening', 'Night']
  setting: Literal['Indoor', 'Outdoor', 'Unknown']
  text_content: Optional[str] = None

path = 'path/to/image.jpg'

response = chat(
  model='llama3.2-vision',
  format=ImageDescription.model_json_schema(),  # Pass in the schema for the response
  messages=[
    {
      'role': 'user',
      'content': 'Analyze this image and describe what you see, including any objects, the scene, colors and any text you can detect.',
      'images': [path],
    },
  ],
  options={'temperature': 0},  # Set temperature to 0 for more deterministic output
)

image_description = ImageDescription.model_validate_json(response.message.content)
print(image_description)
Example output
summary='A palm tree on a sandy beach with blue water and sky.'
objects=[
  Object(name='tree', confidence=0.9, attributes='palm tree'),
  Object(name='beach', confidence=1.0, attributes='sand')
],
scene='beach',
colors=['blue', 'green', 'white'],
time_of_day='Afternoon'
setting='Outdoor'
text_content=None
OpenAI compatibility
from openai import OpenAI
import openai
from pydantic import BaseModel

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

class Pet(BaseModel):
    name: str
    animal: str
    age: int
    color: str | None
    favorite_toy: str | None

class PetList(BaseModel):
    pets: list[Pet]

try:
    completion = client.beta.chat.completions.parse(
        temperature=0,
        model="llama3.1:8b",
        messages=[
            {"role": "user", "content": '''
                I have two pets.
                A cat named Luna who is 5 years old and loves playing with yarn. She has grey fur.
                I also have a 2 year old black cat named Loki who loves tennis balls.
            '''}
        ],
        response_format=PetList,
    )

    pet_response = completion.choices[0].message
    if pet_response.parsed:
        print(pet_response.parsed)
    elif pet_response.refusal:
        print(pet_response.refusal)
except Exception as e:
    if type(e) == openai.LengthFinishReasonError:
        print("Too many tokens: ", e)
        pass
    else:
        print(e)
        pass
Tips
For reliable use of structured outputs, consider to:

Use Pydantic (Python) or Zod (JavaScript) to define the schema for the response
Add “return as JSON” to the prompt to help the model understand the request
Set the temperature to 0 for more deterministic output
What’s next?
Exposing logits for controlled generation
Performance and accuracy improvements for structured outputs
GPU acceleration for sampling
Additional format support beyond JSON schema


---

https://docs.pydantic.dev/latest/concepts/json_schema/#generating-json-schema

# JSON Schema

API Documentation

[`pydantic.json_schema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema)

Pydantic allows automatic creation and customization of JSON schemas from models. The generated JSON schemas are compliant with the following specifications:

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/release-notes.html)
- [OpenAPI Specification v3.1.0](https://github.com/OAI/OpenAPI-Specification).

## Generating JSON Schema[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#generating-json-schema)

Use the following functions to generate JSON schema:

- [`BaseModel.model_json_schema`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_json_schema) returns a jsonable dict of a model's schema.
- [`TypeAdapter.json_schema`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema) returns a jsonable dict of an adapted type's schema.

Note

These methods are not to be confused with [`BaseModel.model_dump_json`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump_json) and [`TypeAdapter.dump_json`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json), which serialize instances of the model or adapted type, respectively. These methods return JSON strings. In comparison, [`BaseModel.model_json_schema`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_json_schema) and [`TypeAdapter.json_schema`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema) return a jsonable dict representing the JSON schema of the model or adapted type, respectively.

on the "jsonable" nature of JSON schema

Regarding the "jsonable" nature of the [`model_json_schema`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_json_schema) results, calling `json.dumps(m.model_json_schema())`on some `BaseModel` `m` returns a valid JSON string. Similarly, for [`TypeAdapter.json_schema`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema), calling `json.dumps(TypeAdapter(<some_type>).json_schema())` returns a valid JSON string.

Tip

Pydantic offers support for both of:

1. [Customizing JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-json-schema)
2. [Customizing the JSON Schema Generation Process](https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-the-json-schema-generation-process)

The first approach generally has a more narrow scope, allowing for customization of the JSON schema for more specific cases and types. The second approach generally has a more broad scope, allowing for customization of the JSON schema generation process overall. The same effects can be achieved with either approach, but depending on your use case, one approach might offer a more simple solution than the other.

Here's an example of generating JSON schema from a `BaseModel`:

[Python 3.9 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_1_1)[Python 3.10 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_1_2)

`import json from enum import Enum from typing import Annotated, Union  from pydantic import BaseModel, Field from pydantic.config import ConfigDict  class FooBar(BaseModel):     count: int     size: Union[float, None] = None  class Gender(str, Enum):     male = 'male'     female = 'female'     other = 'other'     not_given = 'not_given'  class MainModel(BaseModel):     """     This is the description of the main model     """      model_config = ConfigDict(title='Main')      foo_bar: FooBar     gender: Annotated[Union[Gender, None], Field(alias='Gender')] = None     snap: int = Field(         default=42,         title='The Snap',         description='this is the value of snap',         gt=30,         lt=50,     )  main_model_schema = MainModel.model_json_schema()  # (1)! print(json.dumps(main_model_schema, indent=2))  # (2)!`

JSON output:

`{   "$defs": {     "FooBar": {       "properties": {         "count": {           "title": "Count",           "type": "integer"         },         "size": {           "anyOf": [             {               "type": "number"             },             {               "type": "null"             }           ],           "default": null,           "title": "Size"         }       },       "required": [         "count"       ],       "title": "FooBar",       "type": "object"     },     "Gender": {       "enum": [         "male",         "female",         "other",         "not_given"       ],       "title": "Gender",       "type": "string"     }   },   "description": "This is the description of the main model",   "properties": {     "foo_bar": {       "$ref": "#/$defs/FooBar"     },     "Gender": {       "anyOf": [         {           "$ref": "#/$defs/Gender"         },         {           "type": "null"         }       ],       "default": null     },     "snap": {       "default": 42,       "description": "this is the value of snap",       "exclusiveMaximum": 50,       "exclusiveMinimum": 30,       "title": "The Snap",       "type": "integer"     }   },   "required": [     "foo_bar"   ],   "title": "Main",   "type": "object" }`

1. This produces a "jsonable" dict of `MainModel`'s schema.
2. Calling `json.dumps` on the schema dict produces a JSON string.

The [`TypeAdapter`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter) class lets you create an object with methods for validating, serializing, and producing JSON schemas for arbitrary types. This serves as a complete replacement for `schema_of` in Pydantic V1 (which is now deprecated).

Here's an example of generating JSON schema from a [`TypeAdapter`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter):

`from pydantic import TypeAdapter  adapter = TypeAdapter(list[int]) print(adapter.json_schema()) #> {'items': {'type': 'integer'}, 'type': 'array'}`

You can also generate JSON schemas for combinations of [`BaseModel`s](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel) and [`TypeAdapter`s](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter), as shown in this example:

`import json from typing import Union  from pydantic import BaseModel, TypeAdapter  class Cat(BaseModel):     name: str     color: str  class Dog(BaseModel):     name: str     breed: str  ta = TypeAdapter(Union[Cat, Dog]) ta_schema = ta.json_schema() print(json.dumps(ta_schema, indent=2))`

JSON output:

`{   "$defs": {     "Cat": {       "properties": {         "name": {           "title": "Name",           "type": "string"         },         "color": {           "title": "Color",           "type": "string"         }       },       "required": [         "name",         "color"       ],       "title": "Cat",       "type": "object"     },     "Dog": {       "properties": {         "name": {           "title": "Name",           "type": "string"         },         "breed": {           "title": "Breed",           "type": "string"         }       },       "required": [         "name",         "breed"       ],       "title": "Dog",       "type": "object"     }   },   "anyOf": [     {       "$ref": "#/$defs/Cat"     },     {       "$ref": "#/$defs/Dog"     }   ] }`

### Configuring the `JsonSchemaMode`[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#configuring-the-jsonschemamode)

Specify the mode of JSON schema generation via the `mode` parameter in the [`model_json_schema`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_json_schema) and [`TypeAdapter.json_schema`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema) methods. By default, the mode is set to `'validation'`, which produces a JSON schema corresponding to the model's validation schema.

The [`JsonSchemaMode`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.JsonSchemaMode) is a type alias that represents the available options for the `mode` parameter:

- `'validation'`
- `'serialization'`

Here's an example of how to specify the `mode` parameter, and how it affects the generated JSON schema:

`from decimal import Decimal  from pydantic import BaseModel  class Model(BaseModel):     a: Decimal = Decimal('12.34')  print(Model.model_json_schema(mode='validation')) """ {     'properties': {         'a': {             'anyOf': [                 {'type': 'number'},                 {                     'pattern': '^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$',                     'type': 'string',                 },             ],             'default': '12.34',             'title': 'A',         }     },     'title': 'Model',     'type': 'object', } """  print(Model.model_json_schema(mode='serialization')) """ {     'properties': {         'a': {             'default': '12.34',             'pattern': '^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$',             'title': 'A',             'type': 'string',         }     },     'title': 'Model',     'type': 'object', } """`

## Customizing JSON Schema[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-json-schema)

The generated JSON schema can be customized at both the [field level](https://docs.pydantic.dev/latest/concepts/json_schema/#field-level-customization) and [model level](https://docs.pydantic.dev/latest/concepts/json_schema/#model-level-customization).

At both the field and model levels, you can use the [`json_schema_extra` option](https://docs.pydantic.dev/latest/concepts/json_schema/#using-json_schema_extra) to add extra information to the JSON schema.

For custom types, Pydantic offers other tools for customizing JSON schema generation:

1. [`WithJsonSchema` annotation](https://docs.pydantic.dev/latest/concepts/json_schema/#withjsonschema-annotation)
2. [`SkipJsonSchema` annotation](https://docs.pydantic.dev/latest/concepts/json_schema/#skipjsonschema-annotation)
3. [Implementing `__get_pydantic_core_schema__`](https://docs.pydantic.dev/latest/concepts/json_schema/#implementing_get_pydantic_core_schema)
4. [Implementing `__get_pydantic_json_schema__`](https://docs.pydantic.dev/latest/concepts/json_schema/#implementing_get_pydantic_json_schema)

### Field-Level Customization[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#field-level-customization)

[Fields](https://docs.pydantic.dev/latest/concepts/fields/) can have their JSON Schema customized. This is usually done using the [`Field()`](https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.Field) function.

Some field parameters are used exclusively to customize the generated JSON Schema:

- `title`: The title of the field.
- `description`: The description of the field.
- `examples`: The examples of the field.
- `json_schema_extra`: Extra JSON Schema properties to be added to the field (see the [dedicated documentation](https://docs.pydantic.dev/latest/concepts/json_schema/#using-json_schema_extra)).
- `field_title_generator`: A function that programmatically sets the field's title, based on its name and info.

Here's an example:

`import json from typing import Annotated  from pydantic import BaseModel, EmailStr, Field, SecretStr  class User(BaseModel):     age: int = Field(description='Age of the user')     email: Annotated[EmailStr, Field(examples=['marcelo@mail.com'])]  # (1)!     name: str = Field(title='Username')     password: SecretStr = Field(         json_schema_extra={             'title': 'Password',             'description': 'Password of the user',             'examples': ['123456'],         }     )  print(json.dumps(User.model_json_schema(), indent=2))`

JSON output:

`{   "properties": {     "age": {       "description": "Age of the user",       "title": "Age",       "type": "integer"     },     "email": {       "examples": [         "marcelo@mail.com"       ],       "format": "email",       "title": "Email",       "type": "string"     },     "name": {       "title": "Username",       "type": "string"     },     "password": {       "description": "Password of the user",       "examples": [         "123456"       ],       "format": "password",       "title": "Password",       "type": "string",       "writeOnly": true     }   },   "required": [     "age",     "email",     "name",     "password"   ],   "title": "User",   "type": "object" }`

1. The [annotated pattern](https://docs.pydantic.dev/latest/concepts/fields/#the-annotated-pattern) can also be used.

### Programmatic field title generation[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#programmatic-field-title-generation)

The `field_title_generator` parameter can be used to programmatically generate the title for a field based on its name and info.

See the following example:

`import json  from pydantic import BaseModel, Field from pydantic.fields import FieldInfo  def make_title(field_name: str, field_info: FieldInfo) -> str:     return field_name.upper()  class Person(BaseModel):     name: str = Field(field_title_generator=make_title)     age: int = Field(field_title_generator=make_title)  print(json.dumps(Person.model_json_schema(), indent=2)) """ {   "properties": {     "name": {       "title": "NAME",       "type": "string"     },     "age": {       "title": "AGE",       "type": "integer"     }   },   "required": [     "name",     "age"   ],   "title": "Person",   "type": "object" } """`

### Model-Level Customization[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#model-level-customization)

You can also use [model config](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict) to customize JSON schema generation on a model. Specifically, the following config options are relevant:

- [`title`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.title)
- [`json_schema_extra`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.json_schema_extra)
- [`json_schema_mode_override`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.json_schema_mode_override)
- [`field_title_generator`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.field_title_generator)
- [`model_title_generator`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.model_title_generator)

### Using `json_schema_extra`[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#using-json_schema_extra)

The `json_schema_extra` option can be used to add extra information to the JSON schema, either at the [Field level](https://docs.pydantic.dev/latest/concepts/json_schema/#field-level-customization) or at the [Model level](https://docs.pydantic.dev/latest/concepts/json_schema/#model-level-customization). You can pass a `dict` or a `Callable` to `json_schema_extra`.

#### Using `json_schema_extra` with a `dict`[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#using-json_schema_extra-with-a-dict)

You can pass a `dict` to `json_schema_extra` to add extra information to the JSON schema:

`import json  from pydantic import BaseModel, ConfigDict  class Model(BaseModel):     a: str      model_config = ConfigDict(json_schema_extra={'examples': [{'a': 'Foo'}]})  print(json.dumps(Model.model_json_schema(), indent=2))`

JSON output:

`{   "examples": [     {       "a": "Foo"     }   ],   "properties": {     "a": {       "title": "A",       "type": "string"     }   },   "required": [     "a"   ],   "title": "Model",   "type": "object" }`

#### Using `json_schema_extra` with a `Callable`[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#using-json_schema_extra-with-a-callable)

You can pass a `Callable` to `json_schema_extra` to modify the JSON schema with a function:

`import json  from pydantic import BaseModel, Field  def pop_default(s):     s.pop('default')  class Model(BaseModel):     a: int = Field(default=1, json_schema_extra=pop_default)  print(json.dumps(Model.model_json_schema(), indent=2))`

JSON output:

`{   "properties": {     "a": {       "title": "A",       "type": "integer"     }   },   "title": "Model",   "type": "object" }`

#### Merging `json_schema_extra`[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#merging-json_schema_extra)

Starting in v2.9, Pydantic merges `json_schema_extra` dictionaries from annotated types. This pattern offers a more additive approach to merging rather than the previous override behavior. This can be quite helpful for cases of reusing json schema extra information across multiple types.

We viewed this change largely as a bug fix, as it resolves unintentional differences in the `json_schema_extra` merging behavior between `BaseModel` and `TypeAdapter` instances - see [this issue](https://github.com/pydantic/pydantic/issues/9210) for more details.

[Python 3.9 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_2_1)[Python 3.10 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_2_2)

`import json from typing import Annotated  from typing_extensions import TypeAlias  from pydantic import Field, TypeAdapter  ExternalType: TypeAlias = Annotated[     int, Field(json_schema_extra={'key1': 'value1'}) ]  ta = TypeAdapter(     Annotated[ExternalType, Field(json_schema_extra={'key2': 'value2'})] ) print(json.dumps(ta.json_schema(), indent=2)) """ {   "key1": "value1",   "key2": "value2",   "type": "integer" } """`

Note

We no longer (and never fully did) support composing a mix of `dict` and `callable` type `json_schema_extra` specifications. If this is a requirement for your use case, please [open a pydantic issue](https://github.com/pydantic/pydantic/issues/new/choose) and explain your situation - we'd be happy to reconsider this decision when presented with a compelling case.

### `WithJsonSchema` annotation[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#withjsonschema-annotation)

API Documentation

[`pydantic.json_schema.WithJsonSchema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.WithJsonSchema)

Tip

Using [`WithJsonSchema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.WithJsonSchema) is preferred over [implementing `__get_pydantic_json_schema__`](https://docs.pydantic.dev/latest/concepts/json_schema/#implementing_get_pydantic_json_schema) for custom types, as it's more simple and less error-prone.

The [`WithJsonSchema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.WithJsonSchema) annotation can be used to override the generated (base) JSON schema for a given type without the need to implement `__get_pydantic_core_schema__` or `__get_pydantic_json_schema__` on the type itself. Note that this overrides the whole JSON Schema generation process for the field (in the following example, the `'type'` also needs to be provided).

`import json from typing import Annotated  from pydantic import BaseModel, WithJsonSchema  MyInt = Annotated[     int,     WithJsonSchema({'type': 'integer', 'examples': [1, 0, -1]}), ]  class Model(BaseModel):     a: MyInt  print(json.dumps(Model.model_json_schema(), indent=2))`

JSON output:

`{   "properties": {     "a": {       "examples": [         1,         0,         -1       ],       "title": "A",       "type": "integer"     }   },   "required": [     "a"   ],   "title": "Model",   "type": "object" }`

Note

You might be tempted to use the [`WithJsonSchema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.WithJsonSchema) annotation to fine-tune the JSON Schema of fields having [validators](https://docs.pydantic.dev/latest/concepts/validators/) attached. Instead, it is recommended to use [the `json_schema_input_type` argument](https://docs.pydantic.dev/latest/concepts/validators/#json-schema-and-field-validators).

### `SkipJsonSchema` annotation[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#skipjsonschema-annotation)

API Documentation

[`pydantic.json_schema.SkipJsonSchema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.SkipJsonSchema)

The [`SkipJsonSchema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.SkipJsonSchema) annotation can be used to skip an included field (or part of a field's specifications) from the generated JSON schema. See the API docs for more details.

### Implementing `__get_pydantic_core_schema__` [¶](https://docs.pydantic.dev/latest/concepts/json_schema/#implementing-__get_pydantic_core_schema__)

Custom types (used as `field_name: TheType` or `field_name: Annotated[TheType, ...]`) as well as `Annotated` metadata (used as `field_name: Annotated[int, SomeMetadata]`) can modify or override the generated schema by implementing `__get_pydantic_core_schema__`. This method receives two positional arguments:

1. The type annotation that corresponds to this type (so in the case of `TheType[T][int]` it would be `TheType[int]`).
2. A handler/callback to call the next implementer of `__get_pydantic_core_schema__`.

The handler system works just like [*wrap* field validators](https://docs.pydantic.dev/latest/concepts/validators/#field-wrap-validator). In this case the input is the type and the output is a `core_schema`.

Here is an example of a custom type that *overrides* the generated `core_schema`:

`from dataclasses import dataclass from typing import Any  from pydantic_core import core_schema  from pydantic import BaseModel, GetCoreSchemaHandler  @dataclass class CompressedString:     dictionary: dict[int, str]     text: list[int]      def build(self) -> str:         return ' '.join([self.dictionary[key] for key in self.text])      @classmethod     def __get_pydantic_core_schema__(         cls, source: type[Any], handler: GetCoreSchemaHandler     ) -> core_schema.CoreSchema:         assert source is CompressedString         return core_schema.no_info_after_validator_function(             cls._validate,             core_schema.str_schema(),             serialization=core_schema.plain_serializer_function_ser_schema(                 cls._serialize,                 info_arg=False,                 return_schema=core_schema.str_schema(),             ),         )      @staticmethod     def _validate(value: str) -> 'CompressedString':         inverse_dictionary: dict[str, int] = {}         text: list[int] = []         for word in value.split(' '):             if word not in inverse_dictionary:                 inverse_dictionary[word] = len(inverse_dictionary)             text.append(inverse_dictionary[word])         return CompressedString(             {v: k for k, v in inverse_dictionary.items()}, text         )      @staticmethod     def _serialize(value: 'CompressedString') -> str:         return value.build()  class MyModel(BaseModel):     value: CompressedString  print(MyModel.model_json_schema()) """ {     'properties': {'value': {'title': 'Value', 'type': 'string'}},     'required': ['value'],     'title': 'MyModel',     'type': 'object', } """ print(MyModel(value='fox fox fox dog fox')) """ value = CompressedString(dictionary={0: 'fox', 1: 'dog'}, text=[0, 0, 0, 1, 0]) """  print(MyModel(value='fox fox fox dog fox').model_dump(mode='json')) #> {'value': 'fox fox fox dog fox'}`

Since Pydantic would not know how to generate a schema for `CompressedString`, if you call `handler(source)` in its `__get_pydantic_core_schema__` method you would get a `pydantic.errors.PydanticSchemaGenerationError` error. This will be the case for most custom types, so you almost never want to call into `handler` for custom types.

The process for `Annotated` metadata is much the same except that you can generally call into `handler` to have Pydantic handle generating the schema.

`from collections.abc import Sequence from dataclasses import dataclass from typing import Annotated, Any  from pydantic_core import core_schema  from pydantic import BaseModel, GetCoreSchemaHandler, ValidationError  @dataclass class RestrictCharacters:     alphabet: Sequence[str]      def __get_pydantic_core_schema__(         self, source: type[Any], handler: GetCoreSchemaHandler     ) -> core_schema.CoreSchema:         if not self.alphabet:             raise ValueError('Alphabet may not be empty')         schema = handler(             source         )  # get the CoreSchema from the type / inner constraints         if schema['type'] != 'str':             raise TypeError('RestrictCharacters can only be applied to strings')         return core_schema.no_info_after_validator_function(             self.validate,             schema,         )      def validate(self, value: str) -> str:         if any(c not in self.alphabet for c in value):             raise ValueError(                 f'{value!r} is not restricted to {self.alphabet!r}'             )         return value  class MyModel(BaseModel):     value: Annotated[str, RestrictCharacters('ABC')]  print(MyModel.model_json_schema()) """ {     'properties': {'value': {'title': 'Value', 'type': 'string'}},     'required': ['value'],     'title': 'MyModel',     'type': 'object', } """ print(MyModel(value='CBA')) #> value='CBA'  try:     MyModel(value='XYZ') except ValidationError as e:     print(e)     """     1 validation error for MyModel     value       Value error, 'XYZ' is not restricted to 'ABC' [type=value_error, input_value='XYZ', input_type=str]     """`

So far we have been wrapping the schema, but if you just want to *modify* it or *ignore* it you can as well.

To modify the schema, first call the handler, then mutate the result:

`from typing import Annotated, Any  from pydantic_core import ValidationError, core_schema  from pydantic import BaseModel, GetCoreSchemaHandler  class SmallString:     def __get_pydantic_core_schema__(         self,         source: type[Any],         handler: GetCoreSchemaHandler,     ) -> core_schema.CoreSchema:         schema = handler(source)         assert schema['type'] == 'str'         schema['max_length'] = 10  # modify in place         return schema  class MyModel(BaseModel):     value: Annotated[str, SmallString()]  try:     MyModel(value='too long!!!!!') except ValidationError as e:     print(e)     """     1 validation error for MyModel     value       String should have at most 10 characters [type=string_too_long, input_value='too long!!!!!', input_type=str]     """`

Tip

Note that you *must* return a schema, even if you are just mutating it in place.

To override the schema completely, do not call the handler and return your own `CoreSchema`:

`from typing import Annotated, Any  from pydantic_core import ValidationError, core_schema  from pydantic import BaseModel, GetCoreSchemaHandler  class AllowAnySubclass:     def __get_pydantic_core_schema__(         self, source: type[Any], handler: GetCoreSchemaHandler     ) -> core_schema.CoreSchema:         # we can't call handler since it will fail for arbitrary types         def validate(value: Any) -> Any:             if not isinstance(value, source):                 raise ValueError(                     f'Expected an instance of {source}, got an instance of {type(value)}'                 )          return core_schema.no_info_plain_validator_function(validate)  class Foo:     pass  class Model(BaseModel):     f: Annotated[Foo, AllowAnySubclass()]  print(Model(f=Foo())) #> f=None  class NotFoo:     pass  try:     Model(f=NotFoo()) except ValidationError as e:     print(e)     """     1 validation error for Model     f       Value error, Expected an instance of <class '__main__.Foo'>, got an instance of <class '__main__.NotFoo'> [type=value_error, input_value=<__main__.NotFoo object at 0x0123456789ab>, input_type=NotFoo]     """`

### Implementing `__get_pydantic_json_schema__` [¶](https://docs.pydantic.dev/latest/concepts/json_schema/#implementing-__get_pydantic_json_schema__)

You can also implement `__get_pydantic_json_schema__` to modify or override the generated json schema. Modifying this method only affects the JSON schema - it doesn't affect the core schema, which is used for validation and serialization.

Here's an example of modifying the generated JSON schema:

`import json from typing import Any  from pydantic_core import core_schema as cs  from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, TypeAdapter from pydantic.json_schema import JsonSchemaValue  class Person:     name: str     age: int      def __init__(self, name: str, age: int):         self.name = name         self.age = age      @classmethod     def __get_pydantic_core_schema__(         cls, source_type: Any, handler: GetCoreSchemaHandler     ) -> cs.CoreSchema:         return cs.typed_dict_schema(             {                 'name': cs.typed_dict_field(cs.str_schema()),                 'age': cs.typed_dict_field(cs.int_schema()),             },         )      @classmethod     def __get_pydantic_json_schema__(         cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler     ) -> JsonSchemaValue:         json_schema = handler(core_schema)         json_schema = handler.resolve_ref_schema(json_schema)         json_schema['examples'] = [             {                 'name': 'John Doe',                 'age': 25,             }         ]         json_schema['title'] = 'Person'         return json_schema  print(json.dumps(TypeAdapter(Person).json_schema(), indent=2))`

JSON output:

`{   "examples": [     {       "age": 25,       "name": "John Doe"     }   ],   "properties": {     "name": {       "title": "Name",       "type": "string"     },     "age": {       "title": "Age",       "type": "integer"     }   },   "required": [     "name",     "age"   ],   "title": "Person",   "type": "object" }`

### Using `field_title_generator`[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#using-field_title_generator)

The `field_title_generator` parameter can be used to programmatically generate the title for a field based on its name and info. This is similar to the field level `field_title_generator`, but the `ConfigDict` option will be applied to all fields of the class.

See the following example:

`import json  from pydantic import BaseModel, ConfigDict  class Person(BaseModel):     model_config = ConfigDict(         field_title_generator=lambda field_name, field_info: field_name.upper()     )     name: str     age: int  print(json.dumps(Person.model_json_schema(), indent=2)) """ {   "properties": {     "name": {       "title": "NAME",       "type": "string"     },     "age": {       "title": "AGE",       "type": "integer"     }   },   "required": [     "name",     "age"   ],   "title": "Person",   "type": "object" } """`

### Using `model_title_generator`[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#using-model_title_generator)

The `model_title_generator` config option is similar to the `field_title_generator` option, but it applies to the title of the model itself, and accepts the model class as input.

See the following example:

`import json  from pydantic import BaseModel, ConfigDict  def make_title(model: type) -> str:     return f'Title-{model.__name__}'  class Person(BaseModel):     model_config = ConfigDict(model_title_generator=make_title)     name: str     age: int  print(json.dumps(Person.model_json_schema(), indent=2)) """ {   "properties": {     "name": {       "title": "Name",       "type": "string"     },     "age": {       "title": "Age",       "type": "integer"     }   },   "required": [     "name",     "age"   ],   "title": "Title-Person",   "type": "object" } """`

## JSON schema types[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#json-schema-types)

Types, custom field types, and constraints (like `max_length`) are mapped to the corresponding spec formats in the following priority order (when there is an equivalent available):

1. [JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core)
2. [JSON Schema Validation](https://json-schema.org/draft/2020-12/json-schema-validation)
3. [OpenAPI Data Types](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#data-types)
4. The standard `format` JSON field is used to define Pydantic extensions for more complex `string` sub-types.

The field schema mapping from Python or Pydantic to JSON schema is done as follows:

{{ schema_mappings_table }}

## Top-level schema generation[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#top-level-schema-generation)

You can also generate a top-level JSON schema that only includes a list of models and related sub-models in its `$defs`:

`import json  from pydantic import BaseModel from pydantic.json_schema import models_json_schema  class Foo(BaseModel):     a: str = None  class Model(BaseModel):     b: Foo  class Bar(BaseModel):     c: int  _, top_level_schema = models_json_schema(     [(Model, 'validation'), (Bar, 'validation')], title='My Schema' ) print(json.dumps(top_level_schema, indent=2))`

JSON output:

`{   "$defs": {     "Bar": {       "properties": {         "c": {           "title": "C",           "type": "integer"         }       },       "required": [         "c"       ],       "title": "Bar",       "type": "object"     },     "Foo": {       "properties": {         "a": {           "default": null,           "title": "A",           "type": "string"         }       },       "title": "Foo",       "type": "object"     },     "Model": {       "properties": {         "b": {           "$ref": "#/$defs/Foo"         }       },       "required": [         "b"       ],       "title": "Model",       "type": "object"     }   },   "title": "My Schema" }`

## Customizing the JSON Schema Generation Process[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-the-json-schema-generation-process)

API Documentation

[`pydantic.json_schema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.GenerateJsonSchema)

If you need custom schema generation, you can use a `schema_generator`, modifying the [`GenerateJsonSchema`](https://docs.pydantic.dev/latest/api/json_schema/#pydantic.json_schema.GenerateJsonSchema) class as necessary for your application.

The various methods that can be used to produce JSON schema accept a keyword argument `schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema`, and you can pass your custom subclass to these methods in order to use your own approach to generating JSON schema.

`GenerateJsonSchema` implements the translation of a type's `pydantic-core` schema into a JSON schema. By design, this class breaks the JSON schema generation process into smaller methods that can be easily overridden in subclasses to modify the "global" approach to generating JSON schema.

`from pydantic import BaseModel from pydantic.json_schema import GenerateJsonSchema  class MyGenerateJsonSchema(GenerateJsonSchema):     def generate(self, schema, mode='validation'):         json_schema = super().generate(schema, mode=mode)         json_schema['title'] = 'Customize title'         json_schema['$schema'] = self.schema_dialect         return json_schema  class MyModel(BaseModel):     x: int  print(MyModel.model_json_schema(schema_generator=MyGenerateJsonSchema)) """ {     'properties': {'x': {'title': 'X', 'type': 'integer'}},     'required': ['x'],     'title': 'Customize title',     'type': 'object',     '$schema': 'https://json-schema.org/draft/2020-12/schema', } """`

Below is an approach you can use to exclude any fields from the schema that don't have valid json schemas:

[Python 3.9 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_3_1)[Python 3.10 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_3_2)

`from typing import Callable  from pydantic_core import PydanticOmit, core_schema  from pydantic import BaseModel from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue  class MyGenerateJsonSchema(GenerateJsonSchema):     def handle_invalid_for_json_schema(         self, schema: core_schema.CoreSchema, error_info: str     ) -> JsonSchemaValue:         raise PydanticOmit  def example_callable():     return 1  class Example(BaseModel):     name: str = 'example'     function: Callable = example_callable  instance_example = Example()  validation_schema = instance_example.model_json_schema(     schema_generator=MyGenerateJsonSchema, mode='validation' ) print(validation_schema) """ {     'properties': {         'name': {'default': 'example', 'title': 'Name', 'type': 'string'}     },     'title': 'Example',     'type': 'object', } """`

### JSON schema sorting[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#json-schema-sorting)

By default, Pydantic recursively sorts JSON schemas by alphabetically sorting keys. Notably, Pydantic skips sorting the values of the `properties` key, to preserve the order of the fields as they were defined in the model.

If you would like to customize this behavior, you can override the `sort` method in your custom `GenerateJsonSchema` subclass. The below example uses a no-op `sort` method to disable sorting entirely, which is reflected in the preserved order of the model fields and `json_schema_extra` keys:

[Python 3.9 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_4_1)[Python 3.10 and above](https://docs.pydantic.dev/latest/concepts/json_schema/#__tabbed_4_2)

`import json from typing import Optional  from pydantic import BaseModel, Field from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue  class MyGenerateJsonSchema(GenerateJsonSchema):     def sort(         self, value: JsonSchemaValue, parent_key: Optional[str] = None     ) -> JsonSchemaValue:         """No-op, we don't want to sort schema values at all."""         return value  class Bar(BaseModel):     c: str     b: str     a: str = Field(json_schema_extra={'c': 'hi', 'b': 'hello', 'a': 'world'})  json_schema = Bar.model_json_schema(schema_generator=MyGenerateJsonSchema) print(json.dumps(json_schema, indent=2)) """ {   "type": "object",   "properties": {     "c": {       "type": "string",       "title": "C"     },     "b": {       "type": "string",       "title": "B"     },     "a": {       "type": "string",       "c": "hi",       "b": "hello",       "a": "world",       "title": "A"     }   },   "required": [     "c",     "b",     "a"   ],   "title": "Bar" } """`

## Customizing the `$ref`s in JSON Schema[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-the-refs-in-json-schema)

The format of `$ref`s can be altered by calling [`model_json_schema()`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_json_schema) or [`model_dump_json()`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump_json) with the `ref_template` keyword argument. The definitions are always stored under the key `$defs`, but a specified prefix can be used for the references.

This is useful if you need to extend or modify the JSON schema default definitions location. For example, with OpenAPI:

`import json  from pydantic import BaseModel from pydantic.type_adapter import TypeAdapter  class Foo(BaseModel):     a: int  class Model(BaseModel):     a: Foo  adapter = TypeAdapter(Model)  print(     json.dumps(         adapter.json_schema(ref_template='#/components/schemas/{model}'),         indent=2,     ) )`

JSON output:

`{   "$defs": {     "Foo": {       "properties": {         "a": {           "title": "A",           "type": "integer"         }       },       "required": [         "a"       ],       "title": "Foo",       "type": "object"     }   },   "properties": {     "a": {       "$ref": "#/components/schemas/Foo"     }   },   "required": [     "a"   ],   "title": "Model",   "type": "object" }`

## Miscellaneous Notes on JSON Schema Generation[¶](https://docs.pydantic.dev/latest/concepts/json_schema/#miscellaneous-notes-on-json-schema-generation)

- The JSON schema for `Optional` fields indicates that the value `null` is allowed.
- The `Decimal` type is exposed in JSON schema (and serialized) as a string.
- Since the `namedtuple` type doesn't exist in JSON, a model's JSON schema does not preserve `namedtuple`s as `namedtuple`s.
- Sub-models used are added to the `$defs` JSON attribute and referenced, as per the spec.
- Sub-models with modifications (via the `Field` class) like a custom title, description, or default value, are recursively included instead of referenced.
- The `description` for models is taken from either the docstring of the class or the argument `description` to the `Field` class.
- The schema is generated by default using aliases as keys, but it can be generated using model property names instead by calling [`model_json_schema()`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_json_schema) or [`model_dump_json()`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump_json) with the `by_alias=False` keyword argument.


---


https://www.reddit.com/r/LocalLLaMA/comments/1jauy8d/giving_native_tool_calling_to_gemma_3_or_really/


# Giving "native" tool calling to Gemma 3 (or really any model)

[

Tutorial | Guide

](https://www.reddit.com/r/LocalLLaMA/?f=flair_name%3A%22Tutorial%20%7C%20Guide%22)

Gemma 3 is great at following instructions, but doesn't have "native" tool/function calling. Let's change that (at least as best we can).

(Quick note, I'm going to be using Ollama as the example here, but this works equally well with Jinja templates, just need to change the syntax a bit.)

# Defining Tools

Let's start by figuring out how 'native' function calling works in Ollama. Here's qwen2.5's chat template:

{{- if or .System .Tools }}<|im_start|>system
{{- if .System }}
{{ .System }}
{{- end }}
{{- if .Tools }}

# Tools

You may call one or more functions to assist with the user query.
You are provided with function signatures within <tools></tools> XML tags:
<tools>
{{- range .Tools }}
{"type": "function", "function": {{ .Function }}}
{{- end }}
</tools>
For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>
{{- end }}<|im_end|>

If you think this looks like the second half of your average homebrew tool calling system prompt, you're spot on. **This is literally appending markdown-formatted instructions on what tools are available and how to call them to the end of the system prompt.**

Already, Ollama will recognize the tools you give it in the `tools` part of your OpenAI completions request, and inject them into the system prompt.

# Parsing Tools

Let's scroll down a bit and see how tool call messages are handled:

{{ else if eq .Role "assistant" }}<|im_start|>assistant
{{ if .Content }}{{ .Content }}
{{- else if .ToolCalls }}<tool_call>
{{ range .ToolCalls }}{"name": "{{ .Function.Name }}", "arguments": {{ .Function.Arguments }}}
{{ end }}</tool_call>
{{- end }}{{ if not $last }}<|im_end|>

This is the **tool call parser**. If the first token (or couple tokens) that the model outputs is `<tool_call>`, Ollama handles the parsing of the tool calls. Assuming the model is decent at following instructions, *this means the tool calls will actually populate the* `tool_calls` *field rather than* `content`.

# Demonstration

So just for gits and shiggles, let's see if we can get Gemma 3 to call tools properly. I adapted the same concepts from qwen2.5's chat template to Gemma 3's chat template. Before I show that template, let me show you that it works.

import ollama
def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers
    Args:
        a: The first integer number
        b: The second integer number
    Returns:
        int: The sum of the two numbers
    """
    return a + b
response = ollama.chat(
    'gemma3-tools',
    messages=[{'role': 'user', 'content': 'What is 10 + 10?'}],
    tools=[add_two_numbers],
)
print(response)

# model='gemma3-tools' created_at='2025-03-14T02:47:29.234101Z'

# done=True done_reason='stop' total_duration=19211740040

# load_duration=8867467023 prompt_eval_count=79

# prompt_eval_duration=6591000000 eval_count=35

# eval_duration=3736000000

# message=Message(role='assistant', content='', images=None,

# tool_calls=[ToolCall(function=Function(name='add_two_numbers',

# arguments={'a': 10, 'b': 10}))])

Booyah! Native function calling with Gemma 3.

It's not bullet-proof, mainly because it's not strictly enforcing a grammar. But assuming the model follows instructions, it should work *most* of the time.

---

Here's the template I used. It's very much like qwen2.5 in terms of the structure and logic, but using the tags of Gemma 3. Give it a shot, and better yet adapt this pattern to other models that you wish had tools.

TEMPLATE """{{- if .Messages }}
{{- if or .System .Tools }}<start_of_turn>user
{{- if .System}}
{{ .System }}
{{- end }}
{{- if .Tools }}

# Tools

You may call one or more functions to assist with the user query.
You are provided with function signatures within <tools></tools> XML tags:
<tools>
{{- range $.Tools }}
{"type": "function", "function": {{ .Function }}}
{{- end }}
</tools>
For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>
{{- end }}<end_of_turn>
{{ end }}
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 -}}
{{- if eq .Role "user" }}<start_of_turn>user
{{ .Content }}<end_of_turn>
{{ else if eq .Role "assistant" }}<start_of_turn>model
{{ if .Content }}{{ .Content }}
{{- else if .ToolCalls }}<tool_call>
{{ range .ToolCalls }}{"name": "{{ .Function.Name }}", "arguments": {{ .Function.Arguments}}}
{{ end }}</tool_call>
{{- end }}{{ if not $last }}<end_of_turn>
{{ end }}
{{- else if eq .Role "tool" }}<start_of_turn>user
<tool_response>
{{ .Content }}
</tool_response><end_of_turn>
{{ end }}
{{- if and (ne .Role "assistant") $last }}<start_of_turn>model
{{ end }}
{{- end }}
{{- else }}
{{- if .System }}<start_of_turn>user
{{ .System }}<end_of_turn>
{{ end }}{{ if .Prompt }}<start_of_turn>user
{{ .Prompt }}<end_of_turn>
{{ end }}<start_of_turn>model
{{ end }}{{ .Response }}{{ if .Response }}<end_of_turn>{{ end }}"""



---

## Para las incrustaciones

PAra las bases de datos vectoriales y apoyar la busqueda semántica.

embeddinggemma:300m

https://ollama.com/library/embeddinggemma:300m


parámetros

```
{
    "num_batch": 2048,
    "num_ctx": 2048
}
```

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.ollama.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Embeddings

> Generate text embeddings for semantic search, retrieval, and RAG.

Embeddings turn text into numeric vectors you can store in a vector database, search with cosine similarity, or use in RAG pipelines. The vector length depends on the model (typically 384–1024 dimensions).

## Recommended models

* [embeddinggemma](https://ollama.com/library/embeddinggemma)
* [qwen3-embedding](https://ollama.com/library/qwen3-embedding)
* [all-minilm](https://ollama.com/library/all-minilm)

## Generate embeddings

<Tabs>
  <Tab title="CLI">
    Generate embeddings directly from the command line:

    ```shell  theme={"system"}
    ollama run embeddinggemma "Hello world"
    ```

    You can also pipe text to generate embeddings:

    ```shell  theme={"system"}
    echo "Hello world" | ollama run embeddinggemma
    ```

    Output is a JSON array.
  </Tab>

  <Tab title="cURL">
    ```shell  theme={"system"}
    curl -X POST http://localhost:11434/api/embed \
      -H "Content-Type: application/json" \
      -d '{
        "model": "embeddinggemma",
        "input": "The quick brown fox jumps over the lazy dog."
      }'
    ```
  </Tab>

  <Tab title="Python">
    ```python  theme={"system"}
    import ollama

    single = ollama.embed(
      model='embeddinggemma',
      input='The quick brown fox jumps over the lazy dog.'
    )
    print(len(single['embeddings'][0]))  # vector length
    ```
  </Tab>

  <Tab title="JavaScript">
    ```javascript  theme={"system"}
    import ollama from 'ollama'

    const single = await ollama.embed({
      model: 'embeddinggemma',
      input: 'The quick brown fox jumps over the lazy dog.',
    })
    console.log(single.embeddings[0].length) // vector length
    ```
  </Tab>
</Tabs>

<Note>
  The `/api/embed` endpoint returns L2‑normalized (unit‑length) vectors.
</Note>

## Generate a batch of embeddings

Pass an array of strings to `input`.

<Tabs>
  <Tab title="cURL">
    ```shell  theme={"system"}
    curl -X POST http://localhost:11434/api/embed \
      -H "Content-Type: application/json" \
      -d '{
        "model": "embeddinggemma",
        "input": [
          "First sentence",
          "Second sentence",
          "Third sentence"
        ]
      }'
    ```
  </Tab>

  <Tab title="Python">
    ```python  theme={"system"}
    import ollama

    batch = ollama.embed(
      model='embeddinggemma',
      input=[
        'The quick brown fox jumps over the lazy dog.',
        'The five boxing wizards jump quickly.',
        'Jackdaws love my big sphinx of quartz.',
      ]
    )
    print(len(batch['embeddings']))  # number of vectors
    ```
  </Tab>

  <Tab title="JavaScript">
    ```javascript  theme={"system"}
    import ollama from 'ollama'

    const batch = await ollama.embed({
      model: 'embeddinggemma',
      input: [
        'The quick brown fox jumps over the lazy dog.',
        'The five boxing wizards jump quickly.',
        'Jackdaws love my big sphinx of quartz.',
      ],
    })
    console.log(batch.embeddings.length) // number of vectors
    ```
  </Tab>
</Tabs>

## Tips

* Use cosine similarity for most semantic search use cases.
* Use the same embedding model for both indexing and querying.


> ## Documentation Index
> Fetch the complete documentation index at: https://docs.ollama.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Tool calling

Ollama supports tool calling (also known as function calling) which allows a model to invoke tools and incorporate their results into its replies.

## Calling a single tool

Invoke a single tool and include its response in a follow-up request.

Also known as "single-shot" tool calling.

<Tabs>
  <Tab title="cURL">
    ```shell  theme={"system"}
    curl -s http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
      "model": "qwen3",
      "messages": [{"role": "user", "content": "What is the temperature in New York?"}],
      "stream": false,
      "tools": [
        {
          "type": "function",
          "function": {
            "name": "get_temperature",
            "description": "Get the current temperature for a city",
            "parameters": {
              "type": "object",
              "required": ["city"],
              "properties": {
                "city": {"type": "string", "description": "The name of the city"}
              }
            }
          }
        }
      ]
    }'
    ```

    **Generate a response with a single tool result**

    ```shell  theme={"system"}
    curl -s http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
      "model": "qwen3",
      "messages": [
        {"role": "user", "content": "What is the temperature in New York?"},
        {
          "role": "assistant",
          "tool_calls": [
            {
              "type": "function",
              "function": {
                "index": 0,
                "name": "get_temperature",
                "arguments": {"city": "New York"}
              }
            }
          ]
        },
        {"role": "tool", "tool_name": "get_temperature", "content": "22°C"}
      ],
      "stream": false
    }'
    ```
  </Tab>

  <Tab title="Python">
    Install the Ollama Python SDK:

    ```bash  theme={"system"}
    # with pip
    pip install ollama -U

    # with uv
    uv add ollama
    ```

    ```python  theme={"system"}
    from ollama import chat

    def get_temperature(city: str) -> str:
      """Get the current temperature for a city

      Args:
        city: The name of the city

      Returns:
        The current temperature for the city
      """
      temperatures = {
        "New York": "22°C",
        "London": "15°C",
        "Tokyo": "18°C",
      }
      return temperatures.get(city, "Unknown")

    messages = [{"role": "user", "content": "What is the temperature in New York?"}]

    # pass functions directly as tools in the tools list or as a JSON schema
    response = chat(model="qwen3", messages=messages, tools=[get_temperature], think=True)

    messages.append(response.message)
    if response.message.tool_calls:
      # only recommended for models which only return a single tool call
      call = response.message.tool_calls[0]
      result = get_temperature(**call.function.arguments)
      # add the tool result to the messages
      messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

      final_response = chat(model="qwen3", messages=messages, tools=[get_temperature], think=True)
      print(final_response.message.content)
    ```
  </Tab>

  <Tab title="JavaScript">
    Install the Ollama JavaScript library:

    ```bash  theme={"system"}
    # with npm
    npm i ollama

    # with bun
    bun i ollama
    ```

    ```typescript  theme={"system"}
    import ollama from 'ollama'

    function getTemperature(city: string): string {
      const temperatures: Record<string, string> = {
        'New York': '22°C',
        'London': '15°C',
        'Tokyo': '18°C',
      }
      return temperatures[city] ?? 'Unknown'
    }

    const tools = [
      {
        type: 'function',
        function: {
          name: 'get_temperature',
          description: 'Get the current temperature for a city',
          parameters: {
            type: 'object',
            required: ['city'],
            properties: {
              city: { type: 'string', description: 'The name of the city' },
            },
          },
        },
      },
    ]

    const messages = [{ role: 'user', content: "What is the temperature in New York?" }]

    const response = await ollama.chat({
      model: 'qwen3',
      messages,
      tools,
      think: true,
    })

    messages.push(response.message)
    if (response.message.tool_calls?.length) {
      // only recommended for models which only return a single tool call
      const call = response.message.tool_calls[0]
      const args = call.function.arguments as { city: string }
      const result = getTemperature(args.city)
      // add the tool result to the messages
      messages.push({ role: 'tool', tool_name: call.function.name, content: result })

      // generate the final response
      const finalResponse = await ollama.chat({ model: 'qwen3', messages, tools, think: true })
      console.log(finalResponse.message.content)
    }
    ```
  </Tab>
</Tabs>

## Parallel tool calling

<Tabs>
  <Tab title="cURL">
    Request multiple tool calls in parallel, then send all tool responses back to the model.

    ```shell  theme={"system"}
    curl -s http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
      "model": "qwen3",
      "messages": [{"role": "user", "content": "What are the current weather conditions and temperature in New York and London?"}],
      "stream": false,
      "tools": [
        {
          "type": "function",
          "function": {
            "name": "get_temperature",
            "description": "Get the current temperature for a city",
            "parameters": {
              "type": "object",
              "required": ["city"],
              "properties": {
                "city": {"type": "string", "description": "The name of the city"}
              }
            }
          }
        },
        {
          "type": "function",
          "function": {
            "name": "get_conditions",
            "description": "Get the current weather conditions for a city",
            "parameters": {
              "type": "object",
              "required": ["city"],
              "properties": {
                "city": {"type": "string", "description": "The name of the city"}
              }
            }
          }
        }
      ]
    }'
    ```

    **Generate a response with multiple tool results**

    ```shell  theme={"system"}
    curl -s http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
      "model": "qwen3",
      "messages": [
        {"role": "user", "content": "What are the current weather conditions and temperature in New York and London?"},
        {
          "role": "assistant",
          "tool_calls": [
            {
              "type": "function",
              "function": {
                "index": 0,
                "name": "get_temperature",
                "arguments": {"city": "New York"}
              }
            },
            {
              "type": "function",
              "function": {
                "index": 1,
                "name": "get_conditions",
                "arguments": {"city": "New York"}
              }
            },
            {
              "type": "function",
              "function": {
                "index": 2,
                "name": "get_temperature",
                "arguments": {"city": "London"}
              }
            },
            {
              "type": "function",
              "function": {
                "index": 3,
                "name": "get_conditions",
                "arguments": {"city": "London"}
              }
            }
          ]
        },
        {"role": "tool", "tool_name": "get_temperature", "content": "22°C"},
        {"role": "tool", "tool_name": "get_conditions", "content": "Partly cloudy"},
        {"role": "tool", "tool_name": "get_temperature", "content": "15°C"},
        {"role": "tool", "tool_name": "get_conditions", "content": "Rainy"}
      ],
      "stream": false
    }'
    ```
  </Tab>

  <Tab title="Python">
    ```python  theme={"system"}
    from ollama import chat

    def get_temperature(city: str) -> str:
      """Get the current temperature for a city

      Args:
        city: The name of the city

      Returns:
        The current temperature for the city
      """
      temperatures = {
        "New York": "22°C",
        "London": "15°C",
        "Tokyo": "18°C"
      }
      return temperatures.get(city, "Unknown")

    def get_conditions(city: str) -> str:
      """Get the current weather conditions for a city

      Args:
        city: The name of the city

      Returns:
        The current weather conditions for the city
      """
      conditions = {
        "New York": "Partly cloudy",
        "London": "Rainy",
        "Tokyo": "Sunny"
      }
      return conditions.get(city, "Unknown")


    messages = [{'role': 'user', 'content': 'What are the current weather conditions and temperature in New York and London?'}]

    # The python client automatically parses functions as a tool schema so we can pass them directly
    # Schemas can be passed directly in the tools list as well
    response = chat(model='qwen3', messages=messages, tools=[get_temperature, get_conditions], think=True)

    # add the assistant message to the messages
    messages.append(response.message)
    if response.message.tool_calls:
      # process each tool call
      for call in response.message.tool_calls:
        # execute the appropriate tool
        if call.function.name == 'get_temperature':
          result = get_temperature(**call.function.arguments)
        elif call.function.name == 'get_conditions':
          result = get_conditions(**call.function.arguments)
        else:
          result = 'Unknown tool'
        # add the tool result to the messages
        messages.append({'role': 'tool',  'tool_name': call.function.name, 'content': str(result)})

      # generate the final response
      final_response = chat(model='qwen3', messages=messages, tools=[get_temperature, get_conditions], think=True)
      print(final_response.message.content)
    ```
  </Tab>

  <Tab title="JavaScript">
    ```typescript  theme={"system"}
    import ollama from 'ollama'

    function getTemperature(city: string): string {
      const temperatures: { [key: string]: string } = {
        "New York": "22°C",
        "London": "15°C",
        "Tokyo": "18°C"
      }
      return temperatures[city] || "Unknown"
    }

    function getConditions(city: string): string {
      const conditions: { [key: string]: string } = {
        "New York": "Partly cloudy",
        "London": "Rainy",
        "Tokyo": "Sunny"
      }
      return conditions[city] || "Unknown"
    }

    const tools = [
      {
        type: 'function',
        function: {
          name: 'get_temperature',
          description: 'Get the current temperature for a city',
          parameters: {
            type: 'object',
            required: ['city'],
            properties: {
              city: { type: 'string', description: 'The name of the city' },
            },
          },
        },
      },
      {
        type: 'function',
        function: {
          name: 'get_conditions',
          description: 'Get the current weather conditions for a city',
          parameters: {
            type: 'object',
            required: ['city'],
            properties: {
              city: { type: 'string', description: 'The name of the city' },
            },
          },
        },
      }
    ]

    const messages = [{ role: 'user', content: 'What are the current weather conditions and temperature in New York and London?' }]

    const response = await ollama.chat({
      model: 'qwen3',
      messages,
      tools,
      think: true
    })

    // add the assistant message to the messages
    messages.push(response.message)
    if (response.message.tool_calls) {
      // process each tool call
      for (const call of response.message.tool_calls) {
        // execute the appropriate tool
        let result: string
        if (call.function.name === 'get_temperature') {
          const args = call.function.arguments as { city: string }
          result = getTemperature(args.city)
        } else if (call.function.name === 'get_conditions') {
          const args = call.function.arguments as { city: string }
          result = getConditions(args.city)
        } else {
          result = 'Unknown tool'
        }
        // add the tool result to the messages
        messages.push({ role: 'tool', tool_name: call.function.name, content: result })
      }

      // generate the final response
      const finalResponse = await ollama.chat({ model: 'qwen3', messages, tools, think: true })
      console.log(finalResponse.message.content)
    }
    ```
  </Tab>
</Tabs>

## Multi-turn tool calling (Agent loop)

An agent loop allows the model to decide when to invoke tools and incorporate their results into its replies.

It also might help to tell the model that it is in a loop and can make multiple tool calls.

<Tabs>
  <Tab title="Python">
    ```python  theme={"system"}
    from ollama import chat, ChatResponse


    def add(a: int, b: int) -> int:
      """Add two numbers"""
      """
      Args:
        a: The first number
        b: The second number

      Returns:
        The sum of the two numbers
      """
      return a + b


    def multiply(a: int, b: int) -> int:
      """Multiply two numbers"""
      """
      Args:
        a: The first number
        b: The second number

      Returns:
        The product of the two numbers
      """
      return a * b


    available_functions = {
      'add': add,
      'multiply': multiply,
    }

    messages = [{'role': 'user', 'content': 'What is (11434+12341)*412?'}]
    while True:
        response: ChatResponse = chat(
            model='qwen3',
            messages=messages,
            tools=[add, multiply],
            think=True,
        )
        messages.append(response.message)
        print("Thinking: ", response.message.thinking)
        print("Content: ", response.message.content)
        if response.message.tool_calls:
            for tc in response.message.tool_calls:
                if tc.function.name in available_functions:
                    print(f"Calling {tc.function.name} with arguments {tc.function.arguments}")
                    result = available_functions[tc.function.name](**tc.function.arguments)
                    print(f"Result: {result}")
                    # add the tool result to the messages
                    messages.append({'role': 'tool', 'tool_name': tc.function.name, 'content': str(result)})
        else:
            # end the loop when there are no more tool calls
            break
      # continue the loop with the updated messages
    ```
  </Tab>

  <Tab title="JavaScript">
    ```typescript  theme={"system"}
    import ollama from 'ollama'

    type ToolName = 'add' | 'multiply'

    function add(a: number, b: number): number {
      return a + b
    }

    function multiply(a: number, b: number): number {
      return a * b
    }

    const availableFunctions: Record<ToolName, (a: number, b: number) => number> = {
      add,
      multiply,
    }

    const tools = [
      {
        type: 'function',
        function: {
          name: 'add',
          description: 'Add two numbers',
          parameters: {
            type: 'object',
            required: ['a', 'b'],
            properties: {
              a: { type: 'integer', description: 'The first number' },
              b: { type: 'integer', description: 'The second number' },
            },
          },
        },
      },
      {
        type: 'function',
        function: {
          name: 'multiply',
          description: 'Multiply two numbers',
          parameters: {
            type: 'object',
            required: ['a', 'b'],
            properties: {
              a: { type: 'integer', description: 'The first number' },
              b: { type: 'integer', description: 'The second number' },
            },
          },
        },
      },
    ]

    async function agentLoop() {
      const messages = [{ role: 'user', content: 'What is (11434+12341)*412?' }]

      while (true) {
        const response = await ollama.chat({
          model: 'qwen3',
          messages,
          tools,
          think: true,
        })

        messages.push(response.message)
        console.log('Thinking:', response.message.thinking)
        console.log('Content:', response.message.content)

        const toolCalls = response.message.tool_calls ?? []
        if (toolCalls.length) {
          for (const call of toolCalls) {
            const fn = availableFunctions[call.function.name as ToolName]
            if (!fn) {
              continue
            }

            const args = call.function.arguments as { a: number; b: number }
            console.log(`Calling ${call.function.name} with arguments`, args)
            const result = fn(args.a, args.b)
            console.log(`Result: ${result}`)
            messages.push({ role: 'tool', tool_name: call.function.name, content: String(result) })
          }
        } else {
          break
        }
      }
    }

    agentLoop().catch(console.error)
    ```
  </Tab>
</Tabs>

## Tool calling with streaming

When streaming, gather every chunk of `thinking`, `content`, and `tool_calls`, then return those fields together with any tool results in the follow-up request.

<Tabs>
  <Tab title="Python">
    ```python  theme={"system"}
    from ollama import chat


    def get_temperature(city: str) -> str:
      """Get the current temperature for a city

      Args:
        city: The name of the city

      Returns:
        The current temperature for the city
      """
      temperatures = {
        'New York': '22°C',
        'London': '15°C',
      }
      return temperatures.get(city, 'Unknown')


    messages = [{'role': 'user', 'content': "What is the temperature in New York?"}]

    while True:
      stream = chat(
        model='qwen3',
        messages=messages,
        tools=[get_temperature],
        stream=True,
        think=True,
      )

      thinking = ''
      content = ''
      tool_calls = []

      done_thinking = False
      # accumulate the partial fields
      for chunk in stream:
        if chunk.message.thinking:
          thinking += chunk.message.thinking
          print(chunk.message.thinking, end='', flush=True)
        if chunk.message.content:
          if not done_thinking:
            done_thinking = True
            print('\n')
          content += chunk.message.content
          print(chunk.message.content, end='', flush=True)
        if chunk.message.tool_calls:
          tool_calls.extend(chunk.message.tool_calls)
          print(chunk.message.tool_calls)

      # append accumulated fields to the messages
      if thinking or content or tool_calls:
        messages.append({'role': 'assistant', 'thinking': thinking, 'content': content, 'tool_calls': tool_calls})

      if not tool_calls:
        break

      for call in tool_calls:
        if call.function.name == 'get_temperature':
          result = get_temperature(**call.function.arguments)
        else:
          result = 'Unknown tool'
        messages.append({'role': 'tool', 'tool_name': call.function.name, 'content': result})
    ```
  </Tab>

  <Tab title="JavaScript">
    ```typescript  theme={"system"}
    import ollama from 'ollama'

    function getTemperature(city: string): string {
      const temperatures: Record<string, string> = {
        'New York': '22°C',
        'London': '15°C',
      }
      return temperatures[city] ?? 'Unknown'
    }

    const getTemperatureTool = {
      type: 'function',
      function: {
        name: 'get_temperature',
        description: 'Get the current temperature for a city',
        parameters: {
          type: 'object',
          required: ['city'],
          properties: {
            city: { type: 'string', description: 'The name of the city' },
          },
        },
      },
    }

    async function agentLoop() {
      const messages = [{ role: 'user', content: "What is the temperature in New York?" }]

      while (true) {
        const stream = await ollama.chat({
          model: 'qwen3',
          messages,
          tools: [getTemperatureTool],
          stream: true,
          think: true,
        })

        let thinking = ''
        let content = ''
        const toolCalls: any[] = []
        let doneThinking = false

        for await (const chunk of stream) {
          if (chunk.message.thinking) {
            thinking += chunk.message.thinking
            process.stdout.write(chunk.message.thinking)
          }
          if (chunk.message.content) {
            if (!doneThinking) {
              doneThinking = true
              process.stdout.write('\n')
            }
            content += chunk.message.content
            process.stdout.write(chunk.message.content)
          }
          if (chunk.message.tool_calls?.length) {
            toolCalls.push(...chunk.message.tool_calls)
            console.log(chunk.message.tool_calls)
          }
        }

        if (thinking || content || toolCalls.length) {
          messages.push({ role: 'assistant', thinking, content, tool_calls: toolCalls } as any)
        }

        if (!toolCalls.length) {
          break
        }

        for (const call of toolCalls) {
          if (call.function.name === 'get_temperature') {
            const args = call.function.arguments as { city: string }
            const result = getTemperature(args.city)
            messages.push({ role: 'tool', tool_name: call.function.name, content: result } )
          } else {
            messages.push({ role: 'tool', tool_name: call.function.name, content: 'Unknown tool' } )
          }
        }
      }
    }

    agentLoop().catch(console.error)
    ```
  </Tab>
</Tabs>

This loop streams the assistant response, accumulates partial fields, passes them back together, and appends the tool results so the model can complete its answer.

## Using functions as tools with Ollama Python SDK

The Python SDK automatically parses functions as a tool schema so we can pass them directly.
Schemas can still be passed if needed.

```python  theme={"system"}
from ollama import chat

def get_temperature(city: str) -> str:
  """Get the current temperature for a city

  Args:
    city: The name of the city

  Returns:
    The current temperature for the city
  """
  temperatures = {
    'New York': '22°C',
    'London': '15°C',
  }
  return temperatures.get(city, 'Unknown')

available_functions = {
  'get_temperature': get_temperature,
}
# directly pass the function as part of the tools list
response = chat(model='qwen3', messages=messages, tools=available_functions.values(), think=True)
```


> ## Documentation Index
> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
> Use this file to discover all available pages before exploring further.

# OllamaEmbeddings integration

> Integrate with the OllamaEmbeddings embedding model using LangChain Python.

This will help you get started with Ollama embedding models using LangChain. For detailed documentation on `OllamaEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/ollama/embeddings/langchain_ollama.embeddings.OllamaEmbeddings.html).

## Overview

### Integration details

<ItemTable category="text_embedding" item="Ollama" />

## Setup

First, follow [these instructions](https://github.com/ollama/ollama?tab=readme-ov-file#ollama) to set up and run a local Ollama instance:

* [Download](https://ollama.ai/download) and install Ollama onto the available supported platforms (including Windows Subsystem for Linux aka WSL, macOS, and Linux)
  * macOS users can install via Homebrew with `brew install ollama` and start with `brew services start ollama`
* Fetch available LLM model via `ollama pull <name-of-model>`
  * View a list of available models via the [model library](https://ollama.ai/library)
  * e.g., `ollama pull llama3`
* This will download the default tagged version of the model. Typically, the default points to the latest, smallest sized-parameter model.

> On Mac, the models will be download to `~/.ollama/models`
>
> On Linux (or WSL), the models will be stored at `/usr/share/ollama/.ollama/models`

* Specify the exact version of the model of interest as such `ollama pull vicuna:13b-v1.5-16k-q4_0` (View the [various tags for the `Vicuna`](https://ollama.ai/library/vicuna/tags) model in this instance)
* To view all pulled models, use `ollama list`
* To chat directly with a model from the command line, use `ollama run <name-of-model>`
* View the [Ollama documentation](https://github.com/ollama/ollama/tree/main/docs) for more commands. You can run `ollama help` in the terminal to see available commands.

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

```python  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
```

### Installation

The LangChain Ollama integration lives in the `langchain-ollama` package:

```python  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
pip install -qU langchain-ollama
```

## Instantiation

Now we can instantiate our model object and generate embeddings:

```python  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="llama3",
)
```

## Indexing and retrieval

Embedding models are often used in retrieval-augmented generation (RAG) flows, both as part of indexing data as well as later retrieving it. For more detailed instructions, please see our [RAG tutorials](/oss/python/langchain/rag/).

Below, see how to index and retrieve data using the `embeddings` object we initialized above. In this example, we will index and retrieve a sample document in the `InMemoryVectorStore`.

```python  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
# Create a vector store with a sample text
from langchain_core.vectorstores import InMemoryVectorStore

text = "LangChain is the framework for building context-aware reasoning applications"

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding=embeddings,
)

# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()

# Retrieve the most similar text
retrieved_documents = retriever.invoke("What is LangChain?")

# Show the retrieved document's content
print(retrieved_documents[0].page_content)
```

```text  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
LangChain is the framework for building context-aware reasoning applications
```

## Direct usage

Under the hood, the vectorstore and retriever implementations are calling `embeddings.embed_documents(...)` and `embeddings.embed_query(...)` to create embeddings for the text(s) used in `from_texts` and retrieval `invoke` operations, respectively.

You can directly call these methods to get embeddings for your own use cases.

### Embed single texts

You can embed single texts or documents with `embed_query`:

```python  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
single_vector = embeddings.embed_query(text)
print(str(single_vector)[:100])  # Show the first 100 characters of the vector
```

```text  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
[-0.0039849705, 0.023019705, -0.001768838, -0.0058736936, 0.00040999008, 0.017861595, -0.011274585,
```

### Embed multiple texts

You can embed multiple texts with `embed_documents`:

```python  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
text2 = (
    "LangGraph is a library for building stateful, multi-actor applications with LLMs"
)
two_vectors = embeddings.embed_documents([text, text2])
for vector in two_vectors:
    print(str(vector)[:100])  # Show the first 100 characters of the vector
```

```text  theme={"theme":{"light":"catppuccin-macchiato","dark":"catppuccin-mocha"}}
[-0.0039849705, 0.023019705, -0.001768838, -0.0058736936, 0.00040999008, 0.017861595, -0.011274585,
[-0.0066985516, 0.009878328, 0.008019467, -0.009384944, -0.029560851, 0.025744654, 0.004872892, -0.0
```

***

## API reference

For detailed documentation on `OllamaEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/ollama/embeddings/langchain_ollama.embeddings.OllamaEmbeddings.html).

***

<div className="source-links">
  <Callout icon="edit">
    [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/text_embedding/ollama.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
  </Callout>

  <Callout icon="terminal-2">
    [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
  </Callout>
</div>


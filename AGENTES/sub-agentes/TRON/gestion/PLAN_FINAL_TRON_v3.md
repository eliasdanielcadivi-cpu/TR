# Plan de Acción Final para TRON v3: Gestión de Costos y Modelos

**Fecha:** 2026-01-08
**Estado:** En espera de acción del usuario.

## Resumen

El objetivo es evolucionar el sistema TRON para integrar un control de costos y una gestión de modelos inteligente, utilizando PocketBase como base de datos central. Durante la implementación, se encontró un bloqueo crítico: la instancia de PocketBase requiere autenticación para todas las operaciones.

Este documento detalla los pasos pendientes y la justificación de cada uno para completar la remodelación.

---

## Tareas Pendientes y Justificación

### 1. **Integrar Autenticación de PocketBase (ACCIÓN CRÍTICA / BLOQUEANTE)**

*   **QUÉ:** Añadir una clave de API de PocketBase al fichero `tron_config.yaml` y modificar los scripts para que la usen al autenticarse.
*   **POR QUÉ:** Las pruebas de conexión fallan con un error `401 Unauthorized`. Esto demuestra que la instancia de PocketBase no permite ninguna operación (ni siquiera leer colecciones) sin un token de autorización válido. Sin esta autenticación, ningún script puede interactuar con la base de datos.

### 2. **Refactorizar Scripts a `async/await`**

*   **QUÉ:** Convertir todas las funciones que interactúan con la base de datos en `tron_lib.py` y los scripts de prueba a un modelo asíncrono, usando `async def` y `await`.
*   **POR QUÉ:** La librería `pocketbase-sdk` es asíncrona. No usar `await` para sus métodos provoca errores de tipo `RuntimeWarning: coroutine was never awaited` y `AttributeError`, impidiendo que el código funcione.

### 3. **Actualizar el Script Principal `tron`**

*   **QUÉ:** Modificar el script `tron` para que lea la nueva `pocketbase_api_key` desde `tron_config.yaml` y la pase a las funciones de `tron_lib.py` antes de realizar la sincronización o cualquier consulta.
*   **POR QUÉ:** Para que las verificaciones pre-vuelo de costo y estado del modelo funcionen, el script `tron` debe poder orquestar la autenticación de la librería que realiza dichas verificaciones.

### 4. **Implementar "Depuración Paranoica"**

*   **QUÉ:** Agregar un sistema de logging detallado a los ficheros `tron`, `tron_lib.py` y `notify_user.sh`. Los logs deben guardarse en ficheros físicos (`tron.log`, `tron_lib.log`, etc.) que se sobreescriban en cada ejecución.
*   **POR QUÉ:** Es una solicitud explícita del usuario para facilitar la depuración y tener un rastro claro de las operaciones que realizan los scripts, especialmente las interacciones con la base de datos y las APIs externas.

### 5. **Crear Documentación Exhaustiva**

*   **QUÉ:**
    1.  Crear un fichero `README.md` en el directorio `TRON/bin/`.
    2.  Añadir docstrings y comentarios detallados a todos los scripts modificados.
*   **POR QUÉ:** Es una solicitud explícita del usuario para explicar la nueva arquitectura, el propósito de cada componente (`tron`, `tron_lib.py`), los comandos de uso con ejemplos prácticos, y el funcionamiento del nuevo sistema de gestión de costos. Esto hace que el sistema sea mantenible y comprensible a futuro.

---

## URLs Clave del Proyecto

1.  **Panel de Administración de PocketBase:**
    *   **URL:** `http://localhost:8090/_/`
    *   **Propósito:** Es el lugar donde se debe iniciar sesión para **generar la API Key necesaria** que desbloqueará todo el proceso.

2.  **API de Modelos de OpenRouter:**
    *   **URL:** `https://openrouter.ai/api/v1/models`
    *   **Propósito:** Es la fuente de datos oficial para los precios, nombres y capacidades de todos los modelos, con la que se alimenta la base de datos en PocketBase.

3.  **Documentación de OpenRouter:**
    *   **Autenticación:** `https://openrouter.ai/docs#authentication`
    *   **Control de Costos:** `https://openrouter.ai/docs/guides/guides/usage-accounting`
    *   **Requests y Respuestas:** `https://openrouter.ai/docs#requests`

---
**Conclusión:** La ejecución está pausada. Una vez que la **Tarea 1** sea completada por el usuario, se podrán reanudar las demás tareas para finalizar la implementación.

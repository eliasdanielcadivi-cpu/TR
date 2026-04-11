# 🛰️ Manual 05: El Maestro de Orquesta (Flujos de Trabajo Productivos)

Este manual te enseña a trabajar **con** Ares, no solo para Ares. Aprende a integrar la IA en tu ciclo de desarrollo.

## ⚙️ Flujo 01: Creación de un Nuevo Módulo
Cuando creas código nuevo, Ares no lo conoce. No preguntes, **Ingesta**.

1. **Escribe el código:** (ej: `src/models/user.py`).
2. **Ingesta inmediata:** `ares ingest --path src/models/ --dataset codigo`.
3. **Valida la ingesta:** `ares p "clase User" --rag codigo -v`. 
   - *¿Aparece en la tabla SQL?* ✅ Sigue.
   - *¿El score semántico es > 0.6?* ✅ Sigue.
4. **Pide Auditoría:** `ares i --rag codigo` y pregunta "¿Ves algún bug en mi nueva clase User?".

## ⚙️ Flujo 02: Análisis de Documentación Compleja
Si tienes 50 archivos de texto y quieres un resumen coherente.

1. **Indexa por separado:** `ares ingest --path docs/investigacion/ --dataset lab`.
2. **Consulta con Fusión RRF:** `ares p "¿Cuál es el hilo conductor de estos documentos?" --rag lab -v`.
3. **Observa la tabla RRF:** Los chunks con mayor score son los más citados en las 3 capas. Esos son los más importantes de tu investigación.

## ⚙️ Flujo 03: Depuración de Razonamiento (Think)
Si estás resolviendo un problema lógico difícil.

1. **Usa el modelo pensante:** `ares p "¿Por qué falla esta conexión?" --think`.
2. **Lee las etiquetas `<think>`:** Ahí verás si Ares está asumiendo cosas erróneas.
3. **Corrige el rumbo:** Si Ares asume algo mal, dile: "No es X, es Y. Revisa de nuevo". El filtrado automático en el modo interactivo mantendrá la pantalla limpia pero Ares seguirá pensando.

---
*💡 Flujo Táctico: Ingesta → Valida (-v) → Orquesta (Chat).*

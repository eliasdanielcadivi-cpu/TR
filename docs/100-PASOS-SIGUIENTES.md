# 📋 100 PASOS SIGUIENTES — ARES (FASE 3-6)

**Fecha:** 2026-03-10
**Basado en:** Agenda MAESTRA + Conversación 2026-03-09/10 + TODO-RAG.md
**Estado:** FASE 3 (Cognición - Apollo) implementada, pendiente pruebas y expansión

---

## 🎯 CONTEXTO ESTRATÉGICO

### Fases del Proyecto

| Fase | Nombre | Estado | Descripción |
|------|--------|--------|-------------|
| 1 | Entorno | ✅ COMPLETADA | Oh My Zsh, aliases, dotfiles |
| 2 | Percepción | ✅ COMPLETADA | Indexador universal |
| 3 | Cognición | 🟡 EN PROGRESO | Apollo RAG + CRM + Emojis |
| 4 | Ejecución | ⏳ PENDIENTE | Ares Puppet, agentes autónomos |
| 5 | Conectividad | ⏳ PENDIENTE | News Engine, WhatsApp bridge |
| 6 | Producción | ⏳ PENDIENTE | Comercialización, CRM avanzado |

### Prioridad Inmediata

1. **Pruebas Apollo** (pasos 1-19)
2. **Model Creator** (pasos 20-30)
3. **CRM Básico** (pasos 31-45)
4. **Optimización** (pasos 46-60)
5. **FASE 4: Ejecución** (pasos 61-80)
6. **FASE 5-6: Conectividad y Producción** (pasos 81-100)

---

## 📝 100 PASOS DETALLADOS

### 🔴 PRIORIDAD 1: Pruebas Apollo (Pasos 1-19)

#### Emojis y Chat (Pasos 1-6)

1. **Redimensionar emojis PNG** - Usar ImageMagick para reducir `ares-emoji.png` y `user-emoji.png` a 32x8 y 16x8 píxeles respectivamente
2. **Probar `ares i` con emojis redimensionados** - Verificar que se muestran correctamente en encabezado y prompt
3. **Ajustar `emoji_manager.py`** - Si redimensionamiento no funciona, modificar parámetros de `image.draw()`
4. **Documentar tamaño óptimo** - Registrar en `EMOJIS-PNG-INVENTARIO.md` el tamaño que mejor se ve
5. **Probar en diferentes tamaños de terminal** - Verificar que emojis escalan correctamente
6. **Añadir fallback robusto** - Si term-image falla, mostrar emoji Unicode + texto descriptivo

#### Modo Pensante (Pasos 7-10)

7. **Probar `ares i --think`** - Verificar que inicia con `ares-think:latest` y muestra "Think Mode: ON"
8. **Probar comando `/think on`** - Dentro de `ares i`, activar modo pensante y verificar cambio de modelo
9. **Probar comando `/think off`** - Desactivar modo pensante y verificar retorno a `ares:latest`
10. **Verificar post-procesamiento** - Confirmar que `ares` elimina <think></think> pero `ares-think` los mantiene

#### RAG (Pasos 11-16)

11. **Probar `ares i --rag docs`** - Iniciar interactivo con RAG en dataset docs
12. **Hacer pregunta sobre Apollo** - Verificar recuperación de chunks relevantes y respuesta con fuentes
13. **Probar `ares p "¿Qué es Apollo?" --rag docs`** - Consulta directa con RAG
14. **Probar `ares p "¿Qué es Apollo?" --rag docs --think`** - Consulta con RAG y modo pensante
15. **Probar todos los datasets** - `--rag skills`, `--rag codigo`, `--rag config`
16. **Medir tiempo de respuesta** - TTF (Time to First reply) debe ser < 3s

#### Post-procesamiento (Pasos 17-19)

17. **Probar `apply_post_process()` con modelo `ares`** - Verificar que elimina <think></think>
18. **Probar `apply_post_process()` con modelo `ares-think`** - Verificar que MANTIENE <think></think>
19. **Añadir tests unitarios** - `tests/test_apollo_postprocess.py` con casos de prueba

---

### 🟡 PRIORIDAD 2: Model Creator (Pasos 20-30)

#### Integración con Sherlok (Pasos 20-22)

20. **Verificar estado de sherlok** - Ejecutar `sherlok --help` para confirmar que funciona
21. **Revisar `prioritarios.txt`** - Verificar lista de programas prioritarios en `TR/AGENTES/sub-agentes/sherlok/prioritarios.txt`
22. **Ejecutar `sherlok --lista`** - Analizar programas prioritarios y verificar output en `AYUDA/docs/PROGRAMAS-PROPIOS/`

#### Implementación Model Creator (Pasos 23-30)

23. **Crear `model_creator.py`** - Módulo atómico con funciones: `list_models()`, `create_model()`, `update_model()`, `delete_model()`
24. **Implementar `list_models()`** - Ejecutar `ollama list` y mostrar tabla formateada
25. **Implementar `create_model()`** - Crear Modelfile temporal y ejecutar `ollama create`
26. **Implementar `update_model()`** - Modificar parámetros y recrear modelo
27. **Implementar `delete_model()`** - Ejecutar `ollama rm <nombre>`
28. **Implementar `show_model()`** - Mostrar Modelfile asociado y metadatos
29. **Registrar comando en `main.py`** - `@cli.command(name="model-creator")` con subcomandos
30. **Añadir ayuda en `ares_help.yaml`** - Documentar opciones y ejemplos de uso
31. **Probar todos los subcomandos** - `ares model-creator list/create/update/delete/show`
32. **Vincular con sherlok** - Al indexar nuevo programa, registrar en model-creator si es LLM
33. **Actualizar `bd/apollo/modelfiles.yaml`** - Guardar configuración de modelos creados (parent, system, parameters)
34. **Implementar backup automático** - Copia de seguridad antes de cada modificación

---

### 🟡 PRIORIDAD 3: Modelfile Creator (Pasos 35-44)

#### Implementación (Pasos 35-39)

35. **Crear `modelfile_creator.py`** - Módulo atómico con funciones: `create_modelfile()`, `update_modelfile()`, `delete_modelfile()`, `list_modelfiles()`, `show_modelfile()`
36. **Implementar `create_modelfile()`** - Crear entrada en `modelfiles.yaml` con parent, system, parameters
37. **Implementar `update_modelfile()`** - Modificar entrada existente en YAML
38. **Implementar `delete_modelfile()`** - Eliminar entrada de YAML (con confirmación)
39. **Implementar `list_modelfiles()` y `show_modelfile()`** - Mostrar contenido de YAML formateado

#### CLI (Pasos 40-42)

40. **Registrar comando en `main.py`** - `@cli.command(name="modelfile-creator")` con subcomandos
41. **Añadir ayuda en `ares_help.yaml`** - Documentar opciones y ejemplos
42. **Probar todos los subcomandos** - `ares modelfile-creator create/update/delete/list/show`

#### Integración (Pasos 43-44)

43. **Vincular con `model-creator`** - Al crear modelo, preguntar si guardar Modelfile
44. **Documentar en `MODELOS-ARES.md`** - Añadir sección de creación y gestión de Modelfiles

---

### 🟢 PRIORIDAD 4: CRM Básico (Pasos 45-59)

#### Implementación crm.py (Pasos 45-49)

45. **Crear `crm.py`** - Módulo atómico con funciones: `create_client()`, `update_client()`, `search_clients()`
46. **Implementar `create_client()`** - Insertar en `clients` table con name, type, source, status, metadata
47. **Implementar `update_client()`** - Actualizar campos y `updated_at` timestamp
48. **Implementar `search_clients()`** - Búsqueda por nombre, tipo, status con filtros opcionales
49. **Añadir tests unitarios** - `tests/test_crm.py` con casos de prueba

#### Implementación interactions.py (Pasos 50-54)

50. **Crear `interactions.py`** - Módulo atómico con funciones: `log_interaction()`, `get_client_history()`, `get_follow_ups()`
51. **Implementar `log_interaction()`** - Insertar en `interactions` table con client_id, type, channel, summary, sentiment, action_items
52. **Implementar `get_client_history()`** - Obtener todas las interacciones de un cliente ordenadas por fecha
53. **Implementar `get_follow_ups()`** - Extraer action_items pendientes de todas las interacciones
54. **Añadir tests unitarios** - `tests/test_interactions.py`

#### WhatsApp Integration (Pasos 55-59)

55. **Crear `whatsapp_integration.py`** - Módulo atómico con funciones: `import_whatsapp_chat()`, `link_client_to_documents()`, `generate_client_summary()`
56. **Implementar `import_whatsapp_chat()`** - Parsear exportación TXT de WhatsApp, identificar mensajes por número, crear/actualizar cliente
57. **Implementar `link_client_to_documents()`** - Asociar documentos específicos a cliente en tabla `client_documents`
58. **Implementar `generate_client_summary()`** - Usar LLM para generar resumen ejecutivo del cliente (historial, preferencias, action_items)
59. **Documentar formato de exportación WhatsApp** - `docs/WHATSAPP_EXPORT_FORMAT.md`

---

### 🔵 PRIORIDAD 5: Optimización (Pasos 60-74)

#### Estrés RAG (Pasos 60-64)

60. **Ingerir 50+ documentos** - Usar `ares apollo ingest docs/` con múltiples archivos
61. **Medir tiempo de ingesta** - Registrar segundos por documento y total
62. **Medir tamaño de database** - `du -sh bd/apollo/knowledge.db` antes y después
63. **Probar queries complejas** - Preguntas que requieren múltiples chunks y fuentes
64. **Identificar cuellos de botella** - Profile con `cProfile` para identificar funciones lentas

#### Cuantización INT8 (Pasos 65-69)

65. **Implementar `quantize_embeddings()` en `embeddings.py`** - Cuantización simétrica por canal (channel-wise)
66. **Probar cuantización INT8** - Reducir memoria 50-75% con mínima pérdida de precisión
67. **Probar cuantización INT4** - Reducir memoria 75-87% con pérdida aceptable
68. **Medir impacto en precisión** - Comparar similitud coseno antes/después de cuantizar
69. **Documentar trade-offs** - `docs/EMBEDDING_QUANTIZATION.md` con métricas de precisión vs memoria

#### Dashboard Apollo (Pasos 70-74)

70. **Crear `dashboard.py`** - Módulo atómico con funciones: `generate_knowledge_stats()`, `generate_client_activity_report()`, `visualize_knowledge_graph()`
71. **Implementar `generate_knowledge_stats()`** - Contar documentos, chunks, entidades, relaciones, clientes
72. **Implementar `generate_client_activity_report()`** - Últimas interacciones por cliente, follow-ups completados vs pendientes
73. **Implementar `visualize_knowledge_graph()`** - Extraer top N entidades y relaciones, generar grafo ASCII
74. **Registrar comando `ares apollo dashboard`** - Subcomandos: `stats`, `activity`, `graph`

---

### 🟣 PRIORIDAD 6: Documentación y Tests (Pasos 75-84)

#### API RAG (Pasos 75-77)

75. **Crear `docs/APOLLO_API.md`** - Documentación completa de funciones públicas: `retrieve()`, `compress_context()`, `generate_answer()`
76. **Documentar parámetros y retornos** - Para cada función: descripción, parámetros, valor de retorno, ejemplos de uso
77. **Añadir diagramas de flujo** - Flujo completo: ingest → embed → retrieve → compress → generate

#### Tests Automatizados (Pasos 78-81)

78. **Crear `tests/test_apollo.py`** - Tests unitarios para todos los módulos Apollo
79. **Tests para `embeddings.py`** - Verificar que `embed_text()` retorna array 1024-dim, `quantize_embeddings()` reduce tamaño
80. **Tests para `retrieval.py`** - Verificar que `retrieve()` retorna chunks relevantes, RRF fusiona correctamente
81. **Tests para `generation.py`** - Verificar que `generate_answer()` genera respuesta coherente, `apply_post_process()` elimina/mantiene tags

#### Backup Automático (Pasos 82-84)

82. **Crear `scripts/backup_apollo.sh`** - Script bash que copia `bd/apollo/` a backup con timestamp
83. **Añadir a cron** - Ejecutar diariamente a las 3 AM: `0 3 * * * /home/daniel/tron/programas/TR/scripts/backup_apollo.sh`
84. **Implementar rotación de backups** - Mantener últimos 7 backups, eliminar anteriores

---

### 🟤 PRIORIDAD 7: FASE 4 - Ejecución (Pasos 85-94)

#### Ares Puppet (Pasos 85-89)

85. **Crear `modules/ia/puppet/`** - Directorio para módulo de control de terminal
86. **Crear `puppet_controller.py`** - Funciones: `launch_session()`, `run_command()`, `capture_output()`, `close_session()`
87. **Implementar `launch_session()`** - Lanzar sesión Kitty en socket específico con layout definido
88. **Implementar `run_command()`** - Enviar comando a sesión específica y esperar output
89. **Implementar sandbox de seguridad** - Lista blanca de comandos permitidos, bloqueo de comandos peligrosos (rm -rf, etc.)

#### Extractor Cognitivo (Pasos 90-94)

90. **Crear `cognitive_extractor.py`** - Funciones: `extract_entities()`, `extract_relations()`, `structure_document()`
91. **Implementar `extract_entities()`** - Usar LLM para extraer entidades de texto no estructurado (scripts, docs, emails)
92. **Implementar `extract_relations()`** - Extraer relaciones entre entidades (depende_de, usa, importa, etc.)
93. **Implementar `structure_document()`** - Convertir documento no estructurado a JSON con entidades, relaciones, metadata
94. **Integrar con Apollo RAG** - Al ingerir documento, pasar por extractor cognitivo antes de guardar

---

### ⚫ PRIORIDAD 8: FASE 5-6 - Conectividad y Producción (Pasos 95-100)

#### News Engine (Pasos 95-97)

95. **Crear `news_engine.py`** - Funciones: `scrape_feeds()`, `filter_by_preference()`, `generate_summary()`
96. **Implementar `scrape_feeds()`** - Leer RSS/Atom feeds de fuentes configuradas (tech, IA, negocios)
97. **Implementar `filter_by_preference()`** - Filtrar noticias por preferencias del usuario (palabras clave, temas, fuentes)
98. **Implementar `generate_summary()`** - Usar LLM para generar resumen ejecutivo de noticias filtradas
99. **Integrar con Apollo** - Guardar noticias en `documents` table para retrieval futuro

#### Bridge de Comunicaciones (Pasos 100)

100. **Crear `communication_bridge.py`** - Funciones: `send_whatsapp()`, `send_telegram()`, `receive_message()`

---

## 📊 CRONOGRAMA ESTIMADO

| Bloque | Pasos | Duración Estimada | Fecha Tentativa |
|--------|-------|-------------------|-----------------|
| Pruebas Apollo | 1-19 | 1-2 días | 10-11 Mar 2026 |
| Model Creator | 20-40 | 2-3 días | 12-14 Mar 2026 |
| CRM Básico | 41-55 | 2-3 días | 15-17 Mar 2026 |
| Optimización | 56-70 | 3-4 días | 18-21 Mar 2026 |
| Documentación y Tests | 71-80 | 2 días | 22-23 Mar 2026 |
| FASE 4: Ejecución | 81-90 | 4-5 días | 24-28 Mar 2026 |
| FASE 5-6: Producción | 91-100 | 3-4 días | 29 Mar - 1 Abr 2026 |

**Total estimado:** 17-23 días hábiles

---

## ✅ CRITERIOS DE ÉXITO POR FASE

### FASE 3 (Cognición) - Pasos 1-70

- [ ] `ares i` muestra emojis PNG correctamente
- [ ] `ares i --think` activa modo pensante
- [ ] `ares p --rag` recupera contexto relevante
- [ ] Post-procesamiento funciona (strip_think_tags)
- [ ] Model Creator crea/actualiza/elimina modelos
- [ ] CRM crea/actualiza/busca clientes
- [ ] Dashboard muestra estadísticas

### FASE 4 (Ejecución) - Pasos 81-90

- [ ] Ares Puppet lanza sesiones Kitty
- [ ] Ares Puppet ejecuta comandos seguros
- [ ] Extractor Cognitivo estructura documentos

### FASE 5-6 (Conectividad y Producción) - Pasos 91-100

- [ ] News Engine filtra y resume noticias
- [ ] Bridge envía mensajes WhatsApp/Telegram
- [ ] Pack PYME instalable en < 2 horas

---

## 🔗 DEPENDENCIAS CRÍTICAS

| Paso | Depende de | Riesgo si falla |
|------|------------|-----------------|
| 1-6 (Emojis) | term-image, Kitty protocolo gráfico | Bajo (fallback a Unicode) |
| 7-10 (Think) | ares-think:latest en Ollama | Medio (usar ares sin think) |
| 11-16 (RAG) | mxbai-embed-large:335m | Alto (sin RAG semántico) |
| 20-30 (Model Creator) | Ollama API | Medio (crear Modelfiles manualmente) |
| 41-55 (CRM) | SQLite schema | Bajo (usar JSON en vez de SQLite) |
| 81-90 (Puppet) | Kitty remote control | Alto (sin automatización de terminal) |

---

*Documento vivo. Actualizar después de cada paso completado.*

**Próximo paso inmediato:** Paso 1 - Redimensionar emojis PNG con ImageMagick.

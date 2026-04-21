# INFORME 06: GUÍA DE OPERACIÓN INDUSTRIAL
**Sistema:** RAG Mengraph V1.0
**Misión:** Soberanía Cognitiva y Zero-Hallucination

## 🚀 CÓMO OPERAR EL SISTEMA
El sistema ya está integrado en el núcleo de ARES. Aquí tienes los comandos tácticos:

### 1. Gestión de Infraestructura
-   `ares mem start`: Siempre ejecuta esto antes de usar el RAG.
-   `ares mem status`: Verifica que el puerto 7687 esté listo.

### 2. Ingesta Masiva (Manuales/CRM)
Usa el script de orquestación para alimentar el cerebro:
`PYTHONPATH=. uv run python3 modules/rag_mengraph/core/orchestrator.py`
*(Nota: Pronto se integrará como subcomando `ares rag ingest-mengraph`)*

### 3. Consultas Deterministas
-   `ares p "Cómo calificar leads" --mengraph`: Respuesta basada en el grafo.
-   `ares i --mengraph`: Modo interactivo de alta fidelidad.

## 📚 FUENTES CONSULTADAS PARA LA CREACIÓN
Para construir este código, me sumergí en la documentación local que proporcionaste:
1.  **Arquitectura de Datos:** `docs/MEMGRAPH/ARQUITECTURA.md` (Entendimiento de Bolt y MAGE).
2.  **Lógica Maestra:** `/home/daniel/Escritorio/BORRAR/NUCLEO DE CREACION DE SOFTWARE KNOW-HOW ARES-TRON.md` (Regla de oro: Máximo 3 funciones).
3.  **Flujo de Datos:** `/home/daniel/Escritorio/BORRAR/DIAGRAMA DE FLUJO RAG NUEVO MENGRAPH.md` (Fases F1-F5).
4.  **Referencia de Código:** `DOCUMENTACION-REPO/Proyecto-Mengraph/memgraph/agentic-graph-rag/agentic/agenticGraphRAG.py`.
5.  **Motor Lingüístico:** Documentación de `spacy-layout` y `EntityRuler`.

## 🔍 BÚSQUEDAS Y AUDITORÍAS REALIZADAS
Durante la sesión, ejecuté las siguientes acciones críticas:
-   **Handshake de RAM:** Auditoría de `free -h` para dimensionar el impacto de Ollama + Memgraph.
-   **Sincronización de Puertos:** Verificación de colisiones en 7687 y 11434.
-   **Forense de spaCy:** Validación empírica de la persistencia del atributo `ent_id_` en el pipeline Blank.
-   **Debugging Cypher:** Refinamiento de las cláusulas `WITH` y `WHERE` para el motor de búsqueda híbrida.

## 💡 CONSEJO FINAL: "SACANDO EL JUGO"
Usa Memgraph Lab (`http://localhost:3000`). No solo es una base de datos; es tu **Centro de Comando Visual**. Cuando inyectes un manual de gurú, entra al Lab y verás cómo las bolitas se conectan físicamente. Si ves una conexión débil, bórrala manualmente; el sistema se adaptará en la próxima consulta. 

**Has construido un cerebro que puedes tocar.**

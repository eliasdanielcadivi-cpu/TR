# 📝 TODO - Desarrollo RAG V3

## 🚀 Funcionalidades Críticas (Indispensables)
- [X] Conectividad: Funciones de conexión con re-intento y manejo de bloqueos.
- [X] **T1 SQL:** Implementar búsqueda FTS5 aislada y probar con acentos.
- [X] **T3 Grafo:** Implementar verificación de nodos y saltos simples en Kùzu.
- [ ] **Fallback Vectorial:** Asegurar que si Ollama falla, el sistema no muera.

## 📈 Funcionalidades Comerciales (Rápido Valor)
- [ ] **Consulta Mixta (Hybrid):** Unir SQL + Vector en un solo resultado ordenado.
- [ ] **Ingesta Automatizada:** Script de un solo paso para nuevos documentos.
- [ ] **CLI Robustecido:** Corregir argumentos de `ares p --rag`.

## 🎨 Funcionalidades Superficiales (Opcionales)
- [ ] **Visualizador de Grafo:** Exportar a formato JSON para UI.
- [ ] **Métricas de Latencia:** Logs detallados por micro-módulo.

---

## 📓 Bitácora de Progreso
### 2026-04-01
- [X] Creación de documentos de gobernanza (`LEEME`, `MODULOS`, `TODO`).
- [X] Backup inicial Git.
- [X] Implementación de primitiva `storage/` (SQLite y Kuzu).
- [X] Implementación de primitiva `engines/sql/` (FTS5 funcional).
- [X] Implementación de primitiva `engines/graph/` (Kuzu funcional).
- [ ] Próximo paso: Implementar `ingestion/` atómica.

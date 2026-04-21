# INFORME 03: SEGURIDAD RELATIONGUARD Y CUARENTENA
**Sistema:** RAG Mengraph V1.0
**Módulo:** `modules/rag_mengraph/validators/`

## 🛡️ EL CONCEPTO: EL ÁRBITRO DETERMINISTA
Inyectar datos automáticamente en un grafo es peligroso si la IA alucina. **RelationGuard** es el enclave de seguridad que filtra cada relación antes de que toque la base de datos de producción.

### Niveles de Criticidad (C1-C4):
-   **C1 (Informativo):** Inyección directa (ej: `EXTRAIDO_DE`).
-   **C2 (Operacional):** Inyección directa con log (ej: `CUALIFICA_A`).
-   **C3 (Estratégico):** Requiere aprobación humana (HITL).
-   **C4 (Seguridad):** Bloqueo y Cuarentena obligatoria (ej: `PUBLICA_EN_REDES`).

## ⚙️ FUNCIONAMIENTO TÉCNICO
El `RelationGuard` consulta la criticidad en la ontología para cada Verbo propuesto.
1.  Si el Verbo es nuevo (**Serendipia**), se clasifica como `NEW_VERB` y se envía a Cuarentena.
2.  Si es C3 o C4, se desvía.

### Zona de Cuarentena (`quarantine.hjson`):
Utilizamos el formato **HJSON** por su legibilidad superior para humanos. El archivo se encuentra en `db/rag_mengraph/quarantine.hjson`.
Contiene:
-   Relación propuesta.
-   Razón del desvío.
-   Texto original (evidencia) para tu revisión.

## 🥤 SACANDO EL JUGO
Este sistema garantiza que **tú tienes la última palabra**. Puedes revisar la Cuarentena semanalmente y, si apruebas un nuevo Verbo, simplemente lo añades a la Ontología Maestra. El sistema es auto-correctivo bajo soberanía humana.

# INFORME 03: THE ENCLAVE - SEGURIDAD RELATIONGUARD
**Sistema:** RAG Mengraph V1.0 - Nucleo Cognitivo

## 🛡️ CRITICIDAD DETERMINISTA (C1-C4)
El sistema no es un "chatbot" suelto; es un orquestador industrial. Por ello, cada acción se clasifica:

- **C1/C2 (Rutinario):** Información pública, manuales, CRM. Inyecta directo.
- **C3/C4 (Crítico):** Publicación en redes, acceso a APIs de pago, datos sensibles. **Bloqueo y Desvío.**

## 🧪 ZONA DE CUARENTENA (HJSON)
He implementado un almacén de seguridad en `db/rag_mengraph/quarantine.hjson`. 

### Beneficios del Formato HJSON:
1. **Legibilidad:** Puedes leerlo como un manual humano.
2. **Edición:** Puedes aprobar una relación simplemente moviéndola del archivo.

## 🚀 JUGO TÁCTICO
Durante el STORM TEST, inyectamos un Verbo prohibido `PUBLICA_EN_REDES`. El `RelationGuard` lo detectó instantáneamente y, en lugar de arruinar el grafo, lo envió a tu revisión con el mensaje: *"Nivel de criticidad elevado: C4"*. 

**Tú tienes el botón rojo.**

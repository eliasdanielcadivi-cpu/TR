# 🌌 LA SABIDURÍA DEL TORRENT (ARES-TRON V1.0)

Este documento contiene la lógica ontológica para la descarga de contenido multimedia. Cualquier IA operando en este sistema debe seguir estas leyes de la física del tracker.

## 🧠 1. LÓGICA DE BÚSQUEDA (JACKETT)
- **Formato Estricto:** `Nombre de la Serie` + `Espacio` + `Capítulo/Temporada` (Ej: `Gen V S01E01` o `Gen V S01`).
- **Paciencia Determinista:** Jackett es lento. Usa un timeout de al menos **180 segundos**.
- **Lógica de Ráfagas (OR):** Si buscas una temporada completa y los capítulos están dispersos, anexa la palabra `COMPLETE`.
- **Pruebas Escalares:** Empieza con una búsqueda simple para recuperar evidencia y escala la complejidad de los filtros.

## 💎 2. EL FILTRO DE CALIDAD (LA LEY DEL 1080)
- **Prohibición:** La resolución `720p` es inaceptable.
- **Preferencia:** Siempre `1080p` para arriba. 
- **Orden:** Ordenar por **Seeders**. Los torrents con más salud suelen ser los de mayor calidad.

## 👤 3. EL PANTEÓN DE UPLOADERS (LOS ELEGIDOS)
Prioridad absoluta en el scoring a:
- **ETHEL:** Calidad WEB-DL impecable.
- **MEGUSTA:** Versiones HEVC/x265 eficientes.
- **MULTISUB:** Para contenido internacional.

## 🛠️ 4. INGENIERÍA DE SISTEMA
- **Instalación:** Usa `echo "password" | sudo -S apt install` para evitar bloqueos interactivos.
- **Conectividad:** No uses `&&` si temes al fallo; usa `;` o `||` para mantener la soberanía del flujo.
- **Distribución:** Crea siempre un portal web (Flask/Bootstrap) en la carpeta de descarga para compartir en red local.

---
*"Boba nunca. El cerebro manda, la terminal obedece."*

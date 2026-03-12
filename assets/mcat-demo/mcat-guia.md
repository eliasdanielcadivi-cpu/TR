# 🛰️ GUÍA DE OPERACIONES: MCAT (ARES EDITION)

`mcat` es un potente visualizador y convertidor de archivos diseñado para la terminal moderna. Esta guía te ayudará a dominar sus capacidades tácticas.

---

## 🛠️ CAPACIDADES PRINCIPALES

### 📄 DOCUMENTOS Y TEXTO
`mcat` renderiza documentos complejos directamente en tu terminal Kitty:
- **PDF:** Renderizado ANSI de alta fidelidad o interactivo.
- **Office:** Soporta `.docx` y `.pptx` (conversión a Markdown).
- **Código:** Resaltado de sintaxis para 100+ lenguajes (Rust, Python, Java, Bash, etc.).
- **Markdown:** Soporte completo para estilos, tablas e imágenes incrustadas.

### 🖼️ MULTIMEDIA (Kitty Graphics Protocol)
- **Imágenes:** Renderizado de alta resolución (`png`, `jpg`, `webp`).
- **Videos:** Reproducción fluida de `mp4` (requiere FFmpeg).
- **Miniaturas:** El comando `mcat ls` genera un listado con thumbnails visuales.

### 🔄 MOTOR DE CONVERSIÓN
Puedes transformar archivos entre formatos usando el flag `-o`:
- `mcat archivo.pdf -o md > README.md` (PDF a Markdown).
- `mcat sitio.html -o image > captura.png` (HTML a Imagen).
- `mcat codigo.rs -o html > fuente.html` (Código a HTML).

---

## 🎮 MODO INTERACTIVO (`-o interactive` / `-I`)

Ideal para inspeccionar mapas, diagramas o documentos PDF de varias páginas.

### Atajos de Teclado (Visor de Imágenes/PDF)
| Tecla | Acción |
| :--- | :--- |
| `WASD` / `Flechas` | Pan (Desplazamiento) por la imagen. |
| `+` / `-` | Zoom In / Zoom Out. |
| `0` | Resetear Zoom. |
| `PgUp` / `PgDn` | Cambiar página (en archivos PDF). |
| `q` / `Esc` | Salir del modo interactivo. |

---

## 🥋 COMANDOS TÁCTICOS RÁPIDOS

- **Vista Rápida:** `mcat archivo.pdf`
- **Tema de Código:** `mcat script.py -t monokai`
- **Inspección de ZIP:** `mcat archivo.zip`
- **Listado Visual:** `mcat ls .`
- **Desde Tubería:** `cat datos.json | mcat`

---
*Filosofía ARES: Información Instantánea. Soberanía Visual.*

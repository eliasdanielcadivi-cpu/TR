Aquí tienes una **Guía Maestra de Uso** para tu nueva configuración de **Broot**. Está diseñada para que la tengas a mano (puedes guardarla como `HELP_BROOT.md`) y domines la herramienta en minutos.

---

# 🌳 Guía Maestra: Broot (Power User Edition)

Esta guía explica cómo sacarle el jugo a tu archivo `conf.toml` personalizado. Broot no es solo un visualizador de archivos, es tu centro de mando desde la terminal.

---

## 🖱️ 1. Interacción con el Ratón

Tu configuración tiene el **soporte de ratón activado**.

* **Un solo clic:** Selecciona un archivo o carpeta.
* **Doble clic:** Abre una carpeta (hace *focus*) o abre un archivo en tu editor.
* **Rueda del ratón (Scroll):** Desplázate hacia arriba o hacia abajo por el árbol de directorios de forma fluida.

---

## ⌨️ 2. Atajos de Navegación Críticos

Olvida las flechas del teclado; usa estos atajos rápidos para moverte como un rayo:

| Tecla | Acción | Descripción |
| --- | --- | --- |
| `alt` + `j` | **Bajar** | Mueve la selección una línea hacia abajo. |
| `alt` + `k` | **Subir** | Mueve la selección una línea hacia arriba. |
| `ctrl` + `h` | **Home** | Te lleva instantáneamente a tu carpeta personal (`~`). |
| `F9` | **Raíz** | Te lleva a la raíz del sistema (`/`). |
| `p` (o `:p`) | **Padre** | Sube un nivel en la jerarquía de carpetas. |
| `Esc` | **Atrás** | Cancela la búsqueda actual o vuelve al estado anterior. |

---

## 🛠️ 3. Verbos de Acción (Crear, Editar y Borrar)

Estos comandos se activan escribiendo `:` seguido del atajo o el nombre.

### 📝 Edición y Creación

* **`F2` o `e`:** Abre el archivo seleccionado en tu editor (definido en `$EDITOR`). **No cierra Broot**, al salir del editor vuelves al árbol.
* **`n` (New):** Invocación `:new nombre_archivo.txt`. Crea el archivo, crea las carpetas necesarias si no existen y lo abre para editarlo.

### 🗑️ Gestión de Archivos

* **`Supr` (Delete):** Mueve el archivo a la **Papelera** (usa `trash-put`). Es mucho más seguro que un `rm` permanente.
* **`cp` (Copy Path):** Copia la **ruta completa** del archivo seleccionado al portapapeles. Ideal para pegar la ubicación en un correo de Gmail o en otra terminal.

---

## 📑 4. Paneles y Multitarea (Staging)

¿Necesitas trabajar con 5 archivos de carpetas distintas? Usa el **Panel de Staging**.

1. Busca un archivo y presiona `ctrl` + `s` para "estacionarlo".
2. Busca otro y vuelve a presionar `ctrl` + `s`.
3. Presiona `ctrl` + `o` para filtrar y ver solo esos archivos que seleccionaste.
4. Esto te permite tener una lista de trabajo temporal sin perderte en el árbol.

---

## 🌿 5. Visualización e Indicadores

Gracias a las banderas `default_flags = "gh"`, verás lo siguiente por defecto:

* **Archivos Ocultos:** Se muestran automáticamente (los que empiezan con `.`).
* **Estado de Git:** * Archivos en **verde**: Son archivos nuevos (untracked).
* Archivos en **amarillo/naranja**: Son archivos modificados.


* **`gd` (Git Diff):** Si escribes `:gd` sobre un archivo modificado, verás qué cambios le has hecho sin salir de la terminal.

---

## 🎨 6. Código de Colores (Skin)

Para que identifiques todo de un vistazo:

* **Naranja Negrita:** Directorios (carpetas).
* **Cian/Celeste:** Archivos ejecutables.
* **Magenta:** Enlaces simbólicos (links).
* **Gris Oscuro:** Permisos y metadatos.

---

### 💡 Tip Pro: Búsqueda Difusa

No necesitas escribir la ruta exacta. Simplemente empieza a escribir letras.

* Ejemplo: Si escribes `conf` y luego `toml`, Broot encontrará `~/.config/broot/conf.toml` aunque estén en niveles muy profundos.

---

**¿Te gustaría que te ayude a crear un alias en tu sistema para que al escribir un comando corto se abra Broot con esta configuración específica?**


# ⚓ DOCUMENTO MAESTRO DE OPERACIONES TÁCTICAS: PROYECTO ARES LAYOUT
**Comandante, aquí se consolida toda la inteligencia técnica recopilada durante la incursión.**  
Este documento contiene la visión de diseño, el mapa de recursos, la arquitectura de módulos y un informe forense detallado de los problemas encontrados, con fragmentos de código, soluciones implementadas y el estado actual del Dragón.

---

## 1. VISIÓN DEL DISEÑO (LAYOUT UX/UI)
**Objetivo:** Interfaz *Responsive-Industrial* con contenedores invisibles, priorizando el contenido multimedia y eliminando el ruido ASCII.

### A. Bloque LLM (ARES)
- **Header (Flex-Row):**
  - **[Item 1: Avatar Square]** (4x4 celdas) – extremo izquierdo.
  - **[Item 2: Cintillo Banner]** – rectángulo dinámico al lado del avatar. Admite MP4 (Vivo), GIF o PNG. Identidad visual de la IA.
- **Body (Stream-Container):** Texto puro fluyendo en tiempo real debajo del header. Sin decoraciones para permitir copy-paste limpio.
- **Footer (Centered-Bar):** Un único **[GIF Separador]** centrado horizontalmente en la terminal. Sin avatar.

### B. Bloque Usuario
- **Header (Flex-Row):**
  - **[Item 1: Avatar Square]** (2x2 celdas) – izquierda.
  - **[Item 2: Invisible Header]** – rectángulo invisible a la derecha con un **[GIF Animado]** de identidad de usuario.
- **Footer:** Rectángulo igual al del LLM pero simplificado.

---

## 2. MAPA DE RECURSOS (RUTAS ABSOLUTAS)
Todos los activos residen en la *Armería Visual* de ARES:

| Recurso               | Ruta Absoluta                                                                 | Tipo       |
|-----------------------|-------------------------------------------------------------------------------|------------|
| Avatar IA             | `/home/daniel/tron/programas/TR/assets/ares/ares-neon.png`                    | PNG        |
| Avatar IA Wow (Vivo)  | `/home/daniel/tron/programas/TR/assets/ares/ares-wow.mp4`                     | MP4        |
| Avatar Usuario        | `/home/daniel/tron/programas/TR/assets/user/user-emoji.png`                   | PNG        |
| Spinners (carga)      | `/home/daniel/tron/programas/TR/assets/ui/layaout/spinner[1-7].gif`           | GIF        |
| Separadores           | `/home/daniel/tron/programas/TR/assets/ui/layaout/separador.gif`              | GIF        |
| Cintillo IA           | `/home/daniel/tron/programas/TR/assets/ui/layaout/header-ares.png`            | PNG        |

---

## 3. MÓDULOS CLAVE Y RESPONSABILIDADES
*Soberanía de Modularidad Atómica* – división táctica del sistema.

| Módulo            | Ruta Absoluta                               | Descripción Táctica                                                                                                 |
|-------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Orquestador       | `src/main.py`                               | Despachador puro. Recibe comandos (`ares i`, `ares maq`) y delega la ejecución. Blindado contra lógica de UI.      |
| Interfaz REPL     | `modules/ui/chat_interface.py`               | Gestor de Estados. Controla el loop, el streaming de texto y decide cuándo activar modo Wow o Light.                |
| Motor Gráfico     | `modules/ui/layout_engine.py`                | Constructor de Ilusión. Usa KGP (Kitty Graphics Protocol) para posicionar contenedores mediante coordenadas absolutas. |
| Optimizador       | `modules/multimedia/asset_optimizer.py`      | Gestor de RAM. Convierte MP4/GIF a PNG estático para el historial, liberando memoria tras la interacción activa.    |
| Configuración     | `config/layout_config.yaml`                  | Panel Soberano. Permite cambiar tamaños y rutas sin tocar código.                                                  |

---

## 4. INFORME TÉCNICO FORENSE: EVOLUCIÓN DEL MOTOR GRÁFICO ARES
Comandante, a continuación se detalla la anatomía de nuestra lucha por dominar el protocolo gráfico de Kitty, con fragmentos de código que ilustran cada error y su solución.

### 4.1. CRONOLOGÍA DE PROBLEMAS Y ERRORES ENCONTRADOS

| Error Detectado                | Explicación Técnica                                                                                                                                                                                                                                 | Impacto                                      | Fragmento de Código (Error)                                                                                             |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| **"Efecto Bizarro" (Lluvia de Base64)** | Superamos el límite de 4096 bytes del buffer de la terminal sin fragmentación. Kitty interpretó los datos binarios como texto, volcándolos en pantalla.                                                                                            | Terminal inundada de caracteres aleatorios.  | ```python\ncmd = f"\033_Ga=T,f=100;{b64_encoded_image}\033\\"\nsys.stdout.write(cmd)\n```                              |
| **"EINVAL: Zero width/height"**        | Uso incorrecto de unidades: se pasaron píxeles (`w`, `h`) en comandos que esperaban celdas (`c`, `r`), o viceversa.                                                                                                | Imágenes gigantes que desbordaban el diseño. | ```python\ncmd = {"a": "T", "w": "100", "h": "100"}   # MAL\n```                                                      |
| **"Colapso de Ventana" (Crash)**       | La IA intentó usar `termios` y `tty` para "ver" la respuesta de Kitty, entrando en conflicto con el proceso padre y causando un cierre abrupto.                                                                     | Cierre repentino de Kitty y pérdida de sesión.| ```python\nimport termios, tty\n...  # Operaciones no autorizadas en el flujo principal\n```                          |
| **"ENOENT: Non-existent image"**       | Sincronización fallida. Se intentó proyectar (`a=p`) o animar (`a=a`) una imagen antes de que Kitty terminara de procesar su transmisión.                                                                           | Spinners y separadores invisibles.           | ```python\ninject_asset(avatar)       # Envío inmediato\ninject_asset(spinner)   # Falla porque el ID aún no existe\n``` |
| **"Efecto Cuchillo" (Corte Horizontal)** | El cursor llegó al final de la línea física durante el renderizado, insertando un salto de línea en medio de la imagen.                                                                                             | Spinner dividido en dos partes desplazadas.  | ```python\n# Sin posicionamiento previo\nsys.stdout.write(gif_data)   # Kitty hace wrap automático\n```               |

### 4.2. LO QUE HEMOS INTENTADO (TÉCNICAS Y CÓDIGOS DE SOLUCIÓN)

#### Técnica 1: Fragmentación por Chunking (Solución al "Efecto Bizarro")
```python
# Fragmentación a 4KB por ráfaga - ESTABLE V6
chunk_size = 4096
for i in range(0, len(b64_data), chunk_size):
    chunk = b64_data[i:i+chunk_size]
    is_last = (i + chunk_size) >= len(b64_data)
    cmd = {
        "a": "T" if i == 0 else "",          # Solo el primer fragmento lleva "a=T"
        "m": "0" if is_last else "1",        # m=1 indica "más datos"
        "f": "100",                           # Formato PNG
        "t": "d",                              # Transmisión directa
        "d": chunk
    }
    sys.stdout.write(f"\033_G{encode_cmd(cmd)}\033\\")
    sys.stdout.flush()
```

#### Técnica 2: Uso Correcto de Unidades (Solución a "EINVAL")
```python
# Usar celdas (c, r) para maquetación basada en terminal - V7
cmd = {"a": "T", "c": "4", "r": "4"}  # Fuerza 4x4 celdas, independiente de resolución
# También se pueden usar s (ancho de fuente) y v (alto de fuente) si se requiere control por píxeles.
```

#### Técnica 3: Posicionamiento Absoluto ANSI (Solución al "Efecto Cuchillo")
```python
# V8: Forzar posición espacial antes de inyectar y evitar wrap
def inject_at(x, y, asset_data):
    sys.stdout.write(f"\033[{y+1};{x+1}H")   # Mover cursor a (x,y)
    cmd = {"a": "T", "C": "1"}                # C=1: no mover cursor tras la imagen
    # ... envío fragmentado del asset
    sys.stdout.flush()
```

#### Técnica 4: Pausas Tácticas para Sincronización (Solución a "ENOENT")
```python
# V11: Transmisión síncrona con pausa
inject_asset(avatar)          # Envía imagen y espera respuesta implícita
time.sleep(0.05)               # Pausa de sincronización necesaria
inject_asset(spinner)          # Ahora Kitty ya tiene el ID del avatar
```

#### Técnica 5: Tecnología Híbrida (KGP + Term-Image) para Spinners
Para evitar conflictos con múltiples ráfagas APC, se optó por usar la librería `term-image` para los spinners, que los trata como caracteres especiales.
```python
# V13: Uso de term-image para spinners (no interfiere con KGP)
from term_image.image import from_file
spinner_img = from_file(spinner_path, height=1)  # Altura de 1 celda
spinner_img.draw()   # Dibuja como un carácter, sin escapes APC complejos
```

### 4.3. LOGROS ALCANZADOS (COSA BUENA)
- ✅ **Soberanía Arquitectónica:** `main.py` es despachador puro; la lógica gráfica reside en módulos aislados.
- ✅ **Identidad Visual Base:** Bloque de Avatar + Rectángulo Gris es estable y se posiciona correctamente.
- ✅ **Control por YAML:** Tamaños y rutas se ajustan desde `layout_config.yaml` sin tocar código.
- ✅ **Rotación Cíclica:** Sistema capaz de alternar entre 7 spinners con índice persistente.
- ✅ **Protocolo Rodilla en Tierra:** Metodología de respaldos y metacognición ahora es ley en el sistema.

### 4.4. LO QUE AÚN NO FUNCIONA (EL RETO DEL DRAGÓN)
- ❌ **Animación Fluida de GIFs:** Kitty recibe los frames, pero el comando de ignición (`a=a`) sigue fallando por milisegundos de sincronización. A veces se congela en el primer frame.
- ❌ **Superposición de Cintillos:** El cintillo gráfico (`header-ares.png`) no logra sustituir al bloque gris de forma consistente en todas las ejecuciones.
- ❌ **Contenedores Invisibles:** Aún se percibe la "costura" entre el avatar y el texto debido a cómo Kitty gestiona los márgenes de celda.

### 4.5. DIAGNÓSTICO FINAL
Estamos intentando maquetar de forma secuencial algo que Kitty procesa de forma asíncrona. Para que el Dragón sea real, el próximo paso no es enviar más comandos, sino implementar un **Manejo de Tiempos y IDs** mucho más estricto, o cambiar a la tecnología de **Unicode Placeholders**, donde Kitty reserva un sitio en el texto para la imagen antes de dibujarla.

Comandante, el informe está en pantalla. ¿Desea que pivotemos hacia los Unicode Placeholders o seguimos refinando el protocolo de inyección directa?

**Instrucciones:** Copia todo el contenido dentro del bloque de código (desde ```markdown hasta ```) y pégalo en un archivo `.md` para tener el documento completo.


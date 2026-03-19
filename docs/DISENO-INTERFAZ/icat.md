# icat

*Mostrar imágenes en la terminal*

El `icat`gatito se puede usar para mostrar imágenes arbitrarias en la terminal *del gatito* . Usarlo es tan simple como:

kitten icat image.jpeg

Admite todos los tipos de imagen compatibles con [ImageMagick](https://www.imagemagick.org/) . Incluso funciona a través de SSH. Para más detalles, consulte el [protocolo gráfico kitty](https://sw.kovidgoyal.net/kitty/graphics-protocol/) .

Es posible que desee crear un alias en los archivos de configuración de su shell:

alias icat="kitten icat"

Luego, simplemente puede usarlo para ver imágenes.`icat image.png`

Nota

[ImageMagick](https://www.imagemagick.org/) debe estar instalado para poder utilizar todos los tipos de imagen. Sin él, solo se admiten PNG/JPG/GIF/BMP/TIFF/WEBP.

Nota

Es posible que el protocolo de visualización de imágenes de kitty no funcione cuando se utiliza dentro de un multiplexor de terminal como **screen** o **tmux** , dependiendo de si el multiplexor ha añadido soporte para ello o no.

El `icat`kit cuenta con varios argumentos de línea de comandos que permiten su uso desde otros programas para mostrar imágenes. En particular, [`--place`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-place), [`--detect-support`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-detect-support)y [`--print-window-size`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-print-window-size).

Si intentas integrar icat en un programa complejo como un gestor de archivos o un editor, hay algunas cosas que debes tener en cuenta. icat normalmente funciona comunicándose a través del dispositivo TTY, tanto escribiendo como leyendo desde él. Por lo tanto, es imprescindible que mientras se ejecuta, el programa anfitrión no realice ninguna operación de entrada/salida en el TTY. Cualquier pulsación de tecla u otra entrada del usuario en el dispositivo TTY se descartará. Si prefieres usarlo solo como backend para generar los códigos de escape para la visualización de imágenes, debes pasarle opciones para indicarle las dimensiones de la ventana, dónde colocar la imagen en la ventana y el modo de transferencia que debe usar. Si haces eso, no intentará comunicarse con el dispositivo TTY en absoluto. Las opciones necesarias son: [`--use-window-size`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-use-window-size), [`--place`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-place) y [`--transfer-mode`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-transfer-mode), [`--stdin=no`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-stdin). Por ejemplo, para demostrar el uso sin acceso al TTY:

zsh -c 'setsid kitten icat --stdin=no --use-window-size $COLUMNS,$LINES,3000,2000 --transfer-mode=file myimage.png'

Aquí, `setsid`se garantiza que icat no tenga acceso al dispositivo TTY. Los valores 3000 y 2000 son ficticios. Representan el ancho y alto de la ventana en píxeles, para obtener el acceso necesario al TTY.

Para lograr una mayor robustez, deberías considerar implementar soporte adecuado para el [protocolo gráfico Kitty](https://sw.kovidgoyal.net/kitty/graphics-protocol/) en el programa. Actualmente existen muchas bibliotecas que lo soportan.

## Código fuente para icat

El código fuente de este gatito está [disponible en GitHub](https://github.com/kovidgoyal/kitty/tree/master/kittens/icat) .

## Interfaz de línea de comandos

kitten icat [options] image-file-or-url-or-directory ...

Una utilidad tipo Cat para mostrar imágenes en la terminal. Puedes especificar varios archivos de imagen y/o directorios. Los directorios se escanean recursivamente en busca de archivos de imagen. Si STDIN no es una terminal, los datos de la imagen también se leerán desde allí. También puedes especificar URL HTTP(S) o FTP, que se descargarán y mostrarán automáticamente.

### Opciones

--alinear <ALIGN>

Alineación horizontal para la imagen mostrada. Predeterminado: `center` Opciones: `center`, `left`,`right`

--lugar <LUGAR>

Elige dónde mostrar la imagen en la pantalla. La imagen se escalará para ajustarse al rectángulo especificado. La sintaxis para especificar rectángulos es <ancho> x <alto> @ <izquierda> x <superior> . Todas las medidas están en celdas (es decir, posiciones del cursor) con el origen (0, 0) en la esquina superior izquierda de la pantalla. Ten en cuenta que esta [`--align`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-align)opción alineará horizontalmente la imagen dentro de este rectángulo. Por defecto, la imagen se centra horizontalmente dentro del rectángulo. Si usas esta opción, el cursor se posicionará en la esquina superior izquierda de la imagen, en lugar de en la línea que aparece después de la imagen.

--scale-up [=no]

Provoca que las imágenes que sean más pequeñas que el área especificada se amplíen para utilizar la mayor parte posible de dicha área. El área especificada depende de las opciones [`--place`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-place)o .[`--fit`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-fit)

--fit <FIT>

Cuando no se utiliza [`--place`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-place), controla cómo se escala la imagen en relación con la pantalla. Puedes hacer que se ajuste al ancho o alto de la pantalla, a ambos o a ninguno. Predeterminado: `width` Opciones: `both`, `height`, `none`,`width`

--fondo <FONDO>

Especifique un color de fondo; esto hará que las imágenes transparentes se compongan sobre el color especificado. Predeterminado:`none`

--mirror <MIRROR>

Reflejar la imagen respecto a un eje horizontal o vertical o ambos. Predeterminado: `none` Opciones: `both`, `horizontal`, `none`,`vertical`

--clear [=no]

Elimina todas las imágenes que se muestran actualmente en la pantalla. Ten en cuenta que esto no funciona con multiplexores de terminal como tmux, ya que solo el multiplexor puede conocer la posición de la pantalla.

--clear-all [=no]

Elimina todas las imágenes de la pantalla y desplázate hacia atrás. Ten en cuenta que con multiplexores de terminal como tmux, esto moverá las imágenes de todos los paneles.

--transfer-mode <MODO_TRANSFERENCIA>

Mecanismo a utilizar para transferir imágenes al terminal. Por defecto, se detecta automáticamente. `file` significa usar un archivo temporal, `memory` significa usar memoria compartida, `stream` significa enviar los datos mediante códigos de escape del terminal. Tenga en cuenta que si utiliza los modos de transferencia de archivo o memoria y se conecta a través de una sesión remota, la visualización de imágenes no funcionará. Predeterminado: `detect` Opciones: `detect`, `file`, `memory`,`stream`

--detect-support [=no]

Detecta la compatibilidad con la visualización de imágenes en la terminal. Si no es compatible, saldrá con el código de salida 1; de lo contrario, saldrá con el código 0 e imprimirá el modo de transferencia compatible en stderr, que se puede usar con la [`--transfer-mode`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-transfer-mode)opción.

--detection-timeout <DETECTION_TIMEOUT>

El tiempo (en segundos) que se debe esperar para obtener una respuesta del terminal al detectar la compatibilidad con la visualización de imágenes. Valor predeterminado:`10`

--use-window-size <USE_WINDOW_SIZE>

En lugar de consultar el tamaño de la ventana en la terminal, utilice el tamaño especificado, que debe tener el formato: ancho_en_celdas,alto_en_celdas,ancho_en_píxeles,alto_en_píxeles.

--print-window-size [=no]

Imprime el tamaño de la ventana como <ancho> x <alto> ( en píxeles) y finaliza. Este es un método práctico para consultar el tamaño de la ventana si se utiliza un lenguaje de scripting que no admite llamadas a termios.`kitten icat`

--stdin <STDIN>

Lee los datos de la imagen desde STDIN. Por defecto, se hace automáticamente cuando STDIN no es una terminal, pero puedes activarlo o desactivarlo explícitamente si es necesario. Predeterminado: `detect` Opciones: `detect`, `no`,`yes`

--silencioso [=no]

No se utiliza, se incluye para garantizar la compatibilidad con versiones anteriores.

--motor <MOTOR>

El motor utilizado para la decodificación y el procesamiento de imágenes. Por defecto, se utiliza el motor más apropiado. El `builtin`motor utiliza las bibliotecas de imágenes nativas de Go. El `magick`motor utiliza ImageMagick, que requiere que esté instalado en el sistema. Predeterminado: `auto` Opciones: `auto`, `builtin`,`magick`

--z-index <Z_INDEX> , -z <Z_INDEX>

Índice Z de la imagen. Si es negativo, el texto se mostrará encima de la imagen. Use un doble menos para valores inferiores al umbral para dibujar imágenes bajo los colores de fondo de las celdas. Por ejemplo, `--1`se evalúa como -1.073.741.825. Predeterminado:`0`

--loop <LOOP> , -l <LOOP>

Número de veces que se repetirán las animaciones. Los valores negativos indican que el bucle es infinito. Cero significa que solo se muestra el primer fotograma de la animación. De lo contrario, la animación se repite el número de veces especificado. Valor predeterminado:`-1`

--mantener [=no]

Espere a que se pulse una tecla antes de salir después de que se muestren las imágenes.

--unicode-placeholder [=no]

Utilice el método de marcador de posición Unicode para mostrar las imágenes. Es útil para mostrar imágenes desde programas de terminal a pantalla completa que no reconocen el protocolo gráfico Kitty, como multiplexores o editores. Consulte [Marcadores de posición Unicode](https://sw.kovidgoyal.net/kitty/graphics-protocol/#graphics-unicode-placeholders) para obtener más información. Tenga en cuenta que, al usar este método, las imágenes colocadas (con [`--place`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-place)) que no caben en la pantalla se ajustarán al borde de la pantalla en lugar de truncarse. Este ajuste se realiza por línea, por lo que la imagen parecerá intercalada con líneas en blanco.

--passthrough <PASSTHROUGH>

Si se deben rodear los comandos gráficos con secuencias de escape que les permitan pasar a través de programas como tmux. Por defecto, se detecta cuando se ejecuta dentro de tmux y se utilizan automáticamente los códigos de escape de paso de tmux. Tenga en cuenta que cuando esta opción está habilitada, [`--unicode-placeholder`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-unicode-placeholder)también implica. Predeterminado: `detect` Opciones: `detect`, `none`,`tmux`

--image-id <IMAGE_ID>

El identificador del protocolo gráfico que se utilizará para la imagen creada. Normalmente, se crea un identificador aleatorio si es necesario. Esta opción permite controlar el identificador. Cuando se envían varias imágenes, se utilizan identificadores secuenciales a partir del identificador especificado. Los identificadores válidos van del 1 al 4294967295. Los números fuera de este rango se ajustan automáticamente. Predeterminado:`0`

--no-trailing-newline [=no] , -n [=no]

Por defecto, el cursor se mueve a la siguiente línea después de mostrar una imagen. Esta opción lo impide. No debe usarse al mostrar varias imágenes en un catálogo. Tampoco tiene efecto cuando [`--place`](https://sw.kovidgoyal.net/kitty/kittens/icat/#cmdoption-kitty-kitten-icat-place)se usa la opción.

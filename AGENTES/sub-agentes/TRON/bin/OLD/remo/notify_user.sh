#!/bin/bash
# notify_user.sh - Un simple wrapper para notificaciones de escritorio con Zenity.

# Título por defecto para la ventana de notificación.
TITLE="Notificación del Sistema TRON"

# Asegurarse de que se proporcionó un mensaje.
if [ -z "$1" ]; then
    MESSAGE="Se ha solicitado una notificación, pero no se proporcionó ningún mensaje."
else
    MESSAGE="$1"
fi

# Comprobar si Zenity está instalado.
if ! command -v zenity &> /dev/null; then
    # Si no está, intentar mostrar un mensaje de error en la terminal.
    echo "Error: El comando 'zenity' no se encuentra. No se puede mostrar la notificación gráfica." >&2
    echo "Por favor, instálalo con: sudo apt-get install zenity" >&2
    exit 1
fi

# Mostrar la notificación de información.
# El texto se pasa como argumento al script.
zenity --info --title="$TITLE" --text="$MESSAGE" --width=400

# No se necesita botón de "Aceptar" explícito, Zenity lo incluye por defecto en --info.

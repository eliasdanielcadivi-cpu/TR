#!/bin/bash

# --- ARES DOWNLOADER SCRIPT (TR/scripts/descargar_yt.sh) ---
# Autor: Daniel Hung (v2.7 - 2026 iOS Edition)
# Objetivo: Evadir bots con cliente iOS (HLS) + Cookies Chrome (Gnome Keyring).

TIPO=$1  # audio, video, sub, full
URL=$2
TRON_PY_ROOT="/home/daniel/tron/programas/ENTORNOS/python"

if [ -z "$URL" ]; then
    echo "Uso: $0 [audio|video|sub|full] 'URL'"
    exit 1
fi

# 1. Configuración de Cookies (descifra v11 con secretstorage ahora instalado)
COOKIE_FLAGS=(
    "--cookies-from-browser" "chrome+gnomekeyring"
)

# 2. Configuración de Evasión 2026 (El cliente iOS es el menos bloqueado)
# Usamos el extractor de iOS porque usa un flujo de datos distinto (m3u8) que suele saltar el PO Token.
FLAGS=(
    "--js-runtime" "node"
    "--impersonate" "safari"  # Combina bien con cliente iOS
    "--no-check-certificate"
    "--extractor-args" "youtube:player_client=ios,web_safari"
)

# 3. Configuración de Subtítulos (Eng/Esp)
SUB_FLAGS=(
    "--write-subs"
    "--write-auto-subs"
    "--sub-lang" "en,es"
    "--convert-subs" "srt"
)

# Comando base usando el entorno de UV con TODAS las librerías activas
YTP_CMD="env -u VIRTUAL_ENV uv run --project $TRON_PY_ROOT yt-dlp"

case $TIPO in
    audio)
        $YTP_CMD "${COOKIE_FLAGS[@]}" "${FLAGS[@]}" -x -f "bestaudio" --ppa "EmbedThumbnail+ffmpeg_o:-c:v copy" --audio-quality 0 "$URL"
        ;;
    video)
        $YTP_CMD "${COOKIE_FLAGS[@]}" "${FLAGS[@]}" -f "bestvideo+bestaudio/best" --merge-output-format mp4 "$URL"
        ;;
    sub)
        $YTP_CMD "${COOKIE_FLAGS[@]}" "${FLAGS[@]}" "${SUB_FLAGS[@]}" --skip-download -o "%(title)s.%(ext)s" "$URL"
        ;;
    full)
        # Descarga video + subtítulos incrustados y por separado
        $YTP_CMD "${COOKIE_FLAGS[@]}" "${FLAGS[@]}" "${SUB_FLAGS[@]}" -f "bestvideo+bestaudio/best" --merge-output-format mp4 --embed-subs --embed-thumbnail --add-metadata "$URL"
        ;;
    *)
        echo "Opción no válida. Usa: audio, video, sub, full"
        exit 1
        ;;
esac

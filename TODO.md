# TODO: Reparar comandos de multimedia en ARES

## 1. Análisis y Preparación
- [x] Leer `LEEME.md` y documentación de arquitectura.
- [x] Identificar la falta de registro de comandos en `src/main.py`.
- [x] Verificar la implementación actual en `modules/multimedia/media_manager.py`.
- [x] Confirmar el comando mpv correcto para Kitty: `mpv --profile=sw-fast --vo=kitty --vo-kitty-use-shm=yes --really-quiet`.

## 2. Ejecución (Cirujano)
- [x] Registrar comando `video` en `src/main.py`.
- [x] Registrar comando `image` en `src/main.py`.
- [x] Corregir lógica de `show_image` para usar `--place` y evitar errores de `unknown option`.
- [x] **Limpieza:** Eliminar mensajes de "Reproduciendo" que ensucian la salida.
- [x] **Corrección:** Quitar carga explícita de `mpv.conf` en `play_video` para evitar conflictos y asegurar que use el comando base verificado.

## 4. Gestión de Sesiones (Kitty Socket)
- [x] Crear directorio `test` y `db` si no existen.
- [x] Crear script `test/capture_session.py` para leer el socket.
- [x] Extraer nombres de ventanas (OS), pestañas y sus IDs.
- [x] Guardar captura en `db/last_session.json` de forma estructurada.
- [ ] Implementar comando `guardaSesion` en `main.py` delegando al nuevo módulo.

## 4. Notas para el Usuario
- [x] Informar sobre el problema de zsh globbing (corchetes `[]` en nombres de archivos requieren escape o desactivar globbing temporalmente).

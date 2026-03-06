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

## 3. Validación
- [x] Probar `ares video <ruta>` con un archivo real. (Exitoso)
- [x] Probar `ares image <ruta>` con archivos reales. (Exitoso tras corrección)
- [x] Verificar que no se rompan otras funcionalidades.

## 4. Notas para el Usuario
- [x] Informar sobre el problema de zsh globbing (corchetes `[]` en nombres de archivos requieren escape o desactivar globbing temporalmente).

# skill-sesion

## Propósito
Gestionar el ciclo de vida de las sesiones de terminal Kitty en ARES. Permite guardar el estado actual, listar sesiones disponibles, restaurarlas y ejecutar comandos en pestañas específicas.

## Cuándo usar
- "guarda sesión", "respalda terminal", "gs"
- "lista sesiones", "qué sesiones hay"
- "restaura sesión [nombre]", "vuelve a abrir la sesión de ayer"
- "ejecuta [comando] en [pestaña]", "manda esto a la pestaña de código"

## Entradas requeridas
- `nombre_sesion`: string (para guardar/restaurar)
- `nombre_pestaña`: string (para ejecutar comandos)
- `comando`: string (comando simple o encadenado con ;)

## Flujo de ejecución

### 1. Guardar Sesión
- **Comando:** `ares gs [nombre]`
- Si no se especifica nombre, el sistema preguntará.
- Almacena ventanas y títulos en `db/`.

### 2. Listar Sesiones
- **Comando:** `ares gs list`
- Muestra los nombres de las sesiones disponibles en la base de datos JSON.

### 3. Restaurar Sesión
- **Comando:** `ares gs restore [nombre]`
- Abre nuevas pestañas en Kitty con los títulos originales guardados.

### 4. Enviar Comandos (Orquestación Remota)
- **Comando:** `ares gs com "[pestaña]" "[comando]"`
- Útil para automatizar el inicio de una sesión restaurada.
- Ejemplo: `ares gs com "MATRIX" "cd ~/proyectos; ls -la"`

## Validaciones críticas
- [ ] Kitty debe estar corriendo con el socket ARES (`ares status` para verificar).
- [ ] Los nombres de pestañas en `gs com` deben coincidir exactamente con el título.
- [ ] La base de datos reside en `TR/db/`.

## Reglas de oro ARES
- **No duplicar**: Antes de restaurar, el usuario suele preferir una ventana limpia.
- **Soberanía**: El usuario decide cuándo enviar comandos destructivos.
- **Encadenamiento**: Prefiere comandos encadenados con `;` para ejecuciones de una sola línea.

## Despliegue Dinámico y Titulado Inteligente
Si el usuario pide abrir varias pestañas con comandos pero no da títulos, la IA debe:
1.  **Analizar el comando**: Si es `npm run dev`, el título es `WEB-DEV`. Si es `python`, es `PY-CORE`. Si es `repo`, es `AUDIT`.
2.  **Formato de Título**: Mayúsculas, corto, semántico (máx 10 caracteres).
3.  **Ejecución**: Usar `ares gs com "[TITULO]" "[comando]"` después de asegurar que la pestaña existe (o usar `launch --tab-title=[TITULO]`).

## Verificación de Éxito (Protocolo Papelera)
Para comprobar que los comandos se ejecutaron correctamente en las pestañas, se recomienda añadir una redirección a un archivo en la papelera.
**Ejemplo de comando verificable:**
`ares gs com "TEST" "ls -la > papelera/test_ls.txt"`

Si el archivo `papelera/test_ls.txt` aparece, el orquestador ha funcionado.

## Ejemplo de Intención Compleja
Usuario: "Abre tres pestañas: una para ver los logs, otra para correr el servidor y otra para auditar el repo"
IA genera:
1. `ares gs com "LOGS" "tail -f storage/logs/laravel.log > papelera/log_check.txt"`
2. `ares gs com "SERVER" "php artisan serve > papelera/server_check.txt"`
3. `ares gs com "AUDIT" "repo status > papelera/repo_check.txt"`
*(Nota: Si las pestañas no existen, la IA debe lanzarlas primero usando execute_shell con kitty launch)*

## Output (JSON para Agentes)
```json
{
  "estado": "ok",
  "accion": "sesion_gestionada",
  "datos": {
    "operacion": "guardar|restaurar|listar|comando",
    "nombre": "{nombre_sesion}",
    "resultado": "{mensaje_sistema}"
  }
}
```

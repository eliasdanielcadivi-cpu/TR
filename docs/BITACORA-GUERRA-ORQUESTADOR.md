# 🛰️ Orchestrator - Inteligencia de Despliegue Dinámico

## 📋 Descripción
Este módulo centraliza la orquestación de sesiones de Kitty en ARES. Permite transformar archivos JSON de sesión en entornos de trabajo vivos, con pigmentación Hacker Neon y ejecución determinista de comandos.

---

## 🔬 Bitácora de Guerra (Problemas Pegajosos y Soluciones)

Durante el desarrollo de este módulo se enfrentaron retos técnicos críticos que definieron su arquitectura resiliente:

### 1. El Desafío de las TUIs (Broot/Micro)
- **Problema**: Al intentar capturar errores de arranque con `2> log.txt`, las interfaces visuales (TUI) como Broot desaparecían o se mostraban vacías.
- **Causa**: Muchas TUIs utilizan el canal de error (`stderr`) para renderizar gráficos o capturar eventos.
- **Solución**: Se eliminó la redirección de errores en la ejecución principal. En su lugar, se implementó el encadenamiento `exec zsh -i`, permitiendo que el programa use todos los canales de salida y que la pestaña permanezca abierta si el proceso finaliza.

### 2. El "Pestañeo" de Cierre Prematuro
- **Problema**: Las pestañas se abrían y cerraban en milisegundos.
- **Causa**: Kitty cierra la pestaña inmediatamente cuando el comando principal termina.
- **Solución**: Uso de `sh -c "comando; exec zsh -i"`. Esto garantiza que, incluso tras el éxito o fallo del comando, el usuario mantenga el control en una shell interactiva.

### 3. Sincronía de Socket y Handshake
- **Problema**: Intentar enviar comandos antes de que Kitty terminara de levantar el socket.
- **Causa**: Latencia en la creación de descriptores de archivos UNIX.
- **Solución**: Implementación de un bucle de espera activa con `kitten @ ls` como señal de salud (Handshake) antes de proceder con el despliegue.

---

## 🛠️ Funcionalidades Core
1. **`deploy_session_from_db`**: Carga JSON de `db/`, lanza ventana (respetando Título Soberano) y despliega pestañas.
2. **Ciclo Cromático de 12 Niveles**: Pigmentación automática `index % 12` basada en la paleta Hacker Neon.
3. **Inyección Determinista**: Uso de `exec` para asegurar que el proceso del programa sea el líder de la pestaña.

---

## 📝 Nota para IAs
Al usar este módulo, siempre prefiere el método `deploy_session_from_db`. Si el usuario pide comandos encadenados, asegúrate de unirlos con `;` y usar el envoltorio de persistencia `zsh -i`.

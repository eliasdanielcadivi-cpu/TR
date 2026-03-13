# TR: LISTA MAESTRA DE REQUERIMIENTOS (EXTENSIVA)

Este documento es el registro vivo de todas las tareas, funciones y metas de **TR**. Cada punto debe ser cumplido, evaluado y puesto en producción.

## FASE 0: FUNDAMENTACIÓN Y ARQUITECTURA (001-020)
1. **R001**: Implementar jerarquía de carpetas visible según protocolo `FINAL`.
2. **R002**: Inicializar entorno con `uv` y `pyproject.toml`.
3. **R003**: Configurar `venv/` visible (sin punto).
4. **R004**: Crear script `ini` local para facilitar la puesta en producción global.
5. **R005**: Definir esquema de configuración YAML en `config/config.yaml`.
6. **R006**: Implementar soporte para API DeepSeek con gestión de API Keys segura (vía `.env`).
7. **R007**: Implementar soporte para API Ollama (Localhost).
8. **R008**: Crear sistema de logging en JSONLines para auditoría de IA.
9. **R009**: Establecer socket de comunicación Kitty en `/tmp/tron-kitty`.
10. **R010**: Implementar verificador de dependencias (kitty, ollama, gum, fzf).

## FASE 1: CONTROL REMOTO DE KITTY (021-040)
11. **R021**: Función para crear nuevas pestañas con nombre personalizado.
12. **R022**: Función para cerrar pestañas/ventanas por ID o nombre.
13. **R023**: Implementar cambio de enfoque (focus) entre ventanas mediante scripts.
14. **R024**: Implementar cambio de colores de pestaña dinámicamente.
15. **R025**: Soporte para layouts de Kitty (splits, stack, tall, fat).
16. **R026**: Función de redimensionamiento de ventanas desde CLI.
17. **R027**: Implementar "Broadcast" (enviar comando a todas las ventanas).
18. **R028**: Capacidad de obtener el estado actual de Kitty (JSON) para la IA.
19. **R029**: Renombrado dinámico de ventanas basado en el proceso en ejecución.
20. **R030**: Integración con Openbox para posicionamiento absoluto de la terminal.

## FASE 2: GESTIÓN DE SESIONES INTELIGENTE (041-060)
21. **R041**: Guardado de sesión actual (tabs, ventanas, rutas, comandos) en `data/sessions/`.
22. **R042**: Carga de sesiones por nombre.
23. **R043**: Sistema de "Snapshot" automático cada X minutos.
24. **R044**: Capacidad de la IA para sugerir nombres de sesión basados en el contexto.
25. **R045**: Restauración de entornos de desarrollo (Abrir editor, logs y server en una sesión).
26. **R046**: Persistencia del historial de comandos por sesión.
27. **R047**: Identificación de pestañas por colores según el tipo de proyecto.
28. **R048**: Sincronización de variables de entorno entre pestañas de una sesión.
29. **R049**: Gestión de "Workspaces" lógicos que agrupan sesiones.
30. **R050**: Exportación de configuración de Kitty por sesión.

## FASE 3: MULTIMEDIA Y VISUALIZACIÓN (061-080)
31. **R061**: Comando `tr view <img/video>` para previsualización rápida.
32. **R062**: Integración de `icat` para mostrar imágenes dentro de la terminal.
33. **R063**: Uso de `mpv` (modo minimalista o embed) para video.
34. **R064**: IA capaz de describir el contenido de una imagen (vía Ollama/Llava).
35. **R065**: Galería rápida de archivos multimedia en el directorio actual (`fzf` + `icat`).
36. **R066**: Soporte para visualización de PDF (vía conversión a imagen temporal).
37. **R067**: Comandos para captura de pantalla y visualización inmediata.
38. **R068**: Gestión de brillo/volumen desde la interfaz TR.
39. **R069**: Capacidad de "Pin" multimedia en una ventana pequeña flotante.
40. **R070**: Integración con herramientas de edición rápida (ImageMagick/FFmpeg).

## FASE 4: CEREBRO IA - ORQUESTADOR (081-120)
41. **R081**: Prompt System maestro para el Orquestador (Contexto de programador).
42. **R082**: Implementación de "Pensamiento en Cadena" (Chain of Thought) para tareas complejas.
43. **R083**: Traductor de lenguaje natural a comandos Kitty JSON.
44. **R084**: Ejecución multietapa: "IA, abre un entorno de node, instala express y levanta el server".
45. **R085**: Manejo de errores: Si un comando falla, la IA debe proponer corrección.
46. **R086**: Integración de DeepSeek Context Caching para ahorrar tokens en sesiones largas.
47. **R087**: Selección dinámica de modelo (Ollama para tareas rápidas, DeepSeek para complejas).
48. **R088**: Memoria a corto plazo de la sesión (últimos 50 comandos/salidas).
49. **R089**: Capacidad de leer archivos locales para proporcionar contexto a la IA.
50. **R090**: Sistema de "Agentes" especializados (Debug, Refactor, SysAdmin).
51. **R091**: Interfaz de chat minimalista integrada en una ventana de Kitty lateral.
52. **R092**: Comando de voz (opcional/futuro) -> Texto -> Comandos.
53. **R093**: Búsqueda semántica en la documentación del proyecto (`db/`).
54. **R094**: Generación de scripts Bash/Python al vuelo y ejecución bajo demanda.
55. **R095**: Autocompletado inteligente basado en el proyecto actual.

## FASE 5: HERRAMIENTAS DE DESARROLLADOR (121-150)
56. **R121**: Analizador de logs en tiempo real con alertas visuales.
57. **R122**: Integración con Git (Status visual, sugerencia de commits por IA).
58. **R123**: Comando `tr doctor` para diagnosticar problemas en el entorno local.
59. **R124**: Benchmarking de código rápido vía IA.
60. **R125**: Generador de documentación automática (`Docs/`).

... (Continuará hasta 1000)

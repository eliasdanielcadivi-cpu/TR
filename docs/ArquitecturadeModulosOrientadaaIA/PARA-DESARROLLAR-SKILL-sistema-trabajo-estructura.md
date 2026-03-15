**Documentos clave que rigen este diseño:**
- `VersionIaArquitecturadeMódulosOrientadaaIA.md`: Máximo 3 funciones/módulo, organización paranoica, papelera/, docs/ para lo problemático, LEEME.md como verdad funcional
- `RECOMENDACIONES-OLLAMA-MODELFILE-VARIABLES-ENTORNO-POR-MODELO.md`: Contexto limitado (8K tokens), RAM <1GB, lectura selectiva
- Tus memorias actuales: TRON tools (ini, com, repo), filosofía ARES headless, soberanía tecnológica

## Metodología de Avance Empírico y Registro de Trazabilidad

Para asegurar el progreso constante sin regresiones y mantener la soberanía de autoría, se establece el siguiente protocolo de obligatorio cumplimiento para la IA:

1.  **Inyección Documental Previa**: Antes de proponer cambios estructurales, la IA debe leer los documentos técnicos pertinentes (ej. `COLOR_SYSTEM.md`, `VENTANA_VS_PESTANA.md`).
2.  **Protocolo de No Borrado (Snapshotting)**:
    - Las versiones de scripts que alcancen hitos funcionales (ej. "Abre ventana OK") deben respaldarse físicamente con nombres descriptivos (ej. `abrió-ventana-OK.py`).
    - Estas versiones sirven como puntos de restauración inmediata en caso de fallo en la siguiente iteración.
3.  **Validación Granular por Hitos**:
    - No realizar validaciones de "todo o nada". 
    - Descomponer la verificación en una batería de preguntas granulares (vía Zenity o consola) que aíslen fallos de títulos, colores, sockets y comandos.
4.  **Registro de Logros (INDEX-TESTS.md)**:
    - Cada experimento exitoso debe documentarse en `docs/INDEX-TESTS.md`, detallando el objetivo, los errores superados y los artefactos generados.
    - Este registro es la base legal y operativa para comprobar la evolución del sistema y la autoría del diseño.
5.  **Aislamiento de Sockets**: Para pruebas de orquestación, usar siempre sockets aislados (`--listen-on unix:/tmp/test_socket`) para no interferir con el entorno de trabajo principal hasta la consolidación final.

---

## 👁️ Directiva de IA: Visión y Constatación Soberana
**Definición descriptiva:** "Voy a concluir los programas, pruebas y scripts no de la manera tradicional (tarea realizada). Cuando se necesite una confirmación o mensaje al usuario o se realice una prueba, yo primero tendré que crear mecanismos de visión y constatación que ciertamente el trabajo se realizó, al menos desde dos perspectivas independientes y luego, basado en eso, se condicionará el mensaje o salida de respuesta al usuario o al sistema."

**Protocolo de Cierre IA:**
- **Perspectiva 1 (Técnica):** Validación de buffers, secuencias ANSI, IDs de imagen o logs de ejecución.
- **Perspectiva 2 (Estructural):** Verificación de integridad de archivos, importaciones y cumplimiento de la modularidad atómica.

---

## 🛠️ Directiva de Validación Git (Post-CRUD)
**Obligatoriedad:** Al finalizar la edición de funcionalidades (Cambio, Eliminación, Actualización) que involucren documentos de documentación, `LEEME.md`, agendas o código, la IA **DEBE** ejecutar `git diff`.
**Objetivo:** Constatar fehacientemente que se editó o borró exactamente lo que se debía, evitando truncamientos accidentales o pérdida de contexto histórico.

---

## 🤝 Protocolo de Coexistencia IA: `dont-touch-my-eggs.md`
Para evitar colisiones cuando trabajan dos o más IAs en el mismo proyecto, es obligatorio el uso del "Cuaderno de Apartado".
- **Ubicación:** Raíz del proyecto (`/dont-touch-my-eggs.md`).
- **Uso:** Toda IA, antes de operar, debe leer este cuaderno y anotar su reservación de módulos o documentos (Nombre IA, Fecha, Hora, Archivos Reservados).
- **Referencia:** Ver detalle en `LEEME.md` y el propio archivo de apartado.

---

## Iteración 2: Estructura base de cada skill

Decisión: Cada skill sigue plantilla idéntica para que la IA prediga el formato:
```
# skill-[nombre]
## Propósito
## Cuándo usar (trigger exacto)
## Entradas requeridas
## Flujo de ejecución (pasos numerados)
## Validaciones críticas
## Outputs (JSON obligatorio)
## Reglas de oro (límites ARES)
## Relación con otros skills (solo referencia, no dependencia)
```

---

## Iteración 3: Desarrollo completo de los 4 skills

---

### skill-inicializacion

```markdown
# skill-inicializacion

## Propósito
Crear estructura base de proyecto ARES con organización paranoica. Establecer documentación mínima viable para que IA pueda navegar sin desperdiciar tokens.

## Cuándo usar
- Usuario dice: "inicializa proyecto", "nuevo proyecto", "crea estructura", "empezar"
- Directorio vacío o sin REP_STRUCTURE.md
- Antes de cualquier código

## Entradas requeridas
- `nombre_proyecto`: string (opcional, default=basename pwd)
- `tipo_proyecto`: "python" | "node" | "mixed" (default="python")

## Flujo de ejecución

1. **Validar espacio de trabajo**
   - Verificar que no existe conflicto de nombres
   - Confirmar permisos de escritura
   - Si existe LEEME.md, abortar con error: "Proyecto ya inicializado"

2. **Crear jerarquía paranoica**
   ```
   {nombre_proyecto}/
   ├── .ai/
   │   └── rules.md              # Límites de contexto y RAM
   ├── bin/                      # Binarios externos (vacío inicial)
   ├── config/                   # Configuración centralizada (vacío)
   ├── docs/
   │   ├── skills/               # Capabilities del proyecto
   │   │   ├── skill-inicializacion.md  # Este archivo (copia)
   │   │   └── INDEX.md          # Índice de skills disponibles
   │   └── .ai/                  # Reglas específicas del proyecto
   │       └── context.md        # Variables de entorno, modelos usados
   ├── src/
   │   ├── core/                 # Lógica principal (vacío)
   │   ├── modules/              # Módulos normales (vacío)
   │   └── api/                  # Endpoints si aplica (vacío)
   ├── Agentes/                  # Módulos LLM con JSON output (vacío)
   ├── papelera/                 # Código experimental no funcional (vacío)
   ├── tests/                    # Validaciones (vacío)
   ├── LEEME.md                  # Única fuente de verdad funcional
   └── REP_STRUCTURE.md          # Mapa operativo para IA
   ```

3. **Generar archivos base con contenido mínimo**

   **LEEME.md:**
   ```markdown
   # {nombre_proyecto}
   
   ## Estado: [INIT] {fecha}
   ## Funcionalidades Operativas: Ninguna
   ## Módulos en Desarrollo: Ninguno
   ## En Papelera: Ninguno
   
   ---
   ### Registro de Cambios Funcionales
   - {fecha}: Inicialización estructura ARES
   ```

   **REP_STRUCTURE.md:**
   ```markdown
   # REP_STRUCTURE.md — Mapa Operativo IA
   
   ## Contexto Límite
   - num_ctx: 8192 tokens
   - RAM máxima conversación: 1GB
   - Sliding window: últimas 5-7 interacciones
   
   ## Jerarquía de Lectura Obligatoria
   1. `.ai/rules.md` → límites técnicos
   2. `REP_STRUCTURE.md` → este archivo (mapa)
   3. `LEEME.md` → estado real del proyecto
   4. `docs/skills/skill-{tarea}.md` → capability específica
   
   ## Estructura de Carpetas
   
   | Ruta | Contenido | ¿Lee IA? |
   |------|-----------|----------|
   | `.ai/rules.md` | Restricciones hardware/contexto | Siempre primero |
   | `docs/skills/` | Capabilities ejecutables | Bajo demanda |
   | `src/core/` | Lógica principal | Según tarea |
   | `src/modules/` | Módulos CLI/importables | Según tarea |
   | `Agentes/` | Módulos LLM, JSON output | Si tarea requiere LLM |
   | `bin/` | Binarios externos | Solo configs |
   | `config/` | Configuración centralizada | Solo si aplica |
   | `papelera/` | Código no funcional | No (salvo instrucción) |
   
   ## Reglas de Oro
   - Nunca asumir funcionalidades no listadas en LEEME.md
   - Cargar solo código necesario para tarea actual
   - Máximo 3 funciones por módulo
   - JSON estructurado para outputs de Agentes/
   ```

   **.ai/rules.md:**
   ```markdown
   # AI Execution Rules — {nombre_proyecto}
   
   ## Límites Hard
   - num_ctx: 8192 tokens (conservador)
   - RAM dedicada: <1GB por conversación activa
   - num_batch: 512 (máximo)
   
   ## Estrategia de Memoria
   - Contexto inmediato: últimas 5 interacciones completas (≈20K tokens)
   - Resumen histórico: >5 interacciones condensadas a 500 tokens
   - Documentación RAG: recuperación vectorial de 60K tokens máx
   
   ## Exclusiones Absolutas
   - `node_modules/`, `.git/`, `__pycache__/`, `*.pyc`
   - `papelera/` (salvo comando explícito "revisar papelera")
   - Código fuente en `bin/` (solo leer configs)
   
   ## Formato de Output
   - Módulos normales: código limpio, ≤3 funciones, comentarios solo en lo complejo
   - Agentes/: JSON obligatorio con campos: estado, accion, datos
   - Skills: según plantilla skill-{nombre}.md
   ```

   **docs/skills/INDEX.md:**
   ```markdown
   # Índice de Skills — {nombre_proyecto}
   
   | Skill | Estado | Descripción | Trigger |
   |-------|--------|-------------|---------|
   | inicializacion | [OK] | Crear estructura base | "inicializa", "nuevo proyecto" |
   | desarrollo | [PENDIENTE] | Crear módulos con calidad | "nuevo módulo", "desarrolla" |
   | mantenimiento | [PENDIENTE] | Gestionar código existente | "mantener", "a papelera", "adaptar" |
   | produccion | [PENDIENTE] | Globalizar via ini | "producir", "globalizar", "a /usr/bin" |
   
   Leyenda: [OK]=Documentado y listo | [PENDIENTE]=No creado aún | [DEP]=Deprecado
   ```

4. **Actualizar LEEME.md con estado inicial**
   - Estado: [INIT]
   - Funcionalidades: Ninguna
   - Registrar timestamp

5. **Confirmar al usuario**
   - Mostrar árbol de carpetas creadas (2 niveles)
   - Indicar próximo paso sugerido: "Usar skill-desarrollo para crear primer módulo"

## Validaciones críticas

- [ ] No sobreescribir proyecto existente (LEEME.md presente)
- [ ] Crear exactamente las carpetas documentadas (ni más ni menos)
- [ ] Contenido de LEEME.md debe ser mínimo pero semántico
- [ ] INDEX.md debe reflejar estado real (solo inicializacion como [OK])

## Outputs

### JSON estructurado (para Agentes/ si aplica)
```json
{
  "estado": "ok",
  "accion": "inicializacion_completa",
  "datos": {
    "proyecto": "{nombre_proyecto}",
    "ruta": "{ruta_absoluta}",
    "estructura_creada": [".ai", "bin", "config", "docs/skills", "src/core", "src/modules", "src/api", "Agentes", "papelera", "tests"],
    "archivos_base": ["LEEME.md", "REP_STRUCTURE.md", ".ai/rules.md", "docs/skills/INDEX.md"],
    "siguiente_paso": "skill-desarrollo para crear primer módulo"
  }
}
```

### Output CLI (para humano)
```
⚡ Proyecto '{nombre_proyecto}' inicializado en {ruta}
Estructura ARES creada: 10 carpetas, 4 archivos base
Estado: [INIT] — Listo para skill-desarrollo
```

## Reglas de oro ARES

1. **Organización paranoica**: Todo elemento tiene ubicación explícita, nada suelto
2. **Documentación mínima viable**: Solo lo necesario para IA con contexto limitado
3. **LEEME.md es verdad**: Si no está ahí, no existe funcionalmente
4. **No adelantarse**: Skills de desarrollo/mantenimiento/produccion quedan como [PENDIENTE] en INDEX.md

## Relación con otros skills

| Skill | Relación | Nota |
|-------|----------|------|
| desarrollo | Siguiente en flujo natural | Después de inicializar, se desarrolla |
| mantenimiento | No aplica en proyecto nuevo | Sin código aún, no hay qué mantener |
| produccion | No aplica sin código | Requiere módulos funcionales primero |

**Independencia**: Este skill no carga ni depende de otros. Es punto de entrada único.
```

---

### skill-desarrollo

```markdown
# skill-desarrollo

## Propósito
Crear módulos atómicos con calidad integrada desde el inicio. Desarrollo no es solo escribir código: es escribir, validar, documentar lo problemático, y descartar lo no funcional a papelera.

## Cuándo usar
- Usuario dice: "nuevo módulo", "desarrolla", "crea función para...", "implementa"
- Existe LEEME.md (proyecto inicializado)
- Tarea involucra código nuevo o modificación sustancial

## Entradas requeridas
- `nombre_modulo`: string (kebab-case o snake_case)
- `tipo`: "lib" | "cli" | "hibrido" | "agente"
- `descripcion`: string (una línea, qué hace)
- `complejidad`: "simple" | "complejo" (default="simple")

## Flujo de ejecución

1. **Pre-validación del espacio**
   - Leer LEEME.md: verificar estado proyecto, ver módulos existentes
   - Leer REP_STRUCTURE.md: confirmar rutas válidas
   - Verificar que `nombre_modulo` no existe en `src/modules/` ni `Agentes/`
   - Si existe: abortar o sugerir skill-mantenimiento para modificación

2. **Determinar ubicación según tipo**
   
   | Tipo | Ubicación | Características |
   |------|-----------|----------------|
   | "lib" | `src/modules/{nombre}/` | Solo importable, sin __main__ |
   | "cli" | `src/modules/{nombre}/` | Ejecutable, argparse, ayuda interna |
   | "hibrido" | `src/modules/{nombre}/` | Importable + ejecutable |
   | "agente" | `Agentes/{nombre}/` + `src/modules/{nombre}/` | JSON output obligatorio, conexión LLM |

3. **Crear estructura del módulo**

   **Para lib/cli/hibrido:**
   ```
   src/modules/{nombre}/
   ├── __init__.py          # Exports principales
   └── funciones.py         # Lógica (máximo 3 funciones)
   ```

   **Para agente:**
   ```
   src/modules/{nombre}/    # Lógica reutilizable
   ├── __init__.py
   └── funciones.py
   
   Agentes/{nombre}/        # Wrapper LLM
   ├── agente.py            # Conexión modelo, JSON output
   └── config.yaml          # Parámetros específicos del agente
   ```

4. **Aplicar plantilla de código (regla de 3 funciones máximo)**

   **Plantilla lib/hibrido:**
   ```python
   # Módulo: {nombre}
   # Tipo: {tipo}
   # Propósito: {descripcion}
   # Creado: {fecha} via skill-desarrollo
   
   def funcion_principal(parametro):
       """
       Docstring descriptivo.
       
       Args:
           parametro: tipo y descripción
       
       Returns:
           tipo y descripción
       
       Nota: Comentar solo lo complejo o costoso de resolver.
       """
       pass  # TODO: Implementar lógica
   
   def funcion_auxiliar(dato):
       """Docstring conciso."""
       pass
   
   def utilidad_interna(valor):
       """Docstring conciso."""
       pass
   
   # Si tipo=hibrido o cli:
   if __name__ == "__main__":
       import sys
       # Implementar CLI mínimo
       funcion_principal(sys.argv[1] if len(sys.argv) > 1 else None)
   ```

   **Plantilla agente:**
   ```python
   # Agente: {nombre}
   # Conexión LLM: [especificar modelo en config.yaml]
   # Output: JSON estructurado obligatorio
   
   import json
   from src.modules.{nombre} import funcion_principal
   
   def ejecutar_agente(entrada):
       """
       Procesa entrada via LLM y retorna JSON estructurado.
       """
       resultado = funcion_principal(entrada)
       return {
           "estado": "ok" if resultado else "error",
           "accion": "{nombre}_ejecutado",
           "datos": {
               "entrada": entrada,
               "resultado": resultado,
               "timestamp": "{fecha}"
           }
       }
   
   if __name__ == "__main__":
       import sys
       print(json.dumps(ejecutar_agente(sys.argv[1]), indent=2))
   ```

5. **Aplicar depuración desde inicio (calidad integrada)**
   
   - [ ] Verificar sintaxis: `python -m py_compile` (si es Python)
   - [ ] Verificar imports: no circular dependencies
   - [ ] Aplicar permisos: `chmod +x` si es CLI/agente
   - [ ] Validar que cumple regla de 3 funciones máximo
   - [ ] Comentar SOLO lo complejo (no obvio)

6. **Documentar según complejidad**
   
   Si `complejidad="simple"`:
   - Solo comentarios en código
   - Actualizar LEEME.md: `[DEV] Módulo {nombre} ({tipo}) creado`
   
   Si `complejidad="complejo"`:
   - Crear `docs/{nombre}.md` con:
     - Problema que resuelve
     - Decisiones técnicas difíciles tomadas
     - Errores previos evitados
     - Cómo adaptar a otros contextos
   - Actualizar LEEME.md: `[DEV] Módulo {nombre} ({tipo}, complejo, docs/{nombre}.md)`

7. **Validación funcional mínima**
   
   - Ejecutar módulo con datos de prueba básicos
   - Si falla: aplicar fix inmediato o mover a papelera/ (ver regla de oro)
   - Si funciona: confirmar creación

8. **Actualizar índices**
   
   - Añadir a `docs/skills/INDEX.md` si es nuevo capability
   - Actualizar `LEEME.md` sección "Módulos en Desarrollo"

## Validaciones críticas

- [ ] Máximo 3 funciones principales (contar: def ...)
- [ ] Si hay más de 3: dividir en submódulos o simplificar
- [ ] Agente sin JSON output: rechazar, no cumple especificación ARES
- [ ] CLI sin ayuda interna (--help): rechazar
- [ ] Sin comentarios en código obvio (violación "solo lo complejo")

## Manejo de fallos: Regla de papelera

Si durante desarrollo el módulo:
- No compila después de 3 intentos de fix
- Excede 3 funciones y no puede simplificarse
- Requiere dependencias externas no disponibles

**Acción inmediata:**
1. Mover directorio completo a `papelera/{nombre}_{fecha}/`
2. Crear `papelera/{nombre}_{fecha}/NOTA.md` explicando por qué falló
3. Actualizar LEEME.md: `[PAPELERA] {nombre}: [razón breve]`
4. Informar usuario: "Módulo movido a papelera, ver NOTA.md para detalles"

## Outputs

### JSON estructurado
```json
{
  "estado": "ok|papelera|error",
  "accion": "desarrollo_modulo",
  "datos": {
    "nombre": "{nombre}",
    "tipo": "{tipo}",
    "ruta": "src/modules/{nombre}/|Agentes/{nombre}/",
    "complejidad": "{simple|complejo}",
    "documentacion_extra": "docs/{nombre}.md|null",
    "funciones_count": 3,
    "validacion": "ok|movido_a_papelera"
  }
}
```

### Output CLI
```
✅ Módulo '{nombre}' ({tipo}) creado en src/modules/{nombre}/
   Funciones: 3/3 máximo | Complejidad: {complejidad}
   Estado: [DEV] — Listo para pruebas o skill-produccion
```

## Reglas de oro ARES

1. **Tres funciones máximo**: Si necesitas más, el módulo es demasiado grande. Dividir.
2. **Calidad desde inicio**: No "terminaré después". Pruebas y validación ahora.
3. **Comentarios estratégicos**: Solo donde hubo dolor, no donde es obvio.
4. **Papelera sin vergüenza**: Mejor descartar rápido que mantener código roto.
5. **LEEME.md actualizado**: Si no está registrado ahí, el módulo no existe.

## Relación con otros skills

| Skill | Relación | Nota |
|-------|----------|------|
| inicializacion | Pre-requisito | Este skill requiere proyecto inicializado |
| mantenimiento | Alternativa | Si módulo existe, usar mantenimiento, no desarrollo |
| produccion | Siguiente paso | Cuando módulo esté validado, pasar a produccion |

**Independencia**: No carga otros skills. Solo lee archivos base (LEEME.md, REP_STRUCTURE.md).
```

---

### skill-mantenimiento

```markdown
# skill-mantenimiento

## Propósito
Gestionar código existente: adaptar a nuevos contextos, mover a papelera lo no funcional, actualizar documentación, mantener índice de módulos. Mantenimiento es evolución controlada, no solo reparación.

## Cuándo usar
- Usuario dice: "mantener", "adaptar", "a papelera", "actualiza módulo", "modifica"
- Módulo existe en LEEME.md pero requiere cambios
- Código en `papelera/` necesita revisión o recuperación
- Documentación desactualizada

## Entradas requeridas
- `nombre_modulo`: string (existente en proyecto)
- `accion`: "adaptar" | "papelera" | "recuperar" | "documentar" | "dividir"
- `contexto`: string (descripción del cambio requerido)

## Flujo de ejecución

1. **Localizar módulo**
   
   Buscar en orden:
   1. `src/modules/{nombre}/` → módulo normal
   2. `Agentes/{nombre}/` → agente
   3. `papelera/{nombre}_*/` → versión anterior descartada
   
   Si no encuentra: error "Módulo no existe. Usar skill-desarrollo para crear nuevo."

2. **Ejecutar acción específica**

   **Acción: "adaptar"**
   - Leer código actual
   - Identificar qué cambiar según `contexto`
   - Modificar manteniendo regla de 3 funciones
   - Si adaptación requiere >3 funciones: sugerir acción "dividir"
   - Actualizar docstring con nota de adaptación
   - Si es complejo: actualizar/crear `docs/{nombre}.md`
   - LEEME.md: `[ADAPTADO] {nombre}: {contexto breve}`

   **Acción: "papelera"**
   - Validar que no está ya en papelera
   - Mover directorio completo: `src/modules/{nombre}/` → `papelera/{nombre}_{fecha}/`
   - Crear `papelera/{nombre}_{fecha}/NOTA.md`:
     ```markdown
     # NOTA — Módulo {nombre} movido a papelera
     Fecha: {fecha}
     Razón: {contexto}
     Último estado conocido: [funcional|no funcional|parcial]
     Posible recuperación: [sí|no|requiere reescritura]
     ```
   - LEEME.md: `[PAPELERA] {nombre}: {contexto breve}`
   - Si había docs/{nombre}.md: mover a papelera también

   **Acción: "recuperar"**
   - Buscar en `papelera/{nombre}_*/` (más reciente si hay varios)
   - Leer NOTA.md para evaluar viabilidad
   - Si NOTA.md indica "no recuperable": abortar con explicación
   - Si recuperable: mover a `src/modules/{nombre}/` o `Agentes/{nombre}/`
   - Validar sintaxis y dependencias
   - LEEME.md: `[RECUPERADO] {nombre} desde papelera`
   - Sugerir skill-desarrollo para adaptaciones necesarias

   **Acción: "documentar"**
   - Crear/actualizar `docs/{nombre}.md` con:
     - Qué problema resuelve el módulo
     - Decisiones técnicas difíciles tomadas
     - Errores encontrados y cómo se evitaron
     - Cómo adaptar a otros contextos
     - Dependencias externas
   - Añadir comentario en código: `# Ver docs/{nombre}.md para detalles complejos`
   - LEEME.md: `[DOC] {nombre}: documentación especial creada`

   **Acción: "dividir"**
   - Analizar módulo: identificar funciones que pueden ser módulos independientes
   - Crear nuevos módulos hijos: `{nombre}_{subfuncion}/`
   - Modificar módulo original: convertir en orquestador que importa hijos
   - Validar que cada hijo cumple ≤3 funciones
   - Actualizar imports y dependencias
   - LEEME.md: `[DIVIDIDO] {nombre} → {nombre}_{sub1}, {nombre}_{sub2}...`

3. **Mantener índice de módulos**
   
   Actualizar automáticamente lista en LEEME.md o crear `docs/INDEX_MODULOS.md` si hay más de 10 módulos:
   ```markdown
   | Módulo | Tipo | Estado | Ubicación | Docs |
   |--------|------|--------|-----------|------|
   | {nombre} | lib/cli/hibrido/agente | [DEV|ADAPTADO|PAPELERA] | src/... | docs/... |
   ```

4. **Validación post-mantenimiento**
   
   - Si acción="adaptar" o "recuperar": validar sintaxis
   - Si acción="dividir": validar que imports funcionan
   - Confirmar LEEME.md refleja estado real

## Validaciones críticas

- [ ] Acción "papelera": verificar que módulo no está en uso por otros (grep imports)
- [ ] Acción "recuperar": leer NOTA.md primero, no recuperar lo marcado como "no recuperable"
- [ ] Acción "dividir": resultado debe ser módulos con ≤3 funciones cada uno
- [ ] Siempre actualizar LEEME.md (verdad funcional)

## Outputs

### JSON estructurado
```json
{
  "estado": "ok|error|parcial",
  "accion": "mantenimiento_{accion}",
  "datos": {
    "nombre": "{nombre}",
    "accion_ejecutada": "{adaptar|papelera|recuperar|documentar|dividir}",
    "ruta_origen": "...",
    "ruta_destino": "...",
    "notas": "{contexto de la acción}"
  }
}
```

### Output CLI
```
🔧 Módulo '{nombre}': acción '{accion}' completada
   Estado previo: [DEV] → Estado actual: [ADAPTADO|PAPELERA|RECUPERADO]
   LEEME.md actualizado
```

## Reglas de oro ARES

1. **Papelera es temporal pero documentada**: Siempre NOTA.md explicando por qué.
2. **Recuperación consciente**: Leer NOTA.md antes de recuperar, no automático.
3. **División preferida a complejidad**: Mejor 3 módulos simples que 1 complejo.
4. **Documentar lo problemático**: Si costó resolver, que no se pierda el conocimiento.
5. **Índice actualizado**: Mapa claro de qué existe y en qué estado.

## Relación con otros skills

| Skill | Relación | Nota |
|-------|----------|------|
| desarrollo | Origen del código | Mantenimiento opera sobre lo que desarrollo creó |
| produccion | Destino posible | Después de mantener/adaptar, puede ir a produccion |
| inicializacion | No aplica | Mantenimiento requiere código existente |

**Independencia**: Opera sobre estructura existente, no carga otros skills.
```

---

### skill-produccion

```markdown
# skill-produccion

## Propósito
Globalizar scripts funcionales en el sistema operativo via TRON `ini`. Producción es hacer disponible globalmente lo que está validado, bajo decisión soberana del usuario.

## Cuándo usar
- Usuario dice: "producir", "globalizar", "a /usr/bin", "lanzar", "poner en producción"
- Módulo existe en LEEME.md con estado [DEV] o [ADAPTADO]
- Usuario decide soberanamente que está listo (IA no decide)

## Entradas requeridas
- `nombre_modulo`: string (existente y funcional)
- `metodo`: "auto" | "manual" (default="auto")
- `confirmar`: bool (default=false, requiere explícito true para ejecutar)

## Flujo de ejecución

1. **Verificación pre-producción (calidad de salida)**
   
   Leer LEEME.md:
   - ¿Estado es [DEV] o [ADAPTADO]? Si [PAPELERA] o no existe: abortar.
   - ¿Tiene documentación de complejidad si aplica?
   
   Verificar módulo:
   - Sintaxis válida: `python -m py_compile`
   - Permisos ejecutables: `chmod +x` aplicado
   - Shebang presente: `#!/usr/bin/env python3` (o según lenguaje)
   - Ayuda interna funciona: `--help` o `-h` (para CLI/hibrido/agente)
   
   Si alguna falla: abortar con lista de qué corregir. Sugerir skill-desarrollo o skill-mantenimiento.

2. **Determinar método de globalización**

   **Método "auto" (preferido):**
   - Requisito: estar en directorio del proyecto con estructura detectable
   - Ejecutar: `ini` (sin argumentos, modo automático)
   - `ini` detecta proyecto, crea wrapper en `/usr/bin/`
   
   **Método "manual":**
   - Usar cuando `ini` no detecta automáticamente
   - Ejecutar: `ini -i` (modo interactivo)
   - Seguir prompts de `ini` para especificar ruta y nombre

3. **Validar instalación via TRON `com`**
   
   - Ejecutar: `com ruta {nombre_modulo}`
   - Verificar que apunta a wrapper en `/usr/bin/` y no a código fuente
   - Ejecutar: `com codigo {nombre_modulo}` (verificar wrapper correcto)
   - Probar ejecución: `{nombre_modulo} --help` (debe funcionar)

4. **Actualizar LEEME.md (verdad funcional)**
   
   ```
   [PROD] {nombre_modulo}: Globalizado via ini ({metodo})
   Ruta sistema: /usr/bin/{nombre_modulo}
   Wrapper apunta a: {ruta_real}
   Fecha producción: {fecha}
   ```
   
   Mover de sección "Módulos en Desarrollo" a "Funcionalidades Operativas"

5. **Confirmación final**
   
   Mostrar al usuario:
   - Wrapper creado y su contenido (via `com codigo`)
   - Cómo usar: `{nombre_modulo} [argumentos]`
   - Cómo modificar: nunca editar `/usr/bin/`, editar fuente en `src/` y re-ejecutar `ini`

## Validaciones críticas

- [ ] `confirmar=true` explícito (la IA no produce sin orden clara)
- [ ] Estado previo [DEV] o [ADAPTADO] (no [PAPELERA], no inexistente)
- [ ] Sintaxis válida, permisos +x, shebang correcto
- [ ] Post-instalación: `com ruta` y ejecución `--help` funcionan
- [ ] LEEME.md actualizado con ruta real y fecha

## Manejo de errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ini` no detecta proyecto | Falta estructura reconocible | Usar `ini -i` manual o verificar estructura |
| Wrapper no ejecuta | Permisos o shebang | `chmod +x`, verificar shebang |
| `com ruta` no encuentra | No instalado o nombre diferente | Verificar nombre usado en `ini` |
| Conflicto nombre existente | Otro programa usa mismo nombre | Renombrar módulo o usar `ini -i` con nombre alternativo |

## Outputs

### JSON estructurado
```json
{
  "estado": "ok|error|pendiente_confirmacion",
  "accion": "produccion_globalizar",
  "datos": {
    "nombre": "{nombre}",
    "metodo": "auto|manual",
    "ruta_wrapper": "/usr/bin/{nombre}",
    "ruta_fuente": "{ruta_real}",
    "validacion_com": "ok|fallo",
    "estado_leeme": "[PROD]"
  }
}
```

### Output CLI
```
🚀 Módulo '{nombre}' globalizado en /usr/bin/{nombre}
   Método: {auto|manual} | Validación: OK
   Uso: {nombre} [argumentos]
   Modificar: editar src/modules/{nombre}/ → re-ejecutar ini
   LEEME.md: [PROD] registrado
```

## Reglas de oro ARES

1. **Soberanía del usuario**: IA nunca decide poner en producción. Requiere confirmar=true.
2. **Fuente en ~/tron/programas**: Nunca editar `/usr/bin/` directamente. Wrapper apunta a fuente.
3. **Validación obligatoria**: Si `com ruta` o `--help` fallan, no está en producción real.
4. **LEEME.md es la verdad**: Sin entrada [PROD], el módulo no existe funcionalmente para el sistema.
5. **Reproducible**: Re-ejecutar `ini` debe actualizar wrapper si fuente cambió.

## Relación con otros skills

| Skill | Relación | Nota |
|-------|----------|------|
| desarrollo | Origen | Solo se produce lo que desarrollo creó y validó |
| mantenimiento | Preparación | Puede requerir adaptación antes de producción |
| inicializacion | No aplica | Producción requiere código funcional, no estructura vacía |

**Dependencia externa**: Requiere TRON `ini` y `com` instalados. Si no: error "Herramientas TRON no disponibles. Instalar primero."

**Independencia de otros skills**: No carga skill-desarrollo ni skill-mantenimiento, solo valida su output (código existente).
```

---

## Iteración 4: Verificación contra tus requisitos

| Tu requisito | Verificación |
|-------------|--------------|
| "inicializacion ese OK" | ✓ Skill 1: inicializacion |
| "desarrollo y calidad van en el mismo skill" | ✓ Skill 2: desarrollo (con calidad integrada: depuración desde inicio, validación, papelera si falla) |
| "gestion cambialo a mantenimiento" | ✓ Skill 3: mantenimiento (adaptar, papelera, recuperar, documentar, dividir) |
| "deplay con su skill pero no se llama deploy se llama produccion" | ✓ Skill 4: produccion (usa "globalizar", "/usr/bin", "ini") |
| "no nombres raros como Bootstrap" | ✓ Nombres: inicializacion, desarrollo, mantenimiento, produccion |
| "respecta mi forma de decir las cosas" | ✓ "globalizar", "papelera", "paranoica", "soberanía", "verdad funcional" |
| "carga manual, no tres skills a la vez" | ✓ Cada skill es autocontenido, independiente, carga individual |
| "flujo de trabajo de bajo tokens" | ✓ Skills no se cargan entre sí, solo leen archivos base (LEEME.md, REP_STRUCTURE.md) |
| "usa mis palabras de la documentación" | ✓ "Organización paranoica", "Cerebro Headless", "soberanía tecnológica", "LEEME.md es verdad" |

---

## Resumen entregable

4 skills listos para copiar a `docs/skills/`:

1. **skill-inicializacion.md**
2. **skill-desarrollo.md**
3. **skill-mantenimiento.md**
4. **skill-produccion.md**

---

## Verificación final de convergencia

| Criterio | Estado |
|----------|--------|
| Tus palabras exactas | ✓ "inicializacion", "desarrollo", "mantenimiento", "produccion", "globalizar", "papelera", "paranoica", "soberanía", "verdad funcional" |
| Principios ARES | ✓ ≤3 funciones, LEEME.md verdad, docs/ para complejo, comentarios solo lo complejo, num_ctx 8192, RAM <1GB |
| Herramientas TRON | ✓ ini, com (repo y ayuda son consumo, no skills) |
| Carga manual | ✓ Skills independientes, ninguno carga otro |
| Sin ruido | ✓ Sin Bootstrap, sin meta, sin coordinar multi-skill |
| Bajo tokens | ✓ Cada skill lee máximo 2 archivos base + objetivo |

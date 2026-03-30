Basado en el código fuente proporcionado (el orquestador `ini v3.0`), he realizado una ingeniería inversa para extraer las normativas, procedimientos, estándares y filosofía de desarrollo que rigen en tu entorno (denominado **Ecosistema TRON**). 

A continuación, te presento la **Sistematización y Manual de Procedimientos** que dio lugar a este software, redactado como un documento normativo interno de la empresa/organización:

---

# 📘 MANUAL DE ESTÁNDARES Y CICLO DE VIDA DE SOFTWARE (ECOSISTEMA TRON)
**Versión de la normativa:** 3.0
**Ámbito:** Desarrollo, Gestión de Entornos y Despliegue a Producción.

## 1. FILOSOFÍA Y PRINCIPIOS ARQUITECTÓNICOS
Todo el software desarrollado bajo el Ecosistema TRON debe adherirse a los siguientes principios:
1. **Soberanía del Directorio de Trabajo (CWD Sovereignty):** Los binarios en producción no deben hacer un `cd` global que altere la ruta del usuario. Deben ejecutarse referenciando su ruta de origen mediante la variable inyectada `TR_PROJECT_ROOT`.
2. **Aislamiento por Proyecto:** Cada proyecto es una isla. Tiene sus propias dependencias y sus propias variables de entorno, independientes del sistema global.
3. **Automatización First (Headless):** Todos los procesos de ciclo de vida deben poder ejecutarse sin intervención humana (mediante el flag `-y`) para permitir su integración con IAs y pipelines automatizados.
4. **Preferencia de Herramientas Modernas:** Se abandona `pip`/`venv` tradicional en favor de **`uv`** para Python, buscando máxima velocidad.

---

## 2. CREACIÓN E INICIALIZACIÓN DE PROYECTOS
Cuando un desarrollador o IA inicia un nuevo proyecto, debe seguir este flujo:

### 2.1. Proyectos Python (Estándar Principal)
* **Comando de inicio:** `ini init`
* **Gestor de paquetes:** Es obligatorio el uso de `pyproject.toml`.
* **Versión mínima:** Python >= 3.12.
* **Nomenclatura:** El nombre del proyecto debe derivar del nombre de la carpeta, convertido a *kebab-case* (minúsculas y guiones).
* **Estructura de archivos:** El código fuente debe residir preferiblemente en la raíz, en una carpeta `src/`, o en `modules/`. Los archivos que comiencen con guion bajo (`_*.py`) se consideran privados y no son elegibles como punto de entrada principal.
* **Puntos de entrada prioritarios:** El sistema buscará por defecto archivos nombrados: `main.py`, `app.py`, `cli.py`, `__main__.py`, `tron.py` o `ares.py`.

### 2.2. Proyectos Node.js
* Deben inicializarse con un `package.json` estándar.
* El punto de entrada por defecto será `main.js`.

---

## 3. GESTIÓN DE ENTORNOS DE DESARROLLO
Antes de escribir código, el entorno debe estar sincronizado.
* **Comando:** `ini venv`
* **Para Python:** Es **obligatorio** tener instalado `uv` en el sistema. El comando creará la carpeta `.venv` y sincronizará las dependencias usando `uv sync`.
* **Para Node.js:** Se utilizará `npm install` estándar, generando la carpeta `node_modules`.

---

## 4. GESTIÓN DE VARIABLES DE ENTORNO Y ESTADO
Queda estrictamente prohibido el uso de archivos `.env` tradicionales. El estándar del Ecosistema TRON es el archivo **`.tron.env.json`**.

* **Comando:** `ini env`
* **Estructura obligatoria:**
  * `project_name`: Nombre del proyecto.
  * `command_name`: Nombre del comando que se expondrá en producción.
  * `variables`: Diccionario de variables clave-valor inyectables.
  * `generic_counters`: Sistema nativo para llevar conteos persistentes (ej. `counter_001`, `counter_002`).
* **Inyección:** Estas variables no se cargan en el código fuente mediante librerías (como `python-dotenv`), sino que **el orquestador las inyecta directamente en Bash** antes de ejecutar el script.

---

## 5. DESPLIEGUE Y PASO A PRODUCCIÓN
El paso a producción consiste en convertir un script local en un comando global del sistema operativo Linux.
* **Comando:** `ini prod`

### 5.1. Normativas de Nombrado de Comandos
1. El nombre del comando global será por defecto el nombre de la carpeta.
2. **Regla de Excepción "Ares":** Si la carpeta o proyecto se llama `tr`, el comando en producción se renombrará obligatoriamente a **`ares`**.
3. **Prevención de Colisiones:** Antes de publicar, el sistema verifica `/usr/bin/`. Si el nombre elegido ya existe y es un comando nativo del sistema operativo (ej. `ls`, `cat`), se denegará la publicación y se sugerirá el prefijo `tron-` (ej. `tron-ls`).

### 5.2. Estrategia de Wrappers (Envoltorios)
No se copian los archivos fuente a `/usr/bin`. En su lugar, se generan *Wrappers* en Bash.
Se generan dos wrappers:
1. **Lanzador Local (Portátil):** Se crea en la carpeta `bin/` del proyecto. Permite ejecutar el proyecto empaquetado sin instalarlo globalmente.
2. **Lanzador Global:** Se instala en `/usr/bin/<nombre_comando>` usando privilegios de `sudo`.

### 5.3. Motores de Ejecución (Execution Engines)
El wrapper global ejecutará el código fuente dependiendo de la tecnología detectada, aplicando reglas estrictas de aislamiento:

* **Para Python:** 
  Se debe usar la siguiente instrucción exacta:
  `exec env -u VIRTUAL_ENV uv run --project "$TR_PROJECT_ROOT" python "$TR_PROJECT_ROOT/<target>" "$@"`
  *(Nota técnica: Se destruye la variable `VIRTUAL_ENV` del usuario actual para evitar que el script use el entorno virtual equivocado, delegando la resolución del entorno a `uv run` apuntando a la raíz del proyecto).*
* **Para Node.js:**
  `exec node "$TR_PROJECT_ROOT/<target>" "$@"`
* **Para Bash/Scripts directos:**
  `exec "$TR_PROJECT_ROOT/<target>" "$@"`

### 5.4. Integración con el Entorno de Escritorio
* Si el sistema operativo cuenta con el comando `menu` (gestor de menús de Openbox), el orquestador ofrecerá automáticamente registrar el nuevo binario en la interfaz gráfica del usuario.

---

## 6. HERRAMIENTAS DEL SISTEMA REQUERIDAS
Para que una estación de trabajo sea compatible con el Ecosistema TRON, debe contar con:
1. `uv` (Gestor ultrarrápido de Python de Astral).
2. `npm` / `node` (Para ecosistema JS).
3. `micro` (Editor de texto en terminal por defecto; `nano` como fallback).
4. `sudo` configurado para permitir la escritura en `/usr/bin/`.
5. Entorno Linux/Unix compatible con Bash.

---
### ANEXO: POLÍTICA DE NO INTERVENCIÓN EN PERFILES DE USUARIO Y PATH

**1. Prohibición de alteración de dotfiles:**
El Ecosistema TRON establece como norma arquitectónica estricta la no modificación de los archivos de configuración del shell del usuario. Bajo ninguna circunstancia el orquestador o los procesos de despliegue deben tocar, editar o inyectar código en archivos como `~/.bashrc`, `~/.zshrc`, `~/.profile` o similares.

**2. Inmutabilidad de la variable PATH:**
Queda terminantemente prohibida la práctica de "contaminar" la variable global `$PATH` añadiendo rutas personalizadas de los directorios locales de cada proyecto (ej. `export PATH=$PATH:/ruta/al/proyecto/bin`). El `$PATH` del sistema operativo debe mantenerse intacto, limpio y en su estado original.

**3. Mecanismo de disponibilidad global (Resolución Arquitectónica):**
Para lograr que los comandos de los proyectos estén disponibles globalmente en la terminal sin alterar el `PATH` ni los perfiles de usuario, la normativa dicta el siguiente procedimiento:
* Todo binario que pasa a producción se materializa como un *script wrapper* (envoltorio Bash) independiente.
* Este wrapper se instala e inyecta directamente en el directorio de binarios estándar del sistema operativo: `/usr/bin/` (mediante privilegios `sudo`).
* Al residir nativamente en `/usr/bin/` (una ruta que ya está incluida por defecto en el `PATH` base de cualquier sistema Linux/Unix), el comando es reconocido de forma inmediata por cualquier intérprete de comandos (Bash, Zsh, Fish, etc.) y por cualquier usuario del sistema, eliminando por completo la necesidad de reiniciar la terminal o ejecutar comandos como `source ~/.bashrc`.

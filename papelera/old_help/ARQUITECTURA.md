# 🗃️ Arquitectura Memgraph — Guía Completa para Programadores

> **Documento maestro de referencia.** Cualquier programador puede leer esto y entender qué es Memgraph, dónde está todo, cómo se conecta, enciende, apaga y configura.

---

## 1. ¿Qué es Memgraph?

**Memgraph** es una **base de datos de grafos nativa en memoria** (in-memory graph database), compatible con **Cypher** (el mismo lenguaje de consultas de Neo4j). Está escrita en **C++** y diseñada para velocidad extrema: las consultas se ejecutan en microsegundos porque los datos viven en RAM.

### Tipo de base de datos

| Propiedad | Valor |
|-----------|-------|
| **Tipo** | Grafo nativo en memoria (in-memory graph DB) |
| **Modelo** | Propiedades (nodos + relaciones con propiedades clave-valor) |
| **Lenguaje de consultas** | **Cypher** (openCypher) — `MATCH (n)-[r]->(m) RETURN n, r, m` |
| **Protocolo** | **Bolt** (binario, puerto 7687) — el mismo que Neo4j |
| **Motor** | C++ compilado, single-threaded por defecto, con paralelismo opcional |
| **Persistencia** | Snapshots (WAL) + archivos en disco configurables |
| **Compatibilidad** | Drop-in replacement para Neo4j (mismo protocolo Bolt + Cypher) |

### ¿Para qué sirve un grafo?

Un grafo modela **entidades** (nodos) y **conexiones** (relaciones/aristas) entre ellas. Casos de uso:
- Redes sociales (personas → amistad → personas)
- Sistemas de recomendación (usuario → compró → producto → categoría)
- Detección de fraude (cuentas → transacciones → IPs → dispositivos)
- Knowledge graphs (conceptos → relacionados_con → conceptos)
- Dependencias de software (módulo → importa → módulo)

---

## 2. Arquitectura Instalada — Lo que corre en Docker

Se instalaron **2 imágenes Docker** que forman una plataforma completa:

### 2.1. Imagen: `memgraph/memgraph-mage` (3.2 GB)

**Nombre del contenedor:** `memgraph-mage`
**Rol:** Motor de base de datos + MAGE (Memgraph Advanced Graph Extensions)

**¿Qué es MAGE?**
MAGE es un paquete de **módulos de consulta avanzados** (query modules) que amplían Cypher con algoritmos de grafos profesionales: PageRank, Betweenness Centrality,社区检测 (community detection), pathfinding (Dijkstra, A*), k-NN, etc.

| Propiedad | Detalle |
|-----------|---------|
| **Base OS** | Ubuntu 24.04 |
| **Memgraph** | v3.9.0-rc3 |
| **Python** | 3.12 (para módulos MAGE) |
| **User** | `memgraph` |
| **Entrypoint** | `/usr/lib/memgraph/memgraph` |
| **Puerto interno expuesto** | 7687/tcp (Bolt) |

**Puertos mapeados al host:**

| Puerto Host | Puerto Contenedor | Servicio | Descripción |
|-------------|-------------------|----------|-------------|
| **7687** | 7687 | **Bolt** | Protocolo binario para consultas Cypher (clientes, drivers, aplicaciones) |
| **7444** | 7444 | **HTTP/HTTPS** | API HTTP para monitoreo, métricas, y conexiones alternativas |

**Argumentos de arranque (command):**
```yaml
command: ["--log-level=TRACE"]
```
Esto establece el nivel de log en TRACE (máxima verbosidad). Otros flags útiles de Memgraph:

| Flag | Descripción | Default |
|------|-------------|---------|
| `--log-level=TRACE\|DEBUG\|INFO\|WARNING\|ERROR` | Nivel de verbosidad de logs | INFO |
| `--telemetry-enabled=false` | Desactivar telemetría | true |
| `--storage-snapshot-interval-sec=0` | Desactivar snapshots automáticos | 180 |
| `--storage-wal-enabled=false` | Desactivar Write-Ahead Log | true |
| `--storage-recover-on-startup=true` | Recuperar datos desde WAL al iniciar | false |
| `--memory-limit` | Límite de memoria en MB | 0 (sin límite) |

**Volumen/Persistencia:**
Actualmente **no hay volúmenes montados**. Los datos se almacenan dentro del contenedor en `/var/lib/memgraph/`. Si el contenedor se elimina (`docker rm`), **los datos se pierden**. Para persistencia, se debe agregar un volumen:

```yaml
volumes:
  - mg_data:/var/lib/memgraph
```

**Directorios internos clave del contenedor:**

| Ruta interna | Contenido |
|--------------|-----------|
| `/usr/lib/memgraph/memgraph` | Binario principal del servidor |
| `/usr/lib/memgraph/query_modules/` | Módulos MAGE compilados (.so) + Python |
| `/var/lib/memgraph/` | Datos, snapshots, WAL, configuración |
| `/var/lib/memgraph/settings/` | Almacén key-value para settings |
| `/etc/memgraph/` | Archivos de configuración (si existen) |

---

### 2.2. Imagen: `memgraph/lab` (335 MB)

**Nombre del contenedor:** `memgraph-lab`
**Rol:** Interfaz web (UI) para explorar datos, escribir consultas Cypher y visualizar grafos.

| Propiedad | Detalle |
|-----------|---------|
| **Base OS** | Ubuntu 24.04 |
| **Runtime** | Node.js 22.22.1 |
| **User** | `lab` |
| **Working Dir** | `/home/lab` |
| **Entrypoint** | `docker-entrypoint.sh` |
| **Cmd** | `node dist-backend/index.js` |

**Puerto mapeado al host:**

| Puerto Host | Puerto Contenedor | Servicio | Descripción |
|-------------|-------------------|----------|-------------|
| **3000** | 3000 | **HTTP** | Interfaz web Memgraph Lab |

**Variables de entorno:**

| Variable | Valor | Función |
|----------|-------|---------|
| `QUICK_CONNECT_MG_HOST` | `memgraph` | Host del servicio Memgraph (nombre Docker del contenedor) |
| `QUICK_CONNECT_MG_PORT` | `7687` | Puerto Bolt del servicio Memgraph |

**Qué hace Memgraph Lab:**
- Editor de consultas Cypher con autocompletado
- Visualización interactiva de grafos (nodos y relaciones arrastrables)
- Exploración de esquemas (qué tipos de nodos/relaciones existen)
- Importación de datos (CSV, JSON)
- Dashboard de métricas

---

## 3. Topología de Red — Cómo se conectan entre sí

```
┌─────────────────────────────────────────────────────────┐
│                      HOST (tu máquina)                  │
│                                                         │
│  ┌──────────────────────────┐                           │
│  │  docker-compose.yml      │                           │
│  │  (TR/db/memgraph-        │                           │
│  │   platform/)             │                           │
│  │                          │                           │
│  │  red: memgraph-platform_default (bridge)             │
│  │                          │                           │
│  │  ┌────────────────────┐  │  ┌────────────────────┐  │
│  │  │  memgraph-mage     │  │  │  memgraph-lab      │  │
│  │  │  (DB + MAGE)       │  │  │  (UI Web)          │  │
│  │  │                    │  │  │                    │  │
│  │  │  :7687  Bolt ◄─────┼──┼──► conecta vía Bolt   │  │
│  │  │  :7444  HTTP       │  │  │  :3000  HTTP       │  │
│  │  └─────────┬──────────┘  │  └─────────┬──────────┘  │
│  └────────────┼─────────────┘  └─────────┼─────────────┘
│               │                          │
│         Puertos host               Puertos host
│         7687, 7444                 3000
│               │                          │
└───────────────┼──────────────────────────┼───────────────┘
                │                          │
          Tu código Python/         Tu navegador
          aplicaciones              http://localhost:3000
          bolt://localhost:7687
```

**Red Docker:** `memgraph-platform_default` (tipo `bridge`)
- Los contenedores se resuelven por **nombre de servicio**: `memgraph-lab` conecta a `memgraph` por hostname interno
- Desde el **host**, accedes por `localhost:<puerto>`

---

## 4. Archivos Clave — Dónde está cada cosa

| Archivo / Directorio | Ruta | Qué contiene |
|----------------------|------|--------------|
| **docker-compose.yml** | `TR/db/memgraph-platform/docker-compose.yml` | Definición de servicios, puertos, variables |
| **Módulo gestor** | `TR/modules/admon/memgraph_manager.py` | 3 funciones: start, stop, status |
| **Comando CLI** | `TR/src/main.py` (líneas ~1020-1070) | Registro de `ares mem start/stop/status` |
| **Este documento** | `TR/docs/MEMGRAPH/ARQUITECTURA.md` | Arquitectura completa (este archivo) |
| **Binario Memgraph** | Dentro del contenedor: `/usr/lib/memgraph/memgraph` | Servidor C++ |
| **Módulos MAGE** | Dentro del contenedor: `/usr/lib/memgraph/query_modules/` | Algoritmos de grafos |
| **Datos (efímeros)** | Dentro del contenedor: `/var/lib/memgraph/` | Snapshots, WAL, settings |

---

## 5. Conexiones — Cómo usar Memgraph desde tu código

### 5.1. Desde Python (driver neo4j)

```bash
pip install neo4j
```

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687")
with driver.session() as session:
    # Crear nodos
    session.run("CREATE (a:Persona {nombre: 'Daniel'})")
    session.run("CREATE (b:Persona {nombre: 'Ana'})")
    session.run("MATCH (a:Persona {nombre: 'Daniel'}), (b:Persona {nombre: 'Ana'}) CREATE (a)-[r:CONOCE]->(b)")

    # Consultar
    result = session.run("MATCH (a)-[r]->(b) RETURN a.nombre, type(r), b.nombre")
    for record in result:
        print(f"{record['a.nombre']} -{record['type(r)']}> {record['b.nombre']}")
driver.close()
```

### 5.2. Desde Python (driver oficial gqlalchemy)

```bash
pip install gqlalchemy
```

```python
from gqlalchemy import Memgraph

db = Memgraph(host="localhost", port=7687)
db.execute("CREATE (n:Persona {nombre: 'Daniel'})")
result = list(db.execute("MATCH (n) RETURN n"))
print(result)
```

### 5.3. Desde Memgraph Lab (UI web)

1. Abre `http://localhost:3000`
2. Click en **"Connect"** (ya está preconfigurado a `memgraph:7687`)
3. Escribe Cypher en el editor y ejecuta con **Ctrl+Enter**

### 5.4. Desde la línea de comandos (mgconsole)

Dentro del contenedor:
```bash
docker exec -it memgraph-mage mgconsole --host localhost --port 7687
```

---

## 6. Comandos de Gestión — Encender / Apagar / Verificar

### Vía ARES (recomendado)

```bash
ares mem start    # Inicia Docker daemon (si no corre) + contenedores
ares mem stop     # Detiene contenedores (Docker daemon sigue activo)
ares mem status   # Muestra estado de Docker + contenedores + puertos
ares mem          # Equivale a 'ares mem status'
```

### Vía Docker (manual)

```bash
# Iniciar
cd /home/daniel/tron/programas/TR/db/memgraph-platform
docker compose up -d

# Detener
docker compose down

# Ver estado
docker ps --filter name=memgraph

# Ver logs
docker logs memgraph-mage
docker logs memgraph-lab

# Reiniciar
docker compose restart

# Eliminar contenedores + datos (¡cuidado!)
docker compose down -v
```

### Flujo de arranque interno (lo que hace `ares mem start`):

```
1. ¿Docker daemon corriendo?
   ├─ NO  → sudo systemctl start docker (espera 10s)
   └─ SÍ  → continua

2. ¿Contenedores ya corriendo?
   ├─ SÍ  → retorna mensaje "ya corriendo"
   └─ NO  → continua

3. docker compose up -d
   ├─ Descarga imágenes si no existen (pull_policy: always)
   ├─ Crea red bridge: memgraph-platform_default
   ├─ Inicia memgraph-mage (DB)
   └─ Inicia memgraph-lab (UI, depende de memgraph)

4. Espera 3 segundos

5. Verifica que ambos contenedores estén "Up"

6. Retorna URLs:
   - Bolt: localhost:7687
   - HTTP: localhost:7444
   - Lab UI: http://localhost:3000
```

---

## 7. Tipos de Bases de Datos en el Ecosistema Memgraph

| Tipo | Nombre | Uso |
|------|--------|-----|
| **Memgraph DB** | `memgraph/memgraph-mage` | Base de datos de grafos en memoria + algoritmos MAGE |
| **Memgraph Lab** | `memgraph/lab` | UI web (NO es base de datos, es cliente visual) |
| **Memgraph Platform** | DB + Lab + MAGE | Combinación completa (lo que tenemos instalado) |

**Nota:** Memgraph también ofrece:
- `memgraph/memgraph` — Solo la DB, sin MAGE
- `memgraph/memgraph-mage` — DB + MAGE (lo que usamos)
- `memgraph/lab` — UI web (lo que usamos)

---

## 8. Límites y Consideraciones Técnicas

| Aspecto | Detalle |
|---------|---------|
| **RAM** | Los datos viven en RAM. Un grafo de 1GB necesita ~1GB+ libre |
| **Persistencia** | Sin volúmenes montados, los datos se pierden al eliminar el contenedor |
| **Puertos** | 7687 (Bolt), 7444 (HTTP), 3000 (Lab) — no deben estar en uso |
| **Docker** | Requiere Docker + Docker Compose instalados y corriendo |
| **Contraseña** | Memgraph viene **sin autenticación** por defecto (cualquiera con acceso al puerto puede conectar) |
| **Escalabilidad** | Diseñado para datos que caben en RAM. Para grafos masivos, usar Neo4j en disco |

### Para agregar persistencia (futuro):

Modificar `docker-compose.yml`:
```yaml
services:
  memgraph:
    image: memgraph/memgraph-mage:latest
    container_name: memgraph-mage
    ports:
      - "7687:7687"
      - "7444:7444"
    volumes:
      - mg_data:/var/lib/memgraph
    command: ["--log-level=INFO", "--storage-snapshot-interval-sec=300"]

volumes:
  mg_data:
    driver: local
```

---

## 9. Algoritmos MAGE Disponibles (query modules)

Dentro del contenedor `memgraph-mage`, los módulos MAGE están en `/usr/lib/memgraph/query_modules/`. Los principales:

| Módulo | Algoritmo | Uso |
|--------|-----------|-----|
| `pagerank` | PageRank | Importancia de nodos en red |
| `betweenness_centrality` | Betweenness | Nodos puente/cuello de botella |
| `cycles` | Detección de ciclos | Encontrar ciclos en grafos |
| `katz_centrality` | Katz Centrality | Influencia de nodos |
| `graph_analyzer` | Estadísticas | Contar nodos, relaciones, componentes |
| `node2vec` | Node2Vec | Embeddings de nodos para ML |
| `meta_util` | Meta utilidades | Listar módulos disponibles |

Para ver todos desde Cypher:
```cypher
CALL mg.get_procedures() YIELD name, signature RETURN name, signature;
```

---

## 10. Resumen Rápido para Programador

```
┌─ QUÉ ES ──────────────────────────────────────────────┐
│  Memgraph = Base de datos de grafos en memoria        │
│  Compatible con Neo4j (mismo protocolo Bolt + Cypher)  │
│  Ultra-rápida: todo en RAM                            │
└───────────────────────────────────────────────────────┘

┌─ DÓNDE ESTÁ ──────────────────────────────────────────┐
│  Docker Compose: TR/db/memgraph-platform/             │
│  Módulo gestor:  TR/modules/admon/memgraph_manager.py │
│  Comando:        ares mem start/stop/status            │
└───────────────────────────────────────────────────────┘

┌─ PUERTOS ─────────────────────────────────────────────┐
│  7687 → Bolt (consultas Cypher desde código)          │
│  7444 → HTTP (API/métricas)                           │
│  3000 → Memgraph Lab (UI web en navegador)             │
└───────────────────────────────────────────────────────┘

┌─ CONECTAR ────────────────────────────────────────────┐
│  Python:  neo4j driver → bolt://localhost:7687        │
│  Python:  gqlalchemy → Memgraph(host="localhost")     │
│  Web:     http://localhost:3000                        │
└───────────────────────────────────────────────────────┘

┌─ ENCENDER / APAGAR ───────────────────────────────────┐
│  ares mem start    → Docker daemon + contenedores      │
│  ares mem stop     → Solo contenedores                 │
│  ares mem status   → Estado completo                   │
└───────────────────────────────────────────────────────┘
```

---

*Documento creado: 2026-04-11 | Memgraph v3.9.0-rc3 | MAGE latest | Lab v3.9.0*

# Memgraph RAM Fórmula Dimensionamiento Empresas Ontologías Grafos Venezuela Clientes Escalabilidad

> **Documento adicional de referencia.** No modifica ningún documento existente.  
> **Objetivo:** Que cualquier programador (incluso sin experiencia en grafos) pueda calcular cuánta RAM necesita Memgraph para una empresa real en Venezuela, cuándo migrar a otra base de datos, y cómo funciona todo el stack.

---

## 1. ¿Qué es Memgraph? (Explicación a prueba de tontos)

**Memgraph** es una **base de datos de grafos que vive en RAM**. Eso significa que es rapidísima (microsegundos por consulta) pero limitada por la memoria disponible en tu máquina.

**No es Neo4j.** Es su competidor directo. Hablan el **mismo idioma** (protocolo Bolt + lenguaje Cypher), así que cualquier código que funcione con Neo4j funciona con Memgraph cambiando solo la URL de conexión.

**No es Kùzu.** Kùzu es una librería embebida (ligera, sin servidor). Memgraph es un servidor completo (más pesado, pero con UI visual incluida: Memgraph Lab).

### ¿Para qué sirve un grafo?

Modelas **cosas** (nodos) y **conexiones entre ellas** (relaciones). Ejemplo real de ontología RAG:

```
(Documento_42) -[MENCIONA_A]-> (Empresa_X)
(Empresa_X) -[TIENE_CLIENTE]-> (Cliente_Y)
(Cliente_Y) -[COMPRO]-> (Producto_Z)
```

Un LLM puede **crear** esta ontología automáticamente, tú la **revisas visualmente** en Memgraph Lab, y luego el LLM la **lee** para responder preguntas contextuales.

---

## 2. Arquitectura Instalada — Todo lo que corre en Docker

### 2.1. Contenedor: `memgraph-mage` (Motor de Base de Datos)

| Propiedad | Valor |
|-----------|-------|
| **Imagen** | `memgraph/memgraph-mage:latest` (3.2 GB) |
| **Versión** | Memgraph v3.9.0-rc3 sobre Ubuntu 24.04 |
| **Motor** | C++ compilado |
| **Python** | 3.12 (para módulos MAGE) |
| **Puertos** | **7687** (Bolt — consultas Cypher), **7444** (HTTP — métricas) |
| **RAM base (vacío)** | **~544 MB** |
| **Entrypoint** | `/usr/lib/memgraph/memgraph` |

**¿Qué es MAGE?**  
Algoritmos de grafos profesionales ya instalados: PageRank, centralidad, detección de comunidades, pathfinding (Dijkstra, A*), node2vec, etc. Se llaman desde Cypher con `CALL`.

### 2.2. Contenedor: `memgraph-lab` (Interfaz Web Visual)

| Propiedad | Valor |
|-----------|-------|
| **Imagen** | `memgraph/lab:latest` (335 MB) |
| **Runtime** | Node.js 22 |
| **Puerto** | **3000** (HTTP — abre en navegador) |
| **RAM base** | **~68 MB** |
| **Función** | Editor Cypher + visualización interactiva de grafos |

### 2.3. RAM total del stack (vacío, sin datos)

| Componente | RAM usada | % de 7.3 GB |
|---|---|---|
| memgraph-mage (DB) | 544 MB | 7.26% |
| memgraph-lab (UI) | 68 MB | 0.90% |
| **Total Docker** | **~612 MB** | **8.16%** |

Esto es lo que consumes **antes de meter un solo dato**.

---

## 3. Fórmula Oficial de Memgraph para Calcular RAM

Memgraph publica su fórmula exacta de consumo de memoria por elemento:

```
RAM_datos = (Nodos × 204 bytes) + (Relaciones × 154 bytes) + Propiedades
```

### Desglose por elemento

**Por nodo (vértice):** 204 bytes base
- Objeto base: 80B
- Delta (ACID): 56B
- SkipList + índice: ~68B overhead
- **+4B extra** por cada label adicional

**Por relación (arista):** 154 bytes base
- Objeto base: 32B
- Delta (ACID): 56B
- SkipList overhead: ~66B

**Por propiedad** (cada valor que agregas a un nodo o relación):

| Tipo | Tamaño | Ejemplo |
|------|--------|---------|
| **STRING** | 4B + 1B por carácter | `"Juan"` = 4B + 4B = 8B |
| **INT pequeño** | 3B | edad: 35 |
| **INT grande** | 10B | monto: 9999999999 |
| **FLOAT** | 6B (32-bit) o 10B (64-bit) | precio: 19.99 |
| **VECTOR (embedding)** | 8B × dimensiones | 768 dims = **6,144B (6KB)** |

### Ejemplo de cálculo real

Una ontología con 1,000 nodos, cada uno con 3 propiedades string promedio (20 chars), y 3,000 relaciones con 1 propiedad cada una:

```
Nodos:       1,000 × 204B          = 204,000B
Relaciones:  3,000 × 154B          = 462,000B
Prop nodos:  1,000 × 3 × 24B       = 72,000B
Prop rels:   3,000 × 1 × 8B        = 24,000B
─────────────────────────────────────────
TOTAL:                               762,000B ≈ 744 KB
```

Menos de 1 MB de datos. Irrelevante comparado con los 612 MB base.

---

## 4. Dimensionamiento por Tipo de Empresa Venezolana

### Escenario 1: Microempresa (1-10 empleados) — Consulta médica pequeña

| Concepto | Cantidad |
|----------|----------|
| Pacientes | 2,000 |
| Doctores | 30 |
| Citas | 15,000 |
| Historiales | 2,000 |
| **Total nodos** | **~17,000** |
| **Total relaciones** | **~35,000** |

```
RAM datos = 17,000 × 204 + 35,000 × 154 = 3.47MB + 5.39MB = 8.86 MB
RAM total = 612 MB (base) + 9 MB (datos) = ~621 MB
```

**Tu máquina de 7.3 GB: sobra espacio.**

---

### Escenario 2: Pequeña empresa (10-50 empleados) — Retail con inventario

| Concepto | Cantidad |
|----------|----------|
| Clientes | 10,000 |
| Productos | 3,000 |
| Categorías | 200 |
| Compras | 50,000 |
| Relaciones inventario | 15,000 |
| **Total nodos** | **~13,200** |
| **Total relaciones** | **~65,000** |

```
RAM datos = 13,200 × 204 + 65,000 × 154 = 2.69MB + 10.01MB = 12.7 MB
RAM total = 612 + 13 = ~625 MB
```

---

### Escenario 3: Mediana empresa (50-200 empleados) — Distribuidora B2B

| Concepto | Cantidad |
|----------|----------|
| Clientes empresas | 500 |
| Productos | 10,000 |
| Proveedores | 100 |
| Pedidos | 100,000 |
| Rutas de envío | 20,000 |
| **Total nodos** | **~106,000** |
| **Total relaciones** | **~220,000** |

```
RAM datos = 106,000 × 204 + 220,000 × 154 = 21.6MB + 33.9MB = 55.5 MB
RAM total = 612 + 56 = ~668 MB
```

---

### Escenario 4: RAG Gráfico de Ontologías (tu caso de uso principal)

| Concepto | Cantidad |
|----------|----------|
| Documentos ingeridos | 5,000 |
| Entidades extraídas (personas, orgs, conceptos) | 25,000 |
| Relaciones semánticas | 80,000 |
| Embeddings vectoriales (768 dims × 8B × 5,000 docs) | ~30 MB |
| **Total nodos** | **~30,000** |
| **Total relaciones** | **~105,000** |

```
RAM datos = 30,000 × 204 + 105,000 × 154 + 30MB (embeddings) = 6.1MB + 16.2MB + 30MB = 52.3 MB
RAM total = 612 + 52 = ~664 MB
```

---

### Escenario 5: Empresa grande (200+ empleados) — ERP completo

| Concepto | Cantidad |
|----------|----------|
| Empleados | 1,000 |
| Departamentos | 50 |
| Proyectos | 200 |
| Clientes | 20,000 |
| Transacciones/año | 500,000 |
| Productos/servicios | 5,000 |
| **Total nodos** | **~526,000** |
| **Total relaciones** | **~1,500,000** |

```
RAM datos = 526,000 × 204 + 1,500,000 × 154 = 107MB + 231MB = 338 MB
RAM total = 612 + 338 = ~950 MB (casi 1 GB)
```

**Todavía muy cómodo en tu máquina.**

---

## 5. Tabla Resumen — ¿Cuándo Migrar?

| Tipo empresa venezolana | Nodos | Relaciones | RAM datos | RAM total (Memgraph) | ¿Cabe en 7.3GB? |
|---|---|---|---|---|---|
| **Micro (1-10 emp)** | < 20K | < 40K | < 10 MB | ~622 MB | ✅ Sobrado |
| **Pequeña (10-50)** | < 50K | < 200K | < 41 MB | ~653 MB | ✅ Sobrado |
| **Mediana (50-200)** | < 500K | < 1.5M | < 338 MB | ~950 MB | ✅ Cómodo |
| **Grande (200+)** | < 2M | < 6M | < 1.3 GB | ~1.9 GB | ✅ Cabe |
| **Límite máquina** | ~6M | ~6M | ~2.1 GB | ~2.7 GB | ⚠️ Justo |
| **Migrar a otra DB** | > 10M | > 30M | > 4 GB | > 4.6 GB | ❌ Swap |

### Regla mnemotécnica para decidir:

> **Si la empresa tiene menos de 200 empleados y menos de 1 millón de transacciones → Memgraph sobra.**  
> **Si pasa de 5 millones de transacciones activas → empieza a pensar en Neo4j (disco) o escalar RAM.**

Para el mercado venezolano de pymes: **ningún cliente va a llegar ni cerca del límite.**

---

## 6. Memgraph vs Kùzu vs Neo4j — Cuál y Por Qué

| Criterio | Memgraph | Kùzu | Neo4j |
|----------|----------|------|-------|
| **Tipo** | Servidor en RAM | Librería embebida | Servidor en disco |
| **RAM base (vacío)** | 612 MB (Docker) | ~0 MB | ~1-2 GB |
| **UI visual incluida** | ✅ Memgraph Lab | ❌ No tiene | ✅ Neo4j Browser |
| **Compatible Neo4j** | ✅ Sí (Bolt + Cypher) | Parcial | Nativo |
| **Algoritmos grafos** | ✅ MAGE incluido | ❌ Externos | ✅ GDS |
| **Persistencia** | Snapshots (configurable) | Archivos en disco | ACID completo |
| **Ideal para** | RAG + ontologías + visualización | Apps embebidas sin servidor | Empresas grandes con grafos masivos |

### Para tu caso (RAG gráfico, ontologías LLM → revisión visual → LLM lee):

**Memgraph gana** porque Memgraph Lab te da la UI visual out-of-the-box. Con Kùzu tendrías que construir tu propio visualizador. Con Neo4j consumirías más RAM innecesariamente.

---

## 7. Persistencia — Cómo No Perder Datos

Por defecto, **los datos viven dentro del contenedor**. Si haces `docker compose down -v`, se borran todo.

### Para activar persistencia, modificar `docker-compose.yml`:

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

Esto crea un volumen Docker que sobrevive a `docker compose down`. Los datos se guardan en `/var/lib/docker/volumes/`.

---

## 8. Comandos de Gestión

```bash
ares mem start    # Inicia Docker daemon + contenedores Memgraph
ares mem stop     # Detiene contenedores (Docker daemon sigue activo)
ares mem status   # Estado completo con puertos y URLs
ares mem          # Equivale a 'ares mem status'
```

### URLs de acceso:

| Servicio | URL | Uso |
|---|---|---|
| Bolt | `bolt://localhost:7687` | Consultas Cypher desde código |
| HTTP | `http://localhost:7444` | API/métricas |
| Lab UI | `http://localhost:3000` | Visualización en navegador |

---

## 9. Algoritmos MAGE Disponibles

| Módulo | Qué hace | Ejemplo de uso |
|--------|----------|----------------|
| `pagerank` | Importancia de nodos | ¿Qué cliente es más influyente? |
| `betweenness_centrality` | Nodos puente | ¿Qué producto conecta más categorías? |
| `cycles` | Detecta ciclos | ¿Hay rutas circulares en la ontología? |
| `katz_centrality` | Influencia | ¿Qué concepto es más central? |
| `graph_analyzer` | Estadísticas | Contar nodos, relaciones, componentes |
| `node2vec` | Embeddings | Vectorizar nodos para ML |

Para verlos todos desde Cypher:
```cypher
CALL mg.get_procedures() YIELD name, signature RETURN name, signature;
```

---

## 10. Checklist Rápido para Cualquier Programador

```
□ ¿Qué es?      → Base de datos de grafos en RAM, compatible con Neo4j
□ ¿Dónde está?  → Docker en TR/db/memgraph-platform/
□ ¿Cómo arranco?→ ares mem start
□ ¿Cómo paro?   → ares mem stop
□ ¿Cómo conecto?→ bolt://localhost:7687 (Python: neo4j driver)
□ ¿Cómo veo?    → http://localhost:3000 (Memgraph Lab)
□ ¿Cuánto ocupa?→ 612 MB vacío + 204B/nodo + 154B/relación
□ ¿Cuándo migrar?→ >10M nodos (>4GB RAM datos) → otra base de datos
□ ¿Persistencia?→ Agregar volumen en docker-compose.yml
□ ¿Documentación completa?→ TR/docs/MEMGRAPH/ARQUITECTURA.md
```

---

*Documento creado: 2026-04-11 | Memgraph v3.9.0-rc3 | RAM máquina: 7.3 GB | Fórmula oficial Memgraph*

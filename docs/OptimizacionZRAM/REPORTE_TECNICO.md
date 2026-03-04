# Reporte Técnico: Optimización Extrema de Memoria (zRAM + Kernel Tuning)

## 1. Infraestructura Actualizada
- **RAM Física:** 8GB DDR4.
- **zRAM (Swap en RAM):** 8GB con algoritmo **zstd** (Compresión ~3:1).
- **Swap de Respaldo (NVMe):** 21GB (Prioridad baja).
- **Capacidad Virtual Efectiva:** ~24GB - 28GB antes de tocar disco.

## 2. Componentes Instalados y Por Qué
### zram-tools
- **Para qué:** Gestión granular del dispositivo de bloques comprimidos.
- **Por qué:** Permite usar **zstd**, que comprime mucho más que el estándar lz4, ideal para sistemas con 8GB de RAM que corren modelos de IA o muchas pestañas de Chrome.

### Kernel Tuning (sysctl)
- **vm.swappiness=180:** Fuerza al kernel a preferir la compresión en RAM sobre el archivo de swap lento del NVMe.
- **vm.page-cluster=0:** Ajuste crítico para zRAM. Evita que el CPU descomprima datos innecesarios, eliminando micro-tirones (stuttering).
- **MGLRU (Multi-Gen LRU):** Activado para que el kernel sea más inteligente al decidir qué páginas de memoria están 'frías' (para comprimir) y cuáles 'calientes' (para mantener activas).

## 3. Beneficios Obtenidos
1. **Velocidad:** Acceso a swap a velocidad de bus de memoria, no de disco.
2. **Protección del NVMe:** Se reducen drásticamente las escrituras en el SSD, extendiendo su vida útil.
3. **Estabilidad:** El sistema no se 'congela' cuando la RAM se llena; simplemente comprime más datos en tiempo real.

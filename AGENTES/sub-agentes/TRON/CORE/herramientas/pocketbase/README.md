# 🗄️ Herramientas PocketBase para TRON CORE

**Sistema de herramientas no gestionadas por `despachador.py`** para operaciones CRUD tanto de esquema como de datos en PocketBase.

> **IMPORTANTE**: Estas herramientas son **independientes** del despachador central de TRON. Se ejecutan directamente con Python/NodeJS.

## 📋 Características Principales

✅ **CRUD completo** para datos y esquemas
✅ **Entrada JSON inteligente** - acepta comandos en formato JSON
✅ **Logging extensivo** - depuración detallada con niveles de verbosidad
✅ **Manejo robusto de errores** - con sugerencias contextuales
✅ **Reintentos automáticos** - para fallos de red/conexión
✅ **Herramientas auxiliares** - validación, generación, formateo
✅ **Pruebas de conexión** - verificación completa del entorno

## 🚀 Instalación Rápida

```bash
# Dar permisos de ejecución
chmod +x TRON/CORE/herramientas/pocketbase/*.py

# Crear directorio de logs
mkdir -p TRON/CORE/herramientas/pocketbase/logs/
```

## 🛠️ Herramientas Disponibles

### 1. **pocketbase_crud.py** - Operaciones CRUD de datos
```bash
# Ver ayuda
python3 pocketbase_crud.py --help

# Ejemplos básicos
python3 pocketbase_crud.py '{"action": "list_collections_with_schema"}'
python3 pocketbase_crud.py '{"action": "query_records", "collection": "users", "params": {"limit": 10}}'
python3 pocketbase_crud.py '{"action": "batch_create", "collection": "products", "records": [...]}'
```

### 2. **pocketbase_schema.py** - Gestión de esquemas
```bash
# Ver ayuda
python3 pocketbase_schema.py --help

# Ejemplos
python3 pocketbase_schema.py list_collections
python3 pocketbase_schema.py get_collection users
python3 pocketbase_schema.py create_collection '{"name": "orders", "type": "base", "schema": [...]}'
python3 pocketbase_schema.py add_field users '{"name": "phone", "type": "text", "required": true}'
```

### 3. **pocketbase_utils.py** - Utilidades y helpers
```bash
# Ver ayuda
python3 pocketbase_utils.py --help

# Ejemplos
python3 pocketbase_utils.py validate_schema schema.json
python3 pocketbase_utils.py generate_field email --name user_email --required true
python3 pocketbase_utils.py format_data records.json --type records
```

### 4. **test_connection.py** - Pruebas de conexión
```bash
# Prueba completa
python3 test_connection.py

# Prueba rápida
python3 test_connection.py --quick

# Salida JSON
python3 test_connection.py --json
```

## 📝 Referencia de Comandos JSON

### Acciones soportadas por `pocketbase_crud.py`

#### `query_records` - Consultar registros
```json
{
  "action": "query_records",
  "collection": "nombre_coleccion",
  "params": {
    "filter": "campo='valor'",
    "limit": 10,
    "page": 1,
    "sort": "-created"
  }
}
```

#### `list_collections_with_schema` - Listar colecciones
```json
{
  "action": "list_collections_with_schema"
}
```

#### `batch_create` - Creación masiva
```json
{
  "action": "batch_create",
  "collection": "products",
  "records": [
    {"name": "Producto 1", "price": 100},
    {"name": "Producto 2", "price": 200}
  ]
}
```

#### `update_record` - Actualizar registro único
```json
{
  "action": "update_record",
  "collection": "users",
  "id": "record_id_123",
  "data": {"email": "nuevo@email.com"}
}
```

#### `batch_update` - Actualización masiva
```json
{
  "action": "batch_update",
  "collection": "users",
  "records": [
    {"id": "id1", "status": "active"},
    {"id": "id2", "status": "inactive"}
  ]
}
```

#### `delete_record` - Eliminar registro único
```json
{
  "action": "delete_record",
  "collection": "users",
  "id": "record_id_123"
}
```

#### `batch_delete` - Eliminación masiva
```json
{
  "action": "batch_delete",
  "collection": "logs",
  "record_ids": ["id1", "id2", "id3"]
}
```

## 🔧 Configuración

Las credenciales están configuradas en `PocketBaseConfig` dentro de `pocketbase_crud.py`:

```python
class PocketBaseConfig:
    BASE_URL = "http://127.0.0.1:8090"
    ADMIN_EMAIL = "elprofesorverdad@gmail.com"
    ADMIN_PASSWORD = "Copa007copa."
```

**Para modificar estas credenciales**, edita directamente el archivo `pocketbase_crud.py`.

## 📊 Formatos de Salida

Todas las herramientas soportan múltiples formatos de salida:

```bash
# JSON puro (para scripting)
python3 pocketbase_crud.py '{"action": "..."}' --output json

# Formateado legible (default)
python3 pocketbase_crud.py '{"action": "..."}' --output pretty

# Simple (una línea)
python3 pocketbase_crud.py '{"action": "..."}' --output simple
```

## 🐛 Depuración y Logging

### Niveles de verbosidad
```bash
# Logging normal
python3 pocketbase_crud.py '{"action": "..."}'

# Logging detallado
python3 pocketbase_crud.py '{"action": "..."}' --verbose

# Ver logs en tiempo real
tail -f TRON/CORE/herramientas/pocketbase/logs/*.log
```

### Archivos de log
Los logs se guardan automáticamente en:
```
TRON/CORE/herramientas/pocketbase/logs/
├── pocketbase_crud_20250108_143045.log
├── pocketbase_schema_20250108_143112.log
├── pocketbase_utils_20250108_143130.log
└── test_connection_20250108_143145.log
```

## 🧪 Ejemplos Complejos

### Ejemplo 1: Pipeline completo con JSON
```bash
# 1. Verificar conexión
python3 test_connection.py --json > connection.json

# 2. Listar colecciones
python3 pocketbase_crud.py '{"action": "list_collections_with_schema"}' --output json > collections.json

# 3. Consultar datos de una colección
python3 pocketbase_crud.py '{"action": "query_records", "collection": "users", "params": {"limit": 5}}' --output pretty
```

### Ejemplo 2: Scripting con pipes
```bash
# Crear comando desde archivo
cat command.json | python3 pocketbase_crud.py --stdin

# Filtrar resultados con jq
python3 pocketbase_crud.py '{"action": "..."}' --output json | jq '.result[].name'
```

### Ejemplo 3: Operaciones en lote
```bash
# Crear múltiples registros desde JSON externo
python3 pocketbase_crud.py "$(cat new_records.json)"

# Actualizar en lote desde CSV convertido a JSON
python3 pocketbase_crud.py '{"action": "batch_update", "collection": "inventory", "records": [...]}'
```

## 🔄 Integración con n8n

Estas herramientas replican la funcionalidad del flujo n8n existente:

**Comparación con n8n:**
- ✅ **Mismas acciones**: `query_records`, `batch_create`, etc.
- ✅ **Misma autenticación**: Admin credentials
- ✅ **Mismo formato JSON**: Compatible con contratos existentes
- ✅ **Más características**: Logging, validación, utilidades extras

**Migración desde n8n:**
```bash
# En n8n: {"action": "query_records", "collection": "users"}
# En estas herramientas:
python3 pocketbase_crud.py '{"action": "query_records", "collection": "users"}'
```

## ⚠️ Solución de Problemas

### Error: "No se puede conectar al servidor"
```bash
# Verificar que PocketBase esté corriendo
curl http://127.0.0.1:8090/api/health

# Probar conexión completa
python3 test_connection.py --verbose
```

### Error: "Autenticación fallida"
1. Verificar credenciales en `pocketbase_crud.py`
2. Confirmar que el usuario admin existe en PocketBase
3. Probar manualmente:
   ```bash
   curl -X POST http://127.0.0.1:8090/api/admins/auth-with-password \
     -H "Content-Type: application/json" \
     -d '{"identity": "elprofesorverdad@gmail.com", "password": "Copa007copa."}'
   ```

### Error: "JSON inválido"
```bash
# Validar JSON
python3 pocketbase_utils.py validate_schema tu_archivo.json

# Usar formato correcto
echo '{"action": "query_records", "collection": "test"}' | python3 -m json.tool
```

## 📈 Mejores Prácticas

### 1. **Usar logging extensivo para desarrollo**
```bash
export POCKETBASE_VERBOSE=1
python3 pocketbase_crud.py '{"action": "..."}' --verbose
```

### 2. **Validar esquemas antes de aplicar cambios**
```bash
python3 pocketbase_utils.py validate_schema nuevo_esquema.json
python3 pocketbase_schema.py import nuevo_esquema.json --mode validate
```

### 3. **Probar conexión antes de operaciones críticas**
```bash
python3 test_connection.py
if [ $? -eq 0 ]; then
    python3 pocketbase_crud.py '{"action": "batch_delete", ...}'
fi
```

### 4. **Usar salida JSON para scripting**
```bash
# Capturar resultados en variables
COLLECTIONS=$(python3 pocketbase_crud.py '{"action": "list_collections_with_schema"}' --output json)
echo $COLLECTIONS | jq '.result[].name'
```

## 🎯 Casos de Uso Comunes

### Migración de datos
```bash
# 1. Exportar esquema
python3 pocketbase_schema.py export --output old_schema.json

# 2. Crear nuevas colecciones
python3 pocketbase_schema.py import new_schema.json --mode apply

# 3. Migrar datos
python3 pocketbase_crud.py "$(cat migration_data.json)"
```

### Backup automático
```bash
#!/bin/bash
# backup_pocketbase.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Exportar esquema
python3 pocketbase_schema.py export --output schema_${TIMESTAMP}.json

# Exportar datos clave
python3 pocketbase_crud.py '{"action": "query_records", "collection": "users", "params": {"perPage": 1000}}' \
  --output json > users_${TIMESTAMP}.json
```

### Monitoreo de salud
```bash
#!/bin/bash
# health_check.sh
python3 test_connection.py --json > /tmp/pocketbase_health.json

if jq -e '.success' /tmp/pocketbase_health.json >/dev/null; then
    echo "✅ PocketBase saludable"
else
    echo "❌ Problemas con PocketBase"
    cat /tmp/pocketbase_health.json | jq '.tests'
fi
```

## 🔗 Enlaces Relacionados

- **Documentación PocketBase**: https://pocketbase.io/docs/
- **API Reference**: https://pocketbase.io/docs/api-records/
- **TRON CORE Principal**: `TRON/LEEME_TRON.md`
- **Flujos n8n originales**: `TRON/docs/Respaldo de Flujos de Pocketbase/`

---

**Última actualización**: 2025-01-08
**Versión**: 1.0.0
**Compatibilidad**: PocketBase v0.22+
**Mantenido por**: Sistema TRON CORE
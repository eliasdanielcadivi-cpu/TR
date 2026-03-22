# TRON Bin

Scripts binarios y utilidades del sistema TRON.

## Dependencias

- Python >= 3.8
- uv (recomendado) o pip

## Instalación

```bash
# Usando uv (recomendado)
uv pip install -e .

# Usando pip tradicional
pip install -e .
```

## Estructura

- `pyproject.toml` - Configuración del proyecto Python y dependencias
- `tron/` - Módulos principales

## Uso

El comando `tron` estará disponible después de la instalación.

## Desarrollo

```bash
# Instalar en modo desarrollo
uv pip install -e .

# Ejecutar pruebas (si existen)
python -m pytest
```
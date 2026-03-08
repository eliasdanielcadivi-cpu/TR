# Instalación de AVISO en /usr/bin

## Opción 1: Con sudo (recomendado)

```bash
sudo cp /home/daniel/tron/programas/TR/modules/aviso/aviso /usr/bin/aviso
sudo chmod +x /usr/bin/aviso
```

## Opción 2: Con ini (desde el directorio del módulo)

```bash
cd /home/daniel/tron/programas/TR/modules/aviso
ini prod
# Seguir prompts: Enter para main.py, luego escribir "aviso.py"
```

## Opción 3: Alias temporal (sin instalar)

```bash
# Añadir a ~/.bashrc
alias aviso='python3 ~/tron/programas/TR/modules/aviso/aviso.py'
source ~/.bashrc
```

## Verificación

```bash
aviso --help
aviso lista
```

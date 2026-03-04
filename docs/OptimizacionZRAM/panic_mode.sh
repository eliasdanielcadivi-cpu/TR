#!/bin/bash
# Script: Panic Mode - Limpieza Profunda de Memoria
# Ubicación: /home/daniel/tron/programas/TR/docs/OptimizacionZRAM/panic_mode.sh

echo "--- Iniciando Limpieza de Emergencia (Panic Mode) ---"

# 1. Sincronizar datos pendientes al disco
sync

# 2. Purgar caché de lectura del sistema (PageCache, dentries y inodes)
echo "a" | sudo -S bash -c 'echo 3 > /proc/sys/vm/drop_caches'

# 3. Compactar zRAM (Forzar compresión máxima de lo que hay en swap)
for dev in /dev/zram*; do
    echo "a" | sudo -S bash -c "echo 1 > ${dev}/compact"
done

# 4. Limpieza de memoria swap (Mover de disco a RAM si hay espacio)
echo "a" | sudo -S swapoff -a && echo "a" | sudo -S swapon -a

echo "--- Memoria Optimizada: Listos para IA ---"
free -h

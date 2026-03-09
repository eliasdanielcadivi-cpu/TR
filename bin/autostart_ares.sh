#!/bin/bash
# ARES Autostart Maestro - Protocolo de Supervivencia (SIN SUDO)
LOG="/home/daniel/tron/programas/TR/logs/autostart.log"
SUCCESS_FILE="/home/daniel/tron/programas/TR/papelera/autostart_success.txt"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "--- INICIO AUTOSTART ARES [$DATE] ---" >> "$LOG"

# 1. Lanzar aviso daemon (Soberanía de Usuario)
pkill -f "aviso daemon"
/home/daniel/tron/programas/TR/modules/aviso/aviso daemon >> "$LOG" 2>&1 &

if [ $? -eq 0 ]; then
    echo "[OK] aviso daemon lanzado" >> "$LOG"
    echo "AUTOSTART_SUCCESS: $DATE" > "$SUCCESS_FILE"
else
    echo "[FAIL] error al lanzar aviso daemon" >> "$LOG"
fi

# 2. Notificación visual básica
notify-send "ARES" "Sistema de Avisos Activo"

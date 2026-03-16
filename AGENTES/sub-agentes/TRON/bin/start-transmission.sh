#!/bin/bash
# Start Transmission daemon with web interface

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSMISSION_DIR="${SCRIPT_DIR}/transmission-bin"
DAEMON="${TRANSMISSION_DIR}/transmission-daemon"
CONFIG_DIR="${SCRIPT_DIR}/.transmission-config"
PID_FILE="${CONFIG_DIR}/transmission.pid"
PORT=9091

# Create config directory
mkdir -p "${CONFIG_DIR}"

# Stop existing daemon if running
if [ -f "${PID_FILE}" ]; then
    kill "$(cat "${PID_FILE}")" 2>/dev/null
    rm -f "${PID_FILE}"
fi

# Start daemon
echo "Starting Transmission daemon on port ${PORT}..."
echo "Web interface: http://localhost:${PORT}/transmission/web/"
echo "Config directory: ${CONFIG_DIR}"
echo ""

"${DAEMON}" \
    --foreground \
    --port "${PORT}" \
    --no-auth \
    --config-dir "${CONFIG_DIR}" \
    --pid-file "${PID_FILE}" \
    --logfile "${CONFIG_DIR}/transmission.log" \
    --allowed "127.0.0.1,::1" \
    "$@"

# If foreground mode exits, daemon stopped
echo "Transmission daemon stopped."
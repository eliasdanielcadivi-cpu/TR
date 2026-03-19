#!/bin/bash
# Transmission helper script for using extracted binaries

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${SCRIPT_DIR}/transmission-bin"

# Add bin directory to PATH
export PATH="${BIN_DIR}:${PATH}"

# Display available commands
echo "Available Transmission commands:"
echo ""
echo "  transmission-cli     - Command-line client for single torrents"
echo "  transmission-daemon  - Headless daemon with web interface"
echo "  transmission-remote  - Remote control for transmission-daemon"
echo "  transmission-create  - Create .torrent files"
echo "  transmission-edit    - Edit .torrent files"
echo "  transmission-show    - Show .torrent file contents"
echo "  transmission-gtk     - GTK GUI client (requires GTK)"
echo ""
echo "Quick start:"
echo "  ./start-transmission.sh     - Start daemon with web UI"
echo "  transmission-cli <torrent>  - Download a torrent"
echo ""
echo "Web interface: http://localhost:9091/transmission/web/"
echo ""
echo "Note: All binaries are self-contained with system library dependencies."
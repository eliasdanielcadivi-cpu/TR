#!/bin/bash
# Standalone BR Launcher for ARES
BROOT_BIN="/home/daniel/tron/programas/TR/bin/broot-core/broot-bin"
BROOT_CONF="/home/daniel/tron/programas/TR/config/broot/conf.hjson"
CMD_FILE=$(mktemp)
if "$BROOT_BIN" --conf "$BROOT_CONF" --outcmd "$CMD_FILE" "$@"; then
    CMD=$(<"$CMD_FILE")
    rm -f "$CMD_FILE"
    eval "$CMD"
    exec zsh -i
else
    CODE=$?
    rm -f "$CMD_FILE"
    exit "$CODE"
fi

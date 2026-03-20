#!/bin/bash
# Uso: ./ares-identity.sh [--spinner] [--rotate]
CONFIG="config.yaml"
./ares_engine -mode avatar -config "$CONFIG"
if [[ "$*" == *"--spinner"* ]]; then
    if [[ "$*" == *"--rotate"* ]]; then
        ./ares_engine -mode spinner -rotate -config "$CONFIG"
    else
        ./ares_engine -mode spinner -config "$CONFIG"
    fi
fi

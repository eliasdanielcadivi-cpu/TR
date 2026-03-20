#!/bin/bash
cd /home/daniel/tron/programas/TR/modules/ui/GO2/
./ares_ui -mode avatar -config config.yaml
if [[ "$*" == *"--spinner"* ]]; then
    if [[ "$*" == *"--rotate"* ]]; then
        ./ares_ui -mode spinner -rotate -config config.yaml
    else
        ./ares_ui -mode spinner -config config.yaml
    fi
fi

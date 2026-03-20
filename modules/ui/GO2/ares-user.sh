#!/bin/bash
cd /home/daniel/tron/programas/TR/modules/ui/GO2/
SLOGAN=${1:-""}
./ares_ui -mode user -slogan "$SLOGAN" -config config.yaml

#!/bin/bash
cd /home/daniel/tron/programas/TR/modules/ui/GO2/
SLOGAN="Yo defiendo al usuario"
# Extraer slogan si existe
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
    if [[ "${args[i]}" == "--slogan" ]]; then
        SLOGAN="${args[i+1]}"
    fi
done
./ares_ui -mode avatar -slogan "$SLOGAN" -config config.yaml
if [[ "$*" == *"--spinner"* ]]; then
    if [[ "$*" == *"--rotate"* ]]; then
        ./ares_ui -mode spinner -rotate -config config.yaml
    else
        ./ares_ui -mode spinner -config config.yaml
    fi
fi
# Dos retornos de carro finales (desbloqueo)
echo -e "

"

# ~/tron/programas/TR/config/user/init.zsh
# ORQUESTADOR DEL LEGADO TRON PARA ARES/KITTY

USER_CONFIG_DIR="$HOME/tron/programas/TR/config/user"

# 1. Cargar Variables de Entorno (Prioridad alta)
[[ -f "$USER_CONFIG_DIR/env.zsh" ]] && source "$USER_CONFIG_DIR/env.zsh"

# 2. Cargar Funciones Adaptadas
[[ -f "$USER_CONFIG_DIR/functions.zsh" ]] && source "$USER_CONFIG_DIR/functions.zsh"

# 3. Cargar Alias (Sustituye comandos si es necesario)
[[ -f "$USER_CONFIG_DIR/alias.zsh" ]] && source "$USER_CONFIG_DIR/alias.zsh"

# Confirmación de carga
# echo "🚀 ARES: Legado de Daniel Hung cargado."

# /home/daniel/tron/programas/TR/config/zsh/.zshrc
# --- ARES SOBERANO - CONFIGURACION ENCAPSULADA EN TR ---

# 1. Asegurar ZDOTDIR (Soberanía de Configuración)
export ZDOTDIR="/home/daniel/tron/programas/TR/config/zsh"

# 2. Configuración de Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting fast-syntax-highlighting zsh-completions sudo history colored-man-pages command-not-found copypath copyfile dirhistory fzf)

# Cargar Oh My Zsh
[[ -f $ZSH/oh-my-zsh.sh ]] && source $ZSH/oh-my-zsh.sh

# 3. Opciones de Productividad
setopt AUTO_CD AUTO_PUSHD PUSHD_IGNORE_DUPS EXTENDED_HISTORY SHARE_HISTORY CORRECT CORRECT_ALL

# 4. Atajos de Teclado (Zsh)
bindkey -e
bindkey '^[[1;5C' forward-word
bindkey '^[[1;5D' backward-word

# --- 🛰️ CARGAR EL LEGADO TRON / ARES CORE ---
# Este es el punto de unión con tus variables, alias y funciones
if [[ -f "/home/daniel/tron/programas/TR/config/user/init.zsh" ]]; then
    source "/home/daniel/tron/programas/TR/config/user/init.zsh"
fi

# 5. Estética y Plugins Adicionales
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# 6. Alias de Emergencia (Si actz falla, este te salva)
alias ares-recuperar='source /home/daniel/tron/programas/TR/config/zsh/.zshrc'

export UV_NO_WARN=1

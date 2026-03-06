# ~/tron/programas/TR/config/user/env.zsh
# VARIABLES DE ENTORNO TRON/ARES - Daniel Hung

export usuario="${SUDO_USER:-${USER}}"

# Servidores Casa
export tronDream='tron@172.16.0.141'
export clienteNode='cliente@172.16.0.124'

# TRON CARPETAS
export tron="/home/$usuario/tron"
export programas="$tron/programas"
export TRON="$programas/TRON"
export tron_plugins="$tron/plugins"
export sesiones="$tron/sesiones"
export funciones="$tron/funciones"
export sitio="/home/daniel/ReposWebs/mundomejor/_site"
export biblioteca="$tron/biblioteca"
export zdemas="$tron/zdemas"
export respaldosln="$tron/zzRespaldosDeLn"
export papelera="$tron/ZPAPELERA"
export scripts_ares="/home/daniel/tron/programas/TR/scripts"
export logs="$tron/logs"
export config="$tron/config"
export legos1="$tron/1-LEGOS"
export legos="$legos1"
export inicio="$tron/programas/Admon/inicio"
export TR="$programas/TR"
# SubCarpetas TRON
export tronbash="$tron_plugins/bash"
export trongedit="$tron_plugins/gedit"
export tronscripts="$tron_plugins/admScripts"
export practica="$papelera/practica"
export appimage="$tron_plugins/AppImage"
export musica="$biblioteca/musica"
export musicatv="$biblioteca/musicatv"
export cursos="$legos1/CURSOS"
export mudanza="$programas/Mudanza"
export comprimidos="$tron_plugins/ComprimidosO.deb"
export sesiones_prog="$programas/sesiones/sesiones"
export interfaces="$programas/interfaces"
export consultas="$programas/consultasdb"
export worksym="$programas/WEB/symfonyWorkspace"

# Documentos TRON
export tronalias="$tronbash/alias.sh"
export variables="$tron/plugins/bash/bashVariables.sh"
export bashfunciones="/home/daniel/tron/plugins/bash/bashFunciones.sh"
export bajonivel="$scripts/BajoNivel.sh"
export data="$tron/data"
export agente="$programas/TRON/OLLAMA-LANGCHAING-AGENTE$"

# GEDIT
export geditSis="/usr/share/gedit/plugins/externaltools/tools"
export geditSnippets="/usr/share/gedit/plugins/snippets"

# XDG User Dirs
export desktop=$(xdg-user-dir DESKTOP)
export download=$(xdg-user-dir DOWNLOAD)
export templates=$(xdg-user-dir TEMPLATES)
export publicshare=$(xdg-user-dir PUBLICSHARE)
export documents=$(xdg-user-dir DOCUMENTS)
export music=$(xdg-user-dir MUSIC)
export pictures=$(xdg-user-dir PICTURES)
export videos=$(xdg-user-dir VIDEOS)

export escritorio="$desktop"
export descargas="$download"
export plantillas="$templates"
export carpetascompartidas="$publicshare"
export documentos="$documents"
export musica_lib="$music"
export imagenes="$pictures"
export videos_lib="$videos"

# IMPORTANTES DEL SISTEMA
export servicios="/etc/systemd/system"
export fuentes="/etc/apt/sources.list"

# DESARROLLO
export www="/var/www/html" 
export kivyejemplos="/usr/share/kivy-examples"
export pycharm="/home/daniel/tron/plugins/pycharm"

# ACCESORIOS
export notas="/$tron/zdemas"

# BROOT CONFIG (ENCAPSULADO EN TR)
export TR_BROOT_BIN="/home/daniel/tron/programas/TR/bin/broot-core/broot-bin"
export TR_BROOT_CONF="/home/daniel/tron/programas/TR/config/broot/conf.hjson"

# SOBERANIA ZSH
export ZDOTDIR="/home/daniel/tron/programas/TR/config/zsh"

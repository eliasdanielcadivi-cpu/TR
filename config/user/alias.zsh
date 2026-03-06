# ~/tron/programas/TR/config/user/alias.zsh
# ALIAS MIGRADOS AL SISTEMA ARES - Daniel Hung

# --- CORE ARES RECARGA ---
alias actz='source /home/daniel/tron/programas/TR/config/zsh/.zshrc; echo "🚀 ARES: Entorno TR/config/zsh Sincronizado por Daniel Hung."'

# --- ALIAS DE EDICIÓN RÁPIDA (CON AUTORECARGA) ---
alias aliased='micro ~/tron/programas/TR/config/user/alias.zsh; actz'
alias vared='micro ~/tron/programas/TR/config/user/env.zsh; actz'
alias funced='micro ~/tron/programas/TR/config/user/functions.zsh; actz'
alias inited='micro ~/tron/programas/TR/config/user/init.zsh; actz'
alias aresrced='micro ~/tron/programas/TR/config/zsh/.zshrc; actz'
alias AltoNivel='micro ~/tron/programas/TR/scripts/AltoNivel.sh'
alias BajoNivel='micro ~/tron/programas/TR/scripts/BajoNivel.sh'

# --- ALIAS DEL SISTEMA ---
alias agenda='uv run --quiet --project /home/daniel/tron/programas/AGENDA python /home/daniel/tron/programas/AGENDA/main.py'
alias agendaed='uv run --quiet --project /home/daniel/tron/programas/AGENDA python /home/daniel/tron/programas/AGENDA/main.py editar'
alias agendaweb='uv run --quiet --project /home/daniel/tron/programas/AGENDA python /home/daniel/tron/programas/AGENDA/main.py web'
alias abrircurso="abrirdocuArray"
alias activar="source /home/daniel/.venv/bin/activate"
alias actualizable="apt list --upgradable"
alias adb-iniciar='adb start-server'
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
alias aliaslk='alias | grep $1'
alias antivirus-actualizar='systemctl stop clamav-daemon.service && freshclam'
alias antivirus-comenzar='/etc/init.d/clamav-daemon start'
alias antivirus-parar='systemctl stop clamav-daemon.service || systemctl stop clamav-freshclam.service || systemctl disable clamav-daemon.service || systemctl disable clamav-freshclam.service'
alias apache-restart="sudo systemctl restart apache2"
alias apagar-monitor='export DISPLAY=:0; xset dpms force off'
alias apagarPantalla="export DISPLAY=:0; xset dpms force off"
alias apariencia-ventanas="lxappearance"
alias ap='export DISPLAY=:0; xset dpms force off'
alias audifonos="pactl set-sink-port alsa_output.pci-0000_00_1f.3.analog-stereo analog-output-headphones"
alias audio="python3 /home/daniel/tron/programas/a-DIRECTORIO/EDICION-VIDEO-IMAGENES/audioTel.py"
alias audioVer="pactl list modules"
alias av="playerctl position 10+"
alias bajar="playerctl volume 0.1-"
alias BalancedHenao='crom-tienda https://www.notion.so/02212024bfe3472c9c758dcf68c5ad03?v=92548ff6fa8046c38086759321cf84e7'
alias bashed="sudo micro ~/.zshrc"
alias ba="wget"
alias borrarRedis="redis-cli FLUSHALL"
alias botarbasura="papelera-borrar"
alias box-editar='editar /home/daniel/.config/openbox/autostart'
alias buscarChatGemini='echo ag "Think Tool" -G "\.json$" -C 2 --width 200'
alias buscark='funbuscar'
alias buscar='mlocate -ipt'
alias buscar-txt='funbuscartexto'
alias vared="micro /home/daniel/tron/programas/TR/config/user/env.zsh"
alias cambiosCarpeta="cambios_carpeta"
alias cc='source cambiosCarpeta'
alias chat-pizza='cd ~/tron/programas/ProyectoPizza && gemini --resume 262ccf63-5430-4c1b-819b-f5dab99e7aac --yolo'
alias chmod='chmod -v'
alias chown='chown -v'
alias chuletaDocker="batcat /home/daniel/tron/programas/ProyectoPizza/DOCUMENTACION/Docker/chuleta.md"
alias clasificar="renombra"
alias climaen="curl wttr.in/"
alias clonezilla="/usr/sbin/clonezilla"
alias cloudflareded="br ~/.cloudflared/"
alias cloudflare-node="crom-eliashung https://dash.cloudflare.com"
alias cls='clear'
alias cody-programador="crom-eliashung $programador > /dev/null 2>&1 &"
alias comprimir="sudo /home/daniel/Escritorio/.venv-compressor/bin/python /home/daniel/tron/programas/Admon/COMPRIMIR/comprimir"
alias computadora='echo "--- CPU ---" && lscpu | grep -E "Model name|CPU\(s\)|MHz" && echo "--- Memoria RAM ---" && free -h | grep "Mem" && echo "--- GPU ---" && lspci -vnn | grep -i vga && echo "--- Velocidad de Internet ---" && speedtest-cli; cat /etc/os-release; hostnamectl'
alias conDream="ssh tron@172.16.0.141"
alias conNode="ssh cliente@172.16.0.124"
alias cornetas="pactl set-sink-port alsa_output.pci-0000_00_1f.3.analog-stereo analog-output-speaker"
alias cp='cp -v'
alias cpproy="cp -vfa proyectos /home/daniel/ReposWebs/mundomejor/_site/"
alias crom-elias1='google-chrome --profile-directory="Profile 4"'
alias crom-eliashung='google-chrome --profile-directory="Profile 8"'
alias crom-medicos='google-chrome --profile-directory="Profile 5"'
alias crom-mma='google-chrome --profile-directory="Profile 10"'
alias crom-notas='google-chrome --profile-directory="Profile 3"'
alias croms='google-chrome --profile-directory="System Profile" > /dev/null 2>&1 &'
alias crom-stgo='google-chrome --profile-directory="Profile 7"'
alias crom-tienda='google-chrome --profile-directory="Profile 6"'
alias crom='/usr/bin/google-chrome-stable %U'
alias crush='(cd /home/daniel/tron/programas/proyectos_principales/proyecto_pizza/cli/crush/ && crush)'
alias cualesmiiplocal="hostname -i"
alias da="descargarAudio"
alias depurar='set -x; set -v; set -e' 
alias descargarAudio='sudo yt-dlp -U; yt-dlp -x -f "bestaudio" --ppa "EmbedThumbnail+ffmpeg_o:-c:v copy" --audio-quality 0'
alias descargarsubin='sudo yt-dlp -U; yt-dlp --impersonate Chrome-116 --sub-format srt --write-subs --write-auto-sub --sub-lang "en" --convert-subs srt --skip-download -o "%(title)s.%(ext)s"'
alias descargarVideo="sudo yt-dlp -U; yt-dlp"
alias descomprimir="sudo /home/daniel/Escritorio/.venv-compressor/bin/python /home/daniel/tron/programas/Admon/COMPRIMIR/descomprimir"
alias descomprimir-todos='for archivo in *; do unar "$archivo"; done'
alias discos='gnome-disks'
alias discos-montar='montarDiscos'
alias discos-mostrar='lsblk -fml'
alias dispEntrada="xinput list"
alias display="export DISPLAY=:0"
alias dondeestamongo="netstat -plant | grep mongo"
alias dondeesta="which"
alias dondeestoy="lsblk"
alias dor="xinput disable 9; systemctl suspend"
alias dream="ssh tron@172.16.141"
alias drive="autoSincroDri"
alias dv='descargarVideo'
alias e="cd /home/daniel/Escritorio"
alias editaraudio="$tron_plugins/AppImage/audacity-linux-3.2.3-x64.AppImage"
alias editar='ini="PWD"; cd /home/daniel/tron/programas/Admon; source /home/daniel/.venv/bin/activate; python3 /home/daniel/tron/programas/Admon/config_editor.py; cd "$ini"'
alias emergencia="micro $programas/RepDesastres/desastre.sh"
alias enlaces="ls --hyperlink=auto"
alias entorno-virtual-activar='fnActivar'
alias entrar="ssh -t daniel@172.16.0.217"
alias escritorio-configuracion="xfconf-query -l; xfce4-settings-editor; dconf-editor "
alias espacio="echo Espacio libre y usado en Gb; echo; df -h --output=pcent,avail,used --block-size=1G $(df . | awk 'NR==2{print $1}')"
alias estudiar="legos; abrircurso; kitty 1>/dev/null 2>/dev/null & disown"
alias estudio="estudiar"
alias fire='$tron_plugins/navegadores/firefox/firefox'
alias firewall-abrir="sudo ufw allow"
alias firewall-cerrar-entrantes="sudo ufw default deny incoming"
alias firewall-off="sudo ufw disable"
alias firewall-on="sudo ufw enable"
alias firewall-permitir-ip-puerto="echo 'sudo ufw allow from 203.0.113.4 to any port 22'"
alias firewall-permitir-ip="sudo ufw allow from"
alias firewall-permitir-salientes="sudo ufw default allow outgoing"
alias flash='gemini --model gemini-2.5-flash'
alias GeminiPro='gemini --model gemini-2.5-pro'
alias goose='/home/daniel/tron/programas/proyectos_principales/proyecto_pizza/cli/goose/goose'
alias gp="guardaPromts"
alias grabarAudio='parecord --channels=2 -d alsa_output.pci-0000_00_1f.3.analog-stereo.monitor salida.wav'
alias grip="md"
alias hardware='funHard'
alias hig='history -a ; echo la historia ha sido contada...'
alias historial="history | awk '{ \$1=\"\"; print substr(\$0,2) }'"
alias historysn="history | awk '{ \$1=\"\"; print substr(\$0,2) }'"
alias ibuscar='fire -search'
alias imagen-convertir-fondo='ImgConvFondoCompu'
alias imagen-info='imagenInformacion'
alias impostor="type -a"
alias impresionar="hollywood"
alias instalar-modulo-local='python3.10 -m pip install -e .'
alias installed="editar $programas/Mudanza/quinetaleenubu18sencillo.sh"
alias interfaz-activar='systemctl set-default graphical.target'
alias interfaz-desactivar='systemctl set-default multi-user.target'
alias interfaz-detener='systemctl stop graphical.target ; systemctl isolate multi-user.target'
alias interfaz-iniciar='systemctl start graphical.target'
alias interfaz-parar='systemctl stop graphical.target'
alias jekyllbuild="bundle exec jekyll build"
alias jekyllserve="bundle exec jekyll serve"
alias kaban="crom http://localhost:3001/"
alias kaban-off="sudo snap disable wekan; sudo umount -lfv /snap/core/15511; sudo umount -lfv /snap/wekan/1999; sudo systemctl stop snapd.service"
alias kaban-on="sudo systemctl start snapd.service; sleep 3; sudo snap enable wekan;"
alias kitty-dream="kitty +kitten ssh -L 9090:127.0.0.1:8384 tron@172.16.141"
alias la='ls -A'
alias lamp-stop="sudo service apache2 stop; sudo service mysql stop; sudo service php stop; sudo systemctl stop apache2; sudo systemctl stop mysql; sudo systemctl stop php"
alias leemeinstalar="micro $programas/Mudanza/LEEME.txt"
alias letras1='figlet -f 3d -d /home/daniel/tron/plugins/figlet/figlet-fonts/'
alias letras2='figlet -f Basic -d /home/daniel/tron/plugins/figlet/figlet-fonts/'
alias lik='aliaslike'
alias llave='sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys'
alias ll='ls -alF'
alias l='ls -CF'
alias logosWeb="/usr/bin/google-chrome-stable --profile-directory=Default https://elprofesoverdad.github.io/logos/ &" 
alias lsb="lsbonito"
alias lsbonito="br -sdp"
alias ls='ls --color=auto'
alias mandar-audio="sudo pactl load-module module-simple-protocol-tcp source=0 record=true port=12346"
alias MapasMentales='crom-notas https://gitmind.com/app/docs/mr8ou51a'
alias marcadores='/usr/bin/marcadores.sh'
alias markdown="marktext &"
alias matacrom='mata="kill -9 $(pidof chrome)"; eval $mata; unset mata'
alias memoria='sudo systemctl stop universal_embed.service qdrant.service embedding_server_daniel.service ollama.service && sudo pkill fwupd && sudo pkill -f "embedding_server.py" && echo "✅ Todo detenido. Memoria liberada."'
alias mic='/usr//bin/micro-smart.py camel'
alias mi="micro"
alias miniaturas='editar /etc/xdg/tumbler/tumbler.rc'
alias mis='/usr/bin/micro-smart.py slug'
alias mkbuild="mkdocs build -d"
alias mkserve="mkdocs serve"
alias mma='actual=$PWD; cd /home/daniel/ReposWebs/ArchivoMMA/mma-modificado-js; node gespro.js; cd "$actual"; unset actual'
alias moncrom='/usr/bin/python3 /home/daniel/tron/programas/sesiones/sesiones/monPerfiles.py --monitor --verbose'
alias monitor="export DISPLAY=:0"
alias montado="lsblk"
alias mount='mount -v'
alias mpvAyuda="cat /etc/mpv/input.conf"
alias mudanzaed="editar $programas/Mudanza/MudarSisDeExternoAHostDesdeHost.sh"
alias mudanza="micro $programas/Mudanza/MudarSisDeExternoAHostDesdeHost.sh"
alias musica="python3 /home/daniel/tron/programas/a-DIRECTORIO/MUSICA/mpv_tui_wrapper.py"
alias mv='mv -v'
alias n8n-mcp='/home/daniel/tron/programas/proyectos_principales/proyecto_pizza/mcp/n8n-mcp/run_mcp.sh'
alias n8nWeb='crom --profile-directory="Default" http://localhost:5678/'
alias navegar="br -sd"
alias nav='google-chrome-stable --check-for-update-integrity --profile-directory="Default" --new-window 2>&1 > /dev/null &'
alias negocio="dolphin /home/daniel/tron/1-LEGOS/NEGOCIO &"
alias noRaton="xinput disable 9"
alias op='ini="$PWD"; cd /home/daniel/tron/programas/proyectos_principales/proyecto_pizza/cli/open-interpreter; bash interpreter.sh; cd "$ini"'
alias papelera-borrar='locate --null .Trash | xargs -0 rm -v -r'
alias paquetesrotos="remienda() { apt --fix-broken install \$1 ; }; remienda"
alias pathed="sudo micro /etc/environment"
alias pause="playerctl pause"
alias p="cd $programas"
alias pdf='evince'
alias pizza="cd /home/daniel/tron/programas/ProyectoPizza/"
alias pizzaDocs="cd /home/daniel/tron/programas/ProyectoPizzaDocs/"
alias pizzaOld="cd ~/tron/programas/proyectos_principales/proyecto_pizza"
alias plaympv='mpv --config-dir=/home/daniel/tron/plugins/mpv/'
alias play="playerctl play"
alias practica="pruebas"
alias practicas="pruebas"
alias presupuesto="crom-eliashung https://www.notion.so/A-C-Servicios-Tur-sticos-Santa-Rosa-Oferta-9cef10beda8c4fdaa4a317f57ce1dd0b"
alias promtCarp="cd $legos/IA/PROMPTS/"
alias promted="promtCarp"
alias promt="guardaPromts"
alias prueba="pruebas"
alias pruebas="if [[ ! -d $programas/pruebas ]]; then mkdir $programas/pruebas; fi; cd $programas/pruebas"
alias py='/home/daniel/.venv/bin/python3'
alias qdOff='sudo systemctl stop qdrant.service fastembed.service splade.service'
alias qdOn='sudo systemctl start qdrant.service fastembed.service splade.service'
alias qdStatus='systemctl status qdrant.service fastembed.service splade.service'
alias queinstalesnap="snap-on; snap changes; ls -l /snap/bin; ls -l /var/lib/snapd/snaps"
alias queinstaleubuntu="micro $programas/Mudanza/quinetaleenubu18sencillo.sh"
alias quekerneltengo="uname -srm"
alias quienpuerto="sudo ss -tunelp | grep "
alias ratonOff='xinput disable 9'
alias raton="xinput enable 9"
alias red="nmtui"
alias reiniciaKdeconet="killall kdeconnectd; kdeconnectd &"
alias re="playerctl position 10-"
alias ReunionHook='crom-elias1 https://www.notion.so/Reuni-n-de-Hook-54e69a382e7e40e5b1900cb7c773bd27'
alias rm='rm -v'
alias ruta="readlink -f " 
alias servicio-activar="prin=\$PWD; cd /home/daniel/tron/config/systemd; source index.sh; cd \$prin; unset prin"
alias servicio-editar='br /etc/systemd/system/\$1'
alias servicios='systemctl list-units --type=service'
alias servidorDescargas="ini=\$PWD; cd ~/Descargas/servidor; npx serve; cd \$ini"
alias serv-py="/usr/bin/python3 -m http.server"
alias sesiones="python3 /home/daniel/tron/programas/sesiones/guardaCrom"
alias sesion="sesiones"
alias se="source entorno"
alias sitio-mma="cd ~/ReposWebs/mma; servidor-python"
alias sshed="microOvisual ~/.ssh/config"
alias ssh-reiniciar="sudo systemctl restart ssh"
alias s="sudo su"
alias stop="playerctl stop"
alias subed="flatpak run io.otsaloma.gaupol &"
alias subir="playerctl volume 0.1+"
alias suspender='sudo systemctl suspend'
alias sym-open="symfony open:local"
alias sym-start="symfony server:start"
alias sym-stop="symfony server:stop"
alias tel='crom --profile-directory="Default" https://myaccount.google.com/find-your-phone'
alias telefono='abrirEnTelefono'
alias tera='fire https://www.terabox.com/main?category=all'
alias todoed='editar $tron/1-LEGOS/0-ORGANIZACION/TODO.md'
alias todo='xdg-open $tron/1-LEGOS/0-ORGANIZACION/TODO.md'
alias torr='crom https://rarbgdata.org/index80.php https://thepiratebay.org/index.html https://torrentgalaxy.to https://pelistorrent.org https://pediatorrent.com https://yestorrent.org https://pelispanda.com https://mitorrent.me https://yts.mx https://1337x.to https://www.limetorrents.lol'
alias trans="cd ~/tron/programas/trans"
alias tra='transmission-gtk %U'
alias TrayectoriaProfesional='crom-notas https://lucid.app/lucidchart/436bbf51-662c-40b7-a761-26540038eb34/edit?page=0_0&invitationId=inv_b5109a0e-afc3-474e-8b14-744b464f5c8f#'
alias umount='umount -v'
alias updatedbed='editar /etc/updatedb.conf'
alias var='FunVariables'
alias vertabla='fnvertabla'
alias vol="alsamixer"
alias volumen="alsamixer"
alias warp-off="warp-cli disconnect"
alias warp-on="warp-cli connect"
alias web-a-pdf='wkhtmltopdf'

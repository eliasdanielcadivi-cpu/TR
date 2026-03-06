# ~/tron/programas/TR/config/user/functions.zsh
# FUNCIONES TRON/ARES - Daniel Hung

# --- UTILIDADES ---

# Función br (Broot) - Encapsulada en TR
function br {
    local cmd cmd_file code

    # Si no hay terminal interactivo, ejecutar broot normal
    if [ ! -t 0 ]; then
        "$TR_BROOT_BIN" --conf "$TR_BROOT_CONF" "$@"
        return $?
    fi

    cmd_file=$(mktemp)
    export TERM="${TERM:-xterm-256color}"

    if "$TR_BROOT_BIN" --conf "$TR_BROOT_CONF" --outcmd "$cmd_file" "$@"; then
        cmd=$(cat "$cmd_file")
        rm -f "$cmd_file"
        eval "$cmd"
    else
        code=$?
        rm -f "$cmd_file"
        return "$code"
    fi
}

transcribir() {
  local ini="$PWD"
  cd /home/daniel/tron/programas/trans/
  python3 descargaa.py
  cd "$ini"
} 

on() {
    sudo shutdown -c
    if [[ $? -eq 0 ]]; then
        echo -e "\n✅ Apagado cancelado con éxito."
    else
        echo -e "\n❌ No hay un apagado programado para cancelar."
    fi
}

off() {
    read "tiempo?¿Cuántos minutos apagar? (ej: 180): "
    if [[ "$tiempo" =~ ^[0-9]+$ ]]; then
        read -k 1 "REPLY?¿Apagar pantalla inmediatamente? (s/n): "
        echo 
        if [[ "$REPLY" =~ ^[Ss]$ ]]; then
            sudo shutdown +$tiempo "Apagado programado en $tiempo minutos"
            xset dpms force off
            echo -e "\n✅ Apagado programado y pantalla apagada."
        else
            sudo shutdown +$tiempo "Apagado programado."
            echo -e "\n✅ Apagado programado en $tiempo minutos."
        fi
    else
        echo "❌ Error: Debe ingresar un número."
    fi
}

perfiles(){
    for profile in ~/.config/google-chrome/{Default,Profile*}/; do
        pref="$profile/Preferences"
        if [ -f "$pref" ]; then
            name=$(jq -r '.profile.name // "N/A"' "$pref" 2>/dev/null)
            email=$(jq -r '.account_info[0].email // "N/A"' "$pref" 2>/dev/null)
            printf "\n\033[1;34mRuta:\033[0m\t%s\n\033[1;32mNombre:\033[0m\t%s\n\033[1;33mCorreo:\033[0m\t%s\n" "$profile" "$name" "$email"
        fi
    done
    echo -e "\nFuncion perfiles operativa."
}

abrirEnTelefono() {
    xdg-open "tel:+58$1"
}

arbol() {
   br -ws -c :pt "$@"
}

ir() {
    br --only-folders --cmd "$1;:cd"
}

respaldoDrive() {
	local ini=$PWD
	cd ~/tron/programas/sincroDrive
	./sincroDri.sh
	cd "$ini"
}	

colores() {
    source $scripts/lib/libcolores/libcolores.sh
    tablacoloresbash
}

sinoestainiciado() {
	if [[ -n $(pgrep $1) ]]; then
	    echo "No se ejecutará $1, ya está en ejecución."
	else
	    echo "$1 no está en ejecución. Iniciando..."
	    $1 &
	fi
}

sincro() {
    local inicio=$PWD
    cd "/home/$usuario/tron/plugins/syncthing-linux-amd64-v1.23.4"
    ./syncthing
    cd $inicio   
}
    
sincro-serve() {
    /usr/bin/syncthing serve --no-browser --logfile=default &
    disown
    fire http://127.0.0.1:8384
}

abrirgestordb() {
    local ini=$PWD
    clear
    cd $tron_plugins/AppImage/sqlite
    echo "1: Dbgate | 2: Antares"
    read "op?Opción: "
    if [[ $op == 1 ]]; then
        setsid ./dbgate-latest.AppImage 1>/dev/null 2>/dev/null
    elif [[ $op == 2 ]]; then
        setsid ./Antares-0.7.0-linux_x86_64.AppImage 1>/dev/null 2>/dev/null
    fi
    cd $ini
}

sqlite-ver() {
    local ini=$PWD
    clear
    echo "Ingresa el nombre de la base de datos:"
    local db=$(readlink -f "$data/sqlite")
    cd $tron_plugins/SQLiteStudio
    setsid ./sqlitestudio $db 1>/dev/null 2>/dev/null
    cd $ini
}

systemctl-reboot() {
    local unid=$1
    sudo systemctl disable $unid
    sudo systemctl daemon-reload $unid
    sudo systemctl enable $unid
    sudo systemctl start $unid
    sudo systemctl status $unid
    read "resp?¿Ver log? (1=Si): "
    if [[ $resp == 1 ]]; then
        journalctl -xeu $unid
    fi 
}

git-res() {
	cd /home/$usuario/tron
	local merideam=$(date +"%p")
	local respaldo=respaldo_$(date +%d%b%Y%a%Ih%Mm%Ss)-$merideam
	git config --global user.email "elprofesorverdad@gmail.com"
  	git config --global user.name "EliasHung"
	if [[ -z $1 ]]; then
		git commit -am "$respaldo"
	else
		git commit -am "$1-$respaldo"
	fi
	git push -u origin main
}

crearentorno() {
    local inicio=$PWD
    cd $tron_plugins/python/entornos
    read "nombre?Nombre del entorno: "
    virtualenv $nombre
    cd $inicio
}

activarentorno() {
    local aux=$PWD
    cd $tron_plugins/python/entornos
    if [[ -z $1 ]]; then
        ls
        read "nombre?¿Entorno a activar?: "
        cd "$nombre"
    else
        cd "$1"
    fi
    source bin/activate
    cd $aux
}

sshGit() {
    eval $(ssh-agent -s)
    read "correo?Correo de Git (ej: elias1hung@gmail.com): "
    ssh-keygen -t ed25519 -C $correo 
    ssh-add ~/.ssh/id_ed25519
    cat ~/.ssh/id_ed25519.pub
}

# --- BAJO NIVEL ---

editarComando() {
    micro "$(command -v "$1")"
}

relativa() {
    realpath --relative-to="$(br --conf ~/.config/broot/select.toml $1)" "$(br --conf ~/.config/broot/select.toml $2)"   
}

grepcolor() {
    grep --color=always -R $1
}

lesscolor() {
    less -r $1
}

copiar() {
    if [ -z "$1" ]; then
        echo "❌ Dime qué quieres copiar."
        return 1
    fi
    local RUTA=$(which "$1")
    if [ -n "$RUTA" ]; then
        cat "$RUTA" | xclip -sel clip
        echo "✅ Código de '$1' copiado."
    else
        echo "❌ No encontré '$1'."
    fi
}

verdependencias() {
    echo "1: .deb descargado | 2: nombre paquete"
    read "num?Opción: "
    if [[ $num == 1 ]]; then
        read "direccion?Ruta al paquete: "
        dpkg-deb -I $direccion
    elif [[ $num == 2 ]]; then
        read "paquete?Nombre paquete: "
        apt-cache depends $paquete
    fi
}

cp-igualito() {
    cp -vfa $1 $2
}

dondelovi() {
    if [[ -z $1 || -z $2 ]]; then
        echo "Uso: dondelovi texto ruta"
    else
        ag $1 $2
    fi
}

chismoso() {
    if [[ -z $1 || -z $2 ]]; then
        echo "Uso: chismoso texto ruta"
    else
        dondelovi "$1" "$2"
        echo -e "\nWhich:"
        which $1
        echo -e "\nCommand -V:"
        command -V $1
    fi
}

hayinternet() {
  echo "TRON: Verificando conexión..."
  if ! ping -c 1 google.com &>/dev/null; then
    echo "❌ Sin Internet"
    notify-send "TRON: Sin Internet"
  else
    echo "✅ Con Internet"
    notify-send "TRON: Con Internet"
    if ! command -v speedtest-cli &>/dev/null; then
        sudo apt install -y speedtest-cli
    fi
    speedtest-cli
  fi
}

pausa() {
    echo "$1"
    read -k 1 "?Presiona cualquier tecla..."
    echo
}

montarDiscos() {
    cd /dev
    for dsp in sd*; do
        local destino="/media/$usuario/$dsp"
        sudo mkdir -p $destino
        sudo mount /dev/$dsp $destino
    done
}

desmontarDiscos() {
    for dsp in /media/$usuario/sd*; do
        sudo umount -lf $dsp
        sudo rm -rf $dsp
    done
}

borrartodos() {
    locate $1
    read -k 1 "REPLY?¿Seguro desea borrarlos? (s/n): "
    echo
    if [[ "$REPLY" =~ ^[Ss]$ ]]; then
        rm -rfv $(locate $1)
    fi
}

ordenarfichero() {
    local archivo=$1
    sort --ignore-case "$archivo" -o "$archivo"
    echo "Fichero $archivo ordenado."
}

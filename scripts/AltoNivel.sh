#!/bin/bash

# Define la ruta del script de bajo nivel de forma más clara.
# Podrías usar una única variable para la ruta.
# Por ejemplo:
# SCRIPT_BAJO_NIVEL="$scripts/BajoNivel.sh"


# Abre la agenda de la terminal, pero la opción "web" abre adicionalmente la agenda web.



# Verifica si la variable $scripts está definida y si el archivo existe
if [[ -f "${scripts}/BajoNivel.sh" ]]; then
    source "${scripts}/BajoNivel.sh"
elif [[ -f "/home/tron/Scripts/BajoNivel.sh" ]]; then
    source "/home/tron/Scripts/BajoNivel.sh"
else
    echo "Error: No se encontró el script BajoNivel.sh en ninguna de las rutas." >&2
    exit 1
fi
# libreria que permite guardar las sesiones de chrome las pestañas abiertas

source /home/daniel/tron/programas/sesiones/sesiones/libsesiones.sh

# funcion para transcribir de videos


transcribir() {
  # Guarda el directorio de trabajo actual
  local ini="$PWD"

  # Cambia al directorio del script de Python
  cd /home/daniel/tron/programas/trans/

  # Ejecuta el script de Python
  python3 descargaa.py

  # Regresa al directorio original
  cd "$ini"

  # La variable 'ini' se elimina automáticamente al finalizar la función
} 

## Funciones de Manejo de Apagado

on() {
    sudo shutdown -c
    # Utiliza un código de retorno para saber si el comando fue exitoso
    if [[ $? -eq 0 ]]; then
        echo -e "\n✅ Apagado cancelado con éxito."
    else
        echo -e "\n❌ No hay un apagado programado para cancelar."
    fi
}

off() {
    read -p "¿Cuántos minutos apagar? (ej: 180 para 3 horas): " tiempo
    # Usa una expresión regular más segura para validar la entrada
    if [[ "$tiempo" =~ ^[0-9]+$ ]]; then
        read -p "¿Apagar pantalla inmediatamente? (s/n): " -n 1 -r
        echo # Salto de línea después de la respuesta
        
        if [[ "$REPLY" =~ ^[Ss]$ ]]; then
            sudo shutdown +$tiempo "Apagado programado en $tiempo minutos"
            xset dpms force off
            echo -e "\n✅ Apagado programado en $tiempo minutos y pantalla apagada."
        else
            sudo shutdown +$tiempo "Apagado programado en $tiempo minutos"
            echo -e "\n✅ Apagado programado en $tiempo minutos."
        fi
    else
        echo "❌ Error: Debe ingresar un número de minutos."
    fi
}

perfiles(){
    for profile in ~/.config/google-chrome/{Default,Profile*}/; do   pref="$profile/Preferences";   if [ -f "$pref" ]; then     name=$(jq -r '.profile.name // "N/A"' "$pref" 2>/dev/null);     email=$(jq -r '.account_info[0].email // "N/A"' "$pref" 2>/dev/null);     printf "\n\033[1;34mRuta:\033[0m\t%s\n\033[1;32mNombre del Perfil:\033[0m\t%s\n\033[1;33mCorreo:\033[0m\t%s\n" "$profile" "$name" "$email";   fi; done
 echo
 echo
 echo "Funcion perfiles en AltoNivel"   		
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
	ini=$PWD
	cd ~/tron/programas/sincroDrive
	./sincroDri.sh
	cd "$ini"
}	

colores () {
    source $scripts/lib/libcolores/libcolores.sh
    tablacoloresbash
}

#vlc () {
   # playerctld daemon
    #inicio=$PWD
    #cd "/home/$usuario/tron/plugins/AppImage"
    #./VLC_media_player-3.0.11.1-x86_64.AppImage --qt-continue=2 $1
    #cd $inicio   
#}

sinoestainiciado () {
	
	
	# Función para verificar si la terminal de XFCE está en ejecución
	is_terminal_running() {
		
	    if [[ -n $(pgrep $1) ]]; then
	        return 0
	    else
	        return 1
	    fi
	}
	
	# Verificar si la terminal de XFCE está en ejecución
	if is_terminal_running "$1"; then
	    echo "No se ejecutará $1,  ya está en ejecución."
	else
	    echo "$1  no está en ejecución. Iniciando $1..."
	    $1 &
	fi
	
}

sincro () {
    usuario=${SUDO_USER:-${USER}}
    inicio=$PWD
    cd "/home/$usuario/tron/plugins/syncthing-linux-amd64-v1.23.4"
    ./syncthing
    
    cd $inicio   
}
    
sincro-serve ()
{
/usr/bin/syncthing serve --no-browser --logfile=default &
disown
fire http://127.0.0.1:8384

}



abrirgestordb () {

    ini=$PWD
    clear
    cd $plugins/AppImage/sqlite
    echo "Presione 1 para  Dbgate, y 2 con Antares"
    read op
    if [[ $op == 1 ]]; then
        # setsid desvincula el proceso de la terminal
        setsid ./dbgate-latest.AppImage  1>/dev/null 2>/dev/null
    fi
    if [[ $op == 2 ]]; then
        setsid ./Antares-0.7.0-linux_x86_64.AppImage 1>/dev/null 2>/dev/null
    fi
        
    cd $ini
    unset ini 
}

sqlite-ver () {

    ini=$PWD
    clear
    echo
    echo "Ingresa el nombre de la base de datos:"
    db=$(ruta "$data/sqlite")
        
    cd $plugins/SQLiteStudio
        # setsid desvincula el proceso de la terminal
        setsid ./sqlitestudio $db   1>/dev/null 2>/dev/null
    cd $ini
    unset ini db
}


systemctl-reboot () {
    unid=$1
    systemctl disable $unid
    systemctl daemon-reload $unid
    systemctl enable $unid
    systemctl start $unid
    systemctl status $unid
    echo
    echo
    echo "Ver el log? 1 para si"
    read resp
    if [[ $resp == 1 ]]; then
        journalctl -xeu $unid
    fi 
    
    
}

git-res () {
	cd /home/$usuario/tron
	merideam=`date +"%p"`
	respaldo=respaldo_$(date +%d%b%Y%a%Ih%Mm%Ss)-$merideam
	git config --global user.email "elprofesorverdad@gmail.com"
  	git config --global user.name "EliasHung"
	if [[ -z $1 ]]; then
		git commit -am "$respaldo"
	else
		res=$1-$respaldo
		git commit -am "$res"	
	fi
	
	
	git push -u origin main
}

dlna () {
    usuario=${SUDO_USER:-${USER}}
#	dlna-reset
	sudo mkdir -v /media/$usuario/medios
	sudo mkdir -v /home/$usuario/Vídeos/medios
	sudo chown -vf $usuario:$usuario /home/$usuario/Vídeos/medios
	sudo chown -vf $usuario:$usuario /home/$usuario/Vídeos/
    sudo chown -vf $usuario:$usuario /media/$usuario/medios/medios
    sudo chmod 775 /media/$usuario/medios/medios
    sudo chmod 775 /home/$usuario/Vídeos/medios
	sudo mount -v /dev/sdb5 /media/$usuario/medios 
	sudo mount --bind -v /media/$usuario/medios/medios /home/$usuario/Vídeos/medios
	
	sleep 8
	sudo -u $usuario rygel
#	sudo service minidlna start
#	dlna-status	
}


dlna-off () {
    usuario=${SUDO_USER:-${USER}}
	#sudo service minidlna stop
	rygel --shutdown
	sudo umount -vlf /home/$usuario/Vídeos/medios/medios
	sudo umount -vlf /home/$usuario/Vídeos/
	sudo umount -vlf /media/$usuario/medios
	sudo umount -vlf /home/$usuario/s/sdb5/medios
	sudo umount -vlf /home/$usuario/Vídeos/medios
	sudo umount -lf /media/$usuario/medios 
	sudo umount -lf /media/$usuario/s/sdb5

	
}


dlna-reset () {
sudo service minidlna force-reload
sudo service minidlna restart
}

dlna-status () {
	sudo service minidlna status
}



crearentorno () {
    inicio=$PWD
    cd $plugins/python/entornos
    echo "Ingrese el nombre del entorno"
    read nombre
    #mkdir $nombre
    #cd "$plugins/python/entornos/$nombre"
    virtualenv $nombre
    cd $inicio
}

# Activa un entorno env python existente
# $1 cadena que indica el nombre de del entorno a ser activado
# sino recibe $1 entonces pregunta que entorno activar
activarentorno () {
    aux=$PWD
        
    cd $plugins/python/entornos
    echo
    
    if [[ -z $1 ]]; then
        ls
        echo
        echo "¿Que entorno desea activar?"
        read nombre
        cd $PWD/$nombre
    else
        cd $PWD/$1
    fi
    cd bin
    var="source activate"
    eval "$var"
    cd $PWD
        
    }

sshGit () {
        echo "ver mi llave ssh"
        eval $(ssh-agent -s)

        echo "crear la llave ssh para git"
        echo "ingrese el correo de git"
        echo "puede ser elias1hung@gmail.com"
        read correo

        ssh-keygen -t ed25519 -C $correo 

        echo "agregar la llave al servicio de llaves"
        ssh-add ~/.ssh/id_ed25519

        echo 'la llave esta guardada en  ~/.ssh/id_ed25519.pub'

        echo "mostrando el contenido de la llave"  
        cat ~/.ssh/id_ed25519.pub

        echo "esa llave es la que se coloca en el sitio web de git"
}


DeshabilitarAhorroEnergiaNetworkManager () {

#NM_SETTING_WIRELESS_POWERSAVE_DEFAULT (0): utilice el valor predeterminado
#NM_SETTING_WIRELESS_POWERSAVE_IGNORE (1): no toque la configuración existente
#NM_SETTING_WIRELESS_POWERSAVE_DISABLE (2): deshabilitar ahorro de energía
#NM_SETTING_WIRELESS_POWERSAVE_ENABLE (3): habilitar ahorro de energía
sudo sed -i 's/wifi.powersave = 3/wifi.powersave = 2/' /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf || systemctl restart network-manager.service
echo
echo El ahorro de energia Network MAnager es:
cat /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf


}




installBash () {
usuario=${SUDO_USER:-${USER}}
# NOTA: Al modificar esta funcion debes modificar
# la funcion installBash del script de mudanza
inicio=$PWD
cd /home/$usuario
sudo rm -v /etc/.bashrc; sudo rm -v /etc/.bash.bashrc; sudo rm -v /root/.bashrc; sudo rm -v /home/.bash.bashrc; sudo rm -v /home/$usuario/.bash.bashrc; sudo rm -v /home/.bash.bashrc
sudo rm -v /etc/.bashrc; sudo rm -v /etc/.bash.bashrc; sudo rm -v /root/.bashrc; sudo rm -v /home/.bashrc; sudo rm -v /home/$usuario/bashrc; sudo rm -v /home/.bash.bashrc

# en /home
sudo cp -a -p -f -v /home/$usuario/tron/plugins/bash/bash.bashrc /home/.bashrc
sudo cp -a -p -f -v /home/$usuario/tron/plugins/bash/bash.bashrc /home/$usuario/.bashrc
sudo cp -a -p -f -v /home/$usuario/tron/plugins/bash/bash.bashrc /home/.bash.bashrc
sudo chown  -v root:root /home/.bashrc; sudo chmod  -v 744 /home/.bashrc
sudo chown  -v root:root /home/.bash.bashrc; sudo chmod  -v 744 /home/.bash.bashrc
sudo chown  -v root:root /home/.bashrc; sudo chmod  -v 744 /home/$usuario/.bashrc

# en /etc
sudo cp -a -p -f -v /home/$usuario/tron/plugins/bash/bash.bashrc /etc/.bashrc
sudo cp -a -p -f -v /home/$usuario/tron/plugins/bash/bash.bashrc /etc/.bash.bashrc
sudo chown  -v root:root /etc/.bashrc; sudo chmod  -v 744 /etc/.bashrc
sudo chown  -v root:root /etc/.bash.bashrc; sudo chmod  -v 744 /etc/.bash.bashrc

# para el usuario root
sudo cp -a -p -f -v /home/$usuario/tron/plugins/bash/bash.bashrc /root/.bashrc
sudo cp -a -p -f -v /home/$usuario/tron/plugins/bash/bash.bashrc /root/.bash.bashrc
sudo chown  -v root:root /root/.bashrc; sudo chmod  -v 744 /root/.bashrc
sudo chown  -v root:root /root/.bash.bashrc; sudo chmod  -v 744 /root/.bash.bashrc


source .bashrc
#ln -v -f /home/$usuario/tron/plugins/bash/* $Scripts/
cd $inicio
}





LevantarStreamingAudio () {
cuentafinal 2 "lista de fuentes de audio"
pactl list sources short
cuentafinal 2 "Desbloqueando Firewal"
sudo ufw allow 12345/tcp
cuentafinal 2 "'Ejecutando pactl load-module module-detect'"
pactl load-module module-detect
sleep 8
cuentafinal 2 "Reiniciando el Audio"
pulseaudio -k
sleep 8
pulseaudio --start 
sleep 8
pulseaudio --start 
pulseaudio --start 
sleep 8
pulseaudio --start 

}

streamingAudio () {

sudo echo "load-module module-simple-protocol-tcp source=0 record=true port=12346" >> /etc/pulse/default.pa
sudo -u $usuario pulseaudio -k
echo esperando comando...
sleep 8
sudo -u $usuario pulseaudio --start

}

instalaraudio () {
    streamingAudio
    LevantarStreamingAudio    
}


configurafirewall () {


cuentafinal 2 "CONFIGURANDO EL FIREWALL"
#CONFIGURANDO EL FIREWALL
ufw enable
#  ufw allow Apache
ufw allow OpenSSH
# ufw allow 8245/tcp

ufw allow ssh
service ufw restart
}




correo () {
    #Programa para recibir
    #el correo de el telefono desde
    #la bandeja de salida del mismo
    #en la carpetad destino
    #autor: Elias hung
    #elprofesorverdad@gmail.com
    #
    #
    desktop=$(xdg-user-dir DESKTOP)
    if [[ ! -d $desktop/BandejadeEntrada ]]; then
        mkdir $desktop/BandejadeEntrada
       
    fi
    if [[ ! -d $desktop/BandejadeSalida ]]; then
        mkdir $desktop/BandejadeSalida
        
    fi
    
    
    respaldo="/home/$usuario/respaldo"
    salidaTelefono="/sdcard/A1BandejaDeSalida"
    entradaCompu="$desktop/BandejadeEntrada"
    entradaTelefono="/sdcard/A1BandejaDeEntrada"
    salidaCompu="$desktop/BandejadeSalida"
    #
    salidaTelefonoPelis="/sdcard/A1pelis"
    entradaCompuPelis="/mnt/sdc"
    #entradaTelefonoPelis="sdcard/A1BandejaDeEntrada"
    #salidaCompuPelis="/home/$usuario/Escritorio/PARA_EL_TELEFONO"

    if [[ -z $1  ]];
    then
			    echo por favor mi usuario: $usuario elija una opción válida
			    echo opción 'ern' para enviar y recibir y abrir el navegador de archivos
			    echo opción 'r' Solo recibir
			    echo opción 'e' Solo enviar
			    echo opcion 'r2' Recibir documentos y películas
			    echo opción 'pd' Películas Descargar
			    echo "**********OPCIONES PARA PELICULAS***********"
    #	echo opción '-ps' Películas Subir
    else
	    adb start-server
	    case $1 in
		    "ern")
			    adb pull "$salidaTelefono" "$entradaCompu"
			    adb push "$salidaCompu" "$entradaTelefono"
			    thunar $entradaCompu
		    ;;
		    "e")
			    
			    adb push "$salidaCompu" "$entradaTelefono" 
		    ;;
		    "r")
			    adb pull "$salidaTelefono" "$entradaCompu"
   			    thunar $entradaCompu

		    ;;
		    #"-ps")
		    #	adb push "$salidaCompuPelis"/* "$entradaTelefonoPelis" 
    #		;;
		    "pd")
			    adb pull "$salidaTelefonoPelis" "$entradaCompuPelis"
		    ;;
		    "r2")
			    adb pull "$salidaTelefonoPelis" "$entradaCompuPelis"
			    adb pull "$salidaTelefono" "$entradaCompu"
		    ;;
		    *)
			    echo por favor mi usuario: $usuario elija una opción válida
			    echo opción 'ern' para enviar y recibir y abrir el navegador de archivos
			    echo opción 'r' Solo recibir
			    echo opción 'e' Solo enviar
			    echo opcion 'r2' Recibir documentos y películas
			    echo opción 'pd' Películas Descargar
			    echo "**********OPCIONES PARA PELICULAS***********"
			    
				    
		    ;;
	    esac 
    fi
adb kill-server
}


correow () {
    usuario=${SUDO_USER:-${USER}}
    echo "Conecta el celular con el cable USB y Presiona Enter"
    read soncabezon
    unset soncabezon
    adb tcpip 5555

    desktop=$(xdg-user-dir DESKTOP)
    entradaCompu="$desktop/BandejadeEntrada"
    salidaCompu="$desktop/BandejadeSalida"
    entradaCompuPelis="/mnt/sdc"
    salidaTelefono="/sdcard/A1BandejaDeSalida"
    entradaTelefono="/sdcard/A1BandejaDeEntrada"
    salidaTelefonoPelis="/sdcard/A1pelis"

    if [[ -z $1 ]]; then
        echo "Por favor, seleccione una opción válida:"
        echo "Opción 'ern' para enviar y recibir y abrir el navegador de archivos"
        echo "Opción 'r' para solo recibir"
        echo "Opción 'e' para solo enviar"
        echo "Opción 'r2' para recibir documentos y películas"
        echo "Opción 'pd' para descargar películas"
        echo "********** OPCIONES PARA PELÍCULAS ***********"
    else
        adb start-server
        echo "Conectándose a la dirección IP del teléfono 172.16.0.150:38949"
        adb connect 172.16.0.150:38949
        case $1 in
            "ern")
                adb pull "$salidaTelefono" "$entradaCompu"
                adb push "$salidaCompu" "$entradaTelefono"
                thunar $entradaCompu
                ;;
            "e")
                adb push "$salidaCompu" "$entradaTelefono"
                ;;
            "r")
                adb pull "$salidaTelefono" "$entradaCompu"
                thunar $entradaCompu
                ;;
            "pd")
                adb pull "$salidaTelefonoPelis" "$entradaCompuPelis"
                ;;
            "r2")
                adb pull "$salidaTelefonoPelis" "$entradaCompuPelis"
                adb pull "$salidaTelefono" "$entradaCompu"
                ;;
            *)
                echo "Por favor, seleccione una opción válida:"
                echo "Opción 'ern' para enviar y recibir y abrir el navegador de archivos"
                echo "Opción 'r' para solo recibir"
                echo "Opción 'e' para solo enviar"
                echo "Opción 'r2' para recibir documentos y películas"
                echo "Opción 'pd' para descargar películas"
                echo "********** OPCIONES PARA PELÍCULAS ***********"
                ;;
        esac
    fi
    adb disconnect 172.16.0.150:38949
    adb kill-server
}


hardware ()
{
echo INFORMACION DE HARDWARE
echo
echo Cómo verificar la información sobre el
echo hardware en Linux
echo
echo Comando lscpu – Procesamiento
echo lshw – Lista de hardware en Linux

echo hwinfo – Información del hardware en 
echo Linux
echo lspci – Lista PCI
lspci
echo lsscsi – Listar dispositivos scsi
lsscsi
echo lsusb – Lista de los buses usb y 
echo detalles del 
echo dispositivo
lsusb

echo lsblk – Lista de dispositivos de bloque
lsblk
echo df – espacio en disco de los sistemas de archivos
df
echo Pydf – Python df

echo free – Verifica la RAM
free

}




imagenInformacion ()
{

 	if [[ -z $1 ]];
	then
		#ruta=$PWD
		echo Error: Ingrese la ruta completa de la Imagen desde la raiz
		
	else
		ruta=$1
		echo "# PROGRAMA ELABORADO POR ELIAS HUNG"  >> infoima
		echo "# MUESTRA LA INFORMACION DE UNA IMAGEN"  >> infoima
		echo "#" >> infoima
		echo "#" >> infoima
		echo "#" >> infoima
		echo VALORES POR IMAGEMAGICK >> infoima 
			echo >> infoima
			echo >> infoima
			identify -verbose $ruta >> infoima 2>&1
			echo >> infoima
			echo >> infoima
		echo VALORES POR FILE >> infoima
			echo >> infoima
			echo >> infoima
			file $ruta >> infoima 2>&1
			echo >> infoima
			echo >> infoima
		echo VALORES POR EXIF >> infoima
			echo >> infoima
			echo >> infoima
			exif $ruta >> infoima 2>&1
			echo >> infoima
			echo >> infoima
		editar infoima
	fi
		rm infoima >> infoima 2>&1
	
 	
 	
 }
 
troncontanque ()
{

#el antivirus Escanea la carpeta pasada como argumento
# comprueba si se ha pasado la ruta como argumentu si el argumento es vacio se toma la ruta actual
if [[ -z $1 ]];
then
	ruta=$PWD
else
	ruta=$1
fi

echo "presione 1 solo solo analizar los archivos y 2 para analizar y borrar los virus"
read frase

case $frase in
  1)
    clamscan -r  -v -a $ruta
  ;;
  2)
    clamscan --infected --remove --recursive  -v -a $ruta
 ;;
esac
       
 }


 analizar ()
 {
 	#el antivirus Escanea la carpeta pasada como argumento
 	# comprueba si se ha pasado la ruta como argumentu si el argumento es vacio se toma la ruta actual
	if [[ -z $1 ]];
	then
  		ruta=$PWD
	else
		ruta=$1
 	fi
  
   	# 

       #
       #alert $ruta
	yad --title="ASISTENTE: SR HUNG" \
    	--center \
    	--width=500 \
    	--height=80 \
    	--text-align=center \
        --button=Si:0 \
        --button=No:1 \
    	--text="¿Desea Seguro desea Analizar: $ruta ?"
	ans=$?

	if [ $ans -eq 0 ]
	then

		yad --title="ASISTENTE: SR HUNG" \
    		--center \
    		--width=500 \
    		--height=80 \
    		--text-align=center \
       		 --button=SoloEscanear:0 \
        	--button=EliminarArchivosInfectados:1 \
    		--text="¿Desea Solo Escanear O Escanear y Eliminar Amenazas en  $ruta ?"
		ans=$?

		if [ $ans -eq 0 ]
		then
    		
                	clamscan -r  -v -a --log=/home/logAntivirus.txt $ruta
		else
    			clamscan --infected --remove --recursive  -v -a --log=/home/logAntivirus.txt $ruta
		fi

	else
    		return 0
	fi
       
 } 
 



